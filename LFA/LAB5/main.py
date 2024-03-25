from collections import defaultdict

class Grammar:
    def __init__(self, grammar):
        self.productions = self.getProductions(grammar)
        self.start_symbol = "Add a start symbol"
        self.end_symbols = []
    
    def getProductions(self, grammar):
        productions = defaultdict(list)
        for line in grammar.split('\n'):
            if line.strip():
                non_terminal, production = line.split('→')
                productions[non_terminal.strip()].append(production.strip())

        return productions
    
    def printProductions(self):
        for non_terminal, productions in self.productions.items():
            print(f"{non_terminal}: {productions}")

    def addFirstState(self):
        self.productions["S0"] = ["S", "ɛ"]
    
    def removeEmptyStates(self):
        def backtrack(non_terminal, productions):
            if len(productions) == 1:
                return

            for i in range()
        for non_terminal, productions in self.productions.items():
            print(f"{non_terminal}: {productions}")

    def transformToCNF(self):
        self.addFirstState()

def main():
    grammar = """
    # S → B
    # A → aX
    # A → bx
    # X → ɛ
    # X → BX
    # X → b
    # B → AXaD
    # D → aD
    # D → a
    # C → Ca
    # """

    grammar = """
    S → AB
    S → C
    A → 0A1
    A → ɛ
    B → 2B3
    B → ɛ
    C → 0C3
    C → D
    C → ɛ
    D → 1D2
    D → ɛ
    """
    grammar = Grammar(grammar)
    # grammar.printProductions()
    # print()
    grammar.transformToCNF()
    grammar.printProductions()

if __name__ == "__main__":
    main()  

