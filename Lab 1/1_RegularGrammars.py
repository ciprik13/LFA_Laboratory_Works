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
        states = self.vn  # Non-terminal symbols as states
        alphabet = self.vt  # Terminal symbols as alphabet
        start_state = self.start_symbol  # Start state
        transitions = {}  # Transition function
        final_states = set()

        for key in self.p.keys():
            for rule in self.p[key]:
                if key not in transitions:
                    transitions[key] = []
                if len(rule) == 2:
                    transitions[key].append((rule[0], rule[1]))
                else:
                    transitions[key].append((rule[0], None))

        for key in self.p:
            if all(rule in self.vt for rule in self.p[key]):
                final_states.add(key)
        final_states.add('C')

        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def string_belongs_to_language(self, input_string):
        current_state = self.start_state
        for c in input_string:
            if c not in self.alphabet or current_state not in self.transitions:
                return False
            next_state = None
            for transition in self.transitions[current_state]:
                if c == transition[0]:
                    next_state = transition[1] if transition[1] is not None else current_state
                    break
            if next_state is None:
                return False
            current_state = next_state
        return current_state in self.final_states

