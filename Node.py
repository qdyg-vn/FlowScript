from enum import Enum


class Node:
    def __init__(self, node_type, args=None, operand=None):
        self.type = node_type
        self.operand = operand
        self.args = args

    def __iter__(self):
        return iter(self.args)

    def __repr__(self) -> str:
        output = f'{self.type} '
        if self.operand:
            output += f'{self.operand} '
        output += f'{self.args}'
        return output

class NodeType(Enum):
    CALL = 1
    LOAD = 2
    IDENTIFIER = 3
    FUNCTION = 4
