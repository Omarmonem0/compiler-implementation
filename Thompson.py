from copy import deepcopy

operators_list = ['|', '.', '*', ')', '(', '+']

class State:

    def __init__(self, number):
        self.data = {
            'name': number,
            'trans': {}
        }

    def __str__(self):
        # return 'State#{} trans({}): {}'.format(self.data['name'], len(self.data['trans'].keys()), self.data['trans'])
        return str(self.data['name'])

    def __repr__(self):
        # return 'State#{} trans({}): {}'.format(self.data['name'], len(self.data['trans'].keys()), self.data['trans'])
        return str(self.data['name'])


class Nfa:

    count = 0

    def __init__(self, character):
        self.name = ''
        self.states = []
        self.start_state = None
        self.final_states = []
        if character is not None:
            self.make_character_nfa(character)

    def __str__(self):
        # return 'NFA states({}): {}'.format(len(self.states), self.states)
        return self.name

    def __repr__(self):
        # return 'NFA states({}): {}'.format(len(self.states), self.states)
        return self.name

    def make_character_nfa(self, character):
        Nfa.count += 1
        state_one = State(Nfa.count)
        Nfa.count += 1
        state_two = State(Nfa.count)
        state_one.data['trans'][character] = state_two
        self.start_state = state_one
        self.final_states.append(state_two)
        self.states.append(state_one)
        self.states.append(state_two)

    @staticmethod
    def get_name():
        Nfa.count += 1
        return Nfa.count

    @staticmethod
    def union(first_nfa, second_nfa):
        combined_nfa = Nfa(None)
        Nfa.count += 1
        new_start_state = State(Nfa.count)
        Nfa.count += 1
        new_end_state = State(Nfa.count)
        new_start_state.data['trans'] = {  # epsilon transition from
            #  the new start state to the old start states of nfa1 and nfa2
            'E': [first_nfa.start_state,  second_nfa.start_state]
        }
        for final_state in first_nfa.final_states:
            final_state.data['trans'] = {  # epsilon transition from final states to new the final state
                'E': new_end_state
            }
        for final_state in second_nfa.final_states:
            final_state.data['trans'] = {
                'E': new_end_state
            }
        combined_nfa.start_state = new_start_state  # assigning new start state
        combined_nfa.final_states.append(new_end_state)  # assigning new end state
        combined_nfa.states.append(new_start_state)  # append start and end state to states list of new  the nfa
        combined_nfa.states.append(new_end_state)
        for first_nfa_state in first_nfa.states:  # append states of first nfa to states list of the new nfa
            combined_nfa.states.append(first_nfa_state)
        for second_nfa_state in second_nfa.states:  # append states of second nfa to states list of the new nfa
            combined_nfa.states.append(second_nfa_state)
        return combined_nfa

    @staticmethod
    def concat(first_nfa, second_nfa):
        combined_nfa = Nfa(None)
        combined_nfa.start_state = first_nfa.start_state
        for first_nfa_final_state in first_nfa.final_states:  # append states of first nfa to states list of the new nfa
            first_nfa_final_state.data['trans'] = second_nfa.start_state.data['trans']
        for second_nfa_final_state in second_nfa.final_states:
            combined_nfa.final_states.append(second_nfa_final_state)
            combined_nfa.states.append(second_nfa_final_state)
        for first_nfa_state in first_nfa.states:  # append states of first nfa to states list of the new nfa
            combined_nfa.states.append(first_nfa_state)
        return combined_nfa

    @staticmethod
    def klein(nfa):  # star
        new_nfa = Nfa(None)
        Nfa.count += 1
        new_start_state = State(Nfa.count)
        Nfa.count += 1
        new_final_state = State(Nfa.count)
        new_start_state.data['trans'] = {
            'E': [new_final_state, nfa.start_state]
        }
        for final_states in nfa.final_states:
            final_states.data['trans'].update({'E': [nfa.start_state, new_final_state]})
        for nfa_state in nfa.states:  # append states of first nfa to states list of the new nfa
            new_nfa.states.append(nfa_state)
        new_nfa.start_state = new_start_state
        new_nfa.final_states.append(new_final_state)
        new_nfa.states.append(new_start_state)
        new_nfa.states.append(new_final_state)
        return new_nfa

    @staticmethod
    def plus(nfa):
        result = Nfa.concat(nfa, Nfa.klein(nfa))
        return result

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
    def compile(regex):
        operands_stack = []
        operator_stack = []
        buffer = ""
        for (index, character) in enumerate(regex):
            if character.isalnum():
                buffer += character
                if index == len(regex)-1:
                    operands_stack.append(Nfa(character))
            elif character in operators_list:
                if buffer != "":
                    operands_stack.append(Nfa(buffer))
                buffer = ""
                if character == '|':
                    operator_stack.append(character)
                elif character == '.':
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
        return operands_stack.pop()