
# Laboratory Work 4: Chomsky Normal Form (CNF) Transformation

### Course: Formal Languages & Finite Automata  
### Author: Ciprian Moisenco

---

## Overview

This project implements a robust and modular system that can transform any context-free grammar (CFG) into Chomsky Normal Form (CNF).
The transformations are done step-by-step, strictly following theoretical rules, and ensuring full compliance with CNF structure requirements.
The project also includes an extensive test suite using Python's `unittest` framework to ensure every function works as expected.

---

## Objectives

- Understand the theoretical foundations of CNF and the importance of grammar normalization.
- Implement clean, modular code to perform individual grammar transformations.
- Build reusable and extensible classes for grammar management.
- Perform unit testing for each stage to guarantee correctness and robustness.
- BONUS: Handle **any arbitrary grammar**, not just a predefined one.

---

## Theory

**Chomsky Normal Form (CNF)** is a standard form for context-free grammars where:
- Every production rule is either of the form **A → BC** (two non-terminals) or **A → a** (a single terminal).
- The empty production ε (epsilon) is allowed only if the start symbol can derive ε directly.

Transforming grammars to CNF is crucial for:
- Simplifying parsing algorithms (e.g., CYK parsing).
- Standardizing representations for computational analysis.
- Facilitating formal proofs and reasoning about languages.

---

## Class Overview

### `Grammar`

A fully modular class that provides all functionality needed to:
- Store and manage a grammar.
- Apply normalization and transformation techniques.
- Convert the grammar into CNF in a sequential, step-by-step manner.

```python

```

---

## Detailed Method Descriptions

### `__init__(non_terminals, terminals, rules, start_symbol='S')`
Initializes the grammar with the provided components.
It sets up the structure of the grammar including non-terminals, terminals, production rules, and the start symbol.
An internal counter (`_new_nt_counter`) is also initialized to manage the creation of new non-terminals dynamically during transformations.

```python
    def __init__(self, non_terminals, terminals, rules, start_symbol='S'):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start_symbol = start_symbol
        self._new_nt_counter = 0
```

### `print_rules(title=None)`
Prints the current grammar rules in an aligned and organized format.
If a title is provided, it displays it above the rules to indicate the phase or purpose of the current view (e.g., "After Epsilon Elimination").

```python
    def print_rules(self, title=None):
        def custom_sort(nt):
            if nt == 'S':
                return (0, '')
            elif nt[0].isalpha():
                return (1, nt)
            else:
                return (2, nt)

        if title:
            print(f"\n{'=' * 50}")
            print(f"{title:^50}")
            print(f"{'=' * 50}")

        ordered = sorted(self.rules.keys(), key=custom_sort)
        max_nt_len = max(len(nt) for nt in ordered) if ordered else 0

        for non_terminal in ordered:
            productions = sorted(self.rules[non_terminal])
            arrow = "→"
            print(f"{non_terminal:<{max_nt_len}} {arrow} {' | '.join(productions)}")
```

### `is_cnf()`
Determines whether the grammar is already in Chomsky Normal Form.
Checks that every production is either a single terminal or exactly two non-terminals.
Returns `True` if CNF is satisfied, otherwise `False`.

```python
    def is_cnf(self):
        for non_terminal in self.rules:
            for production in self.rules[non_terminal]:
                if len(production) == 0 or len(production) > 2:
                    return False
                if len(production) == 1 and production not in self.terminals and production != 'ε':
                    return False
                if len(production) == 2 and any(symbol in self.terminals for symbol in production):
                    return False
        return True
```

### `eliminate_epsilon_productions()`
Identifies and removes all ε-productions from the grammar.
Nullable non-terminals (those that can derive ε) are computed, and their effect on other productions is carefully handled by generating all valid combinations without the nullable symbols.

```python
    def eliminate_epsilon_productions(self):
        nullable = set()
        for nt in self.non_terminals:
            if 'ε' in self.rules.get(nt, []):
                nullable.add(nt)

        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for prod in self.rules.get(nt, []):
                    if all(symbol in nullable for symbol in prod):
                        if nt not in nullable:
                            nullable.add(nt)
                            changed = True

        new_rules = {}
        for nt in self.non_terminals:
            new_productions = set()
            for prod in self.rules.get(nt, []):
                if prod == 'ε':
                    continue

                combinations = [""]
                for symbol in prod:
                    new_combinations = []
                    for combination in combinations:
                        new_combinations.append(combination + symbol)
                        if symbol in nullable:
                            new_combinations.append(combination)
                    combinations = new_combinations

                for combination in combinations:
                    if combination:
                        new_productions.add(combination)

            new_rules[nt] = list(new_productions)

        self.rules = new_rules
```

