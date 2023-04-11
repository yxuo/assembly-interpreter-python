"""
Este interpretador emula um processador hipotético.

Requisitos
    - CR armazena comparação
    - O interpretador deve avisar erro léxico, sintático ou semântico

Fonte:
    - https://www.javatpoint.com/lexical-error
    - https://www.javatpoint.com/syntax-error
    - https://www.javatpoint.com/semantic-error
"""

import inspect
import re

class LexicalError(Exception):
    "To represent lexical errors"

def universe(function):

    def function_wrapper():
        return function()

    function_wrapper.a = 1
    function_wrapper.__doc__ = "doc2"
    function_wrapper.__name__ = function.__name__
    
    return function_wrapper

def _mnemonic(*args, **kwargs):
    "Mnemonic metadata for MiniAssembler"

    # @decorator()
    def decorator(func):
        data = {"param_type": []}
        if kwargs:
            data = kwargs
        func.mnemonic = data
        return func

    # @decorator
    if args:
        function = decorator(args[0])
        return function

    return decorator

def _mnemonic1(mnemonic):
    "Decorador for mnemonics in MiniAssembler"
    def decorator(func):
        func.mnemonic = mnemonic
        return func
    return decorator

class MiniAssembler:
    "Class for simple Assembly compiler and runner"

    def __str__(self) -> str:
        return f"""\
Instructions:   {self.instructions}
Memory:         {self.memory}
Registers:      {self.registers}
PC:             {self.pc}
Labels:         {self.labels}\
        """

    ERROR_MESSAGES = {
        "invalid_mnemonic": lambda l,n,t: f"'{t}' is not a valid mnemonic, at line {n}\n{l}",
        "invalid_token": lambda l,n,t: f"'{t}' is not a valid token, at line {n}\n{l}",
        "expected_token": lambda l,n,t: f"expected token after '{t}' at line {n}\n{l}",
        "operator_not_found": lambda l,n,t: f"operator name not found '{t}' at line {n}\n{l}",
        "duplicated_token": lambda l,n,t: \
            f"token '{t}' duplicated at line {n}\n{l}",
        "expected_closing": lambda l,n,t: \
            f"expected closing '{t}' at line {n}\n{l}",
        "expected_operator": lambda l,n,t: f"expected operator after '{t}' at line {n}\n{l}",
    }

    def __init__(self):
        self.registers = {'CP': 0}
        self.labels = {}
        self.memory = [0] * 15 + [1.2]
        self.pc = 0
        self.instructions = []

    def load(self, code):
        "Load instructions to compiler"
        self.instructions = []
        self.labels = {}
        for i, line in enumerate(code.split('\n')):
            line_1 = line.split("--")[0].strip()
            if not line_1:
                continue
            if ':' in line_1:
                label, line_1 = line_1.split(':', 1)
                label = label.strip()
                if label in self.labels:
                    raise ValueError(f"Duplicate label '{label}' on line {i+1}")
                self.labels[label] = len(self.instructions)
            self.instructions.append(line_1)

    def validate(self, code):
        "Load instructions to compiler"
        self.instructions = []
        self.labels = {}
        for i, line in enumerate(code.split('\n')):
            line_1 = line.split("--")[0].strip()
            if not line_1:
                continue

            self.check_lexical_errors(line, i)
            self.check_syntax_errors(line, i)

    def run(self):
        "Run code"
        while self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            operation, *args = instruction.split()
            if operation == "HALT":
                return
            if operation in self.get_mnemonics():
                getattr(self, operation.lower())(*[i.strip(',') for i in args])
            else:
                raise Exception(f'Unknown instruction: {instruction}')
            self.pc += 1

    def check_lexical_errors(self, line:str, line_index):
        "Check for lexical errors in a given line of assembly code"

        # Check for invalid characters
        line = line.strip()
        line_1 = line.split("--")[0].split()
        if not line_1:
            return

        # For each token, lexic check
        for token in line_1:
            self.validate_token_lexic(token, line_index, line)

    def validate_token_lexic(self, token:str, line_number, line:str):
        "Validate token name"
        if token[-1] == ',':
            token = token[:-1]
        if token[-1] == ':':
            token = token[:-1]
        if token[0].isnumeric() and not token.isnumeric():
            raise LexicalError(self.ERROR_MESSAGES["invalid_token"](
                line, line_number, token))
        for char in token:
            if not (char.isalnum() or char in "_"):
                raise LexicalError(self.ERROR_MESSAGES["invalid_token"](line, line_number, char))

    def treat_line(self, line:str) -> list:
        "Treat assembly line and return teated line and a list of tokens"
        line_treated = line.strip()  # Ignore spaces
        line_treated = line_treated.split("--")[0]  # Ignore comment
        line_treated = re.sub(r'"[^"]*"', '""', line_treated)
        return line_treated

    def check_syntax_errors(self, line:str, line_index):
        """
        Check for lexical errors in a given line of assembly code.

        line: A string containing a line of assembly code.
        return: A list of lexical errors found in the line,\
            or an empty list if no errors were found.

        Criteria:
            - Error in structure
            - Missing operators
            - Unbalanced parenthesis or quotes, etc
        """

        # Check for invalid characters
        line_treated = self.treat_line(line)
        tokens = line_treated.split()

        if not tokens:
            return

        # open close string
        if line_treated.count('"') % 2:  # if number of " is odd
            raise SyntaxError(self.ERROR_MESSAGES["expected_closing"](line, line_index, '"'))

        # label unique two dots
        if line_treated.count(':') > 1:
            raise SyntaxError(self.ERROR_MESSAGES["duplicated_token"](line, line_index, ':'))

        # label, mnemonic
        operator_index = 0
        if self.operator_is_label(tokens[operator_index]):
            operator_index += 1
        if self.operator_is_mnemonic(tokens[operator_index]):
            operator_index += 1
        else:
            raise SyntaxError(self.ERROR_MESSAGES["invalid_mnemonic"](
                line, line_index, tokens[operator_index]))

        operators = tokens[operator_index:]
        if operators:
            commas = ''.join(operators).count(',')
            if commas < len(operators)-1:
                raise SyntaxError(self.ERROR_MESSAGES["expected_operator"](line, line_index, ','))
            if commas > len(operators)-1:
                raise SyntaxError(self.ERROR_MESSAGES["expected_token"](line, line_index, ','))

    def validate_operator_semantic(self, opr, line, line_index):
        "Validate register, [pointer], or literal"

        if self.operator_is_label(opr) and self.operator_is_register(opr):
            raise SyntaxError(self.ERROR_MESSAGES["duplicated_operator"](
                line, line_index, opr[-1:]))

    def check_semantic_errors(self, line):
        """
        Check for syntactic errors in a given line of assembly code.

        :param line: A string containing a line of assembly code.
        :return: A list of syntactic errors found in the line, or an empty list if no errors were found.

        Criteria:
            - pre defined mnemonic exists
            - missing or expected token or operator
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
        if mnemonic not in self.get_mnemonics():
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
        return str(src).endswith(':') or src in self.labels

    def operator_is_value(self, src):
        "If operator is value"
        return not self.operator_is_register(src) and not self.operator_is_label(src)

    def operator_is_mnemonic(self, src):
        "If operator is mnemonic"
        return src in self.get_mnemonics()

    def get_operator(self, src):
        "Get operator value based on register or pointer"
        # register
        if self.operator_is_register(src):
            return self.registers[src]
        # memory
        elif src in self.labels:
            return self.memory[self.labels[src]]
        # value
        else:
            if src.isnumeric():
                astype = int
                if  '.' in src:
                    astype = float
                return astype(src)
            return src

    def set_operator(self, src_value, dst:str):
        "Set operator value based on register or label"
        if dst in self.labels:
            label = self.labels[dst]
            self.memory[label] = src_value
        else:
            self.registers[dst] = src_value

    def get_mnemonics(self):
        "Return a list of mnemonic names"
        return {method.upper(): getattr(self, method).mnemonic for method in dir(self)
            if callable(getattr(self, method)) and hasattr(getattr(self, method), 'mnemonic')}

    @_mnemonic(param_type=[["reg", "label"], ["reg", "label", "literal"]])
    def move(self, dst, src):
        "Create or update value to variable"
        src_value = self.get_operator(src)
        self.set_operator(src_value, dst)

    @_mnemonic(param_type=[["reg", "label"], ["reg", "label", "literal"]])
    def add(self, dst, src):
        "Add number to register"
        self.set_operator(self.get_operator(dst) + self.get_operator(src), dst)

    @_mnemonic(param_type=[["reg", "label"], ["reg", "label", "literal"]])
    def subt(self, dst, src):
        "Subtract number to register"
        self.set_operator(self.get_operator(dst) - self.get_operator(src), dst)

    @_mnemonic(param_type=[["reg", "label"], ["reg", "label", "literal"]])
    def mult(self, dst, src):
        "Multiply number to register"
        self.set_operator(self.get_operator(dst) * self.get_operator(src), dst)

    @_mnemonic(param_type=[["reg", "label"], ["reg", "label", "literal"]])
    def div(self, dst, src):
        "Divide number to register. "
        self.set_operator(self.get_operator(dst) / self.get_operator(src), dst)

    @_mnemonic(param_type=[["literal", "label"]])
    def jump(self, dst:str):
        "Jump to label or line number"
        if dst.isnumeric():
            self.pc = int(dst) - 1
        else:
            self.pc = self.labels[dst] - 1

    @_mnemonic(param_type=[["literal", "label"]])
    def jtrue(self, dst):
        "Jump to label or line number if CMP is true"
        if self.registers['CP'] == 1:
            self.jump(dst)

    @_mnemonic(param_type=[["literal", "label"]])
    def jfalse(self, dst):
        "Jump to label or line number if CMP is false"
        if self.registers['CP'] == 0:
            self.jump(dst)

    @_mnemonic(param_type=[["reg", "label", "literal"], ["reg", "label", "literal"]])
    def cmp(self, op1, op2):
        "Compare values and save result in CP"
        self.registers['CP'] = int(self.get_operator(op1) == self.get_operator(op2))

    @_mnemonic(param_type=[["reg", "label", "literal"], ["reg", "label", "literal"]])
    def cmaior(self, op1, op2):
        "Check if the first value is greater than the second value."
        self.registers['CP'] = int(self.get_operator(op1) > self.get_operator(op2))

    @_mnemonic(param_type=[["reg", "label", "literal"], ["reg", "label", "literal"]])
    def cmenor(self, op1, op2):
        "Check if the first value is lower than the second value."
        self.registers['CP'] = int(self.get_operator(op1) < self.get_operator(op2))

    @_mnemonic(param_type=[["label"], ["addr"]])
    def var(self, label, address):
        "Associates a label to a memory address"
        self.labels[label] = int(address)

    @_mnemonic(param_type=[["addr"]])
    def int(self, _type, address:str):
        "Read/write ascii character from memory address"
        if not address.isnumeric():
            return
        if _type == "1":
            self.memory[int(address)] = ord(input()[0])
        if _type == "2":
            print(chr(int(self.memory[int(address)])))

    @_mnemonic
    def halt(self):
        "Stop code"

MY_CODE = """\
    VAR     teste, 3
    MOVE    teste, 10
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

if __name__ == "__main__":
    assembler = MiniAssembler()
    assembler.validate(MY_CODE)
    assembler.load(MY_CODE)
    # print(assembler.registers)
    assembler.run()
    print(assembler)
    # print(assembler.registers) # {'A': 12, 'B