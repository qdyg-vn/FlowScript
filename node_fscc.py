from token_fscc import NodeType


class Node:
    """
    Represents an AST node with a type, optional command, and positional arguments.

    Attributes:
        type: Node category, expected to align with NodeType values.
        command: Optional command name for task nodes; ignored for others.
        args: List of child nodes or a scalar value for scalar nodes.

    __repr__:
        Returns a human-readable form:
        - For scalar nodes, the scalar value as-is.
        - For task nodes, "['<command>', <arg1>, <arg2>, ...]".
        - For other composite nodes, "[<arg1>, <arg2>, ...]".
    """
    def __init__(self, node_type, args, command = None):
        self.type = node_type
        self.command = command
        self.args = args

    def __repr__(self) -> str:
        if self.type == NodeType.SCALAR.value:
            output = f'{self.args}'
        else:
            output = '['
            if self.type == NodeType.TASK_NODE.value:
                output += f"'{self.command}', "
            output += ', '.join(map(str, self.args))
            output += ']'
        return output
