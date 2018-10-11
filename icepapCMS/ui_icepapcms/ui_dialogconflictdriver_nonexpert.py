# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogconflictdriver_nonexpert.ui'
#
# Created: Fri Feb  9 13:20:40 2018
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

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

class Ui_DialogConflictNonExpert(object):
    def setupUi(self, DialogConflictNonExpert):
        DialogConflictNonExpert.setObjectName(_fromUtf8("DialogConflictNonExpert"))
        DialogConflictNonExpert.resize(455, 220)
        self.label = QtGui.QLabel(DialogConflictNonExpert)
        self.label.setGeometry(QtCore.QRect(10, 0, 431, 41))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(DialogConflictNonExpert)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 391, 51))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.btnMoreInfo = QtGui.QPushButton(DialogConflictNonExpert)
        self.btnMoreInfo.setGeometry(QtCore.QRect(340, 180, 100, 26))
        self.btnMoreInfo.setObjectName(_fromUtf8("btnMoreInfo"))
        self.btnUpdate = QtGui.QPushButton(DialogConflictNonExpert)
        self.btnUpdate.setGeometry(QtCore.QRect(100, 120, 100, 51))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        self.btnCancel = QtGui.QPushButton(DialogConflictNonExpert)
        self.btnCancel.setGeometry(QtCore.QRect(230, 120, 100, 51))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))

        self.retranslateUi(DialogConflictNonExpert)
        QtCore.QMetaObject.connectSlotsByName(DialogConflictNonExpert)

    def retranslateUi(self, DialogConflictNonExpert):
        DialogConflictNonExpert.setWindowTitle(_translate("DialogConflictNonExpert", "Configuration conflict", None))
        self.label.setText(_translate("DialogConflictNonExpert", "The current values in the driver board do not match the IcePAP database", None))
        self.label_2.setText(_translate("DialogConflictNonExpert", "The driver board is either new or has been moved to a different slot.\n"
"\n"
"The current values in the driver board will be lost.", None))
        self.btnMoreInfo.setToolTip(_translate("DialogConflictNonExpert", "Show values", None))
        self.btnMoreInfo.setText(_translate("DialogConflictNonExpert", "More info ...", None))
        self.btnUpdate.setToolTip(_translate("DialogConflictNonExpert", "Send database config\n"
"to driver board", None))
        self.btnUpdate.setText(_translate("DialogConflictNonExpert", "Update driver", None))
        self.btnCancel.setToolTip(_translate("DialogConflictNonExpert", "Cancel driver\n"
"configuration", None))
        self.btnCancel.setText(_translate("DialogConflictNonExpert", "Cancel", None))

