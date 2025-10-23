from token_fscc import TokenType


class Parser:
    """
    Recursive-descent parser for a minimal arithmetic language.

    Consumes a mutable list of tokens and produces a list-based AST in prefix form.
    An operator token (+, -, *, /) must be followed by '(' ... ')' containing zero
    or more comma-less operands. Numeric tokens yield literal values.

    Parameters:
        tokens: List of Token instances to parse; consumed in place.

    Methods:
        parse() -> list: Parse and return an expression as ['+', arg1, ...] or a
            literal (int|float) when the next token is not an operator.

    Raises:
        SyntaxError: If '(' is missing after an operator or parentheses are malformed.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.function_type = [TokenType.TT_PLUS.value, TokenType.TT_MINUS.value, TokenType.TT_MUL.value, TokenType.TT_DIV.value]
        self.operator = None

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def peek(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None

    def parse(self):
        expressions = [self.parse_expression()]
        while self.pos < len(self.tokens) - 2:
            expressions.append(self.parse_expression())
        return expressions

    def parse_expression(self) -> list:
        self.advance()
        if self.current_token is not None and self.current_token.type in self.function_type:
            operator = self.current_token.value
            expr = [[operator]]
            index = 0
            self.advance()
            if self.current_token is not None and self.current_token.type != TokenType.TT_LPAREN.value:
                raise SyntaxError(f"Only expected '(' before {expr[0]}")
            while self.peek().type != TokenType.TT_RPAREN.value:
                if self.peek().type == TokenType.TT_SEMICOLON.value:
                    expr.append([operator])
                    index += 1
                    self.advance()
                token = self.parse_expression()
                expr[index].append(token)
            self.advance()
            return expr if index else expr[0]
        else:
            return self.current_token.value
