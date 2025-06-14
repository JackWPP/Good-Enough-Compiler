# Good-Enough-Compiler

一个教学用的编译器实现，支持C语言和Pascal语言。

## 🎯 开发状态

### ✅ 已完成阶段

**第一阶段：词法分析** (已完成)

- ✅ 完整的词法分析器实现
- ✅ 支持C语言和Pascal语言
- ✅ 正则表达式引擎（Thompson构造法、子集构造法）
- ✅ 自动机转换（NFA → DFA → 最小化DFA）
- ✅ 详细的Token统计和错误处理
- ✅ Web界面和命令行工具
- ✅ HTML/JSON报告生成

### 🚧 开发路线图

**第二阶段：语法分析** (基本完成)

- ✅ LR(0)/SLR(1)/LR(1)分析器
- ✅ 抽象语法树(AST)构建和可视化
- ✅ First/Follow集计算
- ✅ 分析表构建和冲突检测
- ✅ 语法分析步骤追踪
- 🔄 语法错误恢复

**第三阶段：语义分析** (部分开始)

- 🔄 符号表管理
- 🔄 类型检查
- 🔄 作用域分析
- 🔄 语义错误检测

**第四阶段：中间代码生成** (初步实现)

- ✅ 四元式(Quadruple)中间代码结构
- ✅ 临时变量和标签生成器
- 🔄 三地址码生成
- 🔄 控制流图构建
- 🔄 代码优化

**第五阶段：目标代码生成** (计划中)

- 🔄 汇编代码生成
- 🔄 寄存器分配
- 🔄 指令选择

**增强功能** (长期计划)

- 🔄 更多编程语言支持
- 🔄 IDE集成
- 🔄 调试器支持
- 🔄 性能分析工具

## 🚀 当前功能特性

### 📝 词法分析 (已完成)

- **多语言支持**: 完整支持C语言和Pascal语言词法分析
- **Token识别**: 识别关键字、标识符、字面量、运算符、分隔符等
- **错误处理**: 详细的词法错误检测和报告
- **统计信息**: 完整的Token统计和分析报告

### 🔍 语法分析 (基本完成)

- **LR分析器**: 支持LR(0)、SLR(1)、LR(1)分析方法
- **AST构建**: 完整的抽象语法树构建和可视化
- **First/Follow集**: 自动计算文法的First和Follow集
- **分析表构建**: 自动生成Action表和Goto表
- **冲突检测**: SLR(1)和LR(1)冲突自动检测
- **步骤追踪**: 详细的语法分析步骤记录
- **可视化**: 自动机状态图和AST树形图生成

### 🔧 正则表达式引擎 (已完成)

- **Thompson构造法**: 正则表达式到NFA的转换
- **子集构造法**: NFA到DFA的转换
- **DFA最小化**: 优化自动机状态数量
- **可视化支持**: 自动机图形化展示

### 🖥️ 用户界面 (已完成)

- **Web界面**: 基于Gradio的现代化Web界面
- **命令行工具**: 支持批处理和脚本化使用
- **多种输出格式**: HTML报告、JSON数据、控制台输出

### 🏗️ 架构设计 (已完成)

- **模块化设计**: 清晰的模块结构，便于扩展
- **API接口**: 统一的编译器API
- **配置系统**: 灵活的编译器配置选项
- **扩展性**: 为后续开发阶段预留接口

## 📦 项目结构

