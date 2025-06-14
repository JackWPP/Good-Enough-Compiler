#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from integrated_app import load_sample_code
from compiler.syntax.parser_engine import parse_sentence

def test_sample_grammar():
    print("测试示例语法...")
    
    # 加载C语言示例
    code, grammar = load_sample_code('c')
    print("C语言示例语法:")
    print(grammar)
    print("\n" + "="*50 + "\n")
    
    # 测试简单句子
    test_sentences = [
        "id + id",
        "id * id",
        "( id )",
        "id + id * id"
    ]
    
    for sentence in test_sentences:
        print(f"测试句子: {sentence}")
        try:
            result = parse_sentence(grammar, sentence, method="SLR(1)", build_ast=True)
            if isinstance(result, dict):
                print(f"  解析成功: {result.get('success', False)}")
                if 'ast' in result:
                    print(f"  AST生成: 是")
                else:
                    print(f"  AST生成: 否")
                # 显示最后几个步骤
                steps = result.get('steps', [])
                if steps:
                    last_step = steps[-1]
                    print(f"  最后动作: {last_step.get('action', 'unknown')}")
            else:
                print(f"  旧格式结果: {len(result) if result else 0} 步骤")
        except Exception as e:
            print(f"  错误: {e}")
        print()

if __name__ == "__main__":
    test_sample_grammar()