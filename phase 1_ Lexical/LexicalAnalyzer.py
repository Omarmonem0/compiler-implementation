class LexicalAnalyzer:

    def __init__(self, dfas, priorities):
        self.dfas = dfas
        self.priorities = priorities

    def parse_code(self, file_name):
        file = open(file_name, 'r')
        content = file.read()
        token_buffer = ''
        accepted_tokens = []
        last_accepted_tokens = []
        output = ''
        content = content.strip()
        for (index, char) in enumerate(content):
            if char == '\n':
                continue
            token_buffer += char
            accepted_tokens = self.get_accepted_tokens(token_buffer)

            if len(accepted_tokens) == 0:
                output += self.get_highest(last_accepted_tokens) + '\n'
                if char == ' ':
                    token_buffer = ''
                    last_accepted_tokens = []
                else:
                    token_buffer = char
                    last_accepted_tokens = self.get_accepted_tokens(token_buffer)
            else:
                last_accepted_tokens = accepted_tokens[:]  # copy accepted tokens
            if index == len(content) - 1:
                output += self.get_highest(last_accepted_tokens) + '\n'
        return output

    def get_accepted_tokens(self, lexeme):
        accepted = []
        for dfa in self.dfas:
            temp = dfa.Dstates[0]
            crash = False
            for char in lexeme:
                if temp.trans.get(char):
                    temp = temp.trans[char]
                else:
                    crash = True
                    break
            if temp.is_accept and not crash:
                accepted.append(dfa.name)
        return accepted

    def get_highest(self, accepted_tokens):
        max_num = 0
        max_token = ''
        for token in accepted_tokens:
            if self.priorities[token] > max_num:
                max_num = self.priorities[token]
                max_token = token
        return max_token



# lex = LexicalAnalyzer([])
# lex.parse_code('inputs/code.java')
