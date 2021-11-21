# Lab2 Teoria Kompilacji
# Norbert Wolniak, Maciej Skoczeń
# Gr. Wtorek 14.20 A


import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens
tokens.remove("COMMENT")  # Nie obsługujemy komentarzy, bo ich nie ma

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
    p[0] = AST.Program(p[1])
    p[0].printTree(0)
    # done


# Instrukcje w programie
def p_instructions(p):
    """instructions : instructions instruction
                    | """
    if len(p) == 3:
        p[0] = AST.Instructions(p[1], p[2])
    else:
        p[0] = AST.Instructions(None, None)

    # done


# Pojedyncza instrukcja
def p_instruction(p):
    """instruction : assignment ';'
                           | instruction_if
                           | instruction_loop
                           | instruction_print ';'
                           | instruction_return ';'
                           | BREAK ';'
                           | CONTINUE ';'
                           | '{' instructions '}' """
    if p[1] == "{":
        p[0] = p[2]
    elif p[1] == "break":
        p[0] = AST.Break()
    elif p[1] == "continue":
        p[0] = AST.Continue()
    else:
        p[0] = p[1]

    # done


# Operacje przypisania
def p_assignments(p):
    """assignment : identifier '=' operations
                    | identifier ADDITION_ASSIGN operations
                    | identifier MULTIPLICATION_ASSIGN operations
                    | identifier SUBTRACTION_ASSIGN operations
                    | identifier DIVISION_ASSIGN operations"""
    p[0] = AST.Assignment(p[2], p[1], p[3])

    # done


# Instrukcja warunkowa
def p_instruction_if(p):
    """instruction_if : IF '(' condition ')' instruction %prec IFX
                      | IF '(' condition ')' instruction ELSE instruction """
    if len(p) == 8:
        p[0] = AST.IfInstruction(p[3], p[5], p[7])
    else:
        p[0] = AST.IfInstruction(p[3], p[5], None)

    # done


# Instrukcje pętli
def p_instruction_loop(p):
    """instruction_loop : FOR ID '=' operations ':' operations instruction
                        | WHILE '(' condition ')' instruction """

    if p[1] == "for":
        p[0] = AST.ForLoop(p[2], p[4], p[6], p[7])
    else:
        p[0] = AST.WhileLoop(p[3], p[5])

    # done


# Instrukcja printa
def p_instruction_print(p):
    """instruction_print : PRINT operations_list """
    p[0] = AST.PrintInstruction(p[2])

    # done


# Instrukcja return
def p_instruction_return(p):
    """instruction_return : RETURN operations
                            | RETURN """
    if len(p) == 3:
        p[0] = AST.ReturnInstruction(p[2])
    else:
        p[0] = AST.ReturnInstruction(None)

    # done


# Instrukcje warunkowe
def p_condition(p):
    """condition : operations"""
    p[0] = p[1]

    # done


# Operacje binarne
def p_operations_binary(p):
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
                      | operations DIVIDE_MATRIX operations
                      | '(' operations ')'
                      | '(' operations ')' "'"
                      | array
                      | value"""

    if p[1] == "(":
        p[0] = AST.OperationsParentheses(p[2])
    elif len(p) == 4:
        p[0] = AST.BinExpr(p[2], p[1], p[3])
    elif len(p) == 5:
        p[0] = AST.Transposition(p[2])
    else:
        p[0] = p[1]


# Uwzględnienie unarnego minusa
def p_operation_uminus(p):
    """operations : '-' operations %prec UMINUS"""
    p[0] = AST.BinExpr(p[1], None, p[3])


# Wartość
def p_value(p):
    """value : identifier
             | FLOAT
             | INT
             | ZEROS '(' INT ')'
             | ONES '(' INT ')'
             | EYE '(' INT ')' """
    if isinstance(p[1], int):
        p[0] = AST.IntNum(p[1])
    elif isinstance(p[1], float):
        p[0] = AST.FloatNum(p[1])
    elif p[1] == "zeros":
        p[0] = AST.Zeros(p[3])
    elif p[1] == "ones":
        p[0] = AST.Ones(p[3])
    elif p[1] == "eye":
        p[0] = AST.Eye(p[3])
    else:
        p[0] = p[1]  # identifier


# Identyfikatory
def p_identifier(p):
    """identifier : ID
                | identifier array
                | identifier "'" """
    if len(p) == 2:
        p[0] = AST.ID(p[1])
    elif len(p) == 3 and p[2] == "'":
        p[0] = AST.Transposition(p[1])
    else:
        p[0] = AST.Reference(p[1], p[2])


# Tablica
def p_array(p):
    """array : '[' array_list ']'
            | '[' operations_list ']' """
    p[0] = AST.Array(p[2])


def p_array_list(p):
    """array_list : array_list ',' array
                    | array """
    if len(p) == 4:
        p[0] = AST.ArrayList(p[1], p[3])
    else:
        p[0] = p[1]


def p_operations_list(p):
    """operations_list : operations_list ',' operations
                        | operations"""
    if len(p) == 4:
        p[0] = AST.OperationsList(p[1], p[3])
    else:
        p[0] = AST.OperationsList(None, p[1])


parser = yacc.yacc()
