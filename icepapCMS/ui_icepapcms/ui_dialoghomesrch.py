# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialoghomesrch.ui'
#
# Created: Thu Dec  6 06:52:15 2018
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

class Ui_DialogHomeSrch(object):
    def setupUi(self, DialogHomeSrch):
        DialogHomeSrch.setObjectName(_fromUtf8("DialogHomeSrch"))
        DialogHomeSrch.resize(400, 300)
        self.bbClose = QtGui.QDialogButtonBox(DialogHomeSrch)
        self.bbClose.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.bbClose.setOrientation(QtCore.Qt.Horizontal)
        self.bbClose.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.bbClose.setObjectName(_fromUtf8("bbClose"))

        self.retranslateUi(DialogHomeSrch)
        QtCore.QObject.connect(self.bbClose, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogHomeSrch.accept)
        QtCore.QObject.connect(self.bbClose, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogHomeSrch.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogHomeSrch)

    def retranslateUi(self, DialogHomeSrch):
        DialogHomeSrch.setWindowTitle(_translate("DialogHomeSrch", "Dialog", None))

