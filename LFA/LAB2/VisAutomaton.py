import networkx as nx
import matplotlib.pyplot as plt 
from ProblemB import Grammar

class AutomatonVisualizer:
    def __init__(self, grammar):
        cGrammar = Grammar(grammar)
        self.data = cGrammar.parseGrammar(grammar)
        self.start_symbol = "Add a start symbol"
        self.end_symbols = []
    
    def addEndSymbols(self, end_symbol):
        if isinstance(end_symbol, list):
            self.end_symbols.extend(end_symbol)
        else:
            self.end_symbols.append(end_symbol)
    
    def setStartSybol(self, start_symbol):
        self.start_symbol = start_symbol
    
    def cleanData(self, parsed_grammar):
        for non_terminal, productions in parsed_grammar.items():
            for node in productions:
                if node == node.lower():
                    parsed_grammar[non_terminal].remove(node)
        return parsed_grammar

    def generateGraph(self):
        G = nx.DiGraph()

        edge_labels = {}
        self_loop = {}
        for node, neighbors in self.data.items():
            for neighbor in neighbors:
                transition = neighbor[0]
                target_node = neighbor[1:]
                G.add_edge(node, target_node)
                if node == target_node:
                    if node in self_loop:
                        self_loop[node] += f", {transition}"
                    else:
                        self_loop[node] = transition

                if (target_node, node) in edge_labels:
                    edge_labels[(target_node, node)] += f", {transition}"
                else:
                    edge_labels[(node, target_node)] = transition

        pos = nx.spring_layout(G, k=0.5)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', arrowsize=20)

        for symbol in self.end_symbols:    
            circle_radius = 0.14
            circle_center = pos[symbol]
            circle_patch = plt.Circle(circle_center, circle_radius, color='red', fill=False)
            plt.gca().add_patch(circle_patch)

        for node, transition in self_loop.items():
            pos_labels = pos.copy()
            pos_labels[node][1] += 0.10
            nx.draw_networkx_labels(G, pos_labels, labels={node: transition}, font_color='black')


        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        pos_labels = pos.copy()
        pos_labels[self.start_symbol][0] -= 0.13
        nx.draw_networkx_labels(G, pos_labels, labels={self.start_symbol: '->'}, font_color='black', font_weight='bold')

        plt.show()

if __name__ == "__main__":
    grammar="""
    S → aA     
    A → bS    
    A → aB   
    B → bC    
    C → aA   
    B → aB     
    C → b
        """

    visualizer = AutomatonVisualizer(grammar)
    visualizer.generateGraph()
