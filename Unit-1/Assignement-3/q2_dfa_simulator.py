"""
Section 2: Deterministic Finite Automata (DFA) Simulator
Accepts a DFA description (states, alphabet, transition table, initial state,
final states) and simulates any number of input strings.
"""
import sys


class DFA:
    def __init__(self, states, alphabet, transitions, start, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions      # {(state, symbol): next_state}
        self.start = start
        self.finals = finals

    def simulate(self, text: str):
        """Return (path, accepted, message)."""
        state = self.start
        path = [state]
        for symbol in text:
            if symbol not in self.alphabet:
                return path, False, f"Symbol '{symbol}' is not in the input alphabet"
            if (state, symbol) not in self.transitions:
                return path, False, f"No transition from {state} on '{symbol}'"
            state = self.transitions[(state, symbol)]
            path.append(state)
        return path, state in self.finals, ""


def read_input(prompt: str) -> str:
    try:
        value = input(prompt)
    except EOFError:
        value = "exit"
    if not sys.stdin.isatty():
        print(value)
    return value.strip()


def read_dfa() -> DFA:
    """Read the DFA description from the user with validation."""
    states = [s.strip() for s in read_input("Enter states (comma separated)        : ").split(",") if s.strip()]
    alphabet = [a.strip() for a in read_input("Enter input alphabet (comma separated): ").split(",") if a.strip()]
    print("Enter transitions as 'state symbol next_state' (blank line to finish):")
    transitions = {}
    while True:
        line = read_input("  > ")
        if not line:
            break
        parts = line.split()
        if len(parts) != 3:
            print("    Invalid format, use: state symbol next_state")
            continue
        src, sym, dst = parts
        if src not in states or dst not in states or sym not in alphabet:
            print("    Unknown state or symbol, transition ignored")
            continue
        transitions[(src, sym)] = dst
    start = read_input("Enter initial state                   : ")
    finals = [f.strip() for f in read_input("Enter final state(s) (comma separated) : ").split(",") if f.strip()]
    if start not in states or not set(finals) <= set(states):
        raise ValueError("Initial/final state is not in the set of states")
    return DFA(states, alphabet, transitions, start, finals)


def print_table(dfa: DFA) -> None:
    print("\nTransition Table")
    header = "State".ljust(8) + "".join(sym.ljust(8) for sym in dfa.alphabet)
    print(header)
    print("-" * len(header))
    for s in dfa.states:
        mark = ("->" if s == dfa.start else "  ") + ("*" if s in dfa.finals else " ")
        row = (mark + s).ljust(8) + "".join(dfa.transitions.get((s, a), "-").ljust(8) for a in dfa.alphabet)
        print(row)
    print("(-> initial state, * final state)\n")


def main() -> None:
    print("=" * 56)
    print(" DFA SIMULATOR  (Language: strings ending with 'ab')")
    print("=" * 56)
    try:
        dfa = read_dfa()
    except ValueError as err:
        print("Error:", err)
        return
    print_table(dfa)
    print("Enter input strings to test (type 'exit' to stop)")
    while True:
        text = read_input("\nInput String : ")
        if text.lower() == "exit":
            break
        path, accepted, message = dfa.simulate(text)
        print("Transition Path:", " \u2192 ".join(path))
        if message:
            print("Note:", message)
        print("Accepted" if accepted else "Rejected")


if __name__ == "__main__":
    main()
