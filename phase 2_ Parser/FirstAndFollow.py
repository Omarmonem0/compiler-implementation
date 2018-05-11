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
        'S': [],
        'A': [],
        'E': [],
        'T': [],
    }
    for key in productions:
        for node in productions[key]:
            if gettype(node) == 0:
                first[key].append(node)
            elif gettype(node) == 1:
                temp = first_for_node(node, productions)
                for node in temp:
                    first[key].append(node)
    return first


def first_for_node(node, productions):
    temporary_first = []
    for node in productions[node.value]:
        if gettype(node) == 0:
            temporary_first.append(node)

        else:
            return first_for_node(node, productions)
    return temporary_first

def get_follow(productions, first):
    follow = {
        'S': [],
        'A': [],
        'E': [],
        'T': [],
    }
    buffer = {}
    nodes_have_epsilons = []
    for key in productions:
        for node in productions[key]:
            if check_type(node) == 3:
                if gettype(node.next.next) == 0:
                    if node.next.next.value not in follow[node.next.value]:
                        follow[node.next.value].append(node.next.next.value)
                        continue
                    else:
                        continue
                for element in first[node.next.next.value]:
                    if element.value not in follow[node.next.value]:
                        follow[node.next.value].append(element.value)
            if check_type(node) == 2:
                if not follow[node.next.value]:
                    buffer.update({node.next.value: key})
                    continue

    for key in buffer:
        for element in follow[buffer[key]]:
            follow[key].append(element)
    return follow


def check_type(node):
    count = 0
    count += 1
    node = node.next
    while node is not None:
            node = node.next
            count += 1
    return count

# Non Terminals


S = NonTerminal('S', None)
A = NonTerminal('A', None)  # e bar
E = NonTerminal('E', None)
T = NonTerminal('T', None)  # t bar

# Terminals
AND = Terminal('&', None)
a = Terminal('a', None)
b = Terminal('b', None)
c = Terminal('c', None)
openBracket = Terminal('(', None)
closeBracket = Terminal(')', None)

# making rules
n_epsilon = Terminal('$', None)

n1 = copy.deepcopy(openBracket)
A_duplicate = copy.deepcopy(A)
A_duplicate.next = closeBracket
n1.next = A_duplicate

n2 = copy.deepcopy(T)
n2.next = copy.deepcopy(E)


n3 = copy.deepcopy(AND)
T_duplicate_two = copy.deepcopy(T)
T_duplicate_two.next = copy.deepcopy(E)
n3.next = T_duplicate_two


n4 = copy.deepcopy(openBracket)
A_duplicate_two = copy.deepcopy(A)
A_duplicate_two.next = closeBracket
n4.next = A_duplicate

n5 = a
n6 = b
n7 = c

rules = {
    'S': [n1],
    'A': [n2],
    'E': [n3],
    'T': [n4, n5, n6, n7]
}
first = get_first(rules)
print("first")
for key in first:
    for nodes in first[key]:
        print(key, '->', nodes.value)
print("follow")
print(get_follow(rules, first))
