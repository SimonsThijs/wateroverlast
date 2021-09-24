# Wateroverlast repo

The goal of this repo is to provide tools to build a model that can solve flooding issues in the Netherlands. The emphasis is on water damage caused by a large amount of rain. Below we will briefly describe the exact tools this repo provides.

## Target
The target used to build the model is based on the p2000 messaging system used by the emergency services in the Netherlands. We have scraped the fire department messages from 2016 onwards in the whole of the netherlands. The data was scraped from alarmfase1.nl by reverse engineering their app. 

We then filter the scraped messages by the use of the word 'wateroverlast' (flooding). The location of the flooding found by alarmfase1.nl is checked and if not correct, manually corrected. Note, not all messages contain exact locations, sometimes only the street is available. The final dataset of negative examples can be found in the 'data/' directory. The full scrape without the processing can be found here: <>

One of the problems with the p2000 messages is that it is not always sure if the flooding is caused by great amounts of rain or e.g. a broken pipe. In a future step we add a threshold on how much rain must have fallen in the past 3 hours in order to try to solve this problem.

The negative examples are obtained by finding adresses close to a flooding which are not mentioned in a p2000 message at that moment of time. For this we use the BAG (see: <https://www.pdok.nl/introductie/-/article/basisregistratie-adressen-en-gebouwen-ba-1>).

## Data sources
- The rain data is obtained from <https://dataplatform.knmi.nl/catalog/datasets/index.html?x-dataset=rad_nl25_rac_mfbs_5min&x-dataset-version=2.0>. Make sure the data is placed like: 'neerslag/data/{year}/{month}/RAD_NL25_RAC_MFBS_5min_XXXXXXXXXXXX_NL.h5'.

- BGT is used to obtain shapefiles with information on the surface type (non-permeable, permeable, water). This requires you to download  and unpack it in 'layerbuilder/data/'.

- BAG is used to obtain geometry of affected and surrounding buildings. We use the public wfs from <https://nationaalgeoregister.nl>, thus, does not requires additional files to be downloaded.

- BAG is used to sample random homes in the Netherlands. This requires you to download  and place it in 'BAG/data/'.

- AHN3 is used to obtain a height map of the area around the affected building. We use the public wcs from <https://nationaalgeoregister.nl>, thus, does not requires additional files to be downloaded.

## Generating the final dataset
We use the script 'scripts/generate_dataset.py' to generate the final dataset. This script also serves as an example on how to use the tools provided in the repo. The script works as follows:

1. Get all positive examples using the p2000 dataset.
2. Enrich positive examples with precipitation data.
3. Only keep the examples with enough precipitation, remove the others. 
4. Find n negative examples in a certain range for each positive example using the bag list of all adresses. We set n to 5. This implies that for every positive example we will have 5 negative examples.
5. Enrich negative examples with precipitation data.
6. Enrich all examples with different layers of information on the surrounding area (e.g. height information, surface area type).

The generated layers, in the correct order, for each example are:
- Height data
- Locations of buildings
- Locations of affected building
- Water surface area (requires you to download the generated geometry files)
- Non-permeable surface area (requires you to download the generated geometry files)
- Permeable surface area (requires you to download the generated geometry files)

Each layer is 200x200 meters in size, with a granualarity of 0.5 meters. This results in an array of size 400x400 for each layer. The affected house is located in the center of this area. 

Note: you probably need a high-memory machine to run the script since we are working with quite a lot of data. If you are not able to generate the dataset you could also download the pre-generated dataset from:


## Setup
```
git clone https://github.com/SimonsThijs/wateroverlast.git
cd wateroverlast

# between these steps I set up my virtualenv but this is not necessary

export PYTHONPATH=$PYTHONPATH:$(pwd)
pip install -r requirements.txt
```

Some tools require additional datasets to be downloaded and placed in the right directory. Please look at the section [data sources](#data-sources). 

