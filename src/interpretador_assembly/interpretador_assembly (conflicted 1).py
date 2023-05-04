"""
Este interpretador emula um processador hipotético.

Requisitos
    - CR armazena comparação
    - O interpretador deve avisar erro léxico, sintático ou semântico

Fonte:
    - https://www.javatpoint.com/lexical-error      - O que é erro léxico
    - https://www.javatpoint.com/syntax-error       - O que é erro sintático
    - https://www.javatpoint.com/semantic-error     - O que é erro semântico

Importando mnemônicos
---
O interpretador vai fazer injeção de dependência, procurando na pasta mnemonicos\
    por arquivos .py para cada mnemônico.

"""

from typing import Dict
import re
import importlib
import importlib.resources
from interpretador_assembly.erros.lexical_error import LexicalError
from interpretador_assembly.modelos.mnemonico import Mnemonico

class InterpretadorAssembly:
    """
    Essa classe vai interpretar o código assembly
    """

    def __str__(self) -> str:
        """
        Quando você der print() da classe InterpretadorAssembly,\
            ele vai exibir o string formatado aqui.
        """
        return f"""\
Memória[{len(self.memory)}]:\t{self.memory}
Mnemônicos:\t{self.mnemonicos.keys()}
Instruções:\t{self.instrucoes}
Registradores:\t{self.registers}
linha_codigo:\t{self.linha_codigo}
Variáveis:\t\t{self.labels}\
Labels:\t\t{self.labels}\
        """

    MENSAGENS_ERRO_LEXICO = {
        "invalid_token": lambda l,n,t: f"'{t}' is not a valid token, at line {n}\n{l}",
    }
    MENSAGENS_ERRO_SINTATICO = {
        "invalid_mnemonic": lambda l,n,t: f"'{t}' is not a valid mnemonic, at line {n}\n{l}",
        "invalid_type": lambda l,n,t: f"'{t}' doesn't have a valid type, at line {n}\n{l}",
        "expected_token": lambda l,n,t: f"expected token after '{t}' at line {n}\n{l}",
        "operator_not_found": lambda l,n,t: f"operator name not found '{t}' at line {n}\n{l}",
        "duplicated_token": lambda l,n,t: \
            f"token '{t}' duplicated at line {n}\n{l}",
        "expected_closing": lambda l,n,t: \
            f"expected closing '{t}' at line {n}\n{l}",
        "expected_operator": lambda l,n,t: f"expected operator after '{t}' at line {n}\n{l}",
    }

    def __init__(self):
        self.registers = {
            'CP': 0         # CP = "ComPare"
            }
        self.labels = {}
        self.variaveis = {}
        self.memory = [0] * 255 + [1.2]
        self.linha_codigo = 0
        self.instrucoes = []
        self.mnemonicos:Dict[str, Mnemonico] = dict()
        self.injetar_mnemonicos()

    def carregar_codigo(self, code):
        """
        Para cada linha no código, carrega uma linha tratada, \
            ou seja, sem espaços antes e depois, e sem comentários.

        Isso permite com que o código tratado seja reaproveitado \
            tanto para validar quanto para executar.
        
        A linha tratada é salva em ``instrucoes``.
        
        Exemplo de linha tratada:
        ---
            Antes:
        ```assembly
            ADD         A, 1            -- adiciona 1 a A
            label1: SUB         B, 2    -- subtrai 2 a A
        ```

            Depois:
        ```python
        self.instrucoes = [
            'ADD         A, 1',  # linha 1
            'SUB         B, 2',  # linha 2
        ]
        self.label = {
            "label1": 2
        }
        ```
        """
        for _, linha in enumerate(code.split('\n')):

            linha_tratada = linha.split("--")[0].strip()

            # se linha tratada estiver vazia, pula para a próxima linha
            if not linha_tratada:
                continue

            # Se a linha tiver ':', ela possui label
            if ':' in linha_tratada:
                # separa a label do resto da linha tratada
                label, linha_tratada = linha_tratada.split(':', 1)
                label = label.strip()  # remove espaço em branco da label

                # len(instrucoes) nesse contexto é sempre a linha atual do label
                self.labels[label] = len(self.instrucoes)

            # Adiciona linha tratada nas instruções
            self.instrucoes.append(linha_tratada)

    def executar_validacao(self, code):
        "Load instructions to compiler"
        self.instrucoes = []
        self.labels = {}
        for i, line in enumerate(code.split('\n')):
            line_1 = line.split("--")[0].strip()
            if not line_1:
                continue

            self.analisar_erro_lexico(line, i)
            self.analisar_erro_sintatico(line, i)

    def executar_codigo(self):
        """
        Executa o código
        
        1. Transformar isntrução em lista de tokens

        Antes:
        ```
        "MOV      A, 1"
        ```

        Depois:
        ```
        ["MOV","A", "1"]
        ```
        
        Por que não transformar instruções em lista de uma vez só?
        - Para poder fazer a validação do código em texto
        """
        # Percorre pela lista de instruções assembly
        while self.linha_codigo < len(self.instrucoes):

            # obtém instrução assembly na respectiva linha
            instrucao = self.instrucoes[self.linha_codigo]

            # se não tiver mais instruções, vai para próxima linha
            if not instrucao:
                self.linha_codigo += 1
                continue

            # 1. Transformar instrução em lista de tokens
            # token_1 pode ser label ou um mnemônico
            # *parametros será a lista de parâmetros: [parametro_1, param_2, ...]
            token_1, *parametros = instrucao.split()

            # Se token_1 for mnemônico HALT, para de executar o código
            if token_1 == "HALT":
                return

            # Se token_1 for um mnemônico que existe na lista de mnemônicos, executa
            if token_1 in self.mnemonicos:
                nome_mnemonico = token_1

                # Tira vírgula dos parâmetros
                parametros = [i.strip(',') for i in parametros]

                self.executar_mnemonico(nome_mnemonico, parametros)

            self.linha_codigo += 1

    def analisar_erro_lexico(self, line:str, numero_linha):
        "Check for lexical errors in a given line of assembly code"

        # Check for invalid characters
        line = line.strip()
        line_1 = line.split("--")[0].split()
        if not line_1:
            return

        # For each token, lexic check
        for token in line_1:
            self.validate_token_lexic(token, numero_linha, line)

    def validate_token_lexic(self, token:str, line_number, line:str):
        "Validate token name"
        if token[-1] == ',':
            token = token[:-1]
        if token[-1] == ':':
            token = token[:-1]
        if token[0].isnumeric() and not token.isnumeric():
            raise LexicalError(self.MENSAGENS_ERRO_LEXICO["invalid_token"](
                line, line_number, token))
        for char in token:
            if not (char.isalnum() or char in "_\""):
                raise LexicalError(self.MENSAGENS_ERRO_LEXICO["invalid_token"](line, line_number, char))

    def treat_line(self, line:str):
        "Treat assembly line and return teated line and a list of tokens"
        line_treated = line.strip()  # Ignore spaces
        line_treated = line_treated.split("--")[0]  # Ignore comment
        line_treated = re.sub(r'"[^"]*"', '""', line_treated)
        return line_treated

    def analisar_erro_sintatico(self, line:str, line_index):
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

        # Erro de aspas duplas a mais
        if line_treated.count('"') % 2:  # if number of " is odd
            raise SyntaxError(self.MENSAGENS_ERRO_SINTATICO[
                "expected_closing"](line, line_index, '"'))

        # Label com mais de um ':'
        if line_treated.count(':') > 1:
            raise SyntaxError(self.MENSAGENS_ERRO_SINTATICO[
                "duplicated_token"](line, line_index, ':'))

        # label ou mnemonic
        operator_index = 0

        def lista_tokens_terminou():
            return operator_index >= len(tokens)

        if lista_tokens_terminou():
            return

        # se for label, pula
        if self.token_e_label(tokens[operator_index]):
            operator_index += 1

        if lista_tokens_terminou():
            return

        # se for mnemônico, pula
        mnemonico = tokens[operator_index]
        if self.token_e_mnemonico(tokens[operator_index]):
            operator_index += 1

        # Senão, verifica parâmetros
        else:
            raise SyntaxError(self.MENSAGENS_ERRO_SINTATICO["invalid_mnemonic"](
                line, line_index, tokens[operator_index]))

        if lista_tokens_terminou():
            return

        # Verifica erros em parâmetros
        operators = tokens[operator_index:]
        if operators:
            commas = ''.join(operators).count(',')

            # Erro: vírgula esperada
            if commas < len(operators)-1:
                raise SyntaxError(self.MENSAGENS_ERRO_SINTATICO[
                    "expected_operator"](line, line_index, ','))

            # Erro: token esperado
            if commas > len(operators)-1:
                raise SyntaxError(self.MENSAGENS_ERRO_SINTATICO[
                    "expected_token"](line, line_index, ','))

            # Erro: tipo de parâmetro incorreto
            if self.mnemonicos[mnemonico].parametros:
                for i, operator in enumerate(operators):
                    tipos_permitidos = self.mnemonicos[mnemonico].parametros[i]["tipos_permitidos"]
                    tipos_token = self.get_tipo_token(operator)

                    # se não tiver nenhum token em tipos permitidos, erro
                    if not any([tipo_token not in tipos_permitidos \
                        for tipo_token in tipos_token]):
                        raise SyntaxError(self.MENSAGENS_ERRO_SINTATICO[
                            "invalid_type"](line, line_index, operator))


    def token_e_endereco(self, operator):
        "Se token é endereço de memória válido"
        return operator.isnumeric() and int(operator) >= 0 and int(operator) < len(self.registers)

    def token_e_variavel(self, operator):
        "Se token é variável"
        return operator in self.variaveis

    def token_e_registrador(self, operator):
        "Se token é registrador"
        return operator in self.registers

    def token_e_label(self, operator):
        "Se token é label"
        return str(operator).endswith(':') or operator in self.labels

    def token_e_literal(self, operator):
        "Se token é literal ('abc' ou 123)"
        return not self.token_e_registrador(operator) and not self.token_e_label(operator)

    def token_e_mnemonico(self, operator):
        "Se token é mnemonico"
        return operator in self.mnemonicos

    def get_tipo_token(self, token) -> str:
        """
        Dado um token, retorna seu tipo como string
        """
        tipos_encontrados = []
        if self.token_e_label(token):
            return "label"
        elif self.token_e_literal(token):
            return "literal"
        elif self.token_e_mnemonico(token):
            return "mnemonico"
        elif self.token_e_registrador(token):
            return "registrador"
        else:
            return "INVALIDO"

    def get_operator(self, operator):
        "Get operator value based on register or pointer"
        # register
        if self.token_e_registrador(operator):
            return self.registers[operator]
        # memory
        elif self.token_e_label(operator):
            return self.memory[self.labels[operator]]
        # value
        else:
            if operator.isnumeric():
                astype = int
                if  '.' in operator:
                    astype = float
                return astype(operator)
            return operator

    def set_operator(self, operator_value, destino:str):
        "Set operator value based on register or label"
        if destino in self.labels:
            label = self.labels[destino]
            self.memory[label] = operator_value
        else:
            self.registers[destino] = operator_value

    def injetar_mnemonicos(self):
        """
        Para injeção de dependência.

        Este método vai procurar no arquivo 'mnemonicos.py' \
            por classes do tipo Mnemonico

        Exemplo de arquivo a ser lido
        ---
        ``interepretador_assembly/mnemonicos.py``:
        ```python
        from interpretador_assembly.models.mnemonico import Mnemonico

        class ADD(Mnemonico):
            ...


        class SUBT(Mnemonico):
            ...
        ```
        """

        # Definir em qual pacote vai procurar na biblioteca
        #   interpretador_assembly.mnemonicos
        modulo_interpretador_assembly = "interpretador_assembly"
        modulo_mnemonicos = f"{modulo_interpretador_assembly}.mnemonicos"


        # importa os mnemônicos do arquivo mnemonicos.py
        modulo_arquivo = importlib.import_module(modulo_mnemonicos)

        # Para cada dado dentro de 'mnemonicos.py',
        # adiciona cada mnemônico à lista de mnemônicos
        for dado in dir(modulo_arquivo):
            obj = getattr(modulo_arquivo, dado)
            if isinstance(obj, type) and issubclass(obj, Mnemonico) and obj is not Mnemonico:
                nome_mnemonico = obj.__name__
                self.mnemonicos[nome_mnemonico] = obj()


    def executar_mnemonico(self, nome_mnemonico:str, parametros: list[str]):
        """
        Executa mnemônico baseado no nome

        Exemplo:
        ADD, SUBT
        """
        self.mnemonicos[nome_mnemonico].executar(self, parametros)
