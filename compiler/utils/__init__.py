#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译器工具模块

提供编译器开发中常用的工具和实用函数：
- 可视化工具
- 文件处理工具
- 格式化工具
- 调试工具
"""

from .visualization import (
    visualize_nfa,
    visualize_dfa,
    render_transition_table,
    create_token_table_html,
    create_statistics_chart
)

from .file_utils import (
    read_file_safe,
    write_file_safe,
    ensure_directory,
    get_file_extension,
    detect_language,
    get_language_info
)

from .formatters import (
    format_token_table,
    format_error_list,
    format_errors,
    format_statistics,
    format_rules_table,
    create_html_report
)

__all__ = [
    # 可视化
    'visualize_nfa',
    'visualize_dfa', 
    'render_transition_table',
    'create_token_table_html',
    'create_statistics_chart',
    
    # 文件工具
    'read_file_safe',
    'write_file_safe',
    'ensure_directory',
    'get_file_extension',
    'detect_language',
    'get_language_info',
    
    # 格式化
    'format_token_table',
    'format_error_list',
    'format_errors',
    'format_statistics',
    'format_rules_table',
    'create_html_report'
]