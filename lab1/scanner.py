import ply.lex as lex
import sys

binary = ['PLUS_BINARY', 'MINUS_BINARY', 'TIMES_BINARY', 'DIVIDE_BINARY']
matrix_binary = ['PLUS_MATRIX', 'MINUS_MATRIX', 'TIMES_MATRIX', 'DIVIDE_MATRIX']
assignment_operators = ["DIRECT_ASSIGNMENT", "ADDITION_ASSIGNMENT", "SUBSTRACTION_ASSIGNMENT",
                        "MULTIPLICATION_ASSIGNMENT", "DIVISION_ASSIGNMENT"]
comparison_operators = ["LESS_THAN", "GREATER_THAN", "LESS_THAN_OR_EQUAL_TO",
                        "GREATER_THAN_OR_EQUAL_TO", "NOT_EQUAL_TO", "EQUAL_TO"]
paren = ["LPAREN", "RPAREN", "LSPAREN", "RSPAREN", "LFPAREN", "RFPAREN"]
operators = ["RANGE_OPERATOR", "MATRIX_TRANSPOSITION", "COMMA", "SEMI_COLON"]
identificators = ["IDENTIFICATOR"]
numbers = ["INT", "FLOAT"]
strings = ["STRING", "ID", "COMMENT"]

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'return' : 'RETURN',
    'eye' : 'EYE',
    'zeros' : 'ZEROS',
    'ones' : 'ONES',
    'print' : 'PRINT'
 }

tokens = binary + matrix_binary + assignment_operators + comparison_operators + \
         paren + operators + identificators + numbers + strings + list(reserved.values())

literals = "+-*/()[]{}<>:,;='"

# t_PLUS_BINARY = r'\+'
# t_MINUS_BINARY = r'-'
# t_TIMES_BINARY = r'\*'
# t_DIVIDE_BINARY = r'/'
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
# t_LSPAREN = r'\['
# t_RSPAREN = r'\]'
# t_LFPAREN = r'\{'
# t_RFPAREN = r'\}'
# t_LESS_THAN = r'>'
# t_GREATER_THAN = r'<'
# t_RANGE_OPERATOR = r':'
# t_COMMA = r','
# t_SEMI_COLON = r';'
# t_DIRECT_ASSIGNMENT = r'\='
# t_MATRIX_TRANSPOSITION = r'\''


def t_PLUS_MATRIX(t):
    r'\.\+'
    return t


def t_MINUS_MATRIX(t):
    r'\.\-'
    return t


def t_TIMES_MATRIX(t):
    r'\.\*'
    return t


def t_DIVIDE_MATRIX(t):
    r'\./'
    return t


def t_ADDITION_ASSIGNMENT(t):
    r'\+\='
    return t


def t_SUBSTRACTION_ASSIGNMENT(t):
    r'-\='
    return t


def t_MULTIPLICATION_ASSIGNMENT(t):
    r'\*\='
    return t


def t_DIVISION_ASSIGNMENT(t):
    r'/\='
    return t


def t_LESS_THAN_OR_EQUAL_TO(t):
    r'>\='
    return t


def t_GREATER_THAN_OR_EQUAL_TO(t):
    r'<\='
    return t


def t_NOT_EQUAL_TO(t):
    r'\!\='
    return t


def t_EQUAL_TO(t):
    r'\=\='
    return t


def t_FLOAT(t):
    r'[-+]? (((\d*\.\d+) | (\d+\.)) ([eE][+-]?\d+)? | (\d+[eE][+-]?\d+))'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'(\'.*\') | (\".*\")'
    t.value = str(t.value)
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
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



lexer = lex.lex()

