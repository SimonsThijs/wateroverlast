import pandas as pd
import numpy as np

from hoogtekaart import height_map_nl
from coords import rdconverter

import time

HMNL = height_map_nl.HeightMapNL()
df = pd.read_csv('test_0_rain.csv')[:]

total = len(df)
count = 0
btime = time.time()

def get_height_data(data):
    global count
    count +=1
    now = time.time()
    avg_time = (now-btime)/count
    left = total-count
    if count % 10 == 0:
        print('======')
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
    rdx = round(rdx, 2)
    rdy = round(rdy, 2)
    try:
        data =  (HMNL.get_height_area(rdx-100, rdy+100, rdx+100, rdy-100))
    except:
        data = np.nan
        print("failed")
    # data = np.where(data > 1000, np.nan, data)
    return data


# df = df[:100]
df['height'] = df.apply(get_height_data, axis=1)
df = df.dropna(axis=0)
df.to_pickle('test_0_no_rain.pkl')
