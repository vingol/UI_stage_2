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
matplotlib.use('Agg')
import pickle

plt.rcParams["font.family"]="SimHei"

from scipy.optimize import curve_fit
def Multi_gauss(x, *params):  #可以指定任意的gauss核项，其个数由P0初始迭代的guess项决定
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        ctr = params[i] #mean
        amp = params[i+1] #amplitude
        wid = params[i+2] #std
        y = y + amp * np.exp( -((x - ctr)/wid)**2)
    return y
def f_gauss(x, *params):  #单个的gauss函数
    y = np.zeros_like(x)
    ctr = params[0] #mean
    amp = params[1] #amplitude
    wid = params[2] #std
    y =  amp * np.exp( -((x - ctr)/wid)**2)
    return y
def local_search (y,i_begin): #这里只在寻找向上波动峰的过程
    begin = -1; local_max = -1; end = -1
    i = i_begin
    ## ----------------向左搜索-----------------
    while(i - 2 >= 0 and begin == -1):
        if i + 1 < y.shape[0]: #假如右边有界
            if (y[i- 1] < y[i] and y[i- 2]<y[i- 1]) and y[i] > y[i+1]:
                local_max = i
        else: #假如在边界上
            if y[i - 1] < y[i] and y[i - 2] < y[i - 1]:
                local_max = i
        if i + 1 <= y.shape[0]:  # 假如右边有界
            if y[i- 1] > y[i] and y[i- 2] > y[i- 1] and y[i] < y[i+1]:
                begin= i
        else:
            if y[i - 1] < y[i] and y[i - 2] < y[i - 1]:
                begin = i
        i = i - 1
    if begin == -1: #假如没有找到极小值，说明一定在边界上
        begin = 0
    ## ------------向右搜索-----------------
    i = i_begin
    if i + 2 >= y.shape[0]: #判断是不是在边上，如果在边上结束时间段就是 右侧边上
        end = y.shape[0]
    while (i + 2 < y.shape[0] and end == -1):
        if i - 1 >= 0:  # 假如左边有界
            if y[i - 1] < y[i] and y[i] > y[i + 1] and y[i + 1] > y[i+ 2]:
                local_max = i
        else:  # 假如在边界上
            if y[i] > y[i + 1] and y[i + 1] > y[i+ 2]:
                local_max = i
        if i - 1 >= 0:  # 假如左边有界
            if y[i - 1] > y[i] and y[i + 2] > y[i + 1] and y[i] < y[i + 1]:
                end = i
        else:
            if y[i + 2] > y[i + 1] and y[i] < y[i + 1]:
                end = i
        i = i + 1
    if end == -1: #假如没有找到右极小值，说明一定在边界上
        end = y.shape[0] - 1 #注意这里的end认为是能够取到的，因此最大是shape[0] - 1
    return [begin,local_max,end] #返回一个list 分别包括起始，最大值和终值值
