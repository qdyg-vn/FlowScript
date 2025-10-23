import sys

from executor import Executor
from transformer_ast import Transformer
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
    print("Lexer: ", tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    print("Parser: ", ast)
    transformer = Transformer()
    ast_transformed = transformer.transform(ast)
    print("Transform: ", ast_transformed)
    executor = Executor()
    result = executor.execute(ast_transformed)
    return result

if __name__ == '__main__':
    result = main()
    print(result)
