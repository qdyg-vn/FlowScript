class BuiltinsFunction:
    def __init__(self):
        self.functions = {
            'print': self.print,
            '+': self.sum,
            '-': self.minus,
            '*': self.multiply,
            '/': self.divide,
        }

    def execute_function(self, function, arg):
        return self.functions[function](arg)

    @staticmethod
    def print(arg):
        print(arg)

    @staticmethod
    def sum(numbers: list) -> int | float:
        return sum(numbers)

    @staticmethod
    def minus(numbers: list) -> int | float:
        if not numbers:
            return 0
        result = numbers[0]
        if len(numbers) >= 2:
            for i in numbers[1:]:
                result -= i
        return result

    @staticmethod
    def multiply(numbers: list) -> int | float:
        if not numbers:
            return 1
        result = 1
        for i in numbers:
            if i == 0:
                return 0
            result *= i
        return result

    @staticmethod
    def divide(numbers: list) -> float:
        if not numbers:
            return 0
        result = numbers[0]
        if len(numbers) >= 2:
            for number in numbers[1:]:
                if number == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= number
        return result
