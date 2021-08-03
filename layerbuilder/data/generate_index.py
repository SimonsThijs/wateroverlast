
name = ''



import rtree


index = rtree.index.Rtree(name)



import geopandas as gpd
import pandas as pd


gdf = gpd.GeoDataFrame(pd.read_pickle('{}.pkl'.format(name)))


for i,d in gdf.iterrows():
	index.insert(i,d.geometry.bounds, d.geometry)






