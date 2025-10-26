class Operation:
    """
    Utility class that applies basic arithmetic to a sequence of numbers.

    Supports '+', '-', '*', and '/' mapped to left-to-right operations:
    - '+' sums all numbers.
    - '-' subtracts subsequent numbers from the first (empty list -> 0).
    - '*' multiplies all numbers (empty list -> 1; short-circuits on 0).
    - '/' divides sequentially (empty list -> 0; raises on division by zero).

    Methods:
        calculate(operator, numbers): Validate operator and execute the mapped operation.

    Args:
        operator (str): One of '+', '-', '*', '/'.
        numbers (list[int | float]): Numbers processed in order.

    Returns:
        int | float: Result of the operation.

    Raises:
        ValueError: If the operator is not supported.
        ZeroDivisionError: If division by zero occurs.
    """

    __slots__ = ['calculator']

    def __init__(self):
        self.calculator = {
            '+': self._sum,
            '-': self._minus,
            '*': self._multiply,
            '/': self._divide
        }

    def calculate(self, operator: str, numbers: list) -> int | float:
        """Perform calculation with given operator and numbers."""
        if operator not in self.calculator:
            raise ValueError(f"Invalid operator: {operator!r}")
        return self.calculator[operator](numbers)

    @staticmethod
    def _sum(numbers: list) -> int | float:
        return sum(numbers)

    @staticmethod
    def _minus(numbers: list) -> int | float:
        if not numbers:
            return 0
        result = numbers[0]
        if len(numbers) >= 2:
            for i in numbers[1:]:
                result -= i
        return result

    @staticmethod
    def _multiply(numbers: list) -> int | float:
        if not numbers:
            return 1
        result = 1
        for i in numbers:
            if i == 0:
                return 0
            result *= i
        return result

    @staticmethod
    def _divide(numbers: list) -> float:
        if not numbers:
            return 0
        result = numbers[0]
        if len(numbers) >= 2:
            for number in numbers[1:]:
                if number == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= number
        return result

class BuiltinsFunction:
    def __init__(self):
        self.functions = {
            'print': self.print,
        }

    def execute_function(self, function, *args):
        if function in self.functions:
            self.functions[function](*args)

    def print(self, *args):
        print(*args)