class Environment:
    """
    Lightweight environment for storing and retrieving variables by scope.

    Attributes:
        variables (dict[str, dict[str, int | float]]): Mapping of scope names to variable dictionaries.

    Methods:
        add_variable(value, name, parent='global'):
            Add or update a variable in the specified scope.
        lookup(variable, parent='global') -> int | float:
            Return the value of a variable from the specified scope.
            Raises KeyError if the variable is not found.
    """

    def __init__(self):
        self.variables = {'global': {}}

    def add_variable(self, value, name: str, parent: str = 'global'):
        self.variables[parent][name] = value

    def lookup(self, variable: str, parent: str = 'global') -> int | float:
        if parent in self.variables and variable in self.variables[parent]:
            return self.variables[parent][variable]
        raise KeyError(f"Variable '{variable}' not found in environment")
