#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from integrated_app import create_integrated_interface
    print("Import successful!")
    
    # 测试创建界面
    demo = create_integrated_interface()
    print("Interface creation successful!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()