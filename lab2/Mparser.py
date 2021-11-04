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


def p_instructions(p):
    """instructions : instructions instruction
                    | instructions '{' instructions '}'
                    | """

# Instrukcja, czyli linijka w programie
def p_instruction(p):
    """instruction : assignment ';'
                   | instruction_if
                   | instruction_loop
                   | instruction_print ';'
                   | RETURN operations ';'
                   | RETURN ';'
                   | BREAK ';'
                   | CONTINUE ';'
                   | ';' """
    # break i continue powinny być tylko dostępne w boku pętel, ale trzeba by zrobić sporo dodatkowych elementów

# Operacje przypisania
def p_assignments(p):
    """assignment : ID '[' operations_list ']' '=' operations
                   | ID '=' operations
                   | ID '=' operations_matrix
                   | ID '[' operations_list ']' ADDITION_ASSIGN operations
                   | ID ADDITION_ASSIGN operations
                   | ID '[' operations_list ']' MULTIPLICATION_ASSIGN operations
                   | ID MULTIPLICATION_ASSIGN operations
                   | ID '[' operations_list ']' SUBTRACTION_ASSIGN operations
                   | ID SUBTRACTION_ASSIGN operations
                   | ID '[' operations_list ']' DIVISION_ASSIGN operations
                   | ID DIVISION_ASSIGN operations
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
       operations_right : value_no_brackets
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

# Możliwość pominięcia klamer przy jednolinijkowej instrukcji
def p_instructions_block(p):
    """instructions_block : '{' instructions '}'
                          | instruction """

# Instrukcja warunkowa
def p_instruction_if(p):
    """instruction_if : IF '(' condition ')' instructions_block ELSE instructions_block
                      | IF '(' condition ')' instructions_block """

# Instrukcje pętli
def p_instruction_loop(p):
    """instruction_loop : FOR ID '=' operations ':' operations instructions_block
                        | WHILE '(' condition ')' instructions_block """

# Printowalne wartości oddzielone przecinkami (do printa)
def p_print_values(p):
    """print_values : print_values ',' operations
                    | print_values ',' STRING
                    | operations
                    | STRING """

# Instrukcja printa
def p_instruction_print(p):
    """instruction_print : PRINT print_values """

# Wartość, która może mieć unarną negację
def p_value_first(p):
    """value_first : identifier_binary
                  | '-' identifier_binary
                  | FLOAT
                  | INT
                  | '-' FLOAT
                  | '-' INT """

# Wartość, która nie generuje dodatkowych nawiasów
def p_value_no_brackets(p):
    """value_no_brackets : identifier_binary
                  | FLOAT
                  | INT """

# Identyfikatory binarne oraz macierzowe
def p_identifier_binary(p):
    """identifier_binary : ID
                         | ID '[' operations_list ']'
       identifier_matrix : ID
                         | ID "'" """
    # Zezwala na indeksowanie floatem, trudne do naprawy

# Tablica
def p_array(p):
    """array : '[' operations_list ']'
             | '[' arrays ']'
       arrays : arrays ',' array
              | array """


parser = yacc.yacc()
