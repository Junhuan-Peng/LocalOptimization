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


class BasicBlock:
    """
    记录分割完成的基本块
    """
    __code = None  # 记录源码
    __index = []  # 记录源码所在行号

    def __init__(self, code: str, start=0, end=len(str)):
        self.__code = code[start:end]
        self.__index = range(start, end)


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
        pass

    @staticmethod
    def basic_block_split(code: str) -> list:
        """
        划分基本块
        :param code: 源码
        :return: list of basic block
        """
        entrylist = BasicBlockSplitTool.__find_entry(str)

