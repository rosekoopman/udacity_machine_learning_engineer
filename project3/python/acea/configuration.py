import numpy as np
import pandas as pd

FORECAST_PERIOD = 60
TRAIN_PERIOD = 365*2
TEST_PERIOD = 30

cleaning_config = {
    'Aquifer_Auser': {
        'drop_cols' : ['Temperature_Ponte_a_Moriano'],
        'replace_cols': [('Depth_to_Groundwater_COS', (0, np.nan)), ('Depth_to_Groundwater_SAL', (0, np.nan))],
        'rename_cols': {'Depth_to_Groundwater_CoS': 'Depth_to_Groundwater_COS'},
        'offsets': [('Hydrometry_Piaggione', 1.19, '2010-01-01', '2021-01-01')],
        'date_min': pd.to_datetime('2015-01-01'),
        'date_max': pd.to_datetime('2020-06-30')
    }
}

cols_to_avg_config = {
    'Aquifer_Auser': [
        [['Rainfall_Gallicano', 'Rainfall_Pontetetto',
         'Rainfall_Monte_Serra', 'Rainfall_Orentano', 'Rainfall_Borgo_a_Mozzano',
         'Rainfall_Piaggione', 'Rainfall_Calavorno', 'Rainfall_Croce_Arcana',
         'Rainfall_Tereglio_Coreglia_Antelminelli',
         'Rainfall_Fabbriche_di_Vallico'],
         'avg_Rainfall_area1'],
        [['Temperature_Orentano', 'Temperature_Monte_Serra',
         'Temperature_Lucca_Orto_Botanico'],
         'avg_Temperature_area1'],
        [['Depth_to_Groundwater_SAL', 'Depth_to_Groundwater_PAG',
         'Depth_to_Groundwater_COS', 'Depth_to_Groundwater_DIEC'],
         'avg_Depth_to_Groundwater_area1'],
        [['Hydrometry_Monte_S_Quirico', 'Hydrometry_Piaggione'],
         'avg_Hydrometry_area1'],
        [['Volume_POL', 'Volume_CC2'],
         'avg_Volume_POL_CC2_area1'],
        [['Volume_CSA', 'Volume_CSAL'],
         'avg_Volume_CSA_area1']
    ],
    'Aquifer_Petrignano' : [
        [['Temperature_Bastia_Umbra', 'Temperature_Petrignano'],
         'avg_Temperature_area1']
    ],
    'River_Arno': [
        [['Rainfall_Le_Croci', 'Rainfall_Cavallina', 'Rainfall_S_Agata',
          'Rainfall_Mangona', 'Rainfall_S_Piero'],
        'avg_Rainfall_area1'],
    ],
    'Lake_Bilancino': [
        [['Rainfall_S_Piero', 'Rainfall_Mangona', 'Rainfall_S_Agata',
          'Rainfall_Cavallina', 'Rainfall_Le_Croci', 'Temperature_Le_Croci'],
         'avg_Rainfall_area1']]
}


cols_to_drop_config = {'Aquifer_Auser': ['Rainfall_Gallicano', 'Rainfall_Pontetetto',
                                  'Rainfall_Monte_Serra', 'Rainfall_Orentano', 'Rainfall_Borgo_a_Mozzano',
                                  'Rainfall_Piaggione', 'Rainfall_Calavorno',
                                  'Temperature_Orentano', 'Temperature_Monte_Serra',
                                  'Temperature_Lucca_Orto_Botanico',
                                  'Depth_to_Groundwater_PAG', 'Depth_to_Groundwater_DIEC',
                                  'Hydrometry_Monte_S_Quirico', 'Hydrometry_Piaggione',
                                  'Volume_POL', 'Volume_CC2',
                                  'Volume_CSA', 'Volume_CSAL',
                                 ],
                'Aquifer_Petrignano' : ['Temperature_Bastia_Umbra', 'Temperature_Petrignano'],
                'River_Arno': ['Rainfall_Le_Croci', 'Rainfall_Cavallina', 'Rainfall_S_Agata',
                               'Rainfall_Mangona', 'Rainfall_S_Piero'],
                'Lake_Bilancino': ['Rainfall_S_Piero', 'Rainfall_Mangona', 'Rainfall_S_Agata',
                                   'Rainfall_Cavallina', 'Rainfall_Le_Croci', 'Temperature_Le_Croci']
               }

