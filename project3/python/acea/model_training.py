from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pickle

from .visualisation import make_timeseries_plot
from .data_loaders import get_batch, get_custom_batch
from .model_evaluation import evaluation_metrics

def batch_training(X, y, dates, regressor, reg_name, train_period=None, test_period=None, name=None):
    if train_period and test_period:
        batches = get_custom_batch(X, train_period, test_period)
    else:
        batches = get_batch(X)

    scores = []

    all_dates = []
    all_ytest = []
    all_ypred = []
    for i, j, k in batches:

        # dates fold
        dates_fold = dates[j:k]

        # get train-test sets
        X_train, X_test = X[i:j], X[j:k]
        y_train, y_test = y[i:j], y[j:k]

        # scale data
        Xscaler = MinMaxScaler()
        yscaler = MinMaxScaler()
        X_train_scaled = Xscaler.fit_transform(X_train)
        y_train_scaled = yscaler.fit_transform(y_train)
        X_test_scaled = Xscaler.transform(X_test)
        y_test_scaled = yscaler.transform(y_test)

        y_train_scaled = y_train_scaled.ravel()

        # fit model
        regressor.fit(X_train_scaled, y_train_scaled)

        # predict
        y_pred_scaled = regressor.predict(X_test_scaled)
        if len(y_pred_scaled.shape) == 1:
            y_pred_scaled = np.expand_dims(y_pred_scaled, axis=0)
        y_pred = yscaler.inverse_transform(y_pred_scaled).squeeze()

        # model evaluation
        model_scores = evaluation_metrics(y_test, y_pred)
        scores.append(model_scores)

        # model_evaluation_plots(dates[j:k], y_test, y_pred)
        if name:
            all_dates.append(dates_fold)
            all_ytest.append(y_test)
            all_ypred.append(y_pred)

    if name:
        pickle.dump({'dates': all_dates, 'y_test': all_ytest, 'y_pred': all_ypred},
                    open('results/%s_%s.p' % (name, reg_name), 'wb'))

        make_timeseries_plot(all_dates, all_ytest, all_ypred, name, reg_name)

    return scores

def get_scores_regressors(df, reg_names, regressors, train_period=None, test_period=None, echo=False, name=None,
                          target=None, features=None):
    dates = df['Date'].values

    y = df.drop(columns='Date').iloc[:, [0]].values
    X = df.drop(columns='Date').iloc[:, 1:].values
    scores = {}

    if X.shape[1] == 0:
        print('No features. Skipping!')
        return {}

    for reg_name, regressor in zip(reg_names, regressors):

        if echo:
            print('## processing', reg_name)

        scores[reg_name] = batch_training(X, y, dates, regressor, reg_name, train_period=train_period,
                                          test_period=test_period, name=name)

    return scores