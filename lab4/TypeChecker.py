import sys
from collections import defaultdict

import AST


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


def multi_dict(K):
    if K == 1:
        return defaultdict()
    else:
        return defaultdict(lambda: multi_dict(K - 1))

MatrixType = 'matrix'
VectorType = 'vector'
IntType = 'int'
FloatType = 'float'
StringType = 'string'

# Generowanie tablicy typów i operacji
def generate_ttype():
    ttype = multi_dict(3)
    # Float and int binops
    for op in ['+', '-', '*', '/']:
        for t1 in [FloatType, IntType]:
            for t2 in [FloatType, IntType]:
                ttype[op][t1][t2] = IntType if t1 == t2 == IntType else FloatType

    # Matrix/vector mult/div by int/float
    for t1 in [MatrixType, VectorType]:
        for t2 in [FloatType, IntType]:
            ttype['*'][t1][t2] = t1
            ttype['*'][t2][t1] = t1
            ttype['/'][t1][t2] = t1

    # Matrix by matrix mult
    ttype['*'][MatrixType][MatrixType] = MatrixType
    ttype['*'][MatrixType][VectorType] = VectorType
    ttype['*'][VectorType][MatrixType] = VectorType

    # Matrix and vector elem by elem ops
    for op in ['+', '-', '.+', '.-', '.*', './']:
        for t in [MatrixType, VectorType]:
            ttype[op][t][t] = t

    # Conditions
    for op in ['>', '<', '==', '>=', '<=', '!=']:
        for t1 in [FloatType, IntType]:
            for t2 in [FloatType, IntType]:
                ttype[op][t1][t2] = IntType
                
    # String mul
    ttype['*'][StringType][IntType] = StringType
    return ttype

ttype = generate_ttype()
# Niezdefiniowane bezpośrednio wymiary będą dla ułatwienia maxintem
undefined_size = sys.maxsize
# Czy obecna instrukcja jest w pętli - wtedy można używać break i continue
inside_loop = False
# Słownik zmiennych w programie
symbol_table = dict()

# Klasa typów w języku
class Type:
    def __init__(self, type_in=None, inner_type=None, x=0, y=0):
        self.type = type_in # typ
        if inner_type is None:
            self.inner_type = type_in
        else:
            self.inner_type = inner_type  # typ wewnątrz wektora/macierzy
        self.x = x  # wymiary wektora/macierzy
        self.y = y

    # Zwraca typ na podstawie operacji op na typach self i other
    def get_type(self, op, other):
        if other.type not in ttype[op][self.type]:
            return Type(None)
        result_type = ttype[op][self.type][other.type]
        if result_type == MatrixType:
            if op == '*':
                inner_type = ttype[op][self.inner_type][other.inner_type]
                if self.type != MatrixType:  # skalar * macierz
                    return Type(MatrixType, inner_type, other.x, other.y)
                if other.type == MatrixType:  # macierz * macierz
                    return Type(MatrixType, inner_type, self.x, other.y)
                # macierz * skalar
                return Type(MatrixType, inner_type, self.x, self.y)
            else:
                if op[0] == '.':
                    op = op[1]
                inner_type = ttype[op][self.inner_type][other.inner_type]
                if self.type == MatrixType:
                    return Type(MatrixType, inner_type, self.x, self.y)
                return Type(MatrixType, inner_type, other.x, other.y)
        elif result_type == VectorType:
            if op[0] == '.':
                op = op[1]
            inner_type = ttype[op][self.inner_type][other.inner_type]
            if self.type == VectorType:
                return Type(VectorType, inner_type, self.x)
            return Type(VectorType, inner_type, other.x)
        return Type(result_type)

    # Rozszerza wektor do macierzy, wartość do wektora
    def extend(self, dim):
        if self.type == VectorType:
            return Type(MatrixType, self.inner_type, self.x, dim)
        elif self.type == MatrixType:
            return Type()
        else:
            return Type(VectorType, self.type, dim)

    # Sprawdza zgodność rozmiarów dla operacji
    def check_sizes(self, op, other):
        if undefined_size in [self.x, self.y, other.x, other.y]:
            return True
        if op in ['+', '-', '.+', '.-', '.*', './']:
            return self.x == other.x and self.y == other.y
        elif op == '*':
            if other.type == VectorType:
                return self.x == other.x
            elif other.type == MatrixType:
                return self.y == other.x
            else:
                return True
        else:
            return True

    # Zwraca typ zawarty w danym typie (dla macierzy wektor, dla wektora typ w nim)
    def get_idx(self, idx=None):
        if self.type == VectorType:
            return Type(self.inner_type)
        elif self.type == MatrixType:
            if idx is not None:
                return Type(self.inner_type)
            else:
                return Type(VectorType, self.inner_type, self.x)
        else:
            return Type()

    def __eq__(self, other):
        return self.type == other.type and self.inner_type == other.inner_type \
               and ((self.x == other.x and self.y == other.y) or
                    undefined_size in [self.x, self.y, other.x, other.y])

    def __str__(self):
        if self.type is None:
            return 'none'
        return self.type


