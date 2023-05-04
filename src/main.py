import os
import sys
from interpretador_assembly.interpretador_assembly import InterpretadorAssembly

if __name__ == "__main__":

    # Ler arquivo
    DIRETORIO_SCRIPT = os.path.dirname(__file__)

    # Se usuário inseriu diretório do arquivo assembly como argumento, lê
    if len(sys.argv) > 1:
        DIRETORIO_ARQUIVO_ASSEMBLY = sys.argv[1]

    # Senão, lê <pasta do arquivo main.py>/assembly-sample.asm
    else:
        DIRETORIO_ARQUIVO_ASSEMBLY = os.path.join(DIRETORIO_SCRIPT, "assembly-sample.asm")

    # Abre arquivo
    MY_CODE = open(DIRETORIO_ARQUIVO_ASSEMBLY, "r", encoding="utf-8").read()

    # Executar
    assembler = InterpretadorAssembly()
    assembler.executar_validacao(MY_CODE)
    assembler.carregar_codigo(MY_CODE)
    assembler.executar_codigo()

    print("---")
    print("Conteúdo do interpretador:")
    print(assembler)
