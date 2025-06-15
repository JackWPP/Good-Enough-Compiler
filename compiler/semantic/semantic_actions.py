def execute_action(prod_num, attrs, symtab):
    if prod_num == 1:  # E → E + T
        return attrs[0] + attrs[2]
    elif prod_num == 2:  # E → T
        return attrs[0]
    elif prod_num == 3:  # T → int
        return int(attrs[0])
    elif prod_num == 4:  # D → int id
        var_name = attrs[1]
        symtab.declare(var_name, "int")
        return None
    elif prod_num == 5:  # S → id = E
        var_name = attrs[0]
        if not symtab.lookup(var_name):
            raise Exception(f"变量未定义: {var_name}")
        # 可扩展：类型检查
        return None
    else:
        raise Exception(f"未知产生式编号: {prod_num}")
    ## end of execute_action
