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
