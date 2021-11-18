import pandas as pd
import numpy as np

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

import matplotlib.pyplot as plt

from .data_loaders import get_batch, get_custom_batch
from .models import BaseModel



def evaluation_metrics(y_true, y_pred, save_name=False):

    """
    Determine model evaluation scores.

    Optionally the model scores can be saved in a csv file. To use this option, provide a filename using the
    argument save_name, eg my_model_scores.csv

    :param y_true: true values (list, array or pd.Series)
    :param y_pred: predicted values (list, array or pd.Series)
    :param save_name: filename to save model scores (str)
    :return: distionary with model scores
    """
    scores = {'r2': r2_score(y_true, y_pred),
              'rmse': mean_squared_error(y_true, y_pred),
              'mae': mean_absolute_error(y_true, y_pred),
              'mape': mean_absolute_percentage_error(y_true, y_pred)}

    if save_name:
        pd.DataFrame(scores, index=[0]).to_csv('../model_scores/%s' % save_name, index=False)

    return scores


def model_evaluation_plots(x, y_true, y_pred, save_name=False):

    """
    Create model evaluation plot for visual inspection of model performance

    Optionally the figures can be saved as both pdf and png file. To use this option, provide a filename using
    the argument save_name. Note that you do not need to provide a file extention

    :param x: x value, e.g. dates in the case of timeseries (list or array)
    :param y_true: true values (list or array)
    :param y_pred: predicted values (list or array)
    :param save_name: filename to save figures
    :return:
    """

    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(2, 2)

    fig.add_subplot(gs[0, :])
    plt.plot(x, y_true, marker='.', linestyle='', label='true')
    plt.plot(x, y_pred, marker='.', linestyle='', label='pred')
    plt.legend()

    fig.add_subplot(gs[1, 0])
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.xlabel('true value')
    plt.ylabel('predicted value')

    fig.add_subplot(gs[1, 1])
    diff = [t - p for t, p in zip(y_true, y_pred)]
    plt.hist(diff, bins=30)
    plt.xlabel('true - pred')
    plt.ylabel('N')

    if save_name:
        plt.savefig('../figs/%s.pdf' % save_name)
        plt.savefig('../figs/%s.png' % save_name)

    return


def get_scores_for_basemodel(df, target, train_period=None, test_period=None):
    feature = 'auto_' + target
    x = ['Date']

    y = df[[target]].values
    X = df[[feature]].values

    base_model = BaseModel()
    base_model_scores = []

    if train_period and test_period:
        batches = get_custom_batch(df, train_period, test_period)
    else:
        batches = get_batch(df)

    for i, j, k in batches:
        # get train-test sets
        X_train, X_test = X[i:j], X[j:k]
        y_train, y_test = y[i:j], y[j:k]

        # fit model
        base_model.fit(X_train, y_train)

        # predict
        y_pred = base_model.predict(X_test)

        # model evaluation
        base_model_scores.append(evaluation_metrics(y_test, y_pred))

    # get summary statistics of scores
    summary = pd.DataFrame(base_model_scores).agg(['mean', 'std']).T

    return summary, base_model_scores


