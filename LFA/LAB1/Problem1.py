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
                    visited.setdefault(char, 0)
                    visited[char] += 1
                    if visited[char] < 3: 
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

def checkStr(grammar, check_str):
    parsed_grammar = parse_grammar(grammar)
    
    def iter(grammar_str, i, path_str, NT):
        if i > len(check_str) - 1:
            return path_str == check_str
        
        for chars in grammar_str:
            if len(chars) == 1:
                if chars == check_str[i]:
                    return iter(parsed_grammar[NT], i + 1, path_str + chars, NT)
            else:
                if chars[0] == check_str[i]:
                    if iter(parsed_grammar[chars[1]], i + 1, path_str + chars[0], chars[1]):
                        return True
        return False
    
    return iter(parsed_grammar["S"], 0, "", "S")

def printGrammarSet(grammar):
    parsed_grammar = parse_grammar(grammar)
    for non_terminal, productions in parsed_grammar.items():
        print(f"{non_terminal}: {productions}")

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
    printGrammarSet(grammar)
    allStrings = getStrings(grammar)
    print(allStrings)
    print(checkStr(grammar, "aabb"))

{'abaaabb', 'aaabb', 'aabaabb', 'abaabb', 'aabb'}

if __name__ == "__main__":
    main()