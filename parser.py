from node_fscc import Node
from token_fscc import TokenType, NodeType


class Parser:
    """
    Recursive-descent parser that builds AST nodes using internal TokenType and NodeType.

    Parses a mutable token list into:
    - Scalar nodes for literals.
    - Task nodes representing prefix operators with grouped operands.
    - Multi-expression nodes when separated by semicolons within parentheses.

    Parameters:
        tokens: In-place consumed list of Token objects.

    Methods:
        parse() -> list[Node]: Returns a list of parsed top-level expressions.
        parse_expression() -> Node: Parses a single expression per the operator/operand rules.
        advance(): Moves to the next token.
        peek(): Returns the upcoming token without consuming it.

    Raises:
        SyntaxError: If an operator is not followed by '(' or if parentheses are mismatched.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.position = -1
        self.operator_type = [TokenType.TT_PLUS.value, TokenType.TT_MINUS.value, TokenType.TT_MUL.value, TokenType.TT_DIV.value]
        self.operator = None

    def advance(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None

    def peek(self):
        return self.tokens[self.position + 1] if self.position + 1 < len(self.tokens) else None

    def parse(self) -> list:
        expressions = [self.parse_expression()]
        while self.position < len(self.tokens) - 1:
            expressions.append(self.parse_expression())
        return expressions

    def parse_expression(self):
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
