# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '风过程自动提取.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import pickle
import datetime
import pandas as pd
import numpy as np
from math import isnan
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from sklearn import preprocessing
import matplotlib

plt.rcParams["font.family"]="SimHei"
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=6, height=3, dpi=75):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.2, bottom=0.25, right=0.9, top=0.9, hspace=0, wspace=0)
        self.axes = fig.add_subplot(111)
        # self.ax_twin = self.axes.twinx()
        self.axes.axis('off')

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.init_plot()

        # self.axess.set_xticks([])
        # self.axes.set_yticks([])

    def init_plot(self):
        self.axes.cla()
        df = pd.read_excel(r'main_win_data/station_info_jilin.xlsx', sheet_name='光伏', index_col=0)
        df.columns = ['CAP', 'Lat', 'Lon', 'NWP_ID']

        Location = df.iloc[:, 1:3].values
        def num_2_ID(x):
            if x<11: return x+501
            else: return x+502
        ## 原始图像
        import matplotlib.pyplot as plt
        matplotlib.use('Agg')
        # fig, ax = plt.subplots(figsize=(10, 5))
        self.axes.scatter(Location[:, 0], Location[:, 1], label='光伏电站', s=8)
        # self.axes.scatter(Location[:, 0] + 0.04, Location[:, 1] + 0.03, color=[], marker='o', edgecolors='#1f77b4',
        #            s=300)  # 把 corlor 设置为空，通过edgecolors来控制颜色
        for i in range(Location.shape[0]):

            # 设定文字位置
            text_loc_x = 0.0355
            text_loc_y = 0.0225

            if i == 15:
                text_loc_y = -0.0225
            if i == 7:
                text_loc_y = -0.1
            if i == 9:
                text_loc_x = 0
                text_loc_y = -0.25
            if i == 11:
                text_loc_x = -0.25
                text_loc_y = -0.0225
            if i == 4:
                text_loc_x = 0.0335
                text_loc_y = 0.4
            if i == 10:
                text_loc_x = 0.0335
                text_loc_y = -0.2
            if i == 5:
                text_loc_x = 0.0335
                text_loc_y = 0

            self.axes.text(Location[i, 0] + text_loc_x, Location[i, 1] + text_loc_y, str(num_2_ID(i)), fontsize=8,
                    color='#1f77b4')
        self.axes.set(xlabel='经度(' + '$^{o}$' + ')', ylabel='纬度(' + '$^{o}$' + ')')# plt.grid()
        # plt.show()
        self.axes.legend(loc='upper right')
        self.axes.tick_params(labelsize=8)
        self.axes.set_xlim([41.5, 46.5])
        self.axes.set_ylim([122,130])
        self.draw()
        # plt.savefig('Location.svg')

    def Plot_2(self, Location, Other_Farms, Farm_for_target, Final_Farm):

        self.axes.cla()
        ## 画完后的图像
        import matplotlib.pyplot as plt
        # fig, self.axes = plt.subplots(figsize=(10, 5))

        def ID_2_num(x):
            if x<513: return x-501
            else: return x-502
        def num_2_ID(x):
            if x<11: return x+501
            else: return x+502

        Farm_for_target = ID_2_num(Farm_for_target)

        Final_Farm = ID_2_num(Final_Farm)

        self.axes.scatter(Location[Other_Farms, 0], Location[Other_Farms, 1], label='其他光伏电站', s=8)
        # self.axes.scatter(Location[Other_Farms, 0] + 0.04, Location[Other_Farms, 1] + 0.03, color=[], marker='o',
        #            edgecolors='#1f77b4', s=300)  # 把 corlor 设置为空，通过edgecolors来控制颜色
        for i in range(len(Other_Farms)):
            text_loc_x = 0.0355
            text_loc_y = 0.0225

            if Other_Farms[i] == 15:
                text_loc_y = -0.0225
            if Other_Farms[i] == 7:
                text_loc_y = -0.1
            if Other_Farms[i] == 9:
                text_loc_x = 0
                text_loc_y = -0.25
            if Other_Farms[i] == 11:
                text_loc_x = -0.25
                text_loc_y = -0.0225
            if Other_Farms[i] == 4:
                text_loc_x = 0.0335
                text_loc_y = 0.4
            if Other_Farms[i] == 10:
                text_loc_x = 0.0335
                text_loc_y = -0.2
            if Other_Farms[i] == 5:
                text_loc_x = 0.0335
                text_loc_y = 0
            self.axes.text(Location[Other_Farms[i], 0] + text_loc_x, Location[Other_Farms[i], 1] + text_loc_y, str(num_2_ID(Other_Farms[i])), fontsize=8,  color='#1f77b4')

        self.axes.scatter(Location[Farm_for_target, 0], Location[Farm_for_target, 1], label='目标光伏电站', s=8)
        # ax.scatter(Location[Farm_for_target,0] + 0.04, Location[Farm_for_target,1] + 0.03 , color=[], marker='o', edgecolors='#ff7f0e', s=300)  # 把 corlor 设置为空，通过edgecolors来控制颜色
        # 设定文字位置
        text_loc_x = 0.0355
        text_loc_y = 0.0225

        if Farm_for_target == 15:
            text_loc_y = -0.0225
        if Farm_for_target == 7:
            text_loc_y = -0.1
        if Farm_for_target == 9:
            text_loc_x = 0
            text_loc_y = -0.25
        if Farm_for_target == 11:
            text_loc_x = -0.25
            text_loc_y = -0.0225
        if Farm_for_target == 4:
            text_loc_x = 0.0335
            text_loc_y = 0.4
        if Farm_for_target == 10:
            text_loc_x = 0.0335
            text_loc_y = -0.2
        if Farm_for_target == 5:
            text_loc_x = 0.0335
            text_loc_y = 0
        self.axes.text(Location[Farm_for_target, 0] + text_loc_x, Location[Farm_for_target, 1] + text_loc_y,
                str(num_2_ID(Farm_for_target)), fontsize=8, color='#ff7f0e')

        self.axes.scatter(Location[Final_Farm, 0], Location[Final_Farm, 1], label='关联光伏电站', s=8)
        # ax.scatter(Location[Final_Farm,0] + 0.04, Location[Final_Farm,1] + 0.03 , color=[], marker='o', edgecolors='#2ca02c', s=300)  # 把 corlor 设置为空，通过edgecolors来控制颜色

        text_loc_x = 0.0355
        text_loc_y = 0.0225

        if Final_Farm == 15:
            text_loc_y = -0.0225
        if Final_Farm == 7:
            text_loc_y = -0.1
        if Final_Farm == 9:
            text_loc_x = 0
            text_loc_y = -0.25
        if Final_Farm == 11:
            text_loc_x = -0.25
            text_loc_y = -0.0225
        if Final_Farm == 4:
            text_loc_x = 0.0335
            text_loc_y = 0.4
        if Final_Farm == 10:
            text_loc_x = 0.0335
            text_loc_y = -0.2
        if Final_Farm == 5:
            text_loc_x = 0.0335
            text_loc_y = 0
        self.axes.text(Location[Final_Farm, 0] + text_loc_x, Location[Final_Farm, 1] + text_loc_y, str(num_2_ID(Final_Farm)),
                fontsize=8, color='#2ca02c')
        self.axes.set(xlabel='经度(' + '$^{o}$' + ')', ylabel='纬度(' + '$^{o}$' + ')')# plt.grid()
        # plt.show()
        self.axes.legend(loc='upper right')
        self.axes.set_xlim([41.5, 46.5])
        self.axes.set_ylim([122, 130])
        # plt.savefig('Processed.svg')
        self.draw()

