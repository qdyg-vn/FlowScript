from builtins_fscc import *
from environment import Environment


class Executor:
    """
    Evaluate list-based arithmetic expressions using Operation.

    Parses a list where one entry is an operator ('+', '-', '*', '/') and the rest are numeric operands or nested subexpressions. Nested lists are evaluated recursively, and operands are applied left-to-right via Operation.calculate.

    Args:
        ast (list): Expression containing one operator and its operands, which may include nested lists.

    Returns:
        int | float: The evaluated result.

    Raises:
        ValueError: If no valid operator is present.
        ZeroDivisionError: If a division by zero occurs.
    """

    def __init__(self):
        self.operation = Operation()
        self.env = Environment()

    def execute(self, ast: list) -> list:
        results = []
        for command in ast:
            results.append(self.execute_command(command))
        return results

    def execute_command(self, ast: list) -> int | float:
        values = []
        operator = ''
        for current in ast:
            if current in ('+', '-', '*', '/'):
                operator = current
            elif isinstance(current, list):
                values.append(self.execute_command(current))
            elif isinstance(current, str):
                values.append(self.env.lookup(current))
            else:
                values.append(current)
        return self.operation.calculate(operator, values)
