from copy import deepcopy


class State:
    def __init__(self, number):
        self.data = {
            'name': number,
            'trans': {}
        }


class Nfa:

    count = 0

    def __init__(self, character):
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
            character: state_two.data['name']
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
            'E': [first_nfa.start_state.data['name'],  second_nfa.start_state.data['name']]
        }
        for final_state in copy_one.final_states:
            final_state.data['trans'] = {  # epsilon transition from final states to new the final state
                'E': new_end_state.data['name']
            }
        for final_state in copy_two.final_states:
            final_state.data['trans'] = {
                'E': new_end_state.data['name']
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
            combined_nfa.states.append(second_nfa_final_state)
        for first_nfa_state in copy.states:  # append states of first nfa to states list of the new nfa
            combined_nfa.states.append(first_nfa_state)
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
            'E': [new_final_state.data['name'], copy.start_state.data['name']]
        }
        for final_states in copy.final_states:
            final_states.data.update({'E': [copy.start_state.data['name'], new_final_state.data['name']]})
        for nfa_state in copy.states:  # append states of first nfa to states list of the new nfa
            new_nfa.states.append(nfa_state)
        new_nfa.start_state = new_start_state
        new_nfa.final_states.append(new_final_state)
        new_nfa.states.append(new_start_state)
        new_nfa.states.append(new_final_state)
        return new_nfa

    @staticmethod
    def display(nfa):
        for nfa_states in nfa.states:
            print('state number: ', nfa_states.data['name'])
            for i in nfa_states.data['trans']:
               print('symbol: ', i, 'new state: ', nfa_states.data['trans'][i])
































