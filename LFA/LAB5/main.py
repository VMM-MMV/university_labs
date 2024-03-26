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
        print()
        for non_terminal, productions in self.productions.items():
            print(f"{non_terminal}: {productions}")
        print()

    def addFirstState(self):
        self.productions["S0"] = ["S", "ɛ"]
                

    def removeEmptyStates(self):
        def getAllEpsilonNonTerminals():
            epsilonNonTerminals = set()
            def dfs(bad_value="ɛ"):
                for non_terminal in self.productions.keys():
                    if non_terminal not in epsilonNonTerminals:
                        for productions in self.productions[non_terminal]:
                            if bad_value in list(productions):
                                epsilonNonTerminals.add(non_terminal)
                                dfs(non_terminal)
            dfs()
            return epsilonNonTerminals
    
        def getEpsilonEmptyProduction(productions):
            res = set()
            def dfs(ignore=set()):
                if len(productions) == 1:
                    return
                
                curr = ""
                for part_id in range(len(productions)):
                    str_part_id = str(part_id)
                    if str_part_id not in ignore:
                        part = productions[part_id]
                        curr += part
                        if part.isalpha() and part == part.upper():
                            dfs(ignore | set(str_part_id))

                if curr not in ["", productions]: 
                    res.add(curr)

            dfs()
            return res
        
        epsilonNonTerminals = getAllEpsilonNonTerminals()
        for non_terminal in epsilonNonTerminals:
            for production_id in range(len(self.productions[non_terminal])):
                production = self.productions[non_terminal][production_id]

                if production == "ɛ":
                    self.productions[non_terminal].pop(production_id)
                    continue

                if len(production) > 1 and production != production.lower():
                    self.productions[non_terminal].extend(list(getEpsilonEmptyProduction(production)))
                    
    def moveNonTerminals(self):
        for non_terminal, productions in self.productions.items():
            for production_id in range(len(productions)):
                production = productions[production_id]
                if len(production) == 1 and production != production.lower():
                    productions.pop(production_id)
                    productions.extend(self.productions[production])
                    self.moveNonTerminals()
            
    def replaceTerminals(self):
        class CyrillicIterator():
            def __init__(self):
                self.cyrillic_alphabet_kinda = [
                    'Б', 'Г', 'Д', 'Є', 'Ж', 'Ꙃ', 'Ꙁ', 'И', 'Л', 'П', 'Ꙋ', 'Ф',
                    'Ѡ', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'ЪІ', 'Ѣ', 'Ҍ', 'Ꙗ', 'Ѥ', 'Ю', 'Ѫ', 'Ѭ', 'Ѧ', 'Ѩ', 'Ѯ', 'Ѱ', 'Ѳ', 'Ҁ'
                ]
                self.iter = 0
            
            def __iter__(self):
                return self
            
            def __next__(self):
                if self.iter < len(self.cyrillic_alphabet_kinda):
                    self.iter += 1
                    return self.cyrillic_alphabet_kinda[self.iter]
                else: 
                    raise IndexError("Iterator Out Of Bounds.")
            
            def reset(self):
                self.iter = 0

        iterator = CyrillicIterator()
        new_non_terminals = {}

        for non_terminal, productions in self.productions.items():
            for production_id in range(len(productions)):
                production = list(productions[production_id])
                for item_id in range(len(production)):
                    item = production[item_id]
                    if item == item.lower():
                        if new_non_terminals.get(item) == None:
                            new_non_terminal = next(iterator)
                            new_non_terminals[item] = new_non_terminal
                        production[item_id] = new_non_terminals[item]
                productions[production_id] = "".join(production)

        for productions, non_terminal in new_non_terminals.items():
            self.productions[non_terminal] = [productions]              
                        
    def transformToCNF(self):
        # self.addFirstState()
        self.removeEmptyStates()
        self.printProductions()
        self.moveNonTerminals()
        self.replaceTerminals()

def main():
    # grammar = """
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
    grammar.printProductions()
    # print()
    grammar.transformToCNF()
    grammar.printProductions()

if __name__ == "__main__":
    main()  

