import unittest
from ChomskyNormalForm import Grammar

class TestGrammar(unittest.TestCase):
    def setUp(self):
        non_terminals = ['S', 'A', 'B', 'C', 'D']
        terminals = ['a', 'b']
        rules = {
            'S': ['aB', 'bA', 'B'],
            'A': ['b', 'aD', 'AS', 'bAB', 'ε'],
            'B': ['a', 'bS'],
            'C': ['AB'],
            'D': ['BB']
        }
        self.grammar = Grammar(non_terminals, terminals, rules)

    def test_initial_grammar(self):
        self.assertEqual(set(self.grammar.non_terminals), {'S', 'A', 'B', 'C', 'D'})
        self.assertEqual(set(self.grammar.terminals), {'a', 'b'})
        for nt in ['S', 'A', 'B', 'C', 'D']:
            self.assertIn(nt, self.grammar.rules)

    def test_eliminate_epsilon_productions(self):
        self.grammar.eliminate_epsilon_productions()
        for prods in self.grammar.rules.values():
            self.assertNotIn('ε', prods)

    def test_eliminate_renaming_productions(self):
        self.grammar.eliminate_epsilon_productions()
        self.grammar.eliminate_renaming()
        for prods in self.grammar.rules.values():
            for prod in prods:
                self.assertNotIn(prod, self.grammar.non_terminals)

    def test_eliminate_inaccessible_symbols(self):
        self.grammar.eliminate_epsilon_productions()
        self.grammar.eliminate_renaming()
        self.grammar.eliminate_inaccessible_symbols()
        accessible = set(self.grammar.non_terminals)
        for nt in accessible:
            self.assertIn(nt, self.grammar.rules)

    def test_eliminate_non_productive_symbols(self):
        self.grammar.eliminate_epsilon_productions()
        self.grammar.eliminate_renaming()
        self.grammar.eliminate_inaccessible_symbols()
        self.grammar.eliminate_non_productive_symbols()
        for prods in self.grammar.rules.values():
            for prod in prods:
                for symbol in prod:
                    self.assertTrue(symbol in self.grammar.terminals or symbol in self.grammar.non_terminals)

    def test_is_cnf(self):
        self.assertFalse(self.grammar.is_cnf())
        self.grammar.to_cnf(print_steps=False)
        self.assertTrue(self.grammar.is_cnf())

    def test_to_cnf(self):
        self.grammar.to_cnf(print_steps=True)
        for nt, prods in self.grammar.rules.items():
            for prod in prods:
                self.assertTrue(1 <= len(prod) <= 2)
                if len(prod) == 1:
                    self.assertTrue(prod in self.grammar.terminals)
                if len(prod) == 2:
                    self.assertTrue(all(symbol in self.grammar.non_terminals for symbol in prod))

if __name__ == '__main__':
    unittest.main()
