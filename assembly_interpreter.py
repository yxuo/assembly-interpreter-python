"""
Este interpretador emula um processador hipotético.

Requisitos
    - CR armazena comparação
    - O interpretador deve avisar erro léxico, sintático ou semântico"""

class MiniAssembler:
    "Class for simple Assembly compiler and runner"
    def __init__(self):
        self.registers = {'CP': 0}
        self.labels = {}
        self.memory = [0] * 15 + [1.2]
        self.pc = 0
        self.instructions = []

    def __str__(self) -> str:
        return f"""\
Instructions:   {self.instructions}
Memory:         {self.memory}
Registers:      {self.registers}
PC:             {self.pc}
Labels:         {self.labels}\
        """

    def load(self, code):
        self.instructions = []
        self.labels = {}
        for i, line in enumerate(code.split('\n')):
            line = line.split("--")[0].strip()
            if not line:
                continue
            if ':' in line:
                label, line = line.split(':', 1)
                label = label.strip()
                if label in self.labels:
                    raise ValueError(f"Duplicate label '{label}' on line {i+1}")
                self.labels[label] = len(self.instructions)
            self.instructions.append(line)

    def run(self):
        while self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            operation, *args = instruction.split()
            if operation == "HALT":
                return
            if operation in ["MOVE","ADD","SUBT","JUMP","JTRUE","JFALSE","CMP","CMAIOR", "CMENOR",
                "MULT", "DIV", "VAR", "INT"]:
                getattr(self, operation.lower())(*[i.strip(',') for i in args])
            else:
                raise Exception(f'Unknown instruction: {instruction}')
            self.pc += 1

    def operator_is_register(self, src):
        return src in self.registers

    def operator_is_label(self, src):
        return src in self.labels and self.labels[src] in self.memory

    def operator_is_value(self, src):
        return not self.operator_is_register(src) and not self.operator_is_label(src)

    def get_operator(self, src):
        "Given source, get operator's value from registers or labels"
        # register
        if self.operator_is_register(src):
            return self.registers[src]
        # memory
        elif self.operator_is_label(src):
            return self.memory[self.labels[src]]
        # value
        else:
            if src.isnumeric():
                astype = int
                if  '.' in src:
                    astype = float
                return astype(src)
            return src

    def set_operator(self, value, reference:str):
        if reference[:0]+reference[:1] == "[]":
            label = self.labels[reference[1:-1]]
            self.memory[label] = value
        else:
            self.registers[reference] = value

    def move(self, dst, src):
        src_value = self.get_operator(src)
        self.set_operator(src_value, dst)

    def add(self, dst, src):
        self.set_operator(self.get_operator(dst) + self.get_operator(src), dst)

    def subt(self, dst, src):
        self.set_operator(self.get_operator(dst) - self.get_operator(src), dst)

    def mult(self, dst, src):
        self.set_operator(self.get_operator(dst) * self.get_operator(src), dst)

    def div(self, dst, src):
        self.set_operator(self.get_operator(dst) / self.get_operator(src), dst)

    def jump(self, dst:str):
        if dst.isnumeric():
            self.pc = int(dst) - 1
        else:
            self.pc = self.labels[dst] - 1

    def jtrue(self, dst):
        if self.registers['CP'] == 1:
            self.jump(dst)

    def jfalse(self, dst):
        if self.registers['CP'] == 0:
            self.jump(dst)

    def cmp(self, op1, op2):
        self.registers['CP'] = int(self.get_operator(op1) == self.get_operator(op2))

    def cmaior(self, op1, op2):
        self.registers['CP'] = int(self.get_operator(op1) > self.get_operator(op2))

    def cmenor(self, op1, op2):
        self.registers['CP'] = int(self.get_operator(op1) < self.get_operator(op2))

    def var(self, label, address):
        self.labels[label] = int(address)

    def int(self, _type, address:str):
        if not address.isnumeric():
            return
        if _type == "1":
            self.memory[int(address)] = ord(input()[0])
        if _type == "2":
            print(chr(int(self.memory[int(address)])))


MY_CODE = """\
    VAR     teste 3
    INT     1, 4
    INT     2, 4
    MOVE    A, 6        -- Coloco o valor 6 no registrador A
    MOVE    B, 5        -- Coloco o valor 5 no registrador A
enquanto:   MOVE  C, B  -- Coloco no registrador C o valor presente no registrador B
    CMP     B, 1        -- Comparo o valor presente em B com o valor 1. O resultado fica no registrador CR
    JTRUE   fim         -- Se CR tiver o valor 1, então JUMP para a linha com o label fim
    MOVE    B, C        -- Coloco em B o valor presente em C
    MULT    A, B        -- Multiplico o valor presente em A com o valor presente em B. O resultado ficará em A
    SUBT    B, 1        -- Subtraio 1 no o valor presente em B
    JUMP    enquanto    -- JUMP para linha com o label enquanto.
fim:        HALT
"""

assembler = MiniAssembler()
assembler.load(MY_CODE)
print(assembler.registers)
assembler.run()
# print(assembler)
print(assembler.registers) # {'A': 12, 'B': 10}
