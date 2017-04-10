#!/usr/bin/python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proj1_test4.ui'
#
# Created: Sun Feb 26 19:59:19 2017
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

#Importing required libraries
import sys

import time

import datetime

import Adafruit_DHT

import pygame

import matplotlib.pyplot as plt

#Defining global variables
alarm = 0
alarmVal = 0
graph = 0
myTime=[]
myTemp=[]
myHumidity=[]
sensor = 22  #DHT22 sensor
pin = 4      #GPIO Pin 4 (Pin 7)

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
        resultWindow.resize(314, 321)
        resultWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        resultWindow.setAutoFillBackground(False)
        resultWindow.setStyleSheet(_fromUtf8("QDialog{background-image: url(:/newPrefix/weather.jpg);}\n"
""))
        self.gridLayout = QtGui.QGridLayout(resultWindow)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.heading = QtGui.QLabel(resultWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.heading.sizePolicy().hasHeightForWidth())
        self.heading.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.heading.setFont(font)
        self.heading.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.heading.setAutoFillBackground(False)
        self.heading.setStyleSheet(_fromUtf8("QLabel{\n"
"background-color: rgb(231, 243, 255);\n"
"}"))
        self.heading.setTextFormat(QtCore.Qt.PlainText)
        self.heading.setScaledContents(False)
        self.heading.setObjectName(_fromUtf8("heading"))
        self.verticalLayout.addWidget(self.heading)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.textEditObj = QtGui.QTextEdit(resultWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditObj.sizePolicy().hasHeightForWidth())
        self.textEditObj.setSizePolicy(sizePolicy)
        self.textEditObj.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEditObj.setObjectName(_fromUtf8("textEditObj"))
        self.verticalLayout.addWidget(self.textEditObj)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.alarmObj = QtGui.QPushButton(resultWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alarmObj.sizePolicy().hasHeightForWidth())
        self.alarmObj.setSizePolicy(sizePolicy)
        self.alarmObj.setObjectName(_fromUtf8("alarmObj"))
        self.horizontalLayout_2.addWidget(self.alarmObj)
        self.sliderObj = QtGui.QSlider(resultWindow)
        self.sliderObj.setStyleSheet(_fromUtf8(""))
        self.sliderObj.setMinimum(-20)
        self.sliderObj.setMaximum(30)
        self.sliderObj.setOrientation(QtCore.Qt.Horizontal)
        self.sliderObj.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sliderObj.setTickInterval(5)
        self.sliderObj.setObjectName(_fromUtf8("sliderObj"))
        self.horizontalLayout_2.addWidget(self.sliderObj)
        self.graphObj = QtGui.QPushButton(resultWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphObj.sizePolicy().hasHeightForWidth())
        self.graphObj.setSizePolicy(sizePolicy)
        self.graphObj.setObjectName(_fromUtf8("graphObj"))
        self.horizontalLayout_2.addWidget(self.graphObj)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.readDataObj = QtGui.QPushButton(resultWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readDataObj.sizePolicy().hasHeightForWidth())
        self.readDataObj.setSizePolicy(sizePolicy)
        self.readDataObj.setObjectName(_fromUtf8("readDataObj"))
        self.horizontalLayout.addWidget(self.readDataObj)
        self.historyObj = QtGui.QPushButton(resultWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.historyObj.sizePolicy().hasHeightForWidth())
        self.historyObj.setSizePolicy(sizePolicy)
        self.historyObj.setObjectName(_fromUtf8("historyObj"))
        self.horizontalLayout.addWidget(self.historyObj)
        self.quitObj = QtGui.QPushButton(resultWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quitObj.sizePolicy().hasHeightForWidth())
        self.quitObj.setSizePolicy(sizePolicy)
        self.quitObj.setObjectName(_fromUtf8("quitObj"))
        self.horizontalLayout.addWidget(self.quitObj)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(resultWindow)
        QtCore.QObject.connect(self.quitObj, QtCore.SIGNAL(_fromUtf8("clicked()")), resultWindow.close)
        QtCore.QObject.connect(self.sliderObj, QtCore.SIGNAL(_fromUtf8("sliderReleased()")), self.textEditObj.setModified)
        QtCore.QMetaObject.connectSlotsByName(resultWindow)

    def retranslateUi(self, resultWindow):
        resultWindow.setWindowTitle(_translate("resultWindow", "Dialog", None))
        self.heading.setText(_translate("resultWindow", "Humidity and Temperature Sensor Data", None))
        self.alarmObj.setText(_translate("resultWindow", "Set Alarm", None))
        self.graphObj.setText(_translate("resultWindow", "Graph", None))
        self.readDataObj.setText(_translate("resultWindow", "Read Data", None))
        self.historyObj.setText(_translate("resultWindow", "History", None))
        self.quitObj.setText(_translate("resultWindow", "Quit", None))
        self.readDataObj.clicked.connect(self.printRead)
        self.historyObj.clicked.connect(self.printHistory)
        self.alarmObj.clicked.connect(self.raiseAlarm)
        self.graphObj.clicked.connect(self.drawGraph)

    #Function to read Temperature and Humidity values when 'Read Data' is clicked
    def printRead(self):

        global sensor
        global pin
        global alarmVal
        global alarm
        
        print("Read Data")
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temperature = round(temperature)
        humidity = round(humidity)
        ts = time.time()

        #Adding a timestamp at which the data was read in Hours, Mins and Seconds
        localtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

        localtime = "Time: "+str(localtime)+" :"
        
        if humidity is not None and temperature is not None:
            if alarm is not 1:
                total_string = "Temperature="+str(temperature)+"'C  Humidity = "+str(humidity)+"%"
                self.textEditObj.setText(localtime)
                self.textEditObj.append(total_string)
            elif temperature > alarmVal:
                    self.textEditObj.append(str(temperature))
                    alarm = 0
                    return 1
            
    def printHistory(self):
        global sensor  #DHT22 sensor
        global pin      #GPIO Pin 4 (Pin 7)
        sleepVal = 0.2 #in seconds

        global graph
        global myTime
        global myTemp
        global myHumidity
        
        for x in range(0, 9):
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            myTemp.append(round(temperature))
            myHumidity.append(round(humidity))
            ts = time.time()
            localtime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            if graph is 1:
                myTime.append(str(localtime))
            else:
                myTime.append("Time: "+str(localtime)+" :")
            time.sleep(sleepVal)

        self.textEditObj.setText("History:")

        for x in range(0, 9):
            self.textEditObj.append(myTime[x])
            self.textEditObj.append("Temp: "+str(myTemp[x]))
            self.textEditObj.append("Humidity: "+str(myHumidity[x])+"\n")
        
        
    def raiseAlarm(self):
        global alarm
        global alarmVal

        alarm = 1

        alarmVal = self.sliderObj.value()
        self.textEditObj.setText(str(alarmVal))
        sound = self.printRead()

        if sound is 1:
            pygame.mixer.init()
            #pygame.mixer.pre_init(frequency=44100, size=-16, channels=2)
            pygame.mixer.music.load("/home/pi/Adafruit_Python_DHT/examples/EID_Proj_1/Alarm.mp3")
            pygame.mixer.music.play(0,23)
            while pygame.mixer.music.get_busy() == True:
                continue
        print("Audio")
          
    def drawGraph(self):
        global graph
        global myTime
        global myTemp
        global myHumidity

        graph = 1
        self.printHistory()

        plt.plot(myTime,myTemp)
        plt.xlabel("Time")
        plt.ylabel("Temperature")
        plt.title("History")
        plt.show()
        graph = 0

    def setModified(textEditObj):
        self.textEditObj.setText(str(self.sliderObj.value()))
        print("update")
        
    
import image_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    resultWindow = QtGui.QDialog()
    ui = Ui_resultWindow()
    ui.setupUi(resultWindow)
    resultWindow.show()
    sys.exit(app.exec_())
