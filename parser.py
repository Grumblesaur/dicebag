import ply.yacc as yacc
from dice_error import DiceParserException
from lexer import tokens
from random import randrange

def p_expression_add(p):
	'expression : expression ADD term'
	p[0] = p[1] + p[3]

def p_expression_subtract(p):
	'expression : expression SUBTRACT term'
	p[0] = p[1] - p[3]

def p_expression_term(p):
	'expression : term'
	p[0] = p[1]

def p_term_multiply(p):
	'term : term MULTIPLY factor'
	p[0] = p[1] * p[3]

def p_term_divide(p):
	'term : term DIVIDE factor'
	p[0] = p[1] // p[3]

def p_factor_die(p):
	'factor : factor DIE factor'
	p[0] = sum([randrange(p[3]) + 1 for x in range(p[1])])

def p_factor_die_drop_high(p):
	'factor : factor DIE factor HIGH NUMBER'
	p[0] = sum(
		sorted([randrange(p[3]) + 1 for x in range(p[1])])[:p[5]]
	)

def p_factor_die_drop_low(p):
	'factor : factor DIE factor LOW NUMBER'
	p[0] = sum(
		sorted([randrange(p[3]) + 1 for x in range(p[1])])[p[5]:]
	)

def p_term_factor(p):
	'term : factor'
	p[0] = p[1]
	
def p_factor_number(p):
	'factor : NUMBER'
	p[0] = p[1]

def p_factor_expression(p):
	'factor : OPEN expression CLOSE'
	p[0] = p[2]

parser = yacc.yacc(optimize=1)

def roll(expr):
	try:
		return parser.parse(expr)
	except Exception as e:
		raise DiceParserException(e)

