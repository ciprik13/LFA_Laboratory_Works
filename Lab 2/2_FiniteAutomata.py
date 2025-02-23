from graphviz import Digraph

# Given FA for Variant 18
Q = {'q0', 'q1', 'q2', 'q3'}  # States
sigma = {'a', 'b', 'c'}  # Alphabet
F = {'q3'}  # Final states
delta = {  # Transition function
    ('q0', 'a'): {'q0', 'q1'},
    ('q1', 'b'): {'q2'},
    ('q2', 'a'): {'q2'},
    ('q2', 'b'): {'q3'},
    ('q3', 'a'): {'q3'}
}


# Task a: Convert FA to Regular Grammar
def fa_to_regular_grammar(Q, sigma, delta, F):
    grammar = {}
    for state in Q:
        grammar[state] = []
        for symbol in sigma:
            if (state, symbol) in delta:
                for next_state in delta[(state, symbol)]:
                    grammar[state].append(f"{symbol}{next_state}")
        if state in F:
            grammar[state].append("ε")  # ε represents an empty string
    return grammar


# Task b: Determine if FA is Deterministic or Non-Deterministic
def is_deterministic(delta):
    for (state, symbol), next_states in delta.items():
        if len(next_states) > 1:
            return False  # Non-deterministic if multiple transitions for the same input
    return True  # Deterministic



