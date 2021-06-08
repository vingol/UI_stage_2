# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forecast_realtime.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']

mpl.rcParams['axes.unicode_minus'] = False


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0.12, bottom=0.2, right=0.9, top=0.9, hspace=0, wspace=0)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # self.init_plot()#打开App时可以初始化图片
        # self.plot()

    def scene_plot(self, Y_toplot, pred_toplot):
        counter = 1

        def start_timer():
            nonlocal counter
            global inputs
            counter += 1
            inputs = [counter, Y_toplot, pred_toplot]
            if counter >= len(Y_toplot):
                timer.stop()
                timer.deleteLater()

        timer = QTimer(self)
        print('timer start')
        timer.timeout.connect(start_timer)
        timer.timeout.connect(lambda: self.scene_update_figure(inputs))
        timer.start(1000)

    def scene_update_figure(self, inputs):

        self.axes.cla()
        counter, Y_toplot, pred_toplot = inputs[0], inputs[1], inputs[2]

        data_toplot_1 = Y_toplot[:counter]
        pred_start = data_toplot_1.iloc[-1:].index[0]
        data_toplot_1.columns = ['power']

        data_toplot_2 = pred_toplot.loc[pred_start]
        index_toplot2 = pd.date_range(start=pred_start, periods=16, freq='15min')
        data_toplot_2 = pd.DataFrame({'power': data_toplot_2.values}, index=index_toplot2)

        data_toplot = data_toplot_1[:-1].append(data_toplot_2)

        data_toplot[counter - 1:].plot(ax=self.axes)
        self.axes.set_xticks([])
        data_toplot[:counter].plot(ax=self.axes)
        # data_toplot[:counter].plot(ax=self.axes)

        # # 横坐标
        x_ticks = pd.date_range(
            start=Y_toplot[:1].index[0], end=Y_toplot[-1:].index[0] + datetime.timedelta(minutes=15 * 16), freq='2h')

        x_ticks_ = list(map(lambda x: str(x)[:-3], x_ticks.time))
        self.axes.set_xlim([x_ticks[0], x_ticks[-1]])
        for tick in self.axes.get_xticklabels():
            tick.set_rotation(45)
            # self.axes.set_xticks([])
        # self.axes.set_xticks(x_ticks)
        # self.axes.set_xticklabels(x_ticks_, fontsize=6, rotation=45)


        #
        # x_ticks = pd.date_range(start=Y_toplot[:1].index, periods=len(Y_toplot), freq='15min')
        # x_ticks_ = list(map(lambda x: str(x), x_ticks.time))
        # self.axes.set_xlim([0, len(Y_toplot)])
        # self.axes.set_xticks(range(0, len(Y_toplot), 1))
        # self.axes.set_xticklabels(x_ticks_, fontsize=6, rotation=45)

        # 图例
        self.axes.legend(['预测值','真实值'])
        #        self.axes.legend([start_time.split(' ')[0]], frameon=True)

        # 纵轴
        self.axes.set_ylabel('功率(MW)')
        self.axes.set_xlabel('时间')
        self.axes.set_title(str(pred_start.date()), fontsize=10, color='r')  # r: red
        self.draw()

