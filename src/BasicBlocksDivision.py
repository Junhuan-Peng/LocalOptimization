"""
基本块的划分——

1.首先求出程序中各个基本块的入口语句。需满足条件(之一)如下：
    1)程序第一个语句；
    2)能由条件转移语句或无条件转移语句转移到的语句；
    3)紧跟在条件转移语句后面的语句。

2.对以上求出的每个入口语句，确定其所属的基本块。
它是由该入口语句到下一入口语句(不含该入口语句)、
或到一个转移语句(含该转移语句)、或一个停语句(含该停语句)之间的语句序列组成的。

3.凡未被纳入某一基本块中的语句，可以从程序中删除。
"""

import re


class BasicBlock:
    """
    记录分割完成的基本块
    """

    def __init__(self, code: str, start=0, end=-1):
        self.__code = []
        for line in code[start:end]:
            self.__code.append(line)
        self.__index = range(start, end)

    def __repr__(self):
        return '\n'.join(self.__code)


class BasicBlockSplitTool:
    """
    划分工具
    """

    @staticmethod
    def __find_entry(code: str) -> list:
        """
        寻找源码的入口
        :param code: 源码
        :return: list of entry
        """
        entry = []
        entry.append(0)  # 程序第一句是入口
        gotopattern = re.compile(r'\s*GOTO (\d+)')
        lines = code.splitlines()
        for i, line in enumerate(lines):
            result = re.match(pattern=gotopattern, string=line)  # 匹配转移语句
            if result is not None:
                gotolinenum = int(result.group(1))
                entry.append(gotolinenum - 1)
                entry.append(i + 1)
        entry.sort()
        return entry

    @staticmethod
    def basic_block_split(code: str) -> list:
        """
        划分基本块
        :param code: 源码
        :return: list of basic block
        """
        entrylist = BasicBlockSplitTool.__find_entry(code)
        print(entrylist)
        lines = code.splitlines()
        basic_blocks = []
        last_index = 0
        for index in entrylist[1:]:
            print(index)
            basic_blocks.append(BasicBlock(lines, last_index, index))
            last_index = index
        return basic_blocks


if __name__ == '__main__':
    test_str = '''var a,b,c
a := 4
b := 5
if a > 3:
    a := a + 2
if b < 6:
    b := b + 1
    GOTO 4
if a+b ==20:
    GOTO 6
if a>4:
    GOTO 7
'''
bbs = BasicBlockSplitTool.basic_block_split(test_str)

for i in bbs:
    print(i)
    print('**************')
