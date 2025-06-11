#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式化工具模块

提供各种格式化和美化输出功能：
- Token表格格式化
- 统计信息格式化
- 错误信息格式化
- 代码高亮
- 报告生成
"""

from typing import List, Dict, Any, Optional, Tuple
from ..lexical.token import Token, TokenType, TokenCategory, get_token_category
import html
import json


def format_token_table(tokens: List[Token], show_position: bool = True, 
                      show_category: bool = True, max_width: int = 80) -> str:
    """
    格式化Token表格
    
    Args:
        tokens: Token列表
        show_position: 是否显示位置信息
        show_category: 是否显示分类信息
        max_width: 最大宽度
    
    Returns:
        格式化的表格字符串
    """
    if not tokens:
        return "没有Token\n"
    
    # 计算列宽
    headers = ['序号', '类型', '值']
    if show_position:
        headers.extend(['行', '列'])
    if show_category:
        headers.append('分类')
    
    # 计算每列的最大宽度
    col_widths = [len(h) for h in headers]
    
    rows = []
    for i, token in enumerate(tokens):
        row = [
            str(i + 1),
            token.type.name,
            repr(token.value) if len(token.value) <= 20 else repr(token.value[:17] + '...')
        ]
        
        if show_position:
            row.extend([str(token.line), str(token.column)])
        
        if show_category:
            category = get_token_category(token.type)
            row.append(category.name if category else 'UNKNOWN')
        
        rows.append(row)
        
        # 更新列宽
        for j, cell in enumerate(row):
            col_widths[j] = max(col_widths[j], len(cell))
    
    # 限制最大宽度
    total_width = sum(col_widths) + len(col_widths) * 3 + 1
    if total_width > max_width:
        # 缩减值列的宽度
        value_col_idx = 2
        reduction = total_width - max_width
        col_widths[value_col_idx] = max(10, col_widths[value_col_idx] - reduction)
    
    # 生成表格
    result = []
    
    # 表头
    header_line = '|' + '|'.join(f' {h:<{w}} ' for h, w in zip(headers, col_widths)) + '|'
    result.append(header_line)
    
    # 分隔线
    separator = '|' + '|'.join('-' * (w + 2) for w in col_widths) + '|'
    result.append(separator)
    
    # 数据行
    for row in rows:
        # 截断过长的值
        truncated_row = []
        for i, (cell, width) in enumerate(zip(row, col_widths)):
            if len(cell) > width:
                truncated_row.append(cell[:width-3] + '...')
            else:
                truncated_row.append(cell)
        
        data_line = '|' + '|'.join(f' {cell:<{w}} ' for cell, w in zip(truncated_row, col_widths)) + '|'
        result.append(data_line)
    
    return '\n'.join(result) + '\n'


def format_statistics(stats: Dict[str, Any]) -> str:
    """
    格式化统计信息
    
    Args:
        stats: 统计信息字典
    
    Returns:
        格式化的统计信息字符串
    """
    result = []
    result.append("=== 词法分析统计 ===")
    
    # 基本统计
    if 'total_tokens' in stats:
        result.append(f"总Token数: {stats['total_tokens']}")
    
    if 'total_lines' in stats:
        result.append(f"总行数: {stats['total_lines']}")
    
    if 'total_characters' in stats:
        result.append(f"总字符数: {stats['total_characters']}")
    
    # Token类型统计
    if 'token_counts' in stats:
        result.append("\n--- Token类型统计 ---")
        token_counts = stats['token_counts']
        
        # 按数量排序
        sorted_counts = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)
        
        for token_type, count in sorted_counts:
            percentage = (count / stats.get('total_tokens', 1)) * 100
            result.append(f"{token_type:<20}: {count:>6} ({percentage:>5.1f}%)")
    
    # 分类统计
    if 'category_counts' in stats:
        result.append("\n--- Token分类统计 ---")
        category_counts = stats['category_counts']
        
        for category, count in sorted(category_counts.items()):
            percentage = (count / stats.get('total_tokens', 1)) * 100
            result.append(f"{category:<15}: {count:>6} ({percentage:>5.1f}%)")
    
    # 错误统计
    if 'error_count' in stats:
        result.append(f"\n错误数: {stats['error_count']}")
    
    # 处理时间
    if 'processing_time' in stats:
        result.append(f"处理时间: {stats['processing_time']:.3f}秒")
    
    return '\n'.join(result) + '\n'


def format_errors(errors: List[Dict[str, Any]]) -> str:
    """
    格式化错误信息
    
    Args:
        errors: 错误信息列表
    
    Returns:
        格式化的错误信息字符串
    """
    if not errors:
        return "没有错误\n"
    
    result = []
    result.append(f"=== 发现 {len(errors)} 个错误 ===")
    
    for i, error in enumerate(errors, 1):
        result.append(f"\n错误 {i}:")
        
        if 'line' in error and 'column' in error:
            result.append(f"  位置: 第{error['line']}行，第{error['column']}列")
        
        if 'message' in error:
            result.append(f"  信息: {error['message']}")
        
        if 'context' in error:
            result.append(f"  上下文: {repr(error['context'])}")
        
        if 'suggestion' in error:
            result.append(f"  建议: {error['suggestion']}")
    
    return '\n'.join(result) + '\n'


def format_error_list(errors: List[str]) -> str:
    """
    格式化错误列表
    
    Args:
        errors: 错误信息字符串列表
    
    Returns:
        格式化的错误信息字符串
    """
    if not errors:
        return "没有错误\n"
    
    result = []
    result.append(f"=== 发现 {len(errors)} 个错误 ===")
    
    for i, error in enumerate(errors, 1):
        result.append(f"\n错误 {i}: {error}")
    
    return '\n'.join(result) + '\n'


def format_rules_table(rules: List[Dict[str, Any]]) -> str:
    """
    格式化规则表格
    
    Args:
        rules: 规则列表
    
    Returns:
        格式化的规则表格字符串
    """
    if not rules:
        return "没有规则\n"
    
    result = []
    result.append("=== 词法规则表 ===")
    result.append(f"{'序号':<4} {'类型':<15} {'模式':<30} {'描述':<20}")
    result.append("-" * 70)
    
    for i, rule in enumerate(rules, 1):
        rule_type = rule.get('type', 'UNKNOWN')
        pattern = rule.get('pattern', '')
        description = rule.get('description', '')
        
        # 截断过长的模式
        if len(pattern) > 27:
            pattern = pattern[:24] + '...'
        
        # 截断过长的描述
        if len(description) > 17:
            description = description[:14] + '...'
        
        result.append(f"{i:<4} {rule_type:<15} {pattern:<30} {description:<20}")
    
    return '\n'.join(result) + '\n'


def format_code_with_line_numbers(code: str, start_line: int = 1, 
                                 highlight_lines: Optional[List[int]] = None) -> str:
    """
    格式化代码并添加行号
    
    Args:
        code: 源代码
        start_line: 起始行号
        highlight_lines: 需要高亮的行号列表
    
    Returns:
        带行号的格式化代码
    """
    lines = code.split('\n')
    highlight_lines = highlight_lines or []
    
    # 计算行号宽度
    max_line_num = start_line + len(lines) - 1
    line_num_width = len(str(max_line_num))
    
    result = []
    for i, line in enumerate(lines):
        line_num = start_line + i
        prefix = ">>>" if line_num in highlight_lines else "   "
        formatted_line = f"{prefix} {line_num:>{line_num_width}} | {line}"
        result.append(formatted_line)
    
    return '\n'.join(result)


def create_html_report(tokens: List[Token], stats: Dict[str, Any], 
                      errors: List[Dict[str, Any]], source_code: str = "") -> str:
    """
    创建HTML格式的分析报告
    
    Args:
        tokens: Token列表
        stats: 统计信息
        errors: 错误信息
        source_code: 源代码
    
    Returns:
        HTML格式的报告
    """
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>词法分析报告</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #333;
            border-bottom: 2px solid #007acc;
            padding-bottom: 5px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #007acc;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .code-block {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            white-space: pre;
        }}
        .error {{
            background-color: #ffebee;
            border-left: 4px solid #f44336;
            padding: 10px;
            margin: 10px 0;
        }}
        .error-title {{
            color: #f44336;
            font-weight: bold;
        }}
        .token-type {{
            font-weight: bold;
            color: #007acc;
        }}
        .token-value {{
            font-family: 'Courier New', monospace;
            background-color: #f0f0f0;
            padding: 2px 4px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>词法分析报告</h1>
        
        <h2>统计概览</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{stats.get('total_tokens', 0)}</div>
                <div class="stat-label">总Token数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats.get('total_lines', 0)}</div>
                <div class="stat-label">总行数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(errors)}</div>
                <div class="stat-label">错误数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats.get('processing_time', 0):.3f}s</div>
                <div class="stat-label">处理时间</div>
            </div>
        </div>
"""
    
    # 添加错误信息
    if errors:
        html_content += "\n        <h2>错误信息</h2>\n"
        for i, error in enumerate(errors, 1):
            html_content += f"""
        <div class="error">
            <div class="error-title">错误 {i}</div>
            <div>位置: 第{error.get('line', '?')}行，第{error.get('column', '?')}列</div>
            <div>信息: {html.escape(error.get('message', ''))}</div>
        </div>
"""
    
    # 添加Token表格
    if tokens:
        html_content += "\n        <h2>Token列表</h2>\n        <table>\n"
        html_content += "            <tr><th>序号</th><th>类型</th><th>值</th><th>行</th><th>列</th><th>分类</th></tr>\n"
        
        for i, token in enumerate(tokens[:100]):  # 限制显示前100个Token
            category = get_token_category(token.type)
            category_name = category.name if category else 'UNKNOWN'
            
            html_content += f"""
            <tr>
                <td>{i + 1}</td>
                <td><span class="token-type">{html.escape(token.type.name)}</span></td>
                <td><span class="token-value">{html.escape(repr(token.value))}</span></td>
                <td>{token.line}</td>
                <td>{token.column}</td>
                <td>{category_name}</td>
            </tr>
"""
        
        if len(tokens) > 100:
            html_content += f"            <tr><td colspan='6'>... 还有 {len(tokens) - 100} 个Token</td></tr>\n"
        
        html_content += "        </table>\n"
    
    # 添加源代码
    if source_code:
        html_content += "\n        <h2>源代码</h2>\n"
        html_content += f'        <div class="code-block">{html.escape(source_code)}</div>\n'
    
    html_content += """
    </div>
</body>
</html>
"""
    
    return html_content


