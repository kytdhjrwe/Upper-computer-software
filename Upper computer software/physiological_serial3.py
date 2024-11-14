import binascii
import math
import threading
import time
from collections import deque

import serial
import matplotlib.pyplot as plt

import scipy.signal as ss


###左脚串口线程类
class physiological_serial(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.point1_data = []
        self.point2_data = []
        self.point3_data = []
        self.point4_data = []
        self.point5_data = []
        self.point6_data = []
        self.point7_data = []
        self.point8_data = []

        self.point9_data = []
        self.point10_data = []
        self.point11_data = []
        self.point12_data = []
        self.point13_data = []
        self.point14_data = []
        self.point15_data = []
        self.point16_data = []

        self.serLeft = serial.Serial()  # initialize the serial port
        self.serRight = serial.Serial()  # initialize the serial port

        self.timeLeft = []
        self.timeRight = []

        self.thread_stop = False
        self.time1 = []
        self.time2 = []
        self.all_left_time = []
        self.all_right_time = []

        self.checkHead = deque(maxlen=2) #只保留四个元素的列表
        self.checkHead.append('0')
        self.checkHead.append('0')

        self.checkHead2 = deque(maxlen=2)  # 只保留四个元素的列表
        self.checkHead2.append('0')
        self.checkHead2.append('0')

        # rows = 860  # 指定行数
        # cols = 623  # 指定列数
        # self.valueTable = [[0 for _ in range(cols)] for _ in range(rows)]
        # self.phothhuizhi = 0
        #
        # self.nnn = 0
        # self.jishu = 0

    def receive_data(self):  # Overwrite run() method, put what you want the thread do here
        print("The receive_data threading is start")


        while not self.thread_stop:

            # binascii: 二进制和ASCII互转; b2a_hex: 返回的二进制数据的十六进制表示;
            # decode('utf-8'): 以 utf-8 编码格式解码字符串;
            # int(x, base=10): x为字符串或数字，base为进制数，默认十进制；若使用base，x需使用字符串形式；返回十进制整形数据
            # Hex_head_frame = int(binascii.b2a_hex(Head_frame).decode('utf-8'), 16)
            Head_frame1 = self.serLeft.read(1)  # 读取头帧,从串行端口读取1个字节
            self.checkHead.append(Head_frame1[0])
            # print('self.checkHead', self.checkHead)
            if self.checkHead[0]==205 and self.checkHead[1]==171:
                fenjio = self.serLeft.read(2)
                timeStamp = self.serLeft.read(4)
                Value_array = self.serLeft.read(16)
                end_array = self.serLeft.read(2)

                if end_array[0]==222 and end_array[1]==188:

                    timeStamp = binascii.b2a_hex(timeStamp).decode('utf-8').upper()
                    thetime = timeStamp[6:8] + timeStamp[4:6] + timeStamp[2:4] + timeStamp[0:2]
                    thetime = int(thetime, 16)
                    # print('thetime ',thetime)
                    # print('Value_array',Value_array)
                    # allData = binascii.b2a_hex(Value_array).decode('utf-8').upper()
                    # print('allData',allData)

                    p = 0
                    pointlistLeft = []
                    for i in range(8):
                        onepoint1 = Value_array[p:p + 2]
                        onepoint = onepoint1[1:] + onepoint1[:1]
                        # print('onepoint1',onepoint1)
                        # print('onepoint',onepoint)
                        pointlistLeft.append(int(binascii.b2a_hex(onepoint).decode('utf-8').upper(), 16))
                        p = p + 2

                    self.timeLeft.append(thetime)
                    self.point1_data.append(pointlistLeft[0])
                    self.point2_data.append(pointlistLeft[1])
                    self.point3_data.append(pointlistLeft[2])
                    self.point4_data.append(pointlistLeft[3])
                    self.point5_data.append(pointlistLeft[4])
                    self.point6_data.append(pointlistLeft[5])
                    self.point7_data.append(pointlistLeft[6])
                    self.point8_data.append(pointlistLeft[7])


            Head_frame2 = self.serRight.read(1)  # 读取头帧,从串行端口读取1个字节
            self.checkHead2.append(Head_frame2[0])
            if self.checkHead2[0]==205 and self.checkHead2[1]==171:

                fenjio = self.serRight.read(2)
                timeStamp = self.serRight.read(4)
                Value_array = self.serRight.read(16)
                end_array = self.serRight.read(2)

                if end_array[0]==222 and end_array[1]==188:
                    timeStamp = binascii.b2a_hex(timeStamp).decode('utf-8').upper()
                    thetime = timeStamp[6:8] + timeStamp[4:6] + timeStamp[2:4] + timeStamp[0:2]
                    thetime = int(thetime, 16)
                    # print('thetime ',thetime)
                    # print('Value_array',Value_array)
                    # allData = binascii.b2a_hex(Value_array).decode('utf-8').upper()
                    # print('allData',allData)

                    p = 0
                    pointlistRight = []
                    for i in range(8):
                        onepoint1 = Value_array[p:p + 2]
                        onepoint = onepoint1[1:] + onepoint1[:1]
                        # print('onepoint1',onepoint1)
                        # print('onepoint',onepoint)
                        pointlistRight.append(int(binascii.b2a_hex(onepoint).decode('utf-8').upper(), 16))
                        p = p + 2

                    self.timeRight.append(thetime)
                    self.point9_data.append(pointlistRight[0])
                    self.point10_data.append(pointlistRight[1])
                    self.point11_data.append(pointlistRight[2])
                    self.point12_data.append(pointlistRight[3])
                    self.point13_data.append(pointlistRight[4])
                    self.point14_data.append(pointlistRight[5])
                    self.point15_data.append(pointlistRight[6])
                    self.point16_data.append(pointlistRight[7])

    def MathCapa(self, dataCapa):
        xx1 = int(dataCapa, 16)
        return xx1

    def stop(self):
        self.thread_stop = True
        self.serLeft.close()
        self.serRight.close()

    def turnOn(self):
        self.thread_stop = False

        #设置默认的串口和波特率参数
        # self.ser.port = 'COM5'
        # self.ser.baudrate = 115200

        self.serLeft.open()
        self.serRight.open()
        self.t1 = threading.Thread(target=self.receive_data)
        self.t1.setDaemon(True)
        self.t1.start()

    def getData(self):
        return self.timeLeft, self.point1_data, self.point2_data,self.point3_data,\
               self.point4_data,self.point5_data,self.point6_data,self.point7_data,self.point8_data,\
               self.timeRight, self.point9_data, self.point10_data,self.point11_data,\
               self.point12_data,self.point13_data,self.point14_data,self.point15_data,self.point16_data

    def setLeftPort(self, str):
        print('左脚port修改为 ',str)
        self.serLeft.port = str

    def setRightPort(self, str):
        print('右脚port修改为 ', str)
        self.serRight.port = str

    def setBaud(self, str):
        print('baud修改为 ',str)
        self.serLeft.baudrate = str
        self.serRight.baudrate = str

if __name__ == '__main__':
    pass
