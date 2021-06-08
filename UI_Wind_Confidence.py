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

import warnings
warnings.filterwarnings("ignore")

plt.rcParams["font.family"]="SimHei"

from sklearn import preprocessing
import matplotlib
matplotlib.use('Agg')
import GMM_Distribution, GMM_Calculation


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
def Ramp_CGMM (Data_estimate, df_nwp, n_component, i):
    ### 使用并行计算对多个峰值下的cdf进行计算
    GMM_predict_sample = np.array([df_nwp.loc[i, 'am'], df_nwp.loc[i, 'scale'], 0, 0])
    GMM = GMM_Distribution.GMM_distribution(Data_estimate, n_components=n_component, method='EM', options='conditional', y=GMM_predict_sample)['CGMM']
    alpha1 = (df_nwp.loc[i, 'time'] - df_nwp.loc[i, 'ts']) / df_nwp.loc[i, 'scale']
    alpha2 = (df_nwp.loc[i, 'te'] - df_nwp.loc[i, 'time']) / df_nwp.loc[i, 'scale']
    # print('----------', alpha1, alpha2, '------------')

    ## 计算具体时间t上出现波动的概率
    import scipy, time
    # Data_test = Data_predict[i,:]  #用来计算测试的数据
    # kwargs = {'A':np.array([[1, -alpha1],[-1,-alpha2]]), 'b': np.array([matches_test.loc[i,'nwp_left'],-matches_test.loc[i,'nwp_right']])}
    kwargs = {'A': np.array([[1, -alpha1], [-1, -alpha2]]),
              'b': np.array([df_nwp.loc[i, 'ts'], -df_nwp.loc[i, 'te']])}
    GMM_bound = GMM_Calculation.GMM_calculation(GMM, options='linear', **kwargs)['linear_GMM']
    # t = matches_test.loc[i,'end']-1 #待计算的时间
    t = df_nwp.loc[i, 'te'] - 1  # 待计算的时间
    inf = 0
    sup = 15  # 记录此次波动所需要考虑的时间尺度
    # Prob_target = np.zeros(sup-inf+1); Prob_target[matches_test.loc[i,'begin']-inf:matches_test.loc[i,'end']-inf+1] = 1;
    a = time.time()
    Prob_ = np.zeros(sup - inf + 1)
    Prob_time = list(range(inf,sup+1))
    h_t, _ = scipy.integrate.dblquad(lambda y, x: np.exp(GMM_bound.score_samples(np.array([[x, y]]))), -np.inf, inf, lambda x: -np.inf, lambda x: -(inf))
    Prob_[0] = h_t
    Prob_time[0] = inf
    for g, t in enumerate(range(inf, sup)):  # 快速计算每个时间点的分位数结果
        h__1 = scipy.integrate.dblquad(lambda y, x: np.exp(GMM_bound.score_samples(np.array([[x, y]]))), -np.inf, t, lambda x: -t, lambda x: -(t + 1), epsabs=1.49e-5, epsrel=1.49e-5)
        h__2 = scipy.integrate.dblquad(lambda y, x: np.exp(GMM_bound.score_samples(np.array([[x, y]]))), t, t + 1, lambda x: -np.inf, lambda x: -t, epsabs=1.49e-5, epsrel=1.49e-5)
        h__3 = scipy.integrate.dblquad(lambda y, x: np.exp(GMM_bound.score_samples(np.array([[x, y]]))), t, t + 1, lambda x: -t, lambda x: -(t + 1), epsabs=1.49e-5, epsrel=1.49e-5)
        h_t = h__1[0] + h__2[0] + h__3[0] + h_t
        Prob_[g + 1] = h_t
        Prob_time[g + 1] = t + 1
    return Prob_, Prob_time

