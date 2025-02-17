import random

class Grammar:
    def __init__(self):
        self.vn = {'S', 'A', 'B', 'C'}
        self.vt = {'a', 'b'}
        self.p = {
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
        q = self.vn | {'qf'}  # set of states (non-terminals + final state)
        sigma = self.vt  # alphabet (terminal symbols)
        q0 = self.start_symbol  # start state
        delta = {}  # transition function
        f = {'qf'}  # set of final states

        for key in self.p:
            for rule in self.p[key]:
                if (key, rule[0]) not in delta:
                    delta[(key, rule[0])] = set()

                if len(rule) == 1 and rule in self.vt:
                    delta[(key, rule)].add('qf')  # terminal leads to final state
                elif len(rule) > 1:
                    next_state = rule[1] if rule[1] in self.vn else 'qf'
                    delta[(key, rule[0])].add(next_state)

        return FiniteAutomaton(q, sigma, delta, q0, f)

class FiniteAutomaton:
    def __init__(self, q, sigma, delta, q0, f):
        self.q = q  # set of states
        self.sigma = sigma  # alphabet
        self.delta = delta  # transition function
        self.q0 = q0  # start state
        self.f = f  # set of final states

    def string_in_language(self, input_string):
        current_states = {self.q0}  # start from the initial state

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.delta:
                    next_states.update(self.delta[(state, symbol)])
            if not next_states:
                return False  # no valid transition for the symbol
            current_states = next_states

        return bool(current_states & self.f)  # check if any state is final

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
