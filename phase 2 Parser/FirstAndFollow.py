from Node import Node
from InputParser import start_parsing
import collections


def gettype(node):
    if node.type == 'N':
        return 1
    else:
        return 0


def get_first(productions, non_terminals):
    first = {}
    for non_terminal in non_terminals:
        first[non_terminal.value] = []
    productions = collections.OrderedDict(productions)
    for key, rule in reversed(productions.items()):
        for node in rule:
            if gettype(node) == 0:
                if node not in first[key]:
                    first[key].append(node)
            elif gettype(node) == 1:
                if node.value == key:
                    continue
                for x in first[node.value]:
                    if x not in first[key]:
                        first[key].append(x)
    return first


def get_follow(productions,  first, non_terminals, starting_symbol):
    starting_node = Node('$', None)
    follow = {}
    for non_terminal in non_terminals:
        follow[non_terminal.value] = []
    follow[starting_symbol].append(starting_node)
    for key_one, nodes_one in productions.items():
        for key_two, nodes_two in productions.items():
            for node in nodes_two:
                while node is not None and node.value != "epsilon":
                    if node.value == key_one and node.type == 'N':
                        if node.next is None:
                            if follow[key_two]:
                                for y in follow[key_two]:
                                    if y not in follow[node.value]:
                                        follow[node.value].append(y)
                                node = node.next
                                continue
                        if gettype(node.next) == 0:
                            if node.next not in follow[key_one]:
                                follow[key_one].append(node.next)
                            node = node.next
                            continue
                        if gettype(node.next) == 1:
                            if check_for_epsilons(node.next, first):
                                for x in first[node.next.value]:
                                    if x not in follow[key_one]:
                                        if x.value != "epsilon":
                                            follow[key_one].append(x)
                                for y in follow[key_two]:
                                    if y not in follow[node.value]:
                                        follow[key_one].append(y)
                            else:
                                for x in first[node.next.value]:
                                    if x not in follow[key_one]:
                                        follow[key_one].append(x)

                            node = node.next
                    else:
                        node = node.next

    return follow


def check_for_epsilons(node, first):
    for first_set_node in first[node.value]:
        if first_set_node.value == "epsilon":
            return True
    return False


def first_follow(productions):
    first = get_first(productions)
    follow = get_follow(productions, first)
    return {
        'FIRST': first,
        'FOLLOW': follow
    }


rules = start_parsing('CFG.txt')
first = get_first(rules['productions'], rules['non_terminals'])
# print("First")
# for key, value in first.items():
#     print(key, '->')
#     for node in value:
#         print(node.value)

# print("------------------------------------------------------------------------")
follow = get_follow(rules['productions'], first, rules['non_terminals'], rules['first_production'])
print("Follow")
for key, value in follow.items():
        print(key, '->')
        for node in value:
            print(node.value)
