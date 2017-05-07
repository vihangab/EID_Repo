#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_super_project.ui'
#
# Created: Fri May  5 18:47:31 2017
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

#Import required modules
import logging
import asyncio
import json
from aiocoap import *

#Defining global variable
items = 0
logging.basicConfig(level=logging.INFO)

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

class Ui_resultWindow(object):
    def setupUi(self, resultWindow):
        resultWindow.setObjectName(_fromUtf8("resultWindow"))
        resultWindow.resize(278, 321)
        resultWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        resultWindow.setAutoFillBackground(False)
        resultWindow.setStyleSheet(_fromUtf8("QDialog{background-image: url(:/newPrefix/mountains.jpg);}"))
        resultWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
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
        self.heading.setAlignment(QtCore.Qt.AlignCenter)
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
        self.textEditObj.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.textEditObj.setObjectName(_fromUtf8("textEditObj"))
        self.verticalLayout.addWidget(self.textEditObj)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.readDataObj = QtGui.QPushButton(resultWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readDataObj.sizePolicy().hasHeightForWidth())
        self.readDataObj.setSizePolicy(sizePolicy)
        self.readDataObj.setObjectName(_fromUtf8("readDataObj"))
        self.horizontalLayout_2.addWidget(self.readDataObj)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
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
        QtCore.QMetaObject.connectSlotsByName(resultWindow)

    def retranslateUi(self, resultWindow):
        resultWindow.setWindowTitle(_translate("resultWindow", "Dialog", None))
        self.heading.setText(_translate("resultWindow", "Client RPi3", None))
        self.readDataObj.setText(_translate("resultWindow", "Read Data", None))
        self.quitObj.setText(_translate("resultWindow", "Quit", None))
        self.readDataObj.clicked.connect(self.readData)

    def readData(self):
        global items
        self.textEditObj.setText(items)
        
async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://54.71.205.59/time')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))
        items = response.payload.decode('utf-8')
        items = str(items)
        #mylist = items.replace('{',' ').replace('\'',' ').replace(':',' ').replace(',',' ').split('    ')
        #print(mylist) 
        print(items) 

import image_rc

if __name__ == "__main__":
    import sys
    asyncio.get_event_loop().run_until_complete(main())
    app = QtGui.QApplication(sys.argv)
    resultWindow = QtGui.QDialog()
    ui = Ui_resultWindow()
    ui.setupUi(resultWindow)
    resultWindow.show()
    sys.exit(app.exec_())
