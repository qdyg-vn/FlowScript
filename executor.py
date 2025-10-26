from builtins_fscc import *
from environment import Environment
from token_fscc import NodeType


class Executor:
    """
    Executes an AST for a simple expression language with arithmetic, variable assignment, and built-ins.

    Attributes:
        operation (Operation): Arithmetic dispatcher for '+', '-', '*', '/'.
        env (Environment): Storage for variables with scoped lookup.
        builtin_functions (BuiltinsFunction): Registry for callable built-in functions.

    Methods:
        execute(ast) -> list:
            Walks the top-level AST, executing each command node and flattening results.
        execute_single_command(ast) -> int | float | list:
            Evaluates a single node:
            - MULTI_EXPR: evaluates subexpressions into a list.
            - TASK_NODE: evaluates nested tasks recursively.
            - SCALAR: resolves literals, identifiers (via env), and arrow separators.
            Applies the operator to accumulated values; routes arrow chains to execute_arrow.
        execute_arrow(operator: str, values: list) -> int | float:
            Applies the operator to the left-hand values, then processes each subsequent
            arrow target:
            - 'print' emits the result via built-ins.
            - otherwise stores the result in env under the given name.
            Returns the final computed result.
    """

    def __init__(self):
        self.operation = Operation()
        self.env = Environment()
        self.builtin_functions = BuiltinsFunction()

    def execute(self, ast) -> list:
        all_results = []
        for command in ast.args:
            results = self.execute_single_command(command)
            if isinstance(results, list):
                all_results.extend(results)
            else:
                all_results.append(results)
        return all_results

    def execute_single_command(self, ast) -> int | float | list:
        values = [[]]
        index = 0
        if ast.type == NodeType.MULTI_EXPR.value:
            for subexpression in ast.args:
                values[index].append(self.execute_single_command(subexpression))
            return values[0]
        operator = ast.command.args if ast.command else None
        for current in ast.args:
            if current.type == NodeType.TASK_NODE.value:
                values[index].append(self.execute_single_command(current))
            elif current.type == NodeType.SCALAR.value:
                if isinstance(current.args, str):
                    if current.args == '->':
                        index += 1
                        values.append([])
                    else:
                        if index:
                            values[index].append(current.args)
                        else:
                            values[index].append(self.env.lookup(current.args))
                else:
                    values[index].append(current.args)
        if index:
            return self.execute_arrow(operator, values)
        else:
            return self.operation.calculate(operator, values[0])

    def execute_arrow(self, operator: str, values: list) -> int | float:
        result = self.operation.calculate(operator, values[0])
        for value in values[1:]:
            if value[0] == 'print':
                self.builtin_functions.print(result)
            else:
                self.env.add_variable(value[0], result)
        return result