```
Good-Enough-Compiler/
├── compiler/                    # 编译器核心模块
│   ├── __init__.py             # 主模块初始化 ✅
│   ├── api.py                  # 统一API接口 ✅
│   ├── integrated_analyzer.py  # 集成分析器 ✅ (新增)
│   ├── integrated_app.py       # 集成Web应用 ✅ (新增)
│   ├── ir_generator.py         # 中间代码生成器 ✅
│   ├── lexical/                # 词法分析模块 ✅ (已完成)
│   │   ├── __init__.py         # ✅
│   │   ├── token.py            # Token定义 ✅
│   │   ├── analyzer.py         # 词法分析器 ✅
│   │   ├── automata.py         # 自动机实现 ✅
│   │   ├── c_rules.txt         # C语言词法规则 ✅
│   │   └── pascal_rules.txt    # Pascal语言词法规则 ✅
│   ├── syntax/                 # 语法分析模块 ✅ (基本完成)
│   │   ├── __init__.py         # 基础结构 ✅
│   │   ├── app.py              # 语法分析Web应用 ✅
│   │   ├── ast_builder.py      # AST构建器 ✅
│   │   ├── ast_nodes.py        # AST节点定义 ✅
│   │   ├── first_follow.py     # First/Follow集计算 ✅
│   │   ├── lr0_dfa.py          # LR(0)自动机 ✅
│   │   ├── lr1_dfa.py          # LR(1)自动机 ✅
│   │   ├── parser_engine.py    # 语法分析引擎 ✅
│   │   └── slr1_check.py       # SLR(1)冲突检测 ✅
│   ├── semantic/               # 语义分析模块 🔄 (部分开始)
│   │   └── __init__.py         # 基础结构 ✅
│   ├── codegen/                # 代码生成模块 🔄 (第五阶段)
│   │   └── __init__.py         # 基础结构 ✅
│   └── utils/                  # 工具模块 ✅
│       ├── __init__.py         # ✅
│       ├── visualization.py    # 可视化工具 ✅
│       ├── file_utils.py       # 文件处理 ✅
│       └── formatters.py       # 格式化工具 ✅
├── main_new.py                 # 主程序 ✅
├── integrated_app.py           # 集成编译器Web应用 ✅ (新增)
├── sample_code.c               # C语言测试文件 ✅
├── sample_code.pas             # Pascal测试文件 ✅
├── debug_analyze.py            # 集成分析调试工具 ✅ (新增)
├── debug_lexer.py              # 词法分析器调试工具 ✅
├── debug_parser.py             # 语法分析器调试工具 ✅ (新增)
├── test_slr1_check.py          # SLR(1)冲突检测测试 ✅ (新增)
├── main.py                     # 原版主程序 (保留)
├── main_new.py                 # 新版主程序 ✅
├── lexical_analyzer.py         # 原版词法分析器 (保留)
├── nfa_dfa_converter.py        # 原版自动机转换 (保留)
└── README.md                   # 项目文档 ✅
```

### 📊 开发进度

| 模块         | 状态        | 完成度 | 说明                                        |
| ------------ | ----------- | ------ | ------------------------------------------- |
| 词法分析     | ✅ 已完成   | 100%   | 支持C/Pascal，包含完整的Token识别和错误处理 |
| 语法分析     | ✅ 基本完成 | 85%    | LR分析器、AST构建、可视化已完成             |
| 语义分析     | 🔄 部分开始 | 5%     | 模块结构已创建，等待语法分析完成            |
| 中间代码生成 | 🔄 初步实现 | 15%    | 四元式结构和基础生成器已实现                |
| 目标代码生成 | 🔄 计划中   | 0%     | 第五阶段开发目标                            |

## 🛠️ 安装和使用

### 环境要求

- Python 3.7+
- 依赖包：gradio（可选，用于Web界面）

### 快速开始

1. **克隆项目**

   ```bash
   git clone <repository-url>
   cd Good-Enough-Compiler
   ```
2. **安装依赖**（可选）

   ```bash
   pip install gradio
   ```
3. **体验完整编译功能**

   ```bash
   # 启动集成Web界面（推荐）
   python integrated_app.py

   # 或使用原版词法分析
   python main_new.py --gui

   # 调试语法分析
   python debug_analyze.py

   # 测试SLR(1)冲突检测
   python test_slr1_check.py
   ```

### 🎉 集成编译器成果展示

运行集成分析后，您将看到：

**词法分析结果：**

```
=== 词法分析完成 ===
✅ 成功识别 95 个Token
📊 统计信息:
   - 总行数: 24
   - 总字符数: 332
   - 处理时间: 0.023秒
   - 错误数: 0
```

**语法分析结果：**

```
=== 语法分析完成 ===
✅ 文法类型: SLR(1)
📊 分析信息:
   - 状态数: 12
   - 产生式数: 8
   - 分析步骤: 15
   - AST节点数: 7
   - 分析结果: accept
```

**可视化输出：**

- 🌳 AST树形结构图
- 📊 LR自动机状态转换图
- 📋 Action/Goto分析表
- 📝 详细分析步骤

### 命令行使用

