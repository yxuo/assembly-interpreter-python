"""Arquivo para classe do mnemonico ADD"""

from interpretador_assembly.modelos.mnemonico import Mnemonico
from interpretador_assembly.interpretador_assembly import InterpretadorAssembly

class ADD(Mnemonico):
    """
    Adiciona um número ao registrador
    A soma será destino + origem
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "variavel_destino",
                "tipos_permitidos": ["registrador", "label"]
            },
            {
                "nome": "variavel_origem",
                "tipos_permitidos": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly, params:list):
        # Ler parâmetros
        destino, origem = params

        valor_destino = interpretador_assembly.get_operator(destino)
        valor_origem = interpretador_assembly.get_operator(origem)

        # Calcular
        resultado = valor_destino + valor_origem
        interpretador_assembly.set_operator(resultado, destino)


class MOVE(Mnemonico):
    """
    Classe do mnemonico MOVE
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "destino",
                "tipos_permitidos": ["registrador", "label"]
            },
            {
                "nome": "origem",
                "tipos_permitidos": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly, params:list):
        # Ler parâmetros
        destino, origem = params

        # obtém o valor do token, seja ele um registrador, label, etc
        valor_origem = interpretador_assembly.get_operator(origem)

        # token destino = valor do token origem
        interpretador_assembly.set_operator(valor_origem, destino)


class SUBT(Mnemonico):
    """
    Classe do mnemonico SUBT
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "variavel_destino",
                "tipos_permitidos": ["registrador", "label"]
            },
            {
                "nome": "variavel_origem",
                "tipos_permitidos": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly, params:list):
        """
        Adiciona um número ao registrador
        A soma será destino + origem

        Parâmetros
        ---
        ``variavel_destino`` (registrador ou label):
            O local onde o resultado da adição é salvo

        ``variavel_origem`` (registrador, label, literal):
            Um dos valores a ser somado
        """

        # Ler parâmetros
        destino, origem = params

        valor_destino = interpretador_assembly.get_operator(destino)
        valor_origem = interpretador_assembly.get_operator(origem)

        # Calcular
        resultado = valor_destino - valor_origem
        interpretador_assembly.set_operator(resultado, destino)


class MULT(Mnemonico):
    """
    Classe do mnemonico MULT
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "variavel_destino",
                "tipos_permitidos": ["registrador", "label"]
            },
            {
                "nome": "variavel_origem",
                "tipos_permitidos": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly, params:list):
        """
        Adiciona um número ao registrador
        A soma será destino + origem

        Parâmetros
        ---
        ``variavel_destino`` (registrador ou label):
            O local onde o resultado da adição é salvo

        ``variavel_origem`` (registrador, label, literal):
            Um dos valores a ser somado
        """

        # Ler parâmetros
        destino, origem = params

        valor_destino = interpretador_assembly.get_operator(destino)
        valor_origem = interpretador_assembly.get_operator(origem)

        # Calcular
        resultado = valor_destino * valor_origem
        interpretador_assembly.set_operator(resultado, destino)


class DIV(Mnemonico):
    """
    Classe do mnemonico ADD
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "variavel_destino",
                "tipos_permitidos": ["registrador", "label"]
            },
            {
                "nome": "variavel_origem",
                "tipos_permitidos": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly, params:list):
        """
        Adiciona um número ao registrador
        A soma será destino + origem

        Parâmetros
        ---
        ``variavel_destino`` (registrador ou label):
            O local onde o resultado da adição é salvo

        ``variavel_origem`` (registrador, label, literal):
            Um dos valores a ser somado
        """

        # Ler parâmetros
        destino, origem = params

        valor_destino = interpretador_assembly.get_operator(destino)
        valor_origem = interpretador_assembly.get_operator(origem)

        # Calcular
        resultado = valor_destino / valor_origem
        interpretador_assembly.set_operator(resultado, destino)


class JUMP(Mnemonico):
    """
    Classe do mnemonico MULT
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "variavel_destino",
                "tipos_permitidos": ["registrador", "label"]
            },
            {
                "nome": "variavel_origem",
                "tipos_permitidos": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):
        """
        Adiciona um número ao registrador
        A soma será destino + origem

        Parâmetros
        ---
        ``variavel_destino`` (registrador ou label):
            O local onde o resultado da adição é salvo

        ``variavel_origem`` (registrador, label, literal):
            Um dos valores a ser somado
        """

        # Ler parâmetros
        nome_label = params[0]

        # jump na linha da label
        interpretador_assembly.linha_codigo = \
            interpretador_assembly.labels[nome_label] - 1


class JTRUE(Mnemonico):
    """
    Jump to label or line number if CMP is true
    """

    def __init__(self):
        super().__init__()

        # parâmetros desse mnemônico
        self.parametros = [
            {
                "nome": "nome_label",
                "tipos_permitidos": ["label"]
            },
        ]

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):
        # Ler parâmetros
        nome_label = params

        # Executar
        cmp_deu_true = interpretador_assembly.registers['CP'] == 1

        if cmp_deu_true:
            interpretador_assembly.executar_mnemonico("JUMP", nome_label)


