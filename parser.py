from token import TokenType


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

    def parse(self):
        expressions = []
        while self.tokens:
            expressions.append(self.parse_expression())
        return expressions

    def parse_expression(self) -> list:
        token = self.tokens.pop(0)
        function = [TokenType.TT_PLUS.value, TokenType.TT_MINUS.value, TokenType.TT_MUL.value, TokenType.TT_DIV.value]
        if token.type in function:
            expr = [token.value]
            if self.tokens.pop(0).type != TokenType.TT_LPAREN.value:
                raise SyntaxError('Too many function')
            while self.tokens[0].type != TokenType.TT_RPAREN.value:
                expr.append(self.parse_expression())
            self.tokens.pop(0)
            return expr
        else:
            return token.value
