import pandas as pd
import numpy as np
import Levenshtein
import matplotlib.pyplot as plt
from unidecode import unidecode

from datetime import datetime, timedelta
import json
import re

strfformat = "%Y-%m-%d %H:%M:%S"


def load_data(file):
    with open(file, 'r') as file:
        data = json.load(file)
        return data['data']

def remove_number_from_address(string):
    match = re.search(r' \d+', string)
    if not match:
        raise Exception("Cannot find a number in the address")
    return string[0:match.start()] + string[match.end():len(string)]

def fix_adresses(data):
    keep = []
    for m in data:
        match_address = re.search(r'\d+', m['address'])

        GG0_match = re.search(r'\d\dGG0\d', m['address'])
        if GG0_match:
            # if GG0 in message, it probably has a wrong house number
            number_str = GG0_match.group()[0:2]
            if match_address and number_str == match_address.group():
                m['address'] = remove_number_from_address(m['address'])
                keep.append(m) 

        elif match_address:
            # number found
            match_message = re.search(' {}[A-Z]+'.format(match_address.group()), m['message'])
            match_message2 = re.search(' {} '.format(match_address.group()), m['message'])
            if match_message and match_message2:
                # number in this endcode but also somewhere else so we keep it
                keep.append(m)
            elif match_message:
                m['address'] = remove_number_from_address(m['address'])
                keep.append(m)
            else:
                keep.append(m)


        else:
            # no number in the address so we keep it withouth changing anything
            keep.append(m)

    

    return keep

def get_date_time(d):
    return datetime.strptime(d['date'], strfformat)

def remove_double(data):
    # some messages are emitted twice for some reason
    data.reverse()
    c = 0
    values = []
    compare_key = 'address'
    delta = timedelta(hours=3)
    for d in data:
        datetimecurrent = get_date_time(d)
        i = c
        while i+1 < len(data) and get_date_time(data[i+1]) < datetimecurrent + delta:
            distance = Levenshtein.distance(d[compare_key], data[i+1][compare_key])
            values.append(distance)
            if distance <= 5:
                data.remove(data[i+1])
            i += 1

        c += 1
        

    # used for determining the cutoff point
    # plt.hist(values, color = 'blue', edgecolor = 'black',bins = int(100/1))
    # plt.show()


    return data

def contains_wateroverlast(data):
    keep = []
    for d in data:
        if 'wateroverlast' in d['message'].lower():
            keep.append(d)

    return keep

def check_address_with_message(data):
    # this function can used for validation
    for d in data:
        if not d['correct']: 
            address = unidecode(d['address'].split(',')[0].lower())
            match = re.search(r"^\d?\d?[`a-z ]+", address)
            # print(match.group())
            if unidecode(match.group()) not in unidecode(d['message'].lower()):
                print(d['message'], '-----', d['address'], '----- ')


    return data

def print_json(data):
    to_print = ''
    to_print += '['
    for d in data:
        to_print += json.dumps(d) + ",\n"


    to_print = to_print[0:-2]
    to_print += ']\n'
    print(to_print)

def delete_empty_address(data):
    keep = []
    for d in data:
        if d['address']:
            keep.append(d)

    return keep

def patch(data):
    patch_data = pd.read_csv('patch.txt', delimiter=' -----', engine='python', header=None)
    patch_data.columns = ['m', 'old', 'new']
    mutations = {}
    for i, p in patch_data.iterrows():
        # p2 = list(p)
        ind = p['m']
        old = p['old'][1:]
        new = '  '
        if str(p['new']) != 'nan':
            new = p['new'][1:]

        correct_value = new
        delete = False
        if ind[0:2] == "# ":
            correct_value = old
            ind = ind[2:]

        if new == "delete" or new == "delete " or new == " delete":
            delete = True

        mutation = {'delete': delete, 'correct_value': correct_value}
        mutations[ind] = mutation

    count = 0
    keep = []
    for d in data:
        if d['message'] in mutations:
            if mutations[d['message']]['delete']:
                pass
            else:
                d['address'] = mutations[d['message']]['correct_value']
                d['correct'] = True
                keep.append(d)
        else:
            d['correct'] = False
            keep.append(d)

    return keep

def check_oude_nieuwe(data):
    for d in data:
        m = d['message'].lower()
        a = d['address'].lower()
        for w in ['oude', 'oud', 'nieuw', 'nieuwe']:
            if (w in m and w not in a) or (w in a and w not in m):
                print(m, "=========", a)



def main():
    data = load_data('final.json')
    data = patch(data)
    data = delete_empty_address(data)
    data = contains_wateroverlast(data)
    data = fix_adresses(data)
    data = remove_double(data)
    # check_address_with_message(data)
    # check_oude_nieuwe(data)

    print_json(data)    


if __name__ == '__main__':
    main()








