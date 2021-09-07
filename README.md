# Wateroverlast repo

The goal of this repo is to provide tools to build a model that can solve flooding issues in the Netherlands. The emphasis is on water damage caused by a large amount of rain. Below we will briefly describe the exact tools this repo provides.

## Target
The target used to build the model is based on the p2000 messaging service used by the emergency services in the Netherlands. We have scraped the fire department messages from 2016 onwards in the whole of the netherlands. The data was scraped from alarmfase1.nl by reverse engineering their app.

We then filter the scraped messages by the use of the word 'wateroverlast' (flooding). The location of the flooding found by alarmfase1.nl is checked and if not correct, manually corrected. Note, not all messages contain exact locations, sometimes only the street is available. The final dataset of negative examples can be find in the 'data/' directory.

One of the problems with the p2000 messages is that it is not always sure if the flooding is caused by great amounts of rain or e.g. a broken pipe. In a future step we add a threshold on how much rain must have fallen in the past 3 hours in order to try to solve this problem.

The negative examples are obtained by finding adresses close to a flooding which are not mentioned in a p2000 message at that moment of time. For this we use the BAG (see: <https://www.pdok.nl/introductie/-/article/basisregistratie-adressen-en-gebouwen-ba-1>).

## Other data source
- The rain data is obtained from <https://dataplatform.knmi.nl/catalog/datasets/index.html?x-dataset=rad_nl25_rac_mfbs_5min&x-dataset-version=2.0>. Make sure the data is placed like: 'neerslag/data/{year}/{month}/RAD_NL25_RAC_MFBS_5min_XXXXXXXXXXXX_NL.h5'

- BGT is used to obtain shapefiles with information on the surface type (penetrable, non-penetrable, water)

- BAG is used to obtain geometry of affected and surrounding buildings

- AHN3 is used to obtain a height map of the area around the affected building

## Generating the final dataset




Setup:
```
git clone https://github.com/SimonsThijs/wateroverlast.git
cd wateroverlast

# between these steps I set up my virtualenv but this is not necessary

export PYTHONPATH=$PYTHONPATH:$(pwd)
pip install -r requirements.txt
```
