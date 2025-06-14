from .slr1_check import build_slr1_table
from .lr1_dfa import build_lr1_output
from .ast_builder import ASTBuilder, ParseTreeToAST
from .ast_nodes import ASTVisualizer

def parse_sentence(grammar_text, sentence, method="SLR(1)", build_ast=True):

    tokens = sentence.strip().split() + ['$']
    lines = [line.strip() for line in grammar_text.strip().split('\n') if line.strip()]

    # 获取产生式编号列表（用于规约动作显示）
    prod_map = []
    for line in lines:
        left, right = map(str.strip, line.split('→'))
        for alt in right.split('|'):
            prod_map.append((left, alt.strip().split()))
    prod_map.insert(0, ("S'", [prod_map[0][0]]))  # 增广文法
    
    # 初始化AST构建器
    ast_builder = ASTBuilder() if build_ast else None

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
        step_info = {
            'step': step,
            'stack': str(stack),
            'symbols': " ".join(symbols),
            'input': " ".join(tokens[ip:]),
            'action': act if act else "error"
        }
        
        if not act:
            steps.append(step_info)
            break
        if act == 'acc':
            step_info['action'] = 'accept'
            steps.append(step_info)
            break
        elif act.startswith('s'):
            # 移入操作
            stack.append(int(act[1:]))
            symbols.append(token)
            
            # AST构建：推入终结符
            if ast_builder:
                ast_builder.push_terminal(token, token)
                step_info['ast_action'] = f'push_terminal({token})'
            
            ip += 1
            step_info['action'] = f'shift {act[1:]}'
            
        elif act.startswith('r'):
            # 归约操作
            prod_index = int(act[1:])
            lhs, rhs = prod_map[prod_index]
            
            # 记录产生式信息
            production_str = f"{lhs} -> {' '.join(rhs) if rhs else 'ε'}"
            step_info['production'] = production_str
            step_info['action'] = f'reduce by {production_str}'
            
            # 执行归约
            for _ in rhs:
                stack.pop()
                symbols.pop()
            symbols.append(lhs)
            
            # AST构建：执行归约
            if ast_builder:
                ast_node = ast_builder.reduce(production_str, lhs, rhs)
                step_info['ast_action'] = f'reduce_to({lhs})'
                step_info['ast_node_type'] = type(ast_node).__name__
            
            goto_state = goto_table[stack[-1]].get(lhs)
            if goto_state is None:
                step_info['action'] += "（无效 GOTO）"
                steps.append(step_info)
                break
            stack.append(goto_state)
            
        else:
            steps.append(step_info)
            break
        
        steps.append(step_info)
        step += 1

    # 构建返回结果
    result = {
        'steps': steps,
        'success': steps[-1]['action'] in ['accept', 'acc']
    }
    
    # 添加AST信息
    if ast_builder and result['success']:
        ast_root = ast_builder.get_ast_root()
        if ast_root:
            result['ast'] = {
                'root': ast_root.to_dict(),
                'tree_string': ASTVisualizer.to_tree_string(ast_root),
                'dot_graph': ASTVisualizer.to_dot(ast_root),
                'svg': ASTVisualizer.to_svg(ast_root)
            }
    
    return result
