"""
主模块，用于调用自摸块
"""
import os
from src.FileReader import FileReader
from src.BasicBlocksDivision import BasicBlockSplitTool
from src.BasicBlock import BasicBlock

cwd = os.path.dirname(__file__)  # 获取当前文件所在目录


if __name__ == '__main__':
    file_name = input('输入文件名')
    file_path = file_name
    if not os.path.isabs(file_path):
        file_path = os.path.join(cwd, file_path)
    fr = FileReader(file_path)
    print('源码：')

    result = fr.get_result()
    code = ''
    for s in result:
        code += s

    basic_blocks = None
    if code is not None:
        basic_blocks = BasicBlockSplitTool.basic_block_split(code=code)
    for bb in basic_blocks:
        print('优化前：')
        print(bb)
        print()
        bb.optimization()
        print()
        print('优化后：')
        print(bb)
        print('-----------')
