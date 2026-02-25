from enum import Enum


class Token:
    def __init__(self, type_token, value=None):
        self.type = type_token
        self.value = value

    def __repr__(self) -> str:
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'


class TokenType(Enum):
    INT = 0
    FLOAT = 1
    STRING = 2
    BOOLEAN = 3
    LPAREN = 4
    RPAREN = 5
    PLUS = 6
    MINUS = 7
    MUL = 8
    DIV = 9
    SEMICOLON = 10
    ARROW = 11
    FUNCTION = 12
    IDENTIFIER = 13
