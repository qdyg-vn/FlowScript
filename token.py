from enum import Enum


class TokenType(Enum):
    ALPHABET_DOWN = 'abcdefghijklmnopqrstuvwxyz'
    ALPHABET_UP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIGIT = '0123456789'
    TT_INT = 'INT'
    TT_FLOAT = 'FLOAT'
    TT_STRING = 'STRING'
    TT_BOOLEAN = 'BOOLEAN'
    TT_NONE = 'NONE'
    TT_LPAREN = 'LPAREN'
    TT_RPAREN = 'RPAREN'
    TT_PLUS = 'PLUS'
    TT_MINUS = 'MINUS'
    TT_MUL = 'MUL'
    TT_DIV = 'DIV'
    TT_SEMICOLON = 'SEMICOLON'
    TT_COMMA = 'COMMA'
    TT_UNDERSCORE = 'UNDERSCORE'
    TT_ARROW = 'ARROW'
    TT_FUNCTION = 'FUNCTION'

class Token:
    """
    Lightweight token for lexers/parsers, carrying a type and optional value.

    Attributes:
        type: Token category or identifier.
        value: Optional payload or lexeme; may be None.

    __repr__:
        Returns 'TYPE: VALUE' when value is truthy, otherwise 'TYPE'.
    """

    def __init__(self, type_token, value=None):
        self.type = type_token
        self.value = value

    def __repr__(self) -> str:
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'
