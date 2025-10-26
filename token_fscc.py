from enum import Enum


class CharacterSets(Enum):
    """
    Enumeration of common character sets.

    Members:
    - ALPHABET_DOWN: Lowercase English letters a–z.
    - ALPHABET_UP: Uppercase English letters A–Z.
    - DIGIT: Decimal digits 0–9.

    Use to reference predefined character groups for validation, parsing, or token generation.
    """

    ALPHABET_DOWN = 'abcdefghijklmnopqrstuvwxyz'
    ALPHABET_UP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DIGIT = '0123456789'


class TokenType(Enum):
    """
    Enumeration of token categories used by the tokenizer/parser.

    Members include character sets for letters and digits, and symbolic tokens
    for literals, punctuation, operators, delimiters, and identifiers, such as:
    - ALPHABET_DOWN/ALPHABET_UP/DIGIT: character classes
    - TT_INT, TT_FLOAT, TT_STRING, TT_BOOLEAN, TT_NONE: literal types
    - TT_LPAREN, TT_RPAREN, TT_SEMICOLON, TT_COMMA, TT_UNDERSCORE: delimiters
    - TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_ARROW: operators
    - TT_FUNCTION, TT_IDENTIFIER: keywords and names
    """

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
    TT_IDENTIFIER = 'IDENTIFIER'


class NodeType(Enum):
    """
    Enumeration of node types.

    Members:
    - MULTI_EXPR: Node aggregating multiple expressions.
    - TASK_NODE: Node representing an executable task.
    - SCALAR: Node holding a scalar/atomic value.
    """

    MULTI_EXPR = 1
    TASK_NODE = 2
    SCALAR = 3


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
