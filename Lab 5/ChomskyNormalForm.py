from collections import deque


class Grammar:
    def __init__(self, non_terminals, terminals, rules, start_symbol='S'):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules
        self.start_symbol = start_symbol
        self._new_nt_counter = 0

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

    def _create_new_non_terminal(self):
        new_symbol = str(self._new_nt_counter)
        self._new_nt_counter += 1
        while new_symbol in self.non_terminals:
            new_symbol = str(self._new_nt_counter)
            self._new_nt_counter += 1
        return new_symbol

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