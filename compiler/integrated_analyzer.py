#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成分析器模块

将词法分析和语法分析集成在一起，提供完整的编译前端功能。
包括：
- 词法分析到语法分析的Token流转换
- 统一的分析接口
- 错误处理和报告
- 分析结果的可视化
"""

import os
import sys
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

# 导入词法分析模块
from .lexical import LexicalAnalyzer, Token, TokenType, create_c_analyzer, create_pascal_analyzer

# 导入语法分析模块
from .syntax.first_follow import process_first_follow
from .syntax.lr0_dfa import build_lr0_output
from .syntax.slr1_check import check_slr1, build_slr1_table
from .syntax.lr1_dfa import build_lr1_output
from .syntax.parser_engine import parse_sentence


@dataclass
class AnalysisResult:
    """分析结果数据类"""
    # 词法分析结果
    tokens: List[Token]
    lexical_errors: List[str]
    
    # 语法分析结果
    first_follow: str
    slr1_result: str
    is_slr1: bool
    lr0_states: str
    lr0_transitions: str
    lr0_svg: str
    action_table: Dict
    goto_table: Dict
    lr1_svg: str
    parse_steps: List[List[str]]
    syntax_errors: List[str]
    
    # 统计信息
    token_count: int
    analysis_time: float
    success: bool


class IntegratedAnalyzer:
    """集成分析器类
    
    将词法分析和语法分析集成在一起的主要类。
    """
    
    def __init__(self, language: str = 'c'):
        """
        初始化集成分析器
        
        Args:
            language: 目标语言 ('c' 或 'pascal')
        """
        self.language = language
        self.lexical_analyzer = self._create_lexical_analyzer()
        self.grammar_text = self._get_default_grammar()
        self.errors = []
        
    def _create_lexical_analyzer(self) -> LexicalAnalyzer:
        """创建词法分析器"""
        if self.language.lower() == 'c':
            return create_c_analyzer()
        elif self.language.lower() == 'pascal':
            return create_pascal_analyzer()
        else:
            # 默认使用Pascal分析器
            return create_pascal_analyzer()
    
    def _get_default_grammar(self) -> str:
        """获取默认文法"""
        if self.language.lower() == 'c':
            # C语言简化文法
            return """E → E + T | E - T | T
T → T * F | T / F | F
F → ( E ) | id | num"""
        else:
            # Pascal语言简化文法
            return """program → program id ; block .
