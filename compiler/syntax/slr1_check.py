def check_slr1(grammar):
    parsing_table = {}
    conflicts = []

    for A in grammar.productions:
        for prod in grammar.productions[A]:
            if prod == ['ε']:
                for a in grammar.follow[A]:
                    key = (A, a)
                    if key in parsing_table:
                        conflicts.append(f"冲突: {A} → ε 与 {parsing_table[key]} 同在 Follow({A}) 的 {a}")
                    else:
                        parsing_table[key] = "ε"
            else:
                a = prod[0]
                if a in grammar.first and 'ε' not in grammar.first[a]:
                    for t in grammar.first[a]:
                        key = (A, t)
                        if key in parsing_table:
                            conflicts.append(f"冲突: {A} → {' '.join(prod)} 与 {parsing_table[key]} 同在 First 的 {t}")
                        else:
                            parsing_table[key] = ' '.join(prod)
    return conflicts

def build_slr1_table(grammar):
    """
    构造 SLR(1) 分析表：Action 表和 Goto 表
    参数：
        grammar - 文法对象，包含项目集(states)、转移(transitions)、产生式(productions)、开始符号(start_symbol)、Follow 集(follow)等
    返回：
        action_table, goto_table
        - action_table: dict { state: {terminal: action} }
        - goto_table: dict { state: {nonterminal: next_state} }
    """
    action_table = {}
    goto_table = {}

    # 产生式索引，用于规约动作中指定产生式编号
    # 产生式统一编号方便显示和规约使用，顺序如下：
    # start_symbol' → start_symbol 为第0条产生式
    prod_list = []
    for head in grammar.productions:
        for body in grammar.productions[head]:
            prod_list.append((head, body))

    # 寻找扩展文法开始产生式索引（假设有扩展文法 S' → S）
    # 若无扩展，默认第0条是 S' → S
    # 你也可以自定义扩展文法产生式
    start_prod_index = 0

    # 遍历所有状态
    for state_id, items in grammar.states.items():
        action_table[state_id] = {}
        goto_table[state_id] = {}

        # 遍历状态的所有项目
        for item in items:
            # item 格式示例：(head, body, dot_pos)
            # head: 产生式左部，body:产生式右部列表，dot_pos:点的位置
            head, body, dot_pos = item

            # 判断点是否在产生式末尾（即可规约项目）
            if dot_pos == len(body):
                # 归约项目
                # 如果是扩展文法的开始产生式 S' → S· ，接受动作
                if head == grammar.start_symbol + "'" and body == [grammar.start_symbol]:
                    # 接受动作标记为 acc
                    action_table[state_id]['$'] = 'acc'  # $ 表示输入结束符
                else:
                    # 对当前产生式对应 Follow(head) 集中的终结符添加规约动作
                    # 查找产生式编号
                    prod_index = None
                    for i, (h, b) in enumerate(prod_list):
                        if h == head and b == body:
                            prod_index = i
                            break
                    if prod_index is None:
                        raise ValueError(f"产生式未找到：{head} → {' '.join(body)}")

                    for lookahead in grammar.follow[head]:
                        # 检测冲突
                        if lookahead in action_table[state_id]:
                            # 这里可记录冲突信息或覆盖
                            # 简单覆盖（实际可扩展处理冲突）
                            # 也可以存冲突日志
                            prev = action_table[state_id][lookahead]
                            if prev != f"r{prod_index}":
                                # 冲突处理，这里简单追加警告（可根据需要修改）
                                print(f"冲突：状态 {state_id}，符号 '{lookahead}'，动作冲突 '{prev}' vs 'r{prod_index}'")
                        else:
                            action_table[state_id][lookahead] = f"r{prod_index}"

            else:
                # 点未到末尾，读取下一个符号
                next_sym = body[dot_pos]
                if next_sym in grammar.terminals:
                    # 移进动作
                    if (state_id, next_sym) in grammar.transitions:
                        next_state = grammar.transitions[(state_id, next_sym)]
                        if next_sym in action_table[state_id]:
                            prev = action_table[state_id][next_sym]
                            if prev != f"s{next_state}":
                                print(f"冲突：状态 {state_id}，符号 '{next_sym}'，动作冲突 '{prev}' vs 's{next_state}'")
                        else:
                            action_table[state_id][next_sym] = f"s{next_state}"
                else:
                    # 非终结符，填Goto表
                    if (state_id, next_sym) in grammar.transitions:
                        next_state = grammar.transitions[(state_id, next_sym)]
                        goto_table[state_id][next_sym] = next_state

    return action_table, goto_table
