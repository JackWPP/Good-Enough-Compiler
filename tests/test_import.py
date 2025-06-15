#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, '.')

try:
    from compiler.integrated_analyzer import create_integrated_analyzer
    print("Import successful!")
    
    # 测试创建分析器
    analyzer = create_integrated_analyzer('c')
    print("Analyzer created successfully!")
    
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()