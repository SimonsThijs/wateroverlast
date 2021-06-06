
import json

print('{"data":[')
with open('final.json', 'r') as file:
    data = json.load(file)
    for d in data['data']:
        mess = d['message'].lower()
        if 'wateroverlast' in mess:
            print(json.dumps(d) + ", ")

print(']}')