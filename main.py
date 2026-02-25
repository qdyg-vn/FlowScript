import sys

from emitter import Emitter
from lexer import Lexer
from parser import Parser
from reader import reader
from virmac import VirMac


def main():
    try:
        file = sys.argv[1]
    except IndexError:
        raise Exception("No input file specified.")
    ast = Parser(Lexer(reader(file)).lexer()).parser()
    bytecode = Emitter(ast).emitter()
    VirMac(bytecode).execute()


if __name__ == '__main__':
    main()
