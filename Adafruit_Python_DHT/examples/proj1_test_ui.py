#!/usr/bin/python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proj1_test.ui'
#
# Created: Fri Feb 24 14:15:38 2017
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

import sys

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
        resultWindow.resize(515, 406)
        self.readDataObj = QtGui.QPushButton(resultWindow)
        self.readDataObj.setGeometry(QtCore.QRect(40, 340, 93, 28))
        self.readDataObj.setObjectName(_fromUtf8("readDataObj"))
        self.quitObj = QtGui.QPushButton(resultWindow)
        self.quitObj.setGeometry(QtCore.QRect(380, 340, 93, 28))
        self.quitObj.setObjectName(_fromUtf8("quitObj"))
        self.graphObj = QtGui.QPushButton(resultWindow)
        self.graphObj.setGeometry(QtCore.QRect(210, 340, 93, 28))
        self.graphObj.setObjectName(_fromUtf8("graphObj"))
        self.headingObj = QtGui.QLabel(resultWindow)
        self.headingObj.setGeometry(QtCore.QRect(50, 20, 401, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.headingObj.setFont(font)
        self.headingObj.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.headingObj.setAutoFillBackground(True)
        self.headingObj.setTextFormat(QtCore.Qt.PlainText)
        self.headingObj.setScaledContents(False)
        self.headingObj.setObjectName(_fromUtf8("headingObj"))
        self.textEditObj = QtGui.QTextEdit(resultWindow)
        self.textEditObj.setGeometry(QtCore.QRect(40, 280, 431, 41))
        self.textEditObj.setObjectName(_fromUtf8("textEditObj"))

        self.retranslateUi(resultWindow)
        QtCore.QMetaObject.connectSlotsByName(resultWindow)

    def retranslateUi(self, resultWindow):
        resultWindow.setWindowTitle(_translate("resultWindow", "Dialog", None))
        self.readDataObj.setText(_translate("resultWindow", "Read Data", None))
        self.quitObj.setText(_translate("resultWindow", "Quit", None))
        self.graphObj.setText(_translate("resultWindow", "Graph", None))
        self.headingObj.setText(_translate("resultWindow", "          Humidity and Temperature Sensor Data", None))
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
        if humidity is not None and temperature is not None:

            #total_price = price  + ((tax / 100) * price)
            #total_price_string = "The total price with tax is: " + str(total_price)
            total_string = "Temperature="+str(temperature)+"* Humidity = "+str(humidity)+"%"
            #print("Temperature={0:0.1f}*"+str(temperature)+"Humidity = "+)
            #print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            self.textEditObj.setText(total_string)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_resultWindow()
    ex.show()
    sys.exit(app.exec_())
