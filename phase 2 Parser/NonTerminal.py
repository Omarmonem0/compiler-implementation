from Node import Node


class NonTerminal(Node):
    def __init__(self, value, next):
        super(NonTerminal, self).__init__(value, next)
        self.type = 'N'
