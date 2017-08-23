import random
import char
import names
import dice

races = [
	race for race in names.translation.keys() if len(
		names.translation[race]
	) > 1
]

genders = [
	gender for gender in names.translation.keys() if len(
		names.translation[gender]
	) < 2 and gender[0] != 's'
]

def parse(msg):
	if "!gen" not in msg:
		return []
	tokens = msg.casefold().split('!gen')
	try:
		tokens = [token.strip() for token in tokens[1].split()]
	except IndexError as e:
		argc = 0
	else:
		argc = len(tokens)
	
	race = names.translation[random.choice(races)]
	gender = names.translation[random.choice(genders)]
	
	if argc >= 1:
		race = names.translation[token[0]] if token[0] in races else race
	if argc >= 2:
		gender = names.translation[token[1]] if token[1] in genders else gender
	
	forename = names.name_query(race, gender, 1)
	surname = names.name_query(race, 's', 1)
	full_name = '-'.join(forename + surname).lower()
	
	stats = dice.parse('!roll 4d6l1^6')[0][1]
	
	
	