### `eliminate_renaming()`
Eliminates unit productions, i.e., rules where a non-terminal maps directly to another non-terminal.
Uses a breadth-first search approach to collapse indirect unit productions into terminal-producing or proper non-terminal productions.

```python
    def eliminate_renaming(self):
        unit_pairs = {}
        for nt in self.non_terminals:
            unit_pairs[nt] = set()
            queue = deque([nt])
            while queue:
                current = queue.popleft()
                for prod in self.rules.get(current, []):
                    if prod in self.non_terminals and prod not in unit_pairs[nt]:
                        unit_pairs[nt].add(prod)
                        queue.append(prod)

        new_rules = {}
        for nt in self.non_terminals:
            new_productions = set()
            for prod in self.rules.get(nt, []):
                if prod not in self.non_terminals:
                    new_productions.add(prod)

            for unit_nt in unit_pairs[nt]:
                for prod in self.rules.get(unit_nt, []):
                    if prod not in self.non_terminals:
                        new_productions.add(prod)

            new_rules[nt] = list(new_productions)

        self.rules = new_rules
```

### `eliminate_inaccessible_symbols()`
Traverses from the start symbol to detect all reachable non-terminals.
Any non-terminal that cannot be reached is considered inaccessible and is removed from the grammar to keep it clean and efficient.

```python
    def eliminate_inaccessible_symbols(self):
        accessible = set()
        queue = deque([self.start_symbol])
        accessible.add(self.start_symbol)

        while queue:
            current = queue.popleft()
            for prod in self.rules.get(current, []):
                for symbol in prod:
                    if symbol in self.non_terminals and symbol not in accessible:
                        accessible.add(symbol)
                        queue.append(symbol)

        self.non_terminals = [nt for nt in self.non_terminals if nt in accessible]
        self.rules = {nt: prods for nt, prods in self.rules.items() if nt in accessible}
```

### `eliminate_non_productive_symbols()`
Detects non-terminals that do not contribute to any terminal string derivations.
Such non-productive symbols are removed, along with any rules involving them, ensuring that the grammar remains meaningful and minimal.
```python
    def eliminate_non_productive_symbols(self):
        productive = set()
        for nt in self.non_terminals:
            for prod in self.rules.get(nt, []):
                if all(symbol in self.terminals for symbol in prod):
                    productive.add(nt)
                    break

        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                if nt not in productive:
                    for prod in self.rules.get(nt, []):
                        if all(symbol in productive or symbol in self.terminals for symbol in prod):
                            productive.add(nt)
                            changed = True
                            break

        self.non_terminals = [nt for nt in self.non_terminals if nt in productive]
        new_rules = {}
        for nt in productive:
            new_productions = []
            for prod in self.rules.get(nt, []):
                if all(symbol in productive or symbol in self.terminals for symbol in prod):
                    new_productions.append(prod)
            new_rules[nt] = new_productions

        self.rules = new_rules
```

### `_create_new_non_terminal()`
Generates a fresh non-terminal whenever needed during CNF transformation.
It guarantees name uniqueness by incrementing a counter until a non-conflicting name is found.
```python
    def _create_new_non_terminal(self):
        new_symbol = str(self._new_nt_counter)
        self._new_nt_counter += 1
        while new_symbol in self.non_terminals:
            new_symbol = str(self._new_nt_counter)
            self._new_nt_counter += 1
        return new_symbol
```

### `to_cnf(print_steps=False)`
Executes the full normalization process:
- Epsilon elimination
- Renaming elimination
- Removal of inaccessible and non-productive symbols
- Terminal replacement for multi-symbol productions
- Splitting of productions longer than two symbols into binary productions

Prints intermediate grammars if `print_steps` is enabled, providing a clear transformation trace.

