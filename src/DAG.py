"""
DAG 算法的实现
需要的数据结构：
1.图结构——记录DAG图，可以使用不严格树形结构
2.变量记录表
3.节点存放表
"""

import re


class DAGNode:
    """
    DAG 图节点，记录父节点:set、子节点:set、值:None、变量列表:set、操作符:None
    """

    def __init__(self) -> None:
        self.__parent_node = set()  # 记录父节点
        self.__child_nodes = []  # 记录子节点列表
        self.__value = None  # 记录值
        self.__var = set()  # 记录节点表示的变量
        self.__op = None  # 记录子节点间的操作符

    @property
    def parent(self):
        return self.__parent_node

    def add_parent(self, value):
        self.__parent_node.add(value)

    def add_children(self, children):
        self.__child_nodes.append(children)

    @property
    def child(self):
        return self.__child_nodes

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def vars(self):
        return self.__var

    def remove_var(self, var):
        if var in self.vars:
            self.__var.remove(var)

    def add_var(self, var):
        self.__var.add(var)

    def get_op(self):
        return self.__op

    def set_op(self, value):
        self.__op = value

    def __repr__(self) -> str:
        parents = list(self.__parent_node)
        parents = [str(i) for i in parents]
        parents = ' '.join(parents)

        children = list(self.__child_nodes)
        children = [str(i) for i in children]
        children = ' '.join(children)

        vars_ = list(self.__var)
        vars_ = ' '.join(vars_)

        result = 'var:' + vars_ + '\n'
        result += 'parent:' + parents + '\n'
        result += 'children:' + children + '\n'
        if self.__value is not None:
            result += 'value:' + str(self.__value) + '\n'
        return result


