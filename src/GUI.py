import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from src.windows import Ui_MainWindow

from src.FileReader import FileReader
from src.BasicBlocksDivision import BasicBlockSplitTool
from src.BasicBlock import BasicBlock
from src.DAG import DAG


class MyGui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        self.setupUi(self)
        self.__soucecode = None
        self.__basic_block = None  # type:list[BasicBlock]
        self.fileopen.triggered.connect(self.__open_file)
        self.local_optimization_btn.clicked.connect(self.__local_optimization)
        self.DAG_optimization_btn.clicked.connect(self.__DAG_optimization)

    def __open_file(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "All Files (*);;Text Files (*.txt)")
        if ok:
            fr = FileReader(file)
            self.__soucecode = fr.get_result()

            self.__basic_block = BasicBlockSplitTool.basic_block_split(code=self.__soucecode)
            for bb in self.__basic_block:
                self.sourcecode_text.append(bb.get_code())
                self.sourcecode_text.append("\n******\n")
            self.local_optimization_btn.setEnabled(True)
            self.DAG_optimization_btn.setEnabled(True)

    def __local_optimization(self):
        self.optimization_code.clear()
        if self.__soucecode is None:
            return
        self.__basic_block = BasicBlockSplitTool.basic_block_split(code=self.__soucecode)
        for bb in self.__basic_block:
            bb.optimization()
            self.optimization_code.append(bb.get_code())
            self.optimization_code.append("\n******\n")

    def __DAG_optimization(self):
        self.optimization_code.clear()
        if self.__soucecode is None:
            return
        self.__basic_block = BasicBlockSplitTool.basic_block_split(code=self.__soucecode)
        for bb in self.__basic_block:
            code = bb.get_code()
            if len(code) == 0:
                continue
            dag = DAG(code.splitlines())
            code = dag.final_code
            self.optimization_code.append(code)
            self.optimization_code.append("\n******\n")



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = MyGui()
    mywindow.show()
    sys.exit(app.exec_())
