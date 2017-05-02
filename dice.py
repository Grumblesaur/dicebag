from parser import roll
from dice_error import DiceParserException

def calculate_repeats(msg):
	try:
		die, repeat = ((msg, 1), msg.split('^'))['^' in msg]
		repeat = abs(int(repeat)) or 1
	except (ValueError, TypeError) as e:
		print(e); raise DiceParserException('bad ^ syntax')

	return [roll(die) for i in range(repeat)]
	
def parse(msg):
	if '!roll' not in msg: return []
	tokens = msg.casefold().split('!roll')
	tokens = [token.strip() for token in tokens if token]
	rolls = []
	for token in tokens:
		try:
			rolls.append((token, calculate_repeats(token)))
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