class Ui_MainWindow_solarforecast_realtime(object):
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
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 240, 241, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 0, 731, 31))
        self.label.setObjectName("label")
        # self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        # self.graphicsView.setGeometry(QtCore.QRect(50, 130, 401, 331))
        # self.graphicsView.setMinimumSize(QtCore.QSize(401, 331))
        # self.graphicsView.setMaximumSize(QtCore.QSize(401, 331))
        # self.graphicsView.setObjectName("graphicsView")

        self.m = PlotCanvas(self, width=4, height=3)  # 实例化一个画布对象
        self.m.move(50, 130)

        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 60, 723, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_25 = QtWidgets.QLabel(self.layoutWidget)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_2.addWidget(self.label_25)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.horizontalLayout_2.addLayout(self.horizontalLayout_21)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.horizontalLayout_2.addLayout(self.horizontalLayout_22)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(490, 300, 271, 141))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        # self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        # self.label_3.setObjectName("label_3")
        # self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        # self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        # self.label_4.setObjectName("label_4")
        # self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        # self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        # self.lineEdit.setObjectName("lineEdit")
        # self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        # self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        # self.label_5.setObjectName("label_5")
        # self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        # self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget1)
        # self.lineEdit_2.setObjectName("lineEdit_2")
        # self.gridLayout.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        # self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        # self.label_6.setObjectName("label_6")
        # self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        # self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget1)
        # self.lineEdit_3.setObjectName("lineEdit_3")
        # self.gridLayout.addWidget(self.lineEdit_3, 3, 1, 1, 1)
        # self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        # self.label_2.setObjectName("label_2")
        # self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(490, 140, 275, 66))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        # self.label_24 = QtWidgets.QLabel(self.layoutWidget2)
        # self.label_24.setObjectName("label_24")
        # self.gridLayout_2.addWidget(self.label_24, 1, 0, 1, 2)
        # self.comboBox_8 = QtWidgets.QComboBox(self.layoutWidget2)
        # self.comboBox_8.setObjectName("comboBox_8")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.setItemText(0, "")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.comboBox_8.addItem("")
        # self.gridLayout_2.addWidget(self.comboBox_8, 1, 2, 1, 1)
        self.comboBox_station = QtWidgets.QComboBox(self.layoutWidget2)
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

        self.gridLayout_2.addWidget(self.comboBox_station, 0, 2, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_29.setObjectName("label_29")
        self.gridLayout_2.addWidget(self.label_29, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.comboBox_8.currentIndexChanged[str].connect(
        #     self.get_time_horizen)  # 条目发生改变，发射信号，传递条目内容

        # self.pushButton_2.clicked.connect(hello)
        # self.pushButton_2.clicked.connect(self.prediction)

        self.pushButton_2.clicked.connect(self.scene_forecast_iter)

        self.comboBox_station.currentIndexChanged[str].connect(
            self.get_station_name)  # 条目发生改变，发射信号，传递条目内容

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "显示预测结果"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-family:\'等线\'; font-size:24pt; color:#000000;\">光伏超短期功率预测（实时运行）</span></p><p><br/></p></body></html>"))
        self.label_25.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">功率预测曲线</span></p></body></html>"))
        # self.label_3.setText(_translate("MainWindow", "                   数值"))
        # self.label_4.setText(_translate("MainWindow", "均方根误差/MW"))
        # self.label_5.setText(_translate("MainWindow", "      合格率%"))
        # self.label_6.setText(_translate("MainWindow", "     准确率%"))
        # self.label_2.setText(_translate("MainWindow", "         指标"))
        # self.label_24.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">选择预测时间尺度：</span></p></body></html>"))
        # self.comboBox_8.setItemText(1, _translate("MainWindow", "15min"))
        # self.comboBox_8.setItemText(2, _translate("MainWindow", "30min"))
        # self.comboBox_8.setItemText(3, _translate("MainWindow", "45min"))
        # self.comboBox_8.setItemText(4, _translate("MainWindow", "1h"))
        # self.comboBox_8.setItemText(5, _translate("MainWindow", "1h15min"))
        # self.comboBox_8.setItemText(6, _translate("MainWindow", "1h30min"))
        # self.comboBox_8.setItemText(7, _translate("MainWindow", "1h45min"))
        # self.comboBox_8.setItemText(8, _translate("MainWindow", "2h"))
        # self.comboBox_8.setItemText(9, _translate("MainWindow", "2h15min"))
        # self.comboBox_8.setItemText(10, _translate("MainWindow", "2h30min"))
        # self.comboBox_8.setItemText(11, _translate("MainWindow", "2h45min"))
        # self.comboBox_8.setItemText(12, _translate("MainWindow", "3h"))
        # self.comboBox_8.setItemText(13, _translate("MainWindow", "3h15min"))
        # self.comboBox_8.setItemText(14, _translate("MainWindow", "3h30min"))
        # self.comboBox_8.setItemText(15, _translate("MainWindow", "3h45min"))
        # self.comboBox_8.setItemText(16, _translate("MainWindow", "4h"))
        self.comboBox_station.setItemText(1, _translate("MainWindow", "光伏1"))
        self.comboBox_station.setItemText(2, _translate("MainWindow", "光伏2"))
        self.comboBox_station.setItemText(3, _translate("MainWindow", "光伏3"))
        self.comboBox_station.setItemText(4, _translate("MainWindow", "光伏4"))
        self.comboBox_station.setItemText(5, _translate("MainWindow", "光伏5"))
        self.comboBox_station.setItemText(6, _translate("MainWindow", "光伏6"))
        self.comboBox_station.setItemText(7, _translate("MainWindow", "光伏7"))
        self.comboBox_station.setItemText(8, _translate("MainWindow", "光伏8"))
        self.comboBox_station.setItemText(9, _translate("MainWindow", "光伏9"))
        self.comboBox_station.setItemText(10, _translate("MainWindow", "光伏10"))
        self.comboBox_station.setItemText(11, _translate("MainWindow", "光伏11"))
        self.comboBox_station.setItemText(12, _translate("MainWindow", "光伏12"))
        self.comboBox_station.setItemText(13, _translate("MainWindow", "光伏13"))
        self.comboBox_station.setItemText(14, _translate("MainWindow", "光伏14"))
        self.comboBox_station.setItemText(15, _translate("MainWindow", "光伏15"))
        self.comboBox_station.setItemText(16, _translate("MainWindow", "光伏16"))
        self.comboBox_station.setItemText(17, _translate("MainWindow", "光伏17"))
        self.comboBox_station.setItemText(18, _translate("MainWindow", "光伏18"))
        self.comboBox_station.setItemText(19, _translate("MainWindow", "光伏19"))
        self.comboBox_station.setItemText(20, _translate("MainWindow", "光伏20"))
        self.label_29.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">选择电站：</span></p></body></html>"))

    # def get_time_horizen(self, i):
    #     # 获取数据类型
    #     global time_horizen_
    #     time_horizen_ = i

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

    def scene_forecast_iter(self):

        # read data from UI
        str2num = {"15min": 1, "30min": 2, "45min": 3, "1h": 4, "1h15min": 5, "1h30min": 6, "1h45min": 7, "2h": 8,
                   "2h15min": 9, "2h30min": 10, "2h45min": 11, "3h": 12, "3h15min": 13, "3h30min": 14, "3h45min": 15,
                   "4h": 16}

        #        time_horizen_ = '1'

        start_time = '2019/2/12 06-00-00'
        end_time = '2019/2/12 18-00-00'

        start_time = str(self.str_datetime(start_time))
        end_time = str(self.str_datetime(end_time))

        # start forecast
        path_savedata = './RECORDS_2019/'

        # read预测值
        model_name = 'c2d_3_cnn_1'
        pred = np.loadtxt(path_savedata + model_name + '_pred.txt')
        # read实际值
        Y_test = np.loadtxt(path_savedata + model_name + '_test.txt')

        Y_time_test = np.load('./RECORDS_2019/Y_time_test.npy')

        print('forecast sucess')
        # process prediction result
        index_ = pd.to_datetime(Y_time_test[:, 0])

        result_Y = pd.DataFrame(Y_test, index=index_)
        result_pred = pd.DataFrame(pred, index=index_)

        # read clear sky
        path_P_fit = path_savedata + 'y_hat_final.csv'
        P_fit = pd.read_csv(path_P_fit, index_col=0, parse_dates=True)
        index_sunny_day_all = P_fit.groupby(P_fit.index.date).count().index
        index_sunny_day = index_sunny_day_all

        index_for_update_DL = []
        for date in index_sunny_day:
            index_for_update_DL = index_for_update_DL + result_pred[result_pred.index.date == date].index.tolist()

        index_for_update_cs = []
        for date in index_sunny_day:
            index_for_update_cs = index_for_update_cs + P_fit[P_fit.index.date == date].index.tolist()

        index_for_update = list(set(index_for_update_DL).intersection(set(index_for_update_cs)))
        result_pred.loc[index_for_update] = P_fit.loc[index_for_update]

        # to plot
        # result_Y, result_pred
        Y_toplot = pd.DataFrame(result_Y.loc[start_time:end_time, 1 - 1])
        pred_toplot = pd.DataFrame(result_pred.loc[start_time:end_time, :])
        # Y_toplot = result_Y.loc[start_time:end_time, time_horizen - 1]
        # pred_toplot = result_pred.loc[start_time:end_time, :]


        print(Y_toplot.shape)
        print(pred_toplot.shape)
        #        data_plot_iter = pd.DataFrame({'实际值': Y_toplot, '预测值': pred_toplot})
        #        data_plot_iter =  pd.DataFrame(Data,columns=pd.Index(['实际值','预测值']))
        #  data_plot_iter.columns=['实际值','预测值']
        #        data_plot_iter1.index = data_plot_iter1.index + 1
        #        data_plot_iter2.index = data_plot_iter2.index + 1
        self.m.scene_plot(Y_toplot, pred_toplot)


