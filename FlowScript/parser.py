from .token_fscc import TokenType, NodeType
from .node_fscc import Node

class Parser:
    """
    Recursive-descent parser that consumes a mutable list of Token objects and produces AST Nodes.

    - Builds:
        - Scalar nodes for literals and identifiers.
        - Task nodes for prefix operators with parenthesized, optionally semicolon-separated operands.
        - Multi-expression nodes when multiple task segments are grouped within the same parentheses.
        - Variable-assignment structures as [values, variables].

    Attributes:
        tokens: In-place token buffer.
        current_token: Cursor to the active token.
        position: Current index within tokens.
        operator_type: TokenType values considered operators.
        value_type: TokenType values considered scalar/identifier-like.
        operator: Scratch field for the active operator.

    Methods:
        parse() -> list[Node]: Parses top-level expressions until input is exhausted.
        parse_expression() -> Node: Parses a single expression (scalar or operator-led task/multi-expr).
        variable_assignment_parser() -> list[list[Node]]: Parses values and variable targets.
        advance(): Moves the cursor forward.
        peek(token_ahead: int = 1): Peeks ahead without consuming.

    Raises:
        SyntaxError: When an operator is not followed by '(' or on mismatched parentheses.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.position = -1
        self.operator_type = (TokenType.TT_PLUS.value, TokenType.TT_MINUS.value, TokenType.TT_MUL.value, TokenType.TT_DIV.value)
        self.value_type = (TokenType.TT_INT.value, TokenType.TT_FLOAT.value, TokenType.TT_IDENTIFIER.value, TokenType.TT_BOOLEAN.value, TokenType.TT_STRING.value, TokenType.TT_NONE.value, TokenType.TT_FUNCTION.value)
        self.operator = None

    def advance(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None

    def peek(self, token_ahead: int = 1):
        if self.position + token_ahead < len(self.tokens):
            return self.tokens[self.position + token_ahead]
        else:
            return None

    def parse(self) -> list[Node]:
        expressions = []
        while self.position < len(self.tokens) - 1:
            if self.peek().type in self.operator_type:
                expressions.append(Node(NodeType.CALCULATION.value, self.parse_expression()))
            elif self.peek().type in self.value_type:
                expressions.append(Node(NodeType.VARIABLE_ASSIGNMENT.value, self.variable_assignment_parser()))
        return expressions

    def parse_expression(self) -> Node:
        self.advance()
        if self.current_token is not None and self.current_token.type in self.operator_type:
            operator = self.current_token.value
            expr = [Node(NodeType.SCALAR.value, operator), []]
            index = 1
            self.advance()
            if self.current_token is not None and self.current_token.type != TokenType.TT_LPAREN.value:
                raise SyntaxError(f"Only expected '(' before {expr[0]}")
            while self.peek().type != TokenType.TT_RPAREN.value:
                if self.peek().type == TokenType.TT_SEMICOLON.value:
                    expr[index] = Node(NodeType.TASK_NODE.value, expr[index], expr[0])
                    expr.append([])
                    index += 1
                    self.advance()
                expr[index].append(self.parse_expression())
            self.advance()
            if index:
                expr[-1] = Node(NodeType.TASK_NODE.value, expr[-1], expr[0])
                return Node(NodeType.MULTI_EXPR.value, expr[1:])
            else:
                return Node(NodeType.TASK_NODE.value, expr[1], expr[0])
        else:
            return Node(NodeType.SCALAR.value, self.current_token.value)

    def variable_assignment_parser(self) -> list[list[Node]]:
        self.advance()
        values_and_variables = [[Node(NodeType.SCALAR.value, self.current_token.value)]]
        index = 0
        while self.peek() and self.peek().type in self.value_type + (TokenType.TT_ARROW.value,):
            self.advance()
            if self.current_token.type != TokenType.TT_ARROW.value:
                values_and_variables[index].append(Node(NodeType.SCALAR.value, self.current_token.value))
            else:
                index += 1
                values_and_variables.append([])
        self.advance()
        if len(set(len(list_variables) for list_variables in values_and_variables)) > 1:
            raise ValueError("VariableError: too few values or variables")
        return values_and_variables
