from Node import Node, NodeType
from Token import Token, TokenType


class Parser:
    def __init__(self, lexer):
        self.tokens = []
        self.pos = -1
        self.take_token = lexer
        self.operators = (TokenType.PLUS, TokenType.MINUS, TokenType.MUL, TokenType.DIV)

    def advance(self, step = 1):
        self.pos += step
        while len(self.tokens) <= self.pos:
            try:
                self.tokens.append(next(self.take_token))
            except StopIteration:
                return None
        return self.tokens[self.pos]

    def peek(self):
        while len(self.tokens) <= self.pos + 1:
            try:
                self.tokens.append(next(self.take_token))
            except StopIteration:
                return None
        return self.tokens[self.pos + 1]

    def parser(self):
        result = []
        while self.peek() is not None:
            result.append(self.wrapper_arrow(self.peek()))
        return result

    def operation_collector(self):
        operator = self.advance().value
        if self.advance().type != TokenType.LPAREN:
            raise SyntaxError(f"Behind operator need a left paren! But in your code is {self.peek().value}")
        args = [[]]
        while self.peek() is not None and self.peek().type != TokenType.RPAREN:
            if self.peek() == TokenType.SEMICOLON:
                args.append([])
                continue
            args[-1].append(self.return_values(self.peek()))
            self.advance()
        self.advance()
        return Node(NodeType.CALL, args, operator)

    def return_values(self, tok: Token):
        if tok.type in self.operators:
            return self.operation_collector()
        elif tok.type in (TokenType.INT, TokenType.FLOAT):
            return Node(NodeType.LOAD, tok.value)
        return None

    def wrapper_arrow(self, tok: Token):
        stations = [self.return_values(tok)]
        if self.peek() is None or self.peek().type != TokenType.ARROW:
            return stations[0]
        while self.peek() is not None and self.peek().type == TokenType.ARROW:
            if (next_tok := self.advance(2)).type == TokenType.FUNCTION:
                stations.append(Node(NodeType.FUNCTION, operand=next_tok.value))
            else:
                stations.append(Node(NodeType.IDENTIFIER, next_tok.value))
        return Node(NodeType.CALL, stations, '->')
