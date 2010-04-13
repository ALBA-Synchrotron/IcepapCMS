# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogconflictdriver_nonexpert.ui'
#
# Created: Fri Mar 26 13:02:58 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogConflictNonExpert(object):
    def setupUi(self, DialogConflictNonExpert):
        DialogConflictNonExpert.setObjectName("DialogConflictNonExpert")
        DialogConflictNonExpert.resize(455, 220)
        self.label = QtGui.QLabel(DialogConflictNonExpert)
        self.label.setGeometry(QtCore.QRect(10, 0, 431, 41))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(DialogConflictNonExpert)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 391, 51))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.btnMoreInfo = QtGui.QPushButton(DialogConflictNonExpert)
        self.btnMoreInfo.setGeometry(QtCore.QRect(340, 180, 100, 26))
        self.btnMoreInfo.setObjectName("btnMoreInfo")
        self.btnUpdate = QtGui.QPushButton(DialogConflictNonExpert)
        self.btnUpdate.setGeometry(QtCore.QRect(100, 120, 100, 51))
        self.btnUpdate.setObjectName("btnUpdate")
        self.btnCancel = QtGui.QPushButton(DialogConflictNonExpert)
        self.btnCancel.setGeometry(QtCore.QRect(230, 120, 100, 51))
        self.btnCancel.setObjectName("btnCancel")

        self.retranslateUi(DialogConflictNonExpert)
        QtCore.QMetaObject.connectSlotsByName(DialogConflictNonExpert)

    def retranslateUi(self, DialogConflictNonExpert):
        DialogConflictNonExpert.setWindowTitle(QtGui.QApplication.translate("DialogConflictNonExpert", "Configuration conflict", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogConflictNonExpert", "The current values in the driver board do not match the IcePAP database", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogConflictNonExpert", "The driver board is either new or has been moved to a different slot.\n"
"\n"
"The current values in the driver board will be lost.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMoreInfo.setToolTip(QtGui.QApplication.translate("DialogConflictNonExpert", "Show values", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMoreInfo.setText(QtGui.QApplication.translate("DialogConflictNonExpert", "More info ...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpdate.setToolTip(QtGui.QApplication.translate("DialogConflictNonExpert", "Send database config\n"
"to driver board", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpdate.setText(QtGui.QApplication.translate("DialogConflictNonExpert", "Update driver", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setToolTip(QtGui.QApplication.translate("DialogConflictNonExpert", "Cancel driver\n"
"configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("DialogConflictNonExpert", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

