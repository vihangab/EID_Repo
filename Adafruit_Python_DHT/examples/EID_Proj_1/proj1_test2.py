#!/usr/bin/python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proj1_test2.ui'
#
# Created: Sat Feb 25 15:49:16 2017
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

import sys

import time;

import Adafruit_DHT

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_resultWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        
    def setupUi(self, resultWindow):
        resultWindow.setObjectName(_fromUtf8("resultWindow"))
        resultWindow.resize(375, 266)
        resultWindow.setStyleSheet(_fromUtf8("image: url(:/newPrefix/Snapchat-3660669091553527667.jpg);"))
        self.gridLayout = QtGui.QGridLayout(resultWindow)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(resultWindow)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.heading = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.heading.setFont(font)
        self.heading.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.heading.setAutoFillBackground(False)
        self.heading.setTextFormat(QtCore.Qt.PlainText)
        self.heading.setScaledContents(False)
        self.heading.setObjectName(_fromUtf8("heading"))
        self.verticalLayout.addWidget(self.heading)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 3)
        self.textEditObj = QtGui.QTextEdit(resultWindow)
        self.textEditObj.setObjectName(_fromUtf8("textEditObj"))
        self.gridLayout.addWidget(self.textEditObj, 1, 0, 1, 3)
        self.graphObj = QtGui.QPushButton(resultWindow)
        self.graphObj.setObjectName(_fromUtf8("graphObj"))
        self.gridLayout.addWidget(self.graphObj, 3, 1, 1, 1)
        self.alarmObj = QtGui.QPushButton(resultWindow)
        self.alarmObj.setObjectName(_fromUtf8("alarmObj"))
        self.gridLayout.addWidget(self.alarmObj, 2, 0, 1, 1)
        self.readDataObj = QtGui.QPushButton(resultWindow)
        self.readDataObj.setObjectName(_fromUtf8("readDataObj"))
        self.gridLayout.addWidget(self.readDataObj, 3, 0, 1, 1)
        self.quitObj = QtGui.QPushButton(resultWindow)
        self.quitObj.setObjectName(_fromUtf8("quitObj"))
        self.gridLayout.addWidget(self.quitObj, 3, 2, 1, 1)
        self.horizontalSlider = QtGui.QSlider(resultWindow)
        self.horizontalSlider.setMinimum(-20)
        self.horizontalSlider.setMaximum(30)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.gridLayout.addWidget(self.horizontalSlider, 2, 1, 1, 1)

        self.retranslateUi(resultWindow)
        QtCore.QObject.connect(self.quitObj, QtCore.SIGNAL(_fromUtf8("clicked()")), resultWindow.close)
        QtCore.QMetaObject.connectSlotsByName(resultWindow)

    def retranslateUi(self, resultWindow):
        resultWindow.setWindowTitle(_translate("resultWindow", "Dialog", None))
        self.heading.setText(_translate("resultWindow", "Humidity and Temperature Sensor Data", None))
        self.graphObj.setText(_translate("resultWindow", "Graph", None))
        self.alarmObj.setText(_translate("resultWindow", "Set Alarm", None))
        self.readDataObj.setText(_translate("resultWindow", "Read Data", None))
        self.quitObj.setText(_translate("resultWindow", "Quit", None))
        self.readDataObj.clicked.connect(self.printRead)

    def printRead(self):
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        sensor = 22
        pin = 4
        print("Hello")
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temperature = round(temperature)
        humidity = round(humidity)
        localtime = time.asctime( time.localtime(time.time()))
        localtime = "Time: "+str(localtime)+" :"
        if humidity is not None and temperature is not None:

            #total_price = price  + ((tax / 100) * price)
            #total_price_string = "The total price with tax is: " + str(total_price)
            total_string = "Temperature="+str(temperature)+"*  Humidity = "+str(humidity)+"%"
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            self.textEditObj.setText(localtime)
            self.textEditObj.append(total_string)

import image_rc
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    resultWindow = QtGui.QDialog()
    ui = Ui_resultWindow()
    ui.setupUi(resultWindow)
    resultWindow.show()
    sys.exit(app.exec_())

