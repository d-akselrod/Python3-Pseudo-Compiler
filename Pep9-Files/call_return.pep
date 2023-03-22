         BR      program
_UNIV:   .EQUATE 42
x:       .BLOCK  2
result:  .EQUATE 0 ; local variable #2d
result1: .BLOCK  2
value:   .EQUATE 4 ; local variable #2d
retVal:  .EQUATE 6 ; return value #2d

my_func: SUBSP   2,i ; push #result
         LDWA    value,s
         ADDA    _UNIV,i
         STWA    result,s 
         LDWA    result,s
         STWA    retVal,s
         ADDSP   2,i ;pop #result
         RET

program: SUBSP  4,i ;push #retVal #value
         DECI   x,d
         LDWA   x,d
         STWA   0,s
         CALL   my_func
         ADDSP  2,i ; pop #value
         LDWA   0,s
         STWA   result1,d
         ADDSP  2,i ; pop #retVal
         DECO   result1,d 
         .END
         