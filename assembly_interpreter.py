"""
Este interpretador emula um processador hipotético.

Requisitos
    - CR armazena comparação
    - O interpretador deve avisar erro léxico, sintático ou semântico
"""

INPUT = """
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

variables = {

}

MNEMONICS = {
    "MOVE": lambda x, y: variables.update({x: y}),
    "CMP": lambda x, y: False if variables[x] != int(y) else None,
    "MULT": lambda x, y: variables.update({x: variables[x] * variables[y]})
}

def interpret(INPUT):
    lines = INPUT.split('\n')
    labels = {}
    for l, line in enumerate(lines):
        parts = line.split("--")[0].split()
        if not parts:
            continue
        # print(labels)
        if parts[0][:-1] in labels.keys():
            print("Label called here:")
            continue
        if parts[0].endswith(":"):
            labels[parts[0][:-1]] = l
            parts = parts[1:]
            print(labels)
        instruction = parts[0]
        result = MNEMONICS[instruction](*parts[1:])
        # if result is False:
        #     return False
    return variables

result = interpret(INPUT)
print(result)
