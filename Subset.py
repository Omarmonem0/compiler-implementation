import Thompson
import copy


class DfaState:
    def __init__(self, nfa_states):
        self.nfa_state = copy.deepcopy(nfa_states)


class Subset:
    @staticmethod
    def epsilon_closures(states):
        e_closure = []
        e_closure = copy.deepcopy(states)
        stack = []
        for state in states:
            stack.append(state)
        while not not stack:
            state = stack.pop()
            for key in state.data['trans']:
                if key is 'E':
                    if isinstance(state.data['trans'][key], list):
                        for epsilons in state.data['trans'][key]:
                            if epsilons not in e_closure:
                                e_closure.append(epsilons)
                                stack.append(epsilons)
                    else:
                        if state.data['trans']['E'] not in e_closure:
                            e_closure.append(state.data['trans']['E'])
                            stack.append(state.data['trans']['E'])

        return e_closure

    @staticmethod
    def display_states(states):
        for state in states:
            print('state: ', state.data['name'])

    @staticmethod
    def move(nfa_states, symbol):
        returned_states = []
        for state in nfa_states:
            if symbol in state.data['trans']:
                if isinstance(state.data['trans'][symbol], list):
                    for item in state.data['trans'][symbol]:
                        returned_states.append(item)
                else:
                    returned_states.append(state.data['trans'][symbol])
        return returned_states

    @staticmethod
    def nfa_to_dfa(nfa):
        Dstates = []
        temporary_states = []
        Dtran = []
        unmarked_states = []
        input_symbols = nfa.input_symbols()
        new_state = DfaState(Subset.epsilon_closures([nfa.start_state]))
        Dstates.append(new_state)
        for state in Subset.epsilon_closures([nfa.start_state]):
            unmarked_states.append(state)
        for symbol in input_symbols:
            for unmarked in unmarked_states:
                unmarked_states.remove(unmarked)
                temporary_states.append(Subset.epsilon_closures(Subset.move([unmarked], symbol)))
            for state in temporary_states:
                unmarked_states.append(state)
        Dstates.append(DfaState(temporary_states))


nfa1 = Thompson.Nfa('a')
nfa2 = Thompson.Nfa('b')
nfa3 = Thompson.Nfa.union(nfa1, nfa2)
Subset.nfa_to_dfa(nfa3)
