import sys
from collections import defaultdict
import ply.yacc as yacc
import Mparser
import scanner
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from Interpreter import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "text.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    lexer = scanner.lexer
    text = file.read()
    ast = parser.parse(text, lexer=lexer)

    if not Mparser.error_occurred:
        # Below code shows how to use visitor
        typeChecker = TypeChecker()
        typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)

        interpreter = Interpreter()
        res = interpreter.visit(ast)
        print("Res : ", res)
