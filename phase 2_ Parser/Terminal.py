from Node import Node


class Terminal(Node):
    def __init__(self, value, next):
        Node.__init__(self, value, next)
        self.type = 'T'
