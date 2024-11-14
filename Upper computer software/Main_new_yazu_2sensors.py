import math
import warnings
warnings.filterwarnings("ignore")
import serial
from PyQt5.Qt import QWidget, QMainWindow, QApplication, Qt, QTextCursor,QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets

# 显示图片
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QFont, QPen, QTransform, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem, QDesktopWidget
import matplotlib.pyplot as plt
from numpy import mean

# from PyQt5.Qt import *
# 串口
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import time
from pyqtgraph.dockarea import *
import threading

import physiological_serial_2sensors

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
import os
from scipy import interpolate

from matplotlib.colors import Normalize, LinearSegmentedColormap


# 获取当前目录绝对路径
DIR_PATH = os.path.dirname(os.path.abspath("__file__")).replace('\\', '/')
print('当前目录绝对路径=', DIR_PATH)  # G:/MCC-Project2/界面UI/2021.2.16

signal_lang_eeg = []
# import sys
# sys.path.append(DIR_PATH + '/lib')
# sys.path.append(DIR_PATH + '/conf')
# sys.setrecursionlimit(10000)  # 将默认的递归深度修改为3000

from Mainwindow_VR import Ui_MainWindow2


import pandas as pd
import pickle
from tqdm import tqdm
from datetime import datetime
from PIL import Image


