from builtins_fscc import BuiltinsFunction
from token_fscc import Token, TokenType


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
        self.builtins = BuiltinsFunction()
        self.code = code
        self.pos = -1
        self.current_char = None
        self.token_map = {
            '+': TokenType.TT_PLUS.value,
            '-': TokenType.TT_MINUS.value,
            '*': TokenType.TT_MUL.value,
            '/': TokenType.TT_DIV.value,
            '(': TokenType.TT_LPAREN.value,
            ')': TokenType.TT_RPAREN.value,
            ';': TokenType.TT_SEMICOLON.value
        }
        self.character_start_token = {
            '-': TokenType.TT_MINUS.value
        }
        self.token_map_multi_char = {
            '->': TokenType.TT_ARROW.value,
        }
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.code[self.pos] if self.pos < len(self.code) else None

    def peek(self):
        if self.pos + 1 < len(self.code):
            return self.code[self.pos + 1]
        return None

    def make_tokens(self) -> list[Token]:
        tokens = []
        while self.current_char is not None:
            if self.current_char in self.character_start_token:
                type_token, current_token = self.make_token_chars()
                tokens.append(Token(type_token, current_token))
            if self.current_char in self.token_map:
                tokens.append(Token(self.token_map[self.current_char], self.current_char))
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

    def make_token_chars(self):
        token = self.current_char + self.peek()
        if token in self.token_map_multi_char:
            self.advance()
            self.advance()
            return [self.token_map_multi_char[token], token]
        else:
            token = self.current_char
            self.advance()
            return [self.token_map[token], token]

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
            return Token(TokenType.TT_FLOAT.value, float(number))
        else:
            return Token(TokenType.TT_INT.value, int(number))

    def make_string(self) -> Token:
        string = ''
        while self.current_char is not None and self.current_char in TokenType.ALPHABET_DOWN.value + TokenType.ALPHABET_UP.value + '_':
            string += self.current_char
            self.advance()
        if string in self.builtins.functions:
            return Token(TokenType.TT_FUNCTION, string)
        return Token(TokenType.TT_STRING, string)
