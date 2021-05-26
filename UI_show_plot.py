# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import base64
import datetime
import numpy as np
from images.cloud_image_jpg import img as cloud_image
from images.map_png import img as map_img
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import scipy.io as scio
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PIL import Image

# 需要先设置内存限制，不然仍然会报错内存溢出
Image.MAX_IMAGE_PIXELS = None

tmp = open('cloud_image.jpg', 'wb')        #创建临时的文件
tmp.write(base64.b64decode(cloud_image))    ##把这个one图片解码出来，写入文件中去。
tmp.close()

tmp = open('map_img.png', 'wb')        #创建临时的文件
tmp.write(base64.b64decode(map_img))    ##把这个one图片解码出来，写入文件中去。
tmp.close()

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=7, height=3.5, dpi=80):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.16, bottom=0.25, right=0.84, top=0.9, hspace=0, wspace=0)
        self.axes = fig.add_subplot(111)
        self.ax_twin = self.axes.twinx()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.init_plot()#打开App时可以初始化图片
        # self.plot()

    def plot(self):

        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(100)

    def init_plot(self, data, date=1):

        data[date * 96: (date + 1) * 96].plot(ax=self.axes)
        self.draw()

    def update_figure(self, data_to_plot, start_time, end_time):

        if len(data_to_plot) == 1:

            self.axes.cla()
            data = data_to_plot[0]
            print('data_extract')
            data.loc[start_time:end_time].plot(ax=self.axes)
            danwei = {'power':'功率/MW', 'temperature':'温度/K', 'windspeed_30':'风速/(m/s)'}
            ylabel = danwei[data.columns[0]]
            self.axes.set(ylabel=ylabel, xlabel='时间/h')
            legends = ylabel.split('/')[0]
            self.axes.legend([legends])
            self.draw()

        elif len(data_to_plot) == 2:

            self.axes.cla()

            data1 = data_to_plot[0]
            data1.loc[start_time:end_time].plot(ax=self.axes)
            danwei = {'power': '功率/MW', 'temperature': '温度/K', 'windspeed_30': '风速/(m/s)'}
            ylabel = danwei[data1.columns[0]]
            self.axes.set(ylabel=ylabel, xlabel='时间/h')
            legends = ylabel.split('/')[0]
            self.axes.legend([legends], loc="upper right")

            self.ax_twin.cla()
            data2 = data_to_plot[1]
            data2.loc[start_time:end_time].plot(ax=self.ax_twin, c='r')
            danwei = {'power': '功率/MW', 'temperature': '温度/K', 'windspeed_30': '风速/(m/s)'}
            ylabel = danwei[data2.columns[0]]
            self.ax_twin.set(ylabel=ylabel)
            self.ax_twin.set_xlabel('Same')

            legends = ylabel.split('/')[0]
            self.ax_twin.legend([legends],loc="upper left")

            self.draw()

    def show_image(self, image_file):

        self.axes.cla()
        print('clear axes fininshed')

        self.axes.imshow(image_file, cmap='gray')
        # self.axes.imshow('map_img.png')
        self.draw()

    def scene_plot(self, data_toplot, start_time, end_time):

        counter = 1

        def start_timer():
            nonlocal counter
            global inputs
            counter += 1

            inputs = [counter, data_toplot, start_time, end_time]

            Y_toplot = data_toplot[0].loc[start_time:end_time]

            if counter >= len(Y_toplot):
                timer.stop()
                timer.deleteLater()

        timer = QTimer(self)
        print('timer start')

        timer.timeout.connect(start_timer)
        timer.timeout.connect(lambda: self.scene_update_figure(inputs))
        timer.start(1000)

        # try:
        #     timer.timeout.connect(start_timer)
        #     timer.timeout.connect(lambda: self.scene_update_figure(inputs))
        #     timer.start(1000)
        #
        # except NameError:
        #     pass

    def scene_update_figure(self, inputs):

        [counter, data_to_plot, start_time, end_time] = inputs

        if len(data_to_plot) == 1:

            self.axes.cla()

            Y_toplot = data_to_plot[0].loc[start_time:end_time]

            data_toplot_1 = Y_toplot[:counter]
            pred_start = data_toplot_1.iloc[-1:].index[0]
            data_toplot_1.columns = ['功率']

            data_toplot_1[:counter].plot(ax=self.axes)

            # # 横坐标
            x_ticks = pd.date_range(
                start=start_time, end=end_time, freq='2h')

            self.axes.set_xticks([])
            self.axes.set_xlim([x_ticks[0], x_ticks[-1]])
            for tick in self.axes.get_xticklabels():
                tick.set_rotation(45)

            # 纵轴
            danwei = {'power': '功率/MW', 'temperature': '温度/K', 'windspeed_30': '风速/(m/s)'}
            ylabel = danwei[data_to_plot[0].columns[0]]
            self.axes.set(ylabel=ylabel, xlabel='时间/h')

            self.axes.set_xlabel('时间')
            self.axes.set_title(str(pred_start.date()), fontsize=10, color='r')  # r: red
            self.draw()
            ##############################################
        elif len(data_to_plot) == 2:

            # 清楚图像
            self.axes.cla()
            self.ax_twin.cla()

            # 选择数据
            Y_toplot = data_to_plot[0].loc[start_time:end_time]
            Y_toplot_twin = data_to_plot[1].loc[start_time:end_time]

            data_toplot_1 = Y_toplot[:counter]
            data_toplot_twin = Y_toplot_twin[:counter]

            # 记录日期
            pred_start = data_toplot_1.iloc[-1:].index[0]

            # 设置坐标轴和图例文字
            danwei = {'power': '功率/MW', 'temperature': '温度/K', 'windspeed_30': '风速/(m/s)'}
            ylabel = danwei[data_to_plot[0].columns[0]]
            ylabel_twin = danwei[data_to_plot[1].columns[0]]

            data_toplot_1.columns = [ylabel.split('/')[0]]
            data_toplot_twin.columns = [ylabel_twin.split('/')[0]]

            # 画图
            data_toplot_1[:counter].plot(ax=self.axes)
            data_toplot_twin[:counter].plot(ax=self.ax_twin, c='r')

            # 设置横坐标
            x_ticks = pd.date_range(
                start=start_time, end=end_time, freq='2h')

            self.axes.set_xticks([])
            self.axes.set_xlim([x_ticks[0], x_ticks[-1]])
            for tick in self.axes.get_xticklabels():
                tick.set_rotation(45)

            # 设置纵轴文字
            self.axes.set(ylabel=ylabel, xlabel='时间/h')
            self.ax_twin.set(ylabel=ylabel)

            # 图例
            self.axes.legend(loc="upper right")
            self.ax_twin.legend(loc="upper left")

            self.axes.set_xlabel('时间')
            self.axes.set_title(str(pred_start.date()), fontsize=10, color='r')  # r: red
            self.draw()