# 1）采集界面
class MainWindow_VR(QMainWindow, Ui_MainWindow2):
    def __init__(self):
        super(MainWindow_VR, self).__init__()
        self.setupUi(self)
        self.resize(1400, 800)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))

        self.setWindowTitle("微纳传感与智能感知--2024")
        # 生理信号采集
        self.init_gather_data()
        self.setup_ui_gather_data()
        self.action_run_gather_data()

    def init_gather_data(self):
        # 创建一个定时器 强制更新绘图()

        self.start = False
        self.save = False

        # 模拟实时数据
        # self.currenteegdata = [1.0]*1000
        self.timestamp1 = []
        self.timestamp2 = []

        self.all_left_time = []
        self.all_right_time = []

        self.currentpoint1data = []
        self.currentpoint2data = []
        self.currentpoint3data = []
        self.currentpoint4data = []
        self.currentpoint5data = []
        self.currentpoint6data = []
        self.currentpoint7data = []
        self.currentpoint15data = []

        self.currentpoint8data = []
        self.currentpoint9data = []
        self.currentpoint10data = []
        self.currentpoint11data = []
        self.currentpoint12data = []
        self.currentpoint13data = []
        self.currentpoint14data = []
        self.currentpoint16data = []

        self.averValue = True
        self.updateCLoud = UpdateCLoud()

    def setup_ui_gather_data(self):
        self.dockWidget_data_gather.setWindowTitle('上位机程序-足底电压信号采集软件')

        self.area = DockArea()
        self.dockWidget_data_gather.setWidget(self.area)
        # 1)Create docks, place them into the window one at a time.
        self.d1 = Dock("left foot", size=(600, 800),hideTitle=True)
        self.d2 = Dock("云图",size=(200, 800),hideTitle=True)
        self.d3 = Dock("right foot", size=(600, 800),hideTitle=True)



        self.area.addDock(self.d1, 'left')
        self.area.addDock(self.d3, 'right')
        self.area.addDock(self.d2, 'right')
        # self.area.addDock(self.d3, 'right')

        # 2) Add widgets into each dock
        # d1.hideTitleBar()



        self.w1 = pg.PlotWidget(title="point 1")
        self.w1.setLabel('left', '电压值', 'V')
        # self.w1.setRange(yRange=[-0.8, 1])
        self.w2 = pg.PlotWidget(title="point 2")
        self.w2.setLabel('left', '电压值', 'V')
        self.w3 = pg.PlotWidget(title="point 3")
        self.w3.setLabel('left', '电压值', 'V')
        self.w4 = pg.PlotWidget(title="point 4")
        self.w4.setLabel('left', '电压值', 'V')
        self.w5 = pg.PlotWidget(title="point 5")
        self.w5.setLabel('left', '电压值', 'V')
        self.w6 = pg.PlotWidget(title="point 6")
        self.w6.setLabel('left', '电压值', 'V')
        self.w7 = pg.PlotWidget(title="point 7")
        self.w7.setLabel('left', '电压值', 'V')
        self.w15 = pg.PlotWidget(title="point 8")
        self.w15.setLabel('left', '电压值', 'V')

        self.w8 = pg.PlotWidget(title="point 1")
        self.w8.setLabel('left', '电压值', 'V')
        self.w9 = pg.PlotWidget(title="point 2")
        self.w9.setLabel('left', '电压值', 'V')
        self.w10 = pg.PlotWidget(title="point 3")
        self.w10.setLabel('left', '电压值', 'V')
        self.w11 = pg.PlotWidget(title="point 4")
        self.w11.setLabel('left', '电压值', 'V')
        self.w12 = pg.PlotWidget(title="point 5")
        self.w12.setLabel('left', '电压值', 'V')
        self.w13 = pg.PlotWidget(title="point 6")
        self.w13.setLabel('left', '电压值', 'V')
        self.w14 = pg.PlotWidget(title="point 7")
        self.w14.setLabel('left', '电压值', 'V')
        self.w16 = pg.PlotWidget(title="point 8")
        self.w16.setLabel('left', '电压值', 'V')

        self.wenzi1 = QtWidgets.QLabel("   left foot")
        self.wenzi1.setFixedHeight(30)
        self.wenzi1.setFont(QFont("Roman times",10,QFont.Bold))
        self.wenzi1.setAlignment(Qt.AlignCenter)

        self.wenzi2 = QtWidgets.QLabel("   right foot")
        self.wenzi2.setFixedHeight(30)
        self.wenzi2.setFont(QFont("Roman times", 10, QFont.Bold))
        self.wenzi2.setAlignment(Qt.AlignCenter)

        self.d1.addWidget(self.wenzi1)
        self.d1.addWidget(self.w1)
        self.d1.addWidget(self.w2)
        self.d1.addWidget(self.w3)
        self.d1.addWidget(self.w4)
        self.d1.addWidget(self.w5)
        self.d1.addWidget(self.w6)
        self.d1.addWidget(self.w7)
        self.d1.addWidget(self.w15)

        self.d3.addWidget(self.wenzi2)
        self.d3.addWidget(self.w8)
        self.d3.addWidget(self.w9)
        self.d3.addWidget(self.w10)
        self.d3.addWidget(self.w11)
        self.d3.addWidget(self.w12)
        self.d3.addWidget(self.w13)
        self.d3.addWidget(self.w14)
        self.d3.addWidget(self.w16)


        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)  # 以平滑边缘绘图

        ## first dock gets buttons
        self.r2 = pg.LayoutWidget()
        self.r3 = pg.LayoutWidget()
        self.rightfoot_bund = pg.LayoutWidget()
        # port_label = QtWidgets.QLabel("Port:")
        self.startBtn = QtWidgets.QPushButton('Start')
        self.saveBtn = QtWidgets.QPushButton('Save')
        self.Serialrecearea = QtWidgets.QLabel("OUTPUT:")
        self.Serialrecedata = QtWidgets.QTextBrowser()



        self.saveBtn.setEnabled(False)
        # choose port_num
        self.port_comboBox_left = QtWidgets.QComboBox(self.r2)
        # port_comboBox.setGeometry(QtCore.QRect(50, 270, 51, 21))
        self.port_comboBox_left.setObjectName("port_comboBox_left")
        for i in range(30):
            self.port_comboBox_left.addItem("COM" + str(i))
        # self.port_comboBox.setCurrentIndex(5)

        self.port_comboBox_right = QtWidgets.QComboBox(self.rightfoot_bund)
        # port_comboBox.setGeometry(QtCore.QRect(50, 270, 51, 21))
        self.port_comboBox_right.setObjectName("port_comboBox_right")
        for i in range(30):
            self.port_comboBox_right.addItem("COM" + str(i))

        # choose BaudRateComboBox
        self.baud_comboBox = QtWidgets.QComboBox(self.w2)
        self.baud_comboBox.setObjectName("baud_comboBox")
        self.baud_comboBox.addItems(
            ['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200', '128000', '256000', '921600'])
            # [ '115200', '128000', '256000', '921600'])
        # self.baud_comboBox.setCurrentIndex(7)

        self.sampleRate_comboBox = QtWidgets.QComboBox(self.w2)
        self.sampleRate_comboBox.setObjectName("baud_comboBox")
        self.sampleRate_comboBox.addItems(
            ['50HZ', '60HZ', '70HZ', '80HZ', '90HZ', '100HZ', '110HZ', '120HZ', '130HZ', '140HZ', '150HZ'])

        self.portRear1 = QtWidgets.QLabel("左脚串口号:")
        self.portRear2 = QtWidgets.QLabel("右脚串口号:")
        self.baudRear = QtWidgets.QLabel("波特率:    ")
        self.SampleRear = QtWidgets.QLabel("采样率:")

        self.r4 = pg.LayoutWidget()
        self.r4.addWidget(self.portRear1, row=0,col=0)
        self.r4.addWidget(self.port_comboBox_left, row=0,col=1,colspan=4)

        self.r8 = pg.LayoutWidget()
        self.r8.addWidget(self.portRear2, row=0, col=0)
        self.r8.addWidget(self.port_comboBox_right, row=0, col=1, colspan=4)

        self.r5 = pg.LayoutWidget()
        self.r5.addWidget(self.baudRear, row=0, col=0)
        self.r5.addWidget(self.baud_comboBox, row=0, col=1, colspan=5)

        self.r6 = pg.LayoutWidget()
        self.r6.addWidget(self.SampleRear, row=0, col=0)
        self.r6.addWidget(self.sampleRate_comboBox, row=0, col=1, colspan=5)

        # self.port_comboBox2 = QtWidgets.QComboBox(self.r2)
        # self.port_comboBox2.setObjectName("port_comboBox2")

        self.r3.addWidget(self.startBtn, row=0, col=0)
        self.r3.addWidget(self.saveBtn, row=0, col=1)

        # 加载图片
        self.bg_image = Image.open('css/leg_foot_3.png')
        # 调整图片大小（假设数据是10x10的矩阵）
        self.bg_image = self.bg_image.resize((960, 960))

        # 云图绘制
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.canvas = FigureCanvas(self.fig)

        data = [[0 for _ in range(20)] for _ in range(20)]

        data[2][5] = 3
        data[4][4] = 3
        data[6][3] = 3
        data[8][4] = 3
        data[5][7] = 3
        data[15][7] = 3
        data[16][5] = 3
        data[18][6] = 3

        data[2][15] = 3
        data[4][16] = 3
        data[6][17] = 3
        data[8][16] = 3
        data[5][13] = 3
        data[15][13] = 3
        data[16][15] = 3
        data[18][14] = 3




        x = np.arange(0, 20)
        y = np.arange(0, 20)
        x_new = np.linspace(0, 20, 960)
        y_new = np.linspace(0, 20, 960)

        # 创建一个插值函数
        chazhiF = interpolate.interp2d(x, y, data, kind='linear')
        data = chazhiF(x_new, y_new)

        norm = Normalize(vmin=0, vmax=3)

        self.ax.clear()
        self.ax.imshow(self.bg_image)

        self.ax.imshow(data, cmap='jet', interpolation='nearest',norm=norm, alpha=0.5)
        # 去掉坐标轴和刻度
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

        self.logo2 = QtWidgets.QLabel()
        self.logo2.setPixmap(QtGui.QPixmap("./css/logo7.png"))
        self.logo2.setScaledContents(True)
        # self.logo2.setStyleSheet("border: 1px solid blue")
        self.logo2.setObjectName("logo2")

        self.r2.addWidget(self.logo2, row=0, col=0)
        # self.r2.addWidget(self.wenzi3, row=1, col=0)
        self.r2.addWidget(self.r4, row=1, col=0)
        self.r2.addWidget(self.r8, row=2, col=0)
        self.r2.addWidget(self.r5, row=3, col=0)
        # self.r2.addWidget(self.r6, row=4, col=0)
        self.r2.addWidget(self.r3, row=5, col=0)
        self.r2.addWidget(self.Serialrecearea, row=6, col=0)
        self.r2.addWidget(self.Serialrecedata, row=7, col=0)
        self.r2.addWidget(self.canvas, row=8, col=0)

        self.d2.addWidget(self.r2)

        # Draw and update
        self.point1curve = self.w1.plot(pen='b')  # b为蓝色
        self.point2curve = self.w2.plot(pen='b')
        self.point3curve = self.w3.plot(pen='b')
        self.point4curve = self.w4.plot(pen='b')
        self.point5curve = self.w5.plot(pen='b')
        self.point6curve = self.w6.plot(pen='b')
        self.point7curve = self.w7.plot(pen='b')
        self.point15curve = self.w15.plot(pen='b')

        self.point8curve = self.w8.plot(pen='b')  # b为蓝色
        self.point9curve = self.w9.plot(pen='b')
        self.point10curve = self.w10.plot(pen='b')
        self.point11curve = self.w11.plot(pen='b')
        self.point12curve = self.w12.plot(pen='b')
        self.point13curve = self.w13.plot(pen='b')
        self.point14curve = self.w14.plot(pen='b')
        self.point16curve = self.w16.plot(pen='b')


    def action_run_gather_data(self):
        # 创建一个Serial对象 获取数据
        self.thread1 = physiological_serial_2sensors.physiological_serial()
        self.thread1.start()

        # self.thread2 = cloudChart_serial()
        # self.thread2.start()

        # self.thread3 = physiological_serial2.physiological_serial()
        # self.thread3.start()

        self.port_comboBox_left.activated[str].connect(self.setportLeftCurrentIndex)
        self.port_comboBox_right.activated[str].connect(self.setportRightCurrentIndex)
        self.baud_comboBox.activated[str].connect(self.setbaudCurrentIndex)
        self.sampleRate_comboBox.activated[str].connect(self.setsampleRateCurrentIndex)

        #用来更新绘制的图像
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)  #这儿


        self.startBtn.clicked.connect(self.startExec_click)
        self.saveBtn.clicked.connect(self.saveExec_click)

    def setportLeftCurrentIndex(self):
        self.thread1.setLeftPort(self.port_comboBox_left.currentText())

    def setportRightCurrentIndex(self):
        self.thread1.setRightPort(self.port_comboBox_right.currentText())

    def setbaudCurrentIndex(self):
        self.thread1.setBaud(self.baud_comboBox.currentText())

    def setsampleRateCurrentIndex(self):
        self.thread1.setSampleRate(self.sampleRate_comboBox.currentText())

    def update(self):
        self.timestamp1,self.currentpoint1data, self.currentpoint2data, self.currentpoint3data, \
        self.currentpoint4data, self.currentpoint5data, self.currentpoint6data, self.currentpoint7data, self.currentpoint15data,\
        self.timestamp2, self.currentpoint8data, self.currentpoint9data, self.currentpoint10data, \
        self.currentpoint11data, self.currentpoint12data, self.currentpoint13data, self.currentpoint14data, self.currentpoint16data = self.thread1.getData()
        # print('lang123  ',self.currentpoint1data)

        if self.start == True:

            threshold = 3  # 一般取3，可以根据实际情况调整

            #左脚电容值数据
            data1 = np.array(self.currentpoint1data[-500:])
            # mean1 = np.mean(data1)
            # std_dev1 = np.std(data1)
            # data1 = [x for x in data1 if (mean1 - threshold * std_dev1 < x < mean1 + threshold * std_dev1)]
            # if max(data1) > 1000:
            #     data1 = np.divide(data1, 1000)
            #     self.w1.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w1.setLabel('left', '电容值', 'pF')
            self.point1curve.setData(data1)

            data2 = np.array(self.currentpoint2data[-500:])
            # mean2 = np.mean(data2)
            # std_dev2 = np.std(data2)
            # data2 = [x for x in data2 if (mean2 - threshold * std_dev2 < x < mean2 + threshold * std_dev2)]
            # if max(data2) > 1000:
            #     data2 = np.divide(data2, 1000)
            #     self.w2.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w2.setLabel('left', '电容值', 'pF')
            self.point2curve.setData(data2)

            data3 = np.array(self.currentpoint3data[-500:])
            # mean3 = np.mean(data3)
            # std_dev3 = np.std(data3)
            # data3 = [x for x in data3 if (mean3 - threshold * std_dev3 < x < mean3 + threshold * std_dev3)]
            # if max(data3) > 1000:
            #     data3 = np.divide(data3, 1000)
            #     self.w3.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w3.setLabel('left', '电容值', 'pF')
            self.point3curve.setData(data3)

            data4 = np.array(self.currentpoint4data[-500:])
            # mean4 = np.mean(data4)
            # std_dev4 = np.std(data4)
            # data4 = [x for x in data4 if (mean4 - threshold * std_dev4 < x < mean4 + threshold * std_dev4)]
            # if max(data4) > 1000:
            #     data4 = np.divide(data4, 1000)
            #     self.w4.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w4.setLabel('left', '电容值', 'pF')
            self.point4curve.setData(data4)

            data5 = np.array(self.currentpoint5data[-500:])
            # mean5 = np.mean(data5)
            # std_dev5 = np.std(data5)
            # data5 = [x for x in data5 if (mean5 - threshold * std_dev5 < x < mean5 + threshold * std_dev5)]
            # if max(data5) > 1000:
            #     data5 = np.divide(data5, 1000)
            #     self.w5.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w5.setLabel('left', '电容值', 'pF')
            self.point5curve.setData(data5)

            data6 = np.array(self.currentpoint6data[-500:])
            # mean6 = np.mean(data6)
            # std_dev6 = np.std(data6)
            # data6 = [x for x in data6 if (mean6 - threshold * std_dev6 < x < mean6 + threshold * std_dev6)]
            # if max(data6) > 1000:
            #     data6 = np.divide(data6, 1000)
            #     self.w6.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w6.setLabel('left', '电容值', 'pF')
            self.point6curve.setData(data6)

            data7 = np.array(self.currentpoint7data[-500:])
            # mean7 = np.mean(data7)
            # std_dev7 = np.std(data7)
            # data7 = [x for x in data7 if (mean7 - threshold * std_dev7 < x < mean7 + threshold * std_dev7)]
            # if max(data7) > 1000:
            #     data7 = np.divide(data7, 1000)
            #     self.w7.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w7.setLabel('left', '电容值', 'pF')
            self.point7curve.setData(data7)

            data15 = np.array(self.currentpoint15data[-500:])
            # mean15 = np.mean(data15)
            # std_dev15 = np.std(data15)
            # data15 = [x for x in data15 if (mean15 - threshold * std_dev15 < x < mean15 + threshold * std_dev15)]
            # if max(data15) > 1000:
            #     data15 = np.divide(data15, 1000)
            #     self.w15.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w15.setLabel('left', '电容值', 'pF')
            self.point15curve.setData(data15)

            #右脚数据
            data8 = np.array(self.currentpoint8data[-500:])
            # mean8 = np.mean(data8)
            # std_dev8 = np.std(data8)
            # data8 = [x for x in data8 if (mean8 - threshold * std_dev8 < x < mean8 + threshold * std_dev8)]
            # if max(data8) > 1000:
            #     data8 = np.divide(data8, 1000)
            #     self.w8.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w8.setLabel('left', '电容值', 'pF')
            self.point8curve.setData(data8)

            data9 = np.array(self.currentpoint9data[-500:])
            # mean9 = np.mean(data9)
            # std_dev9 = np.std(data9)
            # data9 = [x for x in data9 if (mean9 - threshold * std_dev9 < x < mean9 + threshold * std_dev9)]
            # if max(data9) > 1000:
            #     data9 = np.divide(data9, 1000)
            #     self.w9.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w9.setLabel('left', '电容值', 'pF')
            self.point9curve.setData(data9)

            data10 = np.array(self.currentpoint10data[-500:])
            # mean10 = np.mean(data10)
            # std_dev10 = np.std(data10)
            # data10 = [x for x in data10 if (mean10 - threshold * std_dev10 < x < mean10 + threshold * std_dev10)]
            # if max(data10) > 1000:
            #     data10 = np.divide(data10, 1000)
            #     self.w10.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w10.setLabel('left', '电容值', 'pF')
            self.point10curve.setData(data10)

            data11 = np.array(self.currentpoint11data[-500:])
            # mean11 = np.mean(data11)
            # std_dev11 = np.std(data11)
            # data11 = [x for x in data11 if (mean11 - threshold * std_dev11 < x < mean11 + threshold * std_dev11)]
            # if max(data11) > 1000:
            #     data11 = np.divide(data11, 1000)
            #     self.w11.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w11.setLabel('left', '电容值', 'pF')
            self.point11curve.setData(data11)

            data12 = np.array(self.currentpoint12data[-500:])
            # mean12 = np.mean(data12)
            # std_dev12 = np.std(data12)
            # data12 = [x for x in data12 if (mean12 - threshold * std_dev12 < x < mean12 + threshold * std_dev12)]
            # if max(data12) > 1000:
            #     data12 = np.divide(data12, 1000)
            #     self.w12.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w12.setLabel('left', '电容值', 'pF')
            self.point12curve.setData(data12)

            data13 = np.array(self.currentpoint13data[-500:])
            # mean13 = np.mean(data13)
            # std_dev13 = np.std(data13)
            # data13 = [x for x in data13 if (mean13 - threshold * std_dev13 < x < mean13 + threshold * std_dev13)]
            # if max(data13) > 1000:
            #     data13 = np.divide(data13, 1000)
            #     self.w13.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w13.setLabel('left', '电容值', 'pF')
            self.point13curve.setData(data13)

            data14 = np.array(self.currentpoint14data[-500:])
            # mean14 = np.mean(data14)
            # std_dev14 = np.std(data14)
            # data14 = [x for x in data14 if (mean14 - threshold * std_dev14 < x < mean14 + threshold * std_dev14)]
            # if max(data14) > 1000:
            #     data14 = np.divide(data14, 1000)
            #     self.w14.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w14.setLabel('left', '电容值', 'pF')
            self.point14curve.setData(data14)

            data16 = np.array(self.currentpoint16data[-500:])
            # mean16 = np.mean(data16)
            # std_dev16 = np.std(data16)
            # data16 = [x for x in data16 if (mean16 - threshold * std_dev16 < x < mean16 + threshold * std_dev16)]
            # if max(data16) > 1000:
            #     data16 = np.divide(data16, 1000)
            #     self.w16.setLabel('left', '电容值', 'nF')
            # else:
            #     self.w16.setLabel('left', '电容值', 'pF')
            self.point16curve.setData(data16)

            # 创建一个自定义的归一化对象，这里假设我们关注的值域是从50到200
            norm = Normalize(vmin=0, vmax=3)

            nowData = [[0 for _ in range(20)] for _ in range(20)]

            if len(self.currentpoint1data[-50:]) != 0:
               # print('1',np.array(self.currentpoint5data[-50:]))
               nowData[2][5] = np.mean(np.array(self.currentpoint15data[-50:]))
               nowData[4][4] = np.mean(np.array(self.currentpoint7data[-50:]))
               nowData[6][3]  = np.mean(np.array(self.currentpoint5data[-50:]))
               nowData[8][4] = np.mean(np.array(self.currentpoint4data[-50:]))
               nowData[5][7] = np.mean(np.array(self.currentpoint6data[-50:]))
               nowData[15][7] = np.mean(np.array(self.currentpoint3data[-50:]))
               nowData[16][5] = np.mean(np.array(self.currentpoint2data[-50:]))
               nowData[18][6] = np.mean(np.array(self.currentpoint1data[-50:]))


            if len(self.currentpoint8data[-50:]) != 0:
                # print('2')
                nowData[2][15] = np.mean(np.array(self.currentpoint8data[-50:]))
                nowData[4][16] = np.mean(np.array(self.currentpoint10data[-50:]))
                nowData[6][17] = np.mean(np.array(self.currentpoint11data[-50:]))
                nowData[8][16] = np.mean(np.array(self.currentpoint12data[-50:]))
                nowData[5][13] = np.mean(np.array(self.currentpoint9data[-50:]))
                nowData[15][13]  = np.mean(np.array(self.currentpoint13data[-50:]))
                nowData[16][15]  = np.mean(np.array(self.currentpoint14data[-50:]))
                nowData[18][14]  = np.mean(np.array(self.currentpoint16data[-50:]))


            # 云图绘制  法3
            x = np.arange(0, 20)
            y = np.arange(0, 20)

            # 创建一个插值函数
            chazhiF = interpolate.interp2d(x, y, nowData, kind='linear')
            x_new = np.linspace(0, 20, 960)
            y_new = np.linspace(0, 20, 960)
            # 对新的网格进行插值
            nowData = chazhiF(x_new, y_new)


            # 使用imshow绘制云图
            self.ax.clear()
            self.ax.imshow(self.bg_image)
            self.ax.imshow(nowData, cmap='jet', interpolation='nearest', norm=norm, alpha=0.5)
            # 去掉坐标轴和刻度
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.canvas.draw()



    #点击开始按钮
    def startExec_click(self):
        if self.start == False:  # 当前未启动，启动采集（启动eeg线程，启动绘图更新timer），按钮文字设置为stop，enable save button，
            self.start = True
            self.timeClickStart = time.time()
            self.saveBtn.setEnabled(True)
            self.startBtn.setText("Stop")
            self.thread1.turnOn()
            # self.thread2.turnOn()
            # self.thread3.turnOn()
            self.Serialrecedata.append('................上位机已开启................')
            self.timer.start(50)  # 刷新时间间隔50ms

        elif self.start == True:
            self.start = False
            self.Serialrecedata.append('................上位机已关闭................')
            self.saveBtn.setEnabled(False)
            self.startBtn.setText("Start")
            self.thread1.stop()
            # self.thread2.stop()
            # self.thread3.stop()

    # 点击保存按钮
    def saveExec_click(self):
        if self.save == False:
            self.save = True
            self.saveBtn.setText("Finish")
            self.dt_ms = self.get_time_stamp()
             # 保存起始点
            self.begin_cnt1 = len(self.timestamp1)
            self.begin_cnt2 = len(self.timestamp2)
            self.Serialrecedata.append('开始存储当前数据\n')


        elif self.save == True:
            self.save = False
            self.saveBtn.setText("Save")
            # 保存结束点
            self.end_cnt1 = len(self.timestamp1)
            self.end_cnt2 = len(self.timestamp2)
            # 时间戳与EEG、EOG对齐

            # timestamp1 = [i for i in self.timestamp1[self.begin_cnt1:self.end_cnt1] for j in range(1)]
            # cal_timestamp1 = [(int)((i - timestamp1[0]) * 1000) for i in timestamp1]

            # print('timestamp', timestamp1)
            # print('cal_timestamp', cal_timestamp1)
            # print('point_one', self.currentpoint1data)
            # print('point_two', self.currentpoint2data)
            data_df1 = pd.DataFrame({'timestamp': self.timestamp1[self.begin_cnt1:self.end_cnt1],
                                     'point_one_left': self.currentpoint1data[self.begin_cnt1:self.end_cnt1],
                                     'point_two_left': self.currentpoint2data[self.begin_cnt1:self.end_cnt1],
                                     'point_three_left': self.currentpoint3data[self.begin_cnt1:self.end_cnt1],
                                     'point_four_left': self.currentpoint4data[self.begin_cnt1:self.end_cnt1],
                                     'point_five_left': self.currentpoint5data[self.begin_cnt1:self.end_cnt1],
                                     'point_six_left': self.currentpoint6data[self.begin_cnt1:self.end_cnt1],
                                     'point_seven_left': self.currentpoint7data[self.begin_cnt1:self.end_cnt1],
                                     'point_eight_left': self.currentpoint15data[self.begin_cnt1:self.end_cnt1],
                                     }, dtype=str)

            new_employee_info = {'timestamp': 'startTime', 'point_one_left': (self.dt_ms)}
            data_df1 = pd.concat([pd.DataFrame(new_employee_info, index=[0]), data_df1], ignore_index=True)

            crt1 = datetime.now().strftime('data/' + '%Y-%m-%d %H-%M-%S')
            filename1 = crt1 + ' plantarForce_left.csv'
            data_df1.to_csv(filename1, index=False)
            self.Serialrecedata.append('数据保存成功，left foot电容值保存路径为'+filename1+'\n')


            # timestamp2 = [i for i in self.timestamp2[self.begin_cnt2:self.end_cnt2] for j in range(1)]
            # cal_timestamp2 = [(int)((i - timestamp2[0]) * 1000) for i in timestamp2]

            data_df2 = pd.DataFrame({'timestamp': self.timestamp2[self.begin_cnt2:self.end_cnt2],
                                     'point_one_right': self.currentpoint8data[self.begin_cnt2:self.end_cnt2],
                                     'point_two_right': self.currentpoint9data[self.begin_cnt2:self.end_cnt2],
                                     'point_three_right': self.currentpoint10data[self.begin_cnt2:self.end_cnt2],
                                     'point_four_right': self.currentpoint11data[self.begin_cnt2:self.end_cnt2],
                                     'point_five_right': self.currentpoint12data[self.begin_cnt2:self.end_cnt2],
                                     'point_six_right': self.currentpoint13data[self.begin_cnt2:self.end_cnt2],
                                     'point_seven_right': self.currentpoint14data[self.begin_cnt2:self.end_cnt2],
                                     'point_eight_right': self.currentpoint16data[self.begin_cnt2:self.end_cnt2]
                                     }, dtype=str)

            new_employee_info2 = {'timestamp': 'startTime', 'point_one_right': (self.dt_ms)}
            data_df2 = pd.concat([pd.DataFrame(new_employee_info2, index=[0]), data_df2], ignore_index=True)

            crt2 = datetime.now().strftime('data/' + '%Y-%m-%d %H-%M-%S')
            filename2 = crt2 + ' plantarForce_right.csv'
            data_df2.to_csv(filename2, index=False)
            self.Serialrecedata.append('数据保存成功，right foot电容值保存路径为' + filename2+'\n')

    #获取当前时间
    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s_%03d" % (data_head, data_secs)
        print(time_stamp)
        return time_stamp

