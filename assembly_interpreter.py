"""
Este interpretador emula um processador hipotético.

Requisitos
    - CR armazena comparação
    - O interpretador deve avisar erro léxico, sintático ou semântico
"""

class LexicalError(Exception):
    """
    Raised when wrong characters are found
    kwargs:
        line:str, line_number:int, token_pos:int, token:Str
    """
    DEFAULT_MESSAGES = {
        "invalid_token": lambda l,n,t: f"'{t}' is not a valid token, at line {n}\n{l}",
        "expected_token": lambda l,n,t: f"expected token after '{t}' at line {n}\n{l}",
        "invalid_mnemonic": lambda l,n,t: f"invalid mnemonic name '{t}' at line {n}\n{l}",
    }

    def __init__(self, *args, **kwargs):
        if not args:
            args = [kwargs.get(k,None) for k,_ in ("line", "line_number", "token")]
        error_type = kwargs.get("error_type", "invalid_token")
        message = self.DEFAULT_MESSAGES[error_type](*args)
        super().__init__(message)


class SyntaxError1(Exception):
    "Raised when the input value is less than 18"


class MiniAssembler:
    "Class for simple Assembly compiler and runner"
    def __init__(self):
        self.registers = {'CP': 0}
        self.labels = {}
        self.memory = [0] * 15 + [1.2]
        self.pc = 0
        self.instructions = []
        self.mnemonics = ['MOVE', 'ADD', 'SUBT', 'JUMP', 'JTRUE', 'JFALSE',
            'CMP', 'CMAIOR', 'CMENOR', 'MULT', 'DIV', 'VAR', 'INT']

    def __str__(self) -> str:
        return f"""\
Instructions:   {self.instructions}
Memory:         {self.memory}
Registers:      {self.registers}
PC:             {self.pc}
Labels:         {self.labels}\
        """

    def load(self, code):
        "Load instructions to compiler"
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
        "Run code"
        while self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            operation, *args = instruction.split()
            if operation == "HALT":
                return
            if operation in self.mnemonics:
                getattr(self, operation.lower())(*[i.strip(',') for i in args])
            else:
                raise Exception(f'Unknown instruction: {instruction}')
            self.pc += 1

    def check_lexical_errors(self, input_code:str):
        """
        Check for lexical errors in a given line of assembly code.

        :param line: A string containing a line of assembly code.
        :return: A list of lexical errors found in the line, or an empty list if no errors were found.
        """
        errors = []

        # Check for invalid characters
        for i, line in enumerate(input_code.splitlines()):
            line_1 = line.split("--")[0].split()
            if not line_1:
                continue

            if not line[0].isalpha():
                raise LexicalError(line, i, line[0])

            chunk = 0
            # label
            is_label = line_1[chunk][-1] == ':'
            if is_label:
                label = line_1[chunk][:-1]
                for char in label:
                    if not char.isalnum():
                        raise LexicalError(line, i, char)
                chunk += 1
            # mnemonic
            else:
                mnemonic = line_1[chunk]

                if mnemonic not in self.mnemonics:
                    raise LexicalError(line, i, mnemonic, error_type="invalid_mnemonic")

                self.check_lexical_variable_name(mnemonic, i, line)
                chunk += 1

                # args
                args = line_1[chunk:]
                for j, arg in enumerate(args):
                    if arg[:0]+arg[:1] == "[]":
                        arg = arg[1:-1]
                    # TODO: add to syntatic error
                    # if arg[-1] == ',':
                    #     if j == len(args)-1:
                    #         raise LexicalError(line, i, ',', error_type="expected_token")
                        arg = arg[:-1]
                    self.check_lexical_variable_name(arg, i, line)

        return errors

    def check_lexical_variable_name(self, variable_name:str, line_number, line:str):
        "Validate lexical variable name"
        if variable_name[0].isnumeric() and not variable_name.isnumeric():
            raise LexicalError(line, line_number, variable_name[0])
        for char in variable_name:
            if not (char.isalnum() or char in "_"):
                raise LexicalError(line, line_number, char)

    def check_syntactic_errors(self, line):
        """
        Check for syntactic errors in a given line of assembly code.

        :param line: A string containing a line of assembly code.
        :return: A list of syntactic errors found in the line, or an empty list if no errors were found.
        """
        errors = []
        # Split the line into its components
        label, sep, rest = line.partition(':')
        mnemonic, sep, operands = rest.lstrip().partition(' ')
        operands = operands.split(',')

        # Check for invalid label
        if label and not label.isalnum():
            errors.append('Invalid label')

        # Check for invalid mnemonic
        if mnemonic not in self.mnemonics:
            errors.append('Invalid mnemonic')

        # Check for invalid number of operands
        if mnemonic in ['MOVE', 'ADD', 'SUBT', 'MULT', 'DIV'] and len(operands) != 2:
            errors.append('Invalid number of operands')

        return errors


    def operator_is_register(self, src):
        "If operator is register"
        return src in self.registers

    def operator_is_label(self, src):
        "If operator is label"
        return src in self.labels and self.labels[src] in self.memory

    def operator_is_value(self, src):
        "If operator is value"
        return not self.operator_is_register(src) and not self.operator_is_label(src)

    def get_operator(self, src):
        "Get operator value based on register or pointer"
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
        "Set operator value based on register or pointer"
        if reference[:0]+reference[:1] == "[]":
            label = self.labels[reference[1:-1]]
            self.memory[label] = value
        else:
            self.registers[reference] = value

    def move(self, dst, src):
        "Create or update value to variable"
        src_value = self.get_operator(src)
        self.set_operator(src_value, dst)

    def add(self, dst, src):
        "Add number to register"
        self.set_operator(self.get_operator(dst) + self.get_operator(src), dst)

    def subt(self, dst, src):
        "Subtract number to register"
        self.set_operator(self.get_operator(dst) - self.get_operator(src), dst)

    def mult(self, dst, src):
        "Multiply number to register"
        self.set_operator(self.get_operator(dst) * self.get_operator(src), dst)

    def div(self, dst, src):
        "Divide number to register. "
        self.set_operator(self.get_operator(dst) / self.get_operator(src), dst)

    def jump(self, dst:str):
        "Jump to label or line number"
        if dst.isnumeric():
            self.pc = int(dst) - 1
        else:
            self.pc = self.labels[dst] - 1

    def jtrue(self, dst):
        "Jump to label or line number if CMP is true"
        if self.registers['CP'] == 1:
            self.jump(dst)

    def jfalse(self, dst):
        "Jump to label or line number if CMP is false"
        if self.registers['CP'] == 0:
            self.jump(dst)

    def cmp(self, op1, op2):
        "Compare values and save result in CP"
        self.registers['CP'] = int(self.get_operator(op1) == self.get_operator(op2))

    def cmaior(self, op1, op2):
        "Check if the first value is greater than the second value."
        self.registers['CP'] = int(self.get_operator(op1) > self.get_operator(op2))

    def cmenor(self, op1, op2):
        "Check if the first value is lower than the second value."
        self.registers['CP'] = int(self.get_operator(op1) < self.get_operator(op2))

    def var(self, label, address):
        "Associates a label to a memory address"
        self.labels[label] = int(address)

    def int(self, _type, address:str):
        "Read/write ascii character from memory address"
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
assembler.check_lexical_errors("VAR     test 3 --s dggsgdfdgf")
# assembler.load(MY_CODE)
# print(assembler.registers)
# assembler.run()
# print(assembler)
# print(assembler.registers) # {'A': 12, 'B': 10}
