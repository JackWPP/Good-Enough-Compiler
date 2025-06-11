#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译器API模块

提供统一的编译器接口和高级API，包括：
- 完整编译流程
- 分阶段编译
- 配置管理
- 结果处理
- 错误报告

这是编译器的主要对外接口，封装了各个编译阶段的复杂性，
为用户提供简单易用的编译功能。
"""

import os
import time
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path

# 导入各个模块
from .lexical import LexicalAnalyzer, Token, create_c_analyzer, create_pascal_analyzer
from .utils import read_file_safe, write_file_safe, detect_language, get_language_info
from .utils import format_token_table, format_statistics, format_errors, create_html_report


class CompilerConfig:
    """
    编译器配置类
    
    管理编译器的各种配置选项
    """
    
    def __init__(self):
        # 基本配置
        self.language = 'c'  # 目标语言
        self.target = 'x86-64'  # 目标平台
        self.optimization_level = 2  # 优化级别 (0-3)
        
        # 编译阶段控制
        self.enable_lexical = True
        self.enable_syntax = False  # 暂未实现
        self.enable_semantic = False  # 暂未实现
        self.enable_codegen = False  # 暂未实现
        
        # 输出控制
        self.verbose = False
        self.debug = False
        self.output_tokens = True
        self.output_ast = False
        self.output_ir = False
        self.output_assembly = False
        
        # 文件配置
        self.input_encoding = 'utf-8'
        self.output_encoding = 'utf-8'
        self.backup_files = False
        
        # 错误处理
        self.stop_on_error = True
        self.max_errors = 10
        
        # 词法分析配置
        self.lexical_rules_file = None
        self.custom_tokens = []
        
    def from_dict(self, config_dict: Dict[str, Any]):
        """
        从字典加载配置
        
        Args:
            config_dict: 配置字典
        """
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典
        
        Returns:
            配置字典
        """
        return {key: value for key, value in self.__dict__.items() 
                if not key.startswith('_')}
    
    def validate(self) -> List[str]:
        """
        验证配置
        
        Returns:
            错误信息列表
        """
        errors = []
        
        # 验证语言
        if self.language not in ['c', 'pascal']:
            errors.append(f"不支持的语言: {self.language}")
        
        # 验证优化级别
        if not 0 <= self.optimization_level <= 3:
            errors.append(f"无效的优化级别: {self.optimization_level}")
        
        # 验证最大错误数
        if self.max_errors <= 0:
            errors.append(f"最大错误数必须大于0: {self.max_errors}")
        
        return errors


class CompilationResult:
    """
    编译结果类
    
    封装编译过程的所有结果和信息
    """
    
    def __init__(self):
        # 基本信息
        self.success = False
        self.source_file = ""
        self.language = ""
        self.processing_time = 0.0
        
        # 各阶段结果
        self.tokens = []
        self.ast = None
        self.symbol_table = None
        self.intermediate_code = None
        self.target_code = ""
        
        # 统计信息
        self.statistics = {}
        
        # 错误和警告
        self.errors = []
        self.warnings = []
        
        # 输出文件
        self.output_files = []
    
    def add_error(self, message: str, line: int = 0, column: int = 0, 
                  stage: str = "unknown"):
        """
        添加错误
        
        Args:
            message: 错误信息
            line: 行号
            column: 列号
            stage: 编译阶段
        """
        self.errors.append({
            'message': message,
            'line': line,
            'column': column,
            'stage': stage,
            'type': 'error'
        })
    
    def add_warning(self, message: str, line: int = 0, column: int = 0, 
                   stage: str = "unknown"):
        """
        添加警告
        
        Args:
            message: 警告信息
            line: 行号
            column: 列号
            stage: 编译阶段
        """
        self.warnings.append({
            'message': message,
            'line': line,
            'column': column,
            'stage': stage,
            'type': 'warning'
        })
    
    def has_errors(self) -> bool:
        """
        是否有错误
        
        Returns:
            是否有错误
        """
        return len(self.errors) > 0
    
    def get_summary(self) -> str:
        """
        获取结果摘要
        
        Returns:
            摘要字符串
        """
        status = "成功" if self.success else "失败"
        return f"编译{status} - {len(self.errors)}个错误, {len(self.warnings)}个警告"


