#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Good-Enough-Compiler - 主程序

一个教学用的编译器实现，支持C语言和Pascal语言的词法分析。
这是使用模块化API的新版本主程序。

功能特性：
- 词法分析（支持C和Pascal）
- 正则表达式到自动机转换
- 可视化界面
- 命令行工具
- 详细的分析报告

使用方法：
    python main_new.py [选项] [文件]
    
选项：
    --gui, -g           启动图形界面
    --analyze, -a       分析指定文件
    --language, -l      指定语言 (c/pascal)
    --output, -o        指定输出文件
    --verbose, -v       详细输出
    --help, -h          显示帮助信息
    --version           显示版本信息
    --create-samples    创建示例文件
    --test-regex        测试正则表达式转换
"""

import sys
import os
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    # 导入编译器模块
    from compiler import (
        Compiler, CompilerConfig, CompilationResult,
        compile_file, compile_source, analyze_tokens,
        get_supported_languages, get_compiler_info
    )
    from compiler.lexical import RegexToNFA, NFAToDFA, DFAMinimizer
    from compiler.utils import read_file_safe, write_file_safe
except ImportError as e:
    print(f"错误：无法导入编译器模块: {e}")
    print("请确保所有依赖都已正确安装")
    sys.exit(1)


def create_sample_files():
    """
    创建示例文件
    """
    print("创建示例文件...")
    
    # C语言示例
    c_sample = '''
#include <stdio.h>
#include <stdlib.h>

// 计算阶乘的函数
int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// 主函数
int main() {
    int num = 5;
    int result;
    
    printf("计算 %d 的阶乘\\n", num);
    result = factorial(num);
    printf("%d! = %d\\n", num, result);
    
    return 0;
}
'''
    
    # Pascal语言示例
    pascal_sample = '''
program FactorialExample;

{ 计算阶乘的函数 }
function Factorial(n: integer): integer;
begin
    if n <= 1 then
        Factorial := 1
    else
        Factorial := n * Factorial(n - 1);
end;

{ 主程序 }
var
    num, result: integer;
begin
    num := 5;
    writeln('计算 ', num, ' 的阶乘');
    result := Factorial(num);
    writeln(num, '! = ', result);
end.
'''
    
    try:
        # 写入C语言示例
        c_file = "sample_code.c"
        error = write_file_safe(c_file, c_sample)
        if error:
            print(f"创建C语言示例失败: {error}")
        else:
            print(f"✓ 创建C语言示例: {c_file}")
        
        # 写入Pascal语言示例
        pascal_file = "sample_code.pas"
        error = write_file_safe(pascal_file, pascal_sample)
        if error:
            print(f"创建Pascal语言示例失败: {error}")
        else:
            print(f"✓ 创建Pascal语言示例: {pascal_file}")
        
        print("\n示例文件创建完成！")
        print("使用以下命令分析示例：")
        print(f"  python {sys.argv[0]} -a {c_file} -l c")
        print(f"  python {sys.argv[0]} -a {pascal_file} -l pascal")
        
    except Exception as e:
        print(f"创建示例文件时发生错误: {e}")


def test_regex_conversion(pattern="a|b"):
    """
    测试正则表达式转换
    
    Args:
        pattern: 正则表达式模式
    """
    print(f"测试正则表达式转换: {pattern}")
    print("=" * 50)
    
    try:
        # 正则表达式转NFA
        print("1. 正则表达式 -> NFA")
        regex_converter = RegexToNFA()
        nfa = regex_converter.convert(pattern)
        print(f"   NFA状态数: {len(nfa.states)}")
        print(f"   起始状态: {nfa.start_state}")
        print(f"   接受状态: {nfa.accept_states}")
        
        # NFA转DFA
        print("\n2. NFA -> DFA")
        nfa_to_dfa = NFAToDFA()
        dfa = nfa_to_dfa.convert(nfa)
        print(f"   DFA状态数: {len(dfa.states)}")
        print(f"   起始状态: {dfa.start_state}")
        print(f"   接受状态: {dfa.accept_states}")
        
        # DFA最小化
        print("\n3. DFA最小化")
        minimizer = DFAMinimizer()
        minimized_dfa = minimizer.minimize(dfa)
        print(f"   最小化DFA状态数: {len(minimized_dfa.states)}")
        print(f"   起始状态: {minimized_dfa.start_state}")
        print(f"   接受状态: {minimized_dfa.accept_states}")
        
        # 显示转移表
        if len(dfa.states) <= 10:  # 只有状态数较少时才显示
            print("\n4. DFA转移表:")
            alphabet = sorted(set(symbol for (_, symbol), _ in dfa.transitions.items()))
            states = sorted(dfa.states)
            
            # 表头
            header = "状态\t" + "\t".join(alphabet)
            print(header)
            print("-" * len(header.expandtabs()))
            
            # 转移表
            for state in states:
                row = f"{state}\t"
                for symbol in alphabet:
                    next_state = dfa.transitions.get((state, symbol), "")
                    row += f"{next_state}\t"
                print(row)
        
        print("\n转换完成！")
        
    except Exception as e:
        print(f"转换过程中发生错误: {e}")


def analyze_file_command(filename, language=None, output=None, verbose=False):
    """
    分析文件命令
    
    Args:
        filename: 文件路径
        language: 指定语言
        output: 输出文件
        verbose: 详细输出
    """
    print(f"分析文件: {filename}")
    
    if not os.path.exists(filename):
        print(f"错误：文件不存在: {filename}")
        return
    
    try:
        # 创建编译器配置
        config = CompilerConfig()
        if language:
            config.language = language
        config.verbose = verbose
        config.output_tokens = True
        
        # 编译文件
        result = compile_file(filename, output, **config.to_dict())
        
        # 显示结果
        print(f"\n{result.get_summary()}")
        print(f"处理时间: {result.processing_time:.3f}秒")
        
        if verbose:
            # 显示详细统计
            if result.statistics:
                print("\n=== 统计信息 ===")
                stats = result.statistics
                print(f"总Token数: {stats.get('total_tokens', 0)}")
                print(f"总行数: {stats.get('total_lines', 0)}")
                print(f"总字符数: {stats.get('total_characters', 0)}")
                
                # Token类型统计
                if 'token_counts' in stats:
                    print("\nToken类型统计:")
                    for token_type, count in sorted(stats['token_counts'].items(), 
                                                   key=lambda x: x[1], reverse=True)[:10]:
                        percentage = (count / stats.get('total_tokens', 1)) * 100
                        print(f"  {token_type:<20}: {count:>6} ({percentage:>5.1f}%)")
        
        # 显示错误
        if result.errors:
            print("\n=== 错误信息 ===")
            for i, error in enumerate(result.errors[:5], 1):  # 只显示前5个错误
                print(f"{i}. 第{error.get('line', '?')}行，第{error.get('column', '?')}列: {error.get('message', '')}")
            
            if len(result.errors) > 5:
                print(f"... 还有 {len(result.errors) - 5} 个错误")
        
        # 显示输出文件
        if result.output_files:
            print("\n=== 输出文件 ===")
            for output_file in result.output_files:
                print(f"  {output_file}")
        
    except Exception as e:
        print(f"分析过程中发生错误: {e}")


def start_gui():
    """
    启动图形界面
    """
    try:
        import gradio as gr
        from compiler.lexical import create_c_analyzer, create_pascal_analyzer
        from compiler.utils import format_token_table, format_statistics, create_html_report
        
        def analyze_code(code, language, show_details):
            """
            分析代码的Gradio接口函数
            """
            if not code.strip():
                return "请输入代码", "", ""
            
            try:
                # 使用编译器API分析代码
                result = compile_source(code, language=language)
                
                # 生成输出
                output = []
                output.append(f"=== 分析结果 ===")
                output.append(f"语言: {result.language}")
                output.append(f"Token数: {len(result.tokens)}")
                output.append(f"错误数: {len(result.errors)}")
                output.append(f"处理时间: {result.processing_time:.3f}秒")
                
                if result.errors:
                    output.append("\n=== 错误信息 ===")
                    for error in result.errors[:5]:
                        output.append(f"第{error.get('line', '?')}行: {error.get('message', '')}")
                
                # Token表格
                token_table = ""
                if result.tokens and show_details:
                    token_table = format_token_table(result.tokens[:50])  # 限制显示数量
                
                # 统计信息
                stats_info = ""
                if result.statistics and show_details:
                    stats_info = format_statistics(result.statistics)
                
                return "\n".join(output), token_table, stats_info
                
            except Exception as e:
                return f"分析失败: {str(e)}", "", ""
        
        # 创建Gradio界面
        with gr.Blocks(title="Good-Enough-Compiler", theme=gr.themes.Soft()) as demo:
            gr.Markdown("# Good-Enough-Compiler")
            gr.Markdown("一个教学用的编译器实现，支持C语言和Pascal语言的词法分析")
            
            with gr.Row():
                with gr.Column(scale=2):
                    code_input = gr.Textbox(
                        label="源代码",
                        placeholder="请输入C语言或Pascal代码...",
                        lines=15,
                        max_lines=20
                    )
                    
                    with gr.Row():
                        language_choice = gr.Radio(
                            choices=["c", "pascal"],
                            value="c",
                            label="编程语言"
                        )
                        show_details = gr.Checkbox(
                            label="显示详细信息",
                            value=True
                        )
                    
                    analyze_btn = gr.Button("分析代码", variant="primary")
                
                with gr.Column(scale=2):
                    result_output = gr.Textbox(
                        label="分析结果",
                        lines=10,
                        max_lines=15
                    )
            
            with gr.Row():
                with gr.Column():
                    token_output = gr.Textbox(
                        label="Token表格",
                        lines=10,
                        max_lines=15
                    )
                
                with gr.Column():
                    stats_output = gr.Textbox(
                        label="统计信息",
                        lines=10,
                        max_lines=15
                    )
            
            # 示例代码
            with gr.Row():
                gr.Examples(
                    examples=[
                        ["#include <stdio.h>\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}", "c"],
                        ["program Hello;\nbegin\n    writeln('Hello, World!');\nend.", "pascal"]
                    ],
                    inputs=[code_input, language_choice],
                    label="示例代码"
                )
            
            # 绑定事件
            analyze_btn.click(
                fn=analyze_code,
                inputs=[code_input, language_choice, show_details],
                outputs=[result_output, token_output, stats_output]
            )
        
        print("启动Web界面...")
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
        
    except ImportError:
        print("错误：Gradio未安装，无法启动图形界面")
        print("请运行: pip install gradio")
    except Exception as e:
        print(f"启动图形界面失败: {e}")


def show_version():
    """
    显示版本信息
    """
    info = get_compiler_info()
    print(f"{info['name']} v{info['version']}")
    print(f"{info['description']}")
    print(f"\n支持的语言: {', '.join(info['supported_languages'])}")
    print(f"\n功能状态:")
    for feature, status in info['features'].items():
        status_text = "✓" if status else "✗"
        print(f"  {status_text} {feature}")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(
        description="Good-Enough-Compiler - 教学用编译器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --gui                    # 启动图形界面
  %(prog)s -a sample.c -l c         # 分析C语言文件
  %(prog)s -a sample.pas -l pascal  # 分析Pascal文件
  %(prog)s --create-samples         # 创建示例文件
  %(prog)s --test-regex "a|b"       # 测试正则表达式转换
"""
    )
    
    parser.add_argument('file', nargs='?', help='要分析的源文件')
    parser.add_argument('-g', '--gui', action='store_true', help='启动图形界面')
    parser.add_argument('-a', '--analyze', metavar='FILE', help='分析指定文件')
    parser.add_argument('-l', '--language', choices=['c', 'pascal'], help='指定编程语言')
    parser.add_argument('-o', '--output', metavar='FILE', help='输出文件路径')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('--version', action='store_true', help='显示版本信息')
    parser.add_argument('--create-samples', action='store_true', help='创建示例文件')
    parser.add_argument('--test-regex', metavar='PATTERN', help='测试正则表达式转换')
    
    args = parser.parse_args()
    
    # 处理命令行参数
    if args.version:
        show_version()
    elif args.create_samples:
        create_sample_files()
    elif args.test_regex:
        test_regex_conversion(args.test_regex)
    elif args.gui:
        start_gui()
    elif args.analyze or args.file:
        filename = args.analyze or args.file
        analyze_file_command(filename, args.language, args.output, args.verbose)
    else:
        # 默认启动图形界面
        print("欢迎使用 Good-Enough-Compiler!")
        print("\n可用选项:")
        print("  --gui           启动图形界面")
        print("  --analyze FILE  分析文件")
        print("  --help          显示帮助")
        print("\n默认启动图形界面...")
        start_gui()


if __name__ == "__main__":
    main()