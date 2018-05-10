from Node import Node


class NonTerminal(Node):
    def __init__(self, value, next):
        Node.__init__(self, value, next)
        self.type = 'N'
