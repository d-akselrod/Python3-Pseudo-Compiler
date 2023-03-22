         BR      program
_UNIV:   .EQUATE 42
variable:.WORD   3
value:   .BLOCK  2
result:  .BLOCK  2

program: DECI    value,d
         LDWA    value,d
         ADDA    _UNIV,i
         STWA    result,d
         SUBA    variable,d
         STWA    result,d
         SUBA    1,i
         STWA    result,d 
         DECO    result,d 
         LDBA    '\n',i
         STBA    charOut,d 
         .END