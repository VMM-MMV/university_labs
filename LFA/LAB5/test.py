# Dictionary mapping characters to values
character_value_dict = {'Ѣ': 'N1', 'Ҍ': 'N2', 'Ꙗ': 'N3', 'Ѥ': 'N4', 'Ю': 'N5', 'Ѫ': 'N6', 'Ѭ': 'N7', 'Ѧ': 'N8', 'Ѩ': 'N9', 'Ѯ': 'N10', 'Ѱ': 'N11', 'Ѳ': 'N12', 'Ҁ': 'N13', 'Б': 'N14', 'Г': 'N15', 'Д': 'N16', 'Є': 'N17', 'Ж': 'N18', 'Ꙃ': 'N19', 'Ꙁ': 'N20', 'И': 'N21', 'Л': 'N22', 'П': 'N23', 'Ꙋ': 'N24', 'Ф': 'N25', 'Ѡ': 'N26', 'Ц': 'N27', 'Ч': 'N28', 'Ш': 'N29', 'Щ': 'N30', 'Ъ': 'N31', 'ЪІ': 'N32'}

# Productions
productions = {
    'S': ['AB', 'ҌД', 'ГД', 'ꙖЄ', 'ГЄ', 'ѤД', 'ЖД', 'ЮЖ', 'ЄЖ'],
    'A': ['ꙖЄ', 'ГЄ'],
    'B': ['ѤД', 'ЖД'],
    'C': ['ҌД', 'ГД', 'ЮЖ', 'ЄЖ'],
    'D': ['ЮЖ', 'ЄЖ'],
    'Г': ['0'],
    'Д': ['3'],
    'Є': ['1'],
    'Ж': ['2'],
    'Ҍ': ['ГC'],
    'Ꙗ': ['ГA'],
    'Ѥ': ['ЖB'],
    'Ю': ['ЄD'],
    'S0': ['S', 'ɛ']
}

def convert_symbol(symbol):
    return character_value_dict.get(symbol, symbol)

def convert_production(production):
    return ''.join([convert_symbol(symbol) for symbol in production])

def printProductions(productions):
    print()
    for non_terminal, prod_list in productions.items():
        converted_productions = [convert_production(prod) for prod in prod_list]
        print(f"{convert_symbol(non_terminal)}: {[convert_production(prod) for prod in prod_list]}")
    print()

printProductions(productions)
