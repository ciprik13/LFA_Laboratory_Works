import random

class Grammar:
    def __init__(self):
        self.vn = {'S', 'A', 'B', 'C'}  # Non-terminals
        self.vt = {'a', 'b'}            # Terminals
        self.p = {                       # Production rules
            'S': ['aA', 'aB'],
            'A': ['bS'],
            'B': ['aC'],
            'C': ['a', 'bS']
        }
        self.start_symbol = 'S'

    def generate_string(self):
        string = self.start_symbol
        while any(v in string for v in self.vn):
            for v in string:
                if v in self.vn:
                    string = string.replace(v, random.choice(self.p[v]), 1)
                    break
        return string

    def to_finite_automaton(self):
        q = self.vn | {'qf'}  # Set of states (non-terminals + final state)
        sigma = self.vt        # Alphabet (terminal symbols)
        q0 = self.start_symbol # Start state
        delta = {}             # Transition function
        f = {'qf'}            # Set of final states

        for key in self.p:
            for rule in self.p[key]:
                if (key, rule[0]) not in delta:
                    delta[(key, rule[0])] = set()

                if len(rule) == 1 and rule in self.vt:
                    delta[(key, rule)].add('qf')  # Terminal leads to final state
                elif len(rule) > 1:
                    next_state = rule[1] if rule[1] in self.vn else 'qf'
                    delta[(key, rule[0])].add(next_state)

        return FiniteAutomaton(q, sigma, delta, q0, f)

    def classify_grammar(self):
        is_regular = True
        is_context_free = True
        is_context_sensitive = True

        for lhs, rhs_list in self.p.items():
            for rhs in rhs_list:
                # Check if the grammar is regular
                if not (len(rhs) == 1 and rhs in self.vt) or \
                   (len(rhs) == 2 and rhs[0] in self.vt and rhs[1] in self.vn):
                    is_regular = False

                # Check if the grammar is context-free
                if not (len(lhs) == 1 and lhs in self.vn):
                    is_context_free = False

                # Check if the grammar is context-sensitive
                if not (len(lhs) <= len(rhs)):
                    is_context_sensitive = False

        if is_regular:
            return "Type 3 (Regular Grammar)"
        elif is_context_free:
            return "Type 2 (Context-Free Grammar)"
        elif is_context_sensitive:
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"

class FiniteAutomaton:
    def __init__(self, q, sigma, delta, q0, f):
        self.q = q      # Set of states
        self.sigma = sigma  # Alphabet
        self.delta = delta  # Transition function
        self.q0 = q0    # Start state
        self.f = f      # Set of final states

    def string_in_language(self, input_string):
        current_states = {self.q0}  # Start from the initial state

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.delta:
                    next_states.update(self.delta[(state, symbol)])
            if not next_states:
                return False  # No valid transition for the symbol
            current_states = next_states

        return bool(current_states & self.f)  # Check if any state is final

# Main
grammar = Grammar()
finite_automaton = grammar.to_finite_automaton()

print("Generated random strings:")
for _ in range(5):
    print(grammar.generate_string())

print("\nChecking if strings belong to the language:")
test_strings = ["aaa", "abaaa", "aa", "aabaababaaa", "ababaaab"]
for s in test_strings:
    print(f"String '{s}' is accepted: {finite_automaton.string_in_language(s)}")

print("\nGrammar Classification:")
print(grammar.classify_grammar())