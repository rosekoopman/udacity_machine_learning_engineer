import pandas as pd

def scores_to_dataframe(scores):
    scores_list = []
    for reg_name in scores.keys():
        dftmp = pd.DataFrame(scores[reg_name])
        dftmp['reg_name'] = reg_name
        scores_list.append(dftmp)
    dfscores = pd.concat(scores_list)

    return dfscores


def select_period(df):
    if 'Date' in df.columns:
        df = df[df['Date'] >= '2015-01-01']
    else:
        df = df.loc['2015-01-01':]

    return df


def format_scores(dfscores, method):
    dfscores = dfscores.groupby('reg_name').agg(['mean', 'std']).unstack().unstack(level=1)
    dfscores = dfscores.reset_index().rename(columns={'level_0': 'metric'})
    dfscores['method'] = method
    return dfscores


def get_best_model(all_scores, all_methods, name, echo=False):
    scores_list = []

    for dfscores_method, method in zip(all_scores, all_methods):
        try:
            scores_list.append(format_scores(dfscores_method[name], method))
        except KeyError:
            pass

    dfall = pd.concat(scores_list).reset_index(drop=True)

    ibest_r2 = dfall[dfall['metric'] == 'r2']['mean'].idxmax()
    ibest_rmse = dfall[dfall['metric'] == 'rmse']['mean'].idxmin()

    result = pd.concat([dfall.loc[[ibest_r2]], dfall.loc[[ibest_rmse]]])

    if echo:
        print(result)

    return result


