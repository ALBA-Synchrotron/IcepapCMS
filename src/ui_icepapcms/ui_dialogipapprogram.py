# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogipapprogram.ui'
#
# Created: Thu Oct  2 15:16:13 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogIcepapProgram(object):
    def setupUi(self, DialogIcepapProgram):
        DialogIcepapProgram.setObjectName("DialogIcepapProgram")
        DialogIcepapProgram.resize(QtCore.QSize(QtCore.QRect(0,0,475,239).size()).expandedTo(DialogIcepapProgram.minimumSizeHint()))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(127,125,123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Highlight,brush)
        DialogIcepapProgram.setPalette(palette)
        DialogIcepapProgram.setWindowIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-cpu.png"))

        self.gridlayout = QtGui.QGridLayout(DialogIcepapProgram)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.txtHost = QtGui.QLineEdit(DialogIcepapProgram)
        self.txtHost.setObjectName("txtHost")
        self.gridlayout.addWidget(self.txtHost,2,6,1,2)

        self.cbProgram = QtGui.QComboBox(DialogIcepapProgram)
        self.cbProgram.setObjectName("cbProgram")
        self.gridlayout.addWidget(self.cbProgram,1,1,1,1)

        self.btnProgram = QtGui.QPushButton(DialogIcepapProgram)
        self.btnProgram.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-cpu.png"))
        self.btnProgram.setObjectName("btnProgram")
        self.gridlayout.addWidget(self.btnProgram,5,5,1,3)

        self.rbSerial = QtGui.QRadioButton(DialogIcepapProgram)
        self.rbSerial.setObjectName("rbSerial")
        self.gridlayout.addWidget(self.rbSerial,1,4,1,2)

        self.label = QtGui.QLabel(DialogIcepapProgram)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.cbSerial = QtGui.QComboBox(DialogIcepapProgram)
        self.cbSerial.setObjectName("cbSerial")
        self.gridlayout.addWidget(self.cbSerial,1,6,1,2)

        self.btnClose = QtGui.QPushButton(DialogIcepapProgram)
        self.btnClose.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/close.png"))
        self.btnClose.setObjectName("btnClose")
        self.gridlayout.addWidget(self.btnClose,6,5,1,3)

        self.label_2 = QtGui.QLabel(DialogIcepapProgram)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.btnBrowser = QtGui.QToolButton(DialogIcepapProgram)
        self.btnBrowser.setObjectName("btnBrowser")
        self.gridlayout.addWidget(self.btnBrowser,0,7,1,1)

        self.btnTest = QtGui.QPushButton(DialogIcepapProgram)
        self.btnTest.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-nettool.png"))
        self.btnTest.setObjectName("btnTest")
        self.gridlayout.addWidget(self.btnTest,4,5,1,3)

        self.rbEth = QtGui.QRadioButton(DialogIcepapProgram)
        self.rbEth.setObjectName("rbEth")
        self.gridlayout.addWidget(self.rbEth,2,4,1,2)

        self.label_3 = QtGui.QLabel(DialogIcepapProgram)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,4,4,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,3,6,1,1)

        self.sbAddr = QtGui.QSpinBox(DialogIcepapProgram)
        self.sbAddr.setMinimum(1)
        self.sbAddr.setMaximum(128)
        self.sbAddr.setObjectName("sbAddr")
        self.gridlayout.addWidget(self.sbAddr,1,2,1,1)

        self.cbOptions = QtGui.QComboBox(DialogIcepapProgram)
        self.cbOptions.setObjectName("cbOptions")
        self.gridlayout.addWidget(self.cbOptions,2,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2,1,3,1,1)

        self.txtFirmwareFile = QtGui.QLineEdit(DialogIcepapProgram)
        self.txtFirmwareFile.setMaximumSize(QtCore.QSize(1666666,16777215))
        self.txtFirmwareFile.setObjectName("txtFirmwareFile")
        self.gridlayout.addWidget(self.txtFirmwareFile,0,1,1,6)

        self.txtLog = QtGui.QTextEdit(DialogIcepapProgram)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.txtLog.setFont(font)
        self.txtLog.setReadOnly(True)
        self.txtLog.setObjectName("txtLog")
        self.gridlayout.addWidget(self.txtLog,3,0,4,4)

        self.chkForce = QtGui.QCheckBox(DialogIcepapProgram)
        self.chkForce.setObjectName("chkForce")
        self.gridlayout.addWidget(self.chkForce,2,2,1,1)

        self.retranslateUi(DialogIcepapProgram)
        QtCore.QMetaObject.connectSlotsByName(DialogIcepapProgram)
        DialogIcepapProgram.setTabOrder(self.txtFirmwareFile,self.btnBrowser)
        DialogIcepapProgram.setTabOrder(self.btnBrowser,self.cbProgram)
        DialogIcepapProgram.setTabOrder(self.cbProgram,self.sbAddr)
        DialogIcepapProgram.setTabOrder(self.sbAddr,self.cbOptions)
        DialogIcepapProgram.setTabOrder(self.cbOptions,self.rbSerial)
        DialogIcepapProgram.setTabOrder(self.rbSerial,self.rbEth)
        DialogIcepapProgram.setTabOrder(self.rbEth,self.cbSerial)
        DialogIcepapProgram.setTabOrder(self.cbSerial,self.txtHost)
        DialogIcepapProgram.setTabOrder(self.txtHost,self.btnTest)
        DialogIcepapProgram.setTabOrder(self.btnTest,self.btnProgram)
        DialogIcepapProgram.setTabOrder(self.btnProgram,self.btnClose)
        DialogIcepapProgram.setTabOrder(self.btnClose,self.txtLog)

    def retranslateUi(self, DialogIcepapProgram):
        DialogIcepapProgram.setWindowTitle(QtGui.QApplication.translate("DialogIcepapProgram", "Icepap Program", None, QtGui.QApplication.UnicodeUTF8))
        self.cbProgram.addItem(QtGui.QApplication.translate("DialogIcepapProgram", "NONE", None, QtGui.QApplication.UnicodeUTF8))
        self.cbProgram.addItem(QtGui.QApplication.translate("DialogIcepapProgram", "ALL", None, QtGui.QApplication.UnicodeUTF8))
        self.cbProgram.addItem(QtGui.QApplication.translate("DialogIcepapProgram", "DRIVERS", None, QtGui.QApplication.UnicodeUTF8))
        self.cbProgram.addItem(QtGui.QApplication.translate("DialogIcepapProgram", "COMM", None, QtGui.QApplication.UnicodeUTF8))
        self.cbProgram.addItem(QtGui.QApplication.translate("DialogIcepapProgram", "ADDR", None, QtGui.QApplication.UnicodeUTF8))
        self.btnProgram.setText(QtGui.QApplication.translate("DialogIcepapProgram", "Upgrade firmware", None, QtGui.QApplication.UnicodeUTF8))
        self.rbSerial.setText(QtGui.QApplication.translate("DialogIcepapProgram", "Serial Line", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogIcepapProgram", "Firmware file", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("DialogIcepapProgram", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogIcepapProgram", "Program", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowser.setText(QtGui.QApplication.translate("DialogIcepapProgram", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnTest.setText(QtGui.QApplication.translate("DialogIcepapProgram", "Test connection", None, QtGui.QApplication.UnicodeUTF8))
        self.rbEth.setText(QtGui.QApplication.translate("DialogIcepapProgram", "Ethernet", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogIcepapProgram", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOptions.addItem(QtGui.QApplication.translate("DialogIcepapProgram", "SAVE", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOptions.addItem(QtGui.QApplication.translate("DialogIcepapProgram", "SL", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOptions.addItem(QtGui.QApplication.translate("DialogIcepapProgram", "NONE", None, QtGui.QApplication.UnicodeUTF8))
        self.chkForce.setText(QtGui.QApplication.translate("DialogIcepapProgram", "Force", None, QtGui.QApplication.UnicodeUTF8))

import icepapcms_rc