```bash
# 显示帮助
python main_new.py --help

# 启动Web界面
python main_new.py --gui

# 分析文件
python main_new.py --analyze <文件路径> --language <c|pascal>

# 详细输出
python main_new.py --analyze <文件路径> --verbose

# 指定输出文件
python main_new.py --analyze <文件路径> --output <输出路径>

# 测试正则表达式转换
python main_new.py --test-regex "a|b*"

# 创建示例文件
python main_new.py --create-samples

# 显示版本信息
python main_new.py --version
```

## 📚 API 文档

### 核心类

#### IntegratedAnalyzer

集成分析器类，提供完整的词法和语法分析功能。

```python
from compiler.integrated_analyzer import create_integrated_analyzer

# 创建集成分析器
analyzer = create_integrated_analyzer('c')  # 或 'pascal'

# 设置自定义文法
grammar = "E → E + T | T\nT → T * F | F\nF → ( E ) | id"
analyzer.set_grammar(grammar)

# 分析源代码和句子
result = analyzer.analyze_code(source_code, sentence)

# 访问分析结果
print(f"Token数量: {len(result.tokens)}")
print(f"是否为SLR(1): {result.is_slr1}")
print(f"AST根节点: {result.ast_root}")
```

#### Compiler (原版)

主编译器类，提供完整的编译功能。

```python
from compiler import Compiler, CompilerConfig

# 创建编译器
compiler = Compiler()

# 编译文件
result = compiler.compile_file('sample.c', language='c')

# 编译源代码
code = '#include <stdio.h>\nint main() { return 0; }'
result = compiler.compile_source(code, language='c')
```

#### CompilerConfig

编译器配置类。

```python
config = CompilerConfig(
    language='c',           # 编程语言
    verbose=True,          # 详细输出
    output_tokens=True,    # 输出Token
    output_html=True,      # 生成HTML报告
    output_json=False      # 生成JSON报告
)
```

#### CompilationResult

编译结果类，包含所有分析信息。

```python
# 访问结果
print(f"Token数量: {len(result.tokens)}")
print(f"错误数量: {len(result.errors)}")
print(f"处理时间: {result.processing_time}秒")
print(f"统计信息: {result.statistics}")
```

### 语法分析API

```python
from compiler.syntax.parser_engine import parse_sentence
from compiler.syntax.first_follow import process_first_follow
from compiler.syntax.slr1_check import check_slr1

# 语法分析
grammar = "E → E + T | T\nT → T * F | F\nF → ( E ) | id"
sentence = "id + id * id"
steps, ast_root = parse_sentence(grammar, sentence, method="SLR(1)")

# First/Follow集计算
grammar_obj = process_first_follow(grammar)
print(f"First集: {grammar_obj.first}")
print(f"Follow集: {grammar_obj.follow}")

# SLR(1)冲突检测
is_slr1, conflicts = check_slr1(grammar_obj)
print(f"是否为SLR(1): {is_slr1}")
```

### 便捷函数

```python
from compiler import compile_file, compile_source, analyze_tokens

# 编译文件
result = compile_file('sample.c', language='c')

# 编译源代码
result = compile_source(code, language='c')

# 仅进行词法分析
tokens = analyze_tokens(code, language='c')
```

### 词法分析器

```python
from compiler.lexical import create_c_analyzer, create_pascal_analyzer

# 创建C语言分析器
analyzer = create_c_analyzer()

# 分析代码
tokens = analyzer.analyze(code)
errors = analyzer.get_errors()
statistics = analyzer.get_statistics()
```

### AST操作

```python
from compiler.syntax.ast_nodes import ASTNode, ASTVisualizer
from compiler.syntax.ast_builder import ASTBuilder

# 创建AST节点
node = ASTNode('expression', 'id')
node.add_child(ASTNode('operator', '+'))
node.add_child(ASTNode('expression', 'id'))

# AST可视化
visualizer = ASTVisualizer()
svg_content = visualizer.to_svg(node)
html_content = visualizer.to_html(node)

# AST构建器
builder = ASTBuilder()
ast_root = builder.build_from_parse_tree(parse_tree)
```

### 自动机转换

