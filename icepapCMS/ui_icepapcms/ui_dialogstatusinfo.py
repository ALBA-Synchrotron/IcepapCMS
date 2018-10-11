# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogstatusinfo.ui'
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

class Ui_DialogStatusInfo(object):
    def setupUi(self, DialogStatusInfo):
        DialogStatusInfo.setObjectName(_fromUtf8("DialogStatusInfo"))
        DialogStatusInfo.resize(428, 550)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogStatusInfo.sizePolicy().hasHeightForWidth())
        DialogStatusInfo.setSizePolicy(sizePolicy)
        DialogStatusInfo.setMinimumSize(QtCore.QSize(50, 0))
        self.verticalLayout_2 = QtGui.QVBoxLayout(DialogStatusInfo)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textBrowser = QtGui.QTextBrowser(DialogStatusInfo)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnUpdate = QtGui.QPushButton(DialogStatusInfo)
        self.btnUpdate.setObjectName(_fromUtf8("btnUpdate"))
        self.horizontalLayout.addWidget(self.btnUpdate)
        self.btnEsync = QtGui.QPushButton(DialogStatusInfo)
        self.btnEsync.setObjectName(_fromUtf8("btnEsync"))
        self.horizontalLayout.addWidget(self.btnEsync)
        self.txt1Command = QtGui.QLineEdit(DialogStatusInfo)
        self.txt1Command.setObjectName(_fromUtf8("txt1Command"))
        self.horizontalLayout.addWidget(self.txt1Command)
        self.cbAllDrivers = QtGui.QComboBox(DialogStatusInfo)
        self.cbAllDrivers.setEditable(True)
        self.cbAllDrivers.setObjectName(_fromUtf8("cbAllDrivers"))
        self.horizontalLayout.addWidget(self.cbAllDrivers)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(DialogStatusInfo)
        QtCore.QMetaObject.connectSlotsByName(DialogStatusInfo)

    def retranslateUi(self, DialogStatusInfo):
        DialogStatusInfo.setWindowTitle(_translate("DialogStatusInfo", "Status Info", None))
        self.btnUpdate.setText(_translate("DialogStatusInfo", "VSTATUS", None))
        self.btnEsync.setText(_translate("DialogStatusInfo", "ESYNC", None))

