# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '风过程自动提取.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.subplots_adjust(left=0.12, bottom=0.2, right=0.9, top=0.9, hspace=0, wspace=0)
        # self.axes = fig.add_subplot(111)

        rect = [0.15, 0.15, 0.75, 0.75]
        axprops = dict(xticks=[], yticks=[])
        ax0 = self.fig.add_axes(rect, label='ax0', **axprops)
        self.ax1 = self.fig.add_axes(rect, label='ax1', frameon=False)
        self.ax1.tick_params(labelsize=8)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.init_plot()#打开App时可以初始化图片
        # self.plot()

    def update_figure_1(self, points, result, map_img, title):



        #     markerStyle = scatterMarkers[random.randint(1,6)%len(scatterMarkers)]
        X = list(map(lambda x: x[1], points))
        Y = list(map(lambda x: x[0], points))

        self.ax1.cla()
        self.ax1.scatter(X, Y, s = 6)

        for j in range(len(X)):
            self.ax1.annotate(result[j] + 1, xy=(X[j], Y[j]), xytext=(X[j] + 5, Y[j] - 5),  size=6)

        self.ax1.set_title(title)
        self.ax1.set_ylim([800, 400])
        # self.ax1.set_xlim([1200, 1900])

        # ax0.set_xlim([0, 1500])
        # ax1.set_xticks(range(2400, 4200, 200))
        # x_ticks_ = np.arange(1200, 2100, 100)
        # ax1.set_xticklabels(x_ticks_, rotation=0, fontsize=8)
        #
        # ax0.set_ylim([0, 1000])
        # ax1.set_yticks(range(900, 1700, 100))
        # y_ticks_ = np.arange(900, 1700, 100)
        # ax1.set_yticklabels(y_ticks_, rotation=0, fontsize=8)

        self.ax1.set_xlabel('km')
        self.ax1.set_ylabel('km')


        self.draw()

    def update_figure_2(self, points, result, map_img, title):
        # self.axes.cla()
        #
        # self.axes.imshow(map_img)
        # X = list(map(lambda x: x[1], points))
        # Y = list(map(lambda x: x[0], points))
        #
        # self.axes.scatter(X, Y)
        #
        # for j in range(len(X)):
        #     self.axes.annotate(result[j] + 1, xy=(X[j], Y[j]), xytext=(X[j] + 0.01, Y[j] + 0.01))
        #
        # self.axes.set_title(title)
        #
        # self.axes.set_xlabel('km')
        # self.axes.set_ylabel('km')

        rect = [0.15, 0.15, 0.75, 0.75]
        # #     scatterMarkers = ['s', 'o', '^', '8','p', 'd', 'v', 'h', '<', ">"]
        axprops = dict(xticks=[], yticks=[])
        # ax0 = self.fig.add_axes(rect, label='ax0', **axprops)

        ax2 = self.fig.add_axes(rect, label='ax0', **axprops)
        ax2.imshow(map_img)


        # self.ax1 = self.fig.add_axes(rect, label='ax1', frameon=False)

        self.ax1.cla()
        self.ax1 = self.fig.add_axes(rect, label='ax1', frameon=False)

        #     markerStyle = scatterMarkers[random.randint(1,6)%len(scatterMarkers)]
        X = list(map(lambda x: x[1], points))
        Y = list(map(lambda x: x[0], points))

        self.ax1.scatter(X, Y)

        for j in range(len(X)):
            self.ax1.annotate(result[j] + 1, xy=(X[j], Y[j]), xytext=(X[j] + 0.01, Y[j] + 0.01))

        self.ax1.set_title(title)
        # ax1.set_ylim([800, 400])

        # ax0.set_xlim([0, 1500])
        # ax1.set_xticks(range(2400, 4200, 200))
        # x_ticks_ = np.arange(1200, 2100, 100)
        # ax1.set_xticklabels(x_ticks_, rotation=0, fontsize=8)
        #
        # ax0.set_ylim([0, 1000])
        # ax1.set_yticks(range(900, 1700, 100))
        # y_ticks_ = np.arange(900, 1700, 100)
        # ax1.set_yticklabels(y_ticks_, rotation=0, fontsize=8)

        self.ax1.set_xlabel('km')
        self.ax1.set_ylabel('km')

        self.draw()

class Ui_MainWindow_wind_process(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 40, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(550, 40, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        # 画布
        self.m = PlotCanvas(self, width=4, height=2.5)  # 实例化一个画布对象
        self.m.move(80, 100)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(590, 220, 151, 26))
        self.comboBox.setObjectName("comboBox")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setGeometry(QtCore.QRect(590, 170, 151, 24))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(590, 390, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(90, 380, 391, 151))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(580, 470, 161, 51))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "风过程自动提取"))
        self.label_2.setText(_translate("MainWindow", "参数设置"))
        self.pushButton.setText(_translate("MainWindow", "开始提取"))


class MyWindow_wind_process(QMainWindow, Ui_MainWindow_wind_process):
    def __init__(self, parent=None):
        super(MyWindow_wind_process, self).__init__(parent)
        self.setupUi(self)

import sys
if __name__ == '__main__':
    # 字体随分辨率自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyWindow_wind_process()
    myWin.show()

    sys.exit(app.exec_())