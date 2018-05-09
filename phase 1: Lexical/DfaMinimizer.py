import Thompson,Subset

def minimize_dfa(dfa):
    """this function takes a transition table of a dfa and minimizes the number of states (if available)
        by comparing the equivalences of each set and if no change occurs then the dfa is minimized"""
    large_minimized = []
    final_states_zero = []
    normal_states_zero = []
    past_equivalence = []
    for i in dfa.Dstates:
        if not i.is_accept:
            normal_states_zero.append(i)
        else:
            final_states_zero.append(i)
    past_equivalence.append(normal_states_zero)
    past_equivalence.append(final_states_zero)
    unchanged = False
    large_minimized.append([normal_states_zero[0]])
    large_minimized.append([final_states_zero[0]])

    while not unchanged:
        for state in dfa.Dstates:
            checker = False
            if inlist(large_minimized,state):
                continue
            for trans_input in range(len(large_minimized)):
                for input in range(len(dfa.Dstates[0]['trans'])):
                    if not (findItem(past_equivalence, state['trans'][input])[0] ==
                            findItem(past_equivalence, large_minimized[trans_input][0]['trans'][input])[0]):
                        checker = True
                if not checker:
                    large_minimized[trans_input].append(state)
                    break
            large_minimized.append([state])
        if(past_equivalence == large_minimized):
            break
        past_equivalence = large_minimized
        large_minimized[:] = []

    new_names = []
    for i in large_minimized:
        for j in i:
            new_names.append(''.join(j))

    for i in large_minimized:
        for j in i:
            for index in dfa.Dstates:
                index['trans'][j] = new_names[findItem(large_minimized,j)[0]]

    for i in large_minimized:
        for j in i:
            if j == 0:
                continue
            dfa.Dstates.remove(j)

    for i in large_minimized:
        for j in i:
            for index in dfa.Dstates:
                if index in j:
                    index['name'] = new_names[findItem(large_minimized,j)[0]]
    return large_minimized


def inlist(input_list,state):
    for i in input_list:
        if state in i:
            return True
    return False


def findItem(theList, item):
   return [(ind) for ind in range(len(theList)) if item in theList[ind]]