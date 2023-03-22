
class StaticMemoryAllocation():

    def __init__(self, global_vars: dict()) -> None:
        self.__global_vars = global_vars

    def generate(self):
        print('; Allocating Global (static) memory')
        for key in self.__global_vars.keys():
            val = self.__global_vars[key]
            if key[0] == "_" and key[1:].isupper():
                print(f'{str(key+":"):<9}\t.EQUATE {val}') # Constants
            elif val is None:
                print(f'{str(key+":"):<9}\t.BLOCK 2') # reserving memory
            else:
                print(f'{str(key+":"):<9}\t.WORD {val}') # Memory Allocation