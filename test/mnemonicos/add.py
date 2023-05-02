"""Arquivo para classe do mnemonico ADD"""

from interpretador_assembly.modelos.mnemonico import Mnemonico

class ADD(Mnemonico):
    """
    Classe do mnemonico ADD
    """

    def __init__(self):
        super().__init__()
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

    def executar(self, interpretador_assembler, params:list):
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

        valor_destino = interpretador_assembler.get_operator(destino)
        valor_origem = interpretador_assembler.get_operator(origem)

        # Calcular
        resultado = valor_destino + valor_origem
        interpretador_assembler.set_operator(resultado, destino)
