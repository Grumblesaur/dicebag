from dice_error import DiceParserException

tokens = (
	'NUMBER',   'DIE',
	'OPEN',     'CLOSE',
	'HIGH',     'LOW',
	'ADD',      'SUBTRACT',
	'MULTIPLY', 'DIVIDE'
)

t_ADD      = r'\+'
t_SUBTRACT = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE   = r'/'
t_DIE      = r'd'
t_HIGH     = r'h'
t_LOW      = r'l'
t_OPEN     = r'\('
t_CLOSE    = r'\)'


def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

t_ignore = " \t\n\r"

def t_error(t):
	raise DiceParserException("Illegal character '%s'" % t.value[0])

	# t.lexer.skip(1)

import ply.lex as lex

lex.lex(optimize=1)

precedence = (
	('left', 'ADD', 'SUBTRACT'),
	('left', 'MULTIPLY', 'DIVIDE'),
	('left', 'DIE')
)





