# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forecast_QT_new.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import math
from sklearn.metrics import mean_squared_error as mse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import xcy
import matlab
from datetime import timedelta
import scipy.io as scio
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import datetime
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']

mpl.rcParams['axes.unicode_minus'] = False
# from main_cs import main_cs

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.15, bottom=0.2, right=0.9, top=0.9, hspace=0, wspace=0)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.init_plot()#打开App时可以初始化图片
        # self.plot()

    def plot_figure(self, Y_toplot, pred_toplot, time_horizen , CAP_):

        self.axes.cla()

        dates = Y_toplot.index
        m1 = pd.DataFrame(Y_toplot.values.flatten(), index=dates+datetime.timedelta(minutes=15*(time_horizen - 1)))
        m2 = pd.DataFrame(pred_toplot.values.flatten(), index=dates+datetime.timedelta(minutes=15*(time_horizen - 1)))

        self.axes.plot(m1, label='实际值')
        self.axes.plot(m2, label='预测值')
        self.axes.legend()  # 显示上面的label

        # data_plot = pd.DataFrame({'实际值':Y_toplot, '预测值':pred_toplot})
        # data_plot.plot(ax=self.axes)
        self.axes.set_ylabel('功率(MW)')
        # self.axes.set_ylim([0,CAP_])
        self.axes.set_xlabel('时间')
        self.axes.tick_params(axis='both', which='major', labelsize=8, rotation=45)
        num2str={1:"15min", 2:"30min", 3:"45min",4:"1h",5:"1h15min",6:"1h30min",7:"1h45min",8:"2h",
                   9:"2h15min",10:"2h30min",11:"2h45min",12:"3h",13:"3h15min",14:"3h30min",15:"3h45min",
                   16:"4h"}
        time_str = num2str[time_horizen]
        # self.axes.set_title(time_str+'时间尺度预测结果',fontsize=10,color='r') #r: red
        self.axes.set_title(station_[:2] + '电站' + station_[2:] + '提前' + time_str + '多场景预测结果', fontsize=10, color='r')
        self.draw()

    def plot_single(self, data_to_plot, start_time, CAP_):
        self.axes.cla()
        data_to_plot.plot(ax=self.axes)
        #
        # plt.plot(data_to_plot.index, data_to_plot.values[:,0], label='1')
        # plt.plot(data_to_plot.index, data_to_plot.values[:, 1], label='1')

        # 横坐标
        x_ticks_ = pd.date_range(start=start_time, periods=16, freq='15min')
        x_ticks_ = list(map(lambda x: str(x)[:-3], x_ticks_.time))
        self.axes.set_xlim([0, 16])
        self.axes.set_xticks(range(0, 16, 1))
        self.axes.set_xticklabels(x_ticks_, rotation=45, fontsize=6)

        # self.axes.set_ylim([0, 35])

        # 图例
        # self.axes.legend([start_time.split(' ')[0]], frameon=True)
        self.axes.legend()

        # 纵轴
        self.axes.set_ylabel('功率(MW)')
        self.axes.set_xlabel('时间')
        # self.axes.set_ylim([0, CAP_])
        # self.axes.set_ylim([0,])

        # self.axes.set_title('风电功率预测结果', fontsize=10, color='r')  # r: red
        self.axes.set_title(station_single[:2] + '电站' + station_single[2:] + '单场景预测结果', fontsize=10, color='r')
        self.draw()

    def update_figure(self, data1, data2, time_horizen, start_time, n, CAP_):
        self.axes.cla()
        #        data1.loc[start_time:end_time].plot(ax=self.axes)
        #        data2.loc[start_time:end_time].plot(ax=self.axes)
        #        data = np.concatenate((data1,data2),axis=1)
        #        data = pd.DataFrame(data,columns=['实际值','预测值'])
        #        data2 = pd.DataFrame(data2)
        #        data.plot(ax=self.axes)
        dates = pd.date_range(start=start_time, periods=n, freq='15min')
        m1 = pd.DataFrame(data1.flatten(), index=dates)
        m2 = pd.DataFrame(data2.flatten(), index=dates)

        self.axes.plot(m1, label='实际值')
        self.axes.plot(m2, label='预测值')
        self.axes.legend()  # 显示上面的label
        self.axes.set_ylabel('功率(MW)')
        self.axes.tick_params(axis='both', which='major', labelsize=8, rotation=45)
        self.axes.set_xlabel('时间')
        self.axes.set_ylim([0, CAP_])

        # x_ticks = pd.date_range(start=start_time, periods=12, freq='2h')
        # x_ticks_ = list(map(lambda x: str(x)[:-3], x_ticks.time))
        # self.axes.set_xlim([0, 96])
        # self.axes.set_xticks(range(0, 96, 8))
        # self.axes.set_xticklabels(x_ticks_, fontsize=6, rotation=45)

        #        self.axes.set_ylabel('功率(MW)')
        num2str = {1: "15min", 2: "30min", 3: "45min", 4: "1h", 5: "1h15min", 6: "1h30min", 7: "1h45min", 8: "2h",
                   9: "2h15min", 10: "2h30min", 11: "2h45min", 12: "3h", 13: "3h15min", 14: "3h30min", 15: "3h45min",
                   16: "4h"}
        time_str = num2str[time_horizen]
        # self.axes.set_title(time_str + '预测结果', fontsize=10, color='r')  # r: red
        self.axes.set_title(station_[:2] + '电站' + station_[2:] + '提前' + time_str + '多场景预测结果', fontsize=10, color='r')
        self.draw()

    def scene_plot(self, data_plot_iter1, data_plot_iter2, start_time):
        counter = 1

        def start_timer():
            nonlocal counter
            global inputs
            counter += 1
            inputs = [counter, data_plot_iter1, data_plot_iter2, start_time]
            if counter >= 80:
                timer.stop()
                timer.deleteLater()

        timer = QTimer(self)
        print('timer start')
        timer.timeout.connect(start_timer)
        timer.timeout.connect(lambda: self.scene_update_figure(inputs))
        timer.start(1000)

    def scene_update_figure(self, inputs):
        self.axes.cla()
        counter, data_plot_iter1, data_plot_iter2, start_time = inputs[0], inputs[1], inputs[2], inputs[3]
        temp1 = data_plot_iter1[:counter + 16].reshape(-1, 1)
        temp2 = data_plot_iter1[:counter].reshape(-1, 1)
        temp3 = data_plot_iter2[counter, :].reshape(-1, 1)
        temp4 = np.concatenate((temp2, temp3), axis=0)
        temp = np.concatenate((temp1, temp4), axis=1)
        data_plot_iter = pd.DataFrame(temp)
        data_plot_iter1 = pd.DataFrame(temp1)
        data_plot_iter2 = pd.DataFrame(temp4)
        data_plot_iter1.columns = ['实际值']
        data_plot_iter2.columns = ['预测值']
        data_plot_iter2[counter - 1:counter + 16].plot(ax=self.axes)
        data_plot_iter1[:counter].plot(ax=self.axes)
        #        data_plot_iter.columns=['实际值','预测值']
        #        data_plot_iter[:counter+16].plot(ax=self.axes)

        # 横坐标
        x_ticks = pd.date_range(start=start_time, periods=12, freq='2h')
        x_ticks_ = list(map(lambda x: str(x)[:-3], x_ticks.time))
        self.axes.set_xlim([0, 96])
        self.axes.set_xticks(range(0, 96, 8))
        self.axes.set_xticklabels(x_ticks_, fontsize=6, rotation=45)

        # 图例
        self.axes.legend()
        #        self.axes.legend([start_time.split(' ')[0]], frameon=True)

        # 纵轴
        self.axes.set_ylabel('功率(MW)')
        self.axes.set_title(start_time.split(' ')[0], fontsize=10, color='r')  # r: red
        self.draw()

