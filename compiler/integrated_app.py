#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成分析器Web界面

提供词法分析、语法分析和AST构建的统一Web界面。
包括：
- 源代码输入和分析
- 词法分析结果展示
- 语法分析过程演示
- AST可视化
- 错误报告和调试信息
"""

import gradio as gr
import json
from typing import List, Dict, Any, Optional, Tuple
import traceback

# 导入集成分析器
from .integrated_analyzer import (
    IntegratedAnalyzer, AnalysisResult, 
    create_integrated_analyzer, analyze_code_complete
)

# 导入AST相关模块
from .syntax.ast_nodes import ASTVisualizer


class IntegratedWebApp:
    """
    集成分析器Web应用类
    """
    
    def __init__(self):
        self.analyzer = None
        self.current_language = 'c'
        self.analysis_result = None
        
    def create_analyzer(self, language: str):
        """创建分析器"""
        self.current_language = language
        self.analyzer = create_integrated_analyzer(language)
        return f"已创建{language.upper()}语言分析器"
    
    def analyze_source_code(self, source_code: str, language: str, custom_grammar: str, sentence: str) -> Tuple[str, str, str, str, str, str, str, str]:
        """
        分析源代码
        
        Returns:
            (词法分析结果, 语法分析结果, AST树形结构, AST图形, 分析步骤, 错误信息, 统计信息, 语义分析结果)
        """
        try:
            # 创建或更新分析器
            if not self.analyzer or self.current_language != language:
                self.create_analyzer(language)
            
            # 设置自定义文法
            if custom_grammar.strip():
                self.analyzer.set_grammar(custom_grammar)
            
            # 执行分析
            self.analysis_result = self.analyzer.analyze_code(source_code, sentence)
            
            # 格式化结果
            lexical_result = self._format_lexical_result()
            syntax_result = self._format_syntax_result()
            ast_tree = self._format_ast_tree()
            ast_graph = self._format_ast_graph()
            parse_steps = self._format_parse_steps()
            errors = self._format_errors()
            stats = self._format_statistics()
            semantic_output = self._format_semantic_result()
            
            return lexical_result, syntax_result, ast_tree, ast_graph, parse_steps, errors, stats, semantic_output
            
        except Exception as e:
            error_msg = f"分析过程中出现错误:\n{str(e)}\n\n详细信息:\n{traceback.format_exc()}"
            return "", "", "", "", "", error_msg, "", ""
    
    def _format_lexical_result(self) -> str:
        """格式化词法分析结果"""
        if not self.analysis_result or not self.analysis_result.tokens:
            return "无词法分析结果"
        
        lines = []
        lines.append("=== 词法分析结果 ===")
        lines.append(f"Token总数: {self.analysis_result.token_count}")
        lines.append("-" * 60)
        lines.append(f"{'序号':<4} {'类型':<20} {'值':<20} {'位置':<10}")
        lines.append("-" * 60)
        
        for i, token in enumerate(self.analysis_result.tokens, 1):
            if hasattr(token, 'type') and token.type.value != 'EOF':
                position = f"{getattr(token, 'line', 'N/A')}:{getattr(token, 'column', 'N/A')}"
                lines.append(f"{i:<4} {token.type.value:<20} {str(token.value):<20} {position:<10}")
        
        if self.analysis_result.lexical_errors:
            lines.append("\n=== 词法错误 ===")
            for error in self.analysis_result.lexical_errors:
                lines.append(f"❌ {error}")
        
        return "\n".join(lines)
    
    def _format_syntax_result(self) -> str:
        """格式化语法分析结果"""
        if not self.analysis_result:
            return "无语法分析结果"
        
        lines = []
        lines.append("=== 语法分析结果 ===")
        
        # First/Follow集
        if self.analysis_result.first_follow:
            lines.append("\n--- First/Follow集 ---")
            lines.append(self.analysis_result.first_follow)
        
        # SLR(1)判断
        lines.append("\n--- SLR(1)文法判断 ---")
        lines.append(f"是否为SLR(1)文法: {'是' if self.analysis_result.is_slr1 else '否'}")
        lines.append(self.analysis_result.slr1_result)
        
        # LR(0)状态
        if self.analysis_result.lr0_states:
            lines.append("\n--- LR(0)状态 ---")
            lines.append(self.analysis_result.lr0_states[:1000] + "..." if len(self.analysis_result.lr0_states) > 1000 else self.analysis_result.lr0_states)
        
        return "\n".join(lines)
    
    def _format_ast_tree(self) -> str:
        """格式化AST树形结构"""
        if not self.analysis_result or not self.analysis_result.ast_tree_string:
            return "无AST结果或分析失败"
        
        lines = []
        lines.append("=== 抽象语法树 (AST) ===")
        lines.append("")
        lines.append(self.analysis_result.ast_tree_string)
        
        return "\n".join(lines)
    
    def _format_ast_graph(self) -> str:
        """格式化AST图形表示"""
        if not self.analysis_result:
            return "<p>无AST结果</p>"
        
        # 优先返回SVG
        if self.analysis_result.ast_svg:
            return self.analysis_result.ast_svg
        
        # 如果没有SVG，返回DOT图
        if self.analysis_result.ast_dot_graph:
            return f"<pre>{self.analysis_result.ast_dot_graph}</pre>"
        
        return "<p>无AST图形表示</p>"
    
    def _format_parse_steps(self) -> str:
        """格式化分析步骤"""
        if not self.analysis_result or not self.analysis_result.parse_steps:
            return "无分析步骤"
        
        lines = []
        lines.append("=== 语法分析步骤 ===")
        lines.append("-" * 100)
        lines.append(f"{'步骤':<4} {'栈':<15} {'符号':<20} {'输入':<20} {'动作':<30} {'AST操作':<15}")
        lines.append("-" * 100)
        
        for step in self.analysis_result.parse_steps:
            if isinstance(step, dict):
                # 新格式
                step_num = step.get('step', '')
                stack = step.get('stack', '')
                symbols = step.get('symbols', '')
                input_str = step.get('input', '')
                action = step.get('action', '')
                ast_action = step.get('ast_action', '')
                
                lines.append(f"{str(step_num):<4} {stack:<15} {symbols:<20} {input_str:<20} {action:<30} {ast_action:<15}")
            else:
                # 兼容旧格式
                if len(step) >= 5:
                    lines.append(f"{str(step[0]):<4} {str(step[1]):<15} {str(step[2]):<20} {str(step[3]):<20} {str(step[4]):<30} {'N/A':<15}")
        
        return "\n".join(lines)
    
    def _format_errors(self) -> str:
        """格式化错误信息"""
        if not self.analysis_result:
            return "无错误信息"
        
        lines = []
        
        # 词法错误
        if self.analysis_result.lexical_errors:
            lines.append("=== 词法错误 ===")
            for error in self.analysis_result.lexical_errors:
                lines.append(f"❌ {error}")
            lines.append("")
        
        # 语法错误
        if self.analysis_result.syntax_errors:
            lines.append("=== 语法错误 ===")
            for error in self.analysis_result.syntax_errors:
                lines.append(f"❌ {error}")
            lines.append("")

        # 语义错误
        if hasattr(self.analysis_result, 'semantic_errors') and self.analysis_result.semantic_errors:
            lines.append("=== 语义错误 ===")
            for error in self.analysis_result.semantic_errors:
                lines.append(f"❌ {error}")
            lines.append("")
        
        if not lines:
            lines.append("✅ 无错误")
        
        return "\n".join(lines)

    def _format_semantic_result(self) -> str:
        """格式化语义分析结果"""
        if not self.analysis_result:
            return "无语义分析结果"

        lines = []
        lines.append("=== 语义分析结果 ===")

        if hasattr(self.analysis_result, 'semantic_result') and self.analysis_result.semantic_result is not None:
            lines.append(f"最终语义结果: {str(self.analysis_result.semantic_result)}")
        else:
            lines.append("未生成最终语义结果或分析失败")
        
        lines.append("\n--- 符号表 ---")
        if hasattr(self.analysis_result, 'symbol_table_string') and self.analysis_result.symbol_table_string:
            lines.append(self.analysis_result.symbol_table_string)
        else:
            lines.append("无符号表信息")
        
        return "\n".join(lines)
    
    def _format_statistics(self) -> str:
        """格式化统计信息"""
        if not self.analysis_result:
            return "无统计信息"
        
        lines = []
        lines.append("=== 分析统计 ===")
        lines.append(f"Token数量: {self.analysis_result.token_count}")
        lines.append(f"分析时间: {self.analysis_result.analysis_time:.4f}秒")
        lines.append(f"分析状态: {'成功' if self.analysis_result.success else '失败'}")
        lines.append(f"是否为SLR(1): {'是' if self.analysis_result.is_slr1 else '否'}")
        
        # AST统计
        if self.analysis_result.ast_root:
            lines.append(f"AST节点: 已生成")
            lines.append(f"AST可视化: {'可用' if self.analysis_result.ast_svg else '不可用'}")
        else:
            lines.append(f"AST节点: 未生成")
        
        return "\n".join(lines)


def create_web_interface():
    """
    创建Gradio Web界面
    """
    app = IntegratedWebApp()
    
    # 示例代码
    example_c_code = """int main() {
    int a = 5;
    int b = 3;
    int c = a + b;
    return 0;
}"""
    
    example_pascal_code = """program example;
