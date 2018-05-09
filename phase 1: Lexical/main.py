import LexicalRulesParser
import Thompson
import Subset
import LexicalAnalyzer

rules = LexicalRulesParser.start_parsing('inputs/lexical.txt')

nfas = Thompson.Nfa.compile(rules)

dfas = []

for nfa in nfas:
    dfas.append(Subset.Subset.nfa_to_dfa(nfa))

# for dfa in dfas:
#     print('DFA: {}'.format(dfa.name))
#     for dfaState in dfa.Dstates:
#         print('({})'.format(dfaState.name) if dfaState.is_accept else '{}'.format(dfaState.name))
#         for symb in dfaState.trans:
#             print('{} => {} | '.format(symb, dfaState.trans[symb]), end='')
#         print('\n')
#     print('\n\n')


lexical_analyzer = LexicalAnalyzer.LexicalAnalyzer(dfas, rules['priorities'])

print(lexical_analyzer.parse_code('inputs/program.txt'))
