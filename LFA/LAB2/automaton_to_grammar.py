from collections import defaultdict


def generate_mapping(elements):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    mapping = {}

    for i in range(len(elements)):
        mapping[elements[i]] = alphabet[i]

    return mapping


def get_visual_grammar(transitions, states):
    mapping = generate_mapping(states)
    replaced_transitions = transitions
    for key, value in mapping.items():
        replaced_transitions = replaced_transitions.replace(key, value)

    replaced_transitions = replaced_transitions.replace(",\n","\n").replace(".", "").replace("δ(", "").replace(")", "").replace(" = ", "").replace(" ","")
    replaced_transitions = replaced_transitions.replace(",", " → ")
    return replaced_transitions


def parseGrammar(grammar):
    productions = defaultdict(list)
    for line in grammar.split('\n'):
        if line.strip():
            non_terminal, production = line.split('→')
            productions[non_terminal.strip()].append(production.strip())

    return productions


def isRepeating(parsed_grammar):
    for key, vals in parsed_grammar.items():
        terminals = [y for x in vals for y in x if y == y.lower()]
        terminals_set = set(terminals)
        print(terminals)
        print(terminals_set)
        if len(terminals) != len(terminals_set):
            return True
    return False



# TODO add epsilon to final state, change back to original signs

if __name__ == "__main__":
    transitions = """
                δ(q0,a) = q0,
                δ(q0,a) = q1,
                δ(q1,a) = q1,
                δ(q1,c) = q2,
                δ(q1,b) = q3,
                δ(q0,b) = q2,
                δ(q2,b) = q3."""

    Q = ["q0","q1","q2","q3"]
    grammar = get_visual_grammar(transitions, Q)
    parsed_grammar = parseGrammar(grammar)
    print(grammar)
    print(isRepeating(parsed_grammar))