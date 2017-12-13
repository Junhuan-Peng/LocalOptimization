"""
主模块，用于调用自摸块
"""
import os
import sys
from PyQt5 import QtWidgets

from src.FileReader import FileReader
from src.BasicBlocksDivision import BasicBlockSplitTool
from src.BasicBlock import BasicBlock
from src.DAG import DAG
from src.GUI import MyGui

cwd = os.path.dirname(__file__)  # 获取当前文件所在目录


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = MyGui()
    mywindow.show()
    sys.exit(app.exec_())



    # file_name = 'demo.txt'
    # file_path = file_name
    # if not os.path.isabs(file_path):
    #     file_path = os.path.join(cwd, file_path)
    # fr = FileReader(file_path)
    # print('源码：')
    #
    # result = fr.get_result()
    #
    #
    # basic_blocks = None
    # basic_blocks = BasicBlockSplitTool.basic_block_split(code=result)
    # for bb in basic_blocks:
    #     print('优化前：')
    #     print(bb)
    #     print()
    #     bb.optimization()
    #     print()
    #     print('优化后：')
    #     print(bb)
    #     print('-----------')
    #
    # DAG(result)
    #
