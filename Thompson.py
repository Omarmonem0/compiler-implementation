from copy import deepcopy

operators_list = ['|', '.', '*', ')', '(', '+']


class State:
    def __init__(self, number):
        self.data = {
            'name': number,
            'trans': {}
        }

class Nfa:

    count = 0

    def __init__(self, character):
        self.name = ''
        self.states = []
        self.start_state = ''
        self.final_states = []
        if character is not None:
            self.make_character_nfa(character)

    def make_character_nfa(self, character):

        Nfa.count += 1
        state_one = State(Nfa.count)
        Nfa.count += 1
        state_two = State(Nfa.count)
        state_one.data['trans'] = {
            character: state_two
        }
        self.start_state = state_one
        self.final_states.append(state_two)
        self.states.append(state_one)
        self.states.append(state_two)

    @staticmethod
    def union(first_nfa, second_nfa):
        copy_one = deepcopy(first_nfa)
        copy_two = deepcopy(second_nfa)
        combined_nfa = Nfa(None)
        Nfa.count += 1
        new_start_state = State(Nfa.count)
        Nfa.count += 1
        new_end_state = State(Nfa.count)
        new_start_state.data['trans'] = {  # epsilon transition from
            #  the new start state to the old start states of nfa1 and nfa2
            'E': [first_nfa.start_state,  second_nfa.start_state]
        }
        for final_state in copy_one.final_states:
            final_state.data['trans'] = {  # epsilon transition from final states to new the final state
                'E': new_end_state
            }
        for final_state in copy_two.final_states:
            final_state.data['trans'] = {
                'E': new_end_state
            }
        combined_nfa.start_state = new_start_state  # assigning new start state
        combined_nfa.final_states.append(new_end_state)  # assigning new end state
        combined_nfa.states.append(new_start_state)  # append start and end state to states list of new  the nfa
        combined_nfa.states.append(new_end_state)
        for first_nfa_state in copy_one.states:  # append states of first nfa to states list of the new nfa
            combined_nfa.states.append(first_nfa_state)
        for second_nfa_state in copy_two.states:  # append states of second nfa to states list of the new nfa
            combined_nfa.states.append(second_nfa_state)
        return combined_nfa

    @staticmethod
    def concat(first_nfa, second_nfa):
        copy = deepcopy(first_nfa)
        combined_nfa = Nfa(None)
        combined_nfa.start_state = copy.start_state
        for first_nfa_final_state in copy.final_states:  # append states of first nfa to states list of the new nfa
            first_nfa_final_state.data['trans'] = second_nfa.start_state.data['trans']
        for second_nfa_final_state in second_nfa.final_states:
            combined_nfa.final_states.append(second_nfa_final_state)
        for first_nfa_state in copy.states:  # append states of first nfa to states list of the new nfa
            combined_nfa.states.append(first_nfa_state)
        for second_nfa_state in second_nfa.states:
            if second_nfa_state != second_nfa.start_state:
                combined_nfa.states.append(second_nfa_state)

        return combined_nfa

    @staticmethod
    def klein(nfa):  # star
        new_nfa = Nfa(None)
        copy = deepcopy(nfa)
        Nfa.count += 1
        new_start_state = State(Nfa.count)
        Nfa.count += 1
        new_final_state = State(Nfa.count)
        new_start_state.data['trans'] = {
            'E': [new_final_state, copy.start_state]
        }
        for final_states in copy.final_states:
            final_states.data['trans'].update({'E': [copy.start_state, new_final_state]})
        for nfa_state in copy.states:  # append states of first nfa to states list of the new nfa
            new_nfa.states.append(nfa_state)
        new_nfa.start_state = new_start_state
        new_nfa.final_states.append(new_final_state)
        new_nfa.states.append(new_start_state)
        new_nfa.states.append(new_final_state)
        return new_nfa

    @staticmethod
    def plus(nfa):
        Nfa.count += 1
        new_start_state = State(Nfa.count)
        Nfa.count += 1
        new_final_state = State(Nfa.count)
        for final_states in nfa.final_states:
            final_states.data['trans'] = {
                '$': [new_final_state, nfa.start_state]
            }
        new_start_state.data['trans'] = {
            '$': nfa.start_state
        }
        nfa.start_state = new_start_state
        del nfa.final_states[:]
        nfa.final_states.append(new_final_state)
        nfa.states.append(new_start_state)
        nfa.states.append(new_final_state)
        return nfa

    @staticmethod
    def display(nfa):
        for nfa_states in nfa.states:
            print('state number: ', nfa_states.data['name'])
            for key in nfa_states.data['trans']:
                    if isinstance(nfa_states.data['trans'][key], list):
                        for trans in nfa_states.data['trans'][key]:
                            print('symbol: ', key, 'new state: ', trans.data['name'])
                    else:
                        print('symbol: ', key, 'new state: ', nfa_states.data['trans'][key].data['name'])

    @staticmethod
    def alpha(character):
        lower = 'abcdefghijklmnopqrstuvwxyz'
        upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        nfas = []
        if character is "lower":
            for c in lower:
                nfas.append(Nfa(c))

        if character is "upper":
            for c in upper:
                nfas.append(Nfa(c))

        if character is "digits":
            for c in digits:
                nfas.append(Nfa(c))

        return nfas

    def input_symbols(self):
        inputs = []
        for states in self.states:
            for trans in states.data['trans']:
                if trans in inputs or trans is 'E':
                    continue
                else:
                    inputs.append(trans)
        return inputs

    @staticmethod
    def eval_concatenated(buffer):
        new_buffer = ""
        operands_stack = []
        concat_stack = []
        for character in buffer:
            if character == " ":
                new_buffer += '.'
            else:
                new_buffer += character
        for character in new_buffer:
            if character.isalnum():
                operands_stack.append(Nfa(character))
            else:
                concat_stack.append(character)
        while concat_stack:
            operand_one = operands_stack.pop()
            concat_stack.pop()
            operand_two = operands_stack.pop()
            operands_stack.append(Nfa.concat(operand_two, operand_one))
        return operands_stack.pop()

    @staticmethod
    def compile(regex):
        nfa_name = ""
        operands_stack = []
        operator_stack = []
        buffer = ""
        backslash_flag = 0
        final_nfas = []
        for field in regex['regular_expressions']:
            nfa_name = field
            for (index, character) in enumerate(regex['regular_expressions'][field]):
                if character.isalnum():
                    if len(buffer) == 0:
                        buffer += character
                    elif len(buffer) >= 1:
                        buffer += " " + character
                    if index == len(regex['regular_expressions'][field])-1:
                        if len(buffer) == 1:
                            operands_stack.append(Nfa(buffer))
                        else:
                            operands_stack.append(Nfa.eval_concatenated(buffer))
                elif character == '\\':
                    backslash_flag = 1
                elif character == '$':
                    operands_stack.append(Nfa(character))
                elif character in operators_list:
                    if buffer != "":
                        if len(buffer) == 1:
                            operands_stack.append(Nfa(buffer))
                        else:
                            operands_stack.append(Nfa.eval_reserved(buffer))
                    buffer = ""
                    if character == '|':
                        operator_stack.append(character)
                    elif character == '.':
                        if backslash_flag == 1:
                            backslash_flag = 0
                            operands_stack.append(Nfa(character))
                        else:
                            operator_stack.append(character)

                    elif character == '(':
                        operator_stack.append(character)
                    elif character == '*':
                        operand = operands_stack.pop()
                        operands_stack.append(Nfa.klein(operand))
                    elif character == '+':
                        operand = operands_stack.pop()
                        operands_stack.append(Nfa.plus(operand))

                    elif character == ')':
                        while True:
                            temp = operator_stack.pop()
                            if temp == '(':
                                break
                            else:
                                operand_one = operands_stack.pop()
                                operand_two = operands_stack.pop()
                                if temp == '|':
                                    operands_stack.append(Nfa.union(operand_one, operand_two))
                                elif temp == '.':
                                    operands_stack.append(Nfa.concat(operand_two, operand_one))
            while operator_stack:
                temp = operator_stack.pop()
                operand_one = operands_stack.pop()
                operand_two = operands_stack.pop()
                if temp == '|':
                    operands_stack.append(Nfa.union(operand_one, operand_two))
                elif temp == '.':
                    operands_stack.append(Nfa.concat(operand_two, operand_one))
                elif character == '*':
                    operand = operands_stack.pop()
                    operands_stack.append(Nfa.klein(operand))
                elif character == '+':
                    operand = operands_stack.pop()
                    operands_stack.append(Nfa.plus(operand))

            result = operands_stack.pop()
            result.name = nfa_name
            final_nfas.append(result)

        for keyword in regex['keyword']:
            nfa_name = keyword
            keyword = " ".join(keyword)

            temp = Nfa.eval_concatenated(keyword)
            temp.name = nfa_name
            final_nfas.append(temp)

        for punctuation in regex['punctuations']:
            temp = Nfa(punctuation)
            temp.name = punctuation
            final_nfas.append(temp)

        return final_nfas


dictionary = {
    'regular_expressions': {
        'id': 'a',
        'token': 'b'
    },
    'keyword': ['while', 'if', 'else'],
    'punctuations': [';', ':', '.']
}

Nfa.compile(dictionary)