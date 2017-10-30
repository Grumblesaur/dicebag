from dice_error import DiceParserException
from random import randint


class DiceValue(object):
	def __init__(self, number):
		self.value = number
	
	def concatenate(self, other):
		return DiceValue(int(str(self.value) + str(other.value)))
		
	def die(self, other, op=None, slicer=None):
		if op is None:
			return DiceValue(
				sum(
					[randint(1, other.value) for x in range(self.value)]
				)
			)
		return DiceValue(
			sum(
				sorted(
					[randint(1, other.value) for x in range(self.value)]
				)[slicer.value:]
			)
		) if op == 'l' else DiceValue(
			sum(
				reversed(
					sorted(
						[randint(1, other.value) for x in range(self.value)]
					)[slicer.value:]
				)
			)
		)
	
	def __add__(self, other):
		return DiceValue(self.value + other.value)
	
	def __sub__(self, other):
		return DiceValue(self.value - other.value)
	
	def __mul__(self, other):
		return DiceValue(self.value * other.value)
	
	def __floordiv__(self, other):
		return DiceValue(self.value // other.value)
	
	def __mod__(self, other):
		return DiceValue(self.value % other.value)
	
	def __matmul__(self, other):
		return DiceValue(self.value ** other.value)
	
	
	
	
	
