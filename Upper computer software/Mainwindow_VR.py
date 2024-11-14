# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainwindow_VR.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow2(object):
    def setupUi(self, MainWindow2):
        MainWindow2.setObjectName("MainWindow2")
        MainWindow2.resize(888, 380)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("css/logo1.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow2.setWindowIcon(icon)



        self.centralwidget = QtWidgets.QWidget(MainWindow2)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_VR_experiment = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_VR_experiment.sizePolicy().hasHeightForWidth())
        self.lineEdit_VR_experiment.setSizePolicy(sizePolicy)
        self.lineEdit_VR_experiment.setObjectName("lineEdit_VR_experiment")
        self.verticalLayout_4.addWidget(self.lineEdit_VR_experiment)
        self.lineEdit_VR_count = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_VR_count.sizePolicy().hasHeightForWidth())
        self.lineEdit_VR_count.setSizePolicy(sizePolicy)
        self.lineEdit_VR_count.setReadOnly(True)
        self.lineEdit_VR_count.setObjectName("lineEdit_VR_count")
        self.verticalLayout_4.addWidget(self.lineEdit_VR_count)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.lineEdit_VR_status = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_VR_status.sizePolicy().hasHeightForWidth())
        self.lineEdit_VR_status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(10)
        self.lineEdit_VR_status.setFont(font)
        self.lineEdit_VR_status.setStyleSheet("QLineEdit:read-only{\n"
"            border: 1px solid gray;\n"
"            border-radius: 12px;\n"
"            padding: 0 8px;\n"
"            background: lightblue;\n"
"            selection-background-color: darkgray;\n"
"        }\n"
"")
        self.lineEdit_VR_status.setReadOnly(True)
        self.lineEdit_VR_status.setObjectName("lineEdit_VR_status")
        self.gridLayout.addWidget(self.lineEdit_VR_status, 0, 4, 1, 1)











        self.dockWidget_data_gather = QtWidgets.QDockWidget(MainWindow2) # 这儿

        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("source/imgs/1_4_VR.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dockWidget_data_gather.setWindowIcon(icon6)
        self.dockWidget_data_gather.setObjectName("dockWidget_data_gather")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.dockWidget_data_gather.setWidget(self.dockWidgetContents)
        MainWindow2.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockWidget_data_gather)

        self.retranslateUi(MainWindow2)

        QtCore.QMetaObject.connectSlotsByName(MainWindow2)

    def retranslateUi(self, MainWindow2):
        _translate = QtCore.QCoreApplication.translate
        MainWindow2.setWindowTitle(_translate("MainWindow2", "MainWindow"))
     
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow2 = QtWidgets.QMainWindow()
    ui = Ui_MainWindow2()
    ui.setupUi(MainWindow2)
    MainWindow2.show()
    sys.exit(app.exec_())

