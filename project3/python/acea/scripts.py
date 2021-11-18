import pandas as pd

from .helpers import select_period, scores_to_dataframe, get_best_model
from .model_evaluation import get_scores_for_basemodel
from .model_training import get_scores_regressors
from .visualisation import compare_regressor_scores
from .report import create_latex_score_table

def train_and_compare_regressors(names, dfs, dfs_basemodel, reg_names, regressors, figname=None):
    scores_dict = {}
    summary_dict = {}
    basescores_dict = {}

    for name in names:

        print('#' * 20, 'Processing', name, '#' * 20)

        body = '_'.join(name.split('_')[:2])
        target = '_'.join(name.split('_')[2:])

        df = dfs[name]
        dfb = dfs_basemodel[body]

        df = select_period(df.copy())
        dfb = select_period(dfb.copy())

        summary, basemodel_scores = get_scores_for_basemodel(dfb, target, train_period=365 * 2, test_period=30)
        dfbasescores = pd.DataFrame(basemodel_scores)

        if figname:
            tmpname = figname + '_' + name
        else:
            tmpname = None

        regressor_scores = get_scores_regressors(df, reg_names, regressors, train_period=365 * 2, name=tmpname)

        if len(regressor_scores.keys()) > 0:
            dfscores = scores_to_dataframe(regressor_scores)
            compare_regressor_scores(dfscores, dfbasescores, suptitle=name.replace('_', ' '),
                                     figname=tmpname + '_folds', save=True)
            scores_dict[name] = dfscores

            basescores_dict[name] = dfbasescores
            summary_dict[name] = summary

    return summary_dict, scores_dict, basescores_dict

def get_best_models_df(all_scores, all_methods, metric='rmse', echo=False):

    names = all_scores[0].keys()

    best_models_dict = {}
    for name in names:
        print(name)
        best_models_dict[name] = get_best_model(all_scores, all_methods, name, echo=echo)

    best_model_list = []
    for name in best_models_dict.keys():
        df = best_models_dict[name]
        df['name'] = name
        best_model_list.append(df)
    dfbest = pd.concat(best_model_list)
    return dfbest[dfbest['metric'] == metric]

def create_latex_score_tables(scores_dict, filename, echo=False):
    for name in scores_dict.keys():

        if echo:
            print(name)

        create_latex_score_table(scores_dict[name], '%s_%s' % (filename, name), echo=echo)

    return