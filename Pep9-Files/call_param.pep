         BR      program
_UNIV:   .EQUATE 42
x:       .BLOCK  2
result:  .EQUATE 0 ;local variable #2d
value:   .EQUATE 4 ; local variable #2d

my_func: SUBSP   2,i ; push #result
         LDWA    value,s
         ADDA    _UNIV,i
         STWA    result,s 
         DECO    result,s 
         ADDSP   2,i ;pop #result
         RET

program: SUBSP  2,i ;push #value
         DECI   x,d
         LDWA   x,d
         STWA   0,s
         CALL   my_func
         ADDSP  2,i ; pop #value
         .END