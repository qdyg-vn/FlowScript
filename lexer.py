from token import Token, TokenType


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
            '+': TokenType.TT_PLUS.value,
            '-': TokenType.TT_MINUS.value,
            '*': TokenType.TT_MUL.value,
            '/': TokenType.TT_DIV.value,
            '(': TokenType.TT_LPAREN.value,
            ')': TokenType.TT_RPAREN.value,
            ';': TokenType.TT_SEMICOLON.value
        }
        while self.current_char is not None:
            if self.current_char in token_map:
                tokens.append(Token(token_map[self.current_char], self.current_char))
                self.advance()
            elif self.current_char in TokenType.ALPHABET_DOWN.value + TokenType.ALPHABET_UP.value:
                tokens.append(self.make_string())
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char in ' \t,\n':
                self.advance()
            else:
                raise SyntaxError(self.current_char)
        return tokens

    def make_number(self) -> Token:
        number = ''
        has_dot = False
        while self.current_char is not None and self.current_char in TokenType.DIGIT.value + '.':
            if self.current_char == '.':
                if has_dot:
                    raise SyntaxError("Multiple decimal points")
                has_dot = True
                number += '.'
            else:
                number += self.current_char
            self.advance()
        if has_dot:
            return Token(TokenType.TT_FLOAT, float(number))
        else:
            return Token(TokenType.TT_INT, int(number))

    def make_string(self) -> Token:
        string = ''
        while self.current_char is not None and self.current_char in TokenType.ALPHABET_DOWN.value + TokenType.ALPHABET_UP.value:
            string += self.current_char
            self.advance()
        return Token(TokenType.TT_STRING, string)
