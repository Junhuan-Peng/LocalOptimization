"""
在每一个基本块中实现：合并已知量、删除多余运算和删除无用赋值三种局部优化
"""
import re


class VarTable:
    """
    记录变量的使用情况，包括变量的声明、赋值、使用

    | 变量名 | 是否赋值 |　   值   　｜ 是否被引用 |
    |－－－－｜－－－－－｜－－－－－－｜－－－－－－|
    |       |         |          |           |
    |－－－－｜－－－－－｜－－－－－－｜－－－－－－｜
    |       |         |          |           |
    |－－－－｜－－－－－｜－－－－－－｜－－－－－－｜


        ```````````````````

    |－－－－｜－－－－－｜－－－－－－｜－－－－－－｜
    |       |         |          |           |
    |－－－－｜－－－－－｜－－－－－－｜－－－－－－｜
    |       |         |          |           |
    |－－－－｜－－－－－｜－－－－－－｜－－－－－－｜

    """
    __vars = []

    @classmethod
    def find_var(cls, var: str) -> (bool, list):
        """
        查询变量是否存在，如果存在，则返回True，同时返回该变量的记录，否咋返回False和None

        :param var: 要查询的变量
        :rtype: tuple
        :return: 状态，结果
        """
        for record in cls.__vars:
            if var.__eq__(record[0]):
                return True, record
        else:
            return False, None

    @classmethod
    def change_var_status(cls, var: str, **kwargs) -> bool:
        """
         修改变量状态

        :param var: 要修改的变量
        :keyword is_assigned: 是否已经赋值
        :keyword value: 值
        :keyword is_referenced: 是否被引用
        :return: None
        """
        for index, record in enumerate(cls.__vars):
            if var.__eq__(record[0]):
                if kwargs['is_assigned'] is not None:
                    cls.__vars[index][1] = kwargs['is_assigned']
                if kwargs['value'] is not None:
                    cls.__vars[index][2] = kwargs['value']
                if kwargs['is_referenced'] is not None:
                    cls.__vars[index][3] = kwargs['is_referenced']
            return True
        else:
            return False

    @classmethod
    def add_var(cls, var: str):
        cls.__vars.append([var, False, None, False])  # 增加变量， 未赋值、无值、未引用


class BasicBlock:
    """
    保存分割完成的基本块

    """
    __var_table = VarTable()

    __VARIABLE_DECLARATION_STATEMENT = re.compile(r'^var (.*)$')  # 变量声明正则
    __VARIABLE_ASSIGNED_STATEMENT = re.compile(r'^\s*(\w+)\s*:=\s*(\S+)\s*$')  # 变量赋值正则

    def __init__(self, code: list, start=0, end=-1):
        self.__code = [line for line in code[start:end]]  # 记录基本块的代码
        self.__index = range(start, end)  # 记录基本块代码对应的行号

    def __repr__(self):
        return '\n'.join(self.__code)

    def __statistic_variables(self):
        """
        整理变量

        :return:
        """
        for line in self.__code:
            result = re.match(self.__VARIABLE_DECLARATION_STATEMENT, line)  # 寻找变量声明
            if result is not None:
                # 如果找到变量声明，则向表中添加
                vars_ = str(result.group(1)).replace(' ', '').split(',')
                for var in vars_:
                    self.__var_table.add_var(var)
                continue

            result = re.match(self.__VARIABLE_ASSIGNED_STATEMENT, line)  # 匹配赋值
            if result is not None:
                var = result.group(1)
                value = result.group(2)
                if self.__var_table.find_var(var):
                    self.__var_table.change_var_status(var, value=value)

    def optimization(self):
        """
        基本块优化
        :return:
        """
        pass

    def __del_unreferenced_var(self):
        """
        删除无用赋值
        :return:
        """

        pass

    def __merge_knowned_member(self):
        """
        合并已知量
        :return:
        """

    def __del_redundant_operations(self):
        """
        删除多余运算
        :return:
        """
        pass
