import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from shapely.geometry import Point
import json

def identity_scale(minval, maxval):
    def scalar(val):
        return val
    return scalar

def log_scale(minval, maxval):
    def scalar(val):
        val = val + abs(minval) + 1
        return np.log10(val)
    return scalar

def power_scale(minval, maxval):
    def scalar(val):
        val = val + abs(minval) + 1
        return (val/1000)**2
    return scalar

def load_data(file):
    with open(file, 'r') as file:
        data = json.load(file)
        return data


# df = pd.read_json('data/parsed_w_precise_coords.json')
# print(df)
# data = list(df['address'])
# print(data)

# data = load_data('../data/parsed_w_coords.json')

df = pd.read_csv('../data/test_randomhomes_big.csv')

# final = {"lat": [], "lon": []}
# lat = []
# lon = []
# for d in data:
#     try:
#         a = d['google_results'][0]['geometry']['location']['lat']
#         b = d['google_results'][0]['geometry']['location']['lng']
#         final['lat'].append(a)
#         final['lon'].append(b)
#     except Exception as e:
#         pass

# df = pd.DataFrame(final)

import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt

collision_points = df.apply(
    lambda srs: Point(float(srs['lon']), float(srs['lat'])),
    axis='columns'
)
gdf = gpd.GeoDataFrame(df, geometry=collision_points)
gdf['constant'] = 1
ax = gplt.webmap(gdf, projection=gcrs.WebMercator())
gplt.pointplot(gdf, ax=ax, scale_func=identity_scale, scale= 'constant')
plt.show()