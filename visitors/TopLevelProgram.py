import ast
from visitors.VarNameExtractor import SymbolTable

LabeledInstruction = tuple[str, str]

class TopLevelProgram(ast.NodeVisitor):
    """We supports assignments and input/print calls"""
    
    def __init__(self, entry_point) -> None:
        super().__init__()
        self.__instructions = list()
        self.__record_instruction('NOP1', label=entry_point)
        self.__should_save = True
        self.__current_variable = None
        self.__elem_id = 0
        self.__if_id = 0
        self.__assigned_vars = set()

        self.to_PEP9_name = SymbolTable.toPEP9Name

    def finalize(self):
        self.__instructions.append((None, '.END'))
        return self.__instructions

    ####
    ## Handling Assignments (variable = ...)
    ####

    def visit_Assign(self, node):
        # remembering the name of the target
        self.__current_variable = self.to_PEP9_name(node.targets[0].id)
        # visiting the left part, now knowing where to store the result
        if isinstance(node.value, ast.Constant) and self.__current_variable not in self.__assigned_vars:
            self.__assigned_vars.add(self.__current_variable)
            return
        self.visit(node.value)
        if self.__should_save:
            self.__record_instruction(f'STWA {self.__current_variable},d')
        else:
            self.__should_save = True
        self.__current_variable = None

    def visit_Constant(self, node):
        self.__record_instruction(f'LDWA {node.value},i')
    
    def visit_Name(self, node):
        self.__record_instruction(f'LDWA {self.to_PEP9_name(node.id)},d')

    def visit_BinOp(self, node):
        self.__access_memory(node.left, 'LDWA')
        if isinstance(node.op, ast.Add):
            self.__access_memory(node.right, 'ADDA')
        elif isinstance(node.op, ast.Sub):
            self.__access_memory(node.right, 'SUBA')
        else:
            raise ValueError(f'Unsupported binary operator: {node.op}')

    def visit_Call(self, node):
        match node.func.id:
            case 'int': 
                # Let's visit whatever is casted into an int
                self.visit(node.args[0])
            case 'input':
                # We are only supporting integers for now
                self.__record_instruction(f'DECI {self.__current_variable},d')
                self.__should_save = False # DECI already save the value in memory
            case 'print':
                # We are only supporting integers for now
                self.__record_instruction(f'DECO {node.args[0].id},d')
            case _:
                raise ValueError(f'Unsupported function call: { node.func.id}')

    ####
    ## Handling While loops (only variable OP variable)
    ####

    def visit_While(self, node):
        loop_id = self.__identifyLoop()
        inverted = {
            ast.Lt:  'BRGE', # '<'  in the code means we branch if '>=' 
            ast.LtE: 'BRGT', # '<=' in the code means we branch if '>' 
            ast.Gt:  'BRLE', # '>'  in the code means we branch if '<='
            ast.GtE: 'BRLT', # '>=' in the code means we branch if '<'
            ast.Eq:  'BRNE', # '==' in the code means we branch if '!='
            ast.NotEq: 'BREQ' # '!=' in the code means we branch if '=='
        }
        # left part can only be a variable
        self.__access_memory(node.test.left, 'LDWA', label = f'test_{loop_id}')
        # right part can only be a variable
        self.__access_memory(node.test.comparators[0], 'CPWA')
        # Branching is condition is not true (thus, inverted)
        self.__record_instruction(f'{inverted[type(node.test.ops[0])]} end_l_{loop_id}')
        # Visiting the body of the loop
        for contents in node.body:
            self.visit(contents)
        self.__record_instruction(f'BR test_{loop_id}')
        # Sentinel marker for the end of the loop
        self.__record_instruction(f'NOP1', label = f'end_l_{loop_id}')

    ####
    ## Handling Conditionals (only variable OP variable)
    ####

    def visit_If(self, node):
        if_id = self.__identifyif()
        

        inverted = {
            ast.Lt:  'BRGE', # '<'  in the code means we branch if '>=' 
            ast.LtE: 'BRGT', # '<=' in the code means we branch if '>' 
            ast.Gt:  'BRLE', # '>'  in the code means we branch if '<='
            ast.GtE: 'BRLT', # '>=' in the code means we branch if '<'
            ast.Eq:  'BRNE', # '==' in the code means we branch if '!='
            ast.NotEq: 'BREQ' # '!=' in the code means we branch if '=='
        }

        self.__access_memory(node.test.left, 'LDWA')
        self.__access_memory(node.test.comparators[0], 'CPWA')
    
        
        if node.orelse != []:
            self.__record_instruction(f'{inverted[type(node.test.ops[0])]} else_{if_id}')
        else:
            self.__record_instruction(f'{inverted[type(node.test.ops[0])]} endif_{if_id}')
        
        for contents in node.body:
            self.visit(contents)
        self.__record_instruction(f'BR endif_{if_id}')

        if len(node.orelse) > 0:
            self.__record_instruction(f'NOP1', label = f'else_{if_id}')

        for contents in node.orelse:
            self.visit(contents)

        self.__record_instruction(f'NOP1', label = f'endif_{if_id}')
        

    ####
    ## Not handling function calls 
    ####

    def visit_FunctionDef(self, node):
        """We do not visit function definitions, they are not top level"""
        pass

    ####
    ## Helper functions to 
    ####

    def __record_instruction(self, instruction, label = None):
        self.__instructions.append((label, instruction))

    def __access_memory(self, node, instruction, label = None):
        if isinstance(node, ast.Constant):
            self.__record_instruction(f'{instruction} {node.value},i', label)
        elif self.to_PEP9_name(node.id[0]) == '_' and self.to_PEP9_name(node.id[1:]).isupper():
            self.__record_instruction(f'{instruction} {self.to_PEP9_name(node.id)},i', label)
        else:
            self.__record_instruction(f'{instruction} {self.to_PEP9_name(node.id)},d', label)

    def __identifyLoop(self):
        result = self.__elem_id
        self.__elem_id = self.__elem_id + 1
        return result

    def __identifyif(self):
        self.__if_id = self.__if_id + 1
        return self.__if_id
