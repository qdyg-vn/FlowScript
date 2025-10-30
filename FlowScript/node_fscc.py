from .token_fscc import NodeType


class Node:
    """
    AST node with a type, optional command, and positional arguments.

    Attributes:
        type: Node category (NodeType or its value).
        command: Command name for task nodes; ignored otherwise.
        args: Sequence of child nodes or a scalar for scalar nodes.

    Iteration:
        Yields elements from args.

    __repr__:
        - Scalar nodes: the scalar value.
        - Task nodes: "['<command>', <arg1>, <arg2>, ...]".
        - Other composites: "[<arg1>, <arg2>, ...]".
    """

    def __init__(self, node_type, args, command=None):
        self.type = node_type
        self.command = command
        self.args = args

    def __iter__(self):
        return iter(self.args)

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
