import json

import osgeo.gdal as gdal
import numpy as np
from numpy import ma
import rasterio
from rasterio.plot import show

from coords import rdconverter

class HeightMapNL(object):
	datatype = '5m_dtm'
	datafolder = 'AHN3_data'
	def __init__(self, data_file="bladindexen.json"):
		self.loaded_tile = None
		with open(data_file) as json_file:
			self.data = json.load(json_file)

	def is_in_tile(self, x, y, tile):
		coords_list = tile['geometry']['coordinates'][0][0]
		min_x = min([x[0] for x in coords_list])
		min_y = min([x[1] for x in coords_list])
		max_x = max([x[0] for x in coords_list])
		max_y = max([x[1] for x in coords_list])
		# print(min_x)
		return min_x <= x and x < max_x and min_y <= y and y < max_y

	def get_filename(self, tilenr):
		return HeightMapNL.datafolder + "/M5_" + tilenr.upper() + ".TIF" 

	def load_file(self, tilenr):
		file_name = self.get_filename(tilenr)
		dataset = gdal.Open(file_name, gdal.GA_ReadOnly)
		if dataset is None:
		    raise Exception()

		# Get the georeferencing metadata.
		# We don't need to know the CRS unless we want to specify coordinates
		# in a different CRS.
		#projection = dataset.GetProjection()
		geotransform = dataset.GetGeoTransform()
		# print(geotransform)
		# We need to know the geographic bounds and resolution of our dataset.
		if geotransform is None:
		    dataset = None
		    raise Exception()

		# Get the first band.
		band = dataset.GetRasterBand(1)
		
		# We need to nodata value for our MaskedArray later.
		nodata = band.GetNoDataValue()
		# Load the entire dataset into one numpy array.
		image = band.ReadAsArray(0, 0, band.XSize, band.YSize)
		# print(image)
		# Close the dataset.
		dataset = None

		# Create a numpy MaskedArray from our regular numpy array.
		# If we want to be really clever, we could subclass MaskedArray to hold
		# our georeference metadata as well.
		# see here: http://docs.scipy.org/doc/numpy/user/basics.subclassing.html
		# For details.
		masked_image = ma.masked_values(image, nodata, copy=False)
		masked_image.fill_value = nodata

		# if succesfull save the data
		self.dataset = dataset
		self.loaded_tile = tilenr
		self.mi = masked_image
		self.gt = geotransform
		self.image = image
		# return masked_image, geotransform

	def map_to_pixel(self, pos):
		# s = self.gt[0] * self.gt[4] - self.gt[3] * self.gt[1]
		x = (pos[0] - self.gt[0]) / self.gt[1]
		y = (pos[1] - self.gt[3]) / self.gt[5] -1
		return (x, y)

	def get_height_from_file(self, x_p, y_p):
		pp = self.map_to_pixel((x_p, y_p))

		x = int(pp[0])
		y = int(pp[1])

		if x < 0 or y < 0 or x >= self.image.shape[1] or y >= self.image.shape[0]:
		    raise Exception()

		# Note how we reference the y column first. This is the way numpy arrays
		# work by default. But GDAL assumes x first.
		value = self.image[y, x]

		return value

	def get_tile(self, x, y):
		for tile in self.data['features']:
			if self.is_in_tile(x,y, tile) and tile['properties']['has_data_' + HeightMapNL.datatype]:
				return tile
		return None

	def get_height(self, x,y):
		tile = self.get_tile(x, y)
		if tile:
			if self.loaded_tile != tile['properties']['bladnr']:
				self.load_file(tile['properties']['bladnr'])
			return self.get_height_from_file(x,y)
		else:
			return None
		
	def get_height_from_latlng(self, lat,lng):
		x = rdconverter.gps2X(lat, lng)
		y = rdconverter.gps2Y(lat, lng)
		return self.get_height(x,y)

	def show_tile(self, x, y):
		bladnr = self.get_tile(x, y)['properties']['bladnr']
		fp = self.get_filename(bladnr)
		img = rasterio.open(fp)
		show(img)







