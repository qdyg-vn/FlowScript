from Node import NodeType
from bytecode import Bytecode, BytecodeType


class Emitter:
    def __init__(self, nodes):
        self.nodes = nodes
        self.queue = []

    def emitter(self) -> list[Bytecode]:
        for node in self.nodes:
            self.emit_bytecode(node)
        return self.queue

    def call_node(self, node):
        if node.operand == '->':
            self.arrow(node)
        else:
            for chunk in node:
                for idx, arg in enumerate(chunk):
                    self.emit_bytecode(arg)
                self.queue.append(Bytecode(BytecodeType.CALL, node.operand, len(chunk)))

    def arrow(self, node):
        self.emit_bytecode(node.args[0])
        for station in node.args[1:]:
            if station.type == NodeType.FUNCTION:
                self.queue.append(Bytecode(BytecodeType.CALL, station.operand))
            else:
                self.queue.append(Bytecode(BytecodeType.STORE, station.args))

    def emit_bytecode(self, node):
        if node.type == NodeType.CALL:
            self.call_node(node)
        elif node.type == NodeType.LOAD:
            self.queue.append(Bytecode(BytecodeType.LOAD, node.args))