plt.rcParams["font.family"]="SimHei"

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, bottom = 0.25, dpi=75):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.16, bottom=bottom, right=0.9, top=0.9, hspace=0, wspace=0)
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

    def show_lineplot(self, df_wave, Line, df_wave_origin, Line_extend):

        self.axes.cla()

        Line_extend[:100 + 16].plot('Time', 'Series', label='NWP', linewidth=2, ax=self.axes)
        Line[:16].plot('Time', 'Series', label='目标NWP序列', linewidth=2.5, ax=self.axes)

        for i in range(df_wave_origin.shape[0]):
            if 15 + 100 < df_wave_origin.loc[i, 'ts']:
                break
            Line_extend[df_wave_origin.loc[i, 'ts']: min(df_wave_origin.loc[i, 'te'], 100 + 16)].plot('Time', 'Wave',
                                                                                                      label='波动过程' + str(i + 1),
                                                                                                      linewidth=2, linestyle='-.',ax=self.axes)


        # plt.fill_between(Line.loc[:15, 'Time'].values, plt.ylim()[1], plt.ylim()[0], color='#9467bd', alpha=0.4, label='Target Zone')

        # for i in range(df_wave.shape[0]):
        #     if 15 < df_wave.loc[i, 'ts']:
        #         break
        #     Line[df_wave.loc[i, 'ts']: min(df_wave.loc[i, 'te'], 16)].plot('Time', 'Wave',
        #                                                                    label='Wave' + str(i + 1),
        #                                                                    linewidth=2, linestyle='-.', ax=self.axes)
        self.axes.set(xlabel='时间 (15min)', ylabel='风速 (m/s)')
        self.axes.legend(loc='best')
        self.axes.set_title('待判断区域及周边的NWP曲线与波动过程识别')
        self.draw()

    def show_barplot(self, df_Warn):

        self.axes.cla()

        if (df_Warn['Warn'].values == np.zeros(16)).all() == True:  ## 如果没有预警
            self.axes.text(0.5, 0.5, '没有波动预警', fontsize=17, horizontalalignment='center',
                    verticalalignment='center')
        else:
            df_Warn.plot('Time', 'Warn', kind='bar', ax=self.axes, label='波动置信度', ylim=[0, 100])
            df_Warn['Loc'] = df_Warn['Warn'] + 10
            self.axes.legend(loc='best')
        self.axes.set(xlabel='时间 (15min)', ylabel='波动置信度 (%)')
        self.axes.set_title('待判断区域内的风波动置信度')
        self.draw()


    def show_plot(self, df, df2, cap):

        # print('stat ploting')

        self.axes.cla()
        df.plot(ax=self.axes)
        df2.plot(ax=self.axes)
        self.axes.set_ylabel('功率/MW')
        self.axes.set_xlabel('时间')
        self.axes.set_ylim([0, cap])
        self.axes.tick_params(labelsize=10)

        self.axes.legend(['功率', '晴空模型'])

        self.draw()

    def show_dist(self, df):
        # print('stat ploting bar')

        df = df*100

        self.axes.cla()
        df.plot(ax=self.axes, kind='bar')

        self.axes.set_ylabel('晴空概率/%')
        self.axes.set_xlabel('时间')
        # plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
        self.axes.tick_params(labelsize=8)
        self.axes.set_ylim([0, 100])
        self.axes.legend(['晴空概率'])
        self.draw()



