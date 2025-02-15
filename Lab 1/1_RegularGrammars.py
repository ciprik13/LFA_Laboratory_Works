# TODO: grammar class
#  function to generate 5 random strings that follows the language
#  function to_finite_automaton
#  function that checks if string can be obtained from state transition

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
        return current_state in self.f