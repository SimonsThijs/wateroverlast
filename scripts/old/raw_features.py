
import pandas as pd
import numpy as np

import math


df = pd.read_pickle('save.pkl').reset_index()


print(df.columns)

column = 'height_dtm'

print(df.at[400, 'height_dtm'].shape)


def apply_func_get_height(row, x0,y0,size):
	height = row[column]
	height[height>1000] = np.nan
	return np.nanmean(height[x0:x0+size,y0:y0+size])


def normalize(row):
	height = row[column]
	height[height>1000] = np.nan
	return (height-np.nanmean(height))/np.nanstd(height)


df[column] = df.apply(normalize, axis=1)
# print(df['height_dtm'])

# we make the raw features here
features = []
array_dim = 200
n = 10000
size = int(math.sqrt(array_dim*array_dim/n))
for x in range(0,array_dim,size):
	for y in range(0,array_dim,size):
		name = "{}_{}_{}_raw".format(column, x,y)
		df[name] = df.apply(apply_func_get_height, args=(x, y, size), axis=1)
		features.append(name)

print(features)


df.to_pickle('save_w_raw_features.pkl')










