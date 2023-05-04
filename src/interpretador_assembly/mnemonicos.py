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

        # Executar
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
                "tipos_permitidos": ["registrador", "endereco", "variavel"]
            },
            {
                "nome": "valor_2",
                "tipos_permitidos": ["registrador", "variavel", "literal"]
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
                "tipos_permitidos": ["registrador", "endereco", "variavel"]
            },
            {
                "nome": "valor_2",
                "tipos_permitidos": ["registrador", "variavel", "literal"]
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
                "tipos_permitidos": ["registrador", "endereco", "variavel"]
            },
            {
                "nome": "valor_2",
                "tipos_permitidos": ["registrador", "variavel", "literal"]
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
                "tipos_permitidos": ["nome_variavel"]
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
                "tipos_permitidos": ["endereco", "variavel"]
            }
        ]

    def executar(self, interpretador_assembly:InterpretadorAssembly, params:list):
        # Ler parâmetros
        comando, endereco = params

        # Se for variável, label e afins, ele lê
        valor_endereco = int(interpretador_assembly.get_operator(endereco))

        # Executar

        # Lê caractede ASCII da entrada de texto e salva no endereço de memória
        if comando == "1":
            interpretador_assembly.memory[valor_endereco] = ord(input()[0])

        # Imprime caractere ASCII do endereço de memória
        if comando == "2":
            if interpretador_assembly.token_e_endereco(endereco):
                valor_endereco = int(interpretador_assembly.get_memory(int(endereco)))
            print(chr(valor_endereco))


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
