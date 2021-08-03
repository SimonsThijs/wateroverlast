import numpy as np
import pandas as pd


from hoogtekaart import height_map_nl
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




df = pd.read_pickle('check.pkl')
i = 4
r = df['rain_flow'][i]
r[df['height_dtm'][i] > 1000] = 1000001
print(df.iloc[i])
show_img(df['rain_flow'][i], df['height_dsm'][i], i, 'positief' if df['target'][i] == 1 else 'negatief')