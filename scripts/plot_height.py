 from hoogtekaart import height_map_nl

import numpy as np


from PIL import Image
from matplotlib import cm


def show_img(data, data2, i, type):
    print('img_{}_{}.png'.format(i,type))
    print(cm.gist_earth(data).shape)
    arr = np.where(data > 1000000, 0, data)
    min_ = np.min(arr)
    max_ = np.max(arr)
    arr = (arr-min_) / (max_-min_)
    arr = cm.gist_earth(arr)
    arr[data>1000000] = [1, 1, 1,  1]
    arr[data2>1000000] = [0, 0, 1,  1]
    im = Image.fromarray(np.uint8(arr*255))
    im.save('img_{}_{}.png'.format(i,type))


HMNL = height_map_nl.HeightMapNL()


# x,y = 144453, 401038
# x,y = 93670, 463998
x,y = 181990, 474479
size = 500
data = HMNL.get_height_area(x-size,y+size,x+size,y-size)
HMNL.dsm = True
data2 = HMNL.get_height_area(x-size,y+size,x+size,y-size)
show_img(data, data2, 1, 'test')

data[data2>1000] = -100
amount_of_water = data.shape[0] * data.shape[1]
building_count = np.sum(data>1000)
amount_of_rain_per_cell = amount_of_water/(amount_of_water-building_count)/1000
result = np.full(data.shape, 0.0)
for i in range(100):
    if i < 60:
        result[data<1000] += amount_of_rain_per_cell
    for x in range(1, data.shape[1]-1):
        for y in range(1, data.shape[0]-1):
            if data[y,x] < 1000:
                val = data[y,x]
                waterval = result[y,x]

                topdiff = val+waterval - data[y+1,x]+result[y+1,x]
                bottomdiff = val+waterval - data[y-1,x]+result[y-1,x]
                leftdiff = val+waterval - data[y,x-1]+result[y,x-1]
                rightdiff = val+waterval - data[y,x+1]+result[y,x+1]
                water_to_move = min(waterval, max([topdiff, bottomdiff, leftdiff, rightdiff]))
                total = 0
                if topdiff > 0:
                    total+=topdiff

                if leftdiff > 0:
                    total+=leftdiff

                if rightdiff > 0:
                    total+=rightdiff

                if bottomdiff > 0:
                    total+=bottomdiff

                if topdiff > 0:
                    result[y+1,x] += (topdiff/total) * water_to_move

                if leftdiff > 0:
                    result[y,x-1] += (leftdiff/total) * water_to_move

                if rightdiff > 0:
                    result[y,x+1] += (rightdiff/total) * water_to_move

                if bottomdiff > 0:
                    result[y-1,x] += (bottomdiff/total) * water_to_move

                if total > 0:
                    result[y,x] -= water_to_move

print(result)
result[data>1000] = 10000000
show_img(result, data2, 2, 'watertest')

























