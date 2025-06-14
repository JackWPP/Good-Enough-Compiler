#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AST构建器

在LR语法分析过程中构建抽象语法树。
"""

from typing import List, Dict, Any, Optional, Tuple
from .ast_nodes import (
    ASTNode, TerminalNode, NonTerminalNode, ProgramNode,
    ExpressionNode, StatementNode, DeclarationNode, create_ast_node
)


class ASTBuilder:
    """
    AST构建器类
    
    在LR语法分析的归约过程中构建抽象语法树。
    """
    
    def __init__(self, grammar_rules: Dict[str, List[str]] = None):
        """
        初始化AST构建器
        
        Args:
            grammar_rules: 语法规则字典，格式为 {left_symbol: [right_symbols]}
        """
        self.grammar_rules = grammar_rules or {}
        self.node_stack: List[ASTNode] = []  # 节点栈，对应分析栈
        self.semantic_actions = {}  # 语义动作字典
        self._setup_default_actions()
    
    def _setup_default_actions(self):
        """
        设置默认的语义动作
        """
        # 表达式相关的语义动作
        self.semantic_actions.update({
            # 二元运算表达式
            'expr -> expr + term': self._build_binary_expr,
            'expr -> expr - term': self._build_binary_expr,
            'term -> term * factor': self._build_binary_expr,
            'term -> term / factor': self._build_binary_expr,
            
            # 一元表达式
            'expr -> term': self._build_unary_expr,
            'term -> factor': self._build_unary_expr,
            'factor -> ( expr )': self._build_parenthesized_expr,
            'factor -> id': self._build_terminal_expr,
            'factor -> num': self._build_terminal_expr,
            
            # 语句相关
            'stmt -> id = expr ;': self._build_assignment_stmt,
            'stmt -> id := expr ;': self._build_assignment_stmt,
            
            # 程序结构
            'program -> stmt_list': self._build_program,
            'stmt_list -> stmt_list stmt': self._build_stmt_list,
            'stmt_list -> stmt': self._build_single_stmt,
        })
    
    def add_semantic_action(self, production: str, action_func):
        """
        添加自定义语义动作
        
        Args:
            production: 产生式字符串，如 "expr -> expr + term"
            action_func: 语义动作函数，接收子节点列表，返回新节点
        """
        self.semantic_actions[production] = action_func
    
    def push_terminal(self, token_type: str, value: str):
        """
        将终结符推入栈
        
        Args:
            token_type: 终结符类型
            value: 终结符值
        """
        node = TerminalNode(token_type, value)
        self.node_stack.append(node)
        return node
    
    def reduce(self, production: str, left_symbol: str, right_symbols: List[str]) -> ASTNode:
        """
        执行归约操作，构建AST节点
        
        Args:
            production: 完整的产生式字符串
            left_symbol: 左部符号
            right_symbols: 右部符号列表
        
        Returns:
            构建的AST节点
        """
        # 从栈中弹出对应数量的节点
        children = []
        for _ in range(len(right_symbols)):
            if self.node_stack:
                children.insert(0, self.node_stack.pop())
        
        # 执行语义动作
        if production in self.semantic_actions:
            new_node = self.semantic_actions[production](children, left_symbol, right_symbols)
        else:
            # 默认动作：创建非终结符节点
            new_node = self._build_default_node(children, left_symbol, production)
        
        # 将新节点推入栈
        self.node_stack.append(new_node)
        return new_node
    
    def get_ast_root(self) -> Optional[ASTNode]:
        """
        获取AST根节点
        
        Returns:
            AST根节点，如果栈为空则返回None
        """
        return self.node_stack[-1] if self.node_stack else None
    
    def clear(self):
        """
        清空构建器状态
        """
        self.node_stack.clear()
    
    # 语义动作函数
    def _build_binary_expr(self, children: List[ASTNode], left_symbol: str, right_symbols: List[str]) -> ASTNode:
        """
        构建二元表达式节点
        """
        if len(children) >= 3:
            left_operand = children[0]
            operator = children[1]
            right_operand = children[2]
            
            # 创建表达式节点
            expr_node = ExpressionNode(
                operator=operator.value if isinstance(operator, TerminalNode) else str(operator),
                children=[left_operand, right_operand]
            )
            expr_node.production_rule = f"{left_symbol} -> {' '.join(right_symbols)}"
            return expr_node
        
        return self._build_default_node(children, left_symbol, f"{left_symbol} -> {' '.join(right_symbols)}")
    
    def _build_unary_expr(self, children: List[ASTNode], left_symbol: str, right_symbols: List[str]) -> ASTNode:
        """
        构建一元表达式节点（通常是传递）
        """
        if len(children) == 1:
            # 直接传递子节点，但更新类型
            child = children[0]
            if isinstance(child, TerminalNode):
                return child
            else:
                # 创建新的表达式节点
                expr_node = ExpressionNode(children=[child])
                expr_node.production_rule = f"{left_symbol} -> {' '.join(right_symbols)}"
                return expr_node
        
        return self._build_default_node(children, left_symbol, f"{left_symbol} -> {' '.join(right_symbols)}")
    
    def _build_parenthesized_expr(self, children: List[ASTNode], left_symbol: str, right_symbols: List[str]) -> ASTNode:
        """
        构建括号表达式节点
        """
        if len(children) == 3:  # ( expr )
            # 返回中间的表达式，忽略括号
            return children[1]
        
        return self._build_default_node(children, left_symbol, f"{left_symbol} -> {' '.join(right_symbols)}")
    
    def _build_terminal_expr(self, children: List[ASTNode], left_symbol: str, right_symbols: List[str]) -> ASTNode:
        """
        构建终结符表达式节点
        """
        if len(children) == 1 and isinstance(children[0], TerminalNode):
            return children[0]
        
        return self._build_default_node(children, left_symbol, f"{left_symbol} -> {' '.join(right_symbols)}")
    
    def _build_assignment_stmt(self, children: List[ASTNode], left_symbol: str, right_symbols: List[str]) -> ASTNode:
        """
        构建赋值语句节点
        """
        if len(children) >= 4:  # id = expr ;
            var_node = children[0]
            assign_op = children[1]
            expr_node = children[2]
            
            stmt_node = StatementNode(
                stmt_type="assignment",
                children=[var_node, expr_node]
            )
            stmt_node.production_rule = f"{left_symbol} -> {' '.join(right_symbols)}"
            return stmt_node
        
        return self._build_default_node(children, left_symbol, f"{left_symbol} -> {' '.join(right_symbols)}")
    
    def _build_program(self, children: List[ASTNode], left_symbol: str, right_symbols: List[str]) -> ASTNode:
        """
        构建程序节点
        """
        program_node = ProgramNode(children)
        program_node.production_rule = f"{left_symbol} -> {' '.join(right_symbols)}"
        return program_node
    
    def _build_stmt_list(self, children: List[ASTNode], left_symbol: str, right_symbols: List[str]) -> ASTNode:
        """
        构建语句列表节点
        """
        if len(children) == 2:  # stmt_list stmt
            stmt_list = children[0]
            new_stmt = children[1]
            
            # 将新语句添加到语句列表中
            if isinstance(stmt_list, NonTerminalNode):
                stmt_list.add_child(new_stmt)
                return stmt_list
        
        return self._build_default_node(children, left_symbol, f"{left_symbol} -> {' '.join(right_symbols)}")
    
    def _build_single_stmt(self, children: List[ASTNode], left_symbol: str, right_symbols: List[str]) -> ASTNode:
        """
        构建单个语句节点
        """
        if len(children) == 1:
            # 创建语句列表节点包含单个语句
            stmt_list_node = NonTerminalNode("stmt_list", f"{left_symbol} -> {' '.join(right_symbols)}", children)
            return stmt_list_node
        
        return self._build_default_node(children, left_symbol, f"{left_symbol} -> {' '.join(right_symbols)}")
    
    def _build_default_node(self, children: List[ASTNode], left_symbol: str, production: str) -> ASTNode:
        """
        构建默认节点
        """
        node = create_ast_node(left_symbol, children, production_rule=production)
        return node


class ParseTreeToAST:
    """
    将分析树转换为AST的工具类
    """
    
    @staticmethod
    def convert(parse_steps: List[Dict[str, Any]]) -> Optional[ASTNode]:
        """
        从分析步骤中构建AST
        
        Args:
            parse_steps: 语法分析步骤列表
        
        Returns:
            AST根节点
        """
        builder = ASTBuilder()
        
        for step in parse_steps:
            action = step.get('action', '')
            
            if action.startswith('shift'):
                # 移入操作：推入终结符
                symbol = step.get('symbol', '')
                builder.push_terminal(symbol, symbol)
            
            elif action.startswith('reduce'):
                # 归约操作：构建AST节点
                production = step.get('production', '')
                if ' -> ' in production:
                    left, right = production.split(' -> ', 1)
                    right_symbols = right.split() if right.strip() != 'ε' else []
                    builder.reduce(production, left.strip(), right_symbols)
        
        return builder.get_ast_root()
    
    @staticmethod
    def enhance_parse_steps_with_ast(parse_steps: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Optional[ASTNode]]:
        """
        增强分析步骤，添加AST构建信息
        
        Args:
            parse_steps: 原始分析步骤
        
        Returns:
            (增强的分析步骤, AST根节点)
        """
        builder = ASTBuilder()
        enhanced_steps = []
        
        for step in parse_steps:
            enhanced_step = step.copy()
            action = step.get('action', '')
            
            if action.startswith('shift'):
                symbol = step.get('symbol', '')
                node = builder.push_terminal(symbol, symbol)
                enhanced_step['ast_node'] = node.to_dict()
            
            elif action.startswith('reduce'):
                production = step.get('production', '')
                if ' -> ' in production:
                    left, right = production.split(' -> ', 1)
                    right_symbols = right.split() if right.strip() != 'ε' else []
                    node = builder.reduce(production, left.strip(), right_symbols)
                    enhanced_step['ast_node'] = node.to_dict()
                    enhanced_step['ast_stack_size'] = len(builder.node_stack)
            
            enhanced_steps.append(enhanced_step)
        
        return enhanced_steps, builder.get_ast_root()