def Gauss_Wave(y_temp, Time_in = range(500), alpha = 1.4 ): # 高斯函数对波动过程的识别
    ## y_temp: 默认为二阶矩阵，为np.array类型。
    ## Time_in: 真实数据中y_temp的时间值，默认为（0，y_temp.shape[0]）,其中Time_in[0]表示起始时刻

    import math
    from scipy.optimize import curve_fit
    if len(y_temp.shape) == 2:
        y = y_temp[Time_in, 0]  # 只对第一个时间尺度的y进行多维高斯混合
    else: y = y_temp[Time_in]
    x = np.array(range(y.shape[0]))  # x默认是从零开始的整数
    guess = []; up_bounds = []; down_bounds = []  # 保存多高斯模型的个数, 保存多维高斯的参数界
    core =math.floor(len(Time_in)/ 50)
    for i in range(core):  # range 决定了核的个数（通过设置初值的形式体现）
        guess += [y.shape[0] // core * i, 0.5, 20]  # 初始值均匀地分布在输入y方位上，初始幅值为0.5， 标准差为20
        up_bounds += [y.shape[0], 1, 60]  # 给出每个参数对应的估计值
        down_bounds += [0, 0, 0]  # 三个主要变量
    popt_origin,_ = curve_fit(Multi_gauss, x, y, p0=guess, bounds=(down_bounds, up_bounds)) #进行第一步多维高斯函数拟合，首先判断出潜在的波动分布
    Params_origin = popt_origin.reshape((-1, 3))  # 将高斯函数拟合的数据按照N*3的形式进行组装
    # Params_origin = np.append(Params_origin, np.ones((Params_origin.shape[0], 1)), axis=1)  # 给Params_power加上一项
    y_fit = Multi_gauss(x, *popt_origin)  # 混合高斯函数拟合结果
    # for i in range(core):  # range 决定了核的个数（通过设置初值的形式体现）
    #     Params_origin[i, 3] = y_fit[math.floor(Params_origin[i, 0])] - Params_origin[i, 1]  # 将低估的单高斯拟合函数与多高斯拟合函数在幅值上匹配

    dy_fit = y_fit[1:] - y_fit[:-1]
    U_local = [];  D_local = [];  wave_time = [[], []] #极大值，极小值，波动起止时刻
    wave_flag = 0 #波动过程的标志
    for t in range(1, dy_fit.shape[0]):
        if (dy_fit[t - 1] >= 0) & (dy_fit[t] <= 0):
            U_local.append(t - 1)  # 判断极大值点
            wave_flag += 1
        if (dy_fit[t - 1] <= 0) & (dy_fit[t] >= 0):
            D_local.append(t - 1)  # 判断极小值点
            if wave_flag == 1:  # 假如前面有一个极大值，需要进行波动区间分割
                wave_time[1].append(D_local[-1])  # 波动的结尾一定是当前的最小值点
                if len(D_local) < 2:
                    wave_time[0].append(0)  # 假如这是第一个极小值点
                else:
                    wave_time[0].append(D_local[-2])  # 假如这不是第一个极小值点
                wave_flag = 0
        if (wave_flag == 1) & (t == dy_fit.shape[0] - 1):  # 对于已经经过了最大值点并且即将到达片段的尾端
            wave_time[0].append(D_local[-1]);
            wave_time[1].append(y_fit.shape[0] - 1)  # 取上一个极小值点到此时的终点
    df_wave = pd.DataFrame(columns=['time', 'am', 'scale', 'ts', 'te'])
     # 表示默认峰值在均值附近多少方差之内： [Mu - alpha * sigma， Mu + alpha * sigma]
    for wave in range(len(wave_time[0])): #开始对部分片段进行划分并拟合
        time = np.arange(wave_time[0][wave], wave_time[1][wave] + 1)
        intial = [U_local[wave], y_fit[U_local[wave]], 20]  # 重新设置单高斯函数拟合值
        popt, _ = curve_fit(Multi_gauss, time, y_fit[time], p0=intial, bounds=((time[0], 0, 0), (time[-1], 1.2, 200)))
        df_wave.loc[df_wave.shape[0] + 1, ['time', 'am', 'scale']] = [popt[0] + Time_in[0], popt[1], popt[2]]
        df_wave.loc[df_wave.shape[0], ['ts', 'te']] = [max(math.floor(popt[0] - alpha * popt[2]), wave_time[0][wave]) + Time_in[0],
                                                       min(math.ceil(popt[0] + alpha * popt[2]), wave_time[1][wave]) + Time_in[0]]
    df_wave = df_wave.reset_index(drop=True)

    return df_wave, y_fit, popt_origin, Params_origin

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, dpi=75):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.1, bottom=0.25, right=0.9, top=0.9, hspace=0, wspace=0)
        self.axes = fig.add_subplot(111)
        # self.ax_twin = self.axes.twinx()
        # self.axes.axis('off')

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # self.axess.set_xticks([])
        # self.axes.set_yticks([])
        
    def show_plot_WP(self, df_wave,Line):
        self.axes.cla()
        # fig = plt.figure(figsize=(6,4))
        # ax= fig.add_subplot()
        Line.plot('Time', 'Series', label='NWP', linewidth=2.5 , ax=self.axes)
        for i in range(df_wave.shape[0]):
            Line[df_wave.loc[i,'ts'] -50 : df_wave.loc[i,'te']-50].plot('Time', 'Wave', label='波动过程'+str(i+1), linewidth=2, linestyle='-.', ax=self.axes)
            Line.loc[[df_wave.loc[i, 'ts'] - 50],:].plot('Time','T','scatter',linewidth=3, ax=self.axes, color = '#2ca02c')
            Line.loc[[df_wave.loc[i, 'te'] - 51],:].plot('Time','T','scatter',linewidth=3, ax=self.axes, color = '#d62728')
        Line.loc[[df_wave.loc[0, 'ts'] - 50],:].plot('Time','T','scatter',linewidth=3, ax=self.axes, color = '#2ca02c', label = '起始点')
        Line.loc[[df_wave.loc[0, 'te'] - 51], :].plot('Time', 'T', 'scatter', linewidth=3, ax=self.axes, color='#d62728', label = '终止点')
        self.axes.set(xlabel='时间 (15min)',ylabel='风速 (m/s)')
        self.axes.legend(loc='best')
        self.draw()


