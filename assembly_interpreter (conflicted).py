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
    "CMP": lambda x, y: variables.update({"CR": variables[x] == int(y)}),
    "MULT": lambda x, y: variables.update({x: variables[x] * variables[y]}),
}

def interpret(INPUT):
    lines = INPUT.split('\n')
    labels = {}
    line_index = 0

    while line_index < len(lines):
        line_splitted = lines[line_index].split("--")[0].split()
        continue
        if not line_splitted:
            line_index += 1
            continue
        # print(labels)
        if line_splitted[0][:-1] in labels.keys():
            print("Label called here:")
            line_index += 1
            continue
        if line_splitted[0].endswith(":"):
            labels[line_splitted[0][:-1]] = l
            line_splitted = line_splitted[1:]
            print(labels)
        instruction = line_splitted[0]
        print("MN", instruction)
        result = MNEMONICS[instruction](*line_splitted[1:])
        # if result is False:
        #     return False
        line_index += 1

    return variables

result = interpret(INPUT)
print(result)
