         BR      program
x:       .BLOCK  2
program: LDWA    3,i
         ADDA    2,i
         STWA    x,d 
         DECO    x,d 
         LDBA    '\n',i
         STBA    charOut,d
         .END