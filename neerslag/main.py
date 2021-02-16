from neerslag.precipitation_nl import PrecipitationNL

prNL = PrecipitationNL()

som = 0
for hour in range(24):
	for minute in range(0,60,5):
		som += (prNL.get_precipation_data(2017, 1, 1, hour, minute, 52.103, 5.179))

print(som)