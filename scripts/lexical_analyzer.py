#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词法分析器 - Good Enough Compiler
实现词法分析的核心功能，包括：
1. Token定义和识别
2. 正则表达式到NFA/DFA的转换
3. 词法分析过程
4. 错误处理
"""

import re
import enum
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
import graphviz
import io
from PIL import Image

# Token类型定义
class TokenType(enum.Enum):
    # 关键字
    PROGRAM = "PROGRAM"
    VAR = "VAR"
    CONST = "CONST"
    PROCEDURE = "PROCEDURE"
    FUNCTION = "FUNCTION"
    BEGIN = "BEGIN"
    END = "END"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    WHILE = "WHILE"
    DO = "DO"
    FOR = "FOR"
    TO = "TO"
    REPEAT = "REPEAT"
    UNTIL = "UNTIL"
    CASE = "CASE"
    OF = "OF"
    
    # 数据类型
    INTEGER = "INTEGER"
    REAL = "REAL"
    BOOLEAN = "BOOLEAN"
    CHAR = "CHAR"
    STRING = "STRING"
    
    # 标识符和字面量
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING_LITERAL = "STRING_LITERAL"
    CHAR_LITERAL = "CHAR_LITERAL"
    
    # 运算符
    PLUS = "PLUS"          # +
    MINUS = "MINUS"        # -
    MULTIPLY = "MULTIPLY"  # *
    DIVIDE = "DIVIDE"      # /
    MOD = "MOD"            # mod
    DIV = "DIV"            # div
    ASSIGN = "ASSIGN"      # :=
    EQUAL = "EQUAL"        # =
    NOT_EQUAL = "NOT_EQUAL"  # <>
    LESS = "LESS"          # <
    LESS_EQUAL = "LESS_EQUAL"  # <=
    GREATER = "GREATER"    # >
    GREATER_EQUAL = "GREATER_EQUAL"  # >=
    AND = "AND"            # and
    OR = "OR"              # or
    NOT = "NOT"            # not
    
    # 分隔符
    SEMICOLON = "SEMICOLON"  # ;
    COMMA = "COMMA"          # ,
    DOT = "DOT"              # .
    COLON = "COLON"          # :
    LPAREN = "LPAREN"        # (
    RPAREN = "RPAREN"        # )
    LBRACKET = "LBRACKET"    # [
    RBRACKET = "RBRACKET"    # ]
    
    # 特殊Token
    EOF = "EOF"
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
    ERROR = "ERROR"

@dataclass
class Token:
    """Token数据结构"""
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        return f"Token({self.type.value}, '{self.value}', {self.line}:{self.column})"

class State:
    """表示自动机中的一个状态"""
    def __init__(self, id):
        self.id = id
        self.transitions = {}  # 存储状态转移: symbol -> [target_states]
        self.is_end = False    # 是否为接受状态
        self.epsilon_moves = []  # 存储ε转移可达的状态
        self.token_type = None  # 如果是接受状态，对应的Token类型

class NFA:
    """非确定有限自动机"""
    def __init__(self):
        self.states = []       # 所有状态列表
        self.start_state = None  # 开始状态
        self.end_states = []   # 接受状态列表
        self.alphabet = set()  # 字母表(输入符号集)

    def create_state(self):
        """创建并添加新状态"""
        state = State(len(self.states))
        self.states.append(state)
        return state

    def set_start(self, state):
        """设置开始状态"""
        self.start_state = state

    def add_end(self, state, token_type=None):
        """添加接受状态"""
        state.is_end = True
        state.token_type = token_type
        self.end_states.append(state)

    def add_transition(self, from_state, symbol, to_state):
        """添加状态转移"""
        if symbol != 'ε':
            self.alphabet.add(symbol)
            
        if symbol in from_state.transitions:
            from_state.transitions[symbol].append(to_state)
        else:
            from_state.transitions[symbol] = [to_state]
            
        if symbol == 'ε':
            from_state.epsilon_moves.append(to_state)

class DFA:
    """确定有限自动机"""
    def __init__(self):
        self.states = {}       # 状态集合 {state_id: state_info}
        self.start_state = None
        self.transitions = {}  # 转移函数 {(state, symbol): next_state}
        self.accept_states = {}  # 接受状态 {state_id: token_type}
        self.alphabet = set()

class LexicalRule:
    """词法规则定义"""
    def __init__(self, pattern: str, token_type: TokenType, priority: int = 0):
        self.pattern = pattern
        self.token_type = token_type
        self.priority = priority  # 优先级，数字越大优先级越高
        self.regex = re.compile(pattern)

class LexicalAnalyzer:
    """词法分析器主类"""
    
    def __init__(self):
        self.rules = []
        self.keywords = {}
        self.tokens = []
        self.errors = []
        self.current_line = 1
        self.current_column = 1
        self.nfa = None
        self.dfa = None
        
        # 初始化默认规则
        self._init_default_rules()
    
    def _init_default_rules(self):
        """初始化默认的词法规则"""
        # 关键字
        keywords = {
            'program': TokenType.PROGRAM,
            'var': TokenType.VAR,
            'const': TokenType.CONST,
            'procedure': TokenType.PROCEDURE,
            'function': TokenType.FUNCTION,
            'begin': TokenType.BEGIN,
            'end': TokenType.END,
            'if': TokenType.IF,
            'then': TokenType.THEN,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'do': TokenType.DO,
            'for': TokenType.FOR,
            'to': TokenType.TO,
            'repeat': TokenType.REPEAT,
            'until': TokenType.UNTIL,
            'case': TokenType.CASE,
            'of': TokenType.OF,
            'integer': TokenType.INTEGER,
            'real': TokenType.REAL,
            'boolean': TokenType.BOOLEAN,
            'char': TokenType.CHAR,
            'string': TokenType.STRING,
            'mod': TokenType.MOD,
            'div': TokenType.DIV,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
        }
        self.keywords = keywords
        
        # 词法规则（按优先级排序）
        rules = [
            # 注释
            (r'\{[^}]*\}', TokenType.COMMENT, 10),
            (r'//.*', TokenType.COMMENT, 10),
            
            # 字符串和字符字面量
            (r"'([^'\\]|\\.)*'", TokenType.STRING_LITERAL, 9),
            (r"'([^'\\]|\\.)'", TokenType.CHAR_LITERAL, 9),
            
            # 数字
            (r'\d+\.\d+', TokenType.NUMBER, 8),  # 实数
            (r'\d+', TokenType.NUMBER, 8),       # 整数
            
            # 双字符运算符
            (r':=', TokenType.ASSIGN, 7),
            (r'<=', TokenType.LESS_EQUAL, 7),
            (r'>=', TokenType.GREATER_EQUAL, 7),
            (r'<>', TokenType.NOT_EQUAL, 7),
            
            # 单字符运算符和分隔符
            (r'\+', TokenType.PLUS, 6),
            (r'-', TokenType.MINUS, 6),
            (r'\*', TokenType.MULTIPLY, 6),
            (r'/', TokenType.DIVIDE, 6),
            (r'=', TokenType.EQUAL, 6),
            (r'<', TokenType.LESS, 6),
            (r'>', TokenType.GREATER, 6),
            (r';', TokenType.SEMICOLON, 6),
            (r',', TokenType.COMMA, 6),
            (r'\.', TokenType.DOT, 6),
            (r':', TokenType.COLON, 6),
            (r'\(', TokenType.LPAREN, 6),
            (r'\)', TokenType.RPAREN, 6),
            (r'\[', TokenType.LBRACKET, 6),
            (r'\]', TokenType.RBRACKET, 6),
            
            # 标识符（必须在关键字检查之后）
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER, 5),
            
            # 空白字符
            (r'\n', TokenType.NEWLINE, 1),
            (r'[ \t]+', TokenType.WHITESPACE, 1),
        ]
        
        for pattern, token_type, priority in rules:
            self.add_rule(pattern, token_type, priority)
    
    def add_rule(self, pattern: str, token_type: TokenType, priority: int = 0):
        """添加词法规则"""
        rule = LexicalRule(pattern, token_type, priority)
        self.rules.append(rule)
        # 按优先级排序
        self.rules.sort(key=lambda x: x.priority, reverse=True)
    
    def load_rules_from_file(self, filename: str):
        """从文件加载词法规则"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('\t')
                        if len(parts) >= 2:
                            pattern = parts[0]
                            token_type_name = parts[1]
                            priority = int(parts[2]) if len(parts) > 2 else 0
                            
                            # 查找对应的TokenType
                            token_type = None
                            for tt in TokenType:
                                if tt.value == token_type_name:
                                    token_type = tt
                                    break
                            
                            if token_type:
                                self.add_rule(pattern, token_type, priority)
            return True
        except Exception as e:
            self.errors.append(f"加载规则文件失败: {e}")
            return False
    
    def analyze(self, text: str) -> List[Token]:
        """执行词法分析"""
        self.tokens = []
        self.errors = []
        self.current_line = 1
        self.current_column = 1
        
        position = 0
        while position < len(text):
            matched = False
            
            # 尝试匹配每个规则
            for rule in self.rules:
                match = rule.regex.match(text, position)
                if match:
                    value = match.group(0)
                    token_type = rule.token_type
                    
                    # 检查是否为关键字
                    if token_type == TokenType.IDENTIFIER and value.lower() in self.keywords:
                        token_type = self.keywords[value.lower()]
                    
                    # 创建Token（跳过空白字符和注释）
                    if token_type not in [TokenType.WHITESPACE, TokenType.COMMENT]:
                        token = Token(token_type, value, self.current_line, self.current_column)
                        self.tokens.append(token)
                    
                    # 更新位置信息
                    if token_type == TokenType.NEWLINE:
                        self.current_line += 1
                        self.current_column = 1
                    else:
                        self.current_column += len(value)
                    
                    position = match.end()
                    matched = True
                    break
            
            if not matched:
                # 未匹配的字符，报告错误
                char = text[position]
                error_msg = f"未识别的字符 '{char}' 在第 {self.current_line} 行第 {self.current_column} 列"
                self.errors.append(error_msg)
                
                # 创建错误Token
                error_token = Token(TokenType.ERROR, char, self.current_line, self.current_column)
                self.tokens.append(error_token)
                
                position += 1
                self.current_column += 1
        
        # 添加EOF Token
        eof_token = Token(TokenType.EOF, '', self.current_line, self.current_column)
        self.tokens.append(eof_token)
        
        return self.tokens
    
    def get_tokens_table(self) -> List[List[str]]:
        """获取Token表格"""
        table = []
        table.append(["序号", "Token类型", "值", "行号", "列号"])
        
        for i, token in enumerate(self.tokens, 1):
            table.append([
                str(i),
                token.type.value,
                token.value,
                str(token.line),
                str(token.column)
            ])
        
        return table
    
    def get_errors(self) -> List[str]:
        """获取错误列表"""
        return self.errors
    
    def has_errors(self) -> bool:
        """检查是否有错误"""
        return len(self.errors) > 0 or any(token.type == TokenType.ERROR for token in self.tokens)

# 测试函数
def test_lexical_analyzer():
    """测试词法分析器"""
    analyzer = LexicalAnalyzer()
    
    # 测试代码
    test_code = """
program test;
var
    x, y: integer;
    result: real;
begin
    x := 10;
    y := 20;
    result := x + y * 2.5;
    if result > 50 then
        writeln('Result is large')
    else
        writeln('Result is small');
end.
"""
    
    print("=== 词法分析测试 ===")
    print(f"源代码:\n{test_code}")
    print("\n=== 分析结果 ===")
    
    tokens = analyzer.analyze(test_code)
    
    # 输出Token
    for token in tokens:
        if token.type != TokenType.EOF:
            print(token)
    
    # 输出错误
    if analyzer.has_errors():
        print("\n=== 错误信息 ===")
        for error in analyzer.get_errors():
            print(error)
    else:
        print("\n词法分析完成，无错误。")

if __name__ == "__main__":
    test_lexical_analyzer()