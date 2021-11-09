# Lab1 Teoria Kompilacji
# Norbert Wolniak, Maciej Skoczeń
# Gr. Wtorek 14.20 A


import scanner
import ply.yacc as yacc

tokens = scanner.tokens
tokens.remove("COMMENT") # Nie obsługujemy komentarzy, bo ich nie ma

precedence = (
    ("right", '=', "ADDITION_ASSIGN", "SUBTRACTION_ASSIGN", "MULTIPLICATION_ASSIGN", "DIVISION_ASSIGN"),
    ("left", "NOT_EQUAL", "EQUAL"),
    ("left", "LESS_OR_EQUAL", "GREATER_OR_EQUAL", '>', '<'),
    ("left", '+', '-', 'PLUS_MATRIX', 'MINUS_MATRIX'),
    ("left", '*', '/', 'MULTIPLY_MATRIX', 'DIVIDE_MATRIX'),
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
                    | instructions '{' instructions '}'
                    | """

# Pojedyncza instrukcja
def p_instruction(p):
    """instruction : assignment ';'
                   | instruction_if
                   | instruction_loop
                   | instruction_print ';'
                   | RETURN operations ';'
                   | RETURN ';'
                   | ';' """

# Instrukcje będące w bloku pętli.
def p_instructions_in_loop(p):
    """instructions_in_loop : instructions_in_loop instruction_in_loop
                            | instructions_in_loop '{' instructions_in_loop '}'
                            |  """

# Instrukcja będąca w bloku pętli. Można wtedy używać break oraz continue
def p_instruction_in_loop(p):
    """instruction_in_loop : assignment ';'
                   | instruction_if_in_loop
                   | instruction_loop
                   | instruction_print ';'
                   | RETURN operations ';'
                   | RETURN ';'
                   | BREAK ';'
                   | CONTINUE ';'
                   | ';' """

# Możliwość pominięcia klamer przy jednolinijkowej instrukcji
def p_instructions_block(p):
    """instructions_block : '{' instructions '}'
                          | instruction
       instructions_block_in_loop : '{' instructions_in_loop '}'
                                  | instruction_in_loop """

# Instrukcja warunkowa
def p_instruction_if(p):
    """instruction_if : IF '(' condition ')' instructions_block ELSE instructions_block
                      | IF '(' condition ')' instructions_block
       instruction_if_in_loop : IF '(' condition ')' instructions_block_in_loop ELSE instructions_block_in_loop
                              | IF '(' condition ')' instructions_block_in_loop """

# Instrukcje pętli
def p_instruction_loop(p):
    """instruction_loop : FOR ID '=' operations ':' operations instructions_block_in_loop
                        | WHILE '(' condition ')' instructions_block_in_loop """

# Instrukcja printa
def p_instruction_print(p):
    """instruction_print : PRINT print_values
       print_values : print_values ',' operations
                    | print_values ',' STRING
                    | operations
                    | STRING """

# Operacje przypisania
def p_assignments(p):
    """assignment : ID '[' operations_list ']' '=' assignment_operations
                  | ID '=' assignment_operations
                  | identifier_value ADDITION_ASSIGN assignment_operations
                  | identifier_value MULTIPLICATION_ASSIGN assignment_operations
                  | identifier_value SUBTRACTION_ASSIGN assignment_operations
                  | identifier_value DIVISION_ASSIGN assignment_operations
                  | ID '=' STRING
                  | ID '=' array
                  | ID '=' ZEROS '(' INT ')'
                  | ID '=' ONES '(' INT ')'
                  | ID '=' EYE '(' INT ')' """

# Instrukcje warunkowe
def p_condition(p):
    """condition : operations '>' operations
                 | operations '<' operations
                 | operations LESS_OR_EQUAL operations
                 | operations GREATER_OR_EQUAL operations
                 | operations NOT_EQUAL operations
                 | operations EQUAL operations
                 | operations
                 | '(' condition ')' """

# Operacje binarne albo macierzowe, które mogą wystąpić po prawej stronie przypisania
def p_assignment_operations(p):
    """assignment_operations : operations
                             | operations_matrix """

# Listowanie operatorów binarnych
def p_operations_list(p):
    """operations_list : operations_list ',' operations
                       | operations """

# Operacje binarne
def p_operations_binary(p):
    """operations : operations '+' operations_right
                  | operations '-' operations_right
                  | operations '*' operations_right
                  | operations '/' operations_right
                  | value_first
                  | '(' operations ')'
                  | '-' '(' operations ')'
       operations_right : value
                        | '(' operations ')' """

# Operacje macierzowe
def p_operations_matrix(p):
    """operations_matrix : operations_matrix PLUS_MATRIX operations_matrix_right
                         | operations_matrix MINUS_MATRIX operations_matrix_right
                         | operations_matrix MULTIPLY_MATRIX operations_matrix_right
                         | operations_matrix DIVIDE_MATRIX operations_matrix_right
                         | identifier_matrix
                         | '(' operations_matrix ')'
       operations_matrix_right : identifier_matrix
                               | '(' operations_matrix ')' """

# Wartość, która może mieć unarną negację
def p_value_first(p):
    """value_first : identifier_value
                   | '-' identifier_value
                   | FLOAT
                   | '-' FLOAT
                   | INT
                   | '-' INT """

# Wartość, która jest bezpośrednio po jakimś operatorze i nie może mieć unarnej negacji
def p_value(p):
    """value : identifier_value
             | FLOAT
             | INT """

# Identyfikatory binarne oraz macierzowe
def p_identifier(p):
    """identifier_value : ID
                        | ID '[' operations_list ']'
       identifier_matrix : ID
                         | ID "'" """

# Tablica
def p_array(p):
    """array : '[' operations_list ']'
             | '[' arrays ']'
       arrays : arrays ',' array
              | array """


parser = yacc.yacc()
