import pandas as pd

from .configuration import FORECAST_PERIOD

def clean_data(dfclean, date_min, date_max, drop_cols=[], replace_cols=[], rename_cols={}, offsets=[]):
    # select time range and make sure there is a record for each day
    dfclean = pd.merge(pd.DataFrame(index=pd.date_range(date_min, date_max)),
                       dfclean.set_index('Date'),
                       left_index=True,
                       right_index=True,
                       how='left')

    # rename columns
    dfclean.rename(columns=rename_cols, inplace=True)

    # drop columns
    dfclean.drop(columns=drop_cols, inplace=True)

    # set dtype
    for c in dfclean.columns:
        dfclean[c] = dfclean[c].astype(float)

    # fix data offsets
    for col, offset, loc_min, loc_max in offsets:
        dfclean.loc[loc_min:loc_max, col] = dfclean.loc[loc_min:loc_max, col] + offset

    # replace invalid values by NaN
    for c, values in replace_cols:
        dfclean[c] = dfclean[c].replace(*values)

    # interpolate data (if only 1 subsequent value is missing)
    for c in dfclean.columns:
        dfclean[c] = dfclean[c].interpolate(method='time', limit=1)

    # all flow columns must have positive values
    for c in dfclean.filter(regex='^Flow_Rate').columns:
        dfclean[c] = dfclean[c].abs()

    dfclean.reset_index(inplace=True)
    dfclean.rename(columns={'index': 'Date'}, inplace=True)

    print('shape', dfclean.shape)

    return dfclean


def get_lagged_value(df, targets, regex, replace_str, shortname, n, period=30, avg=True, difference=True, wrt='nmin1'):
    min_periods = int(period * 0.66)

    if period == 30:
        pname = 'm'  # month
    elif period == 7:
        pname = 'w'  # week
    else:
        print('Error: period not valid')
        raise

    if avg:
        vname = 'avg'
    else:
        vname = 'sum'

    for col in df.filter(regex=regex):

        if col in targets:
            continue

        # location
        if replace_str != 'auto':
            location = col.replace(replace_str, '')[:4]
        else:
            location = col[-8:]

        # create summed features per period
        drop_cols = []
        for ni in range(1, n + 1):

            # calculate the avg in period n
            col_n = '%s_%s_%d%s_%s' % (shortname, vname, ni, pname, location)
            if ni == 1:
                df[col_n] = df[col].rolling(window=period * ni, min_periods=min_periods).sum()
            else:
                df[col_n] = df[col].rolling(window=period * ni, min_periods=min_periods).sum() - df[col].rolling(
                    window=period * (ni - 1), min_periods=min_periods).sum()

            if avg:
                df[col_n] = df[col_n] / period

            if difference:
                # calculate the difference with respect to the previous period

                if ni > 1:

                    # define colnames
                    col_d = '%s_d%s_%d%s_%s' % (shortname, vname, ni, pname, location)
                    if wrt == 'nmin1':
                        col_nmin1 = '%s_%s_%d%s_%s' % (shortname, vname, ni - 1, pname, location)
                    elif wrt == '1':
                        col_nmin1 = '%s_%s_%d%s_%s' % (shortname, vname, 1, pname, location)
                    else:
                        print('Error: invalid choice for wrt', wrt)
                        raise

                    # calculate difference
                    df[col_d] = df[col_nmin1] - df[col_n]

                    # drop column used to calculate difference
                    drop_cols.append(col_n)

        # drop column in case difference is used (if not used the list will be empty)
        # df.drop(columns=drop_cols, inplace=True)

    return df


#     return df

def get_avg_features(df, cols_to_avg_list):
    for cols, colname in cols_to_avg_list:
        df[colname] = df[cols].mean(axis=1)

    return df


def get_window_features(df, targets):
    for target in targets:
        df['span2_%s' % target] = df['target'].ewm(span=2).mean()


def create_features(df, targets, nperiods, cols_to_avg_list, cols_to_drop_list, difference=True):
    # create month feature
    df['month'] = df['Date'].dt.month
    df = pd.get_dummies(df, columns=['month'], prefix='month')
    df.set_index('Date', inplace=True)

    # shift all columns apart from the target solumns with the FORECAST PERIOD
    for c in set(df.columns) - set(targets) - set([c for c in df.columns if 'month' in c]):
        df[c] = df[c].shift(FORECAST_PERIOD)

    # create autocorrelation feature -- this is based on 1 datapoint so this is sensitive to statistical fluctuations!
    for c in targets:
        df['auto_%s' % c] = df[c].shift(FORECAST_PERIOD)

    # average columns with high correlation
    # replace any columns which is also a target with the respective 'auto_' column, to make sure to take the shifted data!
    for avg_list in cols_to_avg_list:
        avg_list[0] = ['auto_%s' % c if c in targets else c for c in avg_list[0]]
    # get average values
    df = get_avg_features(df, cols_to_avg_list)

    # drop columns we do not need anymore (for instance because combined in previous step)
    # note that we cannot throw away column directly in previous step because in some cases targets and features are
    # combined
    df = df.drop(columns=cols_to_drop_list)

    ### get lagged rainfall features -- weeks
    regex = '^avg_Rainfall'
    replace_str = 'avg_Rainfall_'
    shortname = 'ar'
    df = get_lagged_value(df, targets, regex, replace_str, shortname, nperiods, period=7, avg=False,
                          difference=difference)

    ### get lagged features -- months (difference with n-1 value)
    cols = [['^Depth_to_Groundwater', 'Depth_to_Groundwater_', 'd'],
            ['^avg_Depth_to_Groundwater', 'avg_Depth_to_Groundwater_', 'ad'],
            ['^Temperature', 'Temperature_', 't'],
            ['^avg_Temperature', 'avg_Temperature_', 'at'],
            ['^Hydrometry', 'Hydrometry_', 'h'],
            ['^avg_Hydrometry', 'avg_Hydrometry_', 'ah'],
            ['^Volume', 'Volume_', 'v'],
            ['^avg_Volume', 'avg_Volume_', 'av'],
            # ['^Flow_Rate', 'Flow_Rate_', 'f'],
            # ['^auto', 'auto', 'a']
            ]

    for col in cols:
        df = get_lagged_value(df, targets, *col, nperiods, period=30, avg=True, difference=True, wrt='nmin1')

    ### get lagged features -- months (difference with current value)
    cols = [['^auto', 'auto', 'a']
            ]

    for col in cols:
        df = get_lagged_value(df, targets, *col, 6, period=30, avg=True, difference=False)

    df = df.dropna()

    return df



