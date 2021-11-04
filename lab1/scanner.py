import ply.lex as lex

matrix_binary = ['PLUS_MATRIX', 'MINUS_MATRIX', 'MULTIPLY_MATRIX', 'DIVIDE_MATRIX']
assignment_operators = ["ADDITION_ASSIGN", "SUBTRACTION_ASSIGN",
                        "MULTIPLICATION_ASSIGN", "DIVISION_ASSIGN"]
comparison_operators = ["LESS_OR_EQUAL", "GREATER_OR_EQUAL", "NOT_EQUAL", "EQUAL"]
numbers = ["INT", "FLOAT"]
strings = ["STRING", "ID", "COMMENT"]

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
 }

tokens = matrix_binary + assignment_operators + comparison_operators + \
         numbers + strings + list(reserved.values())

literals = "+-*/()[]{}<>:,;='"


def t_PLUS_MATRIX(t):
    r'\.\+'
    return t


def t_MINUS_MATRIX(t):
    r'\.-'
    return t


def t_MULTIPLY_MATRIX(t):
    r'\.\*'
    return t


def t_DIVIDE_MATRIX(t):
    r'\./'
    return t


def t_ADDITION_ASSIGN(t):
    r'\+='
    return t


def t_SUBTRACTION_ASSIGN(t):
    r'-='
    return t


def t_MULTIPLICATION_ASSIGN(t):
    r'\*='
    return t


def t_DIVISION_ASSIGN(t):
    r'/='
    return t


def t_LESS_OR_EQUAL(t):
    r'>='
    return t


def t_GREATER_OR_EQUAL(t):
    r'<\='
    return t


def t_NOT_EQUAL(t):
    r'!='
    return t


def t_EQUAL(t):
    r'=='
    return t


def t_FLOAT(t):
    r'((\d*\.\d+)|(\d+\.\d*))([Ee][-+]?\d+)?'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'(\'.*\') | (\".*\")'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMMENT(t):
    r'\#.*'
    pass


t_ignore = ' \t'


def t_newline(t):
    r'\n+?' # non-greedy
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s' at line %d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)


lexer = lex.lex()