class DAG:
    __code = []

    __SIMPLE_ASSIGNED = re.compile(r'^\s*(\w+)\s*:=\s*(\w+\.?\w*)\s*$')  # 形如 A:=B
    __SIMPLE_CALC = re.compile(r"^\s*(\w+)\s*:=\s*(\w+\.?\w*)\s*([*\-+/])\s*(\w+\.?\w*)\s*$")  # 形如 A := B + C

    __NODE_TYPE_NUMBER = 0
    __NODE_TYPE_NUKNOWN_NUMBER = 1
    __NODE_TYPE_VARIABLE = 2

    __VARIABLE_TABLE = {}  # type: {[],bool}

    def __init__(self, code: list) -> None:
        super().__init__()

        self.__node_list = []  # type: list[DAGNode]
        self.__final_code = []

        self.__code = code
        print(self.__code)

        self.__create()
        self.__restore(self.__node_list[-1])
        for index, node in enumerate(self.__node_list):
            print(index)
            print(node)
        print(self.final_code)

    def __create(self):
        for line in self.__code:
            result = re.match(self.__SIMPLE_ASSIGNED, line)
            if result is not None:  # 简单赋值语句
                var = result.group(1)  # 一定是变量
                value = result.group(2)  # 可能是变量、数值、未知数

                print(line, ' 是简单赋值，var = {var},value={value}'.format(var=var, value=value))

                (type_, index) = self.__judge_type(value)
                self.__node_list[index].add_var(var)

                self.__delete_no_use_var(var, index)


                continue
            result = re.match(self.__SIMPLE_CALC, line)
            if result is not None:  # 复杂赋值
                var = result.group(1)
                values = [result.group(2), result.group(4)]
                op = result.group(3)

                self.__change_var_reference(values[0])
                self.__change_var_reference(values[1])

                print(line, ' 是复杂赋值，var = {var},op_num_1={v1}, op={op}, op_num_2={v2}' \
                      .format(var=var, v1=values[0], v2=values[1], op=op))

                (type_1, index_1) = self.__judge_type(values[0])
                (type_2, index_2) = self.__judge_type(values[1])

                if {type_1, type_2} == {self.__NODE_TYPE_NUMBER, self.__NODE_TYPE_NUMBER}:
                    # 两个数值

                    new_value = eval(values[0] + op + values[1])
                    (type_, index) = self.__judge_type(str(new_value))
                    self.__node_list[index].add_var(var)
                    self.__delete_no_use_var(var, index)


                elif {type_1, type_2} == {self.__NODE_TYPE_NUMBER, self.__NODE_TYPE_VARIABLE}:
                    # 一个数值一个变量（变量可能取值）
                    number_index, variable_index = -1, -1
                    if type_1 == self.__NODE_TYPE_VARIABLE:
                        number_index, variable_index = index_2, index_1
                    else:
                        number_index, variable_index = index_1, index_2

                    temp_value = self.__node_list[variable_index].value
                    (type_temp_value, index_temp_value) = self.__judge_type(temp_value)

                    if type_temp_value == self.__NODE_TYPE_NUMBER:  # 变量存储的是一个数值
                        final_value = eval(temp_value + op + self.__node_list[number_index].value)
                        (type_, index) = self.__judge_type(str(final_value))
                        self.__node_list[index].add_var(var)
                        self.__delete_no_use_var(var, index)

                    else:  # 变量存储的是一个未知数
                        temp_node = DAGNode()
                        temp_node.add_var(var)
                        temp_node.add_children(index_1)
                        temp_node.add_children(index_2)
                        temp_node.set_op(op)

                        index = self.__find_same(temp_node)
                        if index >= 0:
                            self.__node_list[index].add_var(var)
                            self.__delete_no_use_var(var, index)


                        else:
                            self.__node_list.append(temp_node)
                            temp_node_index = self.__node_list.index(temp_node)
                            self.__delete_no_use_var(var, temp_node_index)

                            self.__node_list[index_1].add_parent(temp_node_index)
                            self.__node_list[index_2].add_parent(temp_node_index)
                else:  # 存在一个未知数
                    temp_node = DAGNode()
                    temp_node.add_var(var)
                    temp_node.add_children(index_1)
                    temp_node.add_children(index_2)
                    temp_node.set_op(op)
                    index = self.__find_same(temp_node)
                    if index >= 0:
                        self.__node_list[index].add_var(var)
                        self.__delete_no_use_var(var, index)
                    else:
                        self.__node_list.append(temp_node)
                        temp_node_index = self.__node_list.index(temp_node)
                        self.__delete_no_use_var(var, temp_node_index)

                        self.__node_list[index_1].add_parent(temp_node_index)
                        self.__node_list[index_2].add_parent(temp_node_index)

    def __judge_type(self, var: str):
        """
        判断参数所属类型（数值/未知数/变量）

        :param var: 带判断的变量
        :return: (参数类型， 参数索引)
        :rtype: tuple
        """
        result = []
        if re.match(r'^\s*(\d+.?\d*)\s*$', var):
            # 数值
            result.append(self.__NODE_TYPE_NUMBER)
            for index, node in enumerate(self.__node_list):
                if node.value == var:
                    result.append(index)
                    break
            else:
                temp_node = DAGNode()
                temp_node.value = var
                self.__node_list.append(temp_node)
                result.append(self.__node_list.index(temp_node))
            return tuple(result)

        if re.match(r'^\s*([a-zA-Z]\w*)\s*$', var):
            # 不是数值，那么一定是一个变量或者是一个未知数
            for index, node in enumerate(self.__node_list):
                if var in node.vars:
                    #  如果存在于某个节点的变量列表里，那么是变量
                    result.append(self.__NODE_TYPE_VARIABLE)
                    result.append(index)
                    return result
            # 不是变量， 那么一定是未知数
            for index, node in enumerate(self.__node_list):
                if node.value == var:  # 未知数已存在
                    result.append(self.__NODE_TYPE_NUKNOWN_NUMBER)
                    result.append(index)
                    break
            else:
                temp_node = DAGNode()
                temp_node.value = var
                self.__node_list.append(temp_node)
                result.append(self.__NODE_TYPE_NUKNOWN_NUMBER)
                result.append(self.__node_list.index(temp_node))
            return tuple(result)

    def __find_same(self, mynode: DAGNode) -> int:
        mynode.child.sort()
        for index, node in enumerate(self.__node_list):
            node.child.sort()
            if node.child == mynode.child and node.get_op() == mynode.get_op():
                print(node.child, ' = ', mynode.child)
                print(node.get_op(), ' = ', mynode.get_op())
                return index
        return -1

    def __restore(self, node: DAGNode):
        if len(node.vars) == 0:
            return

        templist = list(node.vars)
        templist.sort()
        if len(templist) != 0 and node.value is not None:  # var := 数值  |  var := 未知数
            for var in templist:
                self.__final_code.append(var + ' := ' + node.value)
            return

        if node.get_op() is not None and node.child != []:
            for i in node.child:
                self.__restore(self.__node_list[i])
            values = []
            if self.__node_list[node.child[0]].value is not None:
                values.append(self.__node_list[node.child[0]].value)
            else:
                values.append(list(self.__node_list[node.child[0]].vars)[0])
            if self.__node_list[node.child[1]].value is not None:
                values.append(self.__node_list[node.child[1]].value)
            else:
                values.append(list(self.__node_list[node.child[1]].vars)[0])
            self.__final_code.append(templist[0] + ' := ' + values[0] + node.get_op() + values[1])
            for var in templist[1:]:
                self.__final_code.append(var + ' := ' + templist[0])
            return

    def __delete_no_use_var(self, var: str, index: int):
        if var in self.__VARIABLE_TABLE.keys():  # 如果变量出现过
            if self.__VARIABLE_TABLE[var][1] is False:  # 上次赋值后还没有被引用过
                self.__node_list[self.__VARIABLE_TABLE[var][0][-1]].remove_var(var)
                if len(self.__VARIABLE_TABLE[var][0]) == 0:
                    self.__VARIABLE_TABLE[var] = [[index], False]
            else:  # 被引用过， 则直接添加新的赋值行， 同时修改引用标志量
                self.__VARIABLE_TABLE[var][1] = False
                self.__VARIABLE_TABLE[var][0].append(index)
        else:  # 还没有出现过
            self.__VARIABLE_TABLE[var] = [[index], False]

    def __change_var_reference(self, var: str):
        if var in self.__VARIABLE_TABLE.keys():
            self.__VARIABLE_TABLE[var][1] = True

    @property
    def final_code(self):
        return '\n'.join(self.__final_code)


if __name__ == '__main__':
    pass
