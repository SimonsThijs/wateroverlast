import json
import os
import time
import warnings
import io

import fiona
from osgeo import gdal
from osgeo import ogr
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import xarray as xr
from owslib.wfs import WebFeatureService
from shapely.geometry import mapping, shape, LineString, Polygon, Point
from shapely.strtree import STRtree
from tqdm import tqdm
import rasterio
import rasterio.features as features
from owslib.wcs import WebCoverageService

def extent2polygon(extent):
    """Make a Polygon of the extent of a matplotlib axes"""
    nw = (extent[0], extent[2])
    no = (extent[1], extent[2])
    zo = (extent[1], extent[3])
    zw = (extent[0], extent[3])
    polygon = Polygon([nw, no, zo, zw])
    return polygon

def get_bag_geopandas(x_min, y_max, x_max, y_min):

    url = "http://geodata.nationaalgeoregister.nl/bag/wfs/v1_1?service=wfs&version=2.0.0&request=GetFeature&typeName=pand&bbox={},{},{},{}&outputFormat=application%2Fjson%3B%20subtype%3Dgeojson".format(
        x_min, y_min, x_max, y_max)

    response = requests.get(url)

    gdf = gpd.geopandas.read_file(io.BytesIO(response.content))
    print(gdf)
    return gdf

def get_ahn3(x_min, y_max, x_max, y_min, dsm=True):
    my_wcs = WebCoverageService('https://geodata.nationaalgeoregister.nl/ahn3/wcs', version='1.0.0')

    identifier = 'ahn3_05m_dsm' if dsm else 'ahn3_05m_dtm'
    output=my_wcs.getCoverage(identifier=identifier, width=2*round(x_max-x_min), height=2*round(y_max-y_min), bbox=(x_min,y_min,x_max,y_max), format='GEOTIFF_FLOAT32', CRS='EPSG:28992')
    f=open('tmp.tif','wb')
    f.write(output.read())
    f.close()

    raster = gdal.Open('tmp.tif', gdal.GA_Update)
    return raster

all_ = [
            "bak",
            "begroeidterreindeel",
            "bord",
            "buurt",
            "functioneelgebied",
            "gebouwinstallatie",
            "installatie",
            "kast",
            "kunstwerkdeel",
            "mast",
            "onbegroeidterreindeel",
            "ondersteunendwaterdeel",
            "ondersteunendwegdeel",
            "ongeclassificeerdobject",
            "openbareruimte",
            "openbareruimtelabel",
            "overbruggingsdeel",
            "overigbouwwerk",
            "overigescheiding",
            "paal",
            "pand",
            "plaatsbepalingspunt",
            "put",
            "scheiding",
            "sensor",
            "spoor",
            "stadsdeel",
            "straatmeubilair",
            "tunneldeel",
            "vegetatieobject",
            "waterdeel",
            "waterinrichtingselement",
            "waterschap",
            "wegdeel",
            "weginrichtingselement",
            "wijk"
          ]

def get_bgt(extent, layer="onbegroeidterreindeel", cut_by_extent=True):
    """
    Get geometries within an extent or polygon from the Basis Registratie Grootschalige Topografie (BGT)
    Parameters
    ----------
    extent : list or tuple of length 4 or shapely Polygon
        The extent (xmin, xmax, ymin, ymax) or polygon for which shapes are
        requested.
    layer : string, optional
        The layer for which shapes are requested. The default is "waterdeel".
    cut_by_extent : bool, optional
        Only return the intersection with the extent if True. The default is True
    Returns
    -------
    gdf : GeoPandas GeoDataFrame
        A GeoDataFrame containing all geometries and properties.
    """

    api_url = 'https://api.pdok.nl'
    url = '{}/lv/bgt/download/v1_0/full/custom'.format(api_url)
    body = {"format": "citygml",
            "featuretypes": [layer]}

    if isinstance(extent, Polygon):
        polygon = extent
    else:
        polygon = extent2polygon(extent)

    body['geofilter'] = polygon.to_wkt()

    headers = {'content-type': 'application/json'}

    response = requests.post(url, headers=headers, data=json.dumps(body))

    # check api-status, if completed, download
    if response.status_code in range(200, 300):
        running = True
        href = response.json()["_links"]["status"]["href"]
        url = '{}{}'.format(api_url, href)

        while running:
            response = requests.get(url)
            if response.status_code in range(200, 300):
                status = response.json()['status']
                if status == "COMPLETED":
                    running = False
                else:
                    time.sleep(2)
            else:
                running = False
    else:
        msg = 'Download of bgt-data failed: {}'.format(response.text)
        raise(Exception(msg))

    href = response.json()["_links"]["download"]["href"]
    response = requests.get('{}{}'.format(api_url, href))


    fc = fiona.BytesCollection(bytes(response.content))
    gdf = gpd.GeoDataFrame.from_features(
        [feature for feature in fc], crs='epsg:28992')

    # remove double features by removing features with an eindRegistratie
    gdf = gdf[gdf['eindRegistratie'].isna()]

    print(gdf.columns)
    # print(gdf[['plus-fysiekVoorkomenOnbegroeidTerrein']])

    # re-order columns
    columns = [col for col in gdf.columns if not col ==
               'geometry'] + ['geometry']

    gdf = gdf[columns]

    if cut_by_extent:
        gdf.geometry = gdf.intersection(polygon)
        gdf = gdf[~gdf.is_empty]

    print(gdf)
    return gdf

