from osgeo import gdal
from owslib.wcs import WebCoverageService
import logging

import rasterio
from rasterio.plot import show
from matplotlib import pyplot
import numpy as np

owslib_log = logging.getLogger('owslib')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
owslib_log.addHandler(ch)
owslib_log.setLevel(logging.DEBUG)

my_wcs = WebCoverageService('https://geodata.nationaalgeoregister.nl/ahn3/wcs', version='1.0.0')

print(my_wcs.contents['ahn3_05m_dtm'].boundingboxes)

output=my_wcs.getCoverage(identifier='ahn3_05m_dtm',width=2000, height=2000, bbox=(93171.54234,463528,94171.54234,464528),format='GEOTIFF_FLOAT32',CRS='EPSG:28992')
print(output)
f=open('tmp.tif','wb')
f.write(output.read())


# src = rasterio.open("foo2.tif")
# pyplot.imshow(src.read(1), cmap='gist_earth')
# pyplot.show()

raster = gdal.Open('tmp.tif')
print(raster.GetMetadata())
print(raster.RasterCount)
band = raster.GetRasterBand(1)
print(np.asarray(band.ReadAsArray()))

f.close()
# 93671, 464028
# https://geodata.nationaalgeoregister.nl/ahn3/wcs?SERVICE=WCS&VERSION=1.0.0&REQUEST=GetCoverage&FORMAT=GEOTIFF_FLOAT32&COVERAGE=ahn3_05m_dsm&BBOX=93171,463528,94171,464528&CRS=EPSG:28992&RESPONSE_CRS=EPSG:28992&WIDTH=1000&HEIGHT=1000


# https://geoforum.nl/t/resolutie-binnegehaalde-geotiff-via-wcs-ahn/4815
