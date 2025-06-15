# 正则表达式toNFA-Code

# 完整代码

```python
import graphviz
import io
from PIL import Image
import gradio as gr

class State:
    """表示自动机中的一个状态"""
    def __init__(self, id):
        self.id = id
        self.transitions = {}  # 存储状态转移: symbol -> [target_states]
        self.is_end = False    # 是否为接受状态
        self.epsilon_moves = []  # 存储ε转移可达的状态

class NFA:
    """非确定有限自动机"""
    def __init__(self):
        self.states = []       # 所有状态列表
        self.start_state = None  # 开始状态
        self.end_states = []   # 接受状态列表
        self.alphabet = set()  # 字母表(输入符号集)

    def create_state(self):
        """创建并添加新状态"""
        state = State(len(self.states))
        self.states.append(state)
        return state

    def set_start(self, state):
        """设置开始状态"""
        self.start_state = state

    def add_end(self, state):
        """添加接受状态"""
        state.is_end = True
        self.end_states.append(state)

    def add_transition(self, from_state, symbol, to_state):
        """添加状态转移"""
        if symbol != 'ε':
            self.alphabet.add(symbol)
            
        if symbol in from_state.transitions:
            from_state.transitions[symbol].append(to_state)
        else:
            from_state.transitions[symbol] = [to_state]
            
        if symbol == 'ε':
            from_state.epsilon_moves.append(to_state)
    
    def get_transition_table(self):
        """获取状态转移表"""
        table = []
        # 表头行
        header = ["状态ID", "是否接受状态"]
        symbols = sorted(list(self.alphabet))
        header.extend(symbols)
        header.append('ε')
        table.append(header)
        
        # 添加每个状态的转移信息
        for state in self.states:
            row = [f"q{state.id}", "是" if state.is_end else "否"]
            
            # 添加每个符号的转移
            for symbol in symbols:
                if symbol in state.transitions:
                    targets = state.transitions[symbol]
                    targets_str = ",".join([f"q{t.id}" for t in targets])
                    row.append(targets_str)
                else:
                    row.append("-")
            
            # 添加ε转移
            if 'ε' in state.transitions:
                targets = state.transitions['ε']
                targets_str = ",".join([f"q{t.id}" for t in targets])
                row.append(targets_str)
            else:
                row.append("-")
                
            table.append(row)
            
        return table

def regex_to_nfa(regex):
    """将正则表达式转换为NFA"""
    # 定义操作符优先级
    precedence = {'|': 1, '.': 2, '*': 3}
    operators = {'|', '.', '*', '(', ')'}
    
    def add_concat_operator(regex):
        """在需要的位置添加连接操作符('.')"""
        output = []
        for i in range(len(regex)):
            output.append(regex[i])
            if i+1 < len(regex) and regex[i] not in '(|' and regex[i+1] not in ')|*':
                output.append('.')
        return ''.join(output)
    
    def to_postfix(regex):
        """使用调度场算法(Shunting Yard)将中缀表达式转换为后缀表达式"""
        output = []
        operator_stack = []
        
        for token in regex:
            if token not in operators:  # 普通字符
                output.append(token)
            elif token == '(':  # 左括号
                operator_stack.append(token)
            elif token == ')':  # 右括号
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                operator_stack.pop()  # 弹出左括号
            else:  # 其他操作符
                while (operator_stack and operator_stack[-1] != '(' and 
                       precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
        
        # 将剩余操作符添加到输出
        while operator_stack:
            output.append(operator_stack.pop())
            
        return output
    
    def basic_nfa(symbol):
        """为单个符号创建基本NFA"""
        nfa = NFA()
        start = nfa.create_state()
        end = nfa.create_state()
        
        nfa.set_start(start)
        nfa.add_end(end)
        nfa.add_transition(start, symbol, end)
        
        return nfa
    
    def concat_nfa(nfa1, nfa2):
        """连接两个NFA"""
        result = NFA()
        
        # 创建新的起始状态
        start = result.create_state()
        result.set_start(start)
        
        # 添加ε转移到nfa1的起始状态
        nfa1_start_copy = result.create_state()
        result.add_transition(start, 'ε', nfa1_start_copy)
        
        # 复制nfa1的所有状态和转移
        state_map_nfa1 = {nfa1.start_state.id: nfa1_start_copy}
        for state in nfa1.states:
            if state.id not in state_map_nfa1:
                new_state = result.create_state()
                state_map_nfa1[state.id] = new_state
                
            for symbol, targets in state.transitions.items():
                for target in targets:
                    if target.id not in state_map_nfa1:
                        new_target = result.create_state()
                        state_map_nfa1[target.id] = new_target
                    result.add_transition(state_map_nfa1[state.id], symbol, state_map_nfa1[target.id])
        
        # 复制nfa2的所有状态和转移
        nfa2_start_copy = result.create_state()
        state_map_nfa2 = {nfa2.start_state.id: nfa2_start_copy}
        
        # 从nfa1的所有结束状态添加ε转移到nfa2的起始状态
        for end_state in nfa1.end_states:
            result.add_transition(state_map_nfa1[end_state.id], 'ε', nfa2_start_copy)
            
        for state in nfa2.states:
            if state.id not in state_map_nfa2:
                new_state = result.create_state()
                state_map_nfa2[state.id] = new_state
                
            for symbol, targets in state.transitions.items():
                for target in targets:
                    if target.id not in state_map_nfa2:
                        new_target = result.create_state()
                        state_map_nfa2[target.id] = new_target
                    result.add_transition(state_map_nfa2[state.id], symbol, state_map_nfa2[target.id])
        
        # 将nfa2的结束状态添加为result的结束状态
        for end_state in nfa2.end_states:
            result.add_end(state_map_nfa2[end_state.id])
            
        return result
    
    def union_nfa(nfa1, nfa2):
        """合并两个NFA (对应 | 操作)"""
        result = NFA()
        
        # 创建新的起始和结束状态
        start = result.create_state()
        end = result.create_state()
        result.set_start(start)
        result.add_end(end)
        
        # 复制nfa1
        nfa1_start_copy = result.create_state()
        result.add_transition(start, 'ε', nfa1_start_copy)
        
        state_map_nfa1 = {nfa1.start_state.id: nfa1_start_copy}
        for state in nfa1.states:
            if state.id not in state_map_nfa1:
                new_state = result.create_state()
                state_map_nfa1[state.id] = new_state
                
            for symbol, targets in state.transitions.items():
                for target in targets:
                    if target.id not in state_map_nfa1:
                        new_target = result.create_state()
                        state_map_nfa1[target.id] = new_target
                    result.add_transition(state_map_nfa1[state.id], symbol, state_map_nfa1[target.id])
        
        # 复制nfa2
        nfa2_start_copy = result.create_state()
        result.add_transition(start, 'ε', nfa2_start_copy)
        
        state_map_nfa2 = {nfa2.start_state.id: nfa2_start_copy}
        for state in nfa2.states:
            if state.id not in state_map_nfa2:
                new_state = result.create_state()
                state_map_nfa2[state.id] = new_state
                
            for symbol, targets in state.transitions.items():
                for target in targets:
                    if target.id not in state_map_nfa2:
                        new_target = result.create_state()
                        state_map_nfa2[target.id] = new_target
                    result.add_transition(state_map_nfa2[state.id], symbol, state_map_nfa2[target.id])
        
        # 从nfa1和nfa2的结束状态添加ε转移到新的结束状态
        for end_state in nfa1.end_states:
            result.add_transition(state_map_nfa1[end_state.id], 'ε', end)
        for end_state in nfa2.end_states:
            result.add_transition(state_map_nfa2[end_state.id], 'ε', end)
            
        return result
    
    def kleene_star_nfa(nfa):
        """克莱尼星操作 (对应 * 操作)"""
        result = NFA()
        
        # 创建新的起始和结束状态
        start = result.create_state()
        end = result.create_state()
        result.set_start(start)
        result.add_end(end)
        
        # 添加ε转移以跳过nfa (允许空字符串)
        result.add_transition(start, 'ε', end)
        
        # 复制原始nfa
        nfa_start_copy = result.create_state()
        result.add_transition(start, 'ε', nfa_start_copy)
        
        state_map = {nfa.start_state.id: nfa_start_copy}
        for state in nfa.states:
            if state.id not in state_map:
                new_state = result.create_state()
                state_map[state.id] = new_state
                
            for symbol, targets in state.transitions.items():
                for target in targets:
                    if target.id not in state_map:
                        new_target = result.create_state()
                        state_map[target.id] = new_target
                    result.add_transition(state_map[state.id], symbol, state_map[target.id])
        
        # 从nfa的结束状态添加ε转移到新的结束状态
        for end_state in nfa.end_states:
            result.add_transition(state_map[end_state.id], 'ε', end)
            # 添加回环 - 从结束状态到起始状态的ε转移
            result.add_transition(state_map[end_state.id], 'ε', nfa_start_copy)
            
        return result
    
    def build_nfa(postfix):
        """根据后缀表达式构建NFA"""
        stack = []
        
        for token in postfix:
            if token == '*':
                if not stack:
                    raise ValueError("无效的表达式: * 操作符没有操作数")
                nfa = stack.pop()
                stack.append(kleene_star_nfa(nfa))
            elif token == '.':
                if len(stack) < 2:
                    raise ValueError("无效的表达式: . 操作符需要两个操作数")
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(concat_nfa(nfa1, nfa2))
            elif token == '|':
                if len(stack) < 2:
                    raise ValueError("无效的表达式: | 操作符需要两个操作数")
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(union_nfa(nfa1, nfa2))
            else:
                stack.append(basic_nfa(token))
        
        if len(stack) != 1:
            raise ValueError("无效的表达式")
            
        return stack[0]
    
    # 处理正则表达式并构建NFA
    regex_with_concat = add_concat_operator(regex)
    postfix = to_postfix(regex_with_concat)
    return build_nfa(postfix)

def visualize_nfa(nfa):
    """使用Graphviz可视化NFA"""
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir='LR', size='8,5')
    
    # 添加一个隐藏的起始节点
    dot.node('start', style='invisible')
    
    # 添加所有状态
    for state in nfa.states:
        if state in nfa.end_states:
            # 接受状态用双圆圈
            dot.node(f'q{state.id}', shape='doublecircle', style='filled', fillcolor='lightgreen')
        else:
            # 普通状态用单圆圈
            dot.node(f'q{state.id}', shape='circle', style='filled', fillcolor='lightblue')
    
    # 添加起始箭头
    if nfa.start_state:
        dot.edge('start', f'q{nfa.start_state.id}', label='')
    
    # 添加所有转移
    for state in nfa.states:
        for symbol, targets in state.transitions.items():
            for target in targets:
                dot.edge(f'q{state.id}', f'q{target.id}', label=symbol)
    
    # 渲染为PNG并转换为PIL图像
    png_data = dot.pipe()
    buf = io.BytesIO(png_data)
    img = Image.open(buf)
    return img

def render_transition_table(table):
    """将状态转移表格式化为HTML"""
    html = "<table border='1' cellpadding='5'>"
    
    # 添加表头
    html += "<tr>"
    for header in table[0]:
        html += f"<th>{header}</th>"
    html += "</tr>"
    
    # 添加数据行
    for row in table[1:]:
        html += "<tr>"
        for i, cell in enumerate(row):
            cell_style = ""
            # 如果是接受状态，添加绿色背景
            if i == 1 and cell == "是":
                cell_style = " style='background-color: lightgreen;'"
            html += f"<td{cell_style}>{cell}</td>"
        html += "</tr>"
    
    html += "</table>"
    return html

def process_regex(regex):
    """处理正则表达式并返回结果"""
    try:
        # 将正则表达式转换为NFA
        nfa = regex_to_nfa(regex)
        
        # 获取状态转移表
        transition_table = nfa.get_transition_table()
        table_html = render_transition_table(transition_table)
        
        # 可视化NFA
        nfa_image = visualize_nfa(nfa)
        
        return nfa_image, table_html
    except Exception as e:
        return None, f"<p style='color: red'>错误: {str(e)}</p>"

# 定义Gradio界面
with gr.Blocks(title="正则表达式到NFA转换工具") as iface:
    gr.Markdown("# 正则表达式到NFA转换工具")
    gr.Markdown("输入正则表达式，查看对应的NFA及其状态转移表。")
    
    regex_input = gr.Textbox(label="正则表达式", placeholder="输入正则表达式，例如: a(b|c)*")
    process_btn = gr.Button("转换为NFA")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### NFA 可视化")
            nfa_graph = gr.Image(label="NFA 图")
        
        with gr.Column():
            gr.Markdown("### NFA 状态转移表")
            transition_table = gr.HTML()
    
    process_btn.click(
        process_regex, 
        inputs=[regex_input], 
        outputs=[nfa_graph, transition_table]
    )
    
    gr.Markdown("""
    ## 使用指南
    1. 在输入框中输入正则表达式
    2. 点击"转换为NFA"按钮
    3. 查看生成的NFA图和状态转移表
    
    ## 支持的运算符
    - `|` (或): a|b 匹配 a 或 b
    - `*` (克莱尼星号): a* 匹配零个或多个 a
    - `()` (分组): (ab)* 匹配零个或多个 ab
    
    ## 示例
    - `a` - 匹配字符 'a'
    - `ab` - 匹配字符串 "ab"
    - `a|b` - 匹配字符 'a' 或 'b'
    - `a*` - 匹配零个或多个 'a'
    - `(a|b)*` - 匹配由 'a' 和 'b' 组成的任意字符串
    - `a(b|c)*` - 匹配 'a' 后跟零个或多个 'b' 或 'c'
    """)

# 启动应用
if __name__ == "__main__":
    iface.launch()

```

