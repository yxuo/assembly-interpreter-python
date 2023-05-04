-- CODIGO 1 - FUNCIONA
--      VAR     teste, 3
--      MOVE    teste, 10
--      INT     1, 4
--      INT     2, 4
--      MOVE    A, 6        -- Coloco o valor 6 no registrador A
--      MOVE    B, 5        -- Coloco o valor 5 no registrador A
--  enquanto:   MOVE  C, B  -- Coloco no registrador C o valor presente no registrador B
--      CMP     B, 1        -- Comparo o valor presente em B com o valor 1. O resultado fica no registrador CR
--      JTRUE   fim         -- Se CR tiver o valor 1, então JUMP para a linha com o label fim
--      MOVE    B, C        -- Coloco em B o valor presente em C
--      MULT    A, B        -- Multiplico o valor presente em A com o valor presente em B. O resultado ficará em A
--      SUBT    B, 1        -- Subtraio 1 no o valor presente em B
--      JUMP    enquanto    -- JUMP para linha com o label enquanto.
--  fim:        HALT

-- CODIGO DO TESTE - FUNCIONA
            VAR    valor, 0                     -- OK           
            INT 1, valor                        -- valor = 51   
             CMENOR valor, 48 -- caracter '0'   -- 0            
             JTRUE  erro                        -- pass         
             CMAIOR valor, 57 -- caracter '9'   -- 0            
             JTRUE  erro                        -- pass         
             SUBT   valor, 48                   -- 3            
             MOVE   A, valor                    -- OK
 enquanto:    CMENOR valor, 2                   -- 0    0   1
                       JTRUE  fim               -- pass pass OK
                        SUBT   valor, 1         -- 2    1
             MULT   A, valor                    -- A=6  A=6
                       JUMP   enquanto          -- .    .
 fim:
            MOVE    valor, A
 ADD    valor, 32
             INT 2, valor            
                       HALT                        
 erro:              MOVE   valor, 69 -- 'E'
                       INT    2, valor    
             MOVE   valor, 82 -- 'R'            
             INT    2, valor    
             INT    2, valor
             MOVE   valor, 79 -- 'O'
             INT    2, valor
             HALT