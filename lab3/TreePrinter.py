from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @classmethod
    def printRow(cls, depth, elem):
        print(" | " * depth, elem)

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, self.op)
        self.identifier.printTree(indent + 1)
        self.operations.printTree(indent + 1)

    @addToClass(AST.IfInstruction)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "IF")
        self.condition.printTree(indent + 1)
        TreePrinter.printRow(indent, "THEN")
        self.if_instruction.printTree(indent + 1)
        if self.else_instruction:
            TreePrinter.printRow(indent, "ELSE")
            self.else_instruction.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "FOR")
        TreePrinter.printRow(indent + 1, self.id)
        TreePrinter.printRow(indent + 1, "RANGE")
        self.start_range.printTree(indent + 2)
        self.end_range.printTree(indent + 2)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "WHILE")
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "PRINT")
        self.operations_list.printTree(indent + 1)

    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "RETURN")
        if self.operations:
            self.operations.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "CONTINUE")

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, self.op)
        if self.left:
            self.left.printTree(indent + 1)
        if self.right:
            self.right.printTree(indent + 1)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, self.value)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, self.value)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, self.value)

    @addToClass(AST.Zeros)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "ZEROS")
        TreePrinter.printRow(indent + 1, self.value)

    @addToClass(AST.Ones)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "ONES")
        TreePrinter.printRow(indent + 1, self.value)

    @addToClass(AST.Eye)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "EYE")
        TreePrinter.printRow(indent + 1, self.value)

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, self.name)

    @addToClass(AST.Array)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "VECTOR")
        self.inside_array.printTree(indent + 1)

    @addToClass(AST.OperationsList)
    def printTree(self, indent=0):
        for operations in self.operations_list:
            operations.printTree(indent + 1)

    @addToClass(AST.Reference)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "REFERENCE")
        self.identifier.printTree(indent + 1)
        self.reference.printTree(indent + 1)

    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        TreePrinter.printRow(indent, "TRANPOSITION")
        self.transposed.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
