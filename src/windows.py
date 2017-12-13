# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windows.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(771, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 371, 301))
        self.groupBox.setObjectName("groupBox")
        self.sourcecode_text = QtWidgets.QTextEdit(self.groupBox)
        self.sourcecode_text.setGeometry(QtCore.QRect(13, 20, 351, 271))
        self.sourcecode_text.setObjectName("sourcecode_text")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(390, 10, 371, 301))
        self.groupBox_2.setObjectName("groupBox_2")
        self.optimization_code = QtWidgets.QTextEdit(self.groupBox_2)
        self.optimization_code.setGeometry(QtCore.QRect(10, 20, 351, 271))
        self.optimization_code.setObjectName("optimization_code")
        self.local_optimization_btn = QtWidgets.QPushButton(self.centralwidget)
        self.local_optimization_btn.setEnabled(False)
        self.local_optimization_btn.setGeometry(QtCore.QRect(30, 320, 151, 31))
        self.local_optimization_btn.setObjectName("local_optimization_btn")
        self.DAG_optimization_btn = QtWidgets.QPushButton(self.centralwidget)
        self.DAG_optimization_btn.setEnabled(False)
        self.DAG_optimization_btn.setGeometry(QtCore.QRect(30, 360, 151, 31))
        self.DAG_optimization_btn.setObjectName("DAG_optimization_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 771, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.fileopen = QtWidgets.QAction(MainWindow)
        self.fileopen.setObjectName("fileopen")
        self.quit = QtWidgets.QAction(MainWindow)
        self.quit.setObjectName("quit")
        self.menu.addAction(self.fileopen)
        self.menu.addAction(self.quit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "源程序"))
        self.groupBox_2.setTitle(_translate("MainWindow", "优化后"))
        self.local_optimization_btn.setText(_translate("MainWindow", "局部优化"))
        self.DAG_optimization_btn.setText(_translate("MainWindow", "DAG图优化"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.fileopen.setText(_translate("MainWindow", "打开"))
        self.quit.setText(_translate("MainWindow", "退出"))

