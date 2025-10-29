from builtins_fscc import *
from environment import Environment
from token_fscc import NodeType


class Executor:
    """
    Interpreter that evaluates a small expression language AST, supporting arithmetic, multi-expression evaluation, variable assignment, and simple built-ins.

    Attributes:
        operation (Operation): Arithmetic engine for '+', '-', '*', '/'.
        env (Environment): Scoped variable store with lookup and assignment.
        builtin_functions (BuiltinsFunction): Built-in function registry (e.g., print).

    Methods:
        execute(ast) -> list:
            Traverse top-level commands, executing calculations and assignments; returns flattened results.
        execute_single_command(ast) -> int | float | list:
            Evaluate a single node (MULTI_EXPR, TASK_NODE, SCALAR), apply operator to values, and handle arrow chains.
        variable_assignment_execute(values_and_variables):
            Perform batch assignments by routing each value/name pair through arrow execution.
        execute_arrow(values, command: str):
            If command is 'print', emit via built-ins; otherwise store in env under the given name.
    """

    def __init__(self):
        self.operation = Operation()
        self.env = Environment()
        self.builtin_functions = BuiltinsFunction()

    def execute(self, ast) -> list:
        all_results = []
        for command in ast.args:
            if command.type == NodeType.CALCULATION.value:
                results = self.execute_single_command(command.args)
                if isinstance(results, list):
                    all_results.extend(results)
                else:
                    all_results.append(results)
            elif command.type == NodeType.VARIABLE_ASSIGNMENT.value:
                self.variable_assignment_execute(command)
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
                if not isinstance(current.args, str):
                    values[index].append(current.args)
                else:
                    if current.args == '->':
                        index += 1
                        values.append([])
                    else:
                        if index:
                            values[index].append(current.args)
                        else:
                            values[index].append(self.env.lookup(current.args))
        if index:
            result = self.operation.calculate(operator, values[0])
            for item in values[1:]:
                self.execute_arrow(result, item[0])
            return result
        else:
            return self.operation.calculate(operator, values[0])

    def variable_assignment_execute(self, values_and_variables):
        for item in values_and_variables:
            self.execute_arrow(item[0].args, item[1].args)

    def execute_arrow(self, values, command: str):
        if command == 'print':
            self.builtin_functions.print(values)
        else:
            self.env.add_variable(values, command)