class Compiler:
    """
    编译器主类
    
    提供完整的编译功能和统一的接口
    """
    
    def __init__(self, config: Optional[CompilerConfig] = None):
        """
        初始化编译器
        
        Args:
            config: 编译器配置
        """
        self.config = config or CompilerConfig()
        self.lexical_analyzer = None
        
        # 验证配置
        config_errors = self.config.validate()
        if config_errors:
            raise ValueError(f"配置错误: {'; '.join(config_errors)}")
    
    def compile_file(self, source_file: str, output_file: Optional[str] = None) -> CompilationResult:
        """
        编译文件
        
        Args:
            source_file: 源文件路径
            output_file: 输出文件路径（可选）
        
        Returns:
            编译结果
        """
        result = CompilationResult()
        result.source_file = source_file
        
        start_time = time.time()
        
        try:
            # 读取源文件
            source_code, error = read_file_safe(source_file, self.config.input_encoding)
            if error:
                result.add_error(f"读取文件失败: {error}", stage="file_io")
                return result
            
            # 检测语言
            if not self.config.language:
                detected_language = detect_language(source_file, source_code)
                self.config.language = detected_language
            
            result.language = self.config.language
            
            # 编译源代码
            return self.compile_source(source_code, source_file, output_file)
            
        except Exception as e:
            result.add_error(f"编译过程中发生异常: {str(e)}", stage="compiler")
            return result
        
        finally:
            result.processing_time = time.time() - start_time
    
    def compile_source(self, source_code: str, source_file: str = "<string>", 
                      output_file: Optional[str] = None) -> CompilationResult:
        """
        编译源代码
        
        Args:
            source_code: 源代码
            source_file: 源文件名（用于错误报告）
            output_file: 输出文件路径（可选）
        
        Returns:
            编译结果
        """
        result = CompilationResult()
        result.source_file = source_file
        result.language = self.config.language
        
        start_time = time.time()
        
        try:
            # 词法分析
            if self.config.enable_lexical:
                success = self._perform_lexical_analysis(source_code, result)
                if not success and self.config.stop_on_error:
                    return result
            
            # 语法分析（暂未实现）
            if self.config.enable_syntax:
                success = self._perform_syntax_analysis(result)
                if not success and self.config.stop_on_error:
                    return result
            
            # 语义分析（暂未实现）
            if self.config.enable_semantic:
                success = self._perform_semantic_analysis(result)
                if not success and self.config.stop_on_error:
                    return result
            
            # 代码生成（暂未实现）
            if self.config.enable_codegen:
                success = self._perform_code_generation(result)
                if not success and self.config.stop_on_error:
                    return result
            
            # 生成输出文件
            if output_file:
                self._generate_output_files(result, output_file)
            
            result.success = not result.has_errors()
            
        except Exception as e:
            result.add_error(f"编译过程中发生异常: {str(e)}", stage="compiler")
        
        finally:
            result.processing_time = time.time() - start_time
        
        return result
    
    def _perform_lexical_analysis(self, source_code: str, result: CompilationResult) -> bool:
        """
        执行词法分析
        
        Args:
            source_code: 源代码
            result: 编译结果
        
        Returns:
            是否成功
        """
        try:
            # 创建词法分析器
            if self.config.language == 'c':
                self.lexical_analyzer = create_c_analyzer()
            elif self.config.language == 'pascal':
                self.lexical_analyzer = create_pascal_analyzer()
            else:
                result.add_error(f"不支持的语言: {self.config.language}", stage="lexical")
                return False
            
            # 加载自定义规则
            if self.config.lexical_rules_file:
                error = self.lexical_analyzer.load_rules_from_file(self.config.lexical_rules_file)
                if error:
                    result.add_error(f"加载词法规则失败: {error}", stage="lexical")
                    return False
            
            # 执行词法分析
            tokens = self.lexical_analyzer.analyze(source_code)
            errors = self.lexical_analyzer.get_errors()
            
            result.tokens = tokens
            
            # 处理错误
            for error in errors:
                if isinstance(error, str):
                    result.add_error(error, stage='lexical')
                else:
                    result.add_error(
                        error.get('message', '未知错误'),
                        error.get('line', 0),
                        error.get('column', 0),
                        'lexical'
                    )
            
            # 生成统计信息
            token_stats = self.lexical_analyzer.get_token_statistics()
            result.statistics = {
                'total_tokens': len(tokens),
                'total_lines': max(token.line for token in tokens) if tokens else 0,
                'total_characters': len(source_code),
                'token_counts': token_stats
            }
            
            return len(errors) == 0
            
        except Exception as e:
            result.add_error(f"词法分析失败: {str(e)}", stage="lexical")
            return False
    
    def _perform_syntax_analysis(self, result: CompilationResult) -> bool:
        """
        执行语法分析（占位符）
        
        Args:
            result: 编译结果
        
        Returns:
            是否成功
        """
        result.add_error("语法分析功能尚未实现", stage="syntax")
        return False
    
    def _perform_semantic_analysis(self, result: CompilationResult) -> bool:
        """
        执行语义分析（占位符）
        
        Args:
            result: 编译结果
        
        Returns:
            是否成功
        """
        result.add_error("语义分析功能尚未实现", stage="semantic")
        return False
    
    def _perform_code_generation(self, result: CompilationResult) -> bool:
        """
        执行代码生成（占位符）
        
        Args:
            result: 编译结果
        
        Returns:
            是否成功
        """
        result.add_error("代码生成功能尚未实现", stage="codegen")
        return False
    
    def _generate_output_files(self, result: CompilationResult, output_file: str):
        """
        生成输出文件
        
        Args:
            result: 编译结果
            output_file: 输出文件路径
        """
        try:
            output_path = Path(output_file)
            
            # 生成Token文件
            if self.config.output_tokens and result.tokens:
                token_file = output_path.with_suffix('.tokens')
                token_content = format_token_table(result.tokens)
                error = write_file_safe(str(token_file), token_content, self.config.output_encoding)
                if not error:
                    result.output_files.append(str(token_file))
            
            # 生成统计文件
            if result.statistics:
                stats_file = output_path.with_suffix('.stats')
                stats_content = format_statistics(result.statistics)
                error = write_file_safe(str(stats_file), stats_content, self.config.output_encoding)
                if not error:
                    result.output_files.append(str(stats_file))
            
            # 生成HTML报告
            html_file = output_path.with_suffix('.html')
            source_code = ""
            if result.source_file and os.path.exists(result.source_file):
                source_code, _ = read_file_safe(result.source_file)
            
            html_content = create_html_report(
                result.tokens, 
                result.statistics, 
                result.errors + result.warnings,
                source_code or ""
            )
            error = write_file_safe(str(html_file), html_content, self.config.output_encoding)
            if not error:
                result.output_files.append(str(html_file))
            
        except Exception as e:
            result.add_error(f"生成输出文件失败: {str(e)}", stage="output")


