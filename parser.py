import ply.yacc as yacc
from DiceValue import DiceValue
from dice_error import DiceParserException

literals = [
	'+', '-', '(', ')',
	'*', '/', '%', '@',
	'$', 'd', 'l', 'h',
	'#', '_', '~', '=',
	'!'
]

tokens = ('NUMBER',)

def t_NUMBER(t):
	r'\d+'
	t.value = DiceValue(int(t.value))
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count('\n')

def t_whitespace(t):
	r'[ \t]+'
	pass

def t_error(t):
	raise DiceParserException("Illegal character `%s'" % t.value[0])

precedence = (
	('left', '='),
	('left', '#', '_'),
	('left', '$'),
	('left', '+', '-'),
	('left', '*', '/', '%'),
	('right', '@', '~'),
	('right', '!'),
	('nonassoc', 'h', 'l'),
	('left', 'd'),
)

import ply.lex as lex
lex.lex()

def p_expr_un(p):
	''' expr : expr ! '''
	p[0] = p[1].factorial()

def p_expr_bin(p):
	''' expr : expr '=' expr
             | expr '#' expr
             | expr '_' expr
             | expr '$' expr
             | expr '+' expr
             | expr '-' expr
             | expr '*' expr
             | expr '/' expr
             | expr '%' expr
             | expr '~' expr
             | expr '@' expr
             | expr 'd' expr
    '''
	if p[2] == '=':
		p[0] = p[1] == p[3]
	elif p[2] == '#':
		p[0] = p[1].maximum(p[3])
	elif p[2] == '_':
		p[0] = p[1].minimum(p[3])
	elif p[2] == '$':
		p[0] = p[1].concatenate(p[3])
	elif p[2] == '+':
		p[0] = p[1] + p[3]
	elif p[2] == '-':
		p[0] = p[1] - p[3]
	elif p[2] == '*':
		p[0] = p[1] * p[3]
	elif p[2] == '/':
		p[0] = p[1] // p[3]
	elif p[2] == '%':
		p[0] = p[1] % p[3]
	elif p[2] == '~':
		p[0] = p[1].logarithm(p[3])
	elif p[2] == '@':
		p[0] = p[1] ** p[3]
	elif p[2] == 'd':
		p[0] = p[1].die(p[3])

def p_expr_tern(p):
	''' expr : expr 'd' term 'h' term
             | expr 'd' term 'l' term
    '''
	p[0] = p[1].die(*tuple(p[3:]))

def p_error(p):
	print("syntax error: ", p)

def p_term(p):
	''' term : '(' expr ')'
             | NUMBER
    '''
	p[0] = p[1] if len(p) == 2 else p[2]

def p_expr(p):
	''' expr : term '''
	p[0] = p[1]

parser = yacc.yacc(optimize=1)

def roll(expr):
	try:
		return parser.parse(expr).value
	except Exception as e:
		raise DiceParserException(e)

