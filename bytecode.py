from enum import Enum


class Bytecode:
    def __init__(self, bc_type, operand, payload=None):
        self.type = bc_type
        self.operand = operand
        self.payload = payload

    def __iter__(self):
        return iter(self.operand)

    def __repr__(self) -> str:
        output = ''
        match self.type:
            case BytecodeType.LOAD:
                output += "LOAD "
            case BytecodeType.STORE:
                output += "STORE "
            case BytecodeType.CALL:
                output += "CALL "
        output += str(self.operand)
        if self.payload:
            return output + ' ' + str(self.payload)
        return output

class BytecodeType(Enum):
    LOAD = 0
    STORE = 1
    CALL = 2