# 正则表达式到NFA转换器详细解析

这个程序实现了将正则表达式转换为非确定有限自动机(NFA)的功能，并提供了直观的可视化展示。下面我将详细讲解程序的各个部分和工作原理。

## 1. 理论基础

在深入代码之前，让我们先了解几个关键概念：

- **正则表达式(Regular Expression)**: 用于描述字符串模式的形式语言
- **非确定有限自动机(NFA)**: 一种计算模型，可以有多条可能的状态转移路径
- **Thompson构造法**: 将正则表达式转换为等价NFA的标准算法

## 2. 程序结构

程序主要分为以下几个部分：

1. 状态和NFA的数据结构定义
2. 正则表达式到NFA的转换算法
3. NFA的可视化
4. 状态转移表的生成
5. Web用户界面

## 3. 核心数据结构

### State类

```python
class State:
    def __init__(self, id):
        self.id = id                   # 状态唯一标识符
        self.transitions = {}          # 存储转移: symbol -> [target_states]
        self.is_end = False            # 是否为接受状态
        self.epsilon_moves = []        # 存储ε转移可达的状态

```

`State`类表示自动机中的一个状态，包含状态ID、转移函数和是否为接受状态等信息。

### NFA类

```python
class NFA:
    def __init__(self):
        self.states = []               # 所有状态列表
        self.start_state = None        # 开始状态
        self.end_states = []           # 接受状态列表
        self.alphabet = set()          # 字母表(输入符号集)

```

