##############################
# ENVIRONMENT
##############################

class Environment:
    def __init__(self):
        self.variables = {'aBz': 110}
        self.variables_private = {}

    def lookup(self, variable: str, parent=None) -> int | float:
        if variable in self.variables:
            return self.variables[variable]
        elif parent in self.variables_private and variable in self.variables_private[parent]:
            return self.variables_private[parent][variable]
        raise KeyError(f"Variable '{variable}' not found in environment")
