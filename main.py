from builtins_fscc import *

##############################
#   TOKENS
##############################
DIGIT = '0123456789'
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_BOOLEAN = 'BOOLEAN'
TT_NONE = 'NONE'
TT_LPAREN = '('
TT_RPAREN = ')'
TT_PLUS = '+'
TT_MINUS = '-'
TT_MUL = '*'
TT_DIV = '/'
TT_SEMICOLON = ';'
TT_COMMA = ','


class Token:
    """
    Lightweight token for lexers/parsers, carrying a type and optional value.

    Attributes:
        type: Token category or identifier.
        value: Optional payload or lexeme; may be None.

    __repr__:
        Returns 'TYPE: VALUE' when value is truthy, otherwise 'TYPE'.
    """

    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'


##############################
#   LEXER
##############################

class Lexer:
    """
    Lexical analyzer for a simple arithmetic language.

    On initialization, primes the first character and position. Tokenizes '+', '-', '*', '/', '(', ')', ';' and integer/float literals; skips spaces, tabs, and commas.

    Parameters:
        code: Source text to tokenize.

    Attributes:
        code: Original source text.
        pos: Current zero-based index into source.
        current_char: Character at pos or None at EOF.

    Methods:
        make_tokens() -> list[Token]: Produce the full token stream.
        make_number() -> Token: Return TT_INT/TT_FLOAT for a numeric literal.

    Raises:
        SyntaxError: On unknown characters or numbers with multiple decimal points.
    """

    def __init__(self, code):
        self.code = code
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.code[self.pos] if self.pos < len(self.code) else None

    def make_tokens(self) -> list[Token]:
        tokens = []
        token_map = {
            '+': TT_PLUS,
            '-': TT_MINUS,
            '*': TT_MUL,
            '/': TT_DIV,
            '(': TT_LPAREN,
            ')': TT_RPAREN,
            ';': TT_SEMICOLON
        }
        while self.current_char is not None:
            if self.current_char in token_map:
                tokens.append(Token(token_map[self.current_char], self.current_char))
                self.advance()
            elif self.current_char in DIGIT:
                tokens.append(self.make_number())
            elif self.current_char in ' \t,':
                self.advance()
            else:
                raise SyntaxError(self.current_char)
        return tokens

    def make_number(self) -> Token:
        number = ''
        has_dot = False
        while self.current_char is not None and self.current_char in DIGIT + '.':
            if self.current_char == '.':
                if has_dot:
                    raise SyntaxError("Multiple decimal points")
                has_dot = True
                number += '.'
            else:
                number += self.current_char
            self.advance()
        if has_dot:
            return Token(TT_FLOAT, float(number))
        else:
            return Token(TT_INT, int(number))


##############################
# PARSER
##############################

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

    def parse(self) -> list:
        token = self.tokens.pop(0)
        function = [TT_PLUS, TT_MINUS, TT_MUL, TT_DIV]
        if token.type in function:
            expr = [token.value]
            if self.tokens.pop(0).type != TT_LPAREN:
                raise SyntaxError('Too many function')
            while self.tokens[0].type != TT_RPAREN:
                expr.append(self.parse())
            self.tokens.pop(0)
            return expr
        else:
            return token.value


##############################
# EXECUTOR
##############################

class Executor:
    """
    Evaluate list-based arithmetic expressions using Operation.

    Parses a list where one entry is an operator ('+', '-', '*', '/') and the rest are numeric operands or nested subexpressions. Nested lists are evaluated recursively, and operands are applied left-to-right via Operation.calculate.

    Args:
        ast (list): Expression containing one operator and its operands, which may include nested lists.

    Returns:
        int | float: The evaluated result.

    Raises:
        ValueError: If no valid operator is present.
        ZeroDivisionError: If a division by zero occurs.
    """

    def __init__(self):
        self.operation = Operation()

    def execute(self, ast) -> int | float:
        values = []
        operator = ''
        for current in ast:
            if current in ('+', '-', '*', '/'):
                operator = current
            elif isinstance(current, list):
                values.append(self.execute(current))
            else:
                values.append(current)
        return self.operation.calculate(operator, values)


##############################
# RUN
##############################

def run(text):
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    executor = Executor()
    result = executor.execute(ast)
    return result


while True:
    text = input(">>")
    result = run(text)
    print(result)
