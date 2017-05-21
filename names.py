from db import *

translation = {
	'altmer' : 'Altmer',
	'alt' : 'Altmer',
	'argonian' : 'Argonian',
	'arg' : 'Argonian',
	'bosmer' : 'Bosmer',
	'bos' : 'Bosmer',
	'breton' : 'Breton',
	'bre' : 'Breton',
	'dunmer' : 'Dunmer',
	'dun' : 'Dunmer',
	'imperial' : 'Imperial',
	'imp' : 'Imperial',
	'khajiit' : 'Khajiit',
	'kha' : 'Khajiit',
	'nord' : 'Nord',
	'nor' : 'Nord',
	'orc' : 'Orc',
	'orsimer' : 'Orc',
	'ors' : 'Orc',
	'redguard' : 'Redguard',
	'red' : 'Redguard',
	'man' : 'm',
	'male' : 'm',
	'm' : 'm',
	'woman' : 'f',
	'female' : 'f',
	'f' : 'f',
	'surname' : 's',
	's' : 's',
	'sur' : 's'
}

def parse(msg):
	if '!name' not in msg:
		return []
	tokens = msg.split('!name')
	try:
		command = [token.strip() for token in tokens[1].split()]
	except IndexError as e:
		return []
	
	# obtain the race of origin and the types of names (masc, fem, sur)
	race, flags = translation[command[0]], command[1:]
	try:
		flags = [translation[flag.lower()] for flag in flags]
	except KeyError as e:
		return ['no names for race `%s`' % e]
	
	unique = list(set(flags))
	
	names_by_type = { }
	for flag in unique:
		names_by_type[flag] = name_query(race, flag, flags.count(flag))
	
	output = []
	for flag in flags:
		output.append(names_by_type[flag].pop())
	return output
	
def message(names):
	return ' '.join(names)

def name_query(race, flag, count):
	con = connect()
	cur = con.cursor()
	
	query = cur.mogrify(
		'select name from names where race = %s and nametype = %s and '
		+ 'random() < 0.01 limit %s',
		(race, flag, count)
	)
	cur.execute(query)
	results = cur.fetchall()
	try:
		out = list(results[0])
	except IndexError as e:
		out = []
	return out
	
	


