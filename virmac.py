from bytecode import Bytecode, BytecodeType
from Builtins import BuiltinsFunction
from environment import Environment


class VirMac:
    def __init__(self, bytecodes: list[Bytecode]):
        self.bytecodes = bytecodes
        self.pos = -1
        self.stack = [None] * 1024
        self.stack_pointer = -1
        self.builtin_functions = BuiltinsFunction()
        self.environment = Environment()

    def advance(self, step=1):
        self.pos = self.pos + step
        return self.bytecodes[self.pos] if self.pos < len(self.bytecodes) else None

    def execute(self):
        while bytecode := self.advance():
            self.match_execute(bytecode)
        return self.stack

    def match_execute(self, bytecode: Bytecode):
        match bytecode.type:
            case BytecodeType.LOAD:
                self.stack_pointer += 1
                if self.stack_pointer >= len(self.stack):
                    self.stack += [None] * 1024
                self.stack[self.stack_pointer] = bytecode.operand
            case BytecodeType.STORE:
                self.environment.variables[bytecode.operand] = self.stack[self.stack_pointer]
            case BytecodeType.CALL:
                if bytecode.operand in '+-*/':
                    target_pointer = self.stack_pointer - bytecode.payload + 1
                    args = self.stack[target_pointer: self.stack_pointer + 1]
                    self.stack[target_pointer] = self.builtin_functions.execute_function(bytecode.operand, args)
                    self.stack_pointer = target_pointer
                else:
                    if result := self.builtin_functions.execute_function(bytecode.operand, self.stack[self.stack_pointer]) is not None:
                        self.stack[self.stack_pointer] = result
