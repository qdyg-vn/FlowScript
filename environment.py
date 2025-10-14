##############################
# ENVIRONMENT
##############################

class Environment:
    def __init__(self):
        self.variables = {'global': {}}

    def add_variable(self, name, value, parent='global'):
        self.variables[parent][name] = value
        print(self.variables)

    def lookup(self, variable: str, parent='global') -> int | float:
        if parent in self.variables and variable in self.variables[parent]:
            return self.variables[parent][variable]
        raise KeyError(f"Variable '{variable}' not found in environment")