class Ui_MainWindow_forecast(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 40, 879, 3))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 0, 681, 31))
        self.label.setObjectName("label")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(20, 50, 411, 33))
        self.label_25.setObjectName("label_25")
        # self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        # self.graphicsView.setGeometry(QtCore.QRect(20, 120, 401, 331))
        # self.graphicsView.setMinimumSize(QtCore.QSize(401, 331))
        # self.graphicsView.setMaximumSize(QtCore.QSize(401, 331))
        # self.graphicsView.setObjectName("graphicsView")

        self.m = PlotCanvas(self, width=4, height=3.5)  # 实例化一个画布对象
        self.m.move(20, 120)

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(460, 80, 311, 429))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_26 = QtWidgets.QLabel(self.widget)
        self.label_26.setObjectName("label_26")
        self.gridLayout_2.addWidget(self.label_26, 0, 0, 1, 1)
        self.dateTimeEdit_9 = QtWidgets.QDateTimeEdit(self.widget)
        self.dateTimeEdit_9.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 2, 1), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit_9.setObjectName("dateTimeEdit_9")
        self.gridLayout_2.addWidget(self.dateTimeEdit_9, 0, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.widget)
        self.label_27.setObjectName("label_27")
        self.gridLayout_2.addWidget(self.label_27, 1, 0, 1, 1)
        self.dateTimeEdit_10 = QtWidgets.QDateTimeEdit(self.widget)
        self.dateTimeEdit_10.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 3, 1), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit_10.setObjectName("dateTimeEdit_10")
        self.gridLayout_2.addWidget(self.dateTimeEdit_10, 1, 1, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.widget)
        self.label_29.setObjectName("label_29")
        self.gridLayout_2.addWidget(self.label_29, 2, 0, 1, 1)
        self.comboBox_station = QtWidgets.QComboBox(self.widget)
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
        self.gridLayout_2.addWidget(self.comboBox_station, 2, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.widget)
        self.label_30.setObjectName("label_30")
        self.gridLayout_2.addWidget(self.label_30, 3, 0, 1, 1)
        self.comboBox_9 = QtWidgets.QComboBox(self.widget)
        self.comboBox_9.setObjectName("comboBox_9")
        self.comboBox_9.addItem("")
        self.comboBox_9.setItemText(0, "")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_9, 3, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.widget)
        self.label_24.setObjectName("label_24")
        self.gridLayout_2.addWidget(self.label_24, 4, 0, 1, 1)
        self.comboBox_8 = QtWidgets.QComboBox(self.widget)
        self.comboBox_8.setObjectName("comboBox_8")
        self.comboBox_8.addItem("")
        self.comboBox_8.setItemText(0, "")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_8, 4, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 5, 0, 1, 2)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_28 = QtWidgets.QLabel(self.widget1)
        self.label_28.setObjectName("label_28")
        self.gridLayout_3.addWidget(self.label_28, 0, 0, 1, 1)
        self.dateTimeEdit_11 = QtWidgets.QDateTimeEdit(self.widget1)
        self.dateTimeEdit_11.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 2, 1), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit_11.setObjectName("dateTimeEdit_11")
        self.gridLayout_3.addWidget(self.dateTimeEdit_11, 0, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.widget1)
        self.label_31.setObjectName("label_31")
        self.gridLayout_3.addWidget(self.label_31, 1, 0, 1, 1)
        self.comboBox_station_2 = QtWidgets.QComboBox(self.widget1)
        self.comboBox_station_2.setObjectName("comboBox_station_2")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.setItemText(0, "")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.comboBox_station_2.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_station_2, 1, 1, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.widget1)
        self.label_32.setObjectName("label_32")
        self.gridLayout_3.addWidget(self.label_32, 2, 0, 1, 1)
        self.comboBox_10 = QtWidgets.QComboBox(self.widget1)
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_10.addItem("")
        self.comboBox_10.setItemText(0, "")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_10, 2, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.pushButton_3, 3, 0, 1, 2)
        self.widget2 = QtWidgets.QWidget(self.splitter)
        self.widget2.setObjectName("widget2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.widget2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 3, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget2)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget2)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget2)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.comboBox_8.currentIndexChanged[str].connect(
            self.get_time_horizen)  # 条目发生改变，发射信号，传递条目内容

        self.comboBox_9.currentIndexChanged[str].connect(
            self.get_forecast_method_1)  # 条目发生改变，发射信号，传递条目内容

        self.comboBox_10.currentIndexChanged[str].connect(
            self.get_forecast_method_2)  # 条目发生改变，发射信号，传递条目内容

        self.comboBox_station.currentIndexChanged[str].connect(
            self.get_station_name)  # 条目发生改变，发射信号，传递条目内容

        self.comboBox_station_2.currentIndexChanged[str].connect(
            self.get_station_name_single)  # 条目发生改变，发射信号，传递条目内容

        # self.pushButton_2.clicked.connect(hello)

        self.pushButton_2.clicked.connect(self.prediction)
        self.pushButton_3.clicked.connect(self.scene_forecast_iter)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'等线\'; font-size:24pt; color:#000000;\">风电超短期功率预测结果统计</span></p><p><br/></p></body></html>"))
        self.label_25.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt;\">功率预测曲线</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "                   数值"))
        self.label_4.setText(_translate("MainWindow", "均方根误差/MW"))
        self.label_6.setText(_translate("MainWindow", "     准确率%"))
        self.label_5.setText(_translate("MainWindow", "      合格率%"))
        self.label_2.setText(_translate("MainWindow", "         指标"))
        self.label_29.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">选择电站：</span></p></body></html>"))
        self.label_30.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">选择预测方法：</span></p></body></html>"))
        self.label_24.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">选择预测时间尺度：</span></p></body></html>"))
        self.dateTimeEdit_10.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm-ss"))
        self.label_27.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">截止时间：</span></p></body></html>"))
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
        self.comboBox_station.setItemText(21, _translate("MainWindow", "集群预测"))
        self.comboBox_station.setItemText(22, _translate("MainWindow", "光伏502"))
        self.comboBox_station.setItemText(23, _translate("MainWindow", "光伏503"))
        self.comboBox_station.setItemText(24, _translate("MainWindow", "光伏504"))
        self.comboBox_station.setItemText(25, _translate("MainWindow", "光伏505"))
        self.comboBox_station.setItemText(26, _translate("MainWindow", "光伏506"))
        self.comboBox_station.setItemText(27, _translate("MainWindow", "光伏507"))
        self.comboBox_station.setItemText(28, _translate("MainWindow", "光伏508"))
        self.comboBox_station.setItemText(29, _translate("MainWindow", "光伏509"))
        self.comboBox_station.setItemText(30, _translate("MainWindow", "光伏510"))
        self.comboBox_station.setItemText(31, _translate("MainWindow", "光伏511"))
        self.comboBox_station.setItemText(32, _translate("MainWindow", "光伏512"))
        self.comboBox_station.setItemText(33, _translate("MainWindow", "光伏513"))
        self.comboBox_station.setItemText(34, _translate("MainWindow", "光伏514"))
        self.comboBox_station.setItemText(35, _translate("MainWindow", "光伏515"))
        self.comboBox_station.setItemText(36, _translate("MainWindow", "光伏516"))
        self.comboBox_station.setItemText(37, _translate("MainWindow", "光伏517"))
        self.comboBox_station.setItemText(38, _translate("MainWindow", "光伏518"))
        self.comboBox_station.setItemText(39, _translate("MainWindow", "光伏519"))
        self.comboBox_station.setItemText(40, _translate("MainWindow", "光伏520"))
        self.comboBox_station.setItemText(41, _translate("MainWindow", "光伏521"))
        self.comboBox_9.setItemText(1, _translate("MainWindow", "GCN"))
        self.comboBox_9.setItemText(2, _translate("MainWindow", "ELM"))
        self.comboBox_8.setItemText(1, _translate("MainWindow", "15min"))
        self.comboBox_8.setItemText(2, _translate("MainWindow", "30min"))
        self.comboBox_8.setItemText(3, _translate("MainWindow", "45min"))
        self.comboBox_8.setItemText(4, _translate("MainWindow", "1h"))
        self.comboBox_8.setItemText(5, _translate("MainWindow", "1h15min"))
        self.comboBox_8.setItemText(6, _translate("MainWindow", "1h30min"))
        self.comboBox_8.setItemText(7, _translate("MainWindow", "1h45min"))
        self.comboBox_8.setItemText(8, _translate("MainWindow", "2h"))
        self.comboBox_8.setItemText(9, _translate("MainWindow", "2h15min"))
        self.comboBox_8.setItemText(10, _translate("MainWindow", "2h30min"))
        self.comboBox_8.setItemText(11, _translate("MainWindow", "2h45min"))
        self.comboBox_8.setItemText(12, _translate("MainWindow", "3h"))
        self.comboBox_8.setItemText(13, _translate("MainWindow", "3h15min"))
        self.comboBox_8.setItemText(14, _translate("MainWindow", "3h30min"))
        self.comboBox_8.setItemText(15, _translate("MainWindow", "3h45min"))
        self.comboBox_8.setItemText(16, _translate("MainWindow", "4h"))
        self.label_26.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">开始时间：</span></p></body></html>"))
        self.dateTimeEdit_9.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm-ss"))
        self.pushButton_2.setText(_translate("MainWindow", "显示多场景结果"))
        self.label_28.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">开始时间：</span></p></body></html>"))
        self.comboBox_10.setItemText(1, _translate("MainWindow", "GCN"))
        self.comboBox_10.setItemText(2, _translate("MainWindow", "ELM"))
        self.label_32.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">选择预测方法：</span></p></body></html>"))
        self.comboBox_station_2.setItemText(1, _translate("MainWindow", "风电1"))
        self.comboBox_station_2.setItemText(2, _translate("MainWindow", "风电2"))
        self.comboBox_station_2.setItemText(3, _translate("MainWindow", "风电3"))
        self.comboBox_station_2.setItemText(4, _translate("MainWindow", "风电4"))
        self.comboBox_station_2.setItemText(5, _translate("MainWindow", "风电5"))
        self.comboBox_station_2.setItemText(6, _translate("MainWindow", "风电6"))
        self.comboBox_station_2.setItemText(7, _translate("MainWindow", "风电7"))
        self.comboBox_station_2.setItemText(8, _translate("MainWindow", "风电8"))
        self.comboBox_station_2.setItemText(9, _translate("MainWindow", "风电9"))
        self.comboBox_station_2.setItemText(10, _translate("MainWindow", "风电10"))
        self.comboBox_station_2.setItemText(11, _translate("MainWindow", "风电11"))
        self.comboBox_station_2.setItemText(12, _translate("MainWindow", "风电12"))
        self.comboBox_station_2.setItemText(13, _translate("MainWindow", "风电13"))
        self.comboBox_station_2.setItemText(14, _translate("MainWindow", "风电14"))
        self.comboBox_station_2.setItemText(15, _translate("MainWindow", "风电15"))
        self.comboBox_station_2.setItemText(16, _translate("MainWindow", "风电16"))
        self.comboBox_station_2.setItemText(17, _translate("MainWindow", "风电17"))
        self.comboBox_station_2.setItemText(18, _translate("MainWindow", "风电18"))
        self.comboBox_station_2.setItemText(19, _translate("MainWindow", "风电19"))
        self.comboBox_station_2.setItemText(20, _translate("MainWindow", "风电20"))
        self.comboBox_station_2.setItemText(21, _translate("MainWindow", "集群预测"))
        self.comboBox_station_2.setItemText(22, _translate("MainWindow", "光伏502"))
        self.comboBox_station_2.setItemText(23, _translate("MainWindow", "光伏503"))
        self.comboBox_station_2.setItemText(24, _translate("MainWindow", "光伏504"))
        self.comboBox_station_2.setItemText(25, _translate("MainWindow", "光伏505"))
        self.comboBox_station_2.setItemText(26, _translate("MainWindow", "光伏506"))
        self.comboBox_station_2.setItemText(27, _translate("MainWindow", "光伏507"))
        self.comboBox_station_2.setItemText(28, _translate("MainWindow", "光伏508"))
        self.comboBox_station_2.setItemText(29, _translate("MainWindow", "光伏509"))
        self.comboBox_station_2.setItemText(30, _translate("MainWindow", "光伏510"))
        self.comboBox_station_2.setItemText(31, _translate("MainWindow", "光伏511"))
        self.comboBox_station_2.setItemText(32, _translate("MainWindow", "光伏512"))
        self.comboBox_station_2.setItemText(33, _translate("MainWindow", "光伏513"))
        self.comboBox_station_2.setItemText(34, _translate("MainWindow", "光伏514"))
        self.comboBox_station_2.setItemText(35, _translate("MainWindow", "光伏515"))
        self.comboBox_station_2.setItemText(36, _translate("MainWindow", "光伏516"))
        self.comboBox_station_2.setItemText(37, _translate("MainWindow", "光伏517"))
        self.comboBox_station_2.setItemText(38, _translate("MainWindow", "光伏518"))
        self.comboBox_station_2.setItemText(39, _translate("MainWindow", "光伏519"))
        self.comboBox_station_2.setItemText(40, _translate("MainWindow", "光伏520"))
        self.comboBox_station_2.setItemText(41, _translate("MainWindow", "光伏521"))
        self.label_31.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">选择电站：</span></p></body></html>"))
        self.dateTimeEdit_11.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm-ss"))
        self.pushButton_3.setText(_translate("MainWindow", "显示单场景结果"))

    def get_time_horizen(self, i):
        # 获取数据类型
        global time_horizen_
        time_horizen_ = i

    def get_forecast_method_1(self, i):
        # 获取数据类型
        global forecast_method_1
        forecast_method_1= i

    def get_forecast_method_2(self, i):
        # 获取数据类型
        global forecast_method_2
        forecast_method_2 = i


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

    def get_station_name(self, i):
        # 获取电站类型
        global station_
        station_ = i

    def get_station_name_single(self, i):
        # 获取电站类型
        global station_single
        station_single = i

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


    def prediction(self, MainWindow):
        if station_ != "集群预测":
            global df_wind_power, cappseries
            Power = scio.loadmat("extra_data/wind_power_19.mat")
            df_wind_power = pd.DataFrame(Power['Power'])
            df_wind_power.index = pd.date_range(start='2019-01-01', periods=len(df_wind_power[0]), freq='15min')

            print(df_wind_power.shape)

            capp = scio.loadmat("extra_data/wind_power_cap.mat")
            capp1 = capp['capp']
            cappseries = matlab.double(capp['capp'].tolist())

            str2num = {"15min": 1, "30min": 2, "45min": 3, "1h": 4, "1h15min": 5, "1h30min": 6, "1h45min": 7, "2h": 8,
                       "2h15min": 9, "2h30min": 10, "2h45min": 11, "3h": 12, "3h15min": 13, "3h30min": 14, "3h45min": 15,
                       "4h": 16}

            #        time_horizen_ = '1'
            print(time_horizen_)
            time_horizen = str2num[time_horizen_]
            #        time_horizen = 1
            print("time_horizen:", time_horizen)

            start_time = self.dateTimeEdit_start1.text()
            end_time = self.dateTimeEdit_end.text()

            # set train data and train
            train_start = pd.to_datetime(str(start_time)) + timedelta(days=-60)
            train_start = train_start + timedelta(hours=-4)
            train_end = pd.to_datetime(str(end_time))
            train_end = train_end
            wind_power_train = df_wind_power.loc[train_start:train_end]
            predict_start = pd.to_datetime(str(start_time))
            predict_end = pd.to_datetime(str(end_time))
            #        wind_power_predict = df_wind_power.loc[predict_start + timedelta(minutes=15*(time_horizen-1)):predict_end + timedelta(minutes=15*(time_horizen-2))]
            wind_power_predict = df_wind_power.loc[predict_start:predict_end + timedelta(minutes=-15)]
            wind_power_predict = np.array(wind_power_predict)
            n = len(wind_power_predict)
            print(wind_power_predict.shape)
            station_num = int(station_[2:]) - 1
            print("场站号:", station_num + 1)
            wind_power_predict_13 = df_wind_power.loc[
                                    predict_start + timedelta(minutes=15 * (13 - 1)):predict_end + timedelta(
                                        minutes=15 * (13 - 2))]
            wind_power_predict_13 = np.array(wind_power_predict_13)
            wind_power_predict_14 = df_wind_power.loc[
                                    predict_start + timedelta(minutes=15 * (14 - 1)):predict_end + timedelta(
                                        minutes=15 * (14 - 2))]
            wind_power_predict_14 = np.array(wind_power_predict_14)
            wind_power_predict_15 = df_wind_power.loc[
                                    predict_start + timedelta(minutes=15 * (15 - 1)):predict_end + timedelta(
                                        minutes=15 * (15 - 2))]
            wind_power_predict_15 = np.array(wind_power_predict_15)
            wind_power_predict_16 = df_wind_power.loc[
                                    predict_start + timedelta(minutes=15 * (16 - 1)):predict_end + timedelta(
                                        minutes=15 * (16 - 2))]
            wind_power_predict_16 = np.array(wind_power_predict_16)

            wind_power_predict_4th_hour = np.concatenate((wind_power_predict_13[:, station_num].reshape(-1, 1),
                                                          wind_power_predict_14[:, station_num].reshape(-1, 1)), axis=1)
            wind_power_predict_4th_hour = np.concatenate(
                (wind_power_predict_4th_hour, wind_power_predict_15[:, station_num].reshape(-1, 1)), axis=1)
            wind_power_predict_4th_hour = np.concatenate(
                (wind_power_predict_4th_hour, wind_power_predict_16[:, station_num].reshape(-1, 1)), axis=1)
            print(wind_power_predict_4th_hour.shape)
            time_delta_train = 20
            time_delta_predict = predict_end - train_end
            wind_power_train = np.array(wind_power_train)
            print(wind_power_train.shape)
            wind_power_train = wind_power_train[:, station_num]
            wind_power_train = wind_power_train.reshape(len(wind_power_train), 1)
            print(wind_power_train.shape)
            wind_train_matlab = matlab.double((wind_power_train).tolist())

            capacity = capp1[station_num, 0]

            a = xcy.initialize()
            jieguo = a.xcy(
                wind_train_matlab, int(capacity), 30, n + 16)
            a.terminate()

            #        jieguo = np.array(jieguo)
            #        jieguo = pd.read_excel(r'C:\Wind Power Prediction Program\UI_design\df_jieguo.xlsx')
            jieguo = np.array(jieguo)
            print(jieguo.shape)

            wucha1 = np.zeros((n, 1))
            wucha2 = np.zeros((n, 1))
            wucha3 = np.zeros((n, 1))

            df_jieguo = pd.DataFrame(jieguo)
            df_jieguo.index = pd.date_range(start=predict_start + timedelta(hours=-4), periods=len(jieguo), freq='15min')

            #        np.save('jieguo.npy',df_jieguo)
            df_jieguo.to_csv(r'extra_data/df_jieguo_fh.csv')

            print('风电场容量:', capacity)
            #        for i in range(n):
            #            wucha1[i,0] = np.sqrt(mean_squared_error(wind_power_predict_4th_hour[i,:]/capacity, jieguo[i+16,12:16]/capacity))

            #        wind_power_predict_4th_hour = np.mean(wucha1)
            #        for i in range(n):

            wucha1 = np.sqrt(mean_squared_error(wind_power_predict[:, station_num] / capacity,
                                                jieguo[17 - time_horizen:17 - time_horizen + n,
                                                time_horizen - 1] / capacity))
            wind_power_predict_4th_hour = wucha1

            wind_power_predict_16 = wind_power_predict_16[:, station_num].reshape(-1, 1)
            for i in range(n):
                temp = 1 - np.abs(wind_power_predict[i, station_num] / capacity - jieguo[
                    16 + i - time_horizen, time_horizen - 1] / capacity)
                if temp > 0.75:
                    wucha2[i, 0] = 1
                else:
                    wucha2[i, 0] = 0

            hegelv = np.mean(wucha2)

            accuracy = 1 - mean_squared_error(wind_power_predict_16 / capacity, jieguo[16:, 15] / capacity)

            print(wind_power_predict_16.shape)
            print(jieguo[:, 15].shape)
            print(wind_power_predict.shape)
            m1 = len(jieguo[:, 15])
            print(jieguo[16 - time_horizen:m1 - time_horizen, time_horizen - 1].shape)

            # self.m.update_figure(wind_power_predict[:, station_num].reshape(-1, 1),
            #                      jieguo[17 - time_horizen:m1 - time_horizen, time_horizen - 1].reshape(-1, 1), time_horizen,
            #                      start_time,
            #                      n,
            #                      capacity)
            self.m.update_figure(wind_power_predict[:, station_num].reshape(-1, 1),
                                 jieguo[17 - time_horizen:m1 - time_horizen + 1, time_horizen - 1].reshape(-1, 1),
                                 time_horizen, start_time,
                                 n,
                                 capacity)
            # self.m.update_figure(wind_power_predict[:, station_num].reshape(-1, 1),
            #                      jieguo[16 : m1, time_horizen - 1].reshape(-1, 1), time_horizen, start_time,
            #                      n,
            #                      capacity)

            toplot_predict_test = wind_power_predict[:, station_num]
            # toplot_jieguo_test = jieguo[16 : m1, time_horizen - 1]
            toplot_jieguo_test = jieguo[17 - time_horizen:m1 - time_horizen + 1, time_horizen - 1]

            rmse = math.sqrt(mse(toplot_predict_test.reshape(-1), toplot_jieguo_test.reshape(-1)))

            Y_max = capacity
            accuracy = 1 - rmse / Y_max

            hege = [1 if (1 - (toplot_predict_test.reshape(-1)[i] - toplot_predict_test.reshape(-1)[i]) / Y_max) > 0.75 else 0 for i in range(len(toplot_predict_test.reshape(-1)))]
            hegelv = np.array(hege).sum() / len(hege)

            self.lineEdit.setText(str(rmse))
            self.lineEdit_2.setText(str(100 * hegelv))
            self.lineEdit_3.setText(str(100 * accuracy))



            #        df1 = pd.DataFrame(wind_power_predict)
            #        df2 = pd.DataFrame(jieguo)
            #        df1.index = pd.date_range(start='2017-03-11 00:00:00', periods=96, freq='15min')
            #        df2.index = pd.date_range(start='2017-03-11 00:00:00', periods=96, freq='15min')

            #        self.lineEdit.setText(str(100*wind_power_predict_4th_hour))self.lineEdit.setText(str(100*wind_power_predict_4th_hour))
            # self.lineEdit.setText(str(100 * wind_power_predict_4th_hour))
            # #        self.lineEdit.setText(str(100*mse_predict))
            # self.lineEdit_2.setText(str(100 * hegelv))
            # self.lineEdit_3.setText(str(100 * accuracy))

        else:

            # read data from UI
            str2num = {"15min": 1, "30min": 2, "45min": 3, "1h": 4, "1h15min": 5, "1h30min": 6, "1h45min": 7, "2h": 8,
                       "2h15min": 9, "2h30min": 10, "2h45min": 11, "3h": 12, "3h15min": 13, "3h30min": 14,
                       "3h45min": 15,
                       "4h": 16}

            #        time_horizen_ = '1'
            print(time_horizen_)
            time_horizen = str2num[time_horizen_]
            #        time_horizen = 1
            print("time_horizen:", time_horizen)

            start_time = self.dateTimeEdit_9.text()
            end_time = self.dateTimeEdit_10.text()

            start_time = str(self.str_datetime(start_time)-datetime.timedelta(minutes=15*(time_horizen - 1)))
            end_time = str(self.str_datetime(end_time)-datetime.timedelta(minutes=15*(time_horizen - 1)))

            # group_pred = pd.read_csv('extra_data/group_pred.csv', index_col=0, parse_dates=True)
            # group_real = pd.read_csv('extra_data/group_real.csv', index_col=0, parse_dates=True)

            # Y_toplot = group_real.loc[start_time:end_time, str(time_horizen - 1)]
            # pred_toplot = group_pred.loc[start_time:end_time, str(time_horizen - 1)]


            # group_pred = pd.read_csv('extra_data/pred_gcn_fh.csv', index_col=0, parse_dates=True)
            # group_real = pd.read_csv('extra_data/y_gcn_fh.csv', index_col=0, parse_dates=True)
            if forecast_method_1 == 'GCN':
                group_pred = pd.read_csv('extra_data/pred_gcn_fh.csv', index_col=0, parse_dates=True)
                group_real = pd.read_csv('extra_data/y_gcn_fh.csv', index_col=0, parse_dates=True)
            else:
                group_pred = pd.read_csv('extra_data/pred_elm.csv', index_col=0, parse_dates=True)
                group_real = pd.read_csv('extra_data/y_elm.csv', index_col=0, parse_dates=True)

            print('load sucess')

            Y_toplot = group_real.loc[start_time:end_time, str(time_horizen - 1)]
            pred_toplot = group_pred.loc[start_time:end_time, str(time_horizen - 1)]


            #TODO
            # rmse = math.sqrt(mse(Y_toplot, pred_toplot))
            rmse = np.sqrt(mse(group_real.loc[start_time:end_time, str(12):], group_pred.loc[start_time:end_time,str(12):]))
            caps = scio.loadmat('extra_data/wind_power_cap.mat')['capp']
            Y_max = caps.sum()
            # Y_max = 1800
            accuracy = 1 - rmse

            hege = [1 if (1 - (Y_toplot[i] - pred_toplot[i]) / Y_max) > 0.75 else 0 for i in range(len(Y_toplot))]
            hegelv = np.array(hege).sum() / len(hege)

            print('calculate finish')

            self.lineEdit.setText(str(rmse*Y_max))
            self.lineEdit_2.setText(str(100 * hegelv))
            self.lineEdit_3.setText(str(100 * accuracy))

            print('lineedit finish')

            self.m.plot_figure(Y_toplot*Y_max, pred_toplot*Y_max, time_horizen, Y_max)

    def scene_forecast_iter(self):
        if station_single != "集群预测":

            Power = scio.loadmat("extra_data/wind_power_19.mat")
            df_wind_power = pd.DataFrame(Power['Power'])
            df_wind_power.index = pd.date_range(start='2019-01-01', periods=len(df_wind_power[0]), freq='15min')

            # read data from UI
            str2num = {"15min": 1, "30min": 2, "45min": 3, "1h": 4, "1h15min": 5, "1h30min": 6, "1h45min": 7, "2h": 8,
                       "2h15min": 9, "2h30min": 10, "2h45min": 11, "3h": 12, "3h15min": 13, "3h30min": 14, "3h45min": 15,
                       "4h": 16}

            start_time = self.dateTimeEdit_11.text()

            start_time = self.str_datetime(start_time)

            #        Y_time_test = np.load('jieguo.npy')
            Y_predict = pd.read_csv(r'extra_data/df_jieguo_fh.csv', index_col=0)
            print(Y_predict.shape)
            #        Y_predict = pd.DataFrame(Y_predict)

            # process prediction result
            #        index_ = pd.to_datetime(Y_time_test[:, 0])

            #        result_Y = pd.DataFrame(Y_test, index=index_)
            #        result_pred = pd.DataFrame(pred, index=index_)

            #        Y_toplot = result_Y.loc[start_time:end_time,:]
            Y_toplot = df_wind_power.loc[start_time:start_time+datetime.timedelta(days=24), :]
            station_num = int(station_[2:]) - 1
            Y_toplot_station = pd.DataFrame(Y_toplot.iloc[0:96, station_num])

            # Y_toplot = np.array(Y_toplot)
            # Y_toplot = pd.DataFrame(Y_toplot)
            pred_toplot_ = Y_predict.loc[str(start_time):str(start_time+datetime.timedelta(days=24)), :]
            pred_toplot = pred_toplot_.iloc[0,:]
            #        pred_toplot = Y_predict.iloc[15,:].reshape(-1,1)
            print(Y_toplot.shape)


            print(pred_toplot.shape)

            #        Data = np.concatenate((Y_toplot,pred_toplot),axis=1)
            #        print(Data.shape)

            Y_tolpot_true = Y_toplot_station[:16].values.reshape(-1)
            pred_toplot_true = pred_toplot.values.reshape(-1)

            rmse = math.sqrt(mse(Y_tolpot_true, pred_toplot_true))

            caps = scio.loadmat('extra_data/wind_power_cap.mat')['capp']
            Y_max = caps[station_num]
            accuracy = 1 - rmse / Y_max

            hege = [1 if (1 - (Y_tolpot_true[i] - pred_toplot_true[i]) / Y_max) > 0.75 else 0 for i in range(len(pred_toplot_true))]
            hegelv = np.array(hege).sum() / len(hege)

            self.lineEdit.setText(str(rmse))
            self.lineEdit_2.setText(str(100 * hegelv))
            self.lineEdit_3.setText(str(100 * accuracy[0]))

            data_plot_iter = pd.DataFrame({'实际值': Y_toplot_station[:16].values.reshape(-1), '预测值': pred_toplot.values.reshape(-1)}, index=np.arange(1,17))
            # data_plot_iter.index = data_plot_iter.index + 1

            self.m.plot_single(data_plot_iter, start_time, Y_max)

            # self.m.scene_plot(data_plot_iter, start_time)
        else:
            # read data from UI
            start_time = self.dateTimeEdit_11.text()

            start_time = self.str_datetime(start_time)


            # group_pred = pd.read_csv('extra_data/group_pred.csv', index_col=0, parse_dates=True)
            # group_real = pd.read_csv('extra_data/group_real.csv', index_col=0, parse_dates=True)
            # group_pred = pd.read_csv('extra_data/pred_gcn_fh.csv', index_col=0, parse_dates=True)
            # group_real = pd.read_csv('extra_data/y_gcn_fh.csv', index_col=0, parse_dates=True)
            if forecast_method_2 == 'GCN':
                group_pred = pd.read_csv('extra_data/pred_gcn_fh.csv', index_col=0, parse_dates=True)
                group_real = pd.read_csv('extra_data/y_gcn_fh.csv', index_col=0, parse_dates=True)
            else:
                group_pred = pd.read_csv('extra_data/pred_elm.csv', index_col=0, parse_dates=True)
                group_real = pd.read_csv('extra_data/y_elm.csv', index_col=0, parse_dates=True)

            Y_toplot_ = group_real.loc[start_time:start_time + datetime.timedelta(minutes=15 * 20), :]
            pred_toplot_ = group_pred.loc[start_time:start_time + datetime.timedelta(minutes=15 * 20), :]



            print('load sucess')

            Y_toplot = Y_toplot_.iloc[0, :]
            pred_toplot = pred_toplot_.iloc[0, :]

            rmse = math.sqrt(mse(Y_toplot, pred_toplot))

            caps = scio.loadmat('extra_data/wind_power_cap.mat')['capp']
            Y_max = caps.sum()
            print(Y_max)
            # Y_max = 1800
            accuracy = 1 - rmse

            hege = [1 if (1 - (Y_toplot[i] - pred_toplot[i]) / Y_max) > 0.75 else 0 for i in range(len(Y_toplot))]
            hegelv = np.array(hege).sum() / len(hege)

            self.lineEdit.setText(str(rmse*Y_max))
            self.lineEdit_2.setText(str(100 * hegelv))
            self.lineEdit_3.setText(str(100 * accuracy))

            data_plot_iter = pd.DataFrame({'实际值': Y_toplot.values.reshape(-1), '预测值': pred_toplot.values.reshape(-1)}, index=np.arange(1,17,1))
            # data_plot_iter.index = data_plot_iter.index + 1

            self.m.plot_single(data_plot_iter*Y_max, start_time, Y_max)


