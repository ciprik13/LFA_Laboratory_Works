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
        states = self.vn | {'qf'}  #q
        alphabet = self.vt #sigma
        start_state = self.start_symbol #delta
        transitions = {} #q0
        final_states = {'qf'}  #F

        for key in self.p:
            for rule in self.p[key]:
                if (key, rule[0]) not in transitions:
                    transitions[(key, rule[0])] = set()

                if len(rule) == 1 and rule in self.vt:
                    transitions[(key, rule)].add('qf')  # terminal leads to final state
                elif len(rule) > 1:
                    next_state = rule[1] if rule[1] in self.vn else 'qf'
                    transitions[(key, rule[0])].add(next_state)

        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def string_in_language(self, input_string):
        current_states = {self.start_state} 

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])
            if not next_states:
                return False 
            current_states = next_states  

        return bool(current_states & self.final_states)  # check if any state is final

# Main 
grammar = Grammar()
finite_automaton = grammar.to_finite_automaton()

print("Generated random strings:")
for _ in range(5):
    print(grammar.generate_string())

print("\nChecking if strings belong to the language:")
test_strings = ["aaa", "aabb", "aa", "aabaababaaa", "ababaaa"]
for s in test_strings:
    print(f"String '{s}' is accepted: {finite_automaton.string_in_language(s)}")
