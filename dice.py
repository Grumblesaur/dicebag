import re
from random import randrange
class DiceParserException(Exception):
	pass

def roll(die):
	try:
		dice, sides = [int(x) for x in die.split('d')]
	except (ValueError, TypeError) as e:
		print(e)
		raise DiceParserException(die + ' (bad syntax)')
	else:
		if dice < 0 or sides < 0:
			raise DiceParserException(die + ' (values must be positive)')
		if dice > 16384 or sides > 1024:
			raise DiceParserException(die + ' (dice too large)')
	return sum([randrange(sides) + 1 for x in range(dice)])
	
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
	command = msg.replace('!roll', '')
	command = command.replace(' ','')
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
			raise DiceParserException('oh my fucking god')
		# got 99 problems and regexes are all of them
		die, modint = (re.split('[\-\+]+', die), (die, 0))[modsym == '']
	except (TypeError, ValueError) as e:
		print(e); raise DiceParserException('bad +/- syntax')
		
	#grab dice info
	die = die.split('d')
	try:
		dice, sides, drop = (die[:] + [0], die[:])[len(die) == 3]
	except Exception as e:
		print(e); raise DiceParserException('bad d syntax')
	
	results = []
	for i in range(repeat):
		results.append(('%s.' % str(i+1), roll_with_drop(
			int(dice), int(sides), int(drop), int(modint), modsym)
			)
		)
	
	return results
	
def parse(msg):
	tokens = msg.casefold().split()
	rolls = []
	for i in range(len(tokens) - 1):
		if tokens[i] == '!roll':
			try:
				rolls.append((roll(tokens[i+1]), tokens[i+1]))
			except DiceParserException as e:
				print('bad roll:', e)
				rolls.append(('error', str(e)))
	return rolls

def dice_message(rolls, msg):
	try:
		username = msg.author.nick
	except AttributeError as e:
		username = msg.author.name
	return ('User %s rolled:\n' % username) + '\n'.join(
		['%s (%s)' % roll for roll in rolls]
	)