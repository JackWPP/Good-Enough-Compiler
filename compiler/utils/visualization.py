#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可视化工具模块

提供编译器相关数据结构的可视化功能：
- NFA/DFA可视化
- 状态转移表渲染
- Token表格生成
- 统计图表生成
"""

import graphviz
import io
import pandas as pd
from PIL import Image
from typing import List, Dict, Set, Optional, Any
from ..lexical.automata import NFA, DFA
from ..lexical.token import Token, TokenType


def visualize_nfa(nfa: NFA, title: str = "NFA", format: str = 'png') -> Image.Image:
    """
    可视化NFA
    
    Args:
        nfa: 要可视化的NFA
        title: 图表标题
        format: 输出格式 ('png', 'svg', 'pdf')
    
    Returns:
        PIL Image对象
    """
    dot = graphviz.Digraph(comment=title)
    dot.attr(rankdir='LR')
    dot.attr('node', fontname='Arial')
    dot.attr('edge', fontname='Arial')
    
    # 添加状态
    for state in nfa.states:
        shape = 'doublecircle' if state.is_accept else 'circle'
        label = f"q{state.id}"
        if state.token_type:
            label += f"\n{state.token_type.value}"
        
        color = 'lightblue' if state.is_accept else 'white'
        dot.node(str(state.id), label, shape=shape, style='filled', fillcolor=color)
    
    # 添加转移
    edge_labels = {}  # 用于合并相同起点和终点的边
    
    for state in nfa.states:
        for symbol, targets in state.transitions.items():
            for target in targets:
                edge_key = (state.id, target.id)
                label = 'ε' if symbol == 'ε' else symbol
                
                if edge_key in edge_labels:
                    edge_labels[edge_key] += f", {label}"
                else:
                    edge_labels[edge_key] = label
    
    # 添加边
    for (from_id, to_id), label in edge_labels.items():
        dot.edge(str(from_id), str(to_id), label=label)
    
    # 标记开始状态
    if nfa.start_state:
        dot.node('start', '', shape='point')
        dot.edge('start', str(nfa.start_state.id))
    
    # 渲染为图片
    if format.lower() == 'svg':
        svg_data = dot.pipe(format='svg')
        return svg_data.decode('utf-8')
    else:
        img_data = dot.pipe(format='png')
        return Image.open(io.BytesIO(img_data))


def visualize_dfa(dfa: DFA, title: str = "DFA", format: str = 'png') -> Image.Image:
    """
    可视化DFA
    
    Args:
        dfa: 要可视化的DFA
        title: 图表标题
        format: 输出格式
    
    Returns:
        PIL Image对象或SVG字符串
    """
    dot = graphviz.Digraph(comment=title)
    dot.attr(rankdir='LR')
    dot.attr('node', fontname='Arial')
    dot.attr('edge', fontname='Arial')
    
    # 添加状态
    for state_id in dfa.states:
        shape = 'doublecircle' if state_id in dfa.accept_states else 'circle'
        label = state_id
        if state_id in dfa.token_types:
            label += f"\n{dfa.token_types[state_id].value}"
        
        color = 'lightgreen' if state_id in dfa.accept_states else 'white'
        dot.node(state_id, label, shape=shape, style='filled', fillcolor=color)
    
    # 添加转移
    edge_labels = {}  # 用于合并相同起点和终点的边
    
    for (from_state, symbol), to_state in dfa.transitions.items():
        edge_key = (from_state, to_state)
        
        if edge_key in edge_labels:
            edge_labels[edge_key] += f", {symbol}"
        else:
            edge_labels[edge_key] = symbol
    
    # 添加边
    for (from_state, to_state), label in edge_labels.items():
        dot.edge(from_state, to_state, label=label)
    
    # 标记开始状态
    if dfa.start_state:
        dot.node('start', '', shape='point')
        dot.edge('start', dfa.start_state)
    
    # 渲染为图片
    if format.lower() == 'svg':
        svg_data = dot.pipe(format='svg')
        return svg_data.decode('utf-8')
    else:
        img_data = dot.pipe(format='png')
        return Image.open(io.BytesIO(img_data))


def render_transition_table(dfa: DFA) -> str:
    """
    渲染DFA状态转移表为HTML
    
    Args:
        dfa: DFA对象
    
    Returns:
        HTML格式的状态转移表
    """
    if not dfa.states:
        return "<p>DFA为空</p>"
    
    # 获取所有状态和符号
    states = sorted(dfa.states.keys())
    symbols = sorted(dfa.alphabet)
    
    # 构建表格
    html = ['<table border="1" style="border-collapse: collapse; margin: 10px;">']
    
    # 表头
    html.append('<tr style="background-color: #f0f0f0;">')
    html.append('<th style="padding: 8px;">状态</th>')
    for symbol in symbols:
        html.append(f'<th style="padding: 8px;">{symbol}</th>')
    html.append('<th style="padding: 8px;">接受状态</th>')
    html.append('<th style="padding: 8px;">Token类型</th>')
    html.append('</tr>')
    
    # 表格内容
    for state in states:
        # 标记开始状态和接受状态
        state_style = ""
        if state == dfa.start_state:
            state_style = 'background-color: #e6f3ff;'  # 浅蓝色
        elif state in dfa.accept_states:
            state_style = 'background-color: #e6ffe6;'  # 浅绿色
        
        html.append(f'<tr style="{state_style}">')
        
        # 状态名
        state_display = state
        if state == dfa.start_state:
            state_display = f"→{state}"
        html.append(f'<td style="padding: 8px; font-weight: bold;">{state_display}</td>')
        
        # 转移
        for symbol in symbols:
            target = dfa.get_transition(state, symbol)
            target_display = target if target else '-'
            html.append(f'<td style="padding: 8px; text-align: center;">{target_display}</td>')
        
        # 接受状态
        is_accept = '是' if state in dfa.accept_states else '否'
        html.append(f'<td style="padding: 8px; text-align: center;">{is_accept}</td>')
        
        # Token类型
        token_type = dfa.token_types.get(state, '')
        token_display = token_type.value if token_type else '-'
        html.append(f'<td style="padding: 8px;">{token_display}</td>')
        
        html.append('</tr>')
    
    html.append('</table>')
    
    # 添加说明
    html.append('<div style="margin: 10px; font-size: 12px; color: #666;">')
    html.append('<p><strong>说明:</strong></p>')
    html.append('<ul>')
    html.append('<li>→ 表示开始状态</li>')
    html.append('<li>蓝色背景表示开始状态</li>')
    html.append('<li>绿色背景表示接受状态</li>')
    html.append('<li>- 表示无转移</li>')
    html.append('</ul>')
    html.append('</div>')
    
    return '\n'.join(html)


def create_token_table_html(tokens: List[Token]) -> str:
    """
    创建Token表格的HTML
    
    Args:
        tokens: Token列表
    
    Returns:
        HTML格式的Token表格
    """
    if not tokens:
        return "<p>没有Token</p>"
    
    html = ['<table border="1" style="border-collapse: collapse; margin: 10px;">']
    
    # 表头
    html.append('<tr style="background-color: #f0f0f0;">')
    html.append('<th style="padding: 8px;">序号</th>')
    html.append('<th style="padding: 8px;">Token类型</th>')
    html.append('<th style="padding: 8px;">值</th>')
    html.append('<th style="padding: 8px;">行号</th>')
    html.append('<th style="padding: 8px;">列号</th>')
    html.append('<th style="padding: 8px;">分类</th>')
    html.append('</tr>')
    
    # 表格内容
    for i, token in enumerate(tokens, 1):
        # 根据Token类型设置颜色
        row_style = ""
        if token.type == TokenType.ERROR:
            row_style = 'background-color: #ffe6e6;'  # 红色
        elif token.is_keyword():
            row_style = 'background-color: #e6e6ff;'  # 蓝色
        elif token.is_operator():
            row_style = 'background-color: #fff0e6;'  # 橙色
        elif token.is_literal():
            row_style = 'background-color: #e6ffe6;'  # 绿色
        
        html.append(f'<tr style="{row_style}">')
        html.append(f'<td style="padding: 8px; text-align: center;">{i}</td>')
        html.append(f'<td style="padding: 8px;">{token.type.value}</td>')
        
        # 转义HTML特殊字符
        value = token.value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        html.append(f'<td style="padding: 8px; font-family: monospace;">{value}</td>')
        
        html.append(f'<td style="padding: 8px; text-align: center;">{token.line}</td>')
        html.append(f'<td style="padding: 8px; text-align: center;">{token.column}</td>')
        
        # Token分类
        category = "其他"
        if token.is_keyword():
            category = "关键字"
        elif token.is_operator():
            category = "运算符"
        elif token.is_literal():
            category = "字面量"
        elif token.type == TokenType.IDENTIFIER:
            category = "标识符"
        elif token.type in [TokenType.SEMICOLON, TokenType.COMMA, TokenType.LPAREN, TokenType.RPAREN]:
            category = "分隔符"
        
        html.append(f'<td style="padding: 8px;">{category}</td>')
        html.append('</tr>')
    
    html.append('</table>')
    
    # 添加颜色说明
    html.append('<div style="margin: 10px; font-size: 12px; color: #666;">')
    html.append('<p><strong>颜色说明:</strong></p>')
    html.append('<ul>')
    html.append('<li style="background-color: #e6e6ff; padding: 2px;">蓝色 - 关键字</li>')
    html.append('<li style="background-color: #fff0e6; padding: 2px;">橙色 - 运算符</li>')
    html.append('<li style="background-color: #e6ffe6; padding: 2px;">绿色 - 字面量</li>')
    html.append('<li style="background-color: #ffe6e6; padding: 2px;">红色 - 错误</li>')
    html.append('</ul>')
    html.append('</div>')
    
    return '\n'.join(html)


def create_statistics_chart(stats: Dict[str, int]) -> str:
    """
    创建统计图表的HTML
    
    Args:
        stats: 统计数据字典
    
    Returns:
        HTML格式的统计图表
    """
    if not stats:
        return "<p>没有统计数据</p>"
    
    # 排序统计数据
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    # 计算总数
    total = sum(stats.values())
    
    html = ['<div style="margin: 10px;">']
    html.append('<h3>Token统计</h3>')
    
    # 创建条形图
    html.append('<div style="margin: 20px 0;">')
    
    max_count = max(stats.values()) if stats else 1
    
    for token_type, count in sorted_stats:
        percentage = (count / total) * 100 if total > 0 else 0
        bar_width = (count / max_count) * 300  # 最大宽度300px
        
        html.append('<div style="margin: 5px 0; display: flex; align-items: center;">')
        html.append(f'<div style="width: 150px; text-align: right; padding-right: 10px; font-size: 12px;">{token_type}:</div>')
        html.append(f'<div style="width: {bar_width}px; height: 20px; background-color: #4CAF50; margin-right: 10px;"></div>')
        html.append(f'<div style="font-size: 12px;">{count} ({percentage:.1f}%)</div>')
        html.append('</div>')
    
    html.append('</div>')
    
    # 添加总计
    html.append(f'<p><strong>总计: {total} 个Token</strong></p>')
    
    html.append('</div>')
    
    return '\n'.join(html)


def export_automata_dot(nfa: Optional[NFA] = None, dfa: Optional[DFA] = None, filename: str = "automata.dot") -> str:
    """
    导出自动机为DOT格式文件
    
    Args:
        nfa: NFA对象
        dfa: DFA对象
        filename: 输出文件名
    
    Returns:
        DOT格式字符串
    """
    dot_content = []
    
    if nfa:
        dot_content.append("// NFA")
        dot_content.append("digraph NFA {")
        dot_content.append("  rankdir=LR;")
        
        # 添加状态
        for state in nfa.states:
            shape = 'doublecircle' if state.is_accept else 'circle'
            label = f"q{state.id}"
            if state.token_type:
                label += f"\\n{state.token_type.value}"
            dot_content.append(f'  {state.id} [label="{label}", shape={shape}];')
        
        # 添加转移
        for state in nfa.states:
            for symbol, targets in state.transitions.items():
                for target in targets:
                    label = 'ε' if symbol == 'ε' else symbol
                    dot_content.append(f'  {state.id} -> {target.id} [label="{label}"];')
        
        # 开始状态
        if nfa.start_state:
            dot_content.append('  start [shape=point];')
            dot_content.append(f'  start -> {nfa.start_state.id};')
        
        dot_content.append("}")
        dot_content.append("")
    
    if dfa:
        dot_content.append("// DFA")
        dot_content.append("digraph DFA {")
        dot_content.append("  rankdir=LR;")
        
        # 添加状态
        for state_id in dfa.states:
            shape = 'doublecircle' if state_id in dfa.accept_states else 'circle'
            label = state_id
            if state_id in dfa.token_types:
                label += f"\\n{dfa.token_types[state_id].value}"
            dot_content.append(f'  "{state_id}" [label="{label}", shape={shape}];')
        
        # 添加转移
        for (from_state, symbol), to_state in dfa.transitions.items():
            dot_content.append(f'  "{from_state}" -> "{to_state}" [label="{symbol}"];')
        
        # 开始状态
        if dfa.start_state:
            dot_content.append('  start [shape=point];')
            dot_content.append(f'  start -> "{dfa.start_state}";')
        
        dot_content.append("}")
    
    dot_string = "\n".join(dot_content)
    
    # 写入文件
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(dot_string)
    except Exception as e:
        print(f"写入DOT文件失败: {e}")
    
    return dot_string


def create_comparison_table(nfa: NFA, dfa: DFA, minimized_dfa: Optional[DFA] = None) -> str:
    """
    创建自动机比较表格
    
    Args:
        nfa: NFA对象
        dfa: DFA对象
        minimized_dfa: 最小化DFA对象
    
    Returns:
        HTML格式的比较表格
    """
    html = ['<table border="1" style="border-collapse: collapse; margin: 10px;">']
    
    # 表头
    html.append('<tr style="background-color: #f0f0f0;">')
    html.append('<th style="padding: 8px;">属性</th>')
    html.append('<th style="padding: 8px;">NFA</th>')
    html.append('<th style="padding: 8px;">DFA</th>')
    if minimized_dfa:
        html.append('<th style="padding: 8px;">最小化DFA</th>')
    html.append('</tr>')
    
    # 状态数
    html.append('<tr>')
    html.append('<td style="padding: 8px; font-weight: bold;">状态数</td>')
    html.append(f'<td style="padding: 8px; text-align: center;">{len(nfa.states)}</td>')
    html.append(f'<td style="padding: 8px; text-align: center;">{len(dfa.states)}</td>')
    if minimized_dfa:
        html.append(f'<td style="padding: 8px; text-align: center;">{len(minimized_dfa.states)}</td>')
    html.append('</tr>')
    
    # 接受状态数
    html.append('<tr>')
    html.append('<td style="padding: 8px; font-weight: bold;">接受状态数</td>')
    html.append(f'<td style="padding: 8px; text-align: center;">{len(nfa.accept_states)}</td>')
    html.append(f'<td style="padding: 8px; text-align: center;">{len(dfa.accept_states)}</td>')
    if minimized_dfa:
        html.append(f'<td style="padding: 8px; text-align: center;">{len(minimized_dfa.accept_states)}</td>')
    html.append('</tr>')
    
    # 转移数
    nfa_transitions = sum(len(targets) for state in nfa.states for targets in state.transitions.values())
    dfa_transitions = len(dfa.transitions)
    
    html.append('<tr>')
    html.append('<td style="padding: 8px; font-weight: bold;">转移数</td>')
    html.append(f'<td style="padding: 8px; text-align: center;">{nfa_transitions}</td>')
    html.append(f'<td style="padding: 8px; text-align: center;">{dfa_transitions}</td>')
    if minimized_dfa:
        min_dfa_transitions = len(minimized_dfa.transitions)
        html.append(f'<td style="padding: 8px; text-align: center;">{min_dfa_transitions}</td>')
    html.append('</tr>')
    
    # 字母表大小
    html.append('<tr>')
    html.append('<td style="padding: 8px; font-weight: bold;">字母表大小</td>')
    html.append(f'<td style="padding: 8px; text-align: center;">{len(nfa.alphabet)}</td>')
    html.append(f'<td style="padding: 8px; text-align: center;">{len(dfa.alphabet)}</td>')
    if minimized_dfa:
        html.append(f'<td style="padding: 8px; text-align: center;">{len(minimized_dfa.alphabet)}</td>')
    html.append('</tr>')
    
    html.append('</table>')
    
    return '\n'.join(html)