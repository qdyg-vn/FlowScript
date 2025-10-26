import sys

from executor import Executor
from transformer_ast import Transformer
from lexer import Lexer
from parser import Parser
from read_file import reader


def main():
    """
    Entry point that compiles and runs a .fscc program.

    Steps:
    - Reads the input file path from sys.argv[1] via reader; raises if missing.
    - Lexes source into tokens (Lexer.make_tokens) and logs them.
    - Parses tokens into an AST (Parser.parse) and logs it.
    - Transforms the AST for task/multi-expression expansion (Transformer.transform_) and logs it.
    - Executes the transformed AST (Executor.execute) and returns the resulting list.

    Returns:
        list: Flattened execution results from the program.

    Raises:
        Exception: If no input file is specified.
        FileNotFoundError, UnicodeDecodeError, SyntaxError: Propagated from underlying stages.
    """

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
    print("Result:", result)