class Ui_MainWindow_wind_process(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(604, 433, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(55, 390, 391, 151))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(6)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 200)

        self.label_title_img = QtWidgets.QLabel(self.centralwidget)
        self.label_title_img.setGeometry(QtCore.QRect(150, 75, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_title_img.setFont(font)
        self.label_title_img.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_title_img.setTextFormat(QtCore.Qt.AutoText)
        self.label_title_img.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title_img.setObjectName("label_title_img")

        self.label_title_table = QtWidgets.QLabel(self.centralwidget)
        self.label_title_table.setGeometry(QtCore.QRect(150, 365, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_title_table.setFont(font)
        self.label_title_table.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_title_table.setTextFormat(QtCore.Qt.AutoText)
        self.label_title_table.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title_table.setObjectName("label_title_table")

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
        self.comboBox_station.addItem("")
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

        self.pushButton.clicked.connect(self.show_wind_process)

        self.comboBox_station.currentIndexChanged[str].connect(
            self.get_station_name)  # 条目发生改变，发射信号，传递条目内容

        self.label_error = QtWidgets.QLabel(self.centralwidget)
        self.label_error.setGeometry(QtCore.QRect(500, 500, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_error.setFont(font)
        self.label_error.setTextFormat(QtCore.Qt.AutoText)
        self.label_error.setAlignment(QtCore.Qt.AlignCenter)
        self.label_error.setObjectName("label_2")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(650, 500, 100, 31))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setAlignment(QtCore.Qt.AlignCenter)

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

        self.comboBox_station.setItemText(1, _translate("MainWindow", "风电1"))
        self.comboBox_station.setItemText(2, _translate("MainWindow", "风电2"))
        self.comboBox_station.setItemText(3, _translate("MainWindow", "风电3"))
        self.comboBox_station.setItemText(4, _translate("MainWindow", "风电4"))
        self.comboBox_station.setItemText(5, _translate("MainWindow", "风电5"))
        self.comboBox_station.setItemText(6, _translate("MainWindow", "风电6"))


        self.label_time.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">开始时间：</span></p></body></html>"))
        self.dateTimeEdit.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm"))
        self.label_station.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">选择电站：</span></p></body></html>"))
        self.label_error.setText(_translate("MainWindow",
                                              "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">提取误差：</span></p></body></html>"))

        # self.dateTimeEdit_end.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm-ss"))
        self.label_title_img.setText(_translate("MainWindow",
                                                "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">风过程提取结果</span></p></body></html>"))
        self.label_title_table.setText(_translate("MainWindow",
                                                  "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">风过程参数展示</span></p></body></html>"))

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

    def show_wind_process(self):

        print('正在提取风过程，请稍后...')

        try:
            Farm_for_target = int(station_[2:]) - 1
        except NameError:
            Farm_for_target = 0

        Time_Target = self.str_datetime(self.dateTimeEdit.text())  # 目标时刻点（认为是最近历史时刻）
          ## 只允许考虑两种风电场

        f1 = open('data_wind_corr/Region_Dataforall.pkl', 'rb')
        Data_all = pickle.load(f1)
        f1.close()
        Data = Data_all[Farm_for_target]
        Series = Data.loc[:, 'MIX']
        Time_range = Data_all[0]['Time']
        Time = Data_all[0][Data_all[0]['Time'] == Time_Target].index.tolist()[0]  # tolist是为了转化成为int型
        Time_Range = pd.date_range(Time_Target - datetime.timedelta(minutes=15 * 50),
                                   Time_Target + datetime.timedelta(minutes=15 * 249), freq='15min')
        ## 数据归一化
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))  # 这里feature_range根据需要自行设置，默认（0,1）
        train_temp = min_max_scaler.fit_transform(Series.values.reshape(-1, 1))  # values可以变成numpy
        Series_stand = min_max_scaler.transform(Data.loc[Time - 50: Time + 249, 'MIX'].values.reshape(-1, 1))
        ## 波动数据识别
        df_wave, y_fit, popt_origin, Params_origin = Gauss_Wave(Series_stand, Time_in=range(300), alpha=1.4)
        Fit = min_max_scaler.inverse_transform(
            Multi_gauss(range(50, 300), *popt_origin).reshape(-1, 1)).squeeze()  ## 拟合后的数据

        for i in range(df_wave.shape[0]):
            if (50 >= df_wave.loc[i, 'ts']) & (50 < df_wave.loc[i, 'te']):
                Start_Wave = i
                df_wave.loc[Start_Wave, 'ts'] = 50
                break
        df_wave = df_wave.loc[Start_Wave:, :].reset_index(drop=True)  # 只保留当前的wave
        df_waveFinal = df_wave.copy()
        df_waveFinal['ts'] = Time_Range[df_waveFinal['ts'].tolist()]
        df_waveFinal['te'] = Time_Range[df_waveFinal['te'].tolist()]
        df_waveFinal['am'] = min_max_scaler.inverse_transform(df_waveFinal['am'].values.reshape(-1, 1)).squeeze()
        df_waveFinal = df_waveFinal.drop(['time'], axis=1).copy()




        df_waveFinal['am'] = df_waveFinal['am'].map(lambda x: x / 1)
        df_waveFinal['am'] = round(df_waveFinal['am'], 2)

        df_waveFinal['scale'] = df_waveFinal['scale'].map(lambda x: x / 1)
        df_waveFinal['scale'] = round(df_waveFinal['scale'], 2)

        # 画图DataFrame，
        Line = pd.DataFrame(columns=['Time', 'Series', 'Wave', 'T'], index=range(250))
        Line.loc[:, 'Time'] = Time_Range[50:]
        Line.loc[:, 'Series'] = Data.loc[Time: Time + 249, 'MIX'].values
        for i in range(df_wave.shape[0]):
            Line.loc[df_wave.loc[i, 'ts'] - 50: df_wave.loc[i, 'te'] - 50, 'Wave'] = min_max_scaler.inverse_transform(
                f_gauss(np.arange(df_wave.loc[i, 'ts'], df_wave.loc[i, 'te'] + 1), *df_wave.iloc[i, :3].values).reshape(
                    -1, 1))
            Line.loc[[df_wave.loc[i, 'ts'] - 50, df_wave.loc[i, 'te'] - 51], 'T'] = [
                Line.loc[df_wave.loc[i, 'ts'] - 50, 'Wave'], Line.loc[df_wave.loc[i, 'te'] - 51, 'Wave']]
        Error_Percent = sum(abs(Fit[:16] - Line.loc[:, 'Series'].values[:16])) / (
                    16 * np.average(Line.loc[:, 'Series'].values))

        Error_Percent = round(Error_Percent, 4)*100

        self.textBrowser.setText(str(Error_Percent)+'%')

        df_waveFinal.columns = ['幅值(m/s)', '范围(15min)', '起始时刻', '终止时刻']

        print('风过程提取完成\n')

        self.m.show_plot_WP(df_wave, Line)

        self.show_table(df_waveFinal)
        
        


    def show_table(self, input_table):

        # show table
        input_table = input_table.round(2)

        input_table_rows = input_table.shape[0]
        input_table_colunms = input_table.shape[1]
        input_table_header = input_table.columns.values.tolist()
        # input_table_index = input_table.index.values.tolist()

        # ===========读取表格，转换表格，============================================
        # ======================给tablewidget设置行列表头============================

        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        # self.tableWidget.setVerticalHeaderLabels(input_table_index)

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