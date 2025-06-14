#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成编译器Web界面

将词法分析和语法分析集成在一个Web界面中，提供完整的编译前端功能。
"""

import gradio as gr
import sys
import os
from typing import List, Tuple, Any

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from compiler.integrated_analyzer import IntegratedAnalyzer, AnalysisResult, create_integrated_analyzer
from compiler.lexical import Token, TokenType


def analyze_complete(source_code: str, language: str, grammar_text: str, sentence: str) -> Tuple[str, str, str, str, str, str, str, str, str, str, List[List[str]], str, str]:
    """
    完整的编译分析函数
    
    Args:
        source_code: 源代码
        language: 编程语言
        grammar_text: 文法定义
        sentence: 待分析句子
        
    Returns:
        分析结果的各个组件
    """
    try:
        # 创建集成分析器
        analyzer = create_integrated_analyzer(language.lower())
        
        # 设置自定义文法（如果提供）
        if grammar_text.strip():
            analyzer.set_grammar(grammar_text)
        
        # 执行分析
        result = analyzer.analyze_code(source_code, sentence)
        
        # 格式化Token结果
        token_output = analyzer.format_tokens(result.tokens)
        
        # 格式化Action-Goto表
        action_str, goto_str = analyzer.format_action_goto_table(result.action_table, result.goto_table)
        
        # 构建分析摘要
        summary_lines = [
            f"分析完成时间: {result.analysis_time:.3f}秒",
            f"Token总数: {result.token_count}",
            f"词法错误: {len(result.lexical_errors)}",
            f"语法错误: {len(result.syntax_errors)}",
            f"分析状态: {'成功' if result.success else '失败'}",
            f"文法类型: {'SLR(1)' if result.is_slr1 else 'LR(1)'}"
        ]
        
        if result.lexical_errors:
            summary_lines.append("\n词法错误详情:")
            for error in result.lexical_errors:
                summary_lines.append(f"  - {error}")
        
        if result.syntax_errors:
            summary_lines.append("\n语法错误详情:")
            for error in result.syntax_errors:
                summary_lines.append(f"  - {error}")
        
        summary = "\n".join(summary_lines)
        
        # 处理AST信息
        ast_tree_str = result.ast_tree_string if result.ast_tree_string else "未生成AST（可能由于语法错误）"
        ast_svg_html = f'<div style="text-align: center;">{result.ast_svg}</div>' if result.ast_svg else "<div>未生成AST图形</div>"
        
        # 处理分析步骤格式转换
        if isinstance(result.parse_steps, list) and result.parse_steps:
            # 转换为表格格式
            parse_table_data = []
            for step in result.parse_steps:
                if isinstance(step, dict):
                    parse_table_data.append([
                        step.get('step', ''),
                        step.get('stack', ''),
                        step.get('symbols', ''),
                        step.get('input', ''),
                        step.get('action', '')
                    ])
                else:
                    # 兼容旧格式
                    parse_table_data.append(step)
        else:
            parse_table_data = [[0, '', '', '', '无分析步骤']]
        
        return (
            summary,
            token_output,
            result.first_follow,
            result.slr1_result,
            result.lr0_states,
            result.lr0_transitions,
            result.lr0_svg,
            action_str,
            goto_str,
            result.lr1_svg,
            parse_table_data,
            ast_tree_str,
            ast_svg_html
        )
        
    except Exception as e:
        error_msg = f"分析过程中发生错误: {str(e)}"
        return (
            error_msg,  # summary
            error_msg,  # token_output
            error_msg,  # first_follow
            error_msg,  # slr1_result
            error_msg,  # lr0_states
            error_msg,  # lr0_transitions
            "",         # lr0_svg
            error_msg,  # action_str
            error_msg,  # goto_str
            "",         # lr1_svg
            [[0, '', '', '', error_msg]],  # parse_steps
            error_msg,  # ast_tree_str
            "<div>分析错误，无法生成AST</div>"  # ast_svg_html
        )


def load_sample_code(language: str) -> Tuple[str, str]:
    """
    加载示例代码和对应的文法
    
    Args:
        language: 编程语言
        
    Returns:
        (sample_code, sample_grammar)
    """
    if language.lower() == 'c':
        sample_code = """int main() {
    int a, b, c;
    a = 5;
    b = 10;
    c = a + b * 2;
    return 0;
}"""
        sample_grammar = """program → function
