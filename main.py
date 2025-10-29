import sys

from executor import Executor
from transformer_ast import Transformer
from lexer import Lexer
from parser import Parser
from read_file import reader


def main():
    """
    Entry point for compiling and executing a .fscc program.

    Workflow:
    - Reads the source path from sys.argv[1] using reader; errors if absent.
    - Tokenizes with Lexer.make_tokens and prints the token stream.
    - Parses tokens into an AST via Parser.parse and prints it.
    - Transforms the AST for MULTI_EXPR/TASK_NODE expansion with Transformer.transform and prints it.
    - Executes with Executor.execute and returns a flattened list of results.

    Returns:
        list: Collected execution results.

    Raises:
        Exception: When no input file is provided.
        FileNotFoundError: If the file path is invalid.
        UnicodeDecodeError: If the file is not valid UTF-8.
        SyntaxError: For lexical or parsing issues surfaced during processing.
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
