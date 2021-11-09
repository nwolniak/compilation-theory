# Lab1 Teoria Kompilacji
# Norbert Wolniak, Maciej Skoczeń
# Gr. Wtorek 14.20 A


import scanner
import ply.yacc as yacc

tokens = scanner.tokens
tokens.remove("COMMENT") # Nie obsługujemy komentarzy, bo ich nie ma

precedence = (
    ("right", '=', "ADDITION_ASSIGN", "SUBTRACTION_ASSIGN", "MULTIPLICATION_ASSIGN", "DIVISION_ASSIGN"),
    ("nonassoc", "NOT_EQUAL", "EQUAL"),
    ("nonassoc", "LESS_OR_EQUAL", "GREATER_OR_EQUAL", '>', '<'),
    ("left", '+', '-', 'PLUS_MATRIX', 'MINUS_MATRIX'),
    ("left", '*', '/', 'MULTIPLY_MATRIX', 'DIVIDE_MATRIX'),
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('right', 'UMINUS'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions"""

# Instrukcje w programie
def p_instructions(p):
    """instructions : instructions instruction
                    | """

# Pojedyncza instrukcja
def p_instruction(p):
    """instruction : assignment ';'
                   | instruction_if
                   | instruction_loop
                   | instruction_print ';'
                   | RETURN operations ';'
                   | RETURN ';'
                   | BREAK ';'
                   | CONTINUE ';'
                   | ';'
                   | '{' instructions '}' """

# Instrukcja warunkowa
def p_instruction_if(p):
    """instruction_if : IF '(' condition ')' instruction %prec IFX
                      | IF '(' condition ')' instruction ELSE instruction """

# Instrukcje pętli
def p_instruction_loop(p):
    """instruction_loop : FOR ID '=' operations ':' operations instruction
                        | WHILE '(' condition ')' instruction """

# Instrukcja printa
def p_instruction_print(p):
    """instruction_print : PRINT print_values
       print_values : print_values ',' print_value
                    | print_value
       print_value : operations
                   | STRING """

# Operacje przypisania
def p_assignments(p):
    """assignment : ID '[' operations_list ']' '=' operations
                  | identifier ADDITION_ASSIGN operations
                  | identifier MULTIPLICATION_ASSIGN operations
                  | identifier SUBTRACTION_ASSIGN operations
                  | identifier DIVISION_ASSIGN operations
                  | ID '=' assignment_value
       assignment_value : STRING
                        | array
                        | operations """

# Instrukcje warunkowe
def p_condition(p):
    """condition : operations '>' operations
                 | operations '<' operations
                 | operations LESS_OR_EQUAL operations
                 | operations GREATER_OR_EQUAL operations
                 | operations NOT_EQUAL operations
                 | operations EQUAL operations
                 | '(' condition ')' """

# Listowanie operacji binarnych
def p_operations_list(p):
    """operations_list : operations_list ',' operations
                       | operations """

# Operacje binarne
def p_operations_binary(p):
    """operations : operations '+' operations
                  | operations '-' operations
                  | operations '*' operations
                  | operations '/' operations
                  | operations PLUS_MATRIX operations
                  | operations MINUS_MATRIX operations
                  | operations MULTIPLY_MATRIX operations
                  | operations DIVIDE_MATRIX operations
                  | value
                  | '(' operations ')'
                  | '(' operations ')' "'" """

# Uwzględnienie unarnego minusa
def p_operation_uminus(p):
    """operations : '-' operations %prec UMINUS"""

# Wartość
def p_value(p):
    """value : identifier
             | FLOAT
             | INT
             | ZEROS '(' INT ')'
             | ONES '(' INT ')'
             | EYE '(' INT ')' """

# Identyfikatory
def p_identifier(p):
    """identifier : ID
                  | ID '[' operations_list ']'
                  | ID "'" """

# Tablica
def p_array(p):
    """array : '[' operations_list ']'
             | '[' arrays ']'
       arrays : arrays ',' array
              | array """


parser = yacc.yacc()
