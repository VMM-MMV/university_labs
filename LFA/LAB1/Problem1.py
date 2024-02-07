from collections import defaultdict

def parse_grammar(grammar):
    productions = defaultdict(list)
    for line in grammar.split('\n'):
        if line.strip():
            non_terminal, production = line.split('→')
            productions[non_terminal.strip()].append(production.strip())

    return productions
    
def getStrings(grammar):
    parsed_grammar = parse_grammar(grammar)
    result_strs = set()
    size = 5
    def iter(grammar_str, result_str, visited, NT):
        if len(result_strs) == size:
            return
        
        for chars in grammar_str:
            for char in chars:
                # print("c", char)
                if parsed_grammar.get(char):
                    visited.setdefault(char, -1)
                    visited[char] += 1
                    if visited[char] < 2: 
                        iter(parsed_grammar[char], result_str.copy(), visited.copy(), char)
                    result_str.pop()
                else:
                    result_str.append(char)
                # print("r", result_str)
        if len(result_strs) == size:
            return
        if NT == "C":
            result_strs.add("".join(result_str))
            
    iter(parsed_grammar["S"], [], {}, "S")
    return result_strs

def main():
    grammar = """
    S → aA
    A → bS
    A → aB
    B → bC
    C → aA
    B → aB
    C → b
    """
    
    parsed_grammar = parse_grammar(grammar)
    for non_terminal, productions in parsed_grammar.items():
        print(f"{non_terminal}: {productions}")
        
    allStrings = getStrings(grammar)
    print(allStrings)

if __name__ == "__main__":
    main()