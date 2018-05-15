import InputParser
import FirstAndFollow
import Parser
import ParsingTable

rules = InputParser.start_parsing("CFG.txt")
first_and_follow = FirstAndFollow.first_follow(rules['productions'], rules['non_terminals'], rules['first_production'])
first_production = rules['first_production']
first = first_and_follow['FIRST']
follow = first_and_follow['FOLLOW']
productions = rules['productions']
terminal = rules['terminals']
non_terminal = rules['non_terminals']

parsing_table = ParsingTable.create_parse_table(first, follow, productions, terminal, non_terminal)
print(parsing_table)
Parser.start_parsing('input-program.txt', parsing_table, first_production)
