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


# Task c: Convert NFA to DFA
def nfa_to_dfa(Q, sigma, delta, F):
    dfa_states = []  # List of DFA states (each is a set of NFA states)
    dfa_delta = {}  # DFA transition function
    dfa_final = []  # DFA final states
    initial_state = frozenset({'q0'})  # Start with the initial state of the NFA
    dfa_states.append(initial_state)

    # Process each DFA state
    for state in dfa_states:
        for symbol in sigma:
            next_state = set()
            for nfa_state in state:
                if (nfa_state, symbol) in delta:
                    next_state.update(delta[(nfa_state, symbol)])
            if next_state:
                next_state = frozenset(next_state)
                if next_state not in dfa_states:
                    dfa_states.append(next_state)
                dfa_delta[(state, symbol)] = next_state

    # Determine final states in DFA
    for state in dfa_states:
        if any(nfa_state in F for nfa_state in state):
            dfa_final.append(state)

    return dfa_states, dfa_delta, dfa_final

# Task d: Represent FA Graphically
def draw_fa(Q, sigma, delta, F):
    fa = Digraph()
    for state in Q:
        if state in F:
            fa.node(state, shape='doublecircle')  # Final state
        else:
            fa.node(state, shape='circle')  # Non-final state
    for (state, symbol), next_states in delta.items():
        for next_state in next_states:
            fa.edge(state, next_state, label=symbol)
    fa.render('fa_graph', format='png', cleanup=True)
    print("FA graph saved as 'fa_graph.png'")


# Main Program
if __name__ == "__main__":
    # Task a: Convert FA to Regular Grammar
    grammar = fa_to_regular_grammar(Q, sigma, delta, F)
    print("Regular Grammar:")
    for non_terminal, productions in grammar.items():
        print(f"{non_terminal} -> {' | '.join(productions)}")

    # Task b: Determine if FA is Deterministic or Non-Deterministic
    if is_deterministic(delta):
        print("\nThe FA is Deterministic (DFA).")
    else:
        print("\nThe FA is Non-Deterministic (NFA).")

    # Task c: Convert NFA to DFA
    dfa_states, dfa_delta, dfa_final = nfa_to_dfa(Q, sigma, delta, F)
    print("\nDFA States:", [set(state) for state in dfa_states])
    print("DFA Transitions:")
    for (state, symbol), next_state in dfa_delta.items():
        print(f"δ({set(state)}, {symbol}) = {set(next_state)}")
    print("DFA Final States:", [set(state) for state in dfa_final])

    # Task d: Represent FA Graphically
    draw_fa(Q, sigma, delta, F)

