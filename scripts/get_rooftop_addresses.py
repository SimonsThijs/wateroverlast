
import json

def load_data(file):
    with open(file, 'r') as file:
        data = json.load(file)
        return data

def print_json(data):
    to_print = ''
    to_print += '['
    for d in data:
        to_print += json.dumps(d) + ",\n"

    to_print = to_print[0:-2]
    to_print += ']\n'
    print(to_print)



data = load_data('../data/parsed_w_coords.json')
results = []
for d in data:
	if 'google_results' in d:
		gr = d['google_results']
		if len(gr) == 1:
			r = gr[0]
			t = r['geometry']['location_type']
			if t == 'ROOFTOP' or t == 'RANGE_INTERPOLATED':
				results.append(d)

print_json(results)











