from hoogtekaart import height_map_nl

import numpy as np
import pandas as pd


from PIL import Image
from matplotlib import cm


def show_img(data, data2, i, type):
    print('img_{}_{}.png'.format(i,type))
    print(cm.gist_earth(data).shape)
    arr = np.where(data > 1000000, 0, data)
    min_ = np.min(arr)
    max_ = np.max(arr)
    arr = (arr-min_) / (max_-min_)
    arr = cm.gist_earth(arr)
    arr[data>1000000] = [1, 1, 1,  1]
    arr[data2>1000000] = [0, 0, 1,  1]
    im = Image.fromarray(np.uint8(arr*255))
    im.save('img_{}_{}.png'.format(i,type))


df = pd.read_pickle('save.pkl').reset_index(drop=True)

print(df)
i = 8
dsm = df.at[i, 'height_dsm']
dtm = df.at[i, 'height_dtm']
rain_flow = df.at[i, 'rain_flow']

rain_flow[dtm>1000] = np.nan

size=10
print(np.nanmax(rain_flow[100-size:100+size, 100-size:100+size]))
size=20
print(np.nanmax(rain_flow[100-size:100+size, 100-size:100+size]))

rain_flow[dtm>1000] = 10000000

print(df.at[i, 'lat'], df.at[i, 'lng'])
print(df.iloc[i])
# print(df.at[i, 'lng'])

show_img(rain_flow, dsm, 2, 'watertest')



















