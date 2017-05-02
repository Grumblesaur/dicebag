from parser import roll
from dice_error import DiceParserException

def parse_with_math(msg):
	try:
		die, repeat = ((command, 1), command.split('^'))['^' in command]
		repeat = abs(int(repeat)) or 1
	except (ValueError, TypeError) as e:
		print(e); raise DiceParserException('bad ^ syntax')

	return [roll(die) for i in range(repeat)]
	
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