def check_valid_reference(node, id_type, types, i):
    if types[i].type != IntType:
        node.error('referenced index is not an int')
        return False
    # Jeżeli indeks jest wpisany bezpośrednio jako liczba, to sprawdzamy czy dobry zakres
    if isinstance(node.reference.children[i], AST.IntNum):
        idx = node.reference.children[i].value
        if idx >= (id_type.x if i == 0 else id_type.y) or idx < 0:
            node.error(id_type.type + ' index out of range')
            return False
    return True

class TypeChecker(NodeVisitor):

    def visit_Program(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Assignment(self, node):
        type2 = self.visit(node.operations)
        op = node.op
        is_reference = isinstance(node.identifier, AST.Reference)
        if op != '=':  # binop + assignment
            type1 = self.visit(node.identifier)
            if type1.type is None or type2.type is None:
                return
            op = op[0]
            result_type = type1.get_type(op, type2)
            if result_type.type is None:
                node.error('invalid operation ' + op + ' between ' + str(type1) + ' and ' + str(type2))
            elif not type1.check_sizes(op, type2):
                node.error('operation ' + op + ' sizes mismatch')
            elif is_reference:
                if type1 != result_type:
                    node.error('invalid types assignment')
            else:
                symbol_table[node.identifier.name] = result_type
        else:  # assignment
            # Jeżeli to identyfikator to bierzemy bezpośrednio typ, by nie wywołać blędu undefined identifier
            if is_reference:
                type1 = self.visit(node.identifier)
                if type1.type is not None and type2.type is not None:  # poprawna referencja
                    if type1 != type2:
                        node.error('invalid types assignment')
                    # nothing to change
            else:
                if type2.type is not None:
                    symbol_table[node.identifier.name] = type2

    def visit_IfInstruction(self, node):
        self.visit(node.condition)
        self.visit(node.if_instruction)
        if node.else_instruction:
            self.visit(node.else_instruction)

    def visit_ForLoop(self, node):
        global inside_loop
        # Zapisujemy stan jaki był przed wejściem do tej pętli
        pre_loop = inside_loop
        inside_loop = Type()
        type2 = self.visit(node.start)
        type3 = self.visit(node.end)
        if type2.type != IntType or type3.type != IntType:
            node.start.error('for loop range bounds have to be integers')
        old_id_type = symbol_table.get(node.id, None)
        symbol_table[node.id] = Type(IntType)
        self.visit(node.instruction)
        if old_id_type is None:
            del symbol_table[node.id]
        else:
            symbol_table[node.id] = old_id_type
        inside_loop = pre_loop

    def visit_WhileLoop(self, node):
        global inside_loop
        # Zapisujemy stan jaki był przed wejściem do tej pętli
        pre_loop = inside_loop
        inside_loop = True
        self.visit(node.condition)
        self.visit(node.instruction)
        inside_loop = pre_loop

    def visit_PrintInstruction(self, node):
        self.visit(node.children)

    def visit_ReturnInstruction(self, node):
        self.visit(node.child)

    def visit_Break(self, node):
        if not inside_loop:
            node.error('break usage outside a loop')

    def visit_Continue(self, node):
        if not inside_loop:
            node.error('continue usage outside a loop')

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if type1.type is None or type2.type is None:
            return Type()
        result_type = type1.get_type(op, type2)
        if result_type.type is None:
            node.error('invalid operation ' + op + ' between ' + str(type1) + ' and ' + str(type2))
            return Type()
        if type1.check_sizes(op, type2):
            return result_type
        else:
            node.error('operation ' + op + ' sizes mismatch')
            return Type()

    def visit_UMinus(self, node):
        return self.visit(node.operation)

    def visit_IntNum(self, node):
        return Type(IntType)

    def visit_FloatNum(self, node):
        return Type(FloatType)

    def visit_String(self, node):
        return Type(StringType)

    def matrix_init_type(self, node, name):
        types = self.visit(node.values)
        if len(types) > 2:
            node.error('too many function arguments')
        if types[0].type != IntType:
            node.error(name + ' argument is not an int')
            return Type()
        values = node.values.children
        if len(types) == 1:
            if isinstance(values[0], AST.IntNum):
                return Type(MatrixType, IntType, values[0].value, values[0].value)
            return Type(MatrixType, IntType, undefined_size, undefined_size)
        if types[1].type != IntType:
            node.error(name + ' argument is not an int')
            return Type()
        x = undefined_size
        y = undefined_size
        if isinstance(values[0], AST.IntNum):
            x = values[0].value
        if isinstance(values[1], AST.IntNum):
            y = values[1].value
        return Type(MatrixType, IntType, x, y)

    def visit_Zeros(self, node):
        return self.matrix_init_type(node, 'zeros')

    def visit_Ones(self, node):
        return self.matrix_init_type(node, 'ones')

    def visit_Eye(self, node):
        return self.matrix_init_type(node, 'eye')

    def visit_ID(self, node):
        if node.name not in symbol_table:
            node.error('undeclared identifier ' + node.name)
            return Type()
        return symbol_table[node.name]

    def visit_Array(self, node):
        types = self.visit(node.child)
        first_type = types[0]
        if first_type.type is None:
            node.error('invalid array element')
            return Type()
        if first_type.type == StringType:
            node.error('cannot create vector of strings')
            return Type()
        if first_type.type == MatrixType:
            node.error('3D matrices are not supported')
            return Type()
        for op_type in types[1:]:
            # Wszystkie typy w wektorze/macierzy muszą być zgodne
            if op_type.type != first_type.type:
                node.error('invalid type in vector. Expected ' + str(first_type))
                return Type()
            elif op_type.type == VectorType and op_type.x != first_type.x:
                node.error('vector sizes mismatch')
                return Type()
        return first_type.extend(len(types))

    def visit_OperationsList(self, node):
        types = []
        for child in node.children:
            types.append(self.visit(child))
        return types

    def visit_Reference(self, node):
        id_type = symbol_table.get(node.name, Type())
        types = self.visit(node.reference)
        if id_type.type is None:
            node.error('undeclared identifier ' + node.name)
            return Type()
        if id_type.type == VectorType:
            if len(types) != 1:
                node.error('cannot reference vector with multiple indexes')
                return Type()
            if check_valid_reference(node, id_type, types, 0):
                return id_type.get_idx()
            return Type()
        elif id_type.type == MatrixType:
            if len(types) > 2:
                node.error('cannot reference matrix with more than two indexes')
                return Type()
            if len(types) == 1:
                if check_valid_reference(node, id_type, types, 0):
                    return id_type.get_idx()
                return Type()
            else:  # len = 2
                if not check_valid_reference(node, id_type, types, 0) or \
                   not check_valid_reference(node, id_type, types, 1):
                    return Type()
                return id_type.get_idx(True)
        else:
            node.error('cannot reference variable of type ' + str(id_type))
            return Type()

    def visit_Transposition(self, node):
        type1 = self.visit(node.child)
        if type1.type == MatrixType:
            return Type(MatrixType, type1.inner_type, type1.y, type1.x)
        if type1.type is None:
            return Type()
        node.error('cannot transpose variable of type ' + str(type1))
        return Type()
