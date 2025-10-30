from .token_fscc import Token, TokenType, CharacterSets
from .builtins_fscc import BuiltinsFunction


class Lexer:
    """
    Lexical analyzer for a minimal expression language with functions and comments.

    Parses the input source into Token instances, recognizing:
    - Single-char tokens: +, -, *, /, (, ), ;
    - Multi-char tokens: ->
    - Literals: integers, floats, strings (single or double-quoted)
    - Identifiers and built-in function names
    - Whitespace (space, tab, comma, newline) is skipped
    - Comments: single-line starting with #, and triple-# block comments ###...###

    Attributes:
        builtins (BuiltinsFunction): Registry used to classify function identifiers.
        code (str): Original source text.
        position (int): Current index in code (-1 before the first advance).
        current_character (str | None): Current character or None at EOF.
        single_character (dict[str, str]): Map of single-char lexemes to token types.
        character_start_token (dict[str, str]): Starters for potentially multi-char tokens.
        multi_characters (dict[str, str]): Map of multi-char lexemes to token types.

    Methods:
        advance(): Move to the next character.
        peek(position=1) -> string: Look ahead without consuming.
        make_tokens() -> list[Token]: Produce the full token stream, tracking line numbers for errors.
        make_command_multi_character(): Emit single- or multi-character operator tokens.
        make_number() -> Token: Scan an int or float literal.
        make_string() -> Token: Scan identifiers, built-in function names, or strings.
        skip_token(): Skip single-line or ### block comments.

    Raises:
        SyntaxError: For unknown characters or malformed numbers (e.g., multiple decimal points).
    """

    def __init__(self, code):
        self.builtins = BuiltinsFunction()
        self.code = code
        self.position = -1
        self.current_character = None
        self.single_character = {
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
        self.multi_characters = {
            '->': TokenType.TT_ARROW.value,
        }
        self.advance()

    def advance(self, character_ahead: int = 1):
        self.position += character_ahead
        self.current_character = self.code[self.position] if self.position < len(self.code) else None

    def peek(self, character_ahead: int = 1) -> str | None:
        if self.position + character_ahead < len(self.code):
            return self.code[self.position + character_ahead]
        return None

    def make_tokens(self) -> list[Token]:
        tokens: list[Token] = []
        line = 1
        while self.current_character is not None:
            if self.current_character in self.character_start_token:
                tokens.append(self.make_command_multi_character())
            if self.current_character in self.single_character:
                tokens.append(Token(self.single_character[self.current_character], self.current_character))
                self.advance()
            elif self.current_character in CharacterSets.ALPHABET_DOWN.value + CharacterSets.ALPHABET_UP.value:
                tokens.append(self.make_string())
            elif self.current_character.isdigit():
                tokens.append(self.make_number())
            elif self.current_character in ' \t,\n':
                if self.current_character == '\n':
                    line += 1
                self.advance()
            elif self.current_character == '#':
                self.skip_token()
                self.advance()
            else:
                raise SyntaxError(f"{self.current_character}, line {line}")
        return tokens

    def make_command_multi_character(self) -> Token:
        command = self.current_character + self.peek()
        token_type = self.multi_characters.get(command)
        if token_type is not None:
            self.advance(2)
            return Token(token_type, command)
        else:
            command = self.current_character
            self.advance()
            return Token(self.single_character.get(command), command)

    def make_number(self) -> Token:
        number = ''
        has_dot = False
        while self.current_character is not None and self.current_character in CharacterSets.DIGIT.value + '.':
            if self.current_character == '.':
                if has_dot:
                    raise SyntaxError("Multiple decimal points")
                has_dot = True
                number += '.'
            else:
                number += self.current_character
            self.advance()
        if has_dot:
            return Token(TokenType.TT_FLOAT.value, float(number))
        else:
            return Token(TokenType.TT_INT.value, int(number))

    def make_string(self) -> Token:
        string = ''
        while self.current_character is not None and self.current_character in CharacterSets.ALPHABET_DOWN.value + CharacterSets.ALPHABET_UP.value + '_' + "'" + '"':
            string += self.current_character
            self.advance()
        if string in self.builtins.functions:
            return Token(TokenType.TT_FUNCTION.value, string)
        elif string[0] == string[-1] in ['"', "'"]:
            return Token(TokenType.TT_STRING.value, string)
        elif string in ['True', 'False']:
            return Token(TokenType.TT_BOOLEAN.value, bool(string))
        elif string == 'None':
            return Token(TokenType.TT_NONE.value, string)
        return Token(TokenType.TT_IDENTIFIER.value, string)

    def skip_token(self):
        if self.peek() == self.peek(2) == '#':
            self.advance(2)
            while self.peek(2) is not None or self.current_character != '#' and self.peek() != '#' and self.peek(
                    2) != '#':
                self.advance()
            self.advance(2)
        else:
            while self.peek() != '\n' and self.current_character is not None:
                self.advance()
