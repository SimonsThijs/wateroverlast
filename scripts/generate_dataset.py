from osgeo import gdal

# this script generates the dataset which we can apply machine learning to
# 1. get all positive examples
# 2. enrich positive examples with rain information
# 3. keep only the examples with enough precipitation
# 4. find n negative examples in a certain range for each positive example using the bag list
# 5. enrich negative examples with precipitation data
# 6. enrich all examples with height, water, infiltration, non-infiltration, house, center-house


import numpy as np
import pandas as pd

begin = '2016-01-01 00:00:00'
end = '2021-02-23 23:59:59'
strfformat = "%Y-%m-%d %H:%M:%S"

from BAG import home_sampler
from coords import rdconverter
from neerslag import precipitation_nl
from layerbuilder import bag_layer, bgt_layer, ahn_layer, util

from random import randrange
from datetime import timedelta, datetime
import time
import os

total = 0
count = 0
btime = time.time()


# helper functions
def get_data(data, a):
    d = data
    # print(d)
    if len(d) > 0 and d[0]['geometry']['location_type'] != 'APPROXIMATE':
        return data[0]['geometry']['location'][a]
    else:
        return np.nan

def parse_datetime(data):
    return datetime.strptime(str(data['date']).strip(), strfformat)

def get_precipitation_data(row):
    global count
    count +=1
    now = time.time()
    avg_time = (now-btime)/count
    left = total-count
    if count % 10 == 0:
        print('====== rain ')
        print('time spent', now-btime)
        print('did', count, 'examples')
        print('avg', avg_time)
        print('left', left)
        print('time left', left*avg_time)
        print('======')

    date = row['date']
    # date = datetime.strptime(str(row['date']), strfformat)
    lat = row['lat']
    lon = row['lng']
    rain = PNL.get_precipation_data_past_hours_list(date.year, date.month, date.day, date.hour, date.minute, lat, lon, 12)
    return rain

def calc_sums(row):
    data = []
    try:
        lst = list(row['prec12'])
        
        for j in range(12):
            d = np.asarray(lst[j*12:j*12+12])
            d = np.where(d == 65535, 0, d)
            d = np.where(d == np.nan, 0, d)
            d = np.where(d < 0, 0, d)
            data.append(np.sum(d))
            
    except:
        data = [0]*12
        
    return data


# step 1
df1 = pd.read_json('../data/parsed_w_precise_coords.json')
df1 = df1.dropna()
df1['lat'] = df1['google_results'].apply(get_data, args=('lat',))
df1['lng'] = df1['google_results'].apply(get_data, args=('lng',))
df1['target'] = 1
df1 = df1[['lat','lng','target','date']]
df1 = df1.dropna()
df1['date'] = df1.apply(parse_datetime, axis=1)

# df1 = df1[150:200]

# step 2
PNL = precipitation_nl.PrecipitationNL(queue_size=300)
total = len(df1)
count = 0
btime = time.time()
df1 = df1.sort_values(by=['date'])
df1['prec12'] = df1.apply(get_precipitation_data, axis=1)


# step 3
df1['prec_sums'] = df1.apply(calc_sums, axis=1)
cols = ['sum'+str(i+1) for i in range(12)]
df1[cols] = pd.DataFrame(df1.prec_sums.tolist(), index=df1.index)
df1['past3hours'] = df1['sum1'] + df1['sum2'] + df1['sum3']
df1 = df1[(df1.past3hours > 500)]
df1 = df1.drop(columns=cols)

# step 4
HM = home_sampler.HomeSampler()
data0 = {'lat':[], 'lng':[], 'date':[], 'target': []}
n = 5
def sample_random_houses_close(data):
    rdx = rdconverter.gps2X(data['lat'],data['lng'])
    rdy = rdconverter.gps2Y(data['lat'],data['lng'])
    da = HM.sample_in_range(rdx, rdy, 500, 50, n)
    for d in da:
        lat = rdconverter.RD2lat(d[0], d[1])
        lng = rdconverter.RD2lng(d[0], d[1])
        data0['lat'].append(lat)
        data0['lng'].append(lng)
        data0['date'].append(data['date'])
        data0['target'].append(0)

df1.apply(sample_random_houses_close, axis=1)
df0 = pd.DataFrame(data0)

# step 5
total = len(df0)
count = 0
btime = time.time()
df0 = df0.sort_values(by=['date'])
df0['prec12'] = df0.apply(get_precipitation_data, axis=1)

df = pd.concat([df0, df1], ignore_index=True)

# step 6
total = len(df)
count = 0
btime = time.time()
ahn = ahn_layer.AHNLayer()
bag = bag_layer.BAGLayer()
bgt = bgt_layer.BGTLayer()

def add_layers(data):
    try:
        global count
        count +=1
        now = time.time()
        avg_time = (now-btime)/count
        left = total-count
        if count % 10 == 0:
            print('====== layers ')
            print('time spent', now-btime)
            print('did', count, 'examples')
            print('avg', avg_time)
            print('left', left)
            print('time left', left*avg_time)
            print('======')

        lat = data['lat']
        lng = data['lng']
        rdx = rdconverter.gps2X(lat,lng)
        rdy = rdconverter.gps2Y(lat,lng)
        # x, y = int(rdx), int(rdy)
        x, y = round(rdx, 2), round(rdy, 2)
        d = 100

        arr = np.empty((6,400,400))

        ahn_data = ahn.get_gdal_dataset(x-d, x+d, y-d, y+d)
        arr[0] = ahn_data.ReadAsArray()

        bag_data = bag.get_gdal_dataset(x-d, x+d, y-d, y+d)
        arr[1] = util.to_raster(bag_data, ahn_data, 'bag')

        bag_data_single = bag.get_gdal_dataset(x-d, x+d, y-d, y+d, intersection_type='single')
        arr[2] = util.to_raster(bag_data_single, ahn_data, 'bag_single')

        bgt_data = bgt.get_gdal_dataset(x-d, x+d, y-d, y+d, layer='water')
        arr[3] = util.to_raster(bgt_data, ahn_data, 'water')

        bgt_data = bgt.get_gdal_dataset(x-d, x+d, y-d, y+d, layer='verhard')
        arr[4] = util.to_raster(bgt_data, ahn_data, 'verhard')

        bgt_data = bgt.get_gdal_dataset(x-d, x+d, y-d, y+d, layer='onverhard')
        arr[5] = util.to_raster(bgt_data, ahn_data, 'onverhard')
        return arr
    except Exception as e:
        print(e)
        return None

df['layers'] = df.apply(add_layers, axis=1)

is_dslab = os.getenv('DS_LAB', None)
if is_dslab:
    dir_ = '/local/s1830120/'
else:
    dir_ = ''


df.to_pickle(dir_ + '50-500.pkl', protocol=4)

print(df)





