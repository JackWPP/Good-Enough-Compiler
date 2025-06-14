from collections import defaultdict, deque
import graphviz

class LR0Item:
    def __init__(self, lhs, rhs, dot=0):
        self.lhs = lhs
        self.rhs = rhs
        self.dot = dot

    def __eq__(self, other):
        return (self.lhs, self.rhs, self.dot) == (other.lhs, other.rhs, other.dot)

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs), self.dot))

    def next_symbol(self):
        return self.rhs[self.dot] if self.dot < len(self.rhs) else None

    def is_complete(self):
        return self.dot >= len(self.rhs)

    def advance(self):
        return LR0Item(self.lhs, self.rhs, self.dot + 1)

    def __str__(self):
        symbols = list(self.rhs)
        symbols.insert(self.dot, "•")
        return f"{self.lhs} → {' '.join(symbols)}"

class LR0DFA:
    def __init__(self, productions):
        self.augmented_start = "S'"
        self.states = []
        self.transitions = dict()
        self.symbols = set()
        self._parse_productions(productions)
        self._build_dfa()

    def _parse_productions(self, lines):
        self.grammar = defaultdict(list)
        start = None
        for line in lines:
            if '→' not in line:
                continue
            left, right = map(str.strip, line.split("→"))
            if start is None:
                start = left
            for alt in right.split('|'):
                body = alt.strip().split()
                self.grammar[left].append(body)
                self.symbols.update(body)
            self.symbols.add(left)
        self.grammar[self.augmented_start] = [[start]]

    def _closure(self, items):
        closure = set(items)
        changed = True
        while changed:
            changed = False
            new_items = set()
            for item in closure:
                sym = item.next_symbol()
                if sym in self.grammar:
                    for prod in self.grammar[sym]:
                        new_item = LR0Item(sym, prod, 0)
                        if new_item not in closure:
                            new_items.add(new_item)
            if new_items:
                closure |= new_items
                changed = True
        return frozenset(closure)

    def _goto(self, state, symbol):
        moved = [item.advance() for item in state if item.next_symbol() == symbol]
        return self._closure(moved) if moved else None

    def _build_dfa(self):
        start_item = LR0Item(self.augmented_start, self.grammar[self.augmented_start][0], 0)
        start_closure = self._closure([start_item])
        states = [start_closure]
        state_map = {start_closure: 0}
        queue = deque([start_closure])
        while queue:
            state = queue.popleft()
            for symbol in self.symbols:
                target = self._goto(state, symbol)
                if target and target not in state_map:
                    state_map[target] = len(states)
                    states.append(target)
                    queue.append(target)
                if target:
                    self.transitions[(state_map[state], symbol)] = state_map[target]
        self.states = states

    def get_states_str(self):
        return "\n".join(f"State {i}:\n  " + "\n  ".join(str(item) for item in sorted(s, key=str))
                         for i, s in enumerate(self.states))

    def get_transitions_str(self):
        return "\n".join(f"State {src} --[{sym}]--> State {tgt}"
                         for (src, sym), tgt in sorted(self.transitions.items()))

    def get_svg(self):
        dot = graphviz.Digraph(format="svg")
        for i, state in enumerate(self.states):
            label = f"State {i}\\n" + "\\n".join(str(item) for item in sorted(state, key=str))
            dot.node(str(i), label=label, shape="box", fontname="Courier")
        for (src, sym), tgt in self.transitions.items():
            dot.edge(str(src), str(tgt), label=sym)
        return dot.pipe().decode("utf-8")

def build_lr0_output(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    dfa = LR0DFA(lines)
    return dfa.get_states_str(), dfa.get_transitions_str(), dfa.get_svg()
