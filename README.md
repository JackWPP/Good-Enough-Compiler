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

**第二阶段：语法分析** (开发中)
- 🔄 递归下降分析器
- 🔄 LR/LALR分析器
- 🔄 抽象语法树(AST)构建
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
│   ├── ir_generator.py         # 中间代码生成器 ✅ (新增)
│   ├── lexical/                # 词法分析模块 ✅ (已完成)
│   │   ├── __init__.py         # ✅
│   │   ├── token.py            # Token定义 ✅
│   │   ├── analyzer.py         # 词法分析器 ✅
│   │   ├── automata.py         # 自动机实现 ✅
│   │   ├── c_rules.txt         # C语言词法规则 ✅
│   │   └── pascal_rules.txt    # Pascal语言词法规则 ✅
│   ├── syntax/                 # 语法分析模块 🔄 (开发中)
│   │   └── __init__.py         # 基础结构 ✅
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
├── sample_code.c               # C语言测试文件 ✅
├── sample_code.pas             # Pascal测试文件 ✅
├── debug_lexer.py              # 词法分析器调试工具 ✅
├── main.py                     # 原版主程序 (保留)
├── lexical_analyzer.py         # 原版词法分析器 (保留)
├── nfa_dfa_converter.py        # 原版自动机转换 (保留)
└── README.md                   # 项目文档 ✅
```

### 📊 开发进度

| 模块 | 状态 | 完成度 | 说明 |
|------|------|--------|------|
| 词法分析 | ✅ 已完成 | 100% | 支持C/Pascal，包含完整的Token识别和错误处理 |
| 语法分析 | 🔄 开发中 | 10% | 基础框架已搭建，正在实现核心功能 |
| 语义分析 | 🔄 部分开始 | 5% | 模块结构已创建，等待语法分析完成 |
| 中间代码生成 | 🔄 初步实现 | 15% | 四元式结构和基础生成器已实现 |
| 目标代码生成 | 🔄 计划中 | 0% | 第五阶段开发目标 |

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

3. **体验词法分析功能**
   ```bash
   # 创建示例文件
   python main_new.py --create-samples
   
   # 分析C语言文件
   python main_new.py --analyze sample_code.c --language c
   
   # 分析Pascal文件
   python main_new.py --analyze sample_code.pas --language pascal
   
   # 启动Web界面（推荐）
   python main_new.py --gui
   ```

### 🎉 第一阶段成果展示

运行词法分析后，您将看到：

```
=== 词法分析完成 ===
✅ 成功识别 95 个Token
📊 统计信息:
   - 总行数: 24
   - 总字符数: 332
   - 处理时间: 0.023秒
   - 错误数: 0

🏷️ Token类型分布:
   IDENTIFIER    : 28 (29.5%)
   KEYWORD       : 15 (15.8%)
   DELIMITER     : 14 (14.7%)
   OPERATOR      : 12 (12.6%)
   LITERAL_INT   : 8 (8.4%)
   ...
```

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

#### Compiler

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

| 序号 | Token类型 | Token值 | 行号 | 列号 |
|------|-----------|---------|------|------|
| 1    | KEYWORD   | int     | 1    | 1    |
| 2    | IDENTIFIER| main    | 1    | 5    |
| 3    | DELIMITER | (       | 1    | 9    |

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

1. **语法分析**: 在`compiler/syntax/`目录下实现
2. **语义分析**: 在`compiler/semantic/`目录下实现
3. **代码生成**: 在`compiler/codegen/`目录下实现

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

A: 在`compiler/lexical/token.py`中的`TokenType`枚举中添加新类型，然后在词法规则文件中使用。

### Q: 如何自定义词法规则？

A: 创建新的规则文件，格式为：`正则表达式 | Token类型 | 优先级`，然后使用`load_rules_from_file()`加载。

### Q: 如何处理词法分析错误？

A: 分析器会自动收集错误信息，可通过`get_errors()`方法获取详细的错误列表。

### Q: 如何扩展到其他编程语言？

A: 参考C语言和Pascal语言的实现，创建对应的词法规则文件和分析器函数。

## 📄 许可证

本项目仅用于教学目的，请遵循相关开源协议。

## 🚀 下一步开发计划

### 第二阶段：语法分析 (开发中)

我们正在第二阶段实现以下功能：

1. **递归下降分析器**
   - 实现C语言和Pascal语言的语法规则
   - 支持表达式、语句、函数定义等语法结构
   - 提供详细的语法错误信息

2. **抽象语法树(AST)**
   - 构建完整的AST节点体系
   - 支持AST可视化
   - 提供AST遍历和操作接口

3. **语法错误恢复**
   - 实现错误恢复策略
   - 支持多个语法错误的检测和报告

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

- 🐛 **Bug修复**: 词法分析器的边界情况处理
- 📝 **文档完善**: API文档和使用示例
- 🧪 **测试增强**: 更多测试用例和边界测试
- 🎨 **UI改进**: Web界面的用户体验优化
- 🔧 **工具增强**: 调试工具和开发辅助功能
- 🚀 **语法分析**: 第二阶段核心功能开发
- 🔍 **语义分析**: 符号表和类型检查实现

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

### v0.2.0 (最新)
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

