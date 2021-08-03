import io
import json
import time

from osgeo import ogr, gdal
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
			'var': 'plus-fysiekVoorkomenWegdeel',
			'allow': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'onbegroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow': ['asfalt','cementbeton','kunststof','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'ondersteunendwegdeel': {
			'var': 'plus-fysiekVoorkomenOndersteunendWegdeel',
			'allow': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		}
	},
	'onverhard': {
		'wegdeel': {
			'var': 'plus-fysiekVoorkomenWegdeel',
			'allow_not': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'onbegroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow_not': ['asfalt','cementbeton','kunststof','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'ondersteunendwegdeel': {
			'var': 'plus-fysiekVoorkomenOndersteunendWegdeel',
			'allow_not': ['asfalt','cementbeton','betonstraatstenen','gebakken klinkers','tegels','sierbestrating','beton element',]
		},
		'begroeidterreindeel': {
			'var': 'plus-fysiekVoorkomen',
			'allow_not': []
		}
	}
}

def get_attributes(lyr):
	ldefn = lyr.GetLayerDefn()
	schema = []
	for n in range(ldefn.GetFieldCount()):
	    fdefn = ldefn.GetFieldDefn(n)
	    schema.append(fdefn.name)
	return (schema)

loaded = {}

# gdal.AllRegister();
# load files
for l in list(layers.keys()):
	print(l)
	for f in list(layers[l].keys()):
		if f not in loaded:
			file = 'testdata/bgt_{}.gml'.format(f)
			dataset = ogr.GetDriverByName('GML').Open(file)
			# ds.ExecuteSQL("ALTER TABLE my_shp DROP COLUMN my_field")
			lyr = dataset.GetLayer(0)
			lyrname = lyr.GetName()
			atts = get_attributes(lyr)
			print(atts)

			cols_to_delete = [s for s in atts if s not in ['eindRegistratie', layers[l][f]['var'] ]]
			for c in cols_to_delete:
				dataset.ExecuteSQL("ALTER TABLE {} DROP COLUMN {}".format(lyrname, c))

			print(get_attributes(lyr))
			lyr.SetAttributeFilter('eindRegistratie IS NULL')

			print(lyr.GetFeatureCount())

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
	gdf.to_pickle('/local/s1830120/{}.pkl'.format(l))














