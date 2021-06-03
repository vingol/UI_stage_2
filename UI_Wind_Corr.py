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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from sklearn import preprocessing
import matplotlib

from show_cloudimage import Cloud_image, load_image, name_to_time, time_to_name_pkl, is_in_cloud, search_points, cloud_move

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, dpi=75):
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
        Location = np.array(
            [[36.9688, 106.2078], [36.662, 106.2263], [36.8413, 106.0225], [37.2548, 106.6315], [37.2176, 106.0225],
             [37.1006, 106.152]])
        ## 原始图像
        import matplotlib.pyplot as plt
        matplotlib.use('Agg')
        # fig, ax = plt.subplots(figsize=(10, 5))
        self.axes.scatter(Location[:, 0], Location[:, 1], label='Wind Farms', linewidth=2)
        self.axes.scatter(Location[:, 0] + 0.04, Location[:, 1] + 0.03, color=[], marker='o', edgecolors='#1f77b4',
                   s=300)  # 把 corlor 设置为空，通过edgecolors来控制颜色
        for i in range(Location.shape[0]):
            self.axes.text(Location[i, 0] + 0.0355, Location[i, 1] + 0.0225, str(i + 1), fontsize=11, weight='bold',
                    color='#1f77b4')
        font_label = {'family': 'Times New Roman','weight': 'normal','size' : 8,}

        self.axes.set(xlabel='Longitude(' + '$^{o}$' + ')', ylabel='Latitude(' + '$^{o}$' + ')')
        # plt.grid()
        # plt.show()
        self.axes.legend(loc='upper left')
        self.axes.tick_params(labelsize=8)
        self.axes.set_ylim([105.8,107])
        self.draw()
        # plt.savefig('Location.svg')

    def Plot_2(self, Location, Other_Farms, Farm_for_target, Final_Farm):

        self.axes.cla()
        ## 画完后的图像
        import matplotlib.pyplot as plt
        # fig, self.axes = plt.subplots(figsize=(10, 5))
        self.axes.scatter(Location[Other_Farms, 0], Location[Other_Farms, 1], label='Other Farms', linewidth=2)
        self.axes.scatter(Location[Other_Farms, 0] + 0.04, Location[Other_Farms, 1] + 0.03, color=[], marker='o',
                   edgecolors='#1f77b4', s=300)  # 把 corlor 设置为空，通过edgecolors来控制颜色
        for i in range(len(Other_Farms)):
            self.axes.text(Location[Other_Farms[i], 0] + 0.0355, Location[Other_Farms[i], 1] + 0.0225,
                    str(Other_Farms[i] + 1), fontsize=11, weight='bold', color='#1f77b4')

        self.axes.scatter(Location[Farm_for_target, 0], Location[Farm_for_target, 1], label='Targeted Farm', linewidth=2)
        self.axes.scatter(Location[Farm_for_target, 0] + 0.04, Location[Farm_for_target, 1] + 0.03, color=[], marker='o',
                   edgecolors='#ff7f0e', s=300)  # 把 corlor 设置为空，通过edgecolors来控制颜色
        self.axes.text(Location[Farm_for_target, 0] + 0.0355, Location[Farm_for_target, 1] + 0.0225,
                str(Farm_for_target + 1), fontsize=11, weight='bold', color='#ff7f0e')

        self.axes.scatter(Location[Final_Farm, 0], Location[Final_Farm, 1], label='Correlated Farm', linewidth=2)
        self.axes.scatter(Location[Final_Farm, 0] + 0.04, Location[Final_Farm, 1] + 0.03, color=[], marker='o',
                   edgecolors='#2ca02c', s=300)  # 把 corlor 设置为空，通过edgecolors来控制颜色
        self.axes.text(Location[Final_Farm, 0] + 0.0355, Location[Final_Farm, 1] + 0.0225, str(Final_Farm + 1),
                fontsize=11, weight='bold', color='#2ca02c')
        self.axes.set(xlabel='Longitude(' + '$^{o}$' + ')', ylabel='Latitude(' + '$^{o}$' + ')')
        # plt.grid()
        # plt.show()
        self.axes.legend(loc='upper left')
        self.axes.set_ylim([105.8, 107])
        # plt.savefig('Processed.svg')
        self.draw()

    def show_image(self, inputs):

        self.axes.cla()

        print('runnning show_image')

        im1, target, points, df_v = inputs

        print('im1:', im1.dst)
        print('target:', target)
        print('points:', points)
        print('df_v:', df_v)

        self.axes.imshow(im1.dst, cmap='gray')

        print('showed image theorically')

        self.axes.scatter(target[1], target[0], s=40, c='r', marker='*')

        for theta in points:
            self.axes.scatter(points[theta][1], points[theta][0], c='y', s=5)

            self.axes.arrow(points[theta][1], points[theta][0], df_v.loc[theta][1] * 20, df_v.loc[theta][0] * 20,
                      length_includes_head=True, color='r',
                      head_width=2, head_length=4, fc='#e87a59', ec='#e87a59')

        # ax1.set_xlabel('像素(500m)')
        # ax1.set_ylabel('像素(500m)')
        self.axes.set_xticks([])
        self.axes.set_yticks([])

        self.draw()


