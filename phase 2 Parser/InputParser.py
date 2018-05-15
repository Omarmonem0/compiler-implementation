from NonTerminal import NonTerminal
from Terminal import Terminal


def start_parsing(file_name):
    file = open(file_name, 'r')
    file_content = file.read()

    terminal_buffer = ''
    non_terminal_buffer = ''
    lhs_buffer = ''
    first_production = ''
    is_lhs = False
    is_rhs = False
    is_first_rhs_node = True
    filling_terminal = False
    productions = {}
    terminals = []
    non_terminals = []

    for index, char in enumerate(file_content):
        if char == '#':
            is_lhs = True
            is_rhs = False
            is_first_rhs_node = True
            filling_terminal = False
            lhs_buffer = ''
            continue
        if char == '=' and not is_rhs:
            is_lhs = False
            is_rhs = True
            is_first_rhs_node = True
            productions[lhs_buffer] = []
            n = NonTerminal(lhs_buffer, None)
            if not check_if_existed(non_terminals, n):
                   non_terminals.append(n)
            if len(productions) == 1:
                first_production = lhs_buffer
            continue
        if is_lhs:
            if char == ' ':
                continue
            if char.isalnum() or char == '_':
                lhs_buffer += char
                continue
        if is_rhs:
            if char == ' ' or char == '|' or char == '\n':
                if non_terminal_buffer:
                    n = NonTerminal(non_terminal_buffer, None)
                    if not check_if_existed(non_terminals, n):
                        non_terminals.append(n)
                    if is_first_rhs_node:
                        productions[lhs_buffer].append(n)
                    else:
                        length = len(productions[lhs_buffer])
                        temp = productions[lhs_buffer][length - 1]
                        while temp.next:
                            temp = temp.next
                        temp.next = n
                    if char == ' ' or char == '\n':
                        is_first_rhs_node = False
                    elif char == '|':
                        is_first_rhs_node = True
                    non_terminal_buffer = ''
                elif char == '|':
                    is_first_rhs_node = True
                continue
            if char == '\'':
                if terminal_buffer:
                    if terminal_buffer == '\L':
                        terminal_buffer = 'epsilon'
                    t = Terminal(terminal_buffer, None)
                    if not check_if_existed(terminals, t):
                        terminals.append(t)
                    if is_first_rhs_node:
                        productions[lhs_buffer].append(t)
                    else:
                        length = len(productions[lhs_buffer])
                        temp = productions[lhs_buffer][length - 1]
                        while temp.next:
                            temp = temp.next
                        temp.next = t
                    is_first_rhs_node = False
                    filling_terminal = False
                    terminal_buffer = ''
                else:
                    filling_terminal = True
                continue
            if not filling_terminal:
                non_terminal_buffer += char
            elif filling_terminal:
                terminal_buffer += char

    check_left_recursion(productions)
    return {
        'productions': productions,
        'terminals': terminals,
        'non_terminals': non_terminals,
        'first_production': first_production
    }


def check_left_recursion(productions):
    for N, L in productions.items():
        left_recursion(N, L, productions, 7)


def left_recursion(non_terminal, node_list, productions, level):
    for node in node_list:
        if node.type == 'N':
            if node.value == non_terminal:
                exit('Left recursion found in {}, Terminating...'.format(node.value))
            elif level:
                left_recursion(non_terminal, productions[node.value], productions, level - 1)


def check_if_existed(node_list, node):
    for n in node_list:
        if node == n:
            return True
    return False


# print(start_parsing('CFG.txt'))

"""
Return Example:
{
    'terminals': [Terminal t1, Terminal t2, ...],
    'non_terminals': [NonTerminal n1, NonTerminal t2, ...],
    'productions': {
        'STATEMENT_LIST': [Node n1, Node n2],
        'METHOD_BODY': [Node n3]
    },
    'first_production': String
}
"""