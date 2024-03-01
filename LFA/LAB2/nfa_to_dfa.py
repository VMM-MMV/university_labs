from VisAutomaton import AutomatonVisualizer
from automaton_to_grammar import *


class NFAConvertor(): 
    def __init__(self, initial_state, final_states, transitions, states, alphabet):
        self.alphabet = alphabet
        self.final_states = final_states
        self.initial_state = "".join(initial_state)
        self.Q = states
        self.mapped_states = generate_mapping(self.Q)

        grammar = get_visual_grammar(transitions, self.Q)
        self.parsed_grammar = parseGrammar(grammar)

    def print_transition_table(self, transition_table):
        print("")
        print("      ".join(["δ"] + self.alphabet))
        for key, val in transition_table.items():
            a,b,c = val
            print(key, a, b, c)


    def get_transition_table(self):
        transition_table = {}
        for state in self.Q:
            mapped_state = self.mapped_states[state]
            mapped_transitions = self.parsed_grammar[mapped_state]
            transition_table.setdefault(mapped_state, [])
            # print(mapped_transitions)
            for terminal in self.alphabet:
                # print(terminal, [list(x)[-1] for x in mapped_transitions if terminal in x])
                transition_table[mapped_state].append(set((list(x)[-1] for x in mapped_transitions if terminal in x)))

        return transition_table


    def get_prime_transition_table(self, transition_table):
        new_Q = set()
        prime_transition_table = {}

        def nfa_to_dfa(state):
            terminals = [set()] * len(self.alphabet)
            for part_of_state in state:
                for non_terminal_id in range(len(self.alphabet)):
                    terminals[non_terminal_id] = terminals[non_terminal_id] | transition_table[part_of_state][non_terminal_id]
            
            prime_transition_table[state] = ["".join(x) for x in terminals]

            for terminal in terminals:
                hashable_terminal = "".join(terminal)
                if hashable_terminal not in new_Q and len(terminal) >= 1:
                    new_Q.add(hashable_terminal)
                    nfa_to_dfa(hashable_terminal)

        nfa_to_dfa(self.mapped_states[self.initial_state])
        return prime_transition_table


    def get_grammar_and_final_states(self, prime_transition_table, final_states):
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


    def map_final_states(self):
        final_states = list(self.final_states)
        for state_id in range(len(final_states)):
            final_states[state_id] = self.mapped_states[final_states[state_id]]
        return final_states


    def unmap_grammar_and_final_states(self, dfa_grammar, final_states):
        for state_id in range(len(final_states)):
            final_states[state_id] = unmap_grammar(self.mapped_states, final_states[state_id])

        dfa_grammar = unmap_grammar(self.mapped_states, dfa_grammar)
        return dfa_grammar, final_states


    def nfa_to_dfa(self):
        transition_table = self.get_transition_table()

        self.print_transition_table(transition_table)

        prime_transition_table = self.get_prime_transition_table(transition_table)

        final_states = self.map_final_states()

        dfa_grammar, final_states = self.get_grammar_and_final_states(prime_transition_table, final_states)

        dfa_grammar, final_states = self.unmap_grammar_and_final_states(dfa_grammar, final_states)

        visualizer = AutomatonVisualizer(dfa_grammar)

        visualizer.setStartSybol(self.initial_state)
        visualizer.addEndSymbols(final_states)

        visualizer.generateGraph()

# transitions = """
# δ(q0,a) = q0,
# δ(q0,a) = q1,
# δ(q1,a) = q1,
# δ(q1,c) = q2,
# δ(q1,b) = q3,
# δ(q0,b) = q2,
# δ(q2,b) = q3."""

# Q = ["q0","q1","q2","q3"]
# Sigma = ["a","b","c"]
# F = {"q3"}
Q0 = {"q0"}

Q = ["q0","q1","q2","q3"]
Sigma = ["a","b","c"]
F = {"q3"}
transitions = """
δ(q0,a) = q0,
δ(q0,a) = q1,
δ(q1,b) = q2,
δ(q2,c) = q3,
δ(q3,c) = q3,
δ(q2,a) = q2."""


nFAConvertor = NFAConvertor(Q0, F, transitions, Q, Sigma)

nFAConvertor.nfa_to_dfa()