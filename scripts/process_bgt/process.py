import io
import json
import time

from shapely.geometry import Polygon
import geopandas as gpd
import fiona



layers = {
	'water': {
		'waterdeel': {
			'var': 'class',
			'allow_not': []
		},
	},
	'verhard': {
		'wegdeel': {
			'var': 'surfaceMaterial',
			'allow': ['open verharding', 'gesloten verharding', 'waardeOnbekend']
		},
		'onbegroeidterreindeel': {
			'var': 'bgt-fysiekVoorkomen',
			'allow': ['open verharding', 'gesloten verharding', 'waardeOnbekend', 'erf']
		},
		'ondersteunendwegdeel': {
			'var': 'surfaceMaterial',
			'allow': ['open verharding', 'gesloten verharding', 'waardeOnbekend']
		}
	},
	'onverhard': {
		'wegdeel': {
			'var': 'surfaceMaterial',
			'allow_not': ['open verharding', 'gesloten verharding', 'waardeOnbekend']
		},
		'onbegroeidterreindeel': {
			'var': 'bgt-fysiekVoorkomen',
			'allow_not': ['open verharding', 'gesloten verharding', 'waardeOnbekend', 'erf']
		},
		'ondersteunendwegdeel': {
			'var': 'surfaceMaterial',
			'allow_not': ['open verharding', 'gesloten verharding', 'waardeOnbekend']
		},
		'begroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow_not': []
		}
	}
}


loaded = {}

local = False

if local:
	dir_ = 'testdata/'
else:
	dir_ = '/local/s1830120/'

# load files
for l in list(layers.keys()):
	print(l)
	for f in list(layers[l].keys()):
		if f not in loaded:
			file = dir_ + 'bgt_{}.gml'.format(f)
			fc = fiona.open(file, ignore_geometry=False)
			print("loaded fiona")
			gdf = gpd.GeoDataFrame.from_features(
				fc, crs='epsg:28992')
			print("loaded in pandas")
			gdf = gdf[gdf['eindRegistratie'].isna()]
			gdf = gdf[['geometry', layers[l][f]['var'] ]]
			loaded[f] = gdf
			# gdf.to_pickle('testdata/bgt_{}.pkl'.format(f))



for l in list(layers.keys()):
	print(l)
	gdf = gpd.GeoDataFrame({'geometry':[]})
	for f in list(layers[l].keys()):
		var = layers[l][f]['var']
		data = loaded[f]
		if 'allow_not' in layers[l][f]:
			gdf_2 = data[~data[var].isin(layers[l][f]['allow_not'])]
		if 'allow' in layers[l][f]:
			gdf_2 = data[data[var].isin(layers[l][f]['allow'])]

		gdf = gdf.append(gdf_2[['geometry']])

	gdf = gdf.reset_index(drop=True)
	gdf.to_pickle(dir_ + '{}.pkl'.format(l))














