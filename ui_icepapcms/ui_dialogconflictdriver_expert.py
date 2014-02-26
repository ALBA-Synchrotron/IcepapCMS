# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogconflictdriver_expert.ui'
#
# Created: Wed Feb 26 18:21:32 2014
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogConflictExpert(object):
    def setupUi(self, DialogConflictExpert):
        DialogConflictExpert.setObjectName("DialogConflictExpert")
        DialogConflictExpert.resize(470, 240)
        self.btnCancel = QtGui.QPushButton(DialogConflictExpert)
        self.btnCancel.setGeometry(QtCore.QRect(250, 140, 100, 51))
        self.btnCancel.setObjectName("btnCancel")
        self.btnMoreInfo = QtGui.QPushButton(DialogConflictExpert)
        self.btnMoreInfo.setGeometry(QtCore.QRect(350, 200, 100, 26))
        self.btnMoreInfo.setObjectName("btnMoreInfo")
        self.label = QtGui.QLabel(DialogConflictExpert)
        self.label.setGeometry(QtCore.QRect(10, 10, 461, 41))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(DialogConflictExpert)
        self.label_2.setGeometry(QtCore.QRect(40, 70, 391, 48))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.btnUpdate = QtGui.QPushButton(DialogConflictExpert)
        self.btnUpdate.setGeometry(QtCore.QRect(100, 140, 121, 51))
        self.btnUpdate.setObjectName("btnUpdate")

        self.retranslateUi(DialogConflictExpert)
        QtCore.QMetaObject.connectSlotsByName(DialogConflictExpert)

    def retranslateUi(self, DialogConflictExpert):
        DialogConflictExpert.setWindowTitle(QtGui.QApplication.translate("DialogConflictExpert", "Configuration conflict - Expert mode", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setToolTip(QtGui.QApplication.translate("DialogConflictExpert", "Cancel driver\n"
"configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("DialogConflictExpert", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMoreInfo.setToolTip(QtGui.QApplication.translate("DialogConflictExpert", "Show values", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMoreInfo.setText(QtGui.QApplication.translate("DialogConflictExpert", "More info ...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogConflictExpert", "The IcePAP database differs from the current configuration in the driver board.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogConflictExpert", "An expert has probably configured the driver with an external tool.\n"
"\n"
"The current values in the database will be overwritten.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpdate.setToolTip(QtGui.QApplication.translate("DialogConflictExpert", "Update database with current\n"
"driver board configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpdate.setText(QtGui.QApplication.translate("DialogConflictExpert", "Update database", None, QtGui.QApplication.UnicodeUTF8))

