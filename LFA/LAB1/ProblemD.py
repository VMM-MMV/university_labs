from ProblemB import Grammar
class FiniteAutomaton:
    def __init__(self, grammar):
        cGrammar = Grammar(grammar)
        self.parsed_grammar = cGrammar.parseGrammar(grammar)
        self.start_symbol = "Add a start symbol"
        self.end_symbols = []

    def addEndSymbols(self, end_symbol):
        if isinstance(end_symbol, list):
            self.end_symbols.extend(end_symbol)
        else:
            self.end_symbols.append(end_symbol)

    def setStartSybol(self, start_symbol):
        self.start_symbol = start_symbol

    def checkStr(self, check_str):        
        def iter(grammar_str, i, path_str, NT):
            if i > len(check_str) - 1:
                return path_str == check_str
            
            for chars in grammar_str:
                if len(chars) == 1:
                    if chars == check_str[i]:
                        return iter(self.parsed_grammar[NT], i + 1, path_str + chars, NT)
                else:
                    if chars[0] == check_str[i]:
                        if iter(self.parsed_grammar[chars[1]], i + 1, path_str + chars[0], chars[1]):
                            return True
            return False
        
        return iter(self.parsed_grammar[self.start_symbol], 0, "", self.start_symbol)