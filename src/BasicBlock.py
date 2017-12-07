"""
在每一个基本块中实现：合并已知量、删除多余运算和删除无用赋值三种局部优化
"""
import re
import sympy

class VarTable:
    """
    记录变量的使用情况，包括变量名、值、引用
    | 变量 | 值 | 引用行数列表 | 出现的行数列表 | 最新赋值行 |
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

    def change_var_status(self, var: str, linenumber: int, **kwargs):
        """
         修改变量状态

        :param var: 要修改的变量
        :param linenumber: 变量出现的索引
        :keyword value: 值
        :keyword referenced_line_number: 被引用的行数
        :keyword lastest_assign_line: 最新被赋值的行
        :return: None
        """

        keys = kwargs.keys()
        for index, record in enumerate(self.__vars):
            if var.__eq__(record[0]):
                # record == self.__vars
                if linenumber not in record[3]:
                    record[3].append(linenumber)

                if 'value' in keys:
                    record[1] = kwargs['value']
                if 'referenced_line_number' in keys:
                    if record[2] is None:  # 如果为空则新建一个列表
                        record[2] = []
                        record[2].append(kwargs['referenced_line_number'])
                    else:
                        record[2].append(kwargs['referenced_line_number'])
                if 'lastest_assign_line' in keys:
                    record[4] = kwargs['lastest_assign_line']
                # print('{var}:{record}'.format(var=self.__vars[index][0], record=self.__vars[index]))

    def add_var(self, var: str):
        self.__vars.append([var, None, None, [], 1000])  # 增加变量， 无值， 无引用，出现的行号, 最新赋值行

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

    def clear(self):
        self.__vars = []

class BasicBlock:
    """
    保存分割完成的基本块

    """
    __VARIABLE_ASSIGNED_STATEMENT = re.compile(r'^\s*(\w+)\s*:=\s*(.+)$')  # 变量赋值正则
    __VARIABLE_FIND = re.compile(r'\b[a-zA-Z]\w*\b')  # 匹配出现的变量名
    __NUMBER_VALUE = re.compile(r'^\s*\d+\s*$')  # 匹配出现的数值

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

        self.__var_table.clear()

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

                self.__del_redundant_operations(var, value, index)  # 判断当前变量是否需要删除多余运算
                self.__var_table.change_var_status(var, index, lastest_assign_line=index)
                # ----------------对值的处理-------------------
                # 先从中找到变量，如果没有则pass
                # 如果有， 先看变量表中有没有，如果有，则修改其的引用列表；否则向变量表中添加新变量
                result = re.match(self.__VARIABLE_ASSIGNED_STATEMENT, line)  # 匹配赋值
                value = result.group(2)

                vars_in_value = re.findall(self.__VARIABLE_FIND, value)
                for var in vars_in_value:
                    ret, _ = self.__var_table.find_var(var)
                    if ret:  # 如果变量在表中出现过
                        self.__var_table.change_var_status(var, index, referenced_line_number=index)
                    else:  # 如果变量没有在表中出现过
                        self.__var_table.add_var(var)
                        self.__var_table.change_var_status(var, index, referenced_line_number=index)
            for code in self.__code:
                print(code)
            self.print_var_table()
            print('%%%%%%%%%%%%%%%%%%%%%%%%')

    def optimization(self):
        """
        基本块优化

        :return:
        """
        self.__statistic_variables()
        self.__merge_knowned_member()
        self.__del_unreferenced_var()
        self.__statistic_variables()
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
        合并已知量,对可计算量进行提前计算： a := 3*7 + b  ==>  a := 21 + b  ,如果b已知，则可做进一步值的化简

        :return:
        """

        print('合并已知量：')

        var_record = {}  # 记录变量赋值情况 [变量名|值]，值的范围限制在数字
        #  如果找到已赋值的变量，则直接替换，如果变量为没有赋值或所赋值不可直接计算，则转换为sympy.Symbol对象以支持运算
        for index, line in enumerate(self.__code):

            print('------- 当前语句：', line)

            result = re.match(self.__VARIABLE_ASSIGNED_STATEMENT, line)  # 匹配赋值语句
            if result is not None:
                var = result.group(1)
                value = result.group(2)

                print('等号左边：', var)
                print('等号右边：', value)

                number = re.match(self.__NUMBER_VALUE, value)  # 匹配变量所赋的值是否是数值
                if number is not None:  # 如果是

                    print(value, '是数值\n\n')

                    var_record[var] = value  # 直接在变量记录中更新值
                else:  # 如果变量所赋值是表达式
                    if re.match(r'^\s*\w+\s*$',value):  # 如果右侧只有一个变量，例如  a := b  则不需要替换

                        print(value,'只是一个简单的变量，不需要替换')

                        continue
                    vars_in_value = re.findall(self.__VARIABLE_FIND, value)  # 提取所有表达式中的变量
                    vars_in_value = list(set(vars_in_value))  # 去重

                    print('找到的变量：', vars_in_value)

                    for var_in_value in vars_in_value:

                        print('当前待处理的变量：', var_in_value)

                        if var_in_value in var_record.keys():  # 如果该变量已经存在表中
                            temp_value = var_record[var_in_value]  # 取出值

                            print(var_in_value, '已经存在记录中，其值为：', temp_value)

                            if re.match(self.__NUMBER_VALUE, temp_value) is not None:  # 如果变量是数值

                                print(temp_value, '是数值')
                                print('执行', var_in_value + '=' + temp_value)

                                exec(var_in_value + '=' + temp_value)
                            else:  # 如果变量不是数值，则一定是表达式,将其转换为Symbol对象

                                print(temp_value, '是表达式')
                                print('执行', var_in_value + '=' + 'sympy.Symbol(\'' + var_in_value + '\')')

                                exec(var_in_value + '=' + 'sympy.Symbol(\'' + var_in_value + '\')')
                        else:  # 如果该变量不存在于表中，那么直接将其转换为Symbol对象

                            print(var_in_value, '不在记录中')
                            print('执行', var_in_value + '=' + 'sympy.Symbol(\'' + var_in_value + '\')')

                            exec(var_in_value + '=' + 'sympy.Symbol(\'' + var_in_value + '\')')

                    print('原表达式为：', value)

                    value = eval(value)  # 计算表达式

                    print('计算后的表达式为:', value)

                    var_record[var] = str(value)  # 更新记录中的值
                    value = var + ' := '+str(value)  # 更新源码
                    self.__code[index] = value

    def __del_redundant_operations(self, var: str, value: str, index: int):
        """
        删除多余运算

        :param var: 测试变量（等号左侧）
        :param value: 测试值（等号右侧）
        :param index: 行号
        :return:
        """
        #  删除多余运算应满足两个条件
        #  一，表达式的值应该相同
        #  二，如果要让"C1 = 4*I;C2 = 4*I" ==>  "C1 = 4*I;C2 = C1"，应满足
        #  lastest_assign_line(I) < lastest_assign_line(C1) < lastest_assign_line(C2)

        vars_in_value = re.findall(self.__VARIABLE_FIND, value)
        if len(vars_in_value) == 0:  # 如果值中不存在变量则返回
            return
        for record in self.__var_table.get_vars():
            if record[0].__eq__(var):  # 不和自己比较
                continue
            if record[1] is None:  # 存在一些变量未赋值,不具有比较性
                continue
            if record[1].replace(' ', '').__eq__(value.replace(' ', '')):  # 找到相同值
                temp_var = record[0]
                print('{temp_var} : {record}'.format(temp_var=temp_var, record=record))
                for var_in_left in vars_in_value:
                    ret, temp_record = self.__var_table.find_var(var_in_left)
                    if temp_record[1] is None:  # 存在一些变量未赋值,则认为满足
                        continue
                    if temp_record[4] < record[4] < index:  # 该变量满足
                        continue
                    else:
                        break  # 有一个变量不满足，则不满足整体
                else:  # 如果所有变量都满足了，则可以替换 “var := value  ==>  var:=temp_var”
                    self.__code[index] = var + " := " + temp_var
                    self.__var_table.change_var_status(var, index, value=temp_var)
                    self.__var_table.change_var_status(temp_var, index, referenced_line_number=index)

    def print_var_table(self):
        for record in self.__var_table.get_vars():
            print(record)


if __name__ == '__main__':
    pass
