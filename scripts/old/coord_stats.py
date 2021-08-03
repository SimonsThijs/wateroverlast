from coords import rdconverter
import json

import numpy as np

def load_data(file):
    with open(file, 'r') as file:
        data = json.load(file)
        return data



def calc_area(bounds):
	ne = bounds['northeast']
	ne_x = rdconverter.gps2X(ne['lat'], ne['lng'])
	ne_y = rdconverter.gps2X(ne['lat'], ne['lng'])
	sw = bounds['southwest']
	sw_x = rdconverter.gps2X(sw['lat'], sw['lng'])
	sw_y = rdconverter.gps2X(sw['lat'], sw['lng'])

	diff_x = abs(ne_x-sw_x)
	diff_y = abs(ne_y-sw_y)

	return diff_y*diff_x

data = load_data('parsed_w_coords.json')

stats = {'nodata': 0, 'multiple_results': 0, 'bounds': 0}

area_list = []

for d in data:
	if 'google_results' in d:
		gr = d['google_results']
		if len(gr) > 1:
			stats['multiple_results'] += 1
		else:
			r = gr[0]
			t = r['geometry']['location_type']
			if t not in stats:
				stats[t] = 1
			else:
				stats[t] += 1

			if 'bounds' in r['geometry']:
				stats['bounds'] += 1
				print(r['geometry']['bounds'])
				area = calc_area(r['geometry']['bounds'])
				area_list.append(area)
				print(area)


	else:
		stats['nodata'] += 1
	
al = np.asarray(area_list)
stats['area_avg'] = np.mean(al)
stats['area_std'] = np.std(al)

print(stats)



