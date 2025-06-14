#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
from integrated_app import analyze_complete, load_sample_code
from compiler.syntax.parser_engine import parse_sentence
from compiler.syntax.lr1_dfa import build_lr1_output

def debug_analyze():
    print("调试analyze_complete函数...")
    
    try:
        # 加载示例
        code, grammar = load_sample_code('c')
        print(f"示例代码: {repr(code)}")
        print(f"示例语法: {repr(grammar)}")
        print("\n" + "="*50 + "\n")
        
        # 直接测试parse_sentence函数
        print("直接测试parse_sentence函数...")
        sentence = "id + id"
        print(f"测试句子: {sentence}")
        
        # 测试LR(1)方法
        print("\n使用LR(1)方法:")
        try:
            result = parse_sentence(grammar, sentence, method="LR(1)", build_ast=True)
            print(f"解析结果: {result}")
            if 'steps' in result:
                print(f"步骤数: {len(result['steps'])}")
                if result['steps']:
                    print(f"最后步骤: {result['steps'][-1]}")
            if 'ast' in result:
                print(f"AST: {result['ast']}")
        except Exception as e:
            print(f"LR(1)解析失败: {e}")
            traceback.print_exc()
        
        # 测试SLR(1)方法
        print("\n使用SLR(1)方法:")
        try:
            result = parse_sentence(grammar, sentence, method="SLR(1)", build_ast=True)
            print(f"解析结果: {result}")
            if 'steps' in result:
                print(f"步骤数: {len(result['steps'])}")
                if result['steps']:
                    print(f"最后步骤: {result['steps'][-1]}")
            if 'ast' in result:
                print(f"AST: {result['ast']}")
        except Exception as e:
            print(f"SLR(1)解析失败: {e}")
            traceback.print_exc()
        
        # 检查分析表
        print("\n检查LR(1)分析表:")
        try:
            action_table, goto_table, svg = build_lr1_output(grammar)
            print(f"Action表状态数: {len(action_table)}")
            print(f"Goto表状态数: {len(goto_table)}")
            
            # 检查状态0的动作
            if 0 in action_table:
                print(f"状态0的动作: {action_table[0]}")
            if 0 in goto_table:
                print(f"状态0的GOTO: {goto_table[0]}")
        except Exception as e:
            print(f"构建分析表失败: {e}")
            traceback.print_exc()
        
        print("\n" + "="*50 + "\n")
        
        # 调用analyze_complete
        print("调用analyze_complete...")
        result = analyze_complete(code, 'c', grammar, 'id + id')
        
        print(f"返回结果类型: {type(result)}")
        print(f"返回结果长度: {len(result)}")
        
        # 检查第一个元素（summary）
        summary = result[0]
        print(f"Summary: {summary[:200]}...")
        
        # 检查AST相关结果
        ast_tree_str = result[11]  # ast_tree_str
        ast_svg_html = result[12]  # ast_svg_html
        
        print(f"AST树形结构: {ast_tree_str[:100]}...")
        print(f"AST SVG HTML: {ast_svg_html[:100]}...")
        
        # 检查分析步骤
        parse_steps = result[10]  # parse_table_data
        print(f"分析步骤数量: {len(parse_steps)}")
        if parse_steps:
            print(f"最后一步: {parse_steps[-1]}")
        
    except Exception as e:
        print(f"发生异常: {e}")
        print("详细错误信息:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_analyze()