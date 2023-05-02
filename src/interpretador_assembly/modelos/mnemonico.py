"""
Arquivo para a classe abstrata Mnemonico

Como funciona
---
1. O interpretador vai asnalisar a pasta mnemonicos
2. Cada mnemonico que o interpretador encontrar ele adiciona na lista de mnemonicos

E para que serve essa classe abstrata nesse conexto?
- A classe abstrata mnemonico vai padronizar quais métodos \
    e atributos todos os mnemônicos devem ter.

Como usar
---
Vá na pasta mnemonicos e crie um arquivo com o nome do seu mnemônico.
Exemplo:
add.py
```python
from mnemonico improt Mnemonico 
a=1
```
"""

from abc import ABC, abstractmethod

class Mnemonico(ABC):
    "Classe abstrata de mnemônico."

    def __init__(self):
        """
        Métodos:
        ---
        tipo_parametro (list):
            Para cada parâmetro posicional da função `executar()`,  
            defina o nome e os tipos permitidos

            Exemplo:
            ```
                >>> parametros=[
                    {
                        "nome": "parametro_1",
                        "tipos_permitidos": ["registrador", "label"]
                    },
                    {
                        "nome": "parametro_1",
                        "tipos_permitidos": ["literal"]
                    },
                ]
            ```
            - Tipos permitidos: registrador, label, literal
        """

        self.parametros = dict()

    @abstractmethod
    def executar(self, interpretador_assembly, params:list):
        """
        Método principal para executar o mnemônico
        """
