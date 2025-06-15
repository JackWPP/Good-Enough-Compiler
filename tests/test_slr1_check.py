#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from integrated_app import load_sample_code
from compiler.syntax.first_follow import process_first_follow
from compiler.syntax.slr1_check import check_slr1

def test_slr1_check():
    print("测试SLR(1)冲突检测...")
    
    # 加载示例语法
    code, grammar = load_sample_code('c')
    print(f"示例语法: {repr(grammar)}")
    print("\n" + "="*50 + "\n")
    
    # 处理First/Follow集
    g = process_first_follow(grammar)
    print(f"语法对象: {g}")
    print(f"产生式数量: {len(g.productions)}")
    
    # 检查SLR(1)冲突
    slr_conflicts = check_slr1(g)
    is_slr1 = not slr_conflicts
    
    print(f"SLR(1)冲突: {slr_conflicts}")
    print(f"是否为SLR(1): {is_slr1}")
    
    if slr_conflicts:
        print("冲突详情:")
        for conflict in slr_conflicts:
            print(f"  - {conflict}")
    else:
        print("无冲突，是SLR(1)文法")

if __name__ == "__main__":
    test_slr1_check()