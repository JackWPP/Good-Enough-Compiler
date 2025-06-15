#!/usr/bin/env python3
from compiler.lexical.analyzer import LexicalAnalyzer

# 创建C语言词法分析器
analyzer = LexicalAnalyzer()
analyzer.init_c_rules()

print(f'规则数量: {len(analyzer.rules)}')
print(f'关键字数量: {len(analyzer.keywords)}')

# 测试sample_code.c文件
with open('sample_code.c', 'r', encoding='utf-8') as f:
    test_code = f.read()

print(f'\n测试代码长度: {len(test_code)} 字符')
print(f'前50个字符: {repr(test_code[:50])}')

tokens = analyzer.analyze(test_code)
print(f'Token数量: {len(tokens)}')

print('\n前10个Token:')
for i, token in enumerate(tokens[:10]):
    print(f'  {i+1}: {token.type.value} - "{repr(token.value)}" (行{token.line}, 列{token.column})')

if analyzer.errors:
    print('\n错误信息:')
    for error in analyzer.errors:
        print(f'  {error}')