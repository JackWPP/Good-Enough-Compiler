#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词法分析模块

提供完整的词法分析功能，包括:
- 词法分析器核心引擎
- 正则表达式到自动机转换
- 多种编程语言的词法规则
- 可视化和调试工具
"""

from .analyzer import LexicalAnalyzer, LexicalRule, create_c_analyzer, create_pascal_analyzer, analyze_file
from .token import Token, TokenType, TokenCategory, get_token_category
from .automata import RegexToNFA, NFAToDFA, DFAMinimizer, NFA, DFA

__all__ = [
    # 核心类
    'LexicalAnalyzer',
    'LexicalRule',
    'Token',
    'TokenType',
    'TokenCategory',
    'get_token_category',
    
    # 自动机相关
    'RegexToNFA',
    'NFAToDFA', 
    'DFAMinimizer',
    'NFA',
    'DFA',
    
    # 便捷函数
    'create_c_analyzer',
    'create_pascal_analyzer',
    'analyze_file',
]

__version__ = "1.0.0"