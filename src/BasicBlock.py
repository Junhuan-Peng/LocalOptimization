"""
在每一个基本块中实现：合并已知量、删除多余运算和删除无用赋值三种局部优化
"""
import re


class VarTable:
    """
    记录变量的使用情况，包括变量名、值、引用
    | 变量 | 值 | 引用行数列表 | 出现的行数列表 |
    """

    def __init__(self):
        self.__vars = []

    def find_var(self, var: str) -> (bool, list):
        """
        查询变量是否存在，如果存在，则返回True，同时返回该变量的记录，否咋返回False和None

        :param var: 要查询的变量
        :rtype: tuple
        :return: 状态，结果
        """
        for record in self.__vars:
            if var.__eq__(record[0]):
                return True, record
        else:
            return False, None

    def change_var_status(self, var: str, linenumber: int, **kwargs) :
        """
         修改变量状态

        :param var: 要修改的变量
        :param linenumber: 变量出现的索引
        :keyword value: 值
        :keyword referenced_line_number: 被引用的行数
        :return: None
        """

        keys = kwargs.keys()
        for index, record in enumerate(self.__vars):
            if var.__eq__(record[0]):
                # record == self.__vars
                record[3].append(linenumber)

                if 'value' in keys:
                    record[1] = kwargs['value']
                if 'referenced_line_number' in keys:
                    if record[2] is None:  # 如果为空则新建一个列表
                        record[2] = []
                        record[2].append(kwargs['referenced_line_number'])
                    else:
                        record[2].append(kwargs['referenced_line_number'])
                print('{var}:{record}'.format(var=self.__vars[index][0], record=self.__vars[index]))

    def add_var(self, var: str):
        self.__vars.append([var, None, None, []])  # 增加变量， 无值， 无引用，出现的行号

    def get_vars(self):
        return self.__vars

    def get_var_s_reference_list(self, var: str):
        ret, record = self.find_var(var)
        return record[2]

    def get_var_s_value(self, var: str):
        ret, record = self.find_var(var)
        return record[1]

    def get_var_s_line_numbers(self, var: str):
        ret, record = self.find_var(var)
        return record[3]

    def del_var(self, var: str):
        for index, record in enumerate(self.__vars):
            if var.__eq__(record[0]):
                self.__vars.pop(index)


class BasicBlock:
    """
    保存分割完成的基本块

    """
    __VARIABLE_ASSIGNED_STATEMENT = re.compile(r'^\s*(\w+)\s*:=\s*(\S+)\s*$')  # 变量赋值正则
    __VARIABLE_FIND = re.compile(r'\b[a-zA-Z]+\b')

    def __init__(self, code: list, start=0, end=-1):
        self.__code = [line for line in code[start:end]]  # 记录基本块的代码
        self.__index = range(start, end)  # 记录基本块代码对应的行号
        self.__var_table = VarTable()  # 记录基本块中的变量使用情况

    def __repr__(self):
        return '\n'.join(self.__code)

    def __statistic_variables(self):
        """
        整理变量，将出现过的变量放入变量表中，同时删除一些重复赋值的语句

        :return:
        """
        for index, line in enumerate(self.__code):
            result = re.match(self.__VARIABLE_ASSIGNED_STATEMENT, line)  # 匹配赋值
            if result is not None:
                var = result.group(1)  # 被赋值的变量
                value = result.group(2)  # 值（注意！其中可能有其它变量，eg:a = b + 2）
                # ---------------对被赋值对象的处理---------------
                ret, _ = self.__var_table.find_var(var)
                if not ret:  # 如果变量还未出现在变量表中
                    self.__var_table.add_var(var)  # 先将变量放入变量表中
                    self.__var_table.change_var_status(var, index, value=value)  # 再向表中添加变量的值
                else:  # 如果变量已经在变量表中出现过
                    reference_list = self.__var_table.get_var_s_reference_list(var)
                    if reference_list is not None:  # 被引用过， 直接更新值
                        self.__var_table.change_var_status(var, index, value=value)
                    else:  # 没有被引用过， 则认为之前的赋值全为无用赋值
                        line_number_list = self.__var_table.get_var_s_line_numbers(var)
                        for line_number in line_number_list:
                            self.__code[line_number] = ' '  # 将对应的源码删去， 视为删除
                        self.__var_table.del_var(var)  # 从表中删除变量
                        self.__var_table.add_var(var)  # 重新向表中添加该变量
                        self.__var_table.change_var_status(var, index, value=value)

                # ----------------对值的处理-------------------
                # 先从中找到变量，如果没有则pass
                # 如果有， 先看变量表中有没有，如果有，则修改其的引用列表；否则向变量表中添加新变量
                vars_in_value = re.findall(self.__VARIABLE_FIND, value)
                for var in vars_in_value:
                    ret, _ = self.__var_table.find_var(var)
                    if ret:  # 如果变量在表中出现过
                        self.__var_table.change_var_status(var, index, referenced_line_number=index)
                    else:  # 如果变量没有在表中出现过
                        self.__var_table.add_var(var)
                        self.__var_table.change_var_status(var, index, referenced_line_number=index)

    def optimization(self):
        """
        基本块优化

        :return:
        """
        self.__statistic_variables()
        self.__del_redundant_operations()
        self.__merge_knowned_member()
        self.__del_unreferenced_var()
        self.print_var_table()

    def __del_unreferenced_var(self):
        """
        删除无用赋值

        :return:
        """
        var_table = self.__var_table.get_vars()
        for var_record in var_table:  # 遍历变量表，找到未引用的变量，从源码中删除，同时从表中删除
            if var_record[2] is None:  # 引用列表为空

                for line_number in var_record[3]:  # 删除源码
                    self.__code[line_number] = ' '

                value = var_record[1]
                line_number = var_record[3][0]  # 如果为无用赋值，则最多出现一次（多余的已在整理变量时删除）
                vars_in_value = re.findall(self.__VARIABLE_FIND, value)
                for var in vars_in_value:
                    ret, record = self.__var_table.find_var(var)
                    record[3].pop(record[3].index(line_number))  # 从被引用的值所出现的行号中删除该行
                self.__var_table.del_var(var_record[0])  # 从表中删除变量

    def __merge_knowned_member(self):
        """
        合并已知量

        :return:
        """
        pass

    def __del_redundant_operations(self):
        """
        删除多余运算

        :return:
        """
        # 在变量表中找到相同value，

        pass

    def print_var_table(self):
        for record in self.__var_table.get_vars():
            print(record)


if __name__ == '__main__':
    pass
