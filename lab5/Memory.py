from collections import defaultdict

class Memory:
    def __init__(self, name='global'): # memory name
        self.name = name
        self.variables = defaultdict(None)

    def get(self, name): # gets from memory current value of variable <name>
        return self.variables.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value

class MemoryStack:
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []
        if memory is None:
            self.stack.append(Memory('global'))
        else:
            self.stack.append(memory)

    def get(self, name):             # gets from memory stack current value of variable <name>
        for memory in self.stack[::-1]:
            value = memory.get(name)
            if value is not None:
                return value
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for memory in self.stack[::-1]:
            if memory.get(name) is not None:
                memory.put(name, value)
                return
        self.insert(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()
