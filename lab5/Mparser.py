# Lab2 Teoria Kompilacji
# Norbert Wolniak, Maciej Skoczeń
# Gr. Wtorek 14.20 A
import string

import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens
tokens.remove("COMMENT")  # Nie obsługujemy komentarzy, bo ich nie ma

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ("right", '=', "ADDITION_ASSIGN", "SUBTRACTION_ASSIGN", "MULTIPLICATION_ASSIGN", "DIVISION_ASSIGN"),
    ("nonassoc", "NOT_EQUAL", "EQUAL"),
    ("nonassoc", "LESS_OR_EQUAL", "GREATER_OR_EQUAL", '>', '<'),
    ("left", '+', '-', 'PLUS_MATRIX', 'MINUS_MATRIX'),
    ("left", '*', '/', 'MULTIPLY_MATRIX', 'DIVIDE_MATRIX'),
    ('right', 'UMINUS'),
)

error_occurred = False

def p_error(p):
    global error_occurred
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")
    error_occurred = True


def p_program(p):
    """program : instructions"""
    p[0] = AST.Program(p[1])
    p[0].lineno = p.lexer.lineno
    # if not error_occurred:
    #     p[0].printTree(0)


# Instrukcje w programie
def p_instructions(p):
    """instructions : instructions instruction
                    | """
    if len(p) == 3:
        p[0] = AST.Instructions(p[1], p[2])
    else:
        p[0] = AST.Instructions(None, None)
    p[0].lineno = p.lexer.lineno


# Pojedyncza instrukcja
def p_instruction(p): # mozna rozdzielic funkcje
    """instruction : '{' instructions '}' """
    p[0] = p[2]
    p[0].lineno = p.lexer.lineno


def p_instruction_2(p):
    """instruction : BREAK ';'
                   | CONTINUE ';' """
    if p[1] == "break":
        p[0] = AST.Break()
    else:
        p[0] = AST.Continue()
    p[0].lineno = p.lexer.lineno


def p_instruction_3(p):
    """instruction : assignment ';'
                   | instruction_if
                   | instruction_loop
                   | instruction_print ';'
                   | instruction_return ';' """
    p[0] = p[1]
    p[0].lineno = p.lexer.lineno


# Operacje przypisania
def p_assignments(p):
    """assignment : identifier '=' operations
                    | identifier ADDITION_ASSIGN operations
                    | identifier MULTIPLICATION_ASSIGN operations
                    | identifier SUBTRACTION_ASSIGN operations
                    | identifier DIVISION_ASSIGN operations"""
    p[0] = AST.Assignment(p[2], p[1], p[3])
    p[0].lineno = p.lexer.lineno


# Instrukcja warunkowa
def p_instruction_if(p):
    """instruction_if : IF '(' condition ')' instruction %prec IFX
                      | IF '(' condition ')' instruction ELSE instruction """
    if len(p) == 8:
        p[0] = AST.IfInstruction(p[3], p[5], p[7])
    else:
        p[0] = AST.IfInstruction(p[3], p[5], None)
    p[0].lineno = p.lexer.lineno


# Instrukcje pętli
def p_instruction_loop(p):
    """instruction_loop : FOR ID '=' operations ':' operations instruction
                        | WHILE '(' condition ')' instruction """

    if p[1] == "for":
        p[0] = AST.ForLoop(AST.ID(p[2]), p[4], p[6], p[7])
    else:
        p[0] = AST.WhileLoop(p[3], p[5])
    p[0].lineno = p.lexer.lineno


# Instrukcja printa
def p_instruction_print(p):
    """instruction_print : PRINT operations_list """
    p[0] = AST.PrintInstruction(p[2])
    p[0].lineno = p.lexer.lineno


# Instrukcja return
def p_instruction_return(p):
    """instruction_return : RETURN operations
                            | RETURN """
    if len(p) == 3:
        p[0] = AST.ReturnInstruction(p[2])
    else:
        p[0] = AST.ReturnInstruction(None)
    p[0].lineno = p.lexer.lineno


# Instrukcje warunkowe
def p_condition(p):
    """condition : operations"""
    p[0] = p[1]


# Operacje
def p_operations(p):
    """operations : '(' operations ')' """
    p[0] = p[2]
    p[0].lineno = p.lexer.lineno


def p_operations_2(p):
    """operations : operations '+' operations
                  | operations '-' operations
                  | operations '*' operations
                  | operations '/' operations
                  | operations '>' operations
                  | operations '<' operations
                  | operations GREATER_OR_EQUAL operations
                  | operations LESS_OR_EQUAL operations
                  | operations NOT_EQUAL operations
                  | operations EQUAL operations
                  | operations PLUS_MATRIX operations
                  | operations MINUS_MATRIX operations
                  | operations MULTIPLY_MATRIX operations
                  | operations DIVIDE_MATRIX operations"""
    p[0] = AST.BinExpr(p[2], p[1], p[3])
    p[0].lineno = p.lexer.lineno


def p_operations_3(p):
    """operations : operations "'" """
    p[0] = AST.Transposition(p[1])
    p[0].lineno = p.lexer.lineno


def p_operations_4(p):
    """operations : array
                  | value"""
    p[0] = p[1]
    p[0].lineno = p.lexer.lineno


# Uwzględnienie unarnego minusa
def p_operation_uminus(p):
    """operations : '-' operations %prec UMINUS"""
    p[0] = AST.UMinus(p[2])
    p[0].lineno = p.lexer.lineno


# Wartość
def p_value(p):
    """value : FLOAT
             | INT
             | STRING """
    if p.slice[1].type == "INT":
        p[0] = AST.IntNum(p[1])
    elif p.slice[1].type == "FLOAT":
        p[0] = AST.FloatNum(p[1])
    else:
        p[0] = AST.String(p[1][1:-1])
    p[0].lineno = p.lexer.lineno


def p_value_2(p):
    """value : ZEROS '(' operations_list ')'
             | ONES '(' operations_list ')'
             | EYE '(' operations_list ')' """
    if p[1] == "zeros":
        p[0] = AST.Zeros(p[3])
    elif p[1] == "ones":
        p[0] = AST.Ones(p[3])
    else:
        p[0] = AST.Eye(p[3])
    p[0].lineno = p.lexer.lineno


def p_value_3(p):
    """value : identifier """
    p[0] = p[1]  # identifier
    p[0].lineno = p.lexer.lineno

# Identyfikatory
def p_identifier(p):
    """identifier : ID
                  | ID '[' operations_list ']' """
    if len(p) == 2:
        p[0] = AST.ID(p[1])
    else:
        p[0] = AST.Reference(p[1], p[3])
    p[0].lineno = p.lexer.lineno


# Tablica
def p_array(p):
    """array : '[' operations_list ']' """
    p[0] = AST.Array(p[2])
    p[0].lineno = p.lexer.lineno


# Listowanie operacji
def p_operations_list(p):
    """operations_list : operations_list ',' operations
                        | operations"""
    if len(p) == 4:
        p[0] = AST.OperationsList(p[1], p[3])
    else:
        p[0] = AST.OperationsList(None, p[1])
    p[0].lineno = p.lexer.lineno


parser = yacc.yacc()