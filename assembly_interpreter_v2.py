"""
suggest me a OOP code to emulate a mini assembly compiler, in python.
"""

class MiniAssembler:
    def __init__(self):
        self.registers = {'A': 0, 'B': 0}
        self.memory = [0] * 256
        self.pc = 0
        self.instructions = []

    def load(self, instructions):
        self.instructions = instructions

    def run(self):
        while self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            op, *args = instruction.split()
            if op == 'MOV':
                self.mov(*args)
            elif op == 'ADD':
                self.add(*args)
            elif op == 'SUB':
                self.sub(*args)
            elif op == 'JMP':
                self.jmp(*args)
            elif op == 'JZ':
                self.jz(*args)  
            elif op == 'JNZ':
                self.jnz(*args)
            else:
                raise Exception(f'Unknown instruction: {instruction}')
            self.pc += 1

    def mov(self, dst, src):
        if src in self.registers:
            src_value = self.registers[src]
        else:
            src_value = int(src)
        if dst in self.registers:
            self.registers[dst] = src_value
        else:
            dst_address = int(dst[1:-1])
            self.memory[dst_address] = src_value

    def add(self, dst, src):
        if src in self.registers:
            src_value = self.registers[src]
        else:
            src_value = int(src)
        if dst in self.registers:
            self.registers[dst] += src_value
        else:
            dst_address = int(dst[1:-1])
            self.memory[dst_address] += src_value

    def sub(self, dst, src):
        if src in self.registers:
            src_value = self.registers[src]
        else:
            src_value = int(src)
        if dst in self.registers:
            self.registers[dst] -= src_value
        else:
            dst_address = int(dst[1:-1])
            self.memory[dst_address] -= src_value

    def jmp(self, address):
        address = int(address)
        self.pc = address - 1

    def jz(self, address):
        address = int(address)
        if self.registers['A'] == 0:
            self.pc = address - 1

    def jnz(self, address):
        address = int(address)
        if self.registers['A'] != 0:
            self.pc = address - 1


instructions = [
    'MOV A 5',
    'MOV B 10',
    'ADD A B',
    'SUB A 3',
    'JZ 7',
    'JMP 8',
    'MOV A 0',
]

assembler = MiniAssembler()
assembler.load(instructions)
assembler.run()
print(assembler.registers) # {'A': 12, 'B': 10}
