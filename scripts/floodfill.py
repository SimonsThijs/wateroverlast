

import pandas as pd


def flood_fill(data):
    dtm = data['height_dtm']
    begin = (int(dtm.shape[0]/2), int(dtm.shape[1]/2))
    q = [begin]
    done = []

    while len(q) > 0:
        to_check = q.pop(0)

        if dtm[to_check] > 1000 and to_check not in done:
            # is a house
            done.append(to_check)
            y = to_check[0]
            x = to_check[1]
            q.append((y+1,x))
            q.append((y-1,x))
            q.append((y,x+1))
            q.append((y,x-1))

    return done

def get_house_radius_xymax(data, x_mode):
    ff = data['flood_fill']
    x_max = 0
    for f in ff:
        if f[x_mode] > x_max:
            x_max = f[x_mode]

    return x_max-100

def get_house_radius_xymin(data, x_mode):
    ff = data['flood_fill']
    x_min = 100000
    for f in ff:
        if f[x_mode] < x_min:
            x_min = f[x_mode]

    return abs(x_min-100)



        




df = pd.read_pickle('save.pkl').reset_index(drop=True)




first = df.iloc[1]

first['flood_fill'] = flood_fill(first)
first['radius_left'] = get_house_radius_xymin(first, 1)
first['radius_right'] = get_house_radius_xymax(first, 1)
first['radius_top'] = get_house_radius_xymin(first, 0)
first['radius_bottom'] = get_house_radius_xymax(first, 0)

print(first)




