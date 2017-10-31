from dice_error import DiceParserException
from random import randint
import math

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
	
	def __pow__(self, other):
		return DiceValue(self.value ** other.value)
	
	def maximum(self, other):
		return DiceValue(max(self, other))
	
	def minimum(self, other):
		return DiceValue(min(self, other))
	
	def logarithm(self, other):
		return DiceValue(int(math.log(other.value, self.value)))
	
	def __eq__(self, other):
		return DiceValue(self.value if self.value == other.value else 0)
	
	def __lt__(self, other):
		return self.value < other.value
	
	def __gt__(self, other):
		return self.value > other.value
	
	def factorial(self):
		return DiceValue(math.factorial(self.value))
	
	
	
