from Node import Node
from NonTerminal import NonTerminal
from Terminal import Terminal
from FirstAndFollow import get_first
import InputParser
from FirstAndFollow import first_follow
import Parser


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
    return parsed_table
