class Node:
    def __init__(self, value, next):
        self.value = value
        self.next = next

    def __eq__(self, other):
        return self.value == other.value
