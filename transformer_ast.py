import copy

class Transformer:
    """
    AST transformation utilities for expanding nested list expressions.

    The Transformer class provides:
    - insert_ast(ast, index, item): Return a deep-copied AST with item inserted at index.
    - have_list(ast): Check whether any element of ast is a list.
    - multi_expr(expr, ast, index, result): Expand combinations when child transformations yield lists.
    - transform(ast): Recursively transform an AST by expanding nested list nodes; returns either
    the original ast, a single transformed branch, or a list of expanded variants.

    Args:
        ast: A list-based AST to inspect or transform.
        index: Position in ast where a child item should be placed.
        item: Replacement element for insertion.
        expr: A list expression (subtree) potentially containing nested lists.
        result: Accumulator list for collecting expanded AST variants.

    Returns:
        For insert_ast: A new AST with the specified insertion.
        For have_list: True if any element is a list, else False.
        For multi_expr: None; results appended to result.
        For transform: Either the original ast, a single transformed AST, or a list of transformed ASTs.
    """
    def insert_ast(self, ast, index, item):
        ast = copy.deepcopy(ast)
        ast[index] = item
        return ast

    def have_list(self, ast):
        for current in ast:
            if isinstance(current, list):
                return True
        return False

    def multi_expr(self, expr, ast, index, result):
        for item in expr:
            child_results = self.transform(item)
            if isinstance(child_results[0], list):
                for expand_sub in child_results:
                    result.append(self.insert_ast(ast, index, expand_sub))
            else:
                result.append(self.insert_ast(ast, index, item))

    def transform(self, ast):
        result = []
        for index,expr in enumerate(ast):
            if isinstance(expr,list):
                if self.have_list(expr):
                    if isinstance(expr[0], list):
                        self.multi_expr(expr, ast, index, result)
                    else:
                        result.append(self.transform(expr))
        if result:
            return result if len(result) > 1 else result[0]
        else:
            return ast