class JFALSE(Mnemonico):
    """
    Classe do mnemonico MULT
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "variavel_destino",
                "tipos_permitidos": ["registrador", "label"]
            },
            {
                "nome": "variavel_origem",
                "tipos_permitidos": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):
        # Ler parâmetros
        nome_label = params

        # valor_<alguma coisa> singifica o seguinte:
        # se for registrador, label, etc ele obtém o valor

        # Calcular
        if interpretador_assembly.registers['CP'] == 0:
            interpretador_assembly.executar_mnemonico("JUMP", nome_label)


class CMP(Mnemonico):
    """
    Verifica se o primeiro valor é igual ao segundo valor.
    O resultado é armazenado em CP.

    Retorna
    ---
    - Se o primeiro valor for igual: CP = 1
    - Se o primeiro valor for diferente: CP = 0
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "valor_1",
                "tipos_permitidos": ["registrador", "label", "literal"]
            },
            {
                "nome": "valor_2",
                "tipos_permitidos": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):
        # Ler parâmetros
        valor_1, valor_2 = params

        # valor_<alguma coisa> singifica que
        # se for registrador, label, etc ele obtém seu valor

        valor_1 = interpretador_assembly.get_operator(valor_1)
        valor_2 = interpretador_assembly.get_operator(valor_2)

        # se valor_1 for igual que valor_2 armazena no CP o valor 1(true)

        interpretador_assembly.registers['CP'] = int(valor_1 == valor_2)


class CMAIOR(Mnemonico):
    """
    Verifica se o primeiro valor é maior que o segundo valor.
    O resultado é armazenado em CP.

    Retorna
    ---
    - Se o primeiro valor for maior: CP = 1
    - Se o primeiro valor for menor: CP = 0
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "valor_1",
                "valorr_1": ["registrador", "label", "literal"]
            },
            {
                "nome": "valor_2",
                "valorr_2": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):
        # Ler parâmetros
        valor_1, valor_2 = params

        # valor_<alguma coisa> singifica que
        # se for registrador, label, etc ele obtém seu valor

        valor_1 = interpretador_assembly.get_operator(valor_1)
        valor_2 = interpretador_assembly.get_operator(valor_2)

        # se valor_1 for maior que valor_2 armazena no CP o valor 1(true)

        interpretador_assembly.registers['CP'] = int(valor_1 > valor_2)


class CMENOR(Mnemonico):
    """
    Verifica se o primeiro valor é menor que o segundo valor.
    O resultado é armazenado em CP.

    Retorna
    ---
    - Se o primeiro valor for menor: CP = 1
    - Se o primeiro valor for maior: CP = 0
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "valor_1",
                "tipos_permitidos": ["registrador", "label", "literal"]
            },
            {
                "nome": "valor_2",
                "tipos_permitidos": ["registrador", "label", "literal"]
            }
        ]

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):
        # Ler parâmetros
        valor_1, valor_2 = params

        # valor_<alguma coisa> singifica que
        # se for registrador, label, etc ele obtém seu valor

        valor_1 = interpretador_assembly.get_operator(valor_1)
        valor_2 = interpretador_assembly.get_operator(valor_2)

        # se valor_1 for menor que valor_2 armazena no CP o valor 1(true)

        interpretador_assembly.registers['CP'] = int(valor_1 < valor_2)


class VAR(Mnemonico):
    """
    Associa um endereço de memória a uma label.
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "label",
                "tipos_permitidos": ["label"]
            },
            {
                "nome": "endereco",
                "tipos_permitidos": ["endereco"]
            }
        ]

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):
        # Ler parâmetros
        label, endereco = params

        # Executar
        interpretador_assembly.labels[label] = int(endereco)

class INT(Mnemonico):
    """
    Lê o primeiro parâmetro de ``comando``
    - Se ``comando`` = 1, lê e salva caractere ASCII no endereço de memória
    - Se ``comando`` = 2, imprime caractere ASCII do endereço de memória
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = [
            {
                "nome": "comando",
                "tipos_permitidos": ["literal"]
            },
            {
                "nome": "endereco",
                "tipos_permitidos": ["endereco"]
            }
        ]

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):

        # Ler parâmetros
        comando, endereco = params

        # Executar
        if not endereco.isnumeric():
            return
        
        # Lê caractede ASCII da entrada de texto e salva no endereço de memória
        if comando == "1":
            interpretador_assembly.memory[int(endereco)] = ord(input()[0])

        # Imprime caractere ASCII do endereço de memória
        if comando == "2":
            print(chr(int(interpretador_assembly.memory[int(endereco)])))


class HALT(Mnemonico):
    """
    Para de executar o código.
    """

    def __init__(self):
        super().__init__()

        # parâmetros do mnemônico
        self.parametros = []  # nenhum

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):
        pass


_="""
    @_mnemonic(param_type=[["reg", "label"], ["reg", "label", "literal"]])
    def subt(self, destino, src):
        "Subtract number to register"
        self.set_operator(self.get_operator(destino) - self.get_operator(src), destino)

    @_mnemonic(param_type=[["reg", "label"], ["reg", "label", "literal"]])
    def mult(self, destino, src):
        "Multiply number to register"
        self.set_operator(self.get_operator(destino) * self.get_operator(src), destino)

    @_mnemonic(param_type=[["reg", "label"], ["reg", "label", "literal"]])
    def div(self, destino, src):
        "Divide number to register. "
        self.set_operator(self.get_operator(destino) / self.get_operator(src), destino)

    @_mnemonic(param_type=[["literal", "label"]])
    def jump(self, destino:str):
        "Jump to label or line number"
        if destino.isnumeric():
            self.pc = int(destino) - 1
        else:
            self.pc = self.labels[destino] - 1

    @_mnemonic(param_type=[["literal", "label"]])
    def jtrue(self, destino):
        "Jump to label or line number if CMP is true"
        if self.registers['CP'] == 1:
            self.jump(destino)

    @_mnemonic(param_type=[["literal", "label"]])
    def jfalse(self, destino):
        "Jump to label or line number if CMP is false"
        if self.registers['CP'] == 0:
            self.jump(destino)

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
"""