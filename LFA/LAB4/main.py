string1 = "(SML|T|A)+(U|V)w*y+24"
string2 = "L(M|N)D^3p*Q(2|3)"
string3 = "R*S(T|U|V)w(x|y|z)^2"


change_string = string1
grammar = ""
class Iterator():
        def __init__(self, data, iterr=0):
            self.data = data
        
        def __iter__(self):
            return self
        
        def __next__(self):
            return self.data.pop()
            # else: 
            #     raise IndexError("Iterator Out Of Bounds.")
      

class RegexGrammar():
    def __init__(self, string):
        self.string = string
        self.data = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.mappedReplacements = {}
        self.replaceString()
        self.iterator = Iterator(self.data)
        self.current_non_terminal = next(self.iterator)
        self.previous_non_terminal = ""
        self.coursor = 0
        self.grammar = ""
    
    def replaceString(self):
        power_simbol = ""
        for char_id in range(len(self.string)):
            char = self.string[char_id]
            if char.isalpha():
                self.data.remove(char.upper())  # Remove used terminals
            
            if char == char.upper() and char.isalpha():
                self.mappedReplacements[char.lower()] = char # Replace and add the terminals to a map
                self.string = self.string.replace(char, char.lower())
            
            if char.isdigit() and power_simbol != "^":
                terminal = self.data.pop().lower()
                self.mappedReplacements[terminal] = char
                list_string = list(self.string)
                list_string[char_id] = terminal
                self.string = "".join(list_string)
                    
            if not char.isalnum():
                power_simbol = char
        print(self.mappedReplacements)

    def add_state(self):
        new_non_terminal = next(self.iterator)
        self.grammar += "\n" + self.current_non_terminal + " → " + new_non_terminal
        self.current_non_terminal = new_non_terminal
        self.grammar += "\n" + self.current_non_terminal + " → "
    
    def handleLiteral(self):
        self.add_state()
        new_non_terminal = next(self.iterator)
        self.grammar += self.string[self.coursor] + new_non_terminal
        self.previous_non_terminal = self.current_non_terminal
        self.current_non_terminal = new_non_terminal
    
    def handleStar(self):
        self.grammar += "\n" + self.previous_non_terminal + " → " + self.current_non_terminal
        self.grammar += "\n" +  self.current_non_terminal + " → " + self.previous_non_terminal

    def handlePlus(self):
        self.grammar += "\n" +  self.current_non_terminal + " → " + self.previous_non_terminal

    def handleParanthesis(self):
        self.add_state()
        self.coursor += 1
        new_non_terminal = next(self.iterator)

        while self.string[self.coursor] != ")":
            if self.string[self.coursor] == "|":
                self.grammar += "\n" + self.current_non_terminal + " → "
                self.coursor += 1

            if self.coursor + 1 < len(self.string) and self.string[self.coursor+1].isalpha():
                intermediary_terminal = next(self.iterator)
                self.grammar += self.string[self.coursor] + intermediary_terminal
                self.grammar += "\n" + intermediary_terminal + " → "
            elif self.string[self.coursor-1].isalpha():
                self.grammar += self.string[self.coursor] + self.current_non_terminal
            else:
                self.grammar += self.string[self.coursor] + new_non_terminal
            self.coursor += 1

        self.previous_non_terminal = self.current_non_terminal
        self.current_non_terminal = new_non_terminal
                
    def handleGrammar(self):
        # self.replaceString()
        # self.iterator = Iterator(self.data)
        while self.coursor < len(self.string):
            if self.string[self.coursor] == "(":
                self.handleParanthesis()
            if self.string[self.coursor] == "*":
                self.handleStar()
            if self.string[self.coursor] == "+":
                self.handlePlus()
            if self.string[self.coursor].isalpha():
                self.handleLiteral()
            self.coursor += 1
        print(self.grammar)        

regex = RegexGrammar(string1)

regex.handleGrammar()


                

        