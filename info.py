helptext = {
	'roll' : [
		"valid operations:",
		"d : binary operator, for a roll MdN, rolls M dice each with N sides",
		"l : with d as MdNlX, drops the lowest X dice from the MdN roll",
		"h : with h as MdNhX, drops the highest X dice from the MdN roll",
		"* : binary operator, multiplies its operands",
		"/ : binary operator, floor-divides its left operand by its right",
		"+ : binary operator, adds its operands",
		"- : binary operator, subtracts its right operator from its left",
		"^ : repetition marker, when given roll^Y, repeats the roll Y times"
	],
	'initiative' : [
		"valid operations:",
		"create <order name> : adds a new turn order order_name to the tracker",
		"add <order name> <actor name> <initiative> : adds a new actor",
		"remove <order name> <actor name> : removes an actor",
		"start <order name> : sorts turn order and enables check and next",
		"next <order name> : advances the turn order and outputs the actor",
		"check <order name> : outputs current actor without advancing the order",
		"stop <order name> : returns turn order to its initial state"
			+ " with all actors not queued for removal left in place",
		"clear <order name> : empties the order (must be stopped first)",
		"delete <order name> : removes the turn order from the tracker"
	],
	'' : [
		"valid help keywords are:",
		"roll",
		"initiative",
		"name",
		"type '!help <keyword>' for more information"
	],
	'char' : [
		"valid operations:",
		"create <char-name> : adds a character to the tracker",
		"delete <char-name> : removes a character from the tracker",
		"<char-name>        : view <char-name>'s stat array",
		"all                : view the names of all characters in the tracker",
		"<char-name> <field-name> : create or view character's value for "
			+ "<field-name>",
		"<char-name> <field-name> set <number> : change character's value for "
			+ "<field-name> to <number>",
		"<char-name> <field-name> add [<number>] : add <number> to character's "
			+ "value for <field-name> or add 1 if <number> omitted>",
		"<char-name> <field-name> subtract [<number>] : subtract <number> from "
			+ "character's value for <field-name> or subtract 1 if <number> "
			+ " omitted",
		"substitutions: add|inc|increment|plus|+, subtract|dec|decrement|minus|"
			+ "-, set|:|=, create|new|make, delete|destroy|~" 
	],
	'name' : [
		"coming soon"
	]
}

def parse(msg):
	if "!help" not in msg or "!help <" in msg:
		return []
	tokens = [token.strip() for token in msg.casefold().split("!help")]
	try:
		keyword = tokens[1]
	except IndexError as e:
		keyword = ''
	else:
		keyword = keyword.lstrip("!")
	
	try:
		out = helptext[keyword]
	except KeyError as e:
		out = helptext['']
	return out

def message(lines):
	return '\n\t'.join(lines)


	
