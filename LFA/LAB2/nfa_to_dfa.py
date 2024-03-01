from automaton_to_grammar import *
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

grammar = get_visual_grammar(transitions, Q)
parsed_grammar = parseGrammar(grammar)
mapped_states = generate_mapping(Q)
transition_table = {}

for state in Q:
    mapped_state = mapped_states[state]
    mapped_transitions = parsed_grammar[mapped_state]
    transition_table.setdefault(mapped_state, [])
    # print(mapped_transitions)
    for terminal in Sigma:
        print(terminal, [list(x)[-1] for x in mapped_transitions if terminal in x])
        transition_table[mapped_state].append([list(x)[-1] for x in mapped_transitions if terminal in x])

print("")
print("      ".join(["δ"] + Sigma))
for key, val in transition_table.items():
    print(key, val)



