tracker = { }
keywords = {
	'+' : ['plus', 'add', 'increment', 'inc', '+'],
	'-' : ['minus', 'subtract', 'decrement', 'dec', '-'],
	'=' : ['set', '=', ':'],
	'*' : ['make', 'create', 'new', '*'],
	'~' : ['destroy', 'delete', '~']
}

def save_config():
	with open('char.config', 'w') as c:
		c.write(str(tracker))
	
def load_config():
	global tracker
	with open('char.config', 'r') as c:
		tracker = eval(c.read())

def parse(msg):
	if '!char' not in msg:
		return []
	
	tokens = msg.casefold().split('!char')
	try:
		tokens = [token.strip() for token in tokens[1].split()]
	except IndexError as e:
		return []

	argc = len(tokens)
	out = []
	if argc == 4:
		out = parse_four(tokens)
	if argc == 3:
		out = parse_three(tokens)
	if argc == 2:
		out = parse_two(tokens)
	if argc == 1:
		out = parse_one(tokens)
	
	return out


def parse_four(tokens):
	name, field, keyword, value = tokens
	out = []
	try:
		value = int(value)
	except Exception as e:
		out = ['%s' % e]
	try:
		if keyword in keywords['+']:
			tracker[name][field] += value
		elif keyword in keywords['-']:
			tracker[name][field] -= value
		elif keyword in keywords['=']:
			tracker[name][field] = value
	except KeyError as e:
		if name in e:
			out = ['invalid char: `%s\'' % name]
		elif field in e:
			out = ['field `%s\' did not exist for %s; defaulting to 0'
				% (second, first)
			]
			tracker[name][field] = 0
	else:
		out = ['%s: %s = %d' % (name, field, tracker[name][field])]
	
	return out

def parse_three(tokens):
	return parse_four(tokens + [1])

def parse_two(tokens):
	first, second = tokens
	out = []
	if first in keywords['*']:
		tracker[second] = { }
		out = ['created new char `%s\'' % second]
	elif first in keywords['~']:
		try:
			del tracker[second]
		except KeyError as e:
			out = []
		else:
			out = ['removed char `%\'' % second]
	else:
		if first in tracker.keys():
			if second in tracker[first].keys():
				out = ['%s: %s = %d' % first, second, tracker[first][second]]
			else:
				tracker[first][second] = 0
				out = ['field `%s\' did not exist for %s; defaulting to 0'
					% (second, first)
				]
		else:
			out = ['char `%s\' does not exist' % first]
	return out

def parse_one(tokens):
	try:
		out = [tokens[0]] + [pair for pair in tracker[tokens[0]].items()]
	except KeyError as e:
		out = ['char `%s\' does not exist' % tokens[0]]
	return out

def message(feedback):
	out = ''
	if len(feedback) == 1:
		out = feedback[0]
	else:
		out = "%s:\n\t" % feedback[0]
		pairs = feedback[1:]
		out += "\n\t".join(
			['%s = %d' % pair for pair in pairs]
		)
	return out



 
