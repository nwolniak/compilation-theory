import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator
import numpy

sys.setrecursionlimit(10000)

MatrixType = 'matrix'
VectorType = 'vector'
VariableType = 'variable'
# Operacje między zmiennymi
var_op = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y,
    '>=': lambda x, y: x >= y,
    '!=': lambda x, y: x != y,
    '==': lambda x, y: x == y
}
# Operacje wektorowe
vector_op = {
    '+': lambda x, y: list(map(operator.add, x, y)),
    '-': lambda x, y: list(map(operator.sub, x, y)),
    '*': lambda x, y: list(map(lambda a: a * x, x)),
    '/': lambda x, y: list(map(lambda a: a // y, x)),
    '.+': lambda x, y: list(map(operator.add, x, y)),
    '.-': lambda x, y: list(map(operator.sub, x, y)),
    '.*': lambda x, y: list(map(operator.mul, x, y)),
    './': lambda x, y: list(map(operator.truediv, x, y))
}
# Operacje macierzowe
matrix_op = {
    '+': lambda x, y: [list(map(operator.add, row_x, row_y)) for row_x, row_y in zip(x, y)],
    '-': lambda x, y: [list(map(operator.sub, row_x, row_y)) for row_x, row_y in zip(x, y)],
    '*': lambda x, y: [list(map(lambda a: a * y, row_x)) for row_x in x],
    '/': lambda x, y: [list(map(lambda a: a // y, row_x)) for row_x in x],
    '.+': lambda x, y: [list(map(operator.add, row_x, row_y)) for row_x, row_y in zip(x, y)],
    '.-': lambda x, y: [list(map(operator.sub, row_x, row_y)) for row_x, row_y in zip(x, y)],
    '.*': lambda x, y: [list(map(operator.mul, row_x, row_y)) for row_x, row_y in zip(x, y)],
    './': lambda x, y: [list(map(operator.truediv, row_x, row_y)) for row_x, row_y in zip(x, y)]
}
matrix_mul = lambda x, y: list(map(list, numpy.matmul(x, y)))


class Interpreter(object):

    def __init__(self):
        self.memory = Memory()

    # Oblicza wynik operacji binarnej op między x i y
    def bin_op(self, op, x, y):
        type1 = VariableType
        type2 = VariableType
        if isinstance(x, list):
            if isinstance(x[0], list):
                type1 = MatrixType
            else:
                type1 = VectorType
        if isinstance(y, list):
            if isinstance(y[0], list):
                type2 = MatrixType
            else:
                type2 = VectorType

        if op == '*' and type1 != VariableType and type2 != VariableType:
            return matrix_mul(x, y)
        if type1 == MatrixType:
            return matrix_op.get(op, lambda: None)(x, y)
        if type1 == VectorType:
            return vector_op.get(op, lambda: None)(x, y)
        return var_op.get(op, lambda: None)(x, y)

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        ret = 0
        try:
            self.visit(node.instructions)
        except ReturnValueException as e:
            ret = e.value
        except RuntimeException as e:
            print("Runtime exception: " + e.description)
            ret = -1
        print("Memory : ", self.memory.variables)
        return ret

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    @when(AST.Assignment)
    def visit(self, node):
        identifier = node.identifier.name
        val = self.visit(node.operations)
        if node.op != '=':
            id_val = self.visit(node.identifier)
            try:
                val = self.bin_op(node.op[0], id_val, val)
            except Exception:
                raise RuntimeException(node.op + " operation error at line " + str(node.lineno))
        if isinstance(node.identifier, AST.Reference):
            id_mem = self.memory.get(identifier)
            idxs = node.identifier.reference.children
            if len(idxs) == 1:
                if len(val) != len(id_mem[idxs[0].value]):
                    raise RuntimeException("invalid vector size at line " + str(node.lineno))
                id_mem[idxs[0].value] = val
            else:
                id_mem[idxs[0].value][idxs[1].value] = val
            self.memory.put(identifier, id_mem)
        else:
            self.memory.put(identifier, val)

    @when(AST.IfInstruction)
    def visit(self, node):
        if self.visit(node.condition):
            return self.visit(node.if_instruction)
        elif node.else_instruction is not None:
            return self.visit(node.else_instruction)

    @when(AST.ForLoop)
    def visit(self, node):
        identifier = node.id.name
        start_range = self.visit(node.start)
        end_range = self.visit(node.end)

        for i in range(start_range, end_range):
            self.memory.put(identifier, i)
            try:
                self.visit(node.instruction)
            except BreakException:
                break
            except ContinueException:
                continue

    @when(AST.WhileLoop)
    def visit(self, node):
        while self.visit(node.condition):
            try:
                self.visit(node.instruction)
            except BreakException:
                break
            except ContinueException:
                continue

    @when(AST.PrintInstruction)
    def visit(self, node):
        print(*[x for x in self.visit(node.children)])

    @when(AST.ReturnInstruction)
    def visit(self, node):
        if node.child is not None:
            raise ReturnValueException(self.visit(node.child))
        raise ReturnValueException(0)

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.BinExpr)
    def visit(self, node):
        x = self.visit(node.left)
        y = self.visit(node.right)
        try:
            return self.bin_op(node.op, x, y)
        except Exception:
            raise RuntimeException(node.op + " operation error at line " + str(node.lineno))

    @when(AST.UMinus)
    def visit(self, node):
        return (-1) * self.visit(node.operation)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Zeros)
    def visit(self, node):
        shape = self.visit(node.values)
        if len(shape) == 1:
            shape.append(shape[0])
        return [[0 for _ in range(shape[1])] for _ in range(shape[0])]

    @when(AST.Ones)
    def visit(self, node):
        shape = self.visit(node.values)
        if len(shape) == 1:
            shape.append(shape[0])
        return [[1 for _ in range(shape[1])] for _ in range(shape[0])]

    @when(AST.Eye)
    def visit(self, node):
        shape = self.visit(node.values)
        if len(shape) == 1:
            shape.append(shape[0])
        return [[1 if i == j else 0 for i in range(shape[1])] for j in range(shape[0])]

    @when(AST.ID)
    def visit(self, node):
        id_name = node.name
        if self.memory.get(id_name) is None:
            raise RuntimeException("undeclared identifier " + id_name + " at line " + str(node.lineno))
        return self.memory.get(id_name)

    @when(AST.Array)
    def visit(self, node):
        return self.visit(node.child)

    @when(AST.OperationsList)
    def visit(self, node):
        res = []
        for child in node.children:
            res.append(self.visit(child))
        return res

    @when(AST.Transposition)
    def visit(self, node):
        arr = self.visit(node.child)
        arr_t = [list(row) for row in zip(*arr)]
        return arr_t

    @when(AST.Reference)
    def visit(self, node):
        idxs_list = self.visit(node.reference)
        var = self.memory.get(node.name)
        if len(var) < idxs_list[0]:
            raise RuntimeException("invalid reference to " + node.name + " at line " + str(node.lineno))
        if len(idxs_list) == 1:
            return var[idxs_list[0]]
        else:
            if len(var[idxs_list[0]]) < idxs_list[1]:
                raise RuntimeException("invalid reference to " + node.name + " at line " + str(node.lineno))
            return var[idxs_list[0]][idxs_list[1]]
