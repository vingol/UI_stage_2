#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import pickle
from UI_main_win import *
from PyQt5.QtWidgets import QApplication, QMainWindow

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["DEBUSSY"] = "1"

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    # 字体随分辨率自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()

    sys.exit(app.exec_())