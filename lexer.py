from Builtins import BuiltinsFunction
from Token import TokenType, Token


class Lexer:
    def __init__(self, reader):
        self.reader = reader
        self.code = ''
        self.pos = -1
        self.identifiers = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MUL,
            '/': TokenType.DIV,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
        }

    def advance(self, step = 1):
        self.pos += step
        while len(self.code) <= self.pos:
            try:
                self.code = next(self.reader)
            except StopIteration:
                return None
        return self.code[self.pos]

    def peek(self):
        while len(self.code) <= self.pos + 1:
            try:
                self.code = next(self.reader)
            except StopIteration:
                return None
        return self.code[self.pos + 1]

    def lexer(self):
        while (char := self.peek()) is not None:
            if char in ('"', "'"):
                yield self.string_collector()
            elif char.isdigit():
                yield self.number_collector()
            elif char in ('+', '-', '*', '/', '(', ')'):
                yield self.identifier_collector()
            elif char.isspace() or char == ',':
                self.advance()
            elif char.isalpha():
                yield self.function_collector()

    def function_collector(self):
        start = self.pos + 1 # Because we're using peek() in lexer() so here pos + 1
        while (char := self.peek()) is not None and (char.isalpha() or char == '_'):
            self.advance()
        function = self.code[start:self.pos + 1]
        if BuiltinsFunction().functions.get(function):
            return Token(TokenType.FUNCTION, function)
        return Token(TokenType.IDENTIFIER, function)

    def identifier_collector(self):
        identifier = self.advance()
        if identifier == '-' and self.peek() == '>':
            self.advance()
            return Token(TokenType.ARROW, '->')
        return Token(self.identifiers.get(identifier), identifier)

    def string_collector(self):
        quotation_mark = self.advance()
        start = self.pos + 1 # Because pos in code is quotation_mark so here pos + 1
        while self.peek() not in (quotation_mark, None):
            self.advance()
        self.advance()
        return Token(TokenType.STRING, self.code[start:self.pos])

    def number_collector(self):
        start = self.pos + 1 # Because we're using self.peek() in self.lexer() so here pos + 1
        has_dot = False
        while self.peek() is not None and self.peek().isdigit() or self.peek() == '.':
            if self.advance() == '.':
                if has_dot:
                    raise SyntaxError("Multiple decimal points")
                has_dot = True
        if has_dot:
            return Token(TokenType.FLOAT, float(self.code[start:self.pos + 1]))
        return Token(TokenType.INT, int(self.code[start:self.pos + 1]))
