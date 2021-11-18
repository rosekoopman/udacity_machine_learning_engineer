import pandas as pd
import numpy as np


def create_latex_score_table(dfscores, filename, echo=False):
    dfscores = dfscores.groupby('reg_name').agg(['mean', 'std']).unstack().unstack(level=1)

    if echo:
        r2_max = \
        dfscores.reset_index().pivot_table(index='reg_name', columns='level_0', values='mean', aggfunc='first')[
            'r2'].idxmax()
        rmse_min = \
        dfscores.reset_index().pivot_table(index='reg_name', columns='level_0', values='mean', aggfunc='first')[
            'rmse'].idxmin()
        print('   r2/rmse :', r2_max, rmse_min)

    dfscores['latex'] = dfscores.apply(lambda x: '$ %.2f \\pm %.2f $' % (x['mean'], x['std']), axis=1)
    dfscores.reset_index(inplace=True)
    dfscores = dfscores.pivot_table(index='reg_name', columns='level_0', values='latex', aggfunc='first')
    dfscores.columns.name = ''
    dfscores = dfscores[['r2', 'rmse', 'mae', 'mape']]

    latex_table = dfscores.to_latex().replace('\\textbackslash pm', '\pm').replace('\$', '$')

    with open('results/%s.tex' % (filename), 'w') as f:
        for line in latex_table:
            f.write(line)

    return


def create_latex_score_summary(names, summary):
    lines = []
    for name in names:
        dfsum = summary[name].copy()
        dfsum = dfsum.T
        dfsum['r2'] = dfsum['r2'].apply(lambda x: np.sign(x) * np.inf if abs(x) > 1E6 else x)
        dfsum = dfsum.T
        dfsum[name] = dfsum.apply(lambda x: '$ %.2f \\pm %.2f $' % (x['mean'], x['std']), axis=1)
        lines.append(dfsum[[name]].T)

    dftable = pd.concat(lines)
    latextable = dftable.to_latex().replace('\\textbackslash pm', '\pm').replace('\$', '$')

    return latextable