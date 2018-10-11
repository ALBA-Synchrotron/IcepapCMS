# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialognewdriver.ui'
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

class Ui_DialogNewDriver(object):
    def setupUi(self, DialogNewDriver):
        DialogNewDriver.setObjectName(_fromUtf8("DialogNewDriver"))
        DialogNewDriver.resize(471, 242)
        self.btnMoreInfo = QtGui.QPushButton(DialogNewDriver)
        self.btnMoreInfo.setGeometry(QtCore.QRect(360, 210, 100, 26))
        self.btnMoreInfo.setObjectName(_fromUtf8("btnMoreInfo"))
        self.btnUseDefaults = QtGui.QPushButton(DialogNewDriver)
        self.btnUseDefaults.setGeometry(QtCore.QRect(40, 140, 121, 51))
        self.btnUseDefaults.setObjectName(_fromUtf8("btnUseDefaults"))
        self.label = QtGui.QLabel(DialogNewDriver)
        self.label.setGeometry(QtCore.QRect(10, 10, 461, 41))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.btnCancel = QtGui.QPushButton(DialogNewDriver)
        self.btnCancel.setGeometry(QtCore.QRect(350, 140, 100, 51))
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.label_2 = QtGui.QLabel(DialogNewDriver)
        self.label_2.setGeometry(QtCore.QRect(50, 50, 391, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.btnUseDriver = QtGui.QPushButton(DialogNewDriver)
        self.btnUseDriver.setGeometry(QtCore.QRect(190, 140, 131, 51))
        self.btnUseDriver.setObjectName(_fromUtf8("btnUseDriver"))
        self.lblExpertInfo = QtGui.QLabel(DialogNewDriver)
        self.lblExpertInfo.setGeometry(QtCore.QRect(50, 80, 391, 31))
        self.lblExpertInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblExpertInfo.setObjectName(_fromUtf8("lblExpertInfo"))

        self.retranslateUi(DialogNewDriver)
        QtCore.QMetaObject.connectSlotsByName(DialogNewDriver)

    def retranslateUi(self, DialogNewDriver):
        DialogNewDriver.setWindowTitle(_translate("DialogNewDriver", "New driver", None))
        self.btnMoreInfo.setToolTip(_translate("DialogNewDriver", "Show values", None))
        self.btnMoreInfo.setText(_translate("DialogNewDriver", "More info ...", None))
        self.btnUseDefaults.setToolTip(_translate("DialogNewDriver", "Set config to default\n"
"values and update the database", None))
        self.btnUseDefaults.setText(_translate("DialogNewDriver", "Use default values", None))
        self.label.setText(_translate("DialogNewDriver", "This driver board has been added to the system.", None))
        self.btnCancel.setToolTip(_translate("DialogNewDriver", "Cancel driver\n"
"configuration", None))
        self.btnCancel.setText(_translate("DialogNewDriver", "Cancel", None))
        self.label_2.setText(_translate("DialogNewDriver", "The driver configuration has to be initialized.", None))
        self.btnUseDriver.setToolTip(_translate("DialogNewDriver", "Update database\n"
"with current driver config", None))
        self.btnUseDriver.setText(_translate("DialogNewDriver", "Use values in the\n"
"driver board", None))
        self.lblExpertInfo.setText(_translate("DialogNewDriver", "The driver board seems to be already configured by an expert.", None))

