import sys
import unittest
import numpy as np
from fraudfeature import parse_normal_time

class parse_normal_time_test(unittest.TestCase):
	def setup(self):
		self.vals = np.array(['20190101', '20190305', '20191201', '20181225'])

	def test_parse_noral_time(self):
		result = parse_normal_time(self.vals)
		print(result)


