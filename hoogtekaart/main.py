from height_map_nl import HeightMapNL
from coords import rdconverter

hmnl = HeightMapNL()
# leiden
lat, lng = (52.160790,4.490839)
# philipine
# lat, lng = (51.549,5.677)
x = rdconverter.gps2X(lat,lng)
y = rdconverter.gps2Y(lat,lng)
hmnl.show_tile(x, y)
print(hmnl.get_height(x, y))
