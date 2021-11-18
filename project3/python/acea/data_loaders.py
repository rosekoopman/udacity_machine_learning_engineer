import numpy as np
import pandas as pd
from .configuration import FORECAST_PERIOD, TRAIN_PERIOD, TEST_PERIOD


def load_data(files):
    # initiate dict to store data
    dfs = {}

    for f in files:

        # get name of the water body from the filename
        database = f.split('\\')[-1].replace('.csv', '')

        # load the data
        df = pd.read_csv(f)

        # get start and end data of the data
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])

        # store data in dictionary by water body name
        dfs[database] = df

    return dfs

def load_raw_data(f):

    # load the data
    df = pd.read_csv(f)

    # drop rows for which all values are NaN
    df.dropna(how='all', axis=0, inplace=True)

    # get start and end data of the data
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

    return df

def get_batch(df):
    # note: forecast horizon is taken into account in feature engineering: features are  moved backwards with
    # forecast_period!
    n = int(np.floor((len(df) - TRAIN_PERIOD - FORECAST_PERIOD) / TEST_PERIOD))
    for i in range(n):
        train_start = i * TEST_PERIOD
        train_end = train_start + TRAIN_PERIOD
        test_end = train_end + TEST_PERIOD
        yield train_start, train_end, test_end


def get_custom_batch(df, train_period, test_period):
    n = int(np.floor((len(df) - train_period - FORECAST_PERIOD) / test_period))
    for i in range(n):
        train_start = i * test_period
        train_end = train_start + train_period
        test_end = train_end + test_period
        yield train_start, train_end, test_end