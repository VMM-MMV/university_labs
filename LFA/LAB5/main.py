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

                if len(production) > 1 and production != production.lower():
                    self.productions[non_terminal].extend(list(getEpsilonEmptyProduction(production)))

        for non_terminal in epsilonNonTerminals:
            productions_copy = self.productions[non_terminal][:]  # Make a copy of the list
            for production_id in range(len(productions_copy)):
                if productions_copy[production_id] == "ɛ":
                    self.productions[non_terminal].pop(production_id)
                    
    def moveNonTerminals(self):
        for non_terminal, productions in self.productions.items():
            for production_id in range(len(productions)):
                production = productions[production_id]
                if len(production) == 1 and production != production.lower():
                    productions.pop(production_id)
                    productions.extend(self.productions[production])
                    self.moveNonTerminals()
            
    class Iterator():
            def __init__(self, data, iterr=0):
                self.data = data
                self.iter = iterr
            
            def __iter__(self):
                return self
            
            def __next__(self):
                if self.iter < len(self.data):
                    self.iter += 1
                    return self.data[self.iter]
                else: 
                    raise IndexError("Iterator Out Of Bounds.")
            
            def reset(self):
                self.iter = 0

    def replaceTerminals(self):
        data = ['Б', 'Г', 'Д', 'Є', 'Ж', 'Ꙃ', 'Ꙁ', 'И', 'Л', 'П', 'Ꙋ', 'Ф', 'Ѡ', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'ЪІ']
        iterator = self.Iterator(data)
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

    def groupSelfLiterals(self):
        data = ['Ѣ', 'Ҍ', 'Ꙗ', 'Ѥ', 'Ю', 'Ѫ', 'Ѭ', 'Ѧ', 'Ѩ', 'Ѯ', 'Ѱ', 'Ѳ', 'Ҁ']
        iterator = self.Iterator(data)
        new_non_terminals = {}

        for non_terminal, productions in self.productions.items():
            for production_id in range(len(productions)):
                production = list(productions[production_id])
                if len(production) > 2:
                    for item_id in range(0, len(production), 2):
                        if item_id + 1 < len(production):
                            item = production[item_id] + production[item_id+1]
                            if new_non_terminals.get(item) == None:
                                new_non_terminal = next(iterator)
                                new_non_terminals[item] = new_non_terminal
                            production.pop(item_id+1)
                            production[item_id] = new_non_terminals[item]
                    productions[production_id] = "".join(production)

        for productions, non_terminal in new_non_terminals.items():
            self.productions[non_terminal] = [productions]

    def printConvertWithoutCyrillic(self):
        character_value_dict = {'Ѣ': 'N1', 'Ҍ': 'N2', 'Ꙗ': 'N3', 'Ѥ': 'N4', 'Ю': 'N5', 'Ѫ': 'N6', 'Ѭ': 'N7', 'Ѧ': 'N8', 'Ѩ': 'N9', 'Ѯ': 'N10', 'Ѱ': 'N11', 'Ѳ': 'N12', 'Ҁ': 'N13', 'Б': 'N14', 'Г': 'N15', 'Д': 'N16', 'Є': 'N17', 'Ж': 'N18', 'Ꙃ': 'N19', 'Ꙁ': 'N20', 'И': 'N21', 'Л': 'N22', 'П': 'N23', 'Ꙋ': 'N24', 'Ф': 'N25', 'Ѡ': 'N26', 'Ц': 'N27', 'Ч': 'N28', 'Ш': 'N29', 'Щ': 'N30', 'Ъ': 'N31', 'ЪІ': 'N32'}

        def convert_symbol(symbol):
            return character_value_dict.get(symbol, symbol)

        def convert_production(production):
            return ''.join([convert_symbol(symbol) for symbol in production])

        def print_productions(productions):
            print()
            for non_terminal, prod_list in productions.items():
                converted_productions = [convert_production(prod) for prod in prod_list]
                print(f"{convert_symbol(non_terminal)}: {[convert_production(prod) for prod in prod_list]}")
            print()

        print_productions(self.productions)


    def transformToCNF(self):
        self.removeEmptyStates()
        self.printProductions()
        self.moveNonTerminals()
        self.printProductions()
        self.replaceTerminals()
        self.printProductions()
        self.groupSelfLiterals()
        self.printProductions()
        self.addFirstState()
        self.printProductions()

def main():
    grammar = """
    S → B
    A → aX
    A → bx
    X → ɛ
    X → BX
    X → b
    B → AXaD
    D → aD
    D → a
    C → Ca
    """

    # grammar = """
    # S → AB
    # S → C
    # A → 0A1
    # A → ɛ
    # B → 2B3
    # B → ɛ
    # C → 0C3
    # C → D
    # C → ɛ
    # D → 1D2
    # D → ɛ
    # """
    grammar = Grammar(grammar)
    grammar.printProductions()
    grammar.transformToCNF()
    grammar.printConvertWithoutCyrillic()

if __name__ == "__main__":
    main()  

