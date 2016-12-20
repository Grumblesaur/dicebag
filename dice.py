import re
from random import randrange
class DiceParserException(Exception):
	pass

def roll_with_drop(dice, sides, drop, addend, sign):
	# no negative args please
	if dice < 0 or sides < 0 or drop < 0:
		raise DiceParserException('value(s) negative')
	# no bot-crashing args please
	if dice > 2 ** 14 or sides > 2 ** 10 or drop > dice:
		raise DiceParserException('value(s) too large')
	
	# roll XdYdropZ
	roll = sum(sorted([randrange(sides)+1 for die in range(dice)])[drop:])
	# return value with modifier
	return {'+' : roll + addend, '-' : roll - addend, '': roll}[sign]

def parse_with_math(msg):
	command = msg.replace(' ','')
	#grab repetitions
	try:
		die, repeat = ((command, 1), command.split('^'))['^' in command]
		repeat = int(repeat) if int(repeat) >= 1 else 1
	except (ValueError, TypeError) as e:
		print(e); raise DiceParserException('bad ^ syntax')
	
	#grab modifiers
	try:
		modsym = ('','+')['+' in die] + ('', '-')['-' in die]
		if modsym == '+-':
			raise ValueError('operation +- not supported')
		# got 99 problems and regexes are all of them
		die, modint = (re.split('[\-\+]+', die), (die, 0))[modsym == '']
	except (TypeError, ValueError) as e:
		print(e); raise DiceParserException('bad +/- syntax')
		
	#grab dice info
	die = die.split('d')
	try:
		dice, sides, drop = (die[:] + [0], die[:])[len(die) == 3]
		dice, sides, drop, modint = [
			int(x) for x in (dice, sides, drop, modint)
		]
	except Exception as e:
		print(e); raise DiceParserException('bad d syntax')
	
	return [roll_with_drop(dice, sides, drop, modint, modsym)
		for i in range(repeat)
	]
	
def parse(msg):
	tokens = msg.casefold().split('!roll')
	tokens = [token.strip() for token in tokens if token]
	rolls = []
	for token in tokens:
		try:
			rolls.append((token, parse_with_math(token)))
		except DiceParserException as e:
			print('bad roll:', token, e)
	return rolls

def dice_message(rolls, msg=None):
	try:
		username = msg.author.nick
	except AttributeError as e:
		username = 'x' # msg.author.name
	return 'User %s rolled:\n%s' % (
		username,
		'\n'.join(['\n'.join(
				[result[0]]
				+ ['  %s' % die for die in result[1]]
			) for result in rolls]
		)
	)
