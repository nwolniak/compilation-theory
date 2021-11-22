class Node(object):
    pass


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
    def __init__(self, id, start_range, end_range, instruction):
        self.id = id
        self.start_range = start_range
        self.end_range = end_range
        self.instruction = instruction


class WhileLoop(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class PrintInstruction(Node):
    def __init__(self, operations_list):
        self.operations_list = operations_list


class ReturnInstruction(Node):
    def __init__(self, operations):
        self.operations = operations


class Break(Node):
    pass


class Continue(Node):
    pass


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


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
    def __init__(self, value):
        self.value = value


class Ones(Node):
    def __init__(self, value):
        self.value = value


class Eye(Node):
    def __init__(self, value):
        self.value = value


class ID(Node):
    def __init__(self, name):
        self.name = name


class Array(Node):
    def __init__(self, inside_array):
        self.inside_array = inside_array


class OperationsList(Node):
    def __init__(self, operations_list, operations):
        self.operations_list = []
        if operations_list:
            self.operations_list += operations_list.operations_list
        if operations:
            self.operations_list.append(operations)


class Reference(Node):
    def __init__(self, identifier, reference):
        self.identifier = identifier
        self.reference = reference


class Transposition(Node):
    def __init__(self, transposed):
        self.transposed = transposed


class Error(Node):
    def __init__(self):
        pass
