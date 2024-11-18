from ProblemB import Grammar
from ProblemC import AutomatonVisualizer
from ProblemD import FiniteAutomaton 

# Variant 28
grammar = """
    S → aA     
    A → bS    
    A → aB   
    B → bC    
    C → aA   
    B → aB     
    C → b
    """
start_symbol = "S"
end_symbols = ["C"] # you can put multiple here, these work for different grammars

cGrammar = Grammar(grammar)
cGrammar.setStartSybol(start_symbol)
cGrammar.addEndSymbols(end_symbols)

cGrammar.printGrammarSet()
allStrings = cGrammar.getStrings()
print(allStrings)



automaton = FiniteAutomaton(grammar)
automaton.setStartSybol(start_symbol)
automaton.addEndSymbols(end_symbols)

print(automaton.checkStr("abdea")) 



visualizer = AutomatonVisualizer(grammar)

visualizer.setStartSybol(start_symbol)
visualizer.addEndSymbols(end_symbols)

visualizer.generateGraph()

