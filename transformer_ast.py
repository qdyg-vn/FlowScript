import copy

from node_fscc import Node
from token_fscc import NodeType


class Transformer:
    """
    Transforms ASTs by enumerating all combinations produced by MULTI_EXPR and TASK_NODE children.

    - replace_node_in_ast(ast, index, node): Deep-copies ast and substitutes the child at index.
    - multi_expression(expression, ast, index, result): Expands a MULTI_EXPR child and appends substituted AST variants.
    - transform_single(ast): Returns a MULTI_EXPR of expansions for one AST or the original when no expansion applies.
    - variable_assignment_transform(ast): Pairs variables and values from a VARIABLE_ASSIGNMENT node into [var, value] lists.
    - transform(ast): Processes a sequence of expressions, preserving CALCULATION variants and wrapping all outputs in a MULTI_EXPR.

    Notes:
    - Uses copy.deepcopy to avoid in-place mutation.
    - Relies on Node and NodeType semantics (MULTI_EXPR, TASK_NODE, CALCULATION, VARIABLE_ASSIGNMENT).
    """

    def replace_node_in_ast(self, ast: Node, index: int, node: Node):
        ast = copy.deepcopy(ast)
        ast.args[index] = node
        return ast

    def multi_expression(self, expression: Node, ast: Node, index: int, result: list):
        for single_expression in expression.args:
            child_results = self.transform_single(single_expression)
            if child_results.args[0].type == NodeType.TASK_NODE.value:
                for single_child_result in child_results.args:
                    result.append(self.replace_node_in_ast(ast, index, single_child_result))
            else:
                result.append(self.replace_node_in_ast(ast, index, child_results))

    def transform_single(self, ast: Node) -> Node:
        result = []
        for index, node in enumerate(ast.args):
            if node.type == NodeType.TASK_NODE.value:
                result.append(self.transform_single(node))
            elif node.type == NodeType.MULTI_EXPR.value:
                self.multi_expression(node, ast, index, result)
        if result:
            return Node(NodeType.MULTI_EXPR.value, result)
        else:
            return ast

    def variable_assignment_transform(self, ast: Node) -> list[list[Node]]:
        number_of_variables = len(ast.args[1])
        result = []
        for index in range(number_of_variables):
            result.append([ast.args[0][index], ast.args[1][index]])
        return result

    def transform(self, ast: list):
        results = []
        for expression in ast:
            if expression.type == NodeType.CALCULATION.value:
                for result in self.transform_single(expression):
                    results.append(Node(NodeType.CALCULATION.value, result))
            elif expression.type == NodeType.VARIABLE_ASSIGNMENT.value:
                results.append(Node(NodeType.VARIABLE_ASSIGNMENT.value, self.variable_assignment_transform(expression)))
        return Node(NodeType.MULTI_EXPR.value, results)
