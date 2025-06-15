#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from compiler.integrated_analyzer import IntegratedAnalyzer
from integrated_app import load_sample_code

def test_full_analysis():
    print("测试完整分析流程...")
    
    # 创建分析器
    analyzer = IntegratedAnalyzer('c')
    
    # 加载示例
    code, grammar = load_sample_code('c')
    print(f"示例代码: {code[:50]}...")
    print(f"示例语法: {grammar}")
    print("\n" + "="*50 + "\n")
    
    # 设置语法
    analyzer.set_grammar(grammar)
    
    # 测试直接句子分析
    test_sentence = "id + id"
    print(f"直接测试句子: {test_sentence}")
    result = analyzer.analyze_complete(code, test_sentence)
    
    print(f"分析步骤数量: {len(result.parse_steps)}")
    if result.parse_steps:
        last_step = result.parse_steps[-1]
        if isinstance(last_step, dict):
            print(f"最后动作: {last_step.get('action', 'unknown')}")
        else:
            print(f"最后步骤: {last_step}")
    
    print(f"AST树形结构: {result.ast_tree_string[:100] if result.ast_tree_string else 'None'}...")
    print(f"AST SVG: {'有' if result.ast_svg else '无'}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试从代码生成句子
    print("测试从代码自动生成句子:")
    result2 = analyzer.analyze_complete(code, "")
    
    print(f"分析步骤数量: {len(result2.parse_steps)}")
    if result2.parse_steps:
        last_step = result2.parse_steps[-1]
        if isinstance(last_step, dict):
            print(f"最后动作: {last_step.get('action', 'unknown')}")
        else:
            print(f"最后步骤: {last_step}")
    
    print(f"AST树形结构: {result2.ast_tree_string[:100] if result2.ast_tree_string else 'None'}...")
    print(f"AST SVG: {'有' if result2.ast_svg else '无'}")

if __name__ == "__main__":
    test_full_analysis()