# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogconflictdriver_expert.ui'
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

class Ui_DialogConflictExpert(object):
    def setupUi(self, DialogConflictExpert):
        DialogConflictExpert.setObjectName(_fromUtf8("DialogConflictExpert"))
        DialogConflictExpert.resize(470, 240)
        self.btnCancel = QtGui.QPushButton(DialogConflictExpert)
        self.btnCancel.setGeometry(QtCore.QRect(250, 140, 100, 51))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.btnMoreInfo = QtGui.QPushButton(DialogConflictExpert)
        self.btnMoreInfo.setGeometry(QtCore.QRect(350, 200, 100, 26))
        self.btnMoreInfo.setObjectName(_fromUtf8("btnMoreInfo"))
        self.label = QtGui.QLabel(DialogConflictExpert)
        self.label.setGeometry(QtCore.QRect(10, 10, 461, 41))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(DialogConflictExpert)
        self.label_2.setGeometry(QtCore.QRect(40, 70, 391, 48))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.btnUpdate = QtGui.QPushButton(DialogConflictExpert)
        self.btnUpdate.setGeometry(QtCore.QRect(100, 140, 121, 51))
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))

        self.retranslateUi(DialogConflictExpert)
        QtCore.QMetaObject.connectSlotsByName(DialogConflictExpert)

    def retranslateUi(self, DialogConflictExpert):
        DialogConflictExpert.setWindowTitle(_translate("DialogConflictExpert", "Configuration conflict - Expert mode", None))
        self.btnCancel.setToolTip(_translate("DialogConflictExpert", "Cancel driver\n"
"configuration", None))
        self.btnCancel.setText(_translate("DialogConflictExpert", "Cancel", None))
        self.btnMoreInfo.setToolTip(_translate("DialogConflictExpert", "Show values", None))
        self.btnMoreInfo.setText(_translate("DialogConflictExpert", "More info ...", None))
        self.label.setText(_translate("DialogConflictExpert", "The IcePAP database differs from the current configuration in the driver board.", None))
        self.label_2.setText(_translate("DialogConflictExpert", "An expert has probably configured the driver with an external tool.\n"
"\n"
"The current values in the database will be overwritten.", None))
        self.btnUpdate.setToolTip(_translate("DialogConflictExpert", "Update database with current\n"
"driver board configuration", None))
        self.btnUpdate.setText(_translate("DialogConflictExpert", "Update database", None))

