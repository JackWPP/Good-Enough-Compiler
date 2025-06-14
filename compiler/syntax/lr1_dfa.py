from collections import defaultdict, deque
import graphviz

class LR1Item:
    def __init__(self, lhs, rhs, dot=0, lookahead='$'):
        self.lhs = lhs
        self.rhs = rhs
        self.dot = dot
        self.lookahead = lookahead

    def __eq__(self, other):
        return (self.lhs == other.lhs and
                self.rhs == other.rhs and
                self.dot == other.dot and
                self.lookahead == other.lookahead)

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs), self.dot, self.lookahead))

    def next_symbol(self):
        return self.rhs[self.dot] if self.dot < len(self.rhs) else None

    def is_complete(self):
        return self.dot >= len(self.rhs)

    def advance(self):
        return LR1Item(self.lhs, self.rhs, self.dot + 1, self.lookahead)

    def __str__(self):
        symbols = list(self.rhs)
        symbols.insert(self.dot, "•")
        return f"{self.lhs} → {' '.join(symbols)}, {self.lookahead}"

class LR1DFA:
    def __init__(self, productions):
        self.augmented_start = "S'"
        self.states = []
        self.transitions = dict()
        self.symbols = set()
        self.grammar = defaultdict(list)
        self.first = defaultdict(set)
        self.productions = []
        self._parse_productions(productions)
        self._build_first()
        self._build_dfa()

    def _parse_productions(self, lines):
        start = None
        for line in lines:
            if '→' not in line:
                continue
            left, right = map(str.strip, line.split('→'))
            if start is None:
                start = left
            for alt in right.split('|'):
                body = alt.strip().split()
                self.grammar[left].append(body)
                self.productions.append((left, body))
                self.symbols.update(body)
            self.symbols.add(left)
        self.grammar[self.augmented_start] = [[start]]
        self.productions.insert(0, (self.augmented_start, [start]))

    def _build_first(self):
        # 简单计算FIRST集（不考虑ε复杂情况）
        for sym in self.symbols:
            if sym not in self.grammar:
                self.first[sym] = {sym}
            else:
                self.first[sym] = set()
        changed = True
        while changed:
            changed = False
            for head in self.grammar:
                for body in self.grammar[head]:
                    before = len(self.first[head])
                    if not body:
                        self.first[head].add('ε')
                        continue
                    for symbol in body:
                        self.first[head].update(self.first[symbol] - {'ε'})
                        if 'ε' not in self.first[symbol]:
                            break
                    else:
                        self.first[head].add('ε')
                    if len(self.first[head]) > before:
                        changed = True

    def _first_sequence(self, symbols):
        result = set()
        for sym in symbols:
            result |= (self.first[sym] - {'ε'})
            if 'ε' not in self.first[sym]:
                break
        else:
            result.add('ε')
        return result

    def _closure(self, items):
        closure = set(items)
        changed = True
        while changed:
            changed = False
            new_items = set()
            for item in closure:
                sym = item.next_symbol()
                if sym and sym in self.grammar:
                    beta = item.rhs[item.dot+1:] if item.dot+1 < len(item.rhs) else []
                    beta.append(item.lookahead)
                    lookaheads = self._first_sequence(beta)
                    for prod in self.grammar[sym]:
                        for la in lookaheads:
                            new_item = LR1Item(sym, prod, 0, la)
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
        start_item = LR1Item(self.augmented_start, self.grammar[self.augmented_start][0], 0, '$')
        start_closure = self._closure([start_item])
        states = [start_closure]
        state_map = {start_closure: 0}
        queue = deque([start_closure])
        while queue:
            state = queue.popleft()
            for sym in self.symbols:
                target = self._goto(state, sym)
                if target is not None:
                    if target not in state_map:
                        state_map[target] = len(states)
                        states.append(target)
                        queue.append(target)
                    self.transitions[(state_map[state], sym)] = state_map[target]
        self.states = states

    def build_action_goto(self):
        terminals = {sym for sym in self.symbols if sym not in self.grammar}
        terminals.add('$')
        nonterminals = set(self.grammar.keys())
        action = defaultdict(dict)
        goto = defaultdict(dict)
        for i, state in enumerate(self.states):
            for item in state:
                sym = item.next_symbol()
                if sym is not None:
                    if sym in terminals:
                        tgt = self.transitions.get((i, sym))
                        if tgt is not None:
                            action[i][sym] = f"s{tgt}"
                    elif sym in nonterminals:
                        tgt = self.transitions.get((i, sym))
                        if tgt is not None:
                            goto[i][sym] = tgt
                else:
                    # 项目完成
                    if (item.lhs == self.augmented_start and
                        item.rhs == self.grammar[self.augmented_start][0] and
                        item.lookahead == '$'):
                        action[i]['$'] = 'acc'
                    else:
                        prod_num = None
                        for idx, (lhs, rhs) in enumerate(self.productions):
                            if lhs == item.lhs and rhs == item.rhs:
                                prod_num = idx
                                break
                        if prod_num is not None:
                            action[i][item.lookahead] = f"r{prod_num}"
        return action, goto

    def visualize_dfa(self):
        dot = graphviz.Digraph(format="svg")
        for i, state in enumerate(self.states):
            label = f"State {i}\\n" + "\\n".join(str(item) for item in sorted(state, key=str))
            dot.node(str(i), label=label, shape="box", fontname="Courier")
        for (src, sym), tgt in self.transitions.items():
            dot.edge(str(src), str(tgt), label=sym)
        return dot.pipe().decode("utf-8")

# 封装成方便调用的接口函数，方便在app.py里调用
def build_lr1_output(text):
    """
    输入文法文本（多行字符串），
    返回 action 表（dict），goto 表（dict），以及SVG字符串
    """
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    lr1dfa = LR1DFA(lines)
    action, goto = lr1dfa.build_action_goto()
    svg = lr1dfa.visualize_dfa()
    return action, goto, svg
