import re
import pandas as pd
import matplotlib.pyplot as plt

def make_timeseries_plot(dates, y_tests, y_preds, name, reg_name):
    title = re.sub('D\d+_', '', name)
    title = re.sub('pearson_|phik_|pps_', '', title)
    body = ' '.join(title.split('_')[:2])
    target = ' '.join(title.split('_')[2:])
    title = '%s - %s (%s)' % (body, target, reg_name)

    n = len(dates[0])
    x = [v for sublist in dates for v in sublist]
    y_test = [v for sublist in y_tests for v in sublist.reshape(1, 30).squeeze()]
    y_pred = [v for sublist in y_preds for v in sublist]

    first_dates = [d[0] for d in dates] + [dates[-1][-1]]

    dfres = pd.DataFrame({'date': x,
                          'true': y_test,
                          'pred': y_pred})

    dfres.set_index('date').plot(marker='.', linestyle='', figsize=(10, 3.5))
    for d in first_dates:
        plt.axvline(d, color='gray', alpha=0.5)
    plt.ylabel(target)
    plt.xlabel('Time')
    plt.title(title)
    plt.tight_layout()

    plt.savefig('figs/%s_%s.pdf' % (name, reg_name))

    return


def compare_regressor_scores(dfscores, dfbasescores, suptitle=None, figname='', save=False):
    fig = plt.figure(figsize=(15, 8))

    fig.add_subplot(2, 2, 1)
    for reg_name in dfscores['reg_name'].unique():
        dfscores[dfscores['reg_name'] == reg_name]['r2'].plot(label=reg_name)
    dfbasescores['r2'].plot(label='basemodel', linewidth=4, linestyle=':', color='black')
    plt.legend()
    plt.title('R2')
    plt.xlabel('fold')

    fig.add_subplot(2, 2, 2)
    for reg_name in dfscores['reg_name'].unique():
        dfscores[dfscores['reg_name'] == reg_name]['rmse'].plot(label=reg_name)
    dfbasescores['rmse'].plot(label='basemodel', linewidth=4, linestyle=':', color='black')
    plt.legend()
    plt.title('RMSE')
    plt.xlabel('fold')

    fig.add_subplot(2, 2, 3)
    for reg_name in dfscores['reg_name'].unique():
        dfscores[dfscores['reg_name'] == reg_name]['mae'].plot(label=reg_name)
    dfbasescores['mae'].plot(label='basemodel', linewidth=4, linestyle=':', color='black')
    plt.legend()
    plt.title('MAE')
    plt.xlabel('fold')

    fig.add_subplot(2, 2, 4)
    for reg_name in dfscores['reg_name'].unique():
        dfscores[dfscores['reg_name'] == reg_name]['mape'].plot(label=reg_name)
    dfbasescores['mape'].plot(label='basemodel', linewidth=4, linestyle=':', color='black')
    plt.legend()
    plt.title('MAPE')
    plt.xlabel('fold')

    if suptitle:
        plt.suptitle(suptitle)

    plt.tight_layout()

    if save:
        plt.savefig('figs/%s.pdf' % (figname))

    return