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

import re
import os

class LexicalError(Exception):
    "To represent lexical errors"

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
            if not (char.isalnum() or char in "_\""):
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

    def operator_is_register(self, operator):
        "If operator is register"
        return operator in self.registers

    def operator_is_label(self, operator):
        "If operator is label"
        return str(operator).endswith(':') or operator in self.labels

    def operator_is_value(self, operator):
        "If operator is value"
        return not self.operator_is_register(operator) and not self.operator_is_label(operator)

    def operator_is_mnemonic(self, operator):
        "If operator is mnemonic"
        return operator in self.get_mnemonics()

    def get_operator(self, operator):
        "Get operator value based on register or pointer"
        # register
        if self.operator_is_register(operator):
            return self.registers[operator]
        # memory
        elif self.operator_is_label(operator):
            return self.memory[self.labels[operator]]
        # value
        else:
            if operator.isnumeric():
                astype = int
                if  '.' in operator:
                    astype = float
                return astype(operator)
            return operator

    def set_operator(self, operator_value, dst:str):
        "Set operator value based on register or label"
        if dst in self.labels:
            label = self.labels[dst]
            self.memory[label] = operator_value
        else:
            self.registers[dst] = operator_value

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
        "Read (1) or write (2) ascii character from memory address"
        if not address.isnumeric():
            return
        if _type == "1":
            self.memory[int(address)] = ord(input()[0])
        if _type == "2":
            print(chr(int(self.memory[int(address)])))

    @_mnemonic
    def halt(self):
        "Stop code"


if __name__ == "__main__":
    # Read path
    SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
    ASSEMBLY_FILE_PATH = input(
        "Insert a path or type Enter to read sample file './assembly-sample.txt'\n> ")
    if not ASSEMBLY_FILE_PATH:
        ASSEMBLY_FILE_PATH = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "assembly-sample.txt")
    MY_CODE = open(ASSEMBLY_FILE_PATH, "r", encoding="utf-8").read()

    # Run
    assembler = MiniAssembler()
    assembler.validate(MY_CODE)
    assembler.load(MY_CODE)
    assembler.run()
    print(assembler)
