from collections import defaultdict

EPSILON = 'ε'
ENDMARK = '$'

class Grammar:
    def __init__(self, productions):
        self.productions = defaultdict(list)
        self.nonterminals = set()
        self.terminals = set()
        self.start_symbol = None
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.parse_productions(productions)
        self.augment_grammar()  # 拓广文法

    def parse_productions(self, lines):
        for line in lines:
            if '→' not in line:
                continue
            left, right = map(str.strip, line.split('→'))
            if self.start_symbol is None:
                self.start_symbol = left
            self.nonterminals.add(left)
            for alt in right.split('|'):
                symbols = alt.strip().split()
                self.productions[left].append(symbols)
        all_symbols = {sym for bodies in self.productions.values() for body in bodies for sym in body}
        self.terminals = all_symbols - self.nonterminals - {EPSILON}

    def augment_grammar(self):
        # 新增拓广开始符号 S'
        new_start = self.start_symbol + "'"
        while new_start in self.nonterminals or new_start in self.terminals:
            new_start += "'"
        self.productions[new_start] = [[self.start_symbol]]
        self.nonterminals.add(new_start)
        self.start_symbol = new_start

    def compute_first(self):
        for t in self.terminals:
            self.first[t] = {t}
        for nt in self.nonterminals:
            self.first[nt] = set()
        changed = True
        while changed:
            changed = False
            for head in self.productions:
                for body in self.productions[head]:
                    i = 0
                    add_epsilon = True
                    while i < len(body):
                        sym = body[i]
                        before = len(self.first[head])
                        self.first[head].update(self.first[sym] - {EPSILON})
                        if EPSILON in self.first[sym]:
                            i += 1
                        else:
                            add_epsilon = False
                            break
                    if add_epsilon:
                        self.first[head].add(EPSILON)
                    if len(self.first[head]) > before:
                        changed = True

    def compute_follow(self):
        self.follow[self.start_symbol].add(ENDMARK)
        changed = True
        while changed:
            changed = False
            for head in self.productions:
                for body in self.productions[head]:
                    trailer = self.follow[head].copy()
                    for sym in reversed(body):
                        if sym in self.nonterminals:
                            before = len(self.follow[sym])
                            self.follow[sym].update(trailer)
                            if EPSILON in self.first[sym]:
                                trailer = trailer.union(self.first[sym] - {EPSILON})
                            else:
                                trailer = self.first[sym]
                            if len(self.follow[sym]) > before:
                                changed = True
                        else:
                            trailer = self.first[sym]

    def get_first_follow_str(self):
        res = []
        for nt in sorted(self.nonterminals):
            res.append(f"First({nt}) = {{ {', '.join(sorted(self.first[nt]))} }}")
        res.append("")
        for nt in sorted(self.nonterminals):
            res.append(f"Follow({nt}) = {{ {', '.join(sorted(self.follow[nt]))} }}")
        return "\n".join(res)

def process_first_follow(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    g = Grammar(lines)
    g.compute_first()
    g.compute_follow()
    return g