```python
from compiler.lexical import RegexToNFA, NFAToDFA, DFAMinimizer

# 正则表达式转NFA
regex_converter = RegexToNFA()
nfa = regex_converter.convert('a|b*')

# NFA转DFA
nfa_to_dfa = NFAToDFA()
dfa = nfa_to_dfa.convert(nfa)

# DFA最小化
minimizer = DFAMinimizer()
minimized_dfa = minimizer.minimize(dfa)
```

### 可视化工具

```python
from compiler.utils import visualize_nfa, visualize_dfa, create_token_table_html

# 可视化自动机
visualize_nfa(nfa, 'nfa.png')
visualize_dfa(dfa, 'dfa.png')

# 生成Token表格
html_table = create_token_table_html(tokens)
```

## 🎯 支持的语言特性

### C语言

- **关键字**: `int`, `float`, `char`, `if`, `else`, `while`, `for`, `return`, `include`, 等
- **数据类型**: 整数、浮点数、字符、字符串
- **运算符**: 算术、关系、逻辑、位运算、赋值运算符
- **分隔符**: 括号、分号、逗号等
- **注释**: 单行注释(`//`)和多行注释(`/* */`)
- **预处理**: `#include`, `#define`等

### Pascal语言

- **关键字**: `program`, `begin`, `end`, `var`, `if`, `then`, `else`, `while`, `for`, 等
- **数据类型**: `integer`, `real`, `char`, `string`, `boolean`
- **运算符**: 算术、关系、逻辑运算符
- **分隔符**: 括号、分号、逗号等
- **注释**: 大括号注释(`{ }`)和圆括号注释(`(* *)`)

## 📊 输出格式

### Token表格

