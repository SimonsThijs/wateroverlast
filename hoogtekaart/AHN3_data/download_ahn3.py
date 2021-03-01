import json
import os

template = "curl --output AHN3_data/{}.zip https://download.pdok.nl/rws/ahn3/v1_0/5m_dtm/M5_{}.ZIP"

with open('bladindexen.json') as json_file:
	data = json.load(json_file)
	for blad in data['features']:
		bladnr = blad['properties']['bladnr']
		command = template.format(bladnr, bladnr.upper())
		os.system(command)

# use command 'unzip' to unzip the downloaded files


# use this to download any of the files that failed downloading the first time
# todo = ["64ez1",
# "26an1",
# "70hn2"]
# for blad in todo:
# 	bladnr = blad
# 	command = template.format(bladnr, bladnr.upper())
# 	os.system(command)