class Ui_MainWindow_wind_confidence(object):
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

        # 画布
        self.m = PlotCanvas(self, width=6, height=3)  # 实例化一个画布对象
        self.m.move(30, 100)

        # 画布
        self.m2 = PlotCanvas(self, width=6, height=3, bottom=0.3)  # 实例化一个画布对象
        self.m2.move(30, 320)

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
        self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 10, 5), QtCore.QTime(1, 0, 0)))
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
        self.widget1.setGeometry(QtCore.QRect(105, 35, 660, 30))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(210)
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

        self.pushButton.clicked.connect(self.show_wind_confidence)

        self.comboBox_station.currentIndexChanged[str].connect(
            self.get_station_name)  # 条目发生改变，发射信号，传递条目内容

        # self.textBrowser.setText('test')
        # self.textBrowser.setAlignment(QtCore.Qt.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "风电波动预警置信度评估"))
        self.label_2.setText(_translate("MainWindow", "参数设置"))
        self.pushButton.setText(_translate("MainWindow", "开始计算"))

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
        # self.dateTimeEdit_end.setDisplayFormat(_translate("MainWindow", "yyyy/MM/dd HH-mm-ss"))

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

    def show_wind_confidence(self):
        print('正在进行风电波动预警置信度评估，请稍后...')

        # load_data

        Time_Target = self.str_datetime(self.dateTimeEdit.text())  # 目标时刻点（认为是最近历史时刻）
        try:

            Farm_for_target = int(station_[2:]) - 1  ## 只允许考虑两种风电场
        except NameError:
            Farm_for_target = 0

        f1 = open('Temp/Region_Dataforall.pkl', 'rb')
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
        df_wave_origin = df_wave.copy()  # 保存一个原版的df_wave

        for i in range(df_wave.shape[0]):
            if (50 >= df_wave.loc[i, 'ts']) & (50 < df_wave.loc[i, 'te']):
                Start_Wave = i
                df_wave.loc[Start_Wave, 'ts'] = 50
                break
        df_wave = df_wave.loc[Start_Wave:, :].reset_index(drop=True)  # 只保留当前的wave
        df_waveFinal = df_wave.copy()
        df_waveFinal['ts'] = Time_Range[df_waveFinal['ts'].tolist()]
        df_waveFinal['te'] = Time_Range[df_waveFinal['te'].tolist()]

        df_wave['ts'] = df_wave['ts'] - 50
        df_wave['te'] = df_wave['te'] - 50
        f = open('Temp/DataFarm' + str(Farm_for_target + 1) + '.pkl', 'rb')
        Data_estimate = pickle.load(f)
        f.close()

        ## 给出最终的df_nwp用于GMM怕短###
        if (df_wave.loc[1, 'te'] < 16) & (df_wave.shape[0] > 2):
            df_nwp = df_wave[:3]
        else:
            df_nwp = df_wave[:2]

        df_nwp = df_nwp[df_nwp['am'] >= 0.25]  # 最终以df_nwp为最终时间序列
        ins = df_nwp.index.tolist()  # 查看满足要求的波动编号

        if len(ins) != 0:
            Prob_Time = np.zeros((len(ins), 16))
            for i, index in enumerate(ins):
                Prob_, _ = Ramp_CGMM(Data_estimate, df_nwp, 3, i=index)
                Prob_Time[i, :] = Prob_
            Prob_Final = np.max(Prob_Time, axis=0)
        else:
            Prob_Final = np.zeros(16)

        ## 最终的判断结果与对应时间 df_Warn 用来画图
        df_Warn = pd.DataFrame(columns=['Time', 'Warn'], index=range(16))
        df_Warn['Time'] = list(map(lambda x: x.time(), Time_Range[50:50 + 16]))
        df_Warn['Warn'] = Prob_Final * 100  # 以百分比示意
        # 画图DataFrame
        Line = pd.DataFrame(columns=['Time', 'Series', 'Wave', 'T'], index=range(250))
        Line.loc[:, 'Time'] = list(map(lambda x: x, Time_Range[50:]))
        Line.loc[:, 'Series'] = Data.loc[Time: Time + 249, 'MIX'].values
        for i in range(df_wave.shape[0]):
            Line.loc[df_wave.loc[i, 'ts']: df_wave.loc[i, 'te'], 'Wave'] = min_max_scaler.inverse_transform(
                f_gauss(np.arange(df_wave.loc[i, 'ts'] + 50, df_wave.loc[i, 'te'] + 51),
                        *df_wave.iloc[i, :3].values).reshape(-1, 1))
            Line.loc[[df_wave.loc[i, 'ts'], df_wave.loc[i, 'te'] - 1], 'T'] = [Line.loc[df_wave.loc[i, 'ts'], 'Wave'],
                                                                               Line.loc[
                                                                                   df_wave.loc[i, 'te'] - 1, 'Wave']]

        Line_extend = pd.DataFrame(columns=['Time', 'Series', 'Wave'], index=range(300))
        Line_extend.loc[:, 'Time'] = list(map(lambda x: x, Time_Range[:]))
        Line_extend.loc[:, 'Series'] = Data.loc[Time - 50: Time + 249, 'MIX'].values
        for i in range(df_wave_origin.shape[0]):
            Line_extend.loc[df_wave_origin.loc[i, 'ts']: df_wave_origin.loc[i, 'te'],
            'Wave'] = min_max_scaler.inverse_transform(
                f_gauss(np.arange(df_wave_origin.loc[i, 'ts'], df_wave_origin.loc[i, 'te'] + 1),
                        *df_wave_origin.iloc[i, :3].values).reshape(-1, 1))

        print('风电波动预警置信度评估完成\n')
        self.m.show_lineplot(df_wave, Line, df_wave_origin, Line_extend)
        self.m2.show_barplot(df_Warn)



class MyWindow_wind_confidence(QMainWindow, Ui_MainWindow_wind_confidence):
    def __init__(self, parent=None):
        super(MyWindow_wind_confidence, self).__init__(parent)
        self.setupUi(self)

import sys
if __name__ == '__main__':
    # 字体随分辨率自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyWindow_wind_confidence()
    myWin.show()

    sys.exit(app.exec_())