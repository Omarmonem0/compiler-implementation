from Node import Node


class Terminal(Node):
    def __init__(self, value, next):
        super(Terminal, self).__init__(value, next)
        self.type = 'T'
