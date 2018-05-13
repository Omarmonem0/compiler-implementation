from Node import Node
from Terminal import Terminal
from NonTerminal import NonTerminal


def top(stack):
    return stack[len(stack) - 1]


def make_array(node):
    temp = []
    while node:
        temp.append(node)
        node = node.next
    return temp

# TODO: handle epsilon $


def start_parsing(file_name, table, first_production):
    file = open(file_name, 'r')
    data = file.read()
    data += '\n$'
    data = data.split('\n')
    stack = [Terminal('$', None), NonTerminal(first_production, None)]
    i = 0

    while i < len(data):
        if data[i] == '' or data[i] == ' ':
            continue
        if top(stack).type == 'T':
            if top(stack).value == data[i]:
                stack.pop()
                print('Matched {}'.format(data[i]))
                i += 1
            else:
                stack.pop()
                print('Error: missing {}, inserted'.format(top(stack).value))
        elif top(stack).type == 'N':
            if isinstance(table[top(stack).value][data[i]], Node):
                # pop that node and reverse its production
                top_node = stack.pop()
                production_array = make_array(table[top_node.value][data[i]])
                while len(production_array):
                    stack.append(production_array.pop())
            elif table[top(stack).value][data[i]] == 'synch':
                # TODO handle synch
                pass
            else:
                print('Error: (illegal {}), discarding {}'.format(top(stack), data[i]))
                i += 1

        if len(stack) == 0 and i == len(data):
            print('Accept')
        elif len(stack) == 0 and i < len(data) or len(stack) > 0 and i == len(data):
            print('Reject')

AbS = NonTerminal('A', Terminal('b', NonTerminal('S', None)))
e = Terminal('e', None)
a = Terminal('a', None)
cAd = Terminal('c', NonTerminal('A', Terminal('d', None)))

table = {
    'S': {
        'a': AbS,
        'b': None,
        'c': AbS,
        'd': None,
        'e': e
    },
    'A': {
        'a': a,
        'b': 'synch',
        'c': cAd,
        'd': 'synch',
        'e': None
    }
}


start_parsing('input-program.txt', table, 'S')
