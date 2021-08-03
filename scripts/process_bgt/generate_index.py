
names = ['verhard', 'onverhard', 'water']



import rtree
import geopandas as gpd
import pandas as pd








local = False

if local:
	dir_ = 'testdata/'
else:
	dir_ = '/local/s1830120/'



for name in names:
	print(name)

	index = rtree.index.Rtree(name)
	gdf = gpd.GeoDataFrame(pd.read_pickle(dir_ + '{}.pkl'.format(name)))
	for i,d in gdf.iterrows():
		index.insert(i,d.geometry.bounds, d.geometry)