`NFA`类表示一个完整的非确定有限自动机，包含所有状态、起始状态、接受状态和字母表。

## 4. 正则表达式到NFA的转换算法

### 4.1 添加连接操作符

正则表达式中的连接通常是隐式的（例如`ab`表示a后接b），但为了处理方便，程序首先显式地添加连接操作符`.`：

```python
def add_concat_operator(regex):
    output = []
    for i in range(len(regex)):
        output.append(regex[i])
        if i+1 < len(regex) and regex[i] not in '(|' and regex[i+1] not in ')|*':
            output.append('.')
    return ''.join(output)

```

例如，`ab(c|d)*` 会变成 `a.b.(c|d)*`

### 4.2 中缀到后缀转换

然后使用调度场算法(Shunting Yard Algorithm)将中缀表达式转换为后缀表达式，这样更便于使用栈来处理：

```python
def to_postfix(regex):
    # 使用调度场算法将中缀表达式转换为后缀表达式
    output = []
    operator_stack = []
    # 算法核心
    for token in regex:
        if token not in operators:  # 普通字符
            output.append(token)
        elif token == '(':  # 左括号
            operator_stack.append(token)
        elif token == ')':  # 右括号
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # 弹出左括号
        else:  # 其他操作符
            while (operator_stack and operator_stack[-1] != '(' and
                   precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0)):
                output.append(operator_stack.pop())
            operator_stack.append(token)
    # 将剩余操作符添加到输出
    while operator_stack:
        output.append(operator_stack.pop())
    return output

```

