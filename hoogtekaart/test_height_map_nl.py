import unittest

from hoogtekaart.height_map_nl import HeightMapNL

class TestHeightMapNL(unittest.TestCase):

	def test_get_height(self):
		HMNL = HeightMapNL()

		x = 135096.47
		y = 444993.09
		height = HMNL.get_height(x,y)
		self.assertTrue(abs(height - 1.6560363) < 0.00001)

		x = 93771.40
		y = 463803.69
		height = HMNL.get_height(x,y)
		self.assertTrue(abs(height - 12.635) < 0.001)

		x = 93770
		y = 463805
		height = HMNL.get_height(x,y)
		self.assertTrue(abs(height - 12.635) < 0.001)

		# x = 95900
		# y = 453789
		# height = HMNL.get_height(x,y)
		# HMNL.show_tile(x,y)
		# print(height)
		# self.assertTrue(abs(height - -3.911) < 0.001)


if __name__ == '__main__':
	unittest.main()