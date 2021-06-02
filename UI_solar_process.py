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

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, dpi=88):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
        self.axes = fig.add_subplot(111)
        # self.ax_twin = self.axes.twinx()
        self.axes.axis('off')

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


class Ui_MainWindow_solar_process(object):
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
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        # 画布
        self.m = PlotCanvas(self, width=4, height=3)  # 实例化一个画布对象
        self.m.move(80, 100)

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

        self.pushButton.clicked.connect(self.show_solar_process)

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

        # MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(800, 600)
        # self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setObjectName("centralwidget")
        # self.label = QtWidgets.QLabel(self.centralwidget)
        # self.label.setGeometry(QtCore.QRect(120, 40, 250, 31))
        # font = QtGui.QFont()
        # font.setPointSize(21)
        # self.label.setFont(font)
        # self.label.setTextFormat(QtCore.Qt.AutoText)
        # self.label.setAlignment(QtCore.Qt.AlignCenter)
        # self.label.setObjectName("label")
        # self.label_2 = QtWidgets.QLabel(self.centralwidget)
        # self.label_2.setGeometry(QtCore.QRect(550, 40, 201, 31))
        # font = QtGui.QFont()
        # font.setPointSize(21)
        # self.label_2.setFont(font)
        # self.label_2.setTextFormat(QtCore.Qt.AutoText)
        # self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_2.setObjectName("label_2")
        #
        # # 画布
        # self.m = PlotCanvas(self, width=4, height=2.5)  # 实例化一个画布对象
        # self.m.move(50, 100)
        #
        #
        #
        # # self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        # # self.dateTimeEdit.setGeometry(QtCore.QRect(590, 170, 151, 24))
        # # self.dateTimeEdit.setObjectName("dateTimeEdit")
        # # self.dateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 6, 19), QtCore.QTime(12, 0, 0)))
        #
        # self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        # self.layoutWidget.setGeometry(QtCore.QRect(450, 170, 350, 66))
        # self.layoutWidget.setObjectName("layoutWidget")
        # self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        # self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        # self.verticalLayout.setObjectName("verticalLayout")
        # self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        # self.label_9.setObjectName("label_9")
        # font_2 = QtGui.QFont()
        # font_2.setPointSize(12)
        # self.label_9.setFont(font_2)
        # self.label_9.setTextFormat(QtCore.Qt.AutoText)
        # self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        # self.horizontalLayout_3.addWidget(self.label_9)
        # self.dateTimeEdit_start = QtWidgets.QDateTimeEdit(self.layoutWidget)
        # self.dateTimeEdit_start.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 6, 19), QtCore.QTime(12, 0, 0)))
        #
        # self.dateTimeEdit_start.setObjectName("dateTimeEdit_start")
        # self.horizontalLayout_3.addWidget(self.dateTimeEdit_start)
        # self.verticalLayout.addLayout(self.horizontalLayout_3)
        # self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        # self.label_8.setObjectName("label_8")
        # self.label_8.setFont(font_2)
        # self.label_8.setTextFormat(QtCore.Qt.AutoText)
        # self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        # self.horizontalLayout_2.addWidget(self.label_8)
        #
        # self.comboBox_station = QtWidgets.QComboBox(self.centralwidget)
        # # self.comboBox_station.setGeometry(QtCore.QRect(590, 220, 151, 26))
        # self.comboBox_station.setObjectName("comboBox")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.setItemText(0, "")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        # self.comboBox_station.addItem("")
        #
        # self.comboBox_station.currentIndexChanged[str].connect(
        #     self.get_station_name)  # 条目发生改变，发射信号，传递条目内容
        #
        # self.horizontalLayout_2.addWidget(self.comboBox_station)
        # self.verticalLayout.addLayout(self.horizontalLayout_2)
        #
        # self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton.setGeometry(QtCore.QRect(590, 390, 131, 51))
        # font = QtGui.QFont()
        # font.setPointSize(16)
        # self.pushButton.setFont(font)
        # self.pushButton.setObjectName("pushButton")
        # self.pushButton.clicked.connect(self.show_solar_process)
        #
        # self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        # self.tableWidget.setGeometry(QtCore.QRect(50, 380, 391, 151))
        # self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setColumnCount(0)
        # self.tableWidget.setRowCount(0)
        #
        # self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        # self.textBrowser.setGeometry(QtCore.QRect(580, 470, 161, 31))
        # self.textBrowser.setObjectName("textBrowser")
        #
        # # TODO
        # # 在之后的点击中将文字替换为要显示的精度等内容
        # self.textBrowser.setText('test')
        # self.textBrowser.setAlignment(QtCore.Qt.AlignCenter)
        #
        # MainWindow.setCentralWidget(self.centralwidget)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        #
        # self.retranslateUi(MainWindow)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "云图特征自动提取"))
        self.label_2.setText(_translate("MainWindow", "参数设置"))
        self.pushButton.setText(_translate("MainWindow", "开始提取"))

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

    def show_solar_process(self):

        # load_data
        sample_time = self.str_datetime(self.dateTimeEdit.text())

        df = pd.read_excel(r'data_show_cloudimage/station_info_jilin.xlsx', sheet_name='光伏', index_col=0)
        df.columns = ['CAP', 'Lat', 'Lon', 'NWP_ID']

        with open('data_show_cloudimage/pixel_pos_relative.pkl', 'rb') as f:
            pixel_pos = pickle.load(f)

        dict_pixel_pos = {}

        for k in range(len(df)):
            dict_pixel_pos[df.index[k]] = pixel_pos[k]

        # 云检测
        ID_sta = int(station_[2:]) + 500
        # sample_time = datetime.datetime(2018, 6, 19, 12, 0, 0)
        dir_image = "cloudimage_2018_06_19"

        im0, im1 = load_image(dir_image, sample_time)
        print('load image sucess')
        target = list(map(int, dict_pixel_pos[ID_sta]))
        target = [target[1], target[0]]
        points = search_points(im1, target)
        print('search points sucess')

        if points:
            # 速度计算
            v = {}
            time_interval = (im1.time - im0.time).seconds

            #     print(points)

            for label in points:
                x, y = points[label]

                v[label] = cloud_move(im0.image, im1.image, x, y)

            df_v = pd.DataFrame(v).T * 500 / time_interval

            df_v.columns = ["v_x/(m/s)", "v_y(m/s)"]

            print('velocity calculation sucess')

            inputs = [im1, target, points, df_v]

            print('ready to run show_image')

            self.m.show_image(inputs)

            self.show_table(df_v)

    def show_table(self, input_table):

        # show table
        input_table = input_table.round(2)

        input_table_rows = input_table.shape[0]
        input_table_colunms = input_table.shape[1]
        input_table_header = input_table.columns.values.tolist()

        # ===========读取表格，转换表格，============================================
        # ======================给tablewidget设置行列表头============================

        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)

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




class MyWindow_solar_process(QMainWindow, Ui_MainWindow_solar_process):
    def __init__(self, parent=None):
        super(MyWindow_solar_process, self).__init__(parent)
        self.setupUi(self)

import sys
if __name__ == '__main__':
    # 字体随分辨率自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyWindow_solar_process()
    myWin.show()

    sys.exit(app.exec_())