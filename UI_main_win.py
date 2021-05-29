# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_win_new.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from UI_Wind_Process import *
from UI_Wind_Confidence import *
from UI_mode import *
from images.location_of_plants_in_jilin_png import img as location_of_plants_in_jilin
from images.wind_plant_jilin_png import img as wind_plant_jilin
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

plt.rcParams["font.family"]="SimHei"

tmp = open('images/location_of_plants_in_jilin.png', 'wb')  # 创建临时的文件
tmp.write(base64.b64decode(location_of_plants_in_jilin))  ##把这个one图片解码出来，写入文件中去。
tmp.close()

tmp = open('images/wind_plant_jilin.png', 'wb')  # 创建临时的文件
tmp.write(base64.b64decode(wind_plant_jilin))  ##把这个one图片解码出来，写入文件中去。
tmp.close()

class MyWindow_wind_process(QMainWindow, Ui_MainWindow_wind_process):
    def __init__(self, parent=None):
        super(MyWindow_wind_process, self).__init__(parent)
        self.setupUi(self)

class MyWindow_wind_Confidence(QMainWindow, Ui_MainWindow_Wind_Confidence):
    def __init__(self, parent=None):
        super(MyWindow_Wind_Confidence, self).__init__(parent)
        self.setupUi(self)

class MyWindow_mode(QMainWindow, Ui_MainWindow_mode):
    def __init__(self, parent=None):
        super(MyWindow_mode, self).__init__(parent)
        self.setupUi(self)

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.subplots_adjust(left=0.12, bottom=0.2, right=0.9, top=0.9, hspace=0, wspace=0)
        # self.axes = fig.add_subplot(111)

        rect = [0.15, 0.15, 0.75, 0.75]
        axprops = dict(xticks=[], yticks=[])
        ax0 = self.fig.add_axes(rect, label='ax0', **axprops)
        map_image = plt.imread('map_img.png')
        ax0.imshow(map_image)
        # #     scatterMarkers = ['s', 'o', '^', '8','p', 'd', 'v', 'h', '<', ">"]
        # axprops = dict(xticks=[], yticks=[])
        # # self.ax0 = self.fig.add_axes(rect)
        self.ax1 = self.fig.add_axes(rect, label='ax1', frameon=False)

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

        self.ax1.set_xlabel('km')
        self.ax1.set_ylabel('km')


        self.draw()

    def update_figure_2(self, points, result, map_img, title):


        rect = [0.15, 0.15, 0.75, 0.75]
        # #     scatterMarkers = ['s', 'o', '^', '8','p', 'd', 'v', 'h', '<', ">"]
        axprops = dict(xticks=[], yticks=[])

        ax2 = self.fig.add_axes(rect, label='ax0', **axprops)
        ax2.imshow(map_img)


        self.ax1.cla()
        self.ax1 = self.fig.add_axes(rect, label='ax1', frameon=False)

        X = list(map(lambda x: x[1], points))
        Y = list(map(lambda x: x[0], points))

        self.ax1.scatter(X, Y)

        for j in range(len(X)):
            self.ax1.annotate(result[j] + 1, xy=(X[j], Y[j]), xytext=(X[j] + 0.01, Y[j] + 0.01))

        self.ax1.set_title(title)

        self.ax1.set_xlabel('km')
        self.ax1.set_ylabel('km')

        self.draw()

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 731, 31))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 60, 879, 3))
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 90, 151, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 160, 151, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(500, 210, 256, 241))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.m = PlotCanvas(self, width=4, height=3)  # 实例化一个画布对象
        self.m.move(50, 150)

        # 增加数据源选择

        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(540, 100, 250, 74))
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.label_choose_dataset = QtWidgets.QLabel(self.layoutWidget1)
        self.label_choose_dataset.setObjectName("选择数据源：")
        # self.horizontalLayout.addWidget(self.label_choose_dataset)

        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(640, 100, 245, 74))
        self.layoutWidget2.setObjectName("layoutWidget2")

        self.comboBox_station = QtWidgets.QComboBox(self.layoutWidget2)
        self.comboBox_station.setObjectName("comboBox_station")
        self.comboBox_station.addItem("")
        self.comboBox_station.setItemText(0, "")
        self.comboBox_station.addItem("")
        self.comboBox_station.addItem("")
        # self.horizontalLayout.addWidget(self.comboBox_station)

        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(260, 90, 151, 41))
        self.pushButton_9.setObjectName("pushButton_9")

        # self.widget = QtWidgets.QWidget(self.centralwidget)
        # self.widget.setGeometry(QtCore.QRect(490, 440, 281, 100))
        # self.widget.setObjectName("widget")
        # self.gridLayout = QtWidgets.QGridLayout(self.widget)
        # self.gridLayout.setContentsMargins(0, 0, 0, 0)
        # self.gridLayout.setObjectName("gridLayout")
        #
        # self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        # self.pushButton_3.setObjectName("pushButton_3")
        # self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 1)
        # self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        # self.pushButton_4.setObjectName("pushButton_4")
        # self.gridLayout.addWidget(self.pushButton_4, 2, 1, 1, 1)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(640, 470, 151, 41))
        self.pushButton_3.setObjectName("pushButton_9")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(490, 470, 151, 41))
        self.pushButton_4.setObjectName("pushButton_9")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(490, 510, 151, 41))
        self.pushButton_5.setObjectName("pushButton_9")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.comboBox_station.currentIndexChanged[str].connect(
            self.get_data_source)  # 条目发生改变，发射信号，传递条目内容

        self.pushButton.clicked.connect(self.slot_wind)
        self.pushButton_9.clicked.connect(self.slot_solar)

        # self.pushButton_2.clicked.connect(self.openfile)
        self.pushButton_2.clicked.connect(self.creat_table_show)

        self.pushButton_3.clicked.connect(self.show_UI_wind_process)
        self.pushButton_4.clicked.connect(self.show_UI_wind_Confidence)
        self.pushButton_5.clicked.connect(self.show_UI_mode)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:24pt;\">风光超短期预测基础数据平台</span></p><p><br/></p></body></html>"))
        self.label_choose_dataset.setText(_translate("MainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt;\">数据源：</span></p></body></html>"))

        self.comboBox_station.setItemText(1, _translate("MainWindow", "吉林"))
        self.comboBox_station.setItemText(2, _translate("MainWindow", "内蒙"))

        self.pushButton.setText(_translate("MainWindow", "风电电站分布"))
        self.pushButton_2.setText(_translate("MainWindow", "电站基本信息"))
        self.pushButton_9.setText(_translate("MainWindow", "光伏电站分布"))
        self.pushButton_3.setText(_translate("MainWindow", "风过程自动提取"))
        self.pushButton_4.setText(_translate("MainWindow", "波动预警的置信度"))
        self.pushButton_5.setText(_translate("MainWindow", "上下游关联模式识别"))
        # self.pushButton_6.setText(_translate("MainWindow", "波动预警的置信度"))


    def show_UI_wind_process(self):

        self.Window_wind_process = MyWindow_wind_process()
        self.Window_wind_process.show()


    def show_UI_wind_Confidence(self):

        self.Window_wind_Confidence = MyWindow_Wind_Confidence()
        self.Window_wind_Confidence.show()

    def show_UI_mode(self):

        self.Window_mode = MyWindow_mode()
        self.Window_mode.show()


    def get_data_source(self, i):

        global data_source
        data_source = i

        self.signal.emit(data_source)


    def slot_solar(self):
        # self.graphicsView.setStyleSheet(
        #     "image: url(location_of_plants_in_jilin.png);\n"
        #     "border-image: url(location_of_plants_in_jilin.png);")
        try:
            if data_source == '吉林':
                filename_data_source = 'data_source_JILIN'
            elif data_source == '内蒙':
                filename_data_source = 'data_source_NEIMENG'
        except NameError:
            filename_data_source = 'data_source_JILIN'

        try:
            points_solar = np.loadtxt('main_win_data/'+filename_data_source+'/pixel_pos_solar.txt')

            map_image = plt.imread('main_win_data/'+filename_data_source+'/map_img.png')

            title = "光伏电站分布"
            result_solar = np.arange(500,521)-500
            self.m.update_figure_1(points_solar/2, result_solar, map_image, title)
        except OSError:
            pass

    def slot_wind(self):

        try:
            if data_source == '吉林':
                filename_data_source = 'data_source_JILIN'
            elif data_source == '内蒙':
                filename_data_source = 'data_source_NEIMENG'
        except NameError:
            filename_data_source = 'data_source_JILIN'

        try:
            import pickle
            f = open('main_win_data/'+filename_data_source+'/pixel_pos_wind.pkl', 'rb')
            points_wind = pickle.load(f)
            f.close()

            map_image = plt.imread('main_win_data/'+filename_data_source+'/map_img.png')

            title = "风电电站分布"
            result_solar = np.arange(0, 20)
            self.m.update_figure_1(np.array(points_wind) / 2, result_solar, map_image, title)
        except OSError:
            pass

    def creat_table_show(self):
        # ===========读取表格，转换表格，===========================================
        # TODO
        # 修改表格具体信息
        try:
            # input_table = pd.read_excel('table_info.xlsx', sheet_name='Sheet1')
            input_table = pd.read_excel('main_win_data/table_info_new.xlsx', sheet_name='info')
            print('readtablesucess')

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
        except NameError:
            pass

        # # ================遍历表格每个元素，同时添加到tablewidget中========================
        # else:
        #     self.centralWidget.show()




# import main_win_rc