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

from show_cloudimage import Cloud_image, load_image, name_to_time, time_to_name_pkl, is_in_cloud, search_points, cloud_move

plt.rcParams["font.family"]="SimHei"

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, bottom = 0.25, dpi=100):
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

    def show_plot(self, df, cap):

        print('stat ploting')

        self.axes.cla()
        df.plot(ax=self.axes)
        self.axes.set_ylabel('功率/MW')
        self.axes.set_xlabel('时间')
        self.axes.set_ylim([0, cap])
        self.axes.tick_params(labelsize=10)

        self.axes.legend(['功率'])

        self.draw()

    def show_dist(self, df):
        print('stat ploting bar')

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



class Ui_MainWindow_solar_confidence(object):
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
        self.m = PlotCanvas(self, width=4, height=2)  # 实例化一个画布对象
        self.m.move(80, 100)

        # 画布
        self.m2 = PlotCanvas(self, width=4, height=3, bottom=0.3)  # 实例化一个画布对象
        self.m2.move(80, 340)

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
        self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 6, 19), QtCore.QTime(12, 0, 0)))
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

        self.pushButton.clicked.connect(self.show_solar_confidence)

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
        self.label.setText(_translate("MainWindow", "波动预警置信度"))
        self.label_2.setText(_translate("MainWindow", "参数设置"))
        self.pushButton.setText(_translate("MainWindow", "开始计算"))

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
        # self.comboBox_station.setItemText(12, _translate("MainWindow", "光伏12"))
        self.comboBox_station.setItemText(12, _translate("MainWindow", "光伏13"))
        self.comboBox_station.setItemText(13, _translate("MainWindow", "光伏14"))
        self.comboBox_station.setItemText(14, _translate("MainWindow", "光伏15"))
        self.comboBox_station.setItemText(15, _translate("MainWindow", "光伏16"))
        self.comboBox_station.setItemText(16, _translate("MainWindow", "光伏17"))
        self.comboBox_station.setItemText(17, _translate("MainWindow", "光伏18"))
        self.comboBox_station.setItemText(18, _translate("MainWindow", "光伏19"))
        self.comboBox_station.setItemText(19, _translate("MainWindow", "光伏20"))
        self.comboBox_station.setItemText(20, _translate("MainWindow", "光伏21"))

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
    #
    # def show_solar_confidence(self):
    #
    #     # load_data
    #     sample_time = self.str_datetime(self.dateTimeEdit.text())
    #
    #     df = pd.read_excel(r'data_show_cloudimage/station_info_jilin.xlsx', sheet_name='光伏', index_col=0)
    #     df.columns = ['CAP', 'Lat', 'Lon', 'NWP_ID']
    #
    #     df_res = pd.read_csv("data_solar_confidence/df_res_threshold.csv", index_col=0, parse_dates=True)
    #
    #     with open('data_show_cloudimage/pixel_pos_relative.pkl', 'rb') as f:
    #         pixel_pos = pickle.load(f)
    #
    #     dict_pixel_pos = {}
    #
    #     for k in range(len(df)):
    #         dict_pixel_pos[df.index[k]] = pixel_pos[k]
    #
    #     # 云检测
    #     ID_sta = int(station_[2:]) + 500
    #     power = pd.read_csv('Time_series_data/JILIN/Solar/Power/'+str(ID_sta)+'.csv', index_col=0, parse_dates=True)
    #
    #     dir_image = "cloudimage_2018_06_19"
    #
    #     im0, im1 = load_image(dir_image, sample_time)
    #     print('load image sucess')
    #     target = list(map(int, dict_pixel_pos[ID_sta]))
    #     target = [target[1], target[0]]
    #     points = search_points(im1, target)
    #     print('search points sucess')
    #
    #     power_to_show = power.loc[sample_time + datetime.timedelta(minutes=15 * 1):sample_time + datetime.timedelta(
    #         minutes=15 * 16)]
    #
    #     if points:
    #         # 速度计算
    #         v = {}
    #         time_interval = (im1.time - im0.time).seconds
    #         for label in points:
    #             x, y = points[label]
    #             v[label] = cloud_move(im0.image, im1.image, x, y)
    #         df_v = pd.DataFrame(v).T * 500 / time_interval
    #         df_v.columns = ["v_x/(m/s)", "v_y(m/s)"]
    #
    #         confidences = []
    #         for i in range(len(power_to_show)):
    #             d_s = []
    #             for theta in points:
    #                 v_ = v[theta]
    #                 point_now = points[theta]
    #                 point_later = np.array(point_now) + np.array(v_) * 15 * 60 * (i+1)/ 500
    #                 d_s.append(np.linalg.norm(np.array(point_later) - np.array(target)))
    #
    #             d_min = min(d_s)
    #             df_chosen = df_res[(d_min - 25 < df_res['distance']) & (df_res['distance'] < d_min + 25)]
    #             confidences.append(len(df_chosen[df_chosen['rmse'] < 1]) / len(df_chosen))
    #
    #         df_confidence = pd.DataFrame(confidences, index=list(map(lambda x: x.time(), power_to_show.index)), columns = ['confidece'])
    #
    #         with open('data_to_draw.pkl', 'wb') as f:
    #             pickle.dump([power_to_show, df_confidence], f)
    #
    #         self.m.show_plot(power_to_show, power.max()[0])
    #         self.m2.show_dist(df_confidence)

    def show_solar_confidence(self):

        with open('data_to_draw.pkl', 'rb') as f:
            [power_to_show, df_confidence] = pickle.load(f)

        self.m.show_plot(power_to_show,20)
        self.m2.show_dist(df_confidence)

class MyWindow_solar_confidence(QMainWindow, Ui_MainWindow_solar_confidence):
    def __init__(self, parent=None):
        super(MyWindow_solar_confidence, self).__init__(parent)
        self.setupUi(self)

import sys
if __name__ == '__main__':
    # 字体随分辨率自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyWindow_solar_confidence()
    myWin.show()

    sys.exit(app.exec_())