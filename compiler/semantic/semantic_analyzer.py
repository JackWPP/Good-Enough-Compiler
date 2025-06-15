from .semantic_actions import execute_action
from .symbol_table import SymbolTable
from .semantic_error import SemanticErrorHandler


class SemanticAnalyzer:
    def __init__(self):
        self.attr_stack = []
        self.symbol_table = SymbolTable()
        self.errors = SemanticErrorHandler()

    def reduce(self, prod_num, rhs_attrs, lineno=None):
        try:
            if not isinstance(rhs_attrs, list):
                raise ValueError("rhs_attrs 必须为列表")
            result = execute_action(prod_num, rhs_attrs, self.symbol_table)
            self.attr_stack.append(result)
        except Exception as e:
            self.errors.report(str(e), lineno)

    def shift(self, token_attr):
        if token_attr is None:
            self.errors.report("shift 时 token_attr 不能为空")
            return
        self.attr_stack.append(token_attr)

    def pop_attrs(self, count):
        if count > len(self.attr_stack):
            self.errors.report("pop_attrs 数量超出栈长度")
            return []
        attrs = self.attr_stack[-count:]
        self.attr_stack = self.attr_stack[:-count]
        return attrs

    def get_result(self):
        return self.attr_stack[-1] if self.attr_stack else None
    
    def get_errors(self):
        """获取语义分析错误信息"""
        return self.errors.get_errors()
    
    def get_symbol_table_string(self):
        """获取符号表的字符串表示"""
        return str(self.symbol_table)
    
    def analyze(self, parse_result):
        """分析语法分析结果并进行语义检查"""
        try:
            # 重置分析状态
            self.attr_stack = []
            self.symbol_table = SymbolTable()
            self.errors = SemanticErrorHandler()
            
            # 如果解析成功，进行语义分析
            if parse_result and hasattr(parse_result, 'success') and parse_result.success:
                # 这里可以根据AST进行语义分析
                # 目前先返回基本的分析结果
                return {
                    'success': True,
                    'errors': self.errors.get_errors(),
                    'symbol_table': str(self.symbol_table),
                    'warnings': []
                }
            else:
                # 语法分析失败，无法进行语义分析
                self.errors.report("语法分析失败，无法进行语义分析")
                return {
                    'success': False,
                    'errors': self.errors.get_errors(),
                    'symbol_table': str(self.symbol_table),
                    'warnings': []
                }
                
        except Exception as e:
            self.errors.report(f"语义分析过程中发生错误: {str(e)}")
            return {
                'success': False,
                'errors': self.errors.get_errors(),
                'symbol_table': str(self.symbol_table),
                'warnings': []
            }
