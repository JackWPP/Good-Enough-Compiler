#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback

try:
    from compiler.syntax.first_follow import process_first_follow
    from compiler.syntax.lr0_dfa import LR0DFA
    
    grammar_text = """E → E + T | T
T → T * F | F
F → ( E ) | id"""
    
    sentence = "id + id"
    
    print("🚀 开始测试语法分析...")
    print(f"📝 句子: {sentence}")
    print("-" * 30)
    
    # 构建Grammar对象
    grammar = process_first_follow(grammar_text)
    
    # 构建LR0 DFA以获取states和transitions
    from compiler.syntax.lr0_dfa import LR0DFA
    lines = [line.strip() for line in grammar_text.strip().split('\n') if line.strip()]
    dfa = LR0DFA(lines)
    grammar.states = dfa.states
    grammar.transitions = dfa.transitions
    
    # 构建SLR(1)分析表
    from compiler.syntax.slr1_check import build_slr1_table
    try:
        action_table, goto_table = build_slr1_table(grammar)
        print("✅ SLR(1)分析表构建成功！")
    except Exception as e:
        print(f"❌ SLR(1)分析表构建失败: {e}")
        exit(1)
    
    # 测试完整的语法分析
    from compiler.syntax.parser_engine import parse_sentence
    result = parse_sentence(grammar_text, sentence, method="SLR(1)", build_ast=True)
    
    print(f"📊 分析结果: {'✅ 成功' if result['success'] else '❌ 失败'}")
    print(f"📈 步骤数: {len(result['steps'])}")
    
    if not result['success']:
        print("\n🔍 最后几个分析步骤:")
        for i, step in enumerate(result['steps'][-3:], len(result['steps'])-2):
            action = step.get('action', 'unknown')
            print(f"  步骤{i}: {action}")
    
    ast = result.get('ast', None)
    if ast:
        print(f"✅ AST生成成功!")
        print(f"AST根节点: {ast.get('root', 'N/A')}")
        if 'tree' in ast:
            print(f"AST树结构:\n{ast['tree']}")
    else:
        print("⚠️ 未生成AST")
        if 'error' in result:
            print(f"错误信息: {result['error']}")
    
    # 显示错误信息（如果有）
    if 'error' in result:
        print(f"错误: {result['error']}")
        
except Exception as e:
    print(f"错误: {e}")
    print("详细错误信息:")
    traceback.print_exc()