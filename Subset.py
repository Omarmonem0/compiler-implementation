import Thompson
import copy


def increment_char(c):
    """
    Increment an uppercase character, returning 'A' if 'Z' is given
    """
    return chr(ord(c) + 1) if c != 'Z' else 'A'


def increment_str(s):
    left_char = s.rstrip('Z')
    if not left_char:  # s contains only 'Z'
        new_s = 'A' * (len(s) + 1)
    else:
        num_replacements = len(s) - len(left_char)
        new_s = left_char[:-1] + increment_char(left_char[-1])
        new_s += 'A' * num_replacements
    return new_s


def get_name():
    DfaState.last_name += 1
    return str(DfaState.last_name)


class DfaState:
    last_name = 0

    def __init__(self, nfa_states, name):
        self.states = copy.deepcopy(nfa_states)
        self.marked = None
        self.name = name
        self.trans = {}

    def __str__(self):
        return 'name: {}, states: {}, trans: {}'.format(self.name, self.states, self.trans)


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
    def check_equal_nfas(first_list, second_list):
        for state1 in first_list:
            if state1 not in second_list:
                return False
        return True

    @staticmethod
    def nfa_to_dfa(nfa):
        Dstates = []
        temporary_states = []
        Dtran = []
        input_symbols = nfa.input_symbols()
        new_start_state = DfaState(Subset.epsilon_closures([nfa.start_state]), get_name())
        new_start_state.marked = False
        Dstates.append(new_start_state)
        unmarked_states = [state for state in Dstates if not state.marked]
        while len(unmarked_states) > 0:
            current_dfa_state = unmarked_states[0]
            current_dfa_state.marked = True
            for symbol in input_symbols:
                temp_nfa_states = Subset.epsilon_closures(Subset.move(current_dfa_state.states, symbol))
                if len(temp_nfa_states) > 0:
                    already_existed = False
                    for dfa in Dstates:
                        if Subset.check_equal_nfas(dfa.states, temp_nfa_states):
                            already_existed = True
                            current_dfa_state.trans[symbol] = dfa
                            break
                    if not already_existed:
                        new_state = DfaState(temp_nfa_states, get_name())
                        current_dfa_state.trans[symbol] = new_state
                        new_state.marked = False
                        Dstates.append(new_state)
            unmarked_states = [state for state in Dstates if not state.marked]
        return Dstates



        # for symbol in input_symbols:
        #     for unmarked in unmarked_states:
        #         unmarked_states.remove(unmarked)
        #         temporary_states.append(Subset.epsilon_closures(Subset.move([unmarked], symbol)))
        #     for state in temporary_states:
        #         unmarked_states.append(state)
        # Dstates.append(DfaState(temporary_states))


# nfa1 = Thompson.Nfa('a')
# nfa2 = Thompson.Nfa('b')
# nfa3 = Thompson.Nfa.union(nfa1, nfa2)
# Subset.nfa_to_dfa(nfa3)

W = Thompson.State('W')
X = Thompson.State('X')
Y = Thompson.State('Y')
Z = Thompson.State('Z')
E = Thompson.State('e')
F = Thompson.State('f')

W.data['trans']['a'] = X
W.data['trans']['b'] = Y
X.data['trans']['d'] = Z
Y.data['trans']['c'] = Z

nfa = Thompson.Nfa(None)
nfa.name = 'hoppa'
nfa.states = [W, X, Y, Z]
nfa.start_state = W
nfa.final_states = [Z]

result = Subset.nfa_to_dfa(nfa)

for s in result:
    print(s)
