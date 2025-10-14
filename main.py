import sys

from executor import Executor
from lexer import Lexer
from parser import Parser
from utils import reader


def main():
    try:
        code = reader(sys.argv[1])
    except IndexError:
        raise Exception("No input file specified.")
    lexer = Lexer(code)
    tokens = lexer.make_tokens()
    parser = Parser(tokens)
    ast = parser.parse()
    executor = Executor()
    result = executor.execute(ast)
    return result


if __name__ == '__main__':
    print(main())
