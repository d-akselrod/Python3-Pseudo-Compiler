         BR      program 
a:       .BLOCK  2
b:       .BLOCK  2
program: DECI    a,d
         DECI    b,d
test_1:  LDWA    a,d
         CPWA    b,d
         BREQ    end_l_1
         LDWA    a,d
         CPWA    b,d
         BRLE    else

if:      SUBA    b,d
         STWA    a,d
         BR      end_if

else:    LDWA    b,d
         SUBA    a,d
         STWA    b,d
         BR      end_if

end_if:  BR      test_1
end_l_1:  DECO    a,d
         .END