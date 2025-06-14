#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抽象语法树(AST)节点定义

定义了语法分析过程中构建的AST节点类型。
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional
import json


class ASTNode(ABC):
    """
    AST节点基类
    """
    
    def __init__(self, node_type: str, value: Any = None, children: List['ASTNode'] = None):
        self.node_type = node_type
        self.value = value
        self.children = children or []
        self.parent = None
        
        # 设置子节点的父节点引用
        for child in self.children:
            if child:
                child.parent = self
    
    def add_child(self, child: 'ASTNode'):
        """添加子节点"""
        if child:
            self.children.append(child)
            child.parent = self
    
    def remove_child(self, child: 'ASTNode'):
        """移除子节点"""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
    
    def get_depth(self) -> int:
        """获取节点深度"""
        if not self.children:
            return 1
        return 1 + max(child.get_depth() for child in self.children)
    
    def to_dict(self) -> dict:
        """转换为字典格式，便于序列化"""
        return {
            'type': self.node_type,
            'value': self.value,
            'children': [child.to_dict() for child in self.children if child]
        }
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def __str__(self) -> str:
        if self.value is not None:
            return f"{self.node_type}({self.value})"
        return self.node_type
    
    def __repr__(self) -> str:
        return self.__str__()


class TerminalNode(ASTNode):
    """
    终结符节点（叶子节点）
    """
    
    def __init__(self, token_type: str, value: str):
        super().__init__("Terminal", value)
        self.token_type = token_type
    
    def to_dict(self) -> dict:
        return {
            'type': 'Terminal',
            'token_type': self.token_type,
            'value': self.value,
            'children': []
        }
    
    def __str__(self) -> str:
        return f"{self.token_type}:{self.value}"


class NonTerminalNode(ASTNode):
    """
    非终结符节点（内部节点）
    """
    
    def __init__(self, symbol: str, production_rule: str = None, children: List[ASTNode] = None):
        super().__init__("NonTerminal", symbol, children)
        self.symbol = symbol
        self.production_rule = production_rule
    
    def to_dict(self) -> dict:
        return {
            'type': 'NonTerminal',
            'symbol': self.symbol,
            'production_rule': self.production_rule,
            'children': [child.to_dict() for child in self.children if child]
        }
    
    def __str__(self) -> str:
        return f"{self.symbol}"


class ProgramNode(NonTerminalNode):
    """
    程序根节点
    """
    
    def __init__(self, children: List[ASTNode] = None):
        super().__init__("Program", "program → ...", children)


class ExpressionNode(NonTerminalNode):
    """
    表达式节点
    """
    
    def __init__(self, operator: str = None, children: List[ASTNode] = None):
        super().__init__("Expression", operator, children)
        self.operator = operator
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result['operator'] = self.operator
        return result


class StatementNode(NonTerminalNode):
    """
    语句节点
    """
    
    def __init__(self, stmt_type: str, children: List[ASTNode] = None):
        super().__init__("Statement", stmt_type, children)
        self.stmt_type = stmt_type
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result['stmt_type'] = self.stmt_type
        return result


class DeclarationNode(NonTerminalNode):
    """
    声明节点
    """
    
    def __init__(self, decl_type: str, children: List[ASTNode] = None):
        super().__init__("Declaration", decl_type, children)
        self.decl_type = decl_type
    
    def to_dict(self) -> dict:
        result = super().to_dict()
        result['decl_type'] = self.decl_type
        return result


class ASTVisualizer:
    """
    AST可视化工具
    """
    
    @staticmethod
    def to_tree_string(node: ASTNode, prefix: str = "", is_last: bool = True) -> str:
        """
        将AST转换为树形字符串表示
        """
        if not node:
            return ""
        
        # 当前节点的连接符
        connector = "└── " if is_last else "├── "
        result = prefix + connector + str(node) + "\n"
        
        # 子节点的前缀
        child_prefix = prefix + ("    " if is_last else "│   ")
        
        # 递归处理子节点
        for i, child in enumerate(node.children):
            if child:
                is_last_child = (i == len(node.children) - 1)
                result += ASTVisualizer.to_tree_string(child, child_prefix, is_last_child)
        
        return result
    
    @staticmethod
    def to_dot(node: ASTNode, graph_name: str = "AST") -> str:
        """
        将AST转换为Graphviz DOT格式
        """
        dot_lines = [f"digraph {graph_name} {{"]
        dot_lines.append("    rankdir=TB;")
        dot_lines.append("    node [shape=box, style=rounded];")
        
        node_id = 0
        node_map = {}
        
        def add_node(n: ASTNode) -> int:
            nonlocal node_id
            current_id = node_id
            node_id += 1
            node_map[id(n)] = current_id
            
            # 节点标签
            if isinstance(n, TerminalNode):
                label = f"{n.token_type}\\n{n.value}"
                dot_lines.append(f'    {current_id} [label="{label}", fillcolor=lightblue, style="rounded,filled"];')
            else:
                label = str(n)
                if hasattr(n, 'production_rule') and n.production_rule:
                    label += f"\\n{n.production_rule}"
                dot_lines.append(f'    {current_id} [label="{label}", fillcolor=lightgreen, style="rounded,filled"];')
            
            # 递归处理子节点
            for child in n.children:
                if child:
                    child_id = add_node(child)
                    dot_lines.append(f"    {current_id} -> {child_id};")
            
            return current_id
        
        if node:
            add_node(node)
        
        dot_lines.append("}")
        return "\n".join(dot_lines)
    
    @staticmethod
    def to_svg(node: ASTNode, graph_name: str = "AST") -> str:
        """
        将AST转换为SVG格式（需要graphviz库）
        """
        try:
            import graphviz
            dot_source = ASTVisualizer.to_dot(node, graph_name)
            graph = graphviz.Source(dot_source)
            return graph.pipe(format='svg', encoding='utf-8')
        except ImportError:
            return "<p>需要安装graphviz库才能生成SVG: pip install graphviz</p>"
        except Exception as e:
            return f"<p>生成SVG时出错: {str(e)}</p>"


def create_ast_node(symbol: str, children: List[ASTNode] = None, **kwargs) -> ASTNode:
    """
    工厂函数：根据符号类型创建相应的AST节点
    """
    symbol_lower = symbol.lower()
    
    # 根据符号名称判断节点类型
    if symbol in ['id', 'num', 'string', '+', '-', '*', '/', '(', ')', ';', '=', ':=']:
        return TerminalNode(symbol, kwargs.get('value', symbol))
    elif 'expr' in symbol_lower or 'term' in symbol_lower or 'factor' in symbol_lower:
        return ExpressionNode(kwargs.get('operator'), children)
    elif 'stmt' in symbol_lower:
        return StatementNode(kwargs.get('stmt_type', symbol), children)
    elif 'decl' in symbol_lower or 'var' in symbol_lower:
        return DeclarationNode(kwargs.get('decl_type', symbol), children)
    elif symbol_lower == 'program':
        return ProgramNode(children)
    else:
        return NonTerminalNode(symbol, kwargs.get('production_rule'), children)