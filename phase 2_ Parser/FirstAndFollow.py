from Node import Node
from Terminal import Terminal
from NonTerminal import NonTerminal
import copy


def gettype(node):
    if node.type == 'N':
        return 1
    else:
        return 0


def get_first(productions):
    first = {
        'E': [],
        'S': [],
        'T': [],
        'M': [],
        'F': []
    }
    for key in productions:
        for node in productions[key]:
            if gettype(node) == 0:
                first[key].append(node.value)
            elif gettype(node) == 1:
                temp = first_for_node(node, productions)
                first[key].append(temp.value)
    return first


def first_for_node(node, productions):
    for node in productions[node.value]:
        if gettype(node) == 0:
            return node
        else:
            return first_for_node(node, productions)


def get_follow():
    return 0


# Non Terminals

E = NonTerminal('E', None)
S = NonTerminal('S', None)  # e bar
T = NonTerminal('T', None)
M = NonTerminal('M', None)  # t bar
F = NonTerminal('F', None)
# Terminals
plus = Terminal('+', None)
Id = Terminal('id', None)
star = Terminal('*', None)
openBracket = Terminal('(', None)
closeBracket = Terminal(')', None)

# making rules
n_epsilon = Terminal('$', None)
n1 = copy.deepcopy(T)
n1.next = S

T_duplicate = copy.deepcopy(T)
T_duplicate.next = copy.deepcopy(S)
n2 = copy.deepcopy(plus)
n2.next = T_duplicate

n3 = copy.deepcopy(F)
n3.next = M

F_duplicate = copy.deepcopy(F)
F_duplicate.next = copy.deepcopy(M)
n4 = copy.deepcopy(star)
n4.next = F_duplicate

E_duplicate = copy.deepcopy(E)
n5 = copy.deepcopy(openBracket)
n5.next = E_duplicate
E_duplicate.next = closeBracket

rules = {
    'E': [n1],
    'S': [n2, n_epsilon],
    'T': [n3],
    'M': [n4, n_epsilon],
    'F': [n5]
}
print(get_first(rules))