class Ui_MainWindow_solar_corr(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(604, 420, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(604, 480, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton2.setFont(font)
        self.pushButton2.setObjectName("pushButton")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(32, 350, 450, 120))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # 画布
        self.m = PlotCanvas(self, width=6, height=3)  # 实例化一个画布对象
        self.m.move(30, 100)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(480, 180, 320, 100))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(25)
        self.gridLayout.setObjectName("gridLayout")
        self.label_time = QtWidgets.QLabel(self.widget)
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setObjectName("label_time")
        self.gridLayout.addWidget(self.label_time, 0, 0, 1, 1)

        # self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.widget)
        # self.dateTimeEdit.setObjectName("dateTimeEdit")
        # self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 6, 19), QtCore.QTime(12, 0, 0)))
        # self.gridLayout.addWidget(self.dateTimeEdit, 0, 1, 1, 1)

        self.comboBox_starttime = QtWidgets.QComboBox(self.widget)
        self.comboBox_starttime.setObjectName("comboBox_starttime")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.setItemText(0, "")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.addItem("")
        self.comboBox_starttime.setCurrentIndex(40)
        self.comboBox_starttime.currentIndexChanged[str].connect(
            self.get_starttime)  # 条目发生改变，发射信号，传递条目内容
        self.gridLayout.addWidget(self.comboBox_starttime, 0, 1, 1, 1)

        self.label_station = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_station.setFont(font)
        self.label_station.setAlignment(QtCore.Qt.AlignCenter)
        self.label_station.setObjectName("label_station")
        self.gridLayout.addWidget(self.label_station, 1, 0, 1, 1)

        self.comboBox_station = QtWidgets.QComboBox(self.widget)
        self.comboBox_station.setObjectName("comboBox")
        self.comboBox_station.addItem("")
        self.comboBox_station.setItemText(0, "")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")

        self.gridLayout.addWidget(self.comboBox_station, 1, 1, 1, 1)


        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(145, 35, 560, 30))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(255)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)

        self.pushButton.clicked.connect(self.show_solar_Correlation)
        self.pushButton2.clicked.connect(self.Solar_Correlation_EVA)


        self.comboBox_station.currentIndexChanged[str].connect(
            self.get_station_name)  # 条目发生改变，发射信号，传递条目内容

        # set_text
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(50, 480, 400, 100))
        self.widget2.setObjectName("widget")
        self.gridLayout2 = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout2.setContentsMargins(10, 10, 10, 10)
        self.gridLayout2.setHorizontalSpacing(10)
        self.gridLayout2.setVerticalSpacing(10)

        self.gridLayout2.setObjectName("gridLayout")
        self.label_error1 = QtWidgets.QLabel(self.widget2)
        self.label_error1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_error1.setObjectName("label_time")
        self.gridLayout2.addWidget(self.label_error1, 0, 0, 1, 1)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")

        self.gridLayout2.addWidget(self.textBrowser, 0, 1, 1, 1)
        self.label_error2 = QtWidgets.QLabel(self.widget2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_error2.setFont(font)
        self.label_error2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_error2.setObjectName("label_station")
        self.gridLayout2.addWidget(self.label_error2, 1, 0, 1, 1)

        self.textBrowser2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser2.setObjectName("textBrowser")

        self.gridLayout2.addWidget(self.textBrowser2, 1, 1, 1, 1)

        # self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        # self.textBrowser.setGeometry(QtCore.QRect(500, 550, 120, 31))
        # self.textBrowser.setObjectName("textBrowser")
        #
        # self.textBrowser2 = QtWidgets.QTextBrowser(self.centralwidget)
        # self.textBrowser2.setGeometry(QtCore.QRect(650, 550, 120, 31))
        # self.textBrowser2.setObjectName("textBrowser")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "光伏关联模式分析"))
        self.label_2.setText(_translate("MainWindow", "参数设置"))
        self.pushButton.setText(_translate("MainWindow", "开始计算"))
        self.pushButton2.setText(_translate("MainWindow", "误差分析"))

        self.comboBox_station.setItemText(1, _translate("MainWindow", "光伏501"))
        self.comboBox_station.setItemText(2, _translate("MainWindow", "光伏509"))
        self.comboBox_station.setItemText(3, _translate("MainWindow", "光伏516"))

        self.comboBox_starttime.setItemText(1, _translate("MainWindow", "2018-6-19 06:30:00"))
        self.comboBox_starttime.setItemText(2, _translate("MainWindow", "2018-6-19 06:34:17"))
        self.comboBox_starttime.setItemText(3, _translate("MainWindow", "2018-6-19 06:38:34"))
        self.comboBox_starttime.setItemText(4, _translate("MainWindow", "2018-6-19 06:45:00"))
        self.comboBox_starttime.setItemText(5, _translate("MainWindow", "2018-6-19 06:49:17"))
        self.comboBox_starttime.setItemText(6, _translate("MainWindow", "2018-6-19 06:53:34"))
        self.comboBox_starttime.setItemText(7, _translate("MainWindow", "2018-6-19 07:15:00"))
        self.comboBox_starttime.setItemText(8, _translate("MainWindow", "2018-6-19 07:19:17"))
        self.comboBox_starttime.setItemText(9, _translate("MainWindow", "2018-6-19 07:23:34"))
        self.comboBox_starttime.setItemText(10, _translate("MainWindow", "2018-6-19 07:30:00"))
        self.comboBox_starttime.setItemText(11, _translate("MainWindow", "2018-6-19 07:34:17"))
        self.comboBox_starttime.setItemText(12, _translate("MainWindow", "2018-6-19 07:38:34"))
        self.comboBox_starttime.setItemText(13, _translate("MainWindow", "2018-6-19 08:30:00"))
        self.comboBox_starttime.setItemText(14, _translate("MainWindow", "2018-6-19 08:34:17"))
        self.comboBox_starttime.setItemText(15, _translate("MainWindow", "2018-6-19 08:38:34"))
        self.comboBox_starttime.setItemText(16, _translate("MainWindow", "2018-6-19 08:45:00"))
        self.comboBox_starttime.setItemText(17, _translate("MainWindow", "2018-6-19 08:49:17"))
        self.comboBox_starttime.setItemText(18, _translate("MainWindow", "2018-6-19 08:53:34"))
        self.comboBox_starttime.setItemText(19, _translate("MainWindow", "2018-6-19 09:15:00"))
        self.comboBox_starttime.setItemText(20, _translate("MainWindow", "2018-6-19 09:19:17"))
        self.comboBox_starttime.setItemText(21, _translate("MainWindow", "2018-6-19 09:23:34"))
        self.comboBox_starttime.setItemText(22, _translate("MainWindow", "2018-6-19 09:30:00"))
        self.comboBox_starttime.setItemText(23, _translate("MainWindow", "2018-6-19 09:34:17"))
        self.comboBox_starttime.setItemText(24, _translate("MainWindow", "2018-6-19 09:38:34"))
        self.comboBox_starttime.setItemText(25, _translate("MainWindow", "2018-6-19 09:45:00"))
        self.comboBox_starttime.setItemText(26, _translate("MainWindow", "2018-6-19 09:49:17"))
        self.comboBox_starttime.setItemText(27, _translate("MainWindow", "2018-6-19 09:53:34"))
        self.comboBox_starttime.setItemText(28, _translate("MainWindow", "2018-6-19 10:15:00"))
        self.comboBox_starttime.setItemText(29, _translate("MainWindow", "2018-6-19 10:19:17"))
        self.comboBox_starttime.setItemText(30, _translate("MainWindow", "2018-6-19 10:23:34"))
        self.comboBox_starttime.setItemText(31, _translate("MainWindow", "2018-6-19 10:30:00"))
        self.comboBox_starttime.setItemText(32, _translate("MainWindow", "2018-6-19 10:34:17"))
        self.comboBox_starttime.setItemText(33, _translate("MainWindow", "2018-6-19 10:38:34"))
        self.comboBox_starttime.setItemText(34, _translate("MainWindow", "2018-6-19 11:30:00"))
        self.comboBox_starttime.setItemText(35, _translate("MainWindow", "2018-6-19 11:34:17"))
        self.comboBox_starttime.setItemText(36, _translate("MainWindow", "2018-6-19 11:38:34"))
        self.comboBox_starttime.setItemText(37, _translate("MainWindow", "2018-6-19 11:45:00"))
        self.comboBox_starttime.setItemText(38, _translate("MainWindow", "2018-6-19 11:49:17"))
        self.comboBox_starttime.setItemText(39, _translate("MainWindow", "2018-6-19 11:53:34"))
        self.comboBox_starttime.setItemText(40, _translate("MainWindow", "2018-6-19 12:15:00"))
        self.comboBox_starttime.setItemText(41, _translate("MainWindow", "2018-6-19 12:19:17"))
        self.comboBox_starttime.setItemText(42, _translate("MainWindow", "2018-6-19 12:23:34"))
        self.comboBox_starttime.setItemText(43, _translate("MainWindow", "2018-6-19 12:30:00"))
        self.comboBox_starttime.setItemText(44, _translate("MainWindow", "2018-6-19 12:34:17"))
        self.comboBox_starttime.setItemText(45, _translate("MainWindow", "2018-6-19 12:38:34"))
        self.comboBox_starttime.setItemText(46, _translate("MainWindow", "2018-6-19 12:45:00"))
        self.comboBox_starttime.setItemText(47, _translate("MainWindow", "2018-6-19 12:49:17"))
        self.comboBox_starttime.setItemText(48, _translate("MainWindow", "2018-6-19 12:53:34"))
        self.comboBox_starttime.setItemText(49, _translate("MainWindow", "2018-6-19 13:15:00"))
        self.comboBox_starttime.setItemText(50, _translate("MainWindow", "2018-6-19 13:19:17"))
        self.comboBox_starttime.setItemText(51, _translate("MainWindow", "2018-6-19 13:23:34"))
        self.comboBox_starttime.setItemText(52, _translate("MainWindow", "2018-6-19 13:30:00"))
        self.comboBox_starttime.setItemText(53, _translate("MainWindow", "2018-6-19 13:34:17"))
        self.comboBox_starttime.setItemText(54, _translate("MainWindow", "2018-6-19 13:38:34"))
        self.comboBox_starttime.setItemText(55, _translate("MainWindow", "2018-6-19 14:30:00"))
        self.comboBox_starttime.setItemText(56, _translate("MainWindow", "2018-6-19 14:34:17"))
        self.comboBox_starttime.setItemText(57, _translate("MainWindow", "2018-6-19 14:38:34"))
        self.comboBox_starttime.setItemText(58, _translate("MainWindow", "2018-6-19 14:45:00"))
        self.comboBox_starttime.setItemText(59, _translate("MainWindow", "2018-6-19 14:49:17"))
        self.comboBox_starttime.setItemText(60, _translate("MainWindow", "2018-6-19 14:53:34"))
        self.comboBox_starttime.setItemText(61, _translate("MainWindow", "2018-6-19 15:15:00"))
        self.comboBox_starttime.setItemText(62, _translate("MainWindow", "2018-6-19 15:19:17"))
        self.comboBox_starttime.setItemText(63, _translate("MainWindow", "2018-6-19 15:23:34"))
        self.comboBox_starttime.setItemText(64, _translate("MainWindow", "2018-6-19 15:30:00"))
        self.comboBox_starttime.setItemText(65, _translate("MainWindow", "2018-6-19 15:34:17"))
        self.comboBox_starttime.setItemText(66, _translate("MainWindow", "2018-6-19 15:38:34"))
        self.comboBox_starttime.setItemText(67, _translate("MainWindow", "2018-6-19 15:45:00"))
        self.comboBox_starttime.setItemText(68, _translate("MainWindow", "2018-6-19 15:49:17"))
        self.comboBox_starttime.setItemText(69, _translate("MainWindow", "2018-6-19 15:53:34"))
        self.comboBox_starttime.setItemText(70, _translate("MainWindow", "2018-6-19 16:15:00"))
        self.comboBox_starttime.setItemText(71, _translate("MainWindow", "2018-6-19 16:19:17"))
        self.comboBox_starttime.setItemText(72, _translate("MainWindow", "2018-6-19 16:23:34"))
        self.comboBox_starttime.setItemText(73, _translate("MainWindow", "2018-6-19 16:30:00"))
        self.comboBox_starttime.setItemText(74, _translate("MainWindow", "2018-6-19 16:34:17"))
        self.comboBox_starttime.setItemText(75, _translate("MainWindow", "2018-6-19 16:38:34"))
        self.comboBox_starttime.setItemText(76, _translate("MainWindow", "2018-6-19 17:30:00"))
        self.comboBox_starttime.setItemText(77, _translate("MainWindow", "2018-6-19 17:34:17"))
        self.comboBox_starttime.setItemText(78, _translate("MainWindow", "2018-6-19 17:38:34"))
        self.comboBox_starttime.setItemText(79, _translate("MainWindow", "2018-6-19 17:45:00"))
        self.comboBox_starttime.setItemText(80, _translate("MainWindow", "2018-6-19 17:49:17"))
        self.comboBox_starttime.setItemText(81, _translate("MainWindow", "2018-6-19 17:53:34"))
        self.comboBox_starttime.setItemText(82, _translate("MainWindow", "2018-6-19 18:15:00"))
        self.comboBox_starttime.setItemText(83, _translate("MainWindow", "2018-6-19 18:19:17"))
        self.comboBox_starttime.setItemText(84, _translate("MainWindow", "2018-6-19 18:23:34"))
        self.comboBox_starttime.setItemText(85, _translate("MainWindow", "2018-6-19 18:30:00"))
        self.comboBox_starttime.setItemText(86, _translate("MainWindow", "2018-6-19 18:34:17"))
        self.comboBox_starttime.setItemText(87, _translate("MainWindow", "2018-6-19 18:38:34"))
        self.comboBox_starttime.setItemText(88, _translate("MainWindow", "2018-6-19 18:38:34"))
        self.comboBox_starttime.setItemText(89, _translate("MainWindow", "2018-6-19 18:49:17"))
        self.comboBox_starttime.setItemText(90, _translate("MainWindow", "2018-6-19 18:53:34"))
        self.comboBox_starttime.setItemText(91, _translate("MainWindow", "2018-6-19 19:15:00"))
        self.comboBox_starttime.setItemText(92, _translate("MainWindow", "2018-6-19 19:19:17"))
        self.comboBox_starttime.setItemText(93, _translate("MainWindow", "2018-6-19 19:23:34"))
        self.comboBox_starttime.setItemText(94, _translate("MainWindow", "2018-6-19 19:30:00"))
        self.comboBox_starttime.setItemText(95, _translate("MainWindow", "2018-6-19 19:34:17"))
        self.comboBox_starttime.setItemText(96, _translate("MainWindow", "2018-6-19 19:38:34"))


        self.label_time.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">开始时间：</span></p></body></html>"))
        # self.dateTimeEdit.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm"))
        self.label_station.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">选择电站：</span></p></body></html>"))
        # self.dateTimeEdit_end.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm-ss"))
        self.label_error1.setText(_translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">时延误差：</span></p></body></html>"))
        self.label_error2.setText(_translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">关联系数误差：</span></p></body></html>"))


    def str_datetime(self, t):

        # tart_time = self.dateTimeEdit_start.text()

        t1, t2 = t.split(' ')
        year, month, day = t1.split('/')
        hour, minute = t2.split('-')

        date1 = datetime.datetime(
            int(year),
            int(month),
            int(day),
            int(hour),
            int(minute),
            0)

        return pd.Timestamp(date1)

    def get_station_name(self, i):
        # 获取电站类型
        global station_
        station_ = i

    def get_starttime(self, i):
        global start_time
        start_time = i

    def show_solar_Correlation(self):

        print('正在分析光伏关联模式，请稍后...')
        try:
            Time_Target = pd.to_datetime(start_time)  # 目标时刻点（认为是最近历史时刻）
        except NameError:
            Time_Target = pd.to_datetime(datetime.datetime(2018,6,19,12,15))
        try:
            Farm_for_target = int(station_[2:])
        except NameError:
            Farm_for_target = 509


            ### 时延相关系数
        def CrossCorr(Farm_target, Farm_Proceed, Time_Target, Period=30, Lag_Bound=15):
            ## 计算目标风电场Farm_target, 上下游风电场 Farm_Proceed 在目标时刻 Time， 时间窗Period下的互相关系数
            # Lag_Bound 是检测超前的时间上限
            data_root = 'Time_series_data/JILIN/Solar'

            Positive = np.zeros((Lag_Bound + 1, 2))  # 超前时间>=0 用正数表示，第一列是时间，第二列是相关系数
            Negative = np.zeros((Lag_Bound + 1, 2))  # 滞后时间<=0 用正数表示，第一列是时间，第二列是相关系数

            filepath_FarmT = data_root + '/Power/' + str(Farm_target) + '.csv'
            FarmT = pd.read_csv(filepath_FarmT, index_col=0, parse_dates=True)  # 目标电场

            filepath_FarmP = data_root + '/Power/' + str(Farm_Proceed) + '.csv'
            FarmP = pd.read_csv(filepath_FarmP, index_col=0, parse_dates=True)  # 目标电场

            # FarmP = Data_all[Farm_Proceed] # 上下游电场

            T_P = Time_Target - datetime.timedelta(minutes=(Period - 1) * 15)
            T = Time_Target

            for lag in range(Lag_Bound + 1):
                Positive[lag, 0] = lag
                T_P_L = Time_Target - datetime.timedelta(minutes=(Period + lag - 1) * 15)
                T_L = Time_Target - datetime.timedelta(minutes=lag * 15)
                # Positive[lag, 1] = np.corrcoef(FarmT.loc[Time - Period + 1: Time, 'WS'].values, FarmP.loc[Time - Period + 1 - lag: Time - lag, 'WS'].values, rowvar=False)[0, -1]
                x_1 = FarmT.loc[T_P: T, 'power'].values.reshape(-1)
                x_2 = FarmP.loc[T_P_L: T_L, 'power'].values.reshape(-1)

                Positive[lag, 1] = np.corrcoef(x_1, x_2, rowvar=False)[0, -1]

            Best_Lag = np.argmax(Positive[:, 1])

            for lag in range(Lag_Bound + 1):
                Negative[lag, 0] = -lag
                T_P_L = Time_Target - datetime.timedelta(minutes=(Period + lag - 1) * 15)
                T_L = Time_Target - datetime.timedelta(minutes=lag * 15)
                # Negative[lag, 1] = np.corrcoef(FarmP.loc[Time - Period + 1: Time, 'WS'].values, FarmT.loc[Time - Period + 1 - lag: Time - lag, 'WS'].values, rowvar=False)[0, -1]
                Negative[lag, 1] = np.corrcoef(FarmP.loc[T_P: T, 'power'].values.reshape(-1),
                                               FarmT.loc[T_P_L: T_L, 'power'].values.reshape(-1), rowvar=False)[0, -1]

            return Positive, Negative, Best_Lag

        #####      外部输入参数      #####
        df = pd.read_excel(r'main_win_data/station_info_jilin.xlsx', sheet_name='光伏', index_col=0)
        df.columns = ['CAP', 'Lat', 'Lon', 'NWP_ID']

        Location = df.iloc[:, 1:3].values

        Farm_for_Proceed = [511, 514, 520, 521]
        # if Farm_for_target == 5: Farm_for_Proceed = [0,2,3,5] #用于上下游检测的风电场编号
        Other_Farms_ID = df.index.tolist()
        Other_Farms_ID.remove(Farm_for_target)

        # del (Other_Farms[Farm_for_target])
        def ID_2_num(x):
            if x < 513:
                return x - 501
            else:
                return x - 502

        Other_Farms = list(map(ID_2_num, Other_Farms_ID))

        Period = 20  # 用于计算lag的时间窗

        Best_of_Farms = np.zeros((len(Farm_for_Proceed), 2))  # 记录各个电场对应的最优提前量和对应的Lag，如果Lag是负值则直接忽略
        for i, farm in enumerate(Farm_for_Proceed):  # 计算各个电场最优的时延结果
            Positive, Negative, Best_Lag = CrossCorr( Farm_for_target, farm, Time_Target, Period, Lag_Bound=15)
            Best_of_Farms[i, :] = [Best_Lag, Positive[Best_Lag, 1]]

        Final_Farm = Farm_for_Proceed[np.argmax(Best_of_Farms[:, 1])]
        Final_Lag = Best_of_Farms[np.argmax(Best_of_Farms[:, 1]), 0]
        Final_Lag = Final_Lag.astype('int')
        Final_CrossCor = Best_of_Farms[np.argmax(Best_of_Farms[:, 1]), 1]

        Final_Farm_str = '光伏' + str(Final_Farm)

        print('光伏关联模式分析完成\n')



        with open('Fianl_cross_nan.pkl', 'wb') as f:
            pickle.dump(Final_CrossCor,f)

        # if Final_Lag == Final_CrossCor_nan:
        if isnan(Final_CrossCor):
            # print('当前时刻相邻电站出力无波动，无关联电站')
            Sheet = pd.DataFrame(['当前时刻相邻电站出力无波动，无关联电站'])

            self.show_table(Sheet)

            self.textBrowser.setText('')
            self.textBrowser.setAlignment(QtCore.Qt.AlignCenter)
            self.textBrowser2.setText('')
            self.textBrowser2.setAlignment(QtCore.Qt.AlignCenter)

        else:
            Sheet = pd.DataFrame([[Final_Farm_str, Final_CrossCor, Final_Lag]], columns=['关联电场', '关联系数', '超前量'],
                                 index=['估计'])

            self.m.Plot_2(Location, Other_Farms, Farm_for_target, Final_Farm)

            self.show_table(Sheet)

    def Solar_Correlation_EVA(self):

        print('正在进行光伏关联模式误差分析，请稍后...')
        ## 输入 #####
        try:
            Time_Target = pd.to_datetime(start_time)
        except NameError:
            Time_Target = datetime.datetime(2018,6,19,12,15)
        # Time_Target = pd.to_datetime(start_time)  # 目标时刻点（认为是最近历史时刻）
        try:
            Farm_for_target = int(station_[2:])
        except NameError:
            Farm_for_target = 509

        # ------------------  主程序 --------------#

        ### 时延相关系数
        def CrossCorr(Farm_target, Farm_Proceed, Time_Target, Period=30, Lag_Bound=15):
            ## 计算目标风电场Farm_target, 上下游风电场 Farm_Proceed 在目标时刻 Time， 时间窗Period下的互相关系数
            # Lag_Bound 是检测超前的时间上限
            data_root = 'Time_series_data/JILIN/Solar'

            Positive = np.zeros((Lag_Bound + 1, 2))  # 超前时间>=0 用正数表示，第一列是时间，第二列是相关系数
            Negative = np.zeros((Lag_Bound + 1, 2))  # 滞后时间<=0 用正数表示，第一列是时间，第二列是相关系数

            filepath_FarmT = data_root + '/Power/' + str(Farm_target) + '.csv'
            FarmT = pd.read_csv(filepath_FarmT, index_col=0, parse_dates=True)  # 目标电场

            filepath_FarmP = data_root + '/Power/' + str(Farm_Proceed) + '.csv'
            FarmP = pd.read_csv(filepath_FarmP, index_col=0, parse_dates=True)  # 目标电场

            # FarmP = Data_all[Farm_Proceed] # 上下游电场

            T_P = Time_Target - datetime.timedelta(minutes=(Period - 1) * 15)
            T = Time_Target

            for lag in range(Lag_Bound + 1):
                Positive[lag, 0] = lag
                T_P_L = Time_Target - datetime.timedelta(minutes=(Period + lag - 1) * 15)
                T_L = Time_Target - datetime.timedelta(minutes=lag * 15)
                # Positive[lag, 1] = np.corrcoef(FarmT.loc[Time - Period + 1: Time, 'WS'].values, FarmP.loc[Time - Period + 1 - lag: Time - lag, 'WS'].values, rowvar=False)[0, -1]
                x_1 = FarmT.loc[T_P: T, 'power'].values.reshape(-1)
                x_2 = FarmP.loc[T_P_L: T_L, 'power'].values.reshape(-1)

                Positive[lag, 1] = np.corrcoef(x_1, x_2, rowvar=False)[0, -1]

            Best_Lag = np.argmax(Positive[:, 1])

            for lag in range(Lag_Bound + 1):
                Negative[lag, 0] = -lag
                T_P_L = Time_Target - datetime.timedelta(minutes=(Period + lag - 1) * 15)
                T_L = Time_Target - datetime.timedelta(minutes=lag * 15)
                # Negative[lag, 1] = np.corrcoef(FarmP.loc[Time - Period + 1: Time, 'WS'].values, FarmT.loc[Time - Period + 1 - lag: Time - lag, 'WS'].values, rowvar=False)[0, -1]
                Negative[lag, 1] = np.corrcoef(FarmP.loc[T_P: T, 'power'].values.reshape(-1),
                                               FarmT.loc[T_P_L: T_L, 'power'].values.reshape(-1), rowvar=False)[0, -1]

            return Positive, Negative, Best_Lag

        #####      外部输入参数      #####
        Farm_for_Proceed = [511, 514, 520, 521]  # 用于上下游检测的风电场编号

        df = pd.read_excel(r'main_win_data/station_info_jilin.xlsx', sheet_name='光伏', index_col=0)
        df.columns = ['CAP', 'Lat', 'Lon', 'NWP_ID']
        Other_Farms_ID = df.index.tolist()
        Other_Farms_ID.remove(Farm_for_target)

        # del (Other_Farms[Farm_for_target])
        def ID_2_num(x):
            if x < 513:
                return x - 501
            else:
                return x - 502

        Other_Farms = list(map(ID_2_num, Other_Farms_ID))

        Period = 20  # 用于计算lag的时间窗

        Best_of_Farms = np.zeros((len(Farm_for_Proceed), 2))  # 记录各个电场对应的最优提前量和对应的Lag，如果Lag是负值则直接忽略
        for i, farm in enumerate(Farm_for_Proceed):  # 计算各个电场最优的时延结果
            Positive, Negative, Best_Lag = CrossCorr(Farm_for_target, farm, Time_Target, Period, Lag_Bound=15)
            Best_of_Farms[i, :] = [Best_Lag, Positive[Best_Lag, 1]]

        Final_Farm = Farm_for_Proceed[np.argmax(Best_of_Farms[:, 1])]
        Final_Lag = Best_of_Farms[np.argmax(Best_of_Farms[:, 1]), 0]
        Final_Lag = Final_Lag.astype('int')
        Final_CrossCor = Best_of_Farms[np.argmax(Best_of_Farms[:, 1]), 1]
        # if Final_CrossCor < 0.2:  # 如果相关系数过于小
        #     Final_Lag = -1

        ## 自动触发后的误差评估环节 ##
        Real_CrossCor, _, Real_Lag = CrossCorr(Farm_for_target, Final_Farm, Time_Target + datetime.timedelta(minutes=15*6), Period=30, Lag_Bound=15)
        Real_CrossCor = Real_CrossCor[Real_Lag, 1]
        if Real_CrossCor < 0.2:  # 如果相关系数过于小
            Real_Lag = -1
            # if Final_CrossCor < 0.2:  # 假如原有系数判断也是对的
            #     Real_CrossCor = Final_CrossCor
        ### 输出 ###
        Error_Lag = Final_Lag - Real_Lag  # 预计的提前时间减去真实的提前时间
        Error_CrossCor = abs(Final_CrossCor - Real_CrossCor)  # 相关系数的相对误差（相对真实的系数结果）
        Error_CrossCor = format(Error_CrossCor, '.3f')

        Final_CrossCor = format(Final_CrossCor, '.2f')
        Real_CrossCor = format(Real_CrossCor, '.2f')

        Final_Farm_str = '光伏' + str(Final_Farm)

        with open('Fianl_cross_nan.pkl', 'rb') as f:
            Final_CrossCor_nan = pickle.load(f)
        print('光伏关联模式误差分析完成\n')

        if isnan(Final_CrossCor_nan):
            Sheet = pd.DataFrame(['当前时刻相邻电站出力无波动，无关联电站'])
            self.show_table(Sheet)

            self.textBrowser.setText('')
            self.textBrowser.setAlignment(QtCore.Qt.AlignCenter)
            self.textBrowser2.setText('')
            self.textBrowser2.setAlignment(QtCore.Qt.AlignCenter)

        else:
            Sheet = pd.DataFrame(np.array([[Final_Farm_str, Final_CrossCor, Final_Lag], [Final_Farm_str, Real_CrossCor, Real_Lag]]),
                                 columns=['关联电场', '关联系数', '超前量'], index=['估计', '真实'])

            self.show_table(Sheet)

            self.textBrowser.setText(str(Error_Lag))
            self.textBrowser.setAlignment(QtCore.Qt.AlignCenter)
            self.textBrowser2.setText(str(Error_CrossCor))
            self.textBrowser2.setAlignment(QtCore.Qt.AlignCenter)





    def show_table(self, input_table):

        # show table
        input_table = input_table.round(2)

        input_table_rows = input_table.shape[0]
        input_table_colunms = input_table.shape[1]
        input_table_header = input_table.columns.values.tolist()
        input_table_index = input_table.index.values.tolist()

        # ===========读取表格，转换表格，============================================
        # ======================给tablewidget设置行列表头============================

        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        if input_table_colunms == 1:
            self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头
            self.tableWidget.horizontalHeader().setVisible(False)  # 隐藏水平表头
        else:
            self.tableWidget.verticalHeader().setVisible(True)  # 隐藏垂直表头
            self.tableWidget.horizontalHeader().setVisible(True)  # 隐藏水平表头
            self.tableWidget.setHorizontalHeaderLabels(input_table_header)
            self.tableWidget.setVerticalHeaderLabels(input_table_index)


        # ======================给tablewidget设置行列表头============================

        # ================遍历表格每个元素，同时添加到tablewidget中========================
        for i in range(input_table_rows):
            input_table_rows_values = input_table.iloc[[i]]
            # print(input_table_rows_values)
            input_table_rows_values_array = np.array(
                input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[
                0]
            # print(input_table_rows_values_list)
            for j in range(input_table_colunms):
                input_table_items_list = input_table_rows_values_list[j]
                # print(input_table_items_list)
                # print(type(input_table_items_list))

                # ==============将遍历的元素添加到tablewidget中并显示=======================

                input_table_items = str(input_table_items_list)
                newItem = QTableWidgetItem(input_table_items)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, newItem)




class MyWindow_solar_corr(QMainWindow, Ui_MainWindow_solar_corr):
    def __init__(self, parent=None):
        super(MyWindow_solar_corr, self).__init__(parent)
        self.setupUi(self)

import sys
if __name__ == '__main__':
    # 字体随分辨率自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyWindow_solar_corr()
    myWin.show()

    sys.exit(app.exec_())