# 便利函数
def compile_file(source_file: str, output_file: Optional[str] = None, 
                language: Optional[str] = None, **kwargs) -> CompilationResult:
    """
    编译文件的便利函数
    
    Args:
        source_file: 源文件路径
        output_file: 输出文件路径
        language: 目标语言
        **kwargs: 其他配置选项
    
    Returns:
        编译结果
    """
    config = CompilerConfig()
    if language:
        config.language = language
    config.from_dict(kwargs)
    
    compiler = Compiler(config)
    return compiler.compile_file(source_file, output_file)


def compile_source(source_code: str, language: str = 'c', **kwargs) -> CompilationResult:
    """
    编译源代码的便利函数
    
    Args:
        source_code: 源代码
        language: 目标语言
        **kwargs: 其他配置选项
    
    Returns:
        编译结果
    """
    config = CompilerConfig()
    config.language = language
    config.from_dict(kwargs)
    
    compiler = Compiler(config)
    return compiler.compile_source(source_code)


def analyze_tokens(source_code: str, language: str = 'c', **kwargs) -> Tuple[List[Token], List[Dict]]:
    """
    仅进行词法分析的便利函数
    
    Args:
        source_code: 源代码
        language: 目标语言
        **kwargs: 其他配置选项
    
    Returns:
        (Token列表, 错误列表)
    """
    config = CompilerConfig()
    config.language = language
    config.enable_syntax = False
    config.enable_semantic = False
    config.enable_codegen = False
    config.from_dict(kwargs)
    
    compiler = Compiler(config)
    result = compiler.compile_source(source_code)
    
    return result.tokens, result.errors


def get_supported_languages() -> List[str]:
    """
    获取支持的编程语言列表
    
    Returns:
        支持的语言列表
    """
    return ['c', 'pascal']


def get_compiler_info() -> Dict[str, Any]:
    """
    获取编译器信息
    
    Returns:
        编译器信息字典
    """
    return {
        'name': 'Good-Enough-Compiler',
        'version': '1.0.0',
        'description': '一个教学用的编译器实现',
        'supported_languages': get_supported_languages(),
        'features': {
            'lexical_analysis': True,
            'syntax_analysis': False,
            'semantic_analysis': False,
            'code_generation': False,
            'optimization': False
        },
        'stages': {
            'implemented': ['lexical'],
            'planned': ['syntax', 'semantic', 'codegen']
        }
    }