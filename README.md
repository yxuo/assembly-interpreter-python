# Trabalho - Leitor assembly

## TDE #01 - Criação de um Interpretador Assembly
Alessandro de Almeida Castro Cerqueira - 
> 7 de mar. Editado às 18:33
100 pontos
>
> Data de entrega: 25 de abr.

Este instrumento de avaliação poderá ser feito trios e corresponde a 40% da nota da 1a avaliação e poderá ser feito por grupos de até 3 pessoas.

O trabalho consiste em criar um interpretador de código Assembly Simplificado. Vamos considerar que o processador hipotético tenha 8 Registradores chamados A, B, C, D, E, F, G e H que armazenam um inteiro (32 bits) cada um. Além desses, há o registrador PC (Program Counter) que contém o número da linha em execução e o registrador CR (Compare Result) que armazena um valor booleano referente à última instrução de comparação realizada. Além dos registradores, o interpretador considerará a existência de uma área de memória de 1024 bytes que pode ser livremente utilizada no programa. Todos os mnemônicos utilizados no programa estão escritos em letras maiúsculas e a relação dos mnemônicos está no final.

O Formato das instruções seguirá o seguinte padrão:
```
    [<label>:]   <MNEMÔNICO>  [<PARAM1>,<PARAM2>]     [-- comentário]
```

O que está em '`[ ]` não é obrigatório. O <label> associa um rótulo à linha em questão e pode ser utilizado nos mnemônicos de JUMP. Para ser um <label>, é necessário que esteja no início da linha e com ':' colado ao final de seu nome. Cada mnemônico pode ter 0, 1 ou 2 parâmetros e se houver '--' no final da linha, é a indicação de um comentário a ser ignorado pelo interpretador. Cada linha só pode ter a presença de um mnemônico.

Para não ser necessário a leitura de arquivos, o código a ser interpretado pode ser colocado em um array de strings e a execução começa pela primeira string do array. Esse trabalho pode ser feito em qualquer linguagem de programação.

### LISTA DOS MNEMÔNICOS

MOVE <Registrador ou Endereço de Memória ou Label> , <Registrador ou Endereço de Memória ou Label  ou Literal> - Atribui ao <Registrador 1> o valor presente em <Registrador 2> ou o valor de uma literal.
Ex:
    MOVE A, -29         -- Atribui em A o valor -29
    MOVE B, A            -- Atribui em B o valor presente em A
    MOVE 200, A        -- Move para a posição de memória 200 o valor presente em A
    MOVE VAR_A, B    -- Move para a posição de memória referenciada por VAR_A o valor presente em B
----------------------------------
ADD <Registrador 1> , <Registrador 2 ou Literal> - Soma o valor presente em <Registrador 1> com o valor <Registrador 2> ou o valor de uma literal. O resultado ficará em <Registrador 1>
Ex:
    ADD D,1  -- Incrementa o valor de D
    ADD B,D  -- Soma o valor de B com o valor de D, armazenando o resultado em B
     
Semelhante a ADD, teremos SUBT <subtração>, MULT <multiplicação> e DIV <divisão>

----------------------------------
CMP <Registrador 1>,<Registrador 2 ou Literal> - Compara o valor presente em <Registrador 1> com valor presente em <Registrador 2> ou o valor de uma literal. Se iguais, o registrador CR recebe o valor 1; senão CR recebe 0

----------------------------------
CMAIOR <Registrador 1>,<Registrador 2 ou Literal> - Compara o valor presente em <Registrador 1> é maior que o valor presente em <Registrador 2> ou o valor de uma literal. Se iguais, o registrador CR recebe o valor 1; senão CR recebe 0

----------------------------------
CMENOR <Registrador 1>,<Registrador 2 ou Literal> - Compara o valor presente em <Registrador 1> é menor que o valor presente em <Registrador 2> ou o valor de uma literal. Se iguais, o registrador CR recebe o valor 1; senão CR recebe 0

----------------------------------
JUMP <label> - Redireciona a executação para a linha indicada por <label>

----------------------------------
JTRUE  <label> - Redireciona a executação para a linha indicada por <label> se CR tiver um valor diferente de 0

----------------------------------
JFALSE <label> - Redireciona a executação para a linha indicada por <label> se CR tiver um valor igual a 0

----------------------------------
INT 1, <Endereço de Memória ou Label> - interrupção tipo 1 que lê uma tecla e coloca o seu valor ASCII na posição de memória indicada

INT 2, <Endereço de Memória ou Label> - interrupção tipo 2 que escreve o valor ASCII da posição de memória indicada

----------------------------------
HALT - Para a execução do programa

----------------------------------
VAR  <Label>, <Endereço de Memória> - Pseudo instrução que associa uma posição de memória a um label. Esse poderá ser usado pelas instruções como local para armazenamento ou leitura de valores.

Exemplo de Código - Cálculo do fatorial de 6.

                   MOVE  A, 6   -- Coloco o valor 6 no registrador A
                   MOVE  B, 5   -- Coloco o valor 5 no registrador A
enquanto:  MOVE  C, B  -- Coloco no registrador C o valor presente no registrador B
                   CMP   B, 1    --  Comparo o valor presente em B com o valor 1. O resultado fica no registrador CR
                   JTRUE fim   -- Se CR tiver o valor 1, então JUMP para a linha com o label fim
                   MOVE B, C   -- Coloco em B o valor presente em C
                   MULT A, B   -- Multiplico o valor presente em A com o valor presente em B. O resultado ficará em A
                   SUBT B, 1    -- Subtraio 1 no o valor presente em B 
                  JUMP enquanto -- JUMP para linha com o label enquanto.
fim:            HALT

---

* CMP B 1 -- CR=1
* O interpretador deve identificar a linha em que o label foi criado.
* Label é um rótulo, um _mecanismo_, que será uma REFERÊNCIA a uma linha.
  Exemplo:
  ```
  1  | LABEL hello
  2  | print "hi"
  3  | goto hello
  ```
  Ao invés de:
  ```
  1  | 
  2  | print "hi"
  3  | goto 1
  ```

  Assembly é uma linguagem que faz uma associação de uma linguagem de mãquina para texto.
  Quando a pessoa fazia u programa em Assembly, ele precisava saber a linha para saltar no código.

Dica do prof:
* Se pensar de pouquinho em pouquinho e avançar um pouco...
* Leia o programa, faça análise léxica dos dados