"""
主模块，用于调用子摸块
"""
import os
import sys
from PyQt5 import QtWidgets

from src.GUI import MyGui


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = MyGui()
    mywindow.show()
    sys.exit(app.exec_())

