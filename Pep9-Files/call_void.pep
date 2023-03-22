         BR      program
_UNIV:   .EQUATE 42 ;global variable
value:   .EQUATE 2  ;local variable, #2d
result:  .EQUATE 0  ;local variable, #2d

my_func: SUBSP   4,i ;push #value, #result 
         DECI    value,s
         LDWA    value,s
         ADDA    _UNIV,i
         STWA    result,s 
         DECO    result,s 
         ADDSP   4,i ;pop #value, #result 
         RET
         
program: CALL    my_func 
         .END