class Ui_MainWindow_wind_corr(object):
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
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.widget)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 10, 1), QtCore.QTime(0, 0, 0)))
        self.gridLayout.addWidget(self.dateTimeEdit, 0, 1, 1, 1)
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

        self.pushButton.clicked.connect(self.show_WindCorrelation)
        self.pushButton2.clicked.connect(self.WindCorrelation_EVA)


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
        self.label.setText(_translate("MainWindow", "风电关联模式分析"))
        self.label_2.setText(_translate("MainWindow", "参数设置"))
        self.pushButton.setText(_translate("MainWindow", "开始计算"))
        self.pushButton2.setText(_translate("MainWindow", "误差分析"))

        self.comboBox_station.setItemText(1, _translate("MainWindow", "风电1"))
        self.comboBox_station.setItemText(2, _translate("MainWindow", "风电6"))


        self.label_time.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">开始时间：</span></p></body></html>"))
        self.dateTimeEdit.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm"))
        self.label_station.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">选择电站：</span></p></body></html>"))
        # self.dateTimeEdit_end.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm-ss"))
        self.label_error1.setText(_translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Error_Lag：</span></p></body></html>"))
        self.label_error2.setText(_translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">Error_CrossCor：</span></p></body></html>"))


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

    def show_WindCorrelation(self):

        Time_Target = self.str_datetime(self.dateTimeEdit.text())  # 目标时刻点（认为是最近历史时刻）
        Farm_for_target = int(station_[2:]) - 1


        ### 各个风电场的位置关系
        Location = np.array(
            [[36.9688, 106.2078], [36.662, 106.2263], [36.8413, 106.0225], [37.2548, 106.6315], [37.2176, 106.0225],
             [37.1006, 106.152]])

        ### 时延相关系数
        def CrossCorr(Data_all, Farm_target, Farm_Proceed, Time, Period=30, Lag_Bound=15):
            ## 计算目标风电场Farm_target, 上下游风电场 Farm_Proceed 在目标时刻 Time， 时间窗Period下的互相关系数
            # Lag_Bound 是检测超前的时间上限
            Positive = np.zeros((Lag_Bound + 1, 2))  # 超前时间>=0 用正数表示，第一列是时间，第二列是相关系数
            Negative = np.zeros((Lag_Bound + 1, 2))  # 滞后时间<=0 用正数表示，第一列是时间，第二列是相关系数
            FarmT = Data_all[Farm_target]  # 目标电场
            FarmP = Data_all[Farm_Proceed]  # 上下游电场
            for lag in range(Lag_Bound + 1):
                Positive[lag, 0] = lag
                Positive[lag, 1] = np.corrcoef(FarmT.loc[Time - Period + 1: Time, 'WS'].values,
                                               FarmP.loc[Time - Period + 1 - lag: Time - lag, 'WS'].values,
                                               rowvar=False)[0, -1]
            Best_Lag = np.argmax(Positive[:, 1])

            for lag in range(Lag_Bound + 1):
                Negative[lag, 0] = -lag
                Negative[lag, 1] = np.corrcoef(FarmP.loc[Time - Period + 1: Time, 'WS'].values,
                                               FarmT.loc[Time - Period + 1 - lag: Time - lag, 'WS'].values,
                                               rowvar=False)[0, -1]

            return Positive, Negative, Best_Lag

        #####      外部输入参数      #####
        if Farm_for_target == 0: Farm_for_Proceed = [1, 2, 3, 5]  # 用于上下游检测的风电场编号
        if Farm_for_target == 5: Farm_for_Proceed = [0, 2, 3, 5]  # 用于上下游检测的风电场编号
        Other_Farms = list(range(6))
        del (Other_Farms[Farm_for_target])

        Period = 20  # 用于计算lag的时间窗

        f1 = open('data_wind_corr/Region_Dataforall.pkl', 'rb')
        Data_all = pickle.load(f1)
        f1.close()
        Time_range = Data_all[0]['Time']
        Time = Data_all[0][Data_all[0]['Time'] == Time_Target].index.tolist()[0]  # tolist是为了转化成为int型
        Best_of_Farms = np.zeros((len(Farm_for_Proceed), 2))  # 记录各个电场对应的最优提前量和对应的Lag，如果Lag是负值则直接忽略
        for i, farm in enumerate(Farm_for_Proceed):  # 计算各个电场最优的时延结果
            Positive, Negative, Best_Lag = CrossCorr(Data_all, Farm_for_target, farm, Time, Period, Lag_Bound=15)
            Best_of_Farms[i, :] = [Best_Lag, Positive[Best_Lag, 1]]

        Final_Farm = Farm_for_Proceed[np.argmax(Best_of_Farms[:, 1])]
        Final_Lag = Best_of_Farms[np.argmax(Best_of_Farms[:, 1]), 0]
        Final_Lag = Final_Lag.astype('int')
        Final_CrossCor = Best_of_Farms[np.argmax(Best_of_Farms[:, 1]), 1]

        Sheet = pd.DataFrame([[Final_Farm, Final_CrossCor, Final_Lag]], columns=['关联电场', '关联系数', '超前量'], index=['估计'])

        self.m.Plot_2(Location, Other_Farms, Farm_for_target, Final_Farm)

        self.show_table(Sheet)

    def WindCorrelation_EVA(self):
        ## 输入 #####
        Time_Target = self.str_datetime(self.dateTimeEdit.text())  # 目标时刻点（认为是最近历史时刻）
        Farm_for_target = int(station_[2:]) - 1

        # ------------------  主程序 --------------#
        ### 各个风电场的位置关系
        Location = np.array(
            [[36.9688, 106.2078], [36.662, 106.2263], [36.8413, 106.0225], [37.2548, 106.6315], [37.2176, 106.0225],
             [37.1006, 106.152]])

        ### 时延相关系数
        def CrossCorr(Data_all, Farm_target, Farm_Proceed, Time, Period=30, Lag_Bound=15):
            ## 计算目标风电场Farm_target, 上下游风电场 Farm_Proceed 在目标时刻 Time， 时间窗Period下的互相关系数
            # Lag_Bound 是检测超前的时间上限
            Positive = np.zeros((Lag_Bound + 1, 2))  # 超前时间>=0 用正数表示，第一列是时间，第二列是相关系数
            Negative = np.zeros((Lag_Bound + 1, 2))  # 滞后时间<=0 用正数表示，第一列是时间，第二列是相关系数
            FarmT = Data_all[Farm_target]  # 目标电场
            FarmP = Data_all[Farm_Proceed]  # 上下游电场
            for lag in range(Lag_Bound + 1):
                Positive[lag, 0] = lag
                Positive[lag, 1] = np.corrcoef(FarmT.loc[Time - Period + 1: Time, 'WS'].values,
                                               FarmP.loc[Time - Period + 1 - lag: Time - lag, 'WS'].values,
                                               rowvar=False)[0, -1]
            Best_Lag = np.argmax(Positive[:, 1])

            for lag in range(Lag_Bound + 1):
                Negative[lag, 0] = -lag
                Negative[lag, 1] = np.corrcoef(FarmP.loc[Time - Period + 1: Time, 'WS'].values,
                                               FarmT.loc[Time - Period + 1 - lag: Time - lag, 'WS'].values,
                                               rowvar=False)[0, -1]

            return Positive, Negative, Best_Lag

        #####      外部输入参数      #####
        if Farm_for_target == 0: Farm_for_Proceed = [1, 2, 3, 5]  # 用于上下游检测的风电场编号
        if Farm_for_target == 5: Farm_for_Proceed = [0, 2, 3, 5]  # 用于上下游检测的风电场编号
        Other_Farms = list(range(6))
        del (Other_Farms[Farm_for_target])

        Period = 20  # 用于计算lag的时间窗

        f1 = open('data_wind_corr/Region_Dataforall.pkl', 'rb')
        Data_all = pickle.load(f1)
        Time_range = Data_all[0]['Time']
        Time = Data_all[0][Data_all[0]['Time'] == Time_Target].index.tolist()[0]  # tolist是为了转化成为int型
        Best_of_Farms = np.zeros((len(Farm_for_Proceed), 2))  # 记录各个电场对应的最优提前量和对应的Lag，如果Lag是负值则直接忽略
        for i, farm in enumerate(Farm_for_Proceed):  # 计算各个电场最优的时延结果
            Positive, Negative, Best_Lag = CrossCorr(Data_all, Farm_for_target, farm, Time, Period, Lag_Bound=15)
            Best_of_Farms[i, :] = [Best_Lag, Positive[Best_Lag, 1]]

        Final_Farm = Farm_for_Proceed[np.argmax(Best_of_Farms[:, 1])]
        Final_Lag = Best_of_Farms[np.argmax(Best_of_Farms[:, 1]), 0]
        Final_Lag = Final_Lag.astype('int')
        Final_CrossCor = Best_of_Farms[np.argmax(Best_of_Farms[:, 1]), 1]
        # if Final_CrossCor < 0.2:  # 如果相关系数过于小
        #     Final_Lag = -1

        ## 自动触发后的误差评估环节 ##
        Real_CrossCor, _, Real_Lag = CrossCorr(Data_all, Farm_for_target, Final_Farm, Time + 6, Period=30, Lag_Bound=15)
        Real_CrossCor = Real_CrossCor[Real_Lag, 1]
        if Real_CrossCor < 0.2:  # 如果相关系数过于小
            Real_Lag = -1
            # if Final_CrossCor < 0.2:  # 假如原有系数判断也是对的
            #     Real_CrossCor = Final_CrossCor
        ### 输出 ###
        Error_Lag = Final_Lag - Real_Lag  # 预计的提前时间减去真实的提前时间
        Error_CrossCor = abs(Final_CrossCor - Real_CrossCor)  # 相关系数的相对误差（相对真实的系数结果）
        Error_CrossCor = format(Error_CrossCor, '.3f')

        Sheet = pd.DataFrame(np.array([[Final_Farm, Final_CrossCor, Final_Lag], [Final_Farm, Real_CrossCor, Real_Lag]]),
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




class MyWindow_wind_corr(QMainWindow, Ui_MainWindow_wind_corr):
    def __init__(self, parent=None):
        super(MyWindow_wind_corr, self).__init__(parent)
        self.setupUi(self)

import sys
if __name__ == '__main__':
    # 字体随分辨率自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyWindow_wind_corr()
    myWin.show()

    sys.exit(app.exec_())