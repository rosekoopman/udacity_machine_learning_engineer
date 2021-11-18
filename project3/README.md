# Acea project

## Introduction

In the last decade humanity faced unprecedented challenges due to rising sea water level, flooding of rivers, draughts and overall more extreme whether conditions. With the effects of climate change becoming a severe thread to humanity, the monitoring of water supplies becomes of increasing importance. 

With a service area covering over 9 million people, the [Acea Group](https://www.gruppo.acea.it/en) is one of Italy's leading companies in the field of water supply. Its main responsibilities include building and maintaining a water network and preserving the health of its water bodies,  in order to guarantee the daily water supply to Italy's inhabitants. 

The Acea Groups utilises different types of water bodies:


- Aquifer: A water-containing layer (such as sand) in the ground. Water can be taken from the aquifer by making a well. 
- Water spring: The place where an underground water body (e.g. underground river) emerges at the earth's surface.
- River: A flowing body of water, typically flowing from a water spring to the ocean.
- Lake: A contained body of water which is surrounded by land. There can be a river feeding into the lake and another river draining the lake.

In order to provide in the daily water consumption, Acea Group carefully monitors the water level and water flow in its different water bodies. Each of these types of water bodies have their own characteristics and respond in a different way to events of rainfall or periods with high temperatures. Typically water bodies fill in autumn and winter when more water enters the bodies then is being utilised, while in spring and autumn water levels drop. In order to guarantee continuous water supply and preserve the health of the water bodies, there is a need to forecast water availability in terms of level and flow.

The task at hand it to build a predictive model which predicts either water level or water flow for several water bodies. This challenge is published as a [Kaggle competition](https://www.kaggle.com/c/acea-water-prediction/). Since the type of features and target depend on the type of water body, a different model needs to be made for each type of water body. As the differences between water bodies of the same type can be large, and the availability of features differs, it might be necessary to create a separate model for each individual water body. 

## Code

The notebooks provided in this repo follow the project sturcture as outline in the proposal. The numbering corresponds to the steps described in the proposal.
Needless to say, the notebooks should be run in order.

Some common functionality is stored in the python package *acea*. To install this package run

```bash
pip install -e .
```

All required packages are included in the `requirements.txt` and are automatically installed when installing *acea*.

The data can be obtained from [here](https://www.kaggle.com/c/acea-water-prediction/data). The raw data is expected to be saved in the folder `data/raw`.
After each data preparation step the data is saved in a folder `data/step-name`.
