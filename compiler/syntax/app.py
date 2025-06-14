import gradio as gr
from first_follow import process_first_follow
from lr0_dfa import build_lr0_output
from slr1_check import check_slr1, build_slr1_table
from lr1_dfa import build_lr1_output
from parser_engine import parse_sentence

def analyze_grammar(text, sentence):
    g = process_first_follow(text)
    ff_str = g.get_first_follow_str()

    # 判断是否为 SLR(1)
    slr_conflicts = check_slr1(g)
    is_slr1 = not slr_conflicts
    slr_result = "SLR(1) 分析表无冲突，文法是 SLR(1) 文法。" if is_slr1 else "\n".join(slr_conflicts)

    # 构造 LR(0)
    state_str, trans_str, svg0 = build_lr0_output(text)

    # 构造 LR(1)
    action_table, goto_table, svg1 = build_lr1_output(text)

    # 格式化 Action-Goto 表输出
    def format_table(table):
        lines = []
        for state in sorted(table.keys()):
            lines.append(f"状态 {state}:")
            for sym, act in sorted(table[state].items()):
                lines.append(f"  on '{sym}': {act}")
        return "\n".join(lines)

    action_str = format_table(action_table)
    goto_str = format_table(goto_table)

    # 分析句子（可选）
    if sentence.strip():
        used_method = "SLR(1)" if is_slr1 else "LR(1)"
        analysis_steps = parse_sentence(text, sentence, method=used_method)
    else:
        analysis_steps = [[0, '', '', '', '未提供句子']]

    return ff_str, slr_result, state_str, trans_str, svg0, action_str, goto_str, svg1, analysis_steps

with gr.Blocks() as demo:
    gr.Markdown("## 自底向上语法分析器（SLR优先）")

    with gr.Row():
        grammar_input = gr.Textbox(label="输入文法产生式", lines=8, placeholder="示例：\nE → E + T | T\nT → T * F | F\nF → id")
        sentence_input = gr.Textbox(label="待分析句子（可选）", placeholder="例如：id + id * id")

    analyze_btn = gr.Button("分析")

    with gr.Tab("基础分析"):
        ff_output = gr.Textbox(label="First / Follow 集", lines=10)
        slr_output = gr.Textbox(label="SLR(1) 判别结果", lines=4)

    with gr.Tab("自动机可视化"):
        states_output = gr.Textbox(label="LR(0) 项集（状态）", lines=10)
        trans_output = gr.Textbox(label="LR(0) 状态转移表", lines=8)
        svg0_output = gr.HTML(label="LR(0) 状态图")
        svg1_output = gr.HTML(label="LR(1) 状态图")

    with gr.Tab("分析表（Action-Goto）"):
        lr_action_output = gr.Textbox(label="Action 表", lines=12)
        lr_goto_output = gr.Textbox(label="Goto 表", lines=8)

    with gr.Tab("句子分析"):
        sentence_table = gr.Dataframe(
            headers=["步骤", "状态栈", "符号栈", "剩余输入", "动作"],
            interactive=False,
            datatype=["number", "str", "str", "str", "str"]
        )

    analyze_btn.click(fn=analyze_grammar,
                      inputs=[grammar_input, sentence_input],
                      outputs=[ff_output, slr_output, states_output, trans_output, svg0_output,
                               lr_action_output, lr_goto_output, svg1_output, sentence_table])

demo.launch()
