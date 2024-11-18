from RegexGrammar import *
from Grammar import *
string1 = "(S|T|A)+(U|V)w*y+24"
string2 = "L(M|N)D^3p*Q(2|3)"
string3 = "R*S(T|U|V)w(x|y|z)^2"
regex = RegexGrammar(string1)
grammar = regex.handleGrammar()
mappings = regex.mappedReplacements
start_symbol = regex.start_symbol
end_symbols = [regex.end_symbol]
cGrammar = Grammar(grammar)
cGrammar.setStartSybol(start_symbol)
cGrammar.addEndSymbols(end_symbols)

cGrammar.printGrammarSet()
allStrings = list(cGrammar.getStrings())
for string_id in range(len(allStrings)):
    string = allStrings[string_id]
    for mapping in mappings.items():
        key, value = mapping
        string = string.replace(key, value)
        allStrings[string_id] = string

print([x[:-1] for x in allStrings])