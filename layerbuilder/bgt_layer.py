from osgeo import gdal

from layerbuilder.base import Layer

import io
import json
import time
import os

import zipfile
import requests
from shapely.geometry import Polygon
import geopandas as gpd
import fiona
import rtree


LAYERS = ['wegdeel', 'onbegroeidterreindeel', 'begroeidterreindeel', 'ondersteunendwegdeel', 'waterdeel']
SPECIFICATION = {
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



class BGTLayer(Layer):
	"""docstring for LayerBuilder"""
	def __init__(self):
		self.indexes = {}
		super(BGTLayer, self).__init__()
		is_dslab = os.getenv('DS_LAB', None)
		if is_dslab:
			self.dir = '/local/s1830120/'
		else:
			self.dir = self.dir_ + '/data/'
		

	def get_gdal_dataset(self, x_min, x_max, y_min, y_max, **kwargs):
		if 'layer' in kwargs:
			type_ = kwargs['layer']

			if type_ not in self.indexes:
				index = rtree.index.Rtree(self.dir + '{}'.format(type_))
				self.indexes[type_] = index

			index = self.indexes[type_]
			r = [s.object for s in index.intersection((x_min, y_min, x_max, y_max), objects=True)]
			gdf = gpd.GeoDataFrame({'geometry':r})
			dataset = gdal.OpenEx(gdf.to_json())
			return dataset
		else:
			return None


if __name__ == '__main__':
	bag = BGTLayer()
	x,y = 93659, 463943
	d = 50.0
	r = bag.get_gdal_dataset(x-d,x+d,y-d,y+d, layer='water')
	print(r)









