from slr1_check import build_slr1_table
from lr1_dfa import build_lr1_output

def parse_sentence(grammar_text, sentence, method="SLR(1)"):

    tokens = sentence.strip().split() + ['$']
    lines = [line.strip() for line in grammar_text.strip().split('\n') if line.strip()]

    # 获取产生式编号列表（用于规约动作显示）
    prod_map = []
    for line in lines:
        left, right = map(str.strip, line.split('→'))
        for alt in right.split('|'):
            prod_map.append((left, alt.strip().split()))
    prod_map.insert(0, ("S'", [prod_map[0][0]]))  # 增广文法

    # 获取分析表
    if method == "SLR(1)":
        action_table, goto_table = build_slr1_table(grammar_text)
    else:
        action_table, goto_table, _ = build_lr1_output(grammar_text)

    # 初始化分析栈
    stack = [0]
    symbols = []
    steps = []
    ip = 0
    step = 1

    while True:
        state = stack[-1]
        token = tokens[ip]
        act = action_table.get(state, {}).get(token)

        # 记录步骤（中间过程）
        steps.append([step, str(stack), " ".join(symbols), " ".join(tokens[ip:]), act if act else "error"])
        step += 1

        if not act:
            break
        if act == 'acc':
            break
        elif act.startswith('s'):
            stack.append(int(act[1:]))
            symbols.append(token)
            ip += 1
        elif act.startswith('r'):
            prod_index = int(act[1:])
            lhs, rhs = prod_map[prod_index]
            for _ in rhs:
                stack.pop()
                symbols.pop()
            symbols.append(lhs)
            goto_state = goto_table[stack[-1]].get(lhs)
            if goto_state is None:
                steps[-1][-1] += "（无效 GOTO）"
                break
            stack.append(goto_state)
        else:
            break

    return steps