function → type id ( ) { stmt_list }
stmt_list → stmt_list stmt | stmt
stmt → type id_list ; | id = expr ; | return expr ;
id_list → id_list , id | id
expr → expr + term | expr - term | term
term → term * factor | term / factor | factor
factor → ( expr ) | id | num
type → int | float | char"""
    else:  # Pascal
        sample_code = """program Example;
var
    a, b, c: integer;
begin
    a := 5;
    b := 10;
    c := a + b * 2;
end."""
        sample_grammar = """program → program id ; block .
block → var_decl stmt_list
var_decl → var id_list : type ;
id_list → id_list , id | id
stmt_list → begin stmt_seq end
stmt_seq → stmt_seq ; stmt | stmt
stmt → id := expr
expr → expr + term | expr - term | term
term → term * factor | term / factor | factor
factor → ( expr ) | id | num
type → integer | real | boolean"""
    
    return sample_code, sample_grammar


def create_integrated_interface():
    """
    创建集成的Web界面
    """
    with gr.Blocks(title="集成编译器 - 词法与语法分析") as demo:
        gr.Markdown("# 🔧 集成编译器 - 词法与语法分析器")
        gr.Markdown("这是一个集成的编译器前端，支持词法分析和语法分析的完整流程。")
        
        with gr.Row():
            with gr.Column(scale=2):
                # 输入区域
                gr.Markdown("## 📝 输入区域")
                
                language_choice = gr.Radio(
                    choices=["C", "Pascal"], 
                    value="C", 
                    label="编程语言"
                )
                
                source_input = gr.Textbox(
                    label="源代码",
                    lines=10,
                    placeholder="请输入源代码...",
                    value=""
                )
                
                grammar_input = gr.Textbox(
                    label="文法定义（可选，留空使用默认文法）",
                    lines=8,
                    placeholder="例如：\nE → E + T | T\nT → T * F | F\nF → ( E ) | id | num",
                    value=""
                )
                
                sentence_input = gr.Textbox(
                    label="待分析句子（可选，留空自动从源代码生成）",
                    placeholder="例如：id + id * id",
                    value=""
                )
                
                with gr.Row():
                    analyze_btn = gr.Button("🚀 开始分析", variant="primary")
                    load_sample_btn = gr.Button("📋 加载示例", variant="secondary")
            
            with gr.Column(scale=1):
                # 分析摘要
                gr.Markdown("## 📊 分析摘要")
                summary_output = gr.Textbox(
                    label="分析结果摘要",
                    lines=12,
                    interactive=False
                )
        
        # 结果展示区域
        with gr.Tabs():
            # 词法分析结果
            with gr.Tab("🔤 词法分析"):
                token_output = gr.Textbox(
                    label="Token序列",
                    lines=15,
                    interactive=False
                )
            
            # 语法分析基础
            with gr.Tab("📝 语法分析基础"):
                with gr.Row():
                    first_follow_output = gr.Textbox(
                        label="First / Follow 集",
                        lines=12,
                        interactive=False
                    )
                    slr1_output = gr.Textbox(
                        label="SLR(1) 判别结果",
                        lines=12,
                        interactive=False
                    )
            
            # 自动机可视化
            with gr.Tab("🔄 自动机可视化"):
                with gr.Row():
                    with gr.Column():
                        lr0_states_output = gr.Textbox(
                            label="LR(0) 项集（状态）",
                            lines=10,
                            interactive=False
                        )
                        lr0_trans_output = gr.Textbox(
                            label="LR(0) 状态转移表",
                            lines=8,
                            interactive=False
                        )
                    
                    with gr.Column():
                        lr0_svg_output = gr.HTML(label="LR(0) 状态图")
                        lr1_svg_output = gr.HTML(label="LR(1) 状态图")
            
            # 分析表
            with gr.Tab("📋 分析表（Action-Goto）"):
                with gr.Row():
                    action_output = gr.Textbox(
                        label="Action 表",
                        lines=15,
                        interactive=False
                    )
                    goto_output = gr.Textbox(
                        label="Goto 表",
                        lines=15,
                        interactive=False
                    )
            
            # 句子分析
            with gr.Tab("🔍 句子分析过程"):
                parse_table = gr.Dataframe(
                    headers=["步骤", "状态栈", "符号栈", "剩余输入", "动作"],
                    interactive=False,
                    datatype=["number", "str", "str", "str", "str"]
                )
            
            # AST语法树
            with gr.Tab("🌳 抽象语法树（AST）"):
                with gr.Row():
                    with gr.Column():
                        ast_tree_output = gr.Textbox(
                            label="AST树形结构",
                            lines=15,
                            interactive=False
                        )
                    with gr.Column():
                        ast_svg_output = gr.HTML(label="AST图形可视化")
        
        # 事件绑定
        analyze_btn.click(
            fn=analyze_complete,
            inputs=[source_input, language_choice, grammar_input, sentence_input],
            outputs=[
                summary_output,
                token_output,
                first_follow_output,
                slr1_output,
                lr0_states_output,
                lr0_trans_output,
                lr0_svg_output,
                action_output,
                goto_output,
                lr1_svg_output,
                parse_table,
                ast_tree_output,
                ast_svg_output
            ]
        )
        
        def load_sample(language):
            code, grammar = load_sample_code(language)
            return code, grammar
        
        load_sample_btn.click(
            fn=load_sample,
            inputs=[language_choice],
            outputs=[source_input, grammar_input]
        )
        
        # 语言切换时自动加载示例
        language_choice.change(
            fn=load_sample,
            inputs=[language_choice],
            outputs=[source_input, grammar_input]
        )
        
        # 添加使用说明
        with gr.Accordion("📖 使用说明", open=False):
            gr.Markdown("""
            ### 使用步骤：
            1. **选择编程语言**：支持C和Pascal语言
            2. **输入源代码**：可以手动输入或点击"加载示例"按钮
            3. **设置文法**（可选）：可以使用默认文法或自定义文法
            4. **指定分析句子**（可选）：留空将自动从源代码生成
            5. **点击"开始分析"**：执行完整的词法和语法分析
            
            ### 功能特性：
            - **词法分析**：将源代码分解为Token序列
            - **语法分析**：构建First/Follow集，判断文法类型
            - **自动机构造**：生成LR(0)和LR(1)状态自动机
            - **分析表生成**：构造Action-Goto分析表
            - **句子分析**：演示语法分析的逐步过程
            - **可视化**：提供状态转移图的SVG可视化
            
            ### 支持的文法格式：
            ```
            E → E + T | T
            T → T * F | F
            F → ( E ) | id | num
            ```
            
            ### 注意事项：
            - 使用 `→` 表示产生式
            - 使用 `|` 分隔多个候选式
            - 终结符和非终结符用空格分隔
            - 支持SLR(1)和LR(1)分析方法
            """)
    
    return demo


if __name__ == "__main__":
    try:
        print("正在初始化集成编译器...")
        
        # 测试导入
        print("测试模块导入...")
        analyzer = create_integrated_analyzer("c")
        print("模块导入成功!")
        
        print("创建Web界面...")
        demo = create_integrated_interface()
        print("Web界面创建成功!")
        
        print("启动集成编译器Web界面...")
        print("界面将在浏览器中打开，地址: http://localhost:7860")
        print("按 Ctrl+C 停止服务")
        
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            debug=False,
            quiet=False
        )
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()