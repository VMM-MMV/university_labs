import random

class Grammar:
    def __init__(self, vn, vt, p, s):
        self.vn = vn  # A set of non-terminal symbols
        self.vt = vt  # A set of terminal symbols
        self.p = p    # A dictionary of production rules
        self.s = s    # The start symbol

    def generate_string(self):
        string = self.s
        while any(symbol in self.vn for symbol in string):
            symbol = random.choice([s for s in string if s in self.vn])
            rule = random.choice(self.p[symbol])
            string = string.replace(symbol, rule, 1)
        return string

    def to_finite_automaton(self):
        fa = FiniteAutomaton()
        fa.add_state(self.s, initial=True)

        for lhs, rhs_list in self.p.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs in self.vt:
                    fa.add_state(rhs, final=True)
                    fa.add_transition(lhs, rhs, rhs)
                elif len(rhs) == 2:
                    fa.add_state(rhs[1])
                    fa.add_transition(lhs, rhs[1], rhs[0])

        return fa


class FiniteAutomaton:
    def __init__(self):
        self.q = set()      # A set of states
        self.sigma = set()  # A set of input symbols
        self.delta = {}     # A dictionary of transition functions
        self.q0 = None      # The initial state
        self.f = set()      # A set of final states

    def add_state(self, state, initial=False, final=False):
        self.q.add(state)
        if initial:
            self.q0 = state
        if final:
            self.f.add(state)

    def add_transition(self, source, target, symbol):
        self.sigma.add(symbol)
        if source not in self.delta:
            self.delta[source] = {}
        self.delta[source][symbol] = target

    def string_belong_to_language(self, input_string):
        current_state = self.q0
        for symbol in input_string:
            if symbol not in self.sigma:
                return False
            if current_state not in self.delta:
                return False
