import json
import os
import time
import warnings
import io

import geopandas as gpd
import numpy as np
import pandas as pd
import requests
import fiona

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

def download_zip(url):
	api_url = 'https://api.pdok.nl'
	response = requests.get('{}{}'.format(api_url, url))



def iterate():
	bbox_nl = -7000, 300000, 289000, 629000
	width = bbox_nl[1] - bbox_nl[0]
	height = bbox_nl[3] - bbox_nl[2]
	n=300
	m=340
	for i in range(n):
	    for j in range(m):
			w_d = width/n
			h_d = height/m
		    bbox = (bbox_nl[0]+w_d*i, bbox_nl[0]+w_d*(i+1), bbox_nl[2]+h_d*j, bbox_nl[2]+h_d*(j+1))
		    url = get_bgt_download_url(bbox, ['wegdeel', 'onbegroeidterreindeel', 'begroeidterreindeel', 'ondersteunendwegdeel', 'waterdeel'])


iterate()

