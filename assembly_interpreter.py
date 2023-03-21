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
    'CR': -1

}


labels = {}


MNEMONICS = {
    "MOVE": lambda x, y: variables.update({x: y}),
    "CMP": lambda x, y: variables.update({"CR": variables[x] == int(y)}),
    "MULT": lambda x, y: variables.update({x: variables[x] * variables[y]}),
    "SUBT": lambda x, y: variables.update({x: variables[x] - variables[y]}),
    "JUMP": lambda x: labels[x] if labels.get(x) else -1,
    "JTRUE": lambda x: labels[x] if variables['CR'] == 1 else -1,
    "JFALSE": lambda x: labels[x] if variables['CR'] != 1 else -1,
}

def interpret(INPUT):
    lines = INPUT.split('\n')
    line_index = 0

    # map labels
    for l, line in enumerate(lines):
        line_splitted = line.replace(",", "").split("--")[0].split()
        if not line_splitted:
            line_index += 1
            continue
        if line_splitted[0].endswith(":"):
            labels[line_splitted[0][:-1]] = l
            line_splitted = line_splitted[1:]

    # run code
    while line_index < len(lines):
        line_splitted = lines[line_index].replace(",", "").split("--")[0].split()
        if not line_splitted:
            line_index += 1
            continue
        if line_splitted[0].endswith(":"):
            if len(line_splitted) == 1:
                line_index += 1
                continue
            line_splitted = line_splitted[1:]

        # Call instruction
        instruction = line_splitted[0]
        print("INST:", instruction)

        # jump
        if instruction in ["JUMP", "JTRUE", "JFALSE"]:
            print("jump", line_index, labels[line_splitted[1]])
            exit(0)
            line_index = labels[line_splitted[1]]
            continue

        # 
        result = MNEMONICS[instruction](*line_splitted[1:])
        # if result is False:
        #     return False
        line_index += 1

result = interpret(INPUT)
print(result)