例如，`a.(b|c)*` 会转换为 `abc|*.`

### 4.3 Thompson构造法

程序使用Thompson构造法构建NFA，该算法的核心思想是为每种正则表达式操作定义一种NFA构造方法：

### 基本NFA (单个字符)

```python
def basic_nfa(symbol):
    nfa = NFA()
    start = nfa.create_state()
    end = nfa.create_state()
    nfa.set_start(start)
    nfa.add_end(end)
    nfa.add_transition(start, symbol, end)
    return nfa

```

### 连接操作 (a.b)

```python
def concat_nfa(nfa1, nfa2):
    # 连接两个NFA的代码
    # 将nfa1的接受状态与nfa2的起始状态通过ε转移连接

```

!

### 选择操作 (a|b)

```python
def union_nfa(nfa1, nfa2):
    # 合并两个NFA的代码
    # 创建新的起始和接受状态，通过ε转移连接两个NFA

```

![](https://i.imgur.com/XK8BXMQ.png)

### 克莱尼星号操作 (a*)

```python
def kleene_star_nfa(nfa):
    # 对NFA应用克莱尼星号操作的代码
    # 创建新的起始和接受状态，添加适当的ε转移

```

![](https://i.imgur.com/eFbXCFZ.png)

### 4.4 构建NFA

程序通过遍历后缀表达式，使用栈来构建最终的NFA：

```python
def build_nfa(postfix):
    stack = []
    for token in postfix:
        if token == '*':
            nfa = stack.pop()
            stack.append(kleene_star_nfa(nfa))
        elif token == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concat_nfa(nfa1, nfa2))
        elif token == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(union_nfa(nfa1, nfa2))
        else:
            stack.append(basic_nfa(token))
    return stack[0]

```

## 5. NFA可视化

程序使用Graphviz库来可视化NFA：

```python
def visualize_nfa(nfa):
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir='LR', size='8,5')
    # 添加一个隐藏的起始节点
    dot.node('start', style='invisible')
    # 添加所有状态
    for state in nfa.states:
        if state in nfa.end_states:
            # 接受状态用双圆圈
            dot.node(f'q{state.id}', shape='doublecircle', style='filled', fillcolor='lightgreen')
        else:
            # 普通状态用单圆圈
            dot.node(f'q{state.id}', shape='circle', style='filled', fillcolor='lightblue')
    # 添加起始箭头和转移
    # ...

```

NFA可视化的关键特点：

- 状态表示为圆圈
- 接受状态用双圆圈并以绿色填充
- 普通状态用蓝色填充
- 转移用带标签的箭头表示
- ε转移特别标记为"ε"

## 6. 状态转移表生成

程序生成一个状态转移表，显示每个状态对每个输入符号的转移：

```python
def get_transition_table(self):
    table = []
    # 表头行
    header = ["状态ID", "是否接受状态"]
    symbols = sorted(list(self.alphabet))
    header.extend(symbols)
    header.append('ε')
    table.append(header)
    # 添加每个状态的转移信息
    for state in self.states:
        row = [f"q{state.id}", "是" if state.is_end else "否"]
        # 添加每个符号的转移
        # ...

```

状态转移表包含以下信息：

- 状态ID
- 是否为接受状态
- 对每个输入符号的转移
- ε转移

## 7. Web用户界面

程序使用Gradio库创建了一个友好的Web界面：

```python
with gr.Blocks(title="正则表达式到NFA转换工具") as iface:
    gr.Markdown("# 正则表达式到NFA转换工具")
    gr.Markdown("输入正则表达式，查看对应的NFA及其状态转移表。")
    regex_input = gr.Textbox(label="正则表达式", placeholder="输入正则表达式，例如: a(b|c)*")
    process_btn = gr.Button("转换为NFA")
    with gr.Row():
        # 定义UI布局
        # ...

```

用户界面允许：

1. 输入正则表达式
2. 点击按钮将其转换为NFA
3. 查看可视化的NFA图形
4. 查看详细的状态转移表

## 8. 程序工作流程

当用户输入正则表达式并点击转换按钮时，完整的工作流程如下：

1. 预处理正则表达式，添加显式连接操作符
2. 将中缀表达式转换为后缀表达式
3. 使用Thompson构造法构建NFA
4. 生成NFA的可视化图形
5. 生成NFA的状态转移表
6. 在用户界面上显示结果

## 9. 示例解析

让我们看一个具体的例子，假设用户输入正则表达式 `a(b|c)*`：

1. 添加连接操作符：`a.(b|c)*`
2. 转换为后缀表达式：`abc|*.`
3. 构建NFA：
    - 创建基本NFA `a`
    - 创建基本NFA `b`
    - 创建基本NFA `c`
    - 使用选择操作合并 `b` 和 `c`，得到 `b|c`
    - 对 `b|c` 应用克莱尼星号，得到 `(b|c)*`
    - 使用连接操作连接 `a` 和 `(b|c)*`，得到最终NFA
4. 可视化NFA并生成状态转移表

## 10. 总结

这个程序通过实现Thompson构造法，展示了正则表达式到NFA的转换过程。它不仅是一个工具，也是一个很好的教学工具，帮助理解形式语言和自动机理论中的重要概念。
主要特点包括：

- 正确实现了正则表达式到NFA的转换算法
- 提供了直观的NFA可视化
- 生成了详细的状态转移表
- 提供了友好的用户界面
通过学习和使用这个工具，您可以更好地理解正则表达式和有限自动机之间的关系，以及正则表达式引擎的工作原理。