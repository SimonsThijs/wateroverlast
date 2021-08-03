

import rtree
import geopandas as gpd
import matplotlib.pyplot as plt


x,y = 93660.0, 463877.0

b = (x-1000, y-1000, x+1000, y+1000)


name = 'onverhard'
index = rtree.index.Rtree(name)

r = [s.object for s in index.intersection(b, objects=True)]


gdf = gpd.GeoDataFrame({'geometry':r})

gdf.plot()
plt.show()


