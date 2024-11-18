from nfa_to_dfa import *


prime_transition_table = get_prime_transition_table("A", transition_table)

dfa_grammar, final_states = get_grammar_and_final_states(prime_transition_table, "D")

mapping = generate_mapping(Q)
for state_id in range(len(final_states)):
    final_states[state_id] = unmap_grammar(mapping, final_states[state_id])

from VisAutomaton import AutomatonVisualizer
start_symbol = "q0"

dfa_grammar = unmap_grammar(mapping, dfa_grammar)
print(dfa_grammar, final_states)

visualizer = AutomatonVisualizer(dfa_grammar)

visualizer.setStartSybol(start_symbol)
visualizer.addEndSymbols(final_states)

visualizer.generateGraph()
# print("")
# print(new_Q)