class Ui_MainWindow_show_plot(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 60, 879, 3))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 371, 31))
        self.label.setObjectName("label")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 410, 94, 32))
        self.pushButton.setObjectName("pushButton")

        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(100, 450, 94, 32))
        self.pushButton2.setObjectName("pushButton2")

        self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(450, 450, 150, 32))
        self.pushButton3.setObjectName("pushButton3")

        #
        # # 增加数据源选择
        #
        # self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        # self.layoutWidget1.setGeometry(QtCore.QRect(540, 100, 250, 74))
        # self.layoutWidget1.setObjectName("layoutWidget1")
        #
        # self.label_choose_dataset = QtWidgets.QLabel(self.layoutWidget1)
        # self.label_choose_dataset.setObjectName("选择数据源：")
        # # self.horizontalLayout.addWidget(self.label_choose_dataset)
        #
        # self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        # self.layoutWidget2.setGeometry(QtCore.QRect(640, 100, 245, 74))
        # self.layoutWidget2.setObjectName("layoutWidget2")
        #
        # self.comboBox_datasource = QtWidgets.QComboBox(self.layoutWidget2)
        # self.comboBox_datasource.setObjectName("comboBox_datasource")
        # self.comboBox_datasource.addItem("")
        # self.comboBox_datasource.setItemText(0, "")
        # self.comboBox_datasource.addItem("")
        # self.comboBox_datasource.addItem("")
        # # self.horizontalLayout.addWidget(self.comboBox_station)


        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(16, 330, 266, 66))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.dateTimeEdit_start = QtWidgets.QDateTimeEdit(self.layoutWidget)
        self.dateTimeEdit_start.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 6, 1), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit_start.setObjectName("dateTimeEdit_start")
        self.horizontalLayout_3.addWidget(self.dateTimeEdit_start)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.dateTimeEdit_end = QtWidgets.QDateTimeEdit(self.layoutWidget)
        self.dateTimeEdit_end.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 6, 2), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit_end.setObjectName("dateTimeEdit_end")
        self.horizontalLayout_2.addWidget(self.dateTimeEdit_end)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        # plot_1
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 130, 245, 74))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox_station = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBox_station.setObjectName("comboBox_station")
        self.comboBox_station.addItem("")
        self.comboBox_station.setItemText(0, "")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_station)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.comboBox_datatype = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBox_datatype.setObjectName("comboBox_datatype")
        self.comboBox_datatype.addItem("")
        self.comboBox_datatype.setItemText(0, "")
        self.comboBox_datatype.addItem("")
        self.comboBox_datatype.addItem("")
        self.comboBox_datatype.addItem("")
        self.comboBox_datatype.addItem("")
        # self.comboBox_datatype.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_datatype)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        # plot_2
        self.layoutWidget1_added = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1_added.setGeometry(QtCore.QRect(20, 230, 245, 74))
        self.layoutWidget1_added.setObjectName("layoutWidget1_added")
        self.verticalLayout_2_added = QtWidgets.QVBoxLayout(self.layoutWidget1_added)
        self.verticalLayout_2_added.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2_added.setObjectName("verticalLayout_2_added")
        self.horizontalLayout_added = QtWidgets.QHBoxLayout()
        self.horizontalLayout_added.setObjectName("horizontalLayout")
        self.label_2_added = QtWidgets.QLabel(self.layoutWidget1_added)
        self.label_2_added.setObjectName("label_2_added")
        self.horizontalLayout_added.addWidget(self.label_2_added)
        self.comboBox_station_added = QtWidgets.QComboBox(self.layoutWidget1_added)
        self.comboBox_station_added.setObjectName("comboBox_station_added")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.setItemText(0, "")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.comboBox_station_added.addItem("")
        self.horizontalLayout_added.addWidget(self.comboBox_station_added)
        self.verticalLayout_2_added.addLayout(self.horizontalLayout_added)
        self.horizontalLayout_4_added = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4_added.setObjectName("horizontalLayout_4_added")
        self.label_7_added = QtWidgets.QLabel(self.layoutWidget1_added)
        self.label_7_added.setObjectName("label_7_added")
        self.horizontalLayout_4_added.addWidget(self.label_7_added)
        self.comboBox_datatype_added = QtWidgets.QComboBox(self.layoutWidget1_added)
        self.comboBox_datatype_added.setObjectName("comboBox_datatype_added")
        self.comboBox_datatype_added.addItem("")
        self.comboBox_datatype_added.setItemText(0, "")
        self.comboBox_datatype_added.addItem("")
        self.comboBox_datatype_added.addItem("")
        self.comboBox_datatype_added.addItem("")
        self.comboBox_datatype_added.addItem("")
        # self.comboBox_datatype.addItem("")
        self.horizontalLayout_4_added.addWidget(self.comboBox_datatype_added)
        self.verticalLayout_2_added.addLayout(self.horizontalLayout_4_added)

        #########

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.m = PlotCanvas(self, width=5.2, height=3.3)  # 实例化一个画布对象
        self.m.move(320, 160)

        self.comboBox_station.currentIndexChanged[str].connect(
            self.get_station_name)  # 条目发生改变，发射信号，传递条目内容
        self.comboBox_datatype.currentIndexChanged[str].connect(
            self.get_data_name)  # 条目发生改变，发射信号，传递条目内容

        self.comboBox_station_added.currentIndexChanged[str].connect(
            self.get_station_name_added)  # 条目发生改变，发射信号，传递条目内容
        self.comboBox_datatype_added.currentIndexChanged[str].connect(
            self.get_data_name_added)  # 条目发生改变，发射信号，传递条目内容

        # self.pushButton.clicked.connect(self.print_)
        self.pushButton.clicked.connect(self.load_data)
        self.pushButton.clicked.connect(self.load_data_added)

        self.pushButton.clicked.connect(self.plot_)

        self.pushButton2.clicked.connect(self.load_data)
        self.pushButton2.clicked.connect(self.load_data_added)

        self.pushButton2.clicked.connect(self.show_gif)

        self.pushButton3.clicked.connect(self.abnormal_detection)

        # self.pushButton_2.clicked.connect(self.show_dir)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:24pt;\">风电/光伏数据展示（吉林）</span></p><p><br/></p></body></html>"))

        self.label_2.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">电站：</span></p></body></html>"))
        self.comboBox_station.setItemText(1, _translate("MainWindow", "风电1"))
        self.comboBox_station.setItemText(2, _translate("MainWindow", "风电2"))
        self.comboBox_station.setItemText(3, _translate("MainWindow", "风电3"))
        self.comboBox_station.setItemText(4, _translate("MainWindow", "风电4"))
        self.comboBox_station.setItemText(5, _translate("MainWindow", "风电5"))
        self.comboBox_station.setItemText(6, _translate("MainWindow", "风电6"))
        self.comboBox_station.setItemText(7, _translate("MainWindow", "风电7"))
        self.comboBox_station.setItemText(8, _translate("MainWindow", "风电8"))
        self.comboBox_station.setItemText(9, _translate("MainWindow", "风电9"))
        self.comboBox_station.setItemText(10, _translate("MainWindow", "风电10"))
        self.comboBox_station.setItemText(11, _translate("MainWindow", "风电11"))
        self.comboBox_station.setItemText(12, _translate("MainWindow", "风电12"))
        self.comboBox_station.setItemText(13, _translate("MainWindow", "风电13"))
        self.comboBox_station.setItemText(14, _translate("MainWindow", "风电14"))
        self.comboBox_station.setItemText(15, _translate("MainWindow", "风电15"))
        self.comboBox_station.setItemText(16, _translate("MainWindow", "风电16"))
        self.comboBox_station.setItemText(17, _translate("MainWindow", "风电17"))
        self.comboBox_station.setItemText(18, _translate("MainWindow", "风电18"))
        self.comboBox_station.setItemText(19, _translate("MainWindow", "风电19"))
        self.comboBox_station.setItemText(20, _translate("MainWindow", "风电20"))
        self.comboBox_station.setItemText(21, _translate("MainWindow", "光伏1"))
        self.comboBox_station.setItemText(22, _translate("MainWindow", "光伏2"))
        self.comboBox_station.setItemText(23, _translate("MainWindow", "光伏3"))
        self.comboBox_station.setItemText(24, _translate("MainWindow", "光伏4"))
        self.comboBox_station.setItemText(25, _translate("MainWindow", "光伏5"))
        self.comboBox_station.setItemText(26, _translate("MainWindow", "光伏6"))
        self.comboBox_station.setItemText(27, _translate("MainWindow", "光伏7"))
        self.comboBox_station.setItemText(28, _translate("MainWindow", "光伏8"))
        self.comboBox_station.setItemText(29, _translate("MainWindow", "光伏9"))
        self.comboBox_station.setItemText(30, _translate("MainWindow", "光伏10"))
        self.comboBox_station.setItemText(31, _translate("MainWindow", "光伏11"))
        self.comboBox_station.setItemText(32, _translate("MainWindow", "光伏12"))
        self.comboBox_station.setItemText(33, _translate("MainWindow", "光伏13"))
        self.comboBox_station.setItemText(34, _translate("MainWindow", "光伏14"))
        self.comboBox_station.setItemText(35, _translate("MainWindow", "光伏15"))
        self.comboBox_station.setItemText(36, _translate("MainWindow", "光伏16"))
        self.comboBox_station.setItemText(37, _translate("MainWindow", "光伏17"))
        self.comboBox_station.setItemText(38, _translate("MainWindow", "光伏18"))
        self.comboBox_station.setItemText(39, _translate("MainWindow", "光伏19"))
        self.comboBox_station.setItemText(40, _translate("MainWindow", "光伏20"))
        self.comboBox_station.setItemText(41, _translate("MainWindow", "光伏21"))
        self.label_7.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">导入数据类型：</span></p></body></html>"))
        self.comboBox_datatype.setItemText(1, _translate("MainWindow", "功率"))
        self.comboBox_datatype.setItemText(2, _translate("MainWindow", "NWP温度"))
        self.comboBox_datatype.setItemText(3, _translate("MainWindow", "NWP风速"))
        self.comboBox_datatype.setItemText(4, _translate("MainWindow", "NWP辐照度"))

        ########################
        # added
        self.label_2_added.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">电站：</span></p></body></html>"))
        self.comboBox_station_added.setItemText(1, _translate("MainWindow", "风电1"))
        self.comboBox_station_added.setItemText(2, _translate("MainWindow", "风电2"))
        self.comboBox_station_added.setItemText(3, _translate("MainWindow", "风电3"))
        self.comboBox_station_added.setItemText(4, _translate("MainWindow", "风电4"))
        self.comboBox_station_added.setItemText(5, _translate("MainWindow", "风电5"))
        self.comboBox_station_added.setItemText(6, _translate("MainWindow", "风电6"))
        self.comboBox_station_added.setItemText(7, _translate("MainWindow", "风电7"))
        self.comboBox_station_added.setItemText(8, _translate("MainWindow", "风电8"))
        self.comboBox_station_added.setItemText(9, _translate("MainWindow", "风电9"))
        self.comboBox_station_added.setItemText(10, _translate("MainWindow", "风电10"))
        self.comboBox_station_added.setItemText(11, _translate("MainWindow", "风电11"))
        self.comboBox_station_added.setItemText(12, _translate("MainWindow", "风电12"))
        self.comboBox_station_added.setItemText(13, _translate("MainWindow", "风电13"))
        self.comboBox_station_added.setItemText(14, _translate("MainWindow", "风电14"))
        self.comboBox_station_added.setItemText(15, _translate("MainWindow", "风电15"))
        self.comboBox_station_added.setItemText(16, _translate("MainWindow", "风电16"))
        self.comboBox_station_added.setItemText(17, _translate("MainWindow", "风电17"))
        self.comboBox_station_added.setItemText(18, _translate("MainWindow", "风电18"))
        self.comboBox_station_added.setItemText(19, _translate("MainWindow", "风电19"))
        self.comboBox_station_added.setItemText(20, _translate("MainWindow", "风电20"))
        self.comboBox_station_added.setItemText(21, _translate("MainWindow", "光伏1"))
        self.comboBox_station_added.setItemText(22, _translate("MainWindow", "光伏2"))
        self.comboBox_station_added.setItemText(23, _translate("MainWindow", "光伏3"))
        self.comboBox_station_added.setItemText(24, _translate("MainWindow", "光伏4"))
        self.comboBox_station_added.setItemText(25, _translate("MainWindow", "光伏5"))
        self.comboBox_station_added.setItemText(26, _translate("MainWindow", "光伏6"))
        self.comboBox_station_added.setItemText(27, _translate("MainWindow", "光伏7"))
        self.comboBox_station_added.setItemText(28, _translate("MainWindow", "光伏8"))
        self.comboBox_station_added.setItemText(29, _translate("MainWindow", "光伏9"))
        self.comboBox_station_added.setItemText(30, _translate("MainWindow", "光伏10"))
        self.comboBox_station_added.setItemText(31, _translate("MainWindow", "光伏11"))
        self.comboBox_station_added.setItemText(32, _translate("MainWindow", "光伏12"))
        self.comboBox_station_added.setItemText(33, _translate("MainWindow", "光伏13"))
        self.comboBox_station_added.setItemText(34, _translate("MainWindow", "光伏14"))
        self.comboBox_station_added.setItemText(35, _translate("MainWindow", "光伏15"))
        self.comboBox_station_added.setItemText(36, _translate("MainWindow", "光伏16"))
        self.comboBox_station_added.setItemText(37, _translate("MainWindow", "光伏17"))
        self.comboBox_station_added.setItemText(38, _translate("MainWindow", "光伏18"))
        self.comboBox_station_added.setItemText(39, _translate("MainWindow", "光伏19"))
        self.comboBox_station_added.setItemText(40, _translate("MainWindow", "光伏20"))
        self.comboBox_station_added.setItemText(41, _translate("MainWindow", "光伏21"))
        self.label_7_added.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">导入数据类型：</span></p></body></html>"))
        self.comboBox_datatype_added.setItemText(1, _translate("MainWindow", "功率"))
        self.comboBox_datatype_added.setItemText(2, _translate("MainWindow", "NWP温度"))
        self.comboBox_datatype_added.setItemText(3, _translate("MainWindow", "NWP风速"))
        self.comboBox_datatype_added.setItemText(4, _translate("MainWindow", "NWP辐照度"))

        # self.label_choose_dataset.setText(_translate("MainWindow",
        #                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">数据源：</span></p></body></html>"))
        #
        # self.comboBox_datasource.setItemText(1, _translate("MainWindow", "吉林"))
        # self.comboBox_datasource.setItemText(2, _translate("MainWindow", "内蒙"))

        ####################

        # self.comboBox_datatype.setItemText(4, _translate("MainWindow", "卫星云图"))
        self.label_9.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">开始时间：</span></p></body></html>"))
        self.dateTimeEdit_start.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm-ss"))
        self.label_8.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">截止时间：</span></p></body></html>"))
        self.dateTimeEdit_end.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm-ss"))

        self.pushButton.setText(_translate("MainWindow", "导入数据"))
        self.pushButton2.setText(_translate("MainWindow", "动态播放"))
        self.pushButton3.setText(_translate("MainWindow", "异常数据识别"))

    def get_data_name(self, i):
        # 获取数据类型
        global data_
        data_ = i

    def get_station_name(self, i):
        # 获取电站类型
        global station_
        station_ = i

    def get_data_name_added(self, i):
        # 获取数据类型
        global series_data_added
        series_data_added = i

    def get_station_name_added(self, i):
        # 获取电站类型
        global station_added
        station_added = i

    def print_(self):
        # print(data_, station_)
        s = self.lineEdit.text()
        t = self.dateTimeEdit.text()

        print(t)

    def show_dir(self):

        global openfile_name

        openfile_name = QFileDialog.getExistingDirectory(self, '选择文件', '')

        # self.pushButton_2.set

    def load_data(self):

        global input_data

        try:
            if data_ == "功率":
                # 导入光伏数据
                if station_[:2] == "光伏":
                    # TODO
                    openfile_name_ = 'Time_series_data/JILIN/Solar/Power/'
                    input_data = pd.read_csv(
                        openfile_name_ +
                        '/' +
                        str(int(station_[2:])+500) +
                        '.csv',
                        index_col=0,
                        parse_dates=True)
                    print('generate input data sucess')
                    # print(input_data[:10])
                elif station_[:2] == "风电":
                    # TODO
                    Power = scio.loadmat("Time_series_data/JILIN/Wind/wind_power_jilin.mat")
                    print('load_sucess')
                    df_wind_power = pd.DataFrame(Power['Power'])
                    print('generate df_wind_power sucess')
                    df_wind_power.index = pd.date_range(start='2017-01-01', periods=len(df_wind_power[0]), freq='15min')
                    print('generate df_wind_power index sucess')
                    input_data = pd.DataFrame(df_wind_power.iloc[:,int(station_[2:])-1])
                    input_data.columns = ['power']
                    print('generate input data sucess')

            elif data_[:3] == "NWP":
                # 导入NWP
                if station_[:2] == "光伏":
                    dict = {501: 'CN0094',
                            502: 'CN0680',
                            503: 'CN0094',
                            504: 'CN0512',
                            505: 'CN0091',
                            506: 'CN0093',
                            507: 'CN0145',
                            508: 'CN0003',
                            509: 'CN0317',
                            510: 'CN0092',
                            511: 'CN0091',
                            513: 'CN0391',
                            514: 'CN0512',
                            515: 'CN0716',
                            516: 'CN0356',
                            517: 'CN0391',
                            518: 'CN0688',
                            519: 'CN0356',
                            520: 'CN0096',
                            521: 'CN0688'}
                    # TODO
                    # change openfile
                    path_openfile_name = 'Time_series_data/JILIN/Solar/NWP/'
                    input_data = pd.read_csv(path_openfile_name +
                                             dict[int(station_[2:])+500] +
                                             '.csv', index_col=2, parse_dates=True)
                    # print(input_data[:10])
                    if data_[3:] == '风速':
                        input_data = pd.DataFrame(input_data['windspeed_30'])
                    elif data_[3:] == '温度':
                        input_data = pd.DataFrame(input_data['temperature'])
                    elif data_[3:] == '辐照度':
                        input_data_added = pd.DataFrame(input_data['shortwave_radiation'])
                    print('generate input data sucess')

                elif station_[:2] == "风电":
                    dict = {1: 'CN0001',
                            2: 'CN0002',
                            3: 'CN0003',
                            4: 'CN0004',
                            5: 'CN0005',
                            6: 'CN0006',
                            7: 'CN0001',
                            8: 'CN0360',
                            9: 'CN0090',
                            10: 'CN0091',
                            11: 'CN0001',
                            12: 'CN0092',
                            13: 'CN0096',
                            14: 'CN0093',
                            15: 'CN0094',
                            16: 'CN0095',
                            17: 'CN0356',
                            18: 'CN0121',
                            19: 'CN0138',
                            20: 'CN0137'}
                    # TODO
                    # change openfile
                    path_openfile_name = 'Time_series_data/JILIN/Solar/NWP/'
                    input_data = pd.read_csv(path_openfile_name +
                                             dict[int(station_[2:])] +
                                             '.csv', index_col=2, parse_dates=True)
                    # print(input_data[:10])
                    if data_[3:] == '风速':
                        input_data = pd.DataFrame(input_data['windspeed_30'])
                    elif data_[3:] == '温度':
                        input_data = pd.DataFrame(input_data['temperature'])
                    elif data_[3:] == '辐照度':
                        input_data_added = pd.DataFrame(input_data['shortwave_radiation'])

        except NameError:
            pass

    def load_data_added(self):

        global input_data_added

        try:

            if series_data_added == "功率":
                # 导入光伏数据
                if station_added[:2] == "光伏":
                    # TODO
                    openfile_name_ = 'Time_series_data/JILIN/Solar/Power/'
                    input_data_added = pd.read_csv(
                        openfile_name_ +
                        '/' +
                        str(int(station_added[2:])+500) +
                        '.csv',
                        index_col=0,
                        parse_dates=True)
                    print('generate input data sucess')
                    # print(input_data[:10])
                elif station_added[:2] == "风电":
                    # TODO
                    Power = scio.loadmat("Time_series_data/JILIN/Wind/wind_power_jilin.mat")
                    print('load_sucess')
                    df_wind_power = pd.DataFrame(Power['Power'])
                    print('generate df_wind_power sucess')
                    df_wind_power.index = pd.date_range(start='2017-01-01', periods=len(df_wind_power[0]), freq='15min')
                    print('generate df_wind_power index sucess')
                    input_data_added = pd.DataFrame(df_wind_power.iloc[:,int(station_added[2:])-1])
                    input_data_added.columns = ['power']
                    print('generate input data sucess')

            elif series_data_added[:3] == "NWP":
                # 导入NWP
                if station_added[:2] == "光伏":
                    dict = {501: 'CN0094',
                            502: 'CN0680',
                            503: 'CN0094',
                            504: 'CN0512',
                            505: 'CN0091',
                            506: 'CN0093',
                            507: 'CN0145',
                            508: 'CN0003',
                            509: 'CN0317',
                            510: 'CN0092',
                            511: 'CN0091',
                            513: 'CN0391',
                            514: 'CN0512',
                            515: 'CN0716',
                            516: 'CN0356',
                            517: 'CN0391',
                            518: 'CN0688',
                            519: 'CN0356',
                            520: 'CN0096',
                            521: 'CN0688'}
                    # TODO
                    # change openfile
                    path_openfile_name = 'Time_series_data/JILIN/Solar/NWP/'
                    input_data_added = pd.read_csv(path_openfile_name +
                                             dict[int(station_added[2:])+500] +
                                             '.csv', index_col=2, parse_dates=True)
                    # print(input_data[:10])
                    if series_data_added[3:] == '风速':
                        input_data_added = pd.DataFrame(input_data_added['windspeed_30'])
                    elif series_data_added[3:] == '温度':
                        input_data_added = pd.DataFrame(input_data_added['temperature'])
                    elif series_data_added[3:] == '辐照度':
                        input_data_added = pd.DataFrame(input_data_added['shortwave_radiation'])
                    print('generate input data sucess')

                elif station_added[:2] == "风电":
                    dict = {1: 'CN0001',
                            2: 'CN0002',
                            3: 'CN0003',
                            4: 'CN0004',
                            5: 'CN0005',
                            6: 'CN0006',
                            7: 'CN0001',
                            8: 'CN0360',
                            9: 'CN0090',
                            10: 'CN0091',
                            11: 'CN0001',
                            12: 'CN0092',
                            13: 'CN0096',
                            14: 'CN0093',
                            15: 'CN0094',
                            16: 'CN0095',
                            17: 'CN0356',
                            18: 'CN0121',
                            19: 'CN0138',
                            20: 'CN0137'}
                    # TODO
                    # change openfile
                    path_openfile_name = 'Time_series_data/JILIN/Solar/NWP/'
                    input_data_added = pd.read_csv(path_openfile_name +
                                             dict[int(station_added[2:])] +
                                             '.csv', index_col=2, parse_dates=True)
                    # print(input_data[:10])
                    if series_data_added[3:] == '风速':
                        input_data_added = pd.DataFrame(input_data_added['windspeed_30'])
                    elif series_data_added[3:] == '温度':
                        input_data_added = pd.DataFrame(input_data_added['temperature'])
                    elif series_data_added[3:] == '辐照度':
                        input_data_added = pd.DataFrame(input_data_added['shortwave_radiation'])

        except NameError:
            pass

    def str_datetime(self, t):
        import datetime

        t1, t2 = t.split(' ')
        year, month, day = t1.split('/')
        hour, minute, second = t2.split('-')

        date1 = datetime.datetime(
            int(year),
            int(month),
            int(day),
            int(hour),
            int(minute),
            0)

        return pd.Timestamp(date1)

    def str_name(self, t):

        t1, t2 = t.split(' ')
        year, month, day = t1.split('/')
        hour, minute, second = t2.split('-')

        date2 = str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second) + '.mat'

        return date2

    def plot_(self):

        start_time = self.dateTimeEdit_start.text()
        end_time = self.dateTimeEdit_end.text()

        global data_to_plot
        data_to_plot = []

        # try:
        #     data_to_plot.append(input_data)
        # except NameError:
        #     ##TODO
        #     # 任意数据
        #     input_data = []
        #
        # try:
        #     data_to_plot.append(input_data_added)
        # except NameError:
        #     ##TODO
        #     # 任意数据
        #     input_data = []

        try:
            data_to_plot.append(input_data)
        except NameError:
            pass

        try:
            data_to_plot.append(input_data_added)
        except NameError:
            pass

        print('data append sucess')
        print('len(data_to_plot):',len(data_to_plot))

        self.m.update_figure(
            data_to_plot,
            self.str_datetime(start_time),
            self.str_datetime(end_time))

    def show_gif(self):

        start_time = self.dateTimeEdit_start.text()
        end_time = self.dateTimeEdit_end.text()

        data_to_plot = []

        data_to_plot.append(input_data)
        data_to_plot.append(input_data_added)

        print('data append sucess')
        print('len(data_to_plot):', len(data_to_plot))

        self.m.scene_plot(data_to_plot,self.str_datetime(start_time), self.str_datetime(end_time))

    def abnormal_detection(self):

        try:

            print('start detect')

            time_abnormal = []
            cache = []

            data_to_detect = data_to_plot[0]

            flag = data_to_detect.diff()
            flag = np.abs(flag)

            if station_[:2] == "光伏":
                flag = flag[(flag.index.time > datetime.time(7, 0)) & (flag.index.time < datetime.time(19, 0))]

            for row in flag.iterrows():

                if row[1][0] < 0.01:
                    cache.append(row[0])

                elif len(cache) > 8:
                    time_abnormal = time_abnormal + cache
                    cache = []

            pd.DataFrame(time_abnormal).to_csv('异常数据检测结果_吉林/'+station_+'_'+data_+'_'+'异常数据检测结果_吉林.txt', sep='\t', index=False, header=None)

            with open('异常数据检测结果_吉林/'+station_+'_'+data_+'_'+'异常数据检测结果_吉林.txt', 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(station_+data_+'数据包含%d个时刻，检测到%d个时刻数据异常，分别如下\n'%(len(data_to_detect),len(time_abnormal)) + content)

        except NameError:
            pass

class MyWindow_show_plot(QMainWindow, Ui_MainWindow_show_plot):
    def __init__(self, parent=None):
        super(MyWindow_show_plot, self).__init__(parent)
        self.setupUi(self)

import sys
if __name__ == '__main__':
    # 字体随分辨率自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyWindow_show_plot()
    myWin.show()

    sys.exit(app.exec_())