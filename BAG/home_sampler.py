from coords import rdconverter

import numpy as np
import pandas as pd
import geopy.distance

import os

LATDEGREE = 111000

class HomeSampler(object):
	"""docstring for HomeSampler"""
	def __init__(self):
		super(HomeSampler, self).__init__()
		dire = os.path.dirname(__file__)
		if dire:
			dire += '/'
		self.df = pd.read_csv(dire + 'data/verblijfplaatsen_shorter.csv')
		self.df = self.df.dropna(axis=0)
		self.df = self.df.astype({"x": float, "y": float})
		# self.df = self.df.set_index(['x','y'])

	def sample_in_range(self, x, y, max_range, min_range, n):
		
		data = self.df.loc[(self.df['x']<=x+max_range)&(self.df['x']>=x-max_range)&(self.df['y']<=y+max_range)&(self.df['y']>=y-max_range)]
		data['xdiff'] = data['x'] - x
		data['ydiff'] = data['y'] - y
		data['dist'] = (data['xdiff']*data['xdiff']+data['ydiff']*data['ydiff'])**0.5
		data = (data[(data['dist']<=max_range)&(data['dist']>=min_range)])

		if len(data) == 0:
			print(x,y)
			return []
		if len(data) < n:
			data = data.sample(len(data))[['x','y']]
		else:
			data = data.sample(n)[['x','y']]

		x = zip(data['x'].tolist(), data['y'].tolist())
		return list(x)

	def sample_location(self, n):
		rows = self.df.sample(n)
		# print(row['pos'].values)
		lst = []
		# print(rows)
		for row in rows:
			# print(row)
			pos = row.split()
			x = float(pos[0])
			y = float(pos[1])
			lat = rdconverter.RD2lat(x,y)
			lon = rdconverter.RD2lng(x,y)
			lst.append((lat, lon))
		return lst



if __name__ == '__main__':
	HM = HomeSampler()

	print(HM.sample_in_range(155000, 463000, 1500, 1000,10))

	print(HM.sample_in_range(155000, 463000, 1500, 1000,10))



	# print("lat,lng")
	# # result = (HM.sample_location(1500000))
	# for r in result:
	# 	print(str(r[0]) + ',' + str(r[1]))






