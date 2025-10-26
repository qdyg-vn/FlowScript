import copy

from node_fscc import Node
from token_fscc import NodeType


class Transformer:
    """
    AST transformer that expands task and multi-expression nodes into all combinations.

    Methods:
    - replace_node_in_ast(ast, index, item): Deep-copies ast and replaces args[index] with item.
    - multi_expression(expr, ast, index, result): Expands a MULTI_EXPR child, appending substituted ASTs to result. If the child yields TASK_NODE results, each is expanded individually.
    - transform_single(ast): Walks a single AST's args. For TASK_NODE children, recurses; for MULTI_EXPR, delegates to multi_expr. Returns a MULTI_EXPR node of expansions or the original ast if no changes.
    - transform(ast): Batch variant for an iterable of ASTs, flattening per-item transform outputs into a single MULTI_EXPR node.

    Notes:
    - Uses copy.deepcopy to avoid mutating the original ASTs.
    - Relies on Node and NodeType contracts where MULTI_EXPR aggregates expansions and TASK_NODE may expand into multiple alternatives.
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

    def transform_single(self, ast: Node):
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

    def transform(self, ast: list):
        results = []
        for expression in ast:
            for result in self.transform_single(expression).args:
                results.append(result)
        return Node(NodeType.MULTI_EXPR.value, results)
