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
        self.builtin_functions = BuiltinsFunction()

    def execute(self, ast: list) -> list:
        results = []
        for command in ast:
            results.append(self.execute_command(command))
        return results

    def execute_command(self, ast: list) -> int | float:
        values = [[]]
        index = 0
        operator = ''
        for current in ast:
            if current in ('+', '-', '*', '/'):
                operator = current
            elif isinstance(current, list):
                values[index].append(self.execute_command(current))
            elif isinstance(current, str):
                if current == '->':
                    index += 1
                    values.append([])
                else:
                    if index:
                        values[index].append(current)
                    else:
                        values[index].append(self.env.lookup(current))
            else:
                values[index].append(current)
        if index:
            return self.execute_arrow(operator, values)
        else:
            return self.operation.calculate(operator, values[0])

    def execute_arrow(self, operator: str, values: list) -> int | float:
        result = self.operation.calculate(operator, values[0])
        for value in values[1:]:
            if value[0] == 'print':
                print("Hàm print built test +(a,b->print): ", end='')
                self.builtin_functions.print(result)
            else:
                self.env.add_variable(value[0], result)
        return result
