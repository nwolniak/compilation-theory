class Node(object):
    lineno = None
    error_occurred = False
    def error(self, desc):
        print("Error at line " + str(self.lineno) + ": " + desc + ".")


class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instructions = []
        if instructions:
            self.instructions = instructions.instructions
        if instruction:
            self.instructions.append(instruction)


class Assignment(Node):
    def __init__(self, op, identifier, operations):
        self.op = op
        self.identifier = identifier
        self.operations = operations


class IfInstruction(Node):
    def __init__(self, condition, if_instruction, else_instruction=None):
        self.condition = condition
        self.if_instruction = if_instruction
        self.else_instruction = else_instruction


class ForLoop(Node):
    def __init__(self, id, start, end, instruction):
        self.id = id
        self.start = start
        self.end = end
        self.instruction = instruction


class WhileLoop(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class PrintInstruction(Node):
    def __init__(self, children):
        self.children = children


class ReturnInstruction(Node):
    def __init__(self, child):
        self.child = child


class Break(Node):
    pass


class Continue(Node):
    pass


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UMinus(Node):
    def __init__(self, operation):
        self.operation = operation


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Zeros(Node):
    def __init__(self, values):
        self.values = values


class Ones(Node):
    def __init__(self, values):
        self.values = values


class Eye(Node):
    def __init__(self, values):
        self.values = values


class ID(Node):
    def __init__(self, name):
        self.name = name


class Array(Node):
    def __init__(self, child):
        self.child = child


class OperationsList(Node):
    def __init__(self, children, operations):
        self.children = []
        if children:
            self.children += children.children
        if operations:
            self.children.append(operations)


class Reference(Node):
    def __init__(self, identifier, reference):
        self.name = identifier
        self.reference = reference


class Transposition(Node):
    def __init__(self, child):
        self.child = child


class Error(Node):
    def __init__(self):
        pass
