# ir_generator.py
# 中间代码生成器 —— 以四元式(Quadruple)形式表示三地址码
# 本模块适用于编译器课程或项目的 IR 中间代码阶段

# 四元式结构： (操作符, 操作数1, 操作数2, 结果)

class Quadruple:
    """四元式结构类"""
    def __init__(self, op, arg1, arg2, result):
        self.op = op        # 操作符，如 +、*、:=、GOTO、LABEL 等
        self.arg1 = arg1    # 操作数1
        self.arg2 = arg2    # 操作数2
        self.result = result  # 结果（或跳转目标）

    def __str__(self):
        """用于输出可读形式"""
        return f"({self.op}, {self.arg1}, {self.arg2}, {self.result})"


class TempVarGenerator:
    """临时变量生成器，如 t0, t1, t2..."""
    def __init__(self):
        self.count = 0

    def new_temp(self):
        temp_name = f"t{self.count}"
        self.count += 1
        return temp_name


class LabelGenerator:
    """跳转标签生成器，如 L0, L1, L2..."""
    def __init__(self):
        self.count = 0

    def new_label(self):
        label_name = f"L{self.count}"
        self.count += 1
        return label_name


class IRGenerator:
    """中间代码生成器：管理四元式生成与打印"""
    def __init__(self):
        self.quadruples = []              # 存储所有生成的四元式
        self.temp_gen = TempVarGenerator()  # 临时变量管理
        self.label_gen = LabelGenerator()   # 标签管理

    def gen(self, op, arg1, arg2, result):
        """生成一条四元式指令"""
        quad = Quadruple(op, arg1, arg2, result)
        self.quadruples.append(quad)
        return quad

    def new_temp(self):
        """分配新的临时变量名"""
        return self.temp_gen.new_temp()

    def new_label(self):
        """分配新的跳转标签名"""
        return self.label_gen.new_label()

    def print_ir(self):
        """打印所有已生成的中间代码"""
        for i, quad in enumerate(self.quadruples):
            print(f"{i:02d}: {quad}")

    def get_ir_list(self):
        """返回四元式列表，可用于后续导出"""
        return self.quadruples

    def reset(self):
        """清空当前状态，重新生成"""
        self.__init__()
