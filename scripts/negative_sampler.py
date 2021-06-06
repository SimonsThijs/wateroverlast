

from coords import rdconverter

import json
import random
import math

import numpy as np

def load_data(file):
    with open(file, 'r') as file:
        data = json.load(file)
        return data




data = load_data('../data/parsed_w_precise_coords.json')

def random_circle(inner_radius, outer_radius):
	r = (outer_radius-inner_radius) * math.sqrt(random.random()) + inner_radius
	theta = random.random() * 2 * math.pi
	x = r * math.cos(theta)
	y = r * math.sin(theta)
	return x, y


# we sample data by taking a position close to the possitive sample
# the datetime is not altered for now
def sample_random(data):
	stop = False
	while not stop:
		d = random.choice(data)
		# print(d['google_results'][0])
		if 'google_results' in d and len(d['google_results']) > 0 and d['google_results'][0]['geometry']['location_type'] != 'APPROXIMATE':
			stop = True
			lat = d['google_results'][0]['geometry']['location']['lat']
			lng = d['google_results'][0]['geometry']['location']['lng']


	rdx = rdconverter.gps2X(lat,lng)
	rdy = rdconverter.gps2Y(lat,lng)
	ranx, rany = random_circle(500, 1500)
	rdx += ranx
	rdy += rany

	return rdconverter.RD2lat(rdx, rdy), rdconverter.RD2lng(rdx, rdy), d['date']

print("lat,lng,date")
for i in range(1,30000):
	lat,lon,date = sample_random(data)
	print("{}, {}, {}".format(lat, lon, date))


