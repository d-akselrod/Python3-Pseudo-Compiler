import ast

class FunctionCalling(ast.NodeVisitor):

    def __init__(self):
        pass

    def visit_FunctionDef(self, node):
        return super().visit_FunctionDef(node) 