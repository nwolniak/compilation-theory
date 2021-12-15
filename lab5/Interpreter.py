import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory = Memory()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        ret = self.visit(node.instructions)
        print("Memory : ", self.memory.variables)
        if ret:
            return 0
        else:
            return -1

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    @when(AST.Assignment)
    def visit(self, node):
        identifier = node.identifier.name
        identifier_value = self.visit(node.identifier)
        val = self.visit(node.operations)
        return {
            '=': lambda: self.memory.put(identifier, val),
            '+=': lambda: self.memory.put(identifier, identifier_value + val),
            '-=': lambda: self.memory.put(identifier, identifier_value - val),
            '*=': lambda: self.memory.put(identifier, identifier_value * val),
            '/=': lambda: self.memory.put(identifier, identifier_value / val)
        }.get(node.op, lambda: None)()

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
            except ReturnValueException as ret:
                print("Return value : ", ret.value)
                return ret.value
            except BreakException:
                print("Break")
                break
            except ContinueException:
                print("Continue")
                continue

    @when(AST.WhileLoop)
    def visit(self, node):
        while self.visit(node.condition):
            try:
                self.visit(node.instruction)
            except ReturnValueException as ret:
                print("Return value : ", ret.value)
                return ret.value
            except BreakException:
                print("Break")
                break
            except ContinueException:
                print("Continue")
                continue

    @when(AST.PrintInstruction)
    def visit(self, node):
        print(",".join([str(x) for x in self.visit(node.children)]))

    @when(AST.ReturnInstruction)
    def visit(self, node):
        raise ReturnValueException(self.visit(node.child))

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
        return {
            '+': lambda: x + y,
            '-': lambda: x - y,
            '*': lambda: x * y,
            '/': lambda: x / y,
            '>': lambda: x > y,
            '<': lambda: x < y,
            '<=': lambda: x <= y,
            '>=': lambda: x >= y,
            '!=': lambda: x != y,
            '==': lambda: x == y,
            '.+': lambda: list(map(operator.add, x, y)),
            '.-': lambda: list(map(operator.sub, x, y)),
            '.*': lambda: list(map(operator.mul, x, y)),
            './': lambda: list(map(operator.truediv, x, y))  # floordiv like //
        }.get(node.op, lambda: None)()

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
            return [0 for _ in range(shape[0])]
        else:
            return [[0 for _ in range(shape[1])] for _ in range(shape[0])]

    @when(AST.Ones)
    def visit(self, node):
        shape = self.visit(node.values)
        if len(shape) == 1:
            return [1 for _ in range(shape[0])]
        else:
            return [[0 for _ in range(shape[1])] for _ in range(shape[0])]

    @when(AST.Eye)
    def visit(self, node):
        shape = self.visit(node.values)
        return [[1 if i == j else 0 for i in range(shape[1])] for j in range(shape[0])]

    @when(AST.ID)
    def visit(self, node):
        r = node.name
        if self.memory.get(r) is not None:
            r = self.memory.get(r)
        return r

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
        if len(idxs_list) == 1:
            return self.memory.get(node.name)[idxs_list[0]]
        else:
            return self.memory.get(node.name)[idxs_list[0]][idxs_list[1]]
