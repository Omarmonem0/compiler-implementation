import LexicalRulesParser
import Thompson
import Subset
import LexicalAnalyzer

rules = LexicalRulesParser.start_parsing('inputs/lexical-rules.txt')

nfas = Thompson.Nfa.compile(rules)

dfas = []

for nfa in nfas:
    dfas.append(Subset.Subset.nfa_to_dfa(nfa))

lexical_analyzer = LexicalAnalyzer.LexicalAnalyzer(dfas, rules['priorities'])

print(lexical_analyzer.parse_code('inputs/code.java'))
