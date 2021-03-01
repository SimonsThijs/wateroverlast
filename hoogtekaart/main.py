from height_map_nl import HeightMapNL
from coords import rdconverter

hmnl = HeightMapNL()
# leiden
lat, lng = (52.160790,4.490839)
# philipine
# lat, lng = (51.549,5.677)
x = rdconverter.gps2X(lat,lng)
y = rdconverter.gps2Y(lat,lng)
x = 94700
y = 463700
# hmnl.show_tile(x, y)
# (hmnl.get_height(x, y))

# print(hmnl.get_height_area(94650, 463700, 97000, 463400))
# print(hmnl.get_height_area(94650, 462750, 95600, 462200))


x1 = 94980.5
y1 = 462519.5

print(hmnl.get_height_area(x1, y1, x1+3, y1-3))