var
    a, b, c: integer;
begin
    a := 5;
    b := 3;
    c := a + b;
end."""
    
    example_grammar = """E → E + T | E - T | T
T → T * F | T / F | F
F → ( E ) | id | num"""
    
    with gr.Blocks(title="集成编译器分析器 - 支持AST生成", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🔬 集成编译器分析器")
        gr.Markdown("**功能**: 词法分析 + 语法分析 + AST生成 + 可视化")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 📝 输入配置")
                
                language = gr.Dropdown(
                    choices=["c", "pascal"], 
                    value="c", 
                    label="编程语言"
                )
                
                source_code = gr.Textbox(
                    lines=10,
                    placeholder="请输入源代码...",
                    label="源代码",
                    value=example_c_code
                )
                
                custom_grammar = gr.Textbox(
                    lines=6,
                    placeholder="可选：自定义文法规则...",
                    label="自定义文法（可选）",
                    value=example_grammar
                )
                
                sentence = gr.Textbox(
                    placeholder="可选：待分析的句子（如：id + num * id）",
                    label="测试句子（可选）",
                    value="id + num * id"
                )
                
                analyze_btn = gr.Button("🚀 开始分析", variant="primary")
            
            with gr.Column(scale=2):
                gr.Markdown("## 📊 分析结果")
                
                with gr.Tabs():
                    with gr.TabItem("词法分析"):
                        lexical_output = gr.Textbox(
                            lines=15,
                            label="词法分析结果",
                            show_copy_button=True
                        )
                    
                    with gr.TabItem("语法分析"):
                        syntax_output = gr.Textbox(
                            lines=15,
                            label="语法分析结果",
                            show_copy_button=True
                        )
                    
                    with gr.TabItem("AST树形结构"):
                        ast_tree_output = gr.Textbox(
                            lines=15,
                            label="AST树形结构",
                            show_copy_button=True
                        )
                    
                    with gr.TabItem("AST图形"):
                        ast_graph_output = gr.HTML(
                            label="AST图形表示"
                        )
                    
                    with gr.TabItem("分析步骤"):
                        steps_output = gr.Textbox(
                            lines=15,
                            label="语法分析步骤",
                            show_copy_button=True
                        )
                    
                    with gr.TabItem("错误信息"):
                        errors_output = gr.Textbox(
                            lines=10,
                            label="错误信息"
                        )
                    
                    with gr.TabItem("统计信息"):
                        stats_output = gr.Textbox(
                            lines=10,
                            label="统计信息"
                        )
                    
                    with gr.TabItem("语义分析"):
                        semantic_output = gr.Textbox(
                            lines=15,
                            label="语义分析结果",
                            show_copy_button=True
                        )
        
        # 示例按钮
        with gr.Row():
            gr.Markdown("### 📚 示例")
        
        with gr.Row():
            example_c_btn = gr.Button("C语言示例")
            example_pascal_btn = gr.Button("Pascal示例")
            example_expr_btn = gr.Button("表达式示例")
        
        # 事件绑定
        analyze_btn.click(
            fn=app.analyze_source_code,
            inputs=[source_code, language, custom_grammar, sentence],
            outputs=[lexical_output, syntax_output, ast_tree_output, ast_graph_output, steps_output, errors_output, stats_output, semantic_output]
        )
        
        # 示例按钮事件
        example_c_btn.click(
            lambda: ("c", example_c_code, example_grammar, "id + num"),
            outputs=[language, source_code, custom_grammar, sentence]
        )
        
        example_pascal_btn.click(
            lambda: ("pascal", example_pascal_code, "", "id := num"),
            outputs=[language, source_code, custom_grammar, sentence]
        )
        
        example_expr_btn.click(
            lambda: ("c", "a + b * c", example_grammar, "id + id * id"),
            outputs=[language, source_code, custom_grammar, sentence]
        )
        
        # 语言切换事件
        language.change(
            lambda lang: example_c_code if lang == "c" else example_pascal_code,
            inputs=[language],
            outputs=[source_code]
        )
    
    return interface


def main():
    """
    主函数：启动Web应用
    """
    print("🚀 启动集成分析器Web界面...")
    
    try:
        # 测试模块导入
        print("📦 测试模块导入...")
        from .integrated_analyzer import create_integrated_analyzer
        analyzer = create_integrated_analyzer('c')
        print("✅ 模块导入成功")
        
        # 创建Web界面
        print("🌐 创建Web界面...")
        interface = create_web_interface()
        print("✅ Web界面创建成功")
        
        # 启动服务器
        print("🔥 启动服务器...")
        interface.launch(
            server_name="127.0.0.1",
            server_port=7861,
            share=False,
            quiet=False,
            show_error=True
        )
        
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断，正在关闭服务器...")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print(f"详细错误: {traceback.format_exc()}")


if __name__ == "__main__":
    main()