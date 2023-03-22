import ast
from visitors.VarNameExtractor import SymbolTable 

class GlobalVariableExtraction(ast.NodeVisitor):
    """ 
        We extract all the left hand side of the global (top-level) assignments
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.to_PEP9_name = SymbolTable.toPEP9Name
        self.results = dict() #{name: type,value}

    def visit_Assign(self, node):
        if len(node.targets) != 1:
            raise ValueError("Only unary assignments are supported")

        if node.targets[0].id not in self.results.keys():
            self.results[self.to_PEP9_name(node.targets[0].id[:8])] = self.visit(node.value)
        

    def visit_Constant(self, node):
        return node.value


    def visit_FunctionDef(self, node):
        """We do not visit function definitions, they are not global by definition"""
        pass
   