from osgeo import gdal

from layerbuilder.base import Layer

import io

from shapely.geometry import Point
import geopandas as gpd
import requests

class BAGLayer(Layer):
	"""docstring for LayerBuilder"""
	def __init__(self):
		self.gdf_cache = None
		self.cached_extend = None
		super(Layer, self).__init__()

	def get_bag_geopandas(self, x_min, x_max, y_min, y_max):

	    url = "http://geodata.nationaalgeoregister.nl/bag/wfs/v1_1?service=wfs&version=2.0.0&request=GetFeature&typeName=pand&bbox={},{},{},{}&outputFormat=application%2Fjson%3B%20subtype%3Dgeojson".format(
	        x_min, y_min, x_max, y_max)

	    response = requests.get(url)

	    gdf = gpd.geopandas.read_file(io.BytesIO(response.content), crs='epsg:28992')
	    self.gdf_cache = gdf
	    self.cached_extend = (x_min, x_max, y_min, y_max)
	    return gdf
	

	def get_gdal_dataset(self, x_min, x_max, y_min, y_max, **kwargs):
		"""General interface"""

		gdf = None

		# we use a simple cache to reduce the amount of requests
		# this is because we have a layer with all houses and a layer with only the house with water damage
		if self.cached_extend == (x_min, x_max, y_min, y_max):
			gdf = self.gdf_cache
		else:
			gdf = self.get_bag_geopandas(x_min, x_max, y_min, y_max)


		# make instersection
		if 'intersection_type' in kwargs and kwargs['intersection_type'] == 'single':
			geometry = gdf.geometry.intersection(Point(x_min+(x_max-x_min)/2, y_min+(y_max-y_min)/2))
			gdf = gdf[~geometry.is_empty]

		return gdal.OpenEx(gdf.to_json())


if __name__ == '__main__':
	bag = BAGLayer()
	x,y = 93659, 463943
	d = 50.0
	r = bag.get_gdal_dataset(x-d,x+d,y-d,y+d, intersection_type='single')
	print(r)




