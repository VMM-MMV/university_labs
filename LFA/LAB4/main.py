string1 = "(S|T)(U|V)w*y+24"
string2 = "L(M|N)D^3p*Q(2|3)"
string3 = "R*S(T|U|V)w(x|y|z)^2"

change_string = string1
grammar = ""
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

class RegexGrammar():
    def __init__(self, string):
        self.string = string
        self.data = ['Б', 'Г', 'Д', 'Є', 'Ж', 'Ꙃ', 'Ꙁ', 'И', 'Л', 'П', 'Ꙋ', 'Ф', 'Ѡ', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'ЪІ']
        self.iterator = Iterator(self.data)
        self.current_non_terminal = next(self.iterator)
        self.coursor = 0
        self.grammar = ""

    def add_state(self):
        new_non_terminal = next(self.iterator)
        self.grammar += "\n" + self.current_non_terminal + " → " + new_non_terminal
        self.current_non_terminal = new_non_terminal
        self.grammar += "\n" + self.current_non_terminal + " → "

    def handleParanthesis(self):
        while self.string[self.coursor] != ")":
            if self.string[self.coursor] == "|":
                self.grammar += "\n" + self.current_non_terminal + " → "
                self.coursor += 1
            self.grammar += self.string[self.coursor]
            self.coursor += 1
                

    def handleGrammar(self):
        while self.coursor != len(self.string):
            if self.string[self.coursor] == "(":
                self.add_state()
                self.coursor += 1
                self.handleParanthesis()
            self.coursor += 1
        print(self.grammar)        

regex = RegexGrammar(string3)

regex.handleGrammar()


                

        