def add_layer(x,y,d, layer, dataset, i):
    gdf = get_bgt((x-d,x+d, y-d,y+d), layer=layer)[['geometry']]
    shp = gdal.OpenEx(gdf.to_json())
    lyr = shp.GetLayer(0)

    dataset.GetRasterBand(i).SetNoDataValue(0)
    gdal.RasterizeLayer(dataset, [i], lyr, burn_values=[255]) 

water = ['waterdeel',]
verhard = ['onbegroeidterreindeel', '']

def get_bgt_download_url(extent, layer):
    """
    Get geometries within an extent or polygon from the Basis Registratie Grootschalige Topografie (BGT)
    Parameters
    ----------
    extent : list or tuple of length 4 or shapely Polygon
        The extent (xmin, xmax, ymin, ymax) or polygon for which shapes are
        requested.
    layer : string, optional
        The layer for which shapes are requested. The default is "waterdeel".
    cut_by_extent : bool, optional
        Only return the intersection with the extent if True. The default is True
    Returns
    -------
    gdf : GeoPandas GeoDataFrame
        A GeoDataFrame containing all geometries and properties.
    """

    api_url = 'https://api.pdok.nl'
    url = '{}/lv/bgt/download/v1_0/full/custom'.format(api_url)
    body = {"format": "citygml",
            "featuretypes": layer}

    if isinstance(extent, Polygon):
        polygon = extent
    else:
        polygon = extent2polygon(extent)

    body['geofilter'] = polygon.to_wkt()

    headers = {'content-type': 'application/json'}

    response = requests.post(url, headers=headers, data=json.dumps(body))

    if response.status_code in range(200, 300):
        running = True
        href = response.json()["_links"]["status"]["href"]
        url = '{}{}'.format(api_url, href)

        while running:
            response = requests.get(url)
            if response.status_code in range(200, 300):
                status = response.json()['status']
                # print(status)
                if status == "COMPLETED":
                    running = False
                else:
                    time.sleep(1)
            else:
                running = False
    else:
        msg = 'Download of bgt-data failed: {}'.format(response.text)
        raise(Exception(msg))

    url = response.json()["_links"]["download"]["href"]
    return url


def get_all_data(x,y,d):
    layers = ['begroeidterreindeel']
    ahn_tif = get_ahn3(x-d, y+d, x+d, y-d)

    geot = ahn_tif.GetGeoTransform()
    drv_tiff = gdal.GetDriverByName("GTiff")
    chn_ras_ds = drv_tiff.Create('tmp2.tif', ahn_tif .RasterXSize, ahn_tif .RasterYSize, len(layers), gdal.GDT_Byte)
    chn_ras_ds.SetGeoTransform(geot)

    
    count = 1
    for l in layers:
        add_layer(x,y,d, l, chn_ras_ds, count)
        count+=1


    ahn_tif, chn_ras_ds, shp, lyr = None, None, None, None


x,y = 93660.0, 463877.0
d = 100.0


bbox_nl = (-7000, 300000, 289000, 629000)
width = bbox_nl[1] - bbox_nl[0]
height = bbox_nl[3] - bbox_nl[2]
n=100
m=100
for i in range(n):
    for j in range(m):
        w_d = width/n
        h_d = height/m
        bbox = (bbox_nl[0]+w_d*i, bbox_nl[0]+w_d*(i+1), bbox_nl[2]+h_d*j, bbox_nl[2]+h_d*(j+1))
        url = get_bgt_download_url(bbox, ['wegdeel', 'onbegroeidterreindeel', 'begroeidterreindeel', 'ondersteunendwegdeel', 'waterdeel'])
        print(bbox, url)
        time.sleep(0.5)



