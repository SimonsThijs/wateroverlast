import json
import os 

from osgeo import osr,gdal 
import numpy as np
from numpy import ma
import rasterio
from rasterio.plot import show
from owslib.wcs import WebCoverageService

from coords import rdconverter

def map_to_pixel(pos, top_left_x, top_left_y, rastersize_x, rastersize_y):
    x = (pos[0] - top_left_x) / rastersize_x
    y = (pos[1] - top_left_y) / rastersize_y
    # print(x,y)
    return (int(x), int(y))


class CustomTile(object):
    def __init__(self, top_left_x, top_left_y, rastersize_x, rastersize_y, data):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.rastersize_x = rastersize_x
        self.rastersize_y = rastersize_y
        self.data = data
    


class HeightMapNL(object):
    datatype = '5m_dtm'

    datafolder = os.path.dirname(__file__) + '/AHN3_data'
    def __init__(self, data_file="/AHN3_data/bladindexen.json"):
        self.loaded_tile = None
        self.dsm = False #dsm zijn gebouwen niet weggewerkt, dtm is alternatief dat is maaiveld
        with open(os.path.dirname(__file__) + data_file) as json_file:
            self.data = json.load(json_file)

        self.detailed = False #0,5 x 0,5 m

    def is_in_tile(self, x, y, tile):
        coords_list = tile['geometry']['coordinates'][0][0]
        min_x = min([x[0] for x in coords_list])
        min_y = min([x[1] for x in coords_list])
        max_x = max([x[0] for x in coords_list])
        max_y = max([x[1] for x in coords_list])

        return min_x <= x and x < max_x and min_y < y and y <= max_y

    def get_filename(self, tilenr):
        if self.dsm:
            return HeightMapNL.datafolder + "/dsm/R5_" + tilenr.upper() + ".TIF" 
        else:
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


    def map_to_pixel(self, pos):
        x, y =  map_to_pixel(pos, self.gt[0], self.gt[3], self.gt[1], self.gt[5])

        return x, y

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


    # for detailed maps 0.5x0.5 we use the WCS map service
    def detailed_height(self, x_min, y_max, x_max, y_min):
        my_wcs = WebCoverageService('https://geodata.nationaalgeoregister.nl/ahn3/wcs', version='1.0.0')

        identifier = 'ahn3_05m_dsm' if self.dsm else 'ahn3_05m_dtm'
        output=my_wcs.getCoverage(identifier=identifier, width=round(x_max-x_min), height=round(y_max-y_min), bbox=(x_min,y_min,x_max,y_max), format='GEOTIFF_FLOAT32', CRS='EPSG:28992')
        f=open('tmp.tif','wb')
        f.write(output.read())
        f.close()

        raster = gdal.Open('tmp.tif')
        band = raster.GetRasterBand(1)
        return np.asarray(band.ReadAsArray())

    def get_height_area(self, x_min, y_max, x_max, y_min):
        # return numpy array met hoogte getallen
        if self.detailed: #geeft hoogte voor 0,5x0,5 anders 5m bij 5m, die moet wel gedownload zijn
            return self.detailed_height(x_min, y_max, x_max, y_min)

        # init the array of the proper size needs to take into account the raster size
        tile = self.get_tile(x_min, y_max)
        if not tile:
            return np.asarray([])

        corners = tile['geometry']['coordinates'][0][0]
        file = self.load_file(tile['properties']['bladnr'])
        w1, h1 = self.map_to_pixel((x_min, y_max))
        w2, h2 = self.map_to_pixel((x_max, y_min))
        width, height = map_to_pixel((x_max, y_min), x_min, y_max, self.gt[1], self.gt[5])
        # print('=======')
        # print(x_min, y_max)
        # print(x_max, y_min)
        # print(height,width)
        result_array = np.full((h2-h1+1,w2-w1+1), np.nan)


        # get part that is definately in the tile
        x, y = self.map_to_pixel((x_min, y_max))
        x2, y2 = self.map_to_pixel((min(x_max, corners[1][0]-0.01), max(y_min, corners[2][1]+0.01)))
        # print('=======')
        # print(y, y2)
        # print(x, x2)
        arr = self.image[y:y2+1, x:x2+1]
        # print(arr)
        # print(arr.shape)
        result_array[0:0+arr.shape[0], 0:0+arr.shape[1]] = arr

        # bottom part
        if not self.is_in_tile(x_min, y_min, tile):
            new_top_left_x = x_min
            new_top_left_y = corners[2][1]-0.01
            # print(tile)
            arr = self.get_height_area(new_top_left_x, new_top_left_y, min(x_max, corners[1][0]-0.01), y_min)
            if arr.any():
                result_array[y2-y+1:y2-y+1+arr.shape[0], 0:0+arr.shape[1]] = arr

        # top part right
        # print(x_max, y_max)
        if not self.is_in_tile(x_max, y_max, tile):
            new_top_left_x = corners[2][0]+0.01
            new_top_left_y = y_max
            arr = self.get_height_area(new_top_left_x, new_top_left_y, x_max, y_min)
            if arr.any():
                result_array[0:0+arr.shape[0], x2-x+1:x2-x+1+arr.shape[1]] = arr


        return result_array
        
    def get_height_from_latlng(self, lat,lng):
        x = rdconverter.gps2X(lat, lng)
        y = rdconverter.gps2Y(lat, lng)
        return self.get_height(x,y)

    def show_tile(self, x, y):
        bladnr = self.get_tile(x, y)['properties']['bladnr']
        fp = self.get_filename(bladnr)
        img = rasterio.open(fp)
        show(img)







