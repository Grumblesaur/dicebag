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
	
	race, flags = translation[command[0]], command[1:]
	try:
		flags = [translation[flag.lower()] for flag in flags]
	except KeyError as e:
		return ['bad name: `%s`' % e]
	return [name_query(race, flag) for flag in flags]
	
def message(names):
	return ' '.join(names)

def name_query(race, flag):
	con = connect()
	cur = con.cursor()
	
	query = cur.mogrify(
		'select name from names where race = %s and nametype = %s and '
		+ 'random() < 0.01 limit 1',
		(race, flag)
	)
	print(query)
	cur.execute(query)
	results = cur.fetchall()
	print(results)
	return results[0][0]
	


