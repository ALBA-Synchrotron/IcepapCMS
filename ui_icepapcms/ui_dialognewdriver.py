# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialognewdriver.ui'
#
# Created: Fri Mar 26 13:02:58 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogNewDriver(object):
    def setupUi(self, DialogNewDriver):
        DialogNewDriver.setObjectName("DialogNewDriver")
        DialogNewDriver.resize(471, 242)
        self.btnMoreInfo = QtGui.QPushButton(DialogNewDriver)
        self.btnMoreInfo.setGeometry(QtCore.QRect(360, 210, 100, 26))
        self.btnMoreInfo.setObjectName("btnMoreInfo")
        self.btnUseDefaults = QtGui.QPushButton(DialogNewDriver)
        self.btnUseDefaults.setGeometry(QtCore.QRect(40, 140, 121, 51))
        self.btnUseDefaults.setObjectName("btnUseDefaults")
        self.label = QtGui.QLabel(DialogNewDriver)
        self.label.setGeometry(QtCore.QRect(10, 10, 461, 41))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.btnCancel = QtGui.QPushButton(DialogNewDriver)
        self.btnCancel.setGeometry(QtCore.QRect(350, 140, 100, 51))
        self.btnCancel.setObjectName("btnCancel")
        self.label_2 = QtGui.QLabel(DialogNewDriver)
        self.label_2.setGeometry(QtCore.QRect(50, 50, 391, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.btnUseDriver = QtGui.QPushButton(DialogNewDriver)
        self.btnUseDriver.setGeometry(QtCore.QRect(190, 140, 131, 51))
        self.btnUseDriver.setObjectName("btnUseDriver")
        self.lblExpertInfo = QtGui.QLabel(DialogNewDriver)
        self.lblExpertInfo.setGeometry(QtCore.QRect(50, 80, 391, 31))
        self.lblExpertInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblExpertInfo.setObjectName("lblExpertInfo")

        self.retranslateUi(DialogNewDriver)
        QtCore.QMetaObject.connectSlotsByName(DialogNewDriver)

    def retranslateUi(self, DialogNewDriver):
        DialogNewDriver.setWindowTitle(QtGui.QApplication.translate("DialogNewDriver", "New driver", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMoreInfo.setToolTip(QtGui.QApplication.translate("DialogNewDriver", "Show values", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMoreInfo.setText(QtGui.QApplication.translate("DialogNewDriver", "More info ...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUseDefaults.setToolTip(QtGui.QApplication.translate("DialogNewDriver", "Set config to default\n"
"values and update the database", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUseDefaults.setText(QtGui.QApplication.translate("DialogNewDriver", "Use default values", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogNewDriver", "This driver board has been added to the system.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setToolTip(QtGui.QApplication.translate("DialogNewDriver", "Cancel driver\n"
"configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("DialogNewDriver", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogNewDriver", "The driver configuration has to be initialized.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUseDriver.setToolTip(QtGui.QApplication.translate("DialogNewDriver", "Update database\n"
"with current driver config", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUseDriver.setText(QtGui.QApplication.translate("DialogNewDriver", "Use values in the\n"
"driver board", None, QtGui.QApplication.UnicodeUTF8))
        self.lblExpertInfo.setText(QtGui.QApplication.translate("DialogNewDriver", "The driver board seems to be already configured by an expert.", None, QtGui.QApplication.UnicodeUTF8))