| 序号 | Token类型  | Token值 | 行号 | 列号 |
| ---- | ---------- | ------- | ---- | ---- |
| 1    | KEYWORD    | int     | 1    | 1    |
| 2    | IDENTIFIER | main    | 1    | 5    |
| 3    | DELIMITER  | (       | 1    | 9    |

### 统计信息

```
=== 词法分析统计 ===
总Token数: 156
总行数: 23
总字符数: 445
错误数: 0
处理时间: 0.023秒

Token类型分布:
  IDENTIFIER    : 45 (28.8%)
  KEYWORD       : 23 (14.7%)
  DELIMITER     : 21 (13.5%)
  OPERATOR      : 18 (11.5%)
  LITERAL_INT   : 12 (7.7%)
```

### HTML报告

生成包含以下内容的HTML报告：

- 源代码语法高亮
- Token表格
- 统计图表
- 错误信息
- 自动机可视化

## 🔧 扩展开发

### 添加新语言支持

1. **创建词法规则文件**

   ```
   # 在 compiler/lexical/ 目录下创建 <language>_rules.txt
   # 格式: 正则表达式 | Token类型 | 优先级
   ```
2. **扩展TokenType枚举**

   ```python
   # 在 compiler/lexical/token.py 中添加新的Token类型
   ```
3. **创建分析器函数**

   ```python
   def create_<language>_analyzer():
       analyzer = LexicalAnalyzer()
       analyzer.load_rules_from_file('<language>_rules.txt')
       return analyzer
   ```

### 添加新的分析阶段

1. **语法分析**: 在 `compiler/syntax/`目录下实现
2. **语义分析**: 在 `compiler/semantic/`目录下实现
3. **代码生成**: 在 `compiler/codegen/`目录下实现

### 自定义可视化

```python
from compiler.utils import create_custom_chart

# 创建自定义统计图表
chart = create_custom_chart(data, chart_type='bar')
```

## 🧪 测试示例

### C语言示例

```c
#include <stdio.h>

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int num = 5;
    printf("%d! = %d\n", num, factorial(num));
    return 0;
}
```

### Pascal语言示例

```pascal
program FactorialExample;

function Factorial(n: integer): integer;
begin
    if n <= 1 then
        Factorial := 1
    else
        Factorial := n * Factorial(n - 1);
end;

var
    num: integer;
begin
    num := 5;
    writeln(num, '! = ', Factorial(num));
end.
```

## 🐛 常见问题

### Q: 如何添加新的Token类型？

A: 在 `compiler/lexical/token.py`中的 `TokenType`枚举中添加新类型，然后在词法规则文件中使用。

### Q: 如何自定义词法规则？

A: 创建新的规则文件，格式为：`正则表达式 | Token类型 | 优先级`，然后使用 `load_rules_from_file()`加载。

### Q: 如何处理词法分析错误？

A: 分析器会自动收集错误信息，可通过 `get_errors()`方法获取详细的错误列表。

### Q: 如何扩展到其他编程语言？

A: 参考C语言和Pascal语言的实现，创建对应的词法规则文件和分析器函数。

## 📄 许可证

本项目仅用于教学目的，请遵循相关开源协议。

## 🚀 下一步开发计划

### 第二阶段：语法分析 (基本完成)

我们已在第二阶段实现了以下功能：

1. **LR分析器系列** ✅

   - LR(0)自动机构建和状态转换
   - SLR(1)分析表生成和冲突检测
   - LR(1)分析器实现
   - 支持自定义文法输入和分析
2. **抽象语法树(AST)** ✅

   - 完整的AST节点体系
   - AST可视化（SVG和HTML格式）
   - AST遍历和操作接口
   - 从分析步骤自动构建AST
3. **分析工具和可视化** ✅

   - First/Follow集自动计算
   - Action/Goto表生成和显示
   - 分析步骤详细追踪
   - 自动机状态图可视化
4. **集成开发环境** ✅

   - 统一的Web界面
   - 词法和语法分析集成
   - 调试工具和测试脚本
   - 错误检测和报告

### 如何参与开发

如果您想参与下一阶段的开发，可以：

1. **Fork项目并创建分支**

   ```bash
   git checkout -b feature/syntax-analysis
   ```
2. **选择开发任务**

   - 语法规则定义
   - AST节点设计
   - 分析器实现
   - 测试用例编写
3. **遵循代码规范**

   - 保持与现有代码风格一致
   - 添加完整的文档和注释
   - 编写单元测试

## 🤝 贡献指南

### 贡献者

感谢以下贡献者对项目的支持：

- **JackWPP** - 项目创始人，词法分析模块核心开发
- **allencat0712** - 语义分析模块贡献
- **Bcccccc03** - 中间代码生成器实现

### 当前贡献重点

- 🔍 **语义分析**: 符号表管理和类型检查系统
- 🏗️ **中间代码优化**: 三地址码生成和优化
- 🎯 **目标代码生成**: 汇编代码生成器
- 🐛 **Bug修复**: 语法分析器的边界情况处理
- 📝 **文档完善**: 语法分析API文档和使用示例
- 🧪 **测试增强**: 更多语法分析测试用例
- 🎨 **UI改进**: 集成界面的用户体验优化
- 🔧 **工具增强**: 更多调试和开发辅助功能

### 提交规范

```bash
# 功能开发
git commit -m "feat: 添加新的Token类型支持"

# Bug修复
git commit -m "fix: 修复字符串字面量解析错误"

# 文档更新
git commit -m "docs: 更新API使用示例"

# 测试相关
git commit -m "test: 添加Pascal语言测试用例"
```

## 📈 最近更新

### v0.3.0 (最新)

- ✅ 完整的语法分析功能实现
- ✅ LR(0)/SLR(1)/LR(1)分析器
- ✅ 抽象语法树(AST)构建和可视化
- ✅ First/Follow集自动计算
- ✅ 分析表构建和冲突检测
- ✅ 集成分析器和Web界面
- ✅ 语法分析步骤追踪和调试工具
- 🔧 修复SLR(1)冲突检测问题
- 🔧 优化AST生成和显示

### v0.2.0

- ✅ 新增中间代码生成器模块 (ir_generator.py)
- ✅ 实现四元式(Quadruple)中间代码结构
- ✅ 添加临时变量和标签生成器
- 🔄 开始语义分析模块开发
- 🔄 语法分析模块框架搭建

### v0.1.0

- ✅ 完整的词法分析功能
- ✅ 支持C语言和Pascal语言
- ✅ Web界面和命令行工具
- ✅ 正则表达式到自动机转换

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📋 **提交Issue**: 报告Bug或提出功能建议
- 🔀 **Pull Request**: 贡献代码或文档改进
- 💬 **讨论区**: 参与技术讨论和经验分享

---

**Good-Enough-Compiler** - 让编译原理学习变得更简单！

🎯 **第一阶段已完成** | 🚧 **第二阶段开发中** | 📚 **持续学习，持续改进**
