import h5py
from PIL import Image
import numpy as np
from pyproj import CRS, Transformer

class PrecipitationNL(object):
	"""docstring for PrecipitationNL"""
	def __init__(self):
		super(PrecipitationNL, self).__init__()
		
	def get_file_name(self, year, month, day, hour, minute):
		# hours and minutes are 0 index e.g. hours go from 0 to 23

		# floor to closest 5 min
		minute = int(minute/5) * 5

		return "data/{}/{:02d}/RAD_NL25_RAC_MFBS_EM_5min_{}{:02d}{:02d}{:02d}{:02d}_NL.h5".format(
				year, month, year, month, day, hour, minute)

	def reproject(self, lat, lon):

		proj4_to = "+proj=stere +lat_0=90 +lon_0=0.0 +lat_ts=60.0 +a=6378.137 +b=6356.752 +x_0=0 +y_0=3650"
		proj4_from = "+proj=latlong +datum=WGS84 +R=+12756274"
		# proj_to = wradlib.georef.proj4_to_osr(proj4_to)
		# proj_from = wradlib.georef.proj4_to_osr(proj4_from)
		# result = wradlib.georef.reproject((lon, lat), projection_source=proj_from, projection_target=proj_to)
		# result[1] *= -1

		csr_to = CRS.from_proj4(proj4_to)
		csr_from = CRS.from_proj4(proj4_from)
		transformer =  Transformer.from_crs(csr_from, csr_to)
		result = transformer.transform(lon, lat)

		return result[0], result[1]*-1

	def get_precipation_data(self, year, month, day, hour, minute, lat, lon):
		file_name = self.get_file_name(year, month, day, hour, minute)

		# if i understand correctly the center of the pixel represents the top left corner
		# see geo_pixel_diff http://bibliotheek.knmi.nl/knmipubIR/IR2003-05.pdf page 12
		# this observation is important for determining the closest grid from a lat lon coordinate
		# we should be able to just round the result of the projection

		coords = self.reproject(lat, lon)
		coords = (int(round(coords[0])), int(round(coords[1])))

		h5file = h5py.File(file_name)
		data = h5file['image1/image_data'][:]

		# data = data*1000
		# img = Image.fromarray(data)
		# img.save('my.png')
		# img.show()

		return data[coords[1],coords[0]]