```python
    def to_cnf(self, print_steps=False):
        if self.is_cnf():
            if print_steps:
                self.print_rules("Grammar is already in CNF")
            return

        self.eliminate_epsilon_productions()
        if print_steps:
            self.print_rules("1. After eliminating epsilon productions")

        self.eliminate_renaming()
        if print_steps:
            self.print_rules("2. After eliminating renaming productions")

        self.eliminate_inaccessible_symbols()
        if print_steps:
            self.print_rules("3. After eliminating inaccessible symbols")

        self.eliminate_non_productive_symbols()
        if print_steps:
            self.print_rules("4. After eliminating non-productive symbols")

        # Step 1: Replace terminals in productions with length > 1
        terminal_replacements = {}
        new_rules = {}
        for terminal in self.terminals:
            new_nt = self._create_new_non_terminal()
            terminal_replacements[terminal] = new_nt
            new_rules[new_nt] = [terminal]
            self.non_terminals.append(new_nt)

        for nt in self.non_terminals:
            if nt not in new_rules:
                new_productions = []
                for prod in self.rules.get(nt, []):
                    if len(prod) == 1:
                        new_productions.append(prod)
                    else:
                        new_prod = []
                        for symbol in prod:
                            if symbol in terminal_replacements:
                                new_prod.append(terminal_replacements[symbol])
                            else:
                                new_prod.append(symbol)
                        new_productions.append(''.join(new_prod))
                new_rules[nt] = new_productions

        self.rules.update(new_rules)

        # Step 2: Break down productions longer than 2 symbols
        pair_replacements = {}
        for nt in list(self.rules.keys()):
            new_productions = []
            for prod in self.rules[nt]:
                while len(prod) > 2:
                    first_two = prod[:2]
                    if first_two not in pair_replacements:
                        new_nt = self._create_new_non_terminal()
                        pair_replacements[first_two] = new_nt
                        self.rules[new_nt] = [first_two]
                        self.non_terminals.append(new_nt)
                    prod = pair_replacements[first_two] + prod[2:]
                new_productions.append(prod)
            self.rules[nt] = new_productions

        if print_steps:
            self.print_rules("5. Final CNF Form")
```

---

## Unit Tests

Tests cover:
- Initial grammar setup validation
- Epsilon elimination
- Renaming elimination
- Inaccessible symbol removal
- Non-productive symbol removal
- CNF validation before and after transformation
- Full pipeline end-to-end correctness

```python
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

```

---

## Example Output Results

```python
==================================================
     1. After eliminating epsilon productions     
==================================================
S → B | aB | b | bA
A → AS | S | aD | b | bAB | bB
B → a | bS
C → AB | B
D → BB

==================================================
    2. After eliminating renaming productions     
==================================================
S → a | aB | b | bA | bS
A → AS | a | aB | aD | b | bA | bAB | bB | bS
B → a | bS
C → AB | a | bS
D → BB

==================================================
    3. After eliminating inaccessible symbols     
==================================================
S → a | aB | b | bA | bS
A → AS | a | aB | aD | b | bA | bAB | bB | bS
B → a | bS
D → BB

==================================================
   4. After eliminating non-productive symbols    
==================================================
S → a | aB | b | bA | bS
A → AS | a | aB | aD | b | bA | bAB | bB | bS
B → a | bS
D → BB

==================================================
                5. Final CNF Form                 
==================================================
S → 0B | 1A | 1S | a | b
A → 0B | 0D | 1A | 1B | 1S | 2B | AS | a | b
B → 1S | a
D → BB
0 → a
1 → b
2 → 1A

Process finished with exit code 0

```

---

## Conclusion

This project achieves a complete, modular, and fully functional implementation of grammar normalization into Chomsky Normal Form (CNF).
Each stage of the normalization process — from epsilon elimination to renaming elimination, and from cleaning inaccessible and non-productive symbols to splitting productions — is handled carefully, following the formal theoretical rules of language and automata theory.

Throughout this project, several important principles of formal language processing are applied:
- **Correctness**: Every transformation preserves the original language generated by the grammar.
- **Robustness**: The methods are designed to work with arbitrary user-supplied grammars, not just specific examples.
- **Transparency**: Each major transformation phase can be printed step-by-step to allow easy debugging and learning.
- **Extensibility**: The modular class design allows future expansion, for instance, supporting grammar visualization or automated CYK parsing preparation.

The unit test suite provides a strong safety net ensuring that:
- Basic structure initialization is correct.
- Intermediate transformation steps behave exactly as theoretically expected.
- The final grammar after transformation satisfies all CNF constraints.

Beyond the immediate implementation, this work enhances deeper academic and practical understanding:
- It shows how theoretical concepts (such as nullable symbols, productive symbols, and accessible symbols) can be turned into real-world algorithms.
- It lays a foundation for further research or projects involving parsers, grammar analyzers, or automated language recognition systems.
- It prepares the ground for implementing more advanced topics like ambiguity detection, syntax-directed translation, and compiler construction.

Ultimately, the project serves not only as a validation of theoretical knowledge but also as an exercise in writing clean, reliable, and extensible software for non-trivial computational problems.

This work is an essential stepping stone toward mastering fields like compiler design, formal verification, and advanced automata theory applications.

---

## References

1. COJUHARI Irina, DUCA Ludmila, FIODOROV Ion. "Formal Languages and Finite Automata: Guide for practical lessons". Technical University of Moldova.
2. N. Chomsky. *Three models for the description of language*, 1956.
3. [Wikipedia - Chomsky Normal Form](https://en.wikipedia.org/wiki/Chomsky_normal_form)
