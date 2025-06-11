#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译器主模块

本模块提供完整的编译器功能，包括：
- 词法分析 (lexical) - 已实现
- 语法分析 (syntax) - 规划中
- 语义分析 (semantic) - 规划中
- 代码生成 (codegen) - 规划中
- 工具模块 (utils) - 已实现
- 统一API (api) - 已实现

主要组件：
- lexical: 词法分析模块
- syntax: 语法分析模块（规划中）
- semantic: 语义分析模块（规划中）
- codegen: 代码生成模块（规划中）
- utils: 工具模块
- api: 统一编译器接口
"""

# 版本信息
__version__ = '1.0.0'
__author__ = 'Good-Enough-Compiler Team'

# 导入词法分析模块
from .lexical import (
    LexicalAnalyzer,
    Token,
    TokenType,
    TokenCategory,
    get_token_category,
    create_c_analyzer,
    create_pascal_analyzer,
    analyze_file
)

# 导入工具模块
from .utils import (
    visualize_nfa,
    visualize_dfa,
    render_transition_table,
    create_token_table_html,
    create_statistics_chart,
    read_file_safe,
    write_file_safe,
    detect_language,
    format_token_table,
    format_statistics,
    format_errors
)

# 导入API模块
from .api import (
    Compiler,
    CompilerConfig,
    CompilationResult,
    compile_file,
    compile_source,
    analyze_tokens,
    get_supported_languages,
    get_compiler_info
)

# 导出列表
__all__ = [
    # 词法分析
    'LexicalAnalyzer',
    'Token',
    'TokenType', 
    'TokenCategory',
    'get_token_category',
    'create_c_analyzer',
    'create_pascal_analyzer',
    'analyze_file',
    
    # 工具函数
    'visualize_nfa',
    'visualize_dfa',
    'render_transition_table',
    'create_token_table_html',
    'create_statistics_chart',
    'read_file_safe',
    'write_file_safe',
    'detect_language',
    'format_token_table',
    'format_statistics',
    'format_errors',
    
    # 编译器API
    'Compiler',
    'CompilerConfig',
    'CompilationResult',
    'compile_file',
    'compile_source',
    'analyze_tokens',
    'get_supported_languages',
    'get_compiler_info'
]