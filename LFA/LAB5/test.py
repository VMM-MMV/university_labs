import unittest
from main import Grammar

class TestTransformToCNF(unittest.TestCase):
    def setUp(self):
        self.grammar1 = """
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

        self.expected_cnf_grammar1 = {
            'S': ['ЮD', 'ГD', 'a', 'ꙖD', 'XГ', 'ҌГ', 'ѤD', 'AГ'],
            'A': ['ГX', 'ДЄ', 'a'],
            'X': ['BX', 'b', 'ЮD', 'ГD', 'a', 'ꙖD', 'XГ', 'ҌГ', 'ѤD', 'AГ', 'BX', 'b', 'ЮD', 'ГD', 'a', 'ꙖD', 'XГ', 'ҌГ', 'ѤD', 'AГ'],
            'B': ['ЮD', 'ГD', 'a', 'ꙖD', 'XГ', 'ҌГ', 'ѤD', 'AГ'],
            'D': ['ГD', 'a'],
            'C': ['CГ'],
            'Г': ['a'],
            'Д': ['b'],
            'Є': ['x'],
            'Ҍ': ['AX'],
            'Ꙗ': ['XГ'],
            'Ѥ': ['AГ'],
            'Ю': ['ҌГ'],
            'S0': ['S', 'ɛ']
        }

        self.grammar2 = """
        S → AB
        S → C
        A → 0A1
        A → ɛ
        B → 2B3
        B → ɛ
        C → 0C3
        C → D
        C → ɛ
        D → 1D2
        D → ɛ
        """

        self.expected_cnf_grammar2  = {
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

    # def test_transform_to_cnf_1(self):
    #     grammar = Grammar(self.grammar1)
    #     grammar.transformToCNF()
    #     self.assertEqual(dict(grammar.productions), self.expected_cnf_grammar1)

    def test_transform_to_cnf_2(self):
        grammar = Grammar(self.grammar2)
        grammar.transformToCNF()
        self.assertEqual(dict(grammar.productions), self.expected_cnf_grammar2)

if __name__ == '__main__':
    unittest.main()
