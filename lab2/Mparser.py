import scanner
import ply.yacc as yacc

tokens = scanner.tokens
tokens.remove("COMMENT") # Nie obsługujemy komentarzy, bo ich nie ma

precedence = (
    # ("nonassoc", 'IF'),
    # ("nonassoc", 'ELSE'),
    ("left", '+', '-'),
    ("left", '*', '/'),
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

# Instrukcje będąca w bloku pętli.
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
    """assignment : ID '[' operations_list ']' '=' operations
                  | ID '=' operations
                  | ID '=' operations_matrix
                  | identifier_value ADDITION_ASSIGN operations
                  | identifier_value MULTIPLICATION_ASSIGN operations
                  | identifier_value SUBTRACTION_ASSIGN operations
                  | identifier_value DIVISION_ASSIGN operations
                  | ID '=' STRING
                  | ID '=' array
                  | ID '=' ZEROS '(' INT ')'
                  | ID '=' ONES '(' INT ')'
                  | ID '=' EYE '(' INT ')' """

# Instrukcje warunkowe
def p_condition(p):
    """condition : condition '>' operations
                 | condition '<' operations
                 | condition LESS_OR_EQUAL operations
                 | condition GREATER_OR_EQUAL operations
                 | condition NOT_EQUAL operations
                 | condition EQUAL operations
                 | operations
                 | '(' condition ')' """

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