block → var_decl stmt_list
var_decl → var id : type ;
stmt_list → stmt_list ; stmt | stmt
stmt → id := expr | if expr then stmt | while expr do stmt
expr → expr + term | expr - term | term
term → term * factor | term / factor | factor
factor → ( expr ) | id | num"""
    
    def set_grammar(self, grammar_text: str):
        """设置自定义文法
        
        Args:
            grammar_text: 文法产生式文本
        """
        self.grammar_text = grammar_text
    
    def tokens_to_grammar_symbols(self, tokens: List[Token]) -> str:
        """将Token序列转换为文法符号序列
        
        Args:
            tokens: Token列表
            
        Returns:
            文法符号序列字符串
        """
        symbols = []
        for token in tokens:
            if token.type == TokenType.EOF:
                continue
            elif token.type == TokenType.WHITESPACE or token.type == TokenType.NEWLINE:
                continue
            elif token.type == TokenType.COMMENT:
                continue
            elif token.type == TokenType.IDENTIFIER:
                symbols.append('id')
            elif token.type == TokenType.NUMBER or token.type == TokenType.INTEGER_LITERAL:
                symbols.append('num')
            elif token.type == TokenType.PLUS:
                symbols.append('+')
            elif token.type == TokenType.MINUS:
                symbols.append('-')
            elif token.type == TokenType.MULTIPLY:
                symbols.append('*')
            elif token.type == TokenType.DIVIDE:
                symbols.append('/')
            elif token.type == TokenType.LPAREN:
                symbols.append('(')
            elif token.type == TokenType.RPAREN:
                symbols.append(')')
            elif token.type == TokenType.SEMICOLON:
                symbols.append(';')
            elif token.type == TokenType.ASSIGN:
                symbols.append(':=')
            elif token.type == TokenType.EQUAL:
                symbols.append('=')
            else:
                # 其他Token类型映射为其值或类型名
                if token.value:
                    symbols.append(token.value)
                else:
                    symbols.append(token.type.value.lower())
        
        return ' '.join(symbols)
    
    def analyze_code(self, source_code: str, sentence: str = "") -> AnalysisResult:
        """分析源代码
        
        Args:
            source_code: 源代码文本
            sentence: 可选的待分析句子（用于语法分析演示）
            
        Returns:
            分析结果
        """
        import time
        start_time = time.time()
        
        try:
            # 1. 词法分析
            tokens = self.lexical_analyzer.analyze(source_code)
            lexical_errors = self.lexical_analyzer.get_errors() if hasattr(self.lexical_analyzer, 'get_errors') else []
            
            # 2. 如果没有提供句子，从Token生成
            if not sentence.strip() and tokens:
                sentence = self.tokens_to_grammar_symbols(tokens)
            
            # 3. 语法分析
            try:
                # 处理First/Follow集
                g = process_first_follow(self.grammar_text)
                ff_str = g.get_first_follow_str()
                
                # 判断是否为SLR(1)
                slr_conflicts = check_slr1(g)
                is_slr1 = not slr_conflicts
                slr_result = "SLR(1) 分析表无冲突，文法是 SLR(1) 文法。" if is_slr1 else "\n".join(slr_conflicts)
                
                # 构造LR(0)
                state_str, trans_str, svg0 = build_lr0_output(self.grammar_text)
                
                # 构造LR(1)
                action_table, goto_table, svg1 = build_lr1_output(self.grammar_text)
                
                # 分析句子
                if sentence.strip():
                    used_method = "SLR(1)" if is_slr1 else "LR(1)"
                    analysis_steps = parse_sentence(self.grammar_text, sentence, method=used_method)
                else:
                    analysis_steps = [[0, '', '', '', '未提供句子']]
                
                syntax_errors = []
                
            except Exception as e:
                # 语法分析出错
                ff_str = f"语法分析错误: {str(e)}"
                slr_result = "语法分析失败"
                is_slr1 = False
                state_str = ""
                trans_str = ""
                svg0 = ""
                action_table = {}
                goto_table = {}
                svg1 = ""
                analysis_steps = []
                syntax_errors = [str(e)]
            
            # 4. 计算统计信息
            analysis_time = time.time() - start_time
            token_count = len([t for t in tokens if t.type != TokenType.EOF])
            success = len(lexical_errors) == 0 and len(syntax_errors) == 0
            
            return AnalysisResult(
                tokens=tokens,
                lexical_errors=lexical_errors,
                first_follow=ff_str,
                slr1_result=slr_result,
                is_slr1=is_slr1,
                lr0_states=state_str,
                lr0_transitions=trans_str,
                lr0_svg=svg0,
                action_table=action_table,
                goto_table=goto_table,
                lr1_svg=svg1,
                parse_steps=analysis_steps,
                syntax_errors=syntax_errors,
                token_count=token_count,
                analysis_time=analysis_time,
                success=success
            )
            
        except Exception as e:
            # 整体分析出错
            analysis_time = time.time() - start_time
            return AnalysisResult(
                tokens=[],
                lexical_errors=[f"分析失败: {str(e)}"],
                first_follow="",
                slr1_result="",
                is_slr1=False,
                lr0_states="",
                lr0_transitions="",
                lr0_svg="",
                action_table={},
                goto_table={},
                lr1_svg="",
                parse_steps=[],
                syntax_errors=[],
                token_count=0,
                analysis_time=analysis_time,
                success=False
            )
    
    def analyze_file(self, file_path: str, sentence: str = "") -> AnalysisResult:
        """分析文件
        
        Args:
            file_path: 源代码文件路径
            sentence: 可选的待分析句子
            
        Returns:
            分析结果
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            return self.analyze_code(source_code, sentence)
        except FileNotFoundError:
            return AnalysisResult(
                tokens=[],
                lexical_errors=[f"文件未找到: {file_path}"],
                first_follow="",
                slr1_result="",
                is_slr1=False,
                lr0_states="",
                lr0_transitions="",
                lr0_svg="",
                action_table={},
                goto_table={},
                lr1_svg="",
                parse_steps=[],
                syntax_errors=[],
                token_count=0,
                analysis_time=0.0,
                success=False
            )
    
    def format_tokens(self, tokens: List[Token]) -> str:
        """格式化Token列表为字符串
        
        Args:
            tokens: Token列表
            
        Returns:
            格式化的字符串
        """
        lines = []
        lines.append("词法分析结果:")
        lines.append("-" * 50)
        lines.append(f"{'序号':<4} {'类型':<20} {'值':<15} {'位置':<10}")
        lines.append("-" * 50)
        
        for i, token in enumerate(tokens, 1):
            if token.type != TokenType.EOF:
                position = f"{token.line}:{token.column}" if hasattr(token, 'line') else "N/A"
                lines.append(f"{i:<4} {token.type.value:<20} {token.value:<15} {position:<10}")
        
        return "\n".join(lines)
    
    def format_action_goto_table(self, action_table: Dict, goto_table: Dict) -> Tuple[str, str]:
        """格式化Action-Goto表
        
        Args:
            action_table: Action表
            goto_table: Goto表
            
        Returns:
            (action_str, goto_str) 格式化的表格字符串
        """
        def format_table(table):
            lines = []
            for state in sorted(table.keys()):
                lines.append(f"状态 {state}:")
                for sym, act in sorted(table[state].items()):
                    lines.append(f"  on '{sym}': {act}")
            return "\n".join(lines)
        
        action_str = format_table(action_table)
        goto_str = format_table(goto_table)
        
        return action_str, goto_str


# 便捷函数
def create_integrated_analyzer(language: str = 'c') -> IntegratedAnalyzer:
    """创建集成分析器
    
    Args:
        language: 目标语言
        
    Returns:
        集成分析器实例
    """
    return IntegratedAnalyzer(language)


def analyze_code_complete(source_code: str, language: str = 'c', grammar: str = "", sentence: str = "") -> AnalysisResult:
    """完整分析源代码的便捷函数
    
    Args:
        source_code: 源代码
        language: 编程语言
        grammar: 自定义文法（可选）
        sentence: 待分析句子（可选）
        
    Returns:
        分析结果
    """
    analyzer = create_integrated_analyzer(language)
    if grammar:
        analyzer.set_grammar(grammar)
    return analyzer.analyze_code(source_code, sentence)


def analyze_file_complete(file_path: str, language: str = 'c', grammar: str = "", sentence: str = "") -> AnalysisResult:
    """完整分析文件的便捷函数
    
    Args:
        file_path: 文件路径
        language: 编程语言
        grammar: 自定义文法（可选）
        sentence: 待分析句子（可选）
        
    Returns:
        分析结果
    """
    analyzer = create_integrated_analyzer(language)
    if grammar:
        analyzer.set_grammar(grammar)
    return analyzer.analyze_file(file_path, sentence)