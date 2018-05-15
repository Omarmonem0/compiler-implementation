def create_parse_table(first:dict, follow:dict, productions : dict, terminal: list, non_terminal:list):
    parsed_table = {}
    for t in non_terminal:
        parsed_table.update({t.value : {}})
    for (key, value) in parsed_table.items():
        for t in terminal:
            parsed_table[key][t.value] = None
    for nt, prod_list in productions.items():
        # nodes = {}
        for x in productions[nt]:
            if x.type == 'T':
                parsed_table[nt][x.value] = x
            elif x.type == 'N':
                first_elements = first[nt]
                for t in first_elements:
                    parsed_table[nt][t.value] = x

    # fill with synch
    for non_terminal_string, terminal_list in follow.items():
        for T in terminal_list:
            if not parsed_table[non_terminal_string].get(T.value) and T.value != '$':
                parsed_table[non_terminal_string][T.value] = 'synch'
    print(parsed_table)
    return parsed_table
