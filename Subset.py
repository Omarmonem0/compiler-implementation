import Thompson


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
    name = increment_str(DfaState.last_name)
    DfaState.last_name = name
    return name


class DfaState:
    last_name = 'A'

    def __init__(self, nfa_states, name):
        self.states = nfa_states
        self.marked = None
        self.name = name
        self.trans = {}
        self.is_accept = None

    def __str__(self):
        return 'DState#{}, trans: {}'.format(self.name, self.trans)

    def __repr__(self):
        return 'DState#{}, trans: {}'.format(self.name, self.trans)


class Dfa:

    def __init__(self, Dstates, name):
        self.Dstates = Dstates
        self.name = name

    def __str__(self):
        return 'DFA#{}'.format(self.name)

    def __repr__(self):
        return 'DFA#{} '.format(self.name)


class Subset:
    @staticmethod
    def epsilon_closures(states):
        e_closure = [state for state in states]
        stack = []
        for state in states:
            stack.append(state)
        while len(stack) > 0:
            state = stack.pop()
            if state.data['trans'].get('$'):
                if isinstance(state.data['trans']['$'], list):
                    for epsilons in state.data['trans']['$']:
                        if epsilons not in e_closure:
                            e_closure.append(epsilons)
                            stack.append(epsilons)
                else:
                    if state.data['trans']['$'] not in e_closure:
                        e_closure.append(state.data['trans']['$'])
                        stack.append(state.data['trans']['$'])

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
            found = False
            for state2 in second_list:
                if state1.data['name'] == state2.data['name']:
                    found = True
            if not found:
                return False
        return True

    @staticmethod
    def nfa_to_dfa(nfa):
        dfa = Dfa([], nfa.name)
        input_symbols = nfa.input_symbols()
        new_start_state = DfaState(Subset.epsilon_closures([nfa.start_state]), get_name())
        new_start_state.marked = False
        dfa.Dstates.append(new_start_state)
        unmarked_states = [state for state in dfa.Dstates if not state.marked]
        while len(unmarked_states) > 0:
            current_dfa_state = unmarked_states[0]
            current_dfa_state.marked = True
            for symbol in input_symbols:
                temp_nfa_states = Subset.epsilon_closures(Subset.move(current_dfa_state.states, symbol))
                if len(temp_nfa_states) > 0:
                    already_existed = False
                    for dState in dfa.Dstates:
                        if Subset.check_equal_nfas(dState.states, temp_nfa_states):
                            already_existed = True
                            current_dfa_state.trans[symbol] = dState
                            break
                    if not already_existed:
                        new_state = DfaState(temp_nfa_states, get_name())
                        current_dfa_state.trans[symbol] = new_state
                        new_state.marked = False
                        dfa.Dstates.append(new_state)
            unmarked_states = [state for state in dfa.Dstates if not state.marked]
        Subset.mark_accepted_states(dfa, nfa)
        Subset.make_dead_state(dfa, input_symbols)
        return dfa

    @staticmethod
    def mark_accepted_states(dfa, nfa):
        for Dstate in dfa.Dstates:
            for nfa_state in Dstate.states:
                for accept_state in nfa.final_states:
                    if nfa_state.data['name'] == accept_state.data['name']:
                        Dstate.is_accept = True

    @staticmethod
    def make_dead_state(dfa, input_symbols):
        dead_state = DfaState([Thompson.Nfa(None)], 'DEAD')
        dead_state.is_accept = False
        for symbol in input_symbols:
            dead_state.trans[symbol] = dead_state
        went_to_dead_state = False
        for Dstate in dfa.Dstates:
            for symbol in input_symbols:
                if not Dstate.trans.get(symbol):
                    Dstate.trans[symbol] = dead_state
                    if not went_to_dead_state:
                        went_to_dead_state = True
        if went_to_dead_state:
            dfa.Dstates.append(dead_state)


W = Thompson.State('W')
X = Thompson.State('X')
Y = Thompson.State('Y')
Z = Thompson.State('Z')
E = Thompson.State('e')
F = Thompson.State('f')

W.data['trans']['a'] = X
W.data['trans']['b'] = Y
X.data['trans']['E'] = Z
Y.data['trans']['c'] = Z
Z.data['trans']['E'] = W

nfa = Thompson.Nfa('q')
nfa.name = 'hoppa'
nfa.states = [W, X, Y, Z]
nfa.start_state = W
nfa.final_states = [Z]


nfa2 = Thompson.Nfa('a')
nfa3 = Thompson.Nfa('b')
nfa4 = Thompson.Nfa('c')


union = Thompson.Nfa.union(nfa2, nfa3)
concat = Thompson.Nfa.concat(union, nfa4)
# po = Thompson.Nfa.klein(union)
# print(union)

# print(Subset.nfa_to_dfa(concat).Dstates)
# print(Subset.epsilon_closures(Subset.move([W], 'a')))

# for s in result:
#     print(s)
