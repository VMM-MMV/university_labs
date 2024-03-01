from VisAutomaton import AutomatonVisualizer
from automaton_to_grammar import *


def print_transition_table(transition_table):
    print("")
    print("      ".join(["δ"] + Sigma))
    for key, val in transition_table.items():
        a,b,c = val
        print(key, a, b, c)


def get_transition_table(parsed_grammar, mapped_states):
    transition_table = {}
    for state in Q:
        mapped_state = mapped_states[state]
        mapped_transitions = parsed_grammar[mapped_state]
        transition_table.setdefault(mapped_state, [])
        # print(mapped_transitions)
        for terminal in Sigma:
            # print(terminal, [list(x)[-1] for x in mapped_transitions if terminal in x])
            transition_table[mapped_state].append(set((list(x)[-1] for x in mapped_transitions if terminal in x)))

    return transition_table


def get_prime_transition_table(initial_state, transition_table):
    new_Q = set()
    prime_transition_table = {}

    def nfa_to_dfa(state):
        terminals = [set()] * len(Sigma)
        for part_of_state in state:
            for non_terminal_id in range(len(Sigma)):
                terminals[non_terminal_id] = terminals[non_terminal_id] | transition_table[part_of_state][non_terminal_id]
        
        prime_transition_table[state] = ["".join(x) for x in terminals]

        for terminal in terminals:
            hashable_terminal = "".join(terminal)
            if hashable_terminal not in new_Q and len(terminal) >= 1:
                new_Q.add(hashable_terminal)
                nfa_to_dfa(hashable_terminal)

    nfa_to_dfa(initial_state)
    return prime_transition_table


def get_grammar_and_final_states(prime_transition_table, final_states):
    grammar = ""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
    new_final_states = set()
    for key, val in prime_transition_table.items():
        for state_id in range(len(val)):
            if len(val[state_id]) >= 1:
                for final_state in final_states:
                    if final_state in val[state_id]:
                        new_final_states.add(val[state_id])
                grammar += f"{key} → {alphabet[state_id]}{val[state_id]} \n"
    return grammar, list(new_final_states)


def map_final_states(final_states, mapped_states):
    final_states = list(final_states)
    for state_id in range(len(final_states)):
        final_states[state_id] = mapped_states[final_states[state_id]]
    return final_states

def unmap_grammar_and_final_states(dfa_grammar, final_states, mapped_states):
    for state_id in range(len(final_states)):
        final_states[state_id] = unmap_grammar(mapped_states, final_states[state_id])

    dfa_grammar = unmap_grammar(mapped_states, dfa_grammar)
    return dfa_grammar, final_states

def nfa_to_dfa(grammar, initial_state, final_states):
    initial_state = "".join(initial_state)
    mapped_states = generate_mapping(Q)

    transition_table = get_transition_table(grammar, mapped_states)

    # print_transition_table(transition_table)

    prime_transition_table = get_prime_transition_table(mapped_states[initial_state], transition_table)

    final_states = map_final_states(final_states, mapped_states)

    dfa_grammar, final_states = get_grammar_and_final_states(prime_transition_table, final_states)

    dfa_grammar, final_states = unmap_grammar_and_final_states(dfa_grammar, final_states, mapped_states)

    visualizer = AutomatonVisualizer(dfa_grammar)

    visualizer.setStartSybol(initial_state)
    visualizer.addEndSymbols(final_states)

    visualizer.generateGraph()

transitions = """
δ(q0,a) = q0,
δ(q0,a) = q1,
δ(q1,a) = q1,
δ(q1,c) = q2,
δ(q1,b) = q3,
δ(q0,b) = q2,
δ(q2,b) = q3."""

Q = ["q0","q1","q2","q3"]
Sigma = ["a","b","c"]
F = {"q3"}
Q0 = {"q0"}

grammar = get_visual_grammar(transitions, Q)
parsed_grammar = parseGrammar(grammar)

print(grammar, parsed_grammar)
nfa_to_dfa(parsed_grammar, Q0, F)