def create_json_report(tokens: List[Token], stats: Dict[str, Any], 
                      errors: List[Dict[str, Any]]) -> str:
    """
    创建JSON格式的分析报告
    
    Args:
        tokens: Token列表
        stats: 统计信息
        errors: 错误信息
    
    Returns:
        JSON格式的报告
    """
    # 转换Token为字典
    token_dicts = []
    for token in tokens:
        category = get_token_category(token.type)
        token_dict = {
            'type': token.type.name,
            'value': token.value,
            'line': token.line,
            'column': token.column,
            'category': category.name if category else 'UNKNOWN'
        }
        token_dicts.append(token_dict)
    
    report = {
        'metadata': {
            'version': '1.0',
            'generator': 'Good-Enough-Compiler',
            'timestamp': stats.get('timestamp', '')
        },
        'statistics': stats,
        'tokens': token_dicts,
        'errors': errors
    }
    
    return json.dumps(report, ensure_ascii=False, indent=2)


def format_transition_table(table: Dict[Tuple[int, str], int], 
                          states: List[int], alphabet: List[str]) -> str:
    """
    格式化状态转移表
    
    Args:
        table: 状态转移表
        states: 状态列表
        alphabet: 字母表
    
    Returns:
        格式化的转移表字符串
    """
    if not states or not alphabet:
        return "空转移表\n"
    
    # 计算列宽
    state_width = max(len(str(s)) for s in states)
    state_width = max(state_width, len("状态"))
    
    symbol_widths = [max(len(symbol), 3) for symbol in alphabet]
    
    # 表头
    result = []
    header = f"{'状态':<{state_width}}"
    for symbol, width in zip(alphabet, symbol_widths):
        header += f" | {symbol:<{width}}"
    result.append(header)
    
    # 分隔线
    separator = "-" * state_width
    for width in symbol_widths:
        separator += "-|-" + "-" * width
    result.append(separator)
    
    # 数据行
    for state in sorted(states):
        row = f"{state:<{state_width}}"
        for symbol, width in zip(alphabet, symbol_widths):
            next_state = table.get((state, symbol), "")
            row += f" | {str(next_state):<{width}}"
        result.append(row)
    
    return "\n".join(result) + "\n"


def format_automata_info(nfa_states: int, dfa_states: int, 
                        minimized_states: int, alphabet_size: int) -> str:
    """
    格式化自动机信息
    
    Args:
        nfa_states: NFA状态数
        dfa_states: DFA状态数
        minimized_states: 最小化DFA状态数
        alphabet_size: 字母表大小
    
    Returns:
        格式化的自动机信息
    """
    result = []
    result.append("=== 自动机转换信息 ===")
    result.append(f"NFA状态数: {nfa_states}")
    result.append(f"DFA状态数: {dfa_states}")
    result.append(f"最小化DFA状态数: {minimized_states}")
    result.append(f"字母表大小: {alphabet_size}")
    
    if dfa_states > 0:
        reduction_ratio = (1 - minimized_states / dfa_states) * 100
        result.append(f"状态减少率: {reduction_ratio:.1f}%")
    
    return "\n".join(result) + "\n"


def create_comparison_table(data: List[Dict[str, Any]], 
                          columns: List[str], title: str = "") -> str:
    """
    创建对比表格
    
    Args:
        data: 数据列表
        columns: 列名列表
        title: 表格标题
    
    Returns:
        格式化的对比表格
    """
    if not data or not columns:
        return "没有数据\n"
    
    result = []
    if title:
        result.append(f"=== {title} ===")
    
    # 计算列宽
    col_widths = [len(col) for col in columns]
    for row in data:
        for i, col in enumerate(columns):
            value = str(row.get(col, ""))
            col_widths[i] = max(col_widths[i], len(value))
    
    # 表头
    header = "|"
    for col, width in zip(columns, col_widths):
        header += f" {col:<{width}} |"
    result.append(header)
    
    # 分隔线
    separator = "|"
    for width in col_widths:
        separator += "-" * (width + 2) + "|"
    result.append(separator)
    
    # 数据行
    for row in data:
        data_line = "|"
        for col, width in zip(columns, col_widths):
            value = str(row.get(col, ""))
            data_line += f" {value:<{width}} |"
        result.append(data_line)
    
    return "\n".join(result) + "\n"


def highlight_code_syntax(code: str, language: str = 'c') -> str:
    """
    简单的语法高亮（文本版本）
    
    Args:
        code: 源代码
        language: 编程语言
    
    Returns:
        带有简单标记的代码
    """
    # 这是一个简化版本，实际应用中可以使用pygments等库
    keywords = {
        'c': ['int', 'char', 'float', 'double', 'void', 'if', 'else', 'for', 'while', 
              'do', 'switch', 'case', 'default', 'break', 'continue', 'return',
              'struct', 'union', 'enum', 'typedef', 'static', 'extern', 'const'],
        'pascal': ['program', 'begin', 'end', 'var', 'const', 'type', 'procedure', 
                  'function', 'if', 'then', 'else', 'while', 'do', 'for', 'to',
                  'repeat', 'until', 'case', 'of', 'array', 'record', 'set']
    }
    
    lang_keywords = keywords.get(language.lower(), [])
    
    # 简单的关键字标记
    result = code
    for keyword in lang_keywords:
        # 使用简单的标记，避免破坏代码结构
        result = result.replace(f' {keyword} ', f' [{keyword}] ')
        result = result.replace(f'\n{keyword} ', f'\n[{keyword}] ')
        result = result.replace(f' {keyword}\n', f' [{keyword}]\n')
    
    return result


def create_summary_report(analysis_results: Dict[str, Any]) -> str:
    """
    创建分析摘要报告
    
    Args:
        analysis_results: 分析结果字典
    
    Returns:
        摘要报告字符串
    """
    result = []
    result.append("=== 词法分析摘要报告 ===")
    
    # 基本信息
    if 'filename' in analysis_results:
        result.append(f"文件: {analysis_results['filename']}")
    
    if 'language' in analysis_results:
        result.append(f"语言: {analysis_results['language']}")
    
    # 统计信息
    stats = analysis_results.get('statistics', {})
    result.append(f"\n总Token数: {stats.get('total_tokens', 0)}")
    result.append(f"总行数: {stats.get('total_lines', 0)}")
    result.append(f"错误数: {len(analysis_results.get('errors', []))}")
    
    # 主要Token类型
    token_counts = stats.get('token_counts', {})
    if token_counts:
        result.append("\n主要Token类型:")
        sorted_counts = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)
        for token_type, count in sorted_counts[:5]:
            percentage = (count / stats.get('total_tokens', 1)) * 100
            result.append(f"  {token_type}: {count} ({percentage:.1f}%)")
    
    # 处理状态
    if analysis_results.get('errors'):
        result.append("\n状态: 发现错误")
    else:
        result.append("\n状态: 分析成功")
    
    return "\n".join(result) + "\n"