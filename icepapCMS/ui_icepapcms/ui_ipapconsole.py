# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ipapconsole.ui'
#
# Created: Fri Feb  9 13:20:39 2018
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

class Ui_IpapConsole(object):
    def setupUi(self, IpapConsole):
        IpapConsole.setObjectName(_fromUtf8("IpapConsole"))
        IpapConsole.resize(648, 477)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(101, 148, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(101, 148, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(101, 148, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(101, 148, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(101, 148, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        IpapConsole.setPalette(palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/IcepapCfg Icons/gnome-terminal.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        IpapConsole.setWindowIcon(icon)
        IpapConsole.setStyleSheet(_fromUtf8(""))
        self.gridlayout = QtGui.QGridLayout(IpapConsole)
        self.gridlayout.setMargin(3)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label = QtGui.QLabel(IpapConsole)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 2, 1, 1)
        self.txtHost = QtGui.QLineEdit(IpapConsole)
        self.txtHost.setObjectName(_fromUtf8("txtHost"))
        self.gridlayout.addWidget(self.txtHost, 0, 1, 1, 1)
        self.btnDisconnect = QtGui.QPushButton(IpapConsole)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/IcepapCfg Icons/disconnect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDisconnect.setIcon(icon1)
        self.btnDisconnect.setIconSize(QtCore.QSize(24, 24))
        self.btnDisconnect.setObjectName(_fromUtf8("btnDisconnect"))
        self.gridlayout.addWidget(self.btnDisconnect, 0, 4, 1, 1)
        self.btnConnect = QtGui.QPushButton(IpapConsole)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/IcepapCfg Icons/connect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnConnect.setIcon(icon2)
        self.btnConnect.setIconSize(QtCore.QSize(24, 24))
        self.btnConnect.setObjectName(_fromUtf8("btnConnect"))
        self.gridlayout.addWidget(self.btnConnect, 0, 3, 1, 1)
        self.console = PyConsoleText(IpapConsole)
        self.console.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.console.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.console.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.console.setUndoRedoEnabled(False)
        self.console.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.console.setAcceptRichText(False)
        self.console.setCursorWidth(5)
        self.console.setObjectName(_fromUtf8("console"))
        self.gridlayout.addWidget(self.console, 1, 0, 1, 5)

        self.retranslateUi(IpapConsole)
        QtCore.QMetaObject.connectSlotsByName(IpapConsole)
        IpapConsole.setTabOrder(self.txtHost, self.btnConnect)
        IpapConsole.setTabOrder(self.btnConnect, self.btnDisconnect)
        IpapConsole.setTabOrder(self.btnDisconnect, self.console)

    def retranslateUi(self, IpapConsole):
        IpapConsole.setWindowTitle(_translate("IpapConsole", "Icepap Console", None))
        self.label.setText(_translate("IpapConsole", "Icepap host", None))
        self.btnDisconnect.setText(_translate("IpapConsole", "Disconnect", None))
        self.btnConnect.setText(_translate("IpapConsole", "Connect", None))

from pyconsoletext import PyConsoleText
import icepapcms_rc