###云图更新类
class cloudChart_serial(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.point1_data = 0
        self.point2_data = 0
        self.point3_data = 0
        self.point4_data = 0
        self.point5_data = 0
        self.point6_data = 0
        self.point7_data = 0

        self.evepoint1 = 0
        self.evepoint2 = 0
        self.evepoint3 = 0
        self.evepoint4 = 0
        self.evepoint5 = 0
        self.evepoint6 = 0
        self.evepoint7 = 0

        self.thread_stop = False

        self.rows = 860  # 指定行数
        self.cols = 623  # 指定列数

        self.updateCLoud = UpdateCLoud()

    def cloudChart(self):  # Overwrite run() method, put what you want the thread do here
        print("The cloudChart_data threading is start")

        while not self.thread_stop:
            self.valueTable = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            # self.valueTable[268][102] = self.point1_data
            # self.valueTable[200][134] = self.point2_data
            # self.valueTable[127][172] = self.point3_data
            # self.valueTable[136][278] = self.point4_data
            # self.valueTable[136][374] = self.point5_data
            # self.valueTable[137][502] = self.point6_data
            # self.valueTable[215][528] = self.point7_data

            self.valueTable[268][102] = self.point7_data
            self.valueTable[200][134] = self.point6_data
            self.valueTable[127][172] = self.point5_data
            self.valueTable[136][278] = self.point4_data
            self.valueTable[136][374] = self.point3_data
            self.valueTable[137][502] = self.point2_data
            self.valueTable[215][528] = self.point1_data

            print('当前用来绘制的电容值  ',self.point1_data,self.point2_data,self.point3_data,self.point4_data,self.point5_data,self.point6_data,self.point7_data)
            self.valueTable = self.setCurrentValue(self.valueTable)
            self.huizhi(self.valueTable)


    def setCurrentValue(self,valueTable):
        speed = 1.2  # 衰减倍数
        spreadDis = 150  # 可影响的距离
        pointList = [[268, 102], [200, 134], [127, 172], [136, 278], [136, 374], [137, 502], [215, 528]]

        for everyPoint in pointList:
            px = -1 * spreadDis
            py = -1 * spreadDis
            flag = True
            while flag:

                # print(everyPoint,px,py)
                dis = math.sqrt(px ** 2 + py ** 2)

                # print(everyPoint[0], everyPoint[1])
                # print(px, py)
                # print(dis)
                # print(valueTable[everyPoint[0]][everyPoint[1]])
                # print(valueTable[everyPoint[0]][everyPoint[1]] - speed*dis)
                # print(valueTable[everyPoint[0]+px][everyPoint[1]+py])

                if px == 0 and py == 0:
                    px += 1
                    continue
                elif px < spreadDis and 0 < everyPoint[0] + px < 860 and 0 < everyPoint[
                    1] + py < 623 and dis <= spreadDis:
                    # print(1)
                    valueTable[everyPoint[0] + px][everyPoint[1] + py] += ((valueTable[everyPoint[0]][everyPoint[1]] - speed * dis) if (valueTable[everyPoint[0]][everyPoint[1]] - speed * dis) > 0 else 0)
                    px += 1
                elif 0 >= everyPoint[0] + px or everyPoint[0] + px >= 860:
                    # print(2)
                    # py += 1
                    # px = -1 * spreadDis
                    px += 1
                    continue
                elif 0 >= everyPoint[1] + py:
                    # print(3)
                    py += 1
                    px = -1 * spreadDis
                    continue
                elif everyPoint[1] + py >= 623:
                    # print(4)
                    flag = False
                elif dis > spreadDis:
                    # print(5)
                    px += 1

                if px >= spreadDis:
                    # print(6)
                    px = -1 * spreadDis
                    py += 1
                if py >= spreadDis:
                    # print(7)
                    flag = False
        return valueTable

    def huizhi(self,valueTable):
        # make these smaller to increase the resolution

        plt.imshow(valueTable, cmap='jet', interpolation='bilinear', origin='lower')  # ,aspect='auto'
        # plt.colorbar()#显示颜色条
        plt.axis('off')  # 隐藏坐标轴
        plt.savefig('css/footpoint.png', transparent=True, bbox_inches='tight', pad_inches=0.0)
        # plt.show()

        jojo1 = Image.open('css/footpoint.png')
        jojo2 = Image.open('css/bbb.png')
        resized_image = jojo2.resize((250, int(jojo2.size[1] * 360 / jojo2.size[0])))

        plt.imshow(jojo1)
        plt.imshow(resized_image)
        plt.axis('off')  # 隐藏坐标轴
        print('更新了云图')

        plt.savefig('css/footfinal.png', transparent=True, bbox_inches='tight', pad_inches=0.0)
        if self.updateCLoud.getCurrentValue() == False:
            self.updateCLoud.updateValue()

    def stop(self):
        self.thread_stop = True

    def turnOn(self):
        self.thread_stop = False
        self.t1 = threading.Thread(target=self.cloudChart)
        self.t1.start()

    def setData(self,currentpoint1data,currentpoint2data,currentpoint3data,currentpoint4data,currentpoint5data,currentpoint6data,currentpoint7data):
        self.point1_data = mean(currentpoint1data) - self.evepoint1 + 5
        self.point2_data = mean(currentpoint2data) - self.evepoint2 + 5
        self.point3_data = mean(currentpoint3data) - self.evepoint3 + 5
        self.point4_data = mean(currentpoint4data) - self.evepoint4 + 5
        self.point5_data = mean(currentpoint5data) - self.evepoint5 + 5
        self.point6_data = mean(currentpoint6data) - self.evepoint6 + 5
        self.point7_data = mean(currentpoint7data) - self.evepoint7 + 5
        # self.point15_data = mean(currentpoint15data) - 900

    def setEver(self,evePoint1,evePoint2,evePoint3,evePoint4,evePoint5,evePoint6,evePoint7):
        self.evepoint1 = evePoint1
        self.evepoint2 = evePoint2
        self.evepoint3 = evePoint3
        self.evepoint4 = evePoint4
        self.evepoint5 = evePoint5
        self.evepoint6 = evePoint6
        self.evepoint7 = evePoint7

    def setUpdateCLoud(self,updateCLoud):
        self.updateCLoud = updateCLoud

# 公共类COmmomHelper,用于风格设计
class CommonHelper:
    def __init__(self):
        pass
    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()

class UpdateCLoud:
    def __init__(self):
        self.updateCloudChart = False
    def updateValue(self):
        if self.updateCloudChart == True:
            self.updateCloudChart = False
        if self.updateCloudChart == False:
            self.updateCloudChart = True
    def getCurrentValue(self):
        return self.updateCloudChart

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # 实例化子窗口
    mainwindow_vr = MainWindow_VR()
    # 界面风格设置
    cssStyle = CommonHelper.readQss(DIR_PATH + '/css/lightblue.css')
    mainwindow_vr.setStyleSheet(cssStyle)
    # 显示
    mainwindow_vr.show()
    sys.exit(app.exec_())