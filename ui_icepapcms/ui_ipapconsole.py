# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ipapconsole.ui'
#
# Created: Wed Feb 26 18:21:28 2014
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IpapConsole(object):
    def setupUi(self, IpapConsole):
        IpapConsole.setObjectName("IpapConsole")
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
        icon.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/gnome-terminal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        IpapConsole.setWindowIcon(icon)
        self.gridlayout = QtGui.QGridLayout(IpapConsole)
        self.gridlayout.setMargin(3)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName("gridlayout")
        self.label = QtGui.QLabel(IpapConsole)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 2, 1, 1)
        self.txtHost = QtGui.QLineEdit(IpapConsole)
        self.txtHost.setObjectName("txtHost")
        self.gridlayout.addWidget(self.txtHost, 0, 1, 1, 1)
        self.btnDisconnect = QtGui.QPushButton(IpapConsole)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/disconnect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDisconnect.setIcon(icon1)
        self.btnDisconnect.setIconSize(QtCore.QSize(24, 24))
        self.btnDisconnect.setObjectName("btnDisconnect")
        self.gridlayout.addWidget(self.btnDisconnect, 0, 4, 1, 1)
        self.btnConnect = QtGui.QPushButton(IpapConsole)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/connect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnConnect.setIcon(icon2)
        self.btnConnect.setIconSize(QtCore.QSize(24, 24))
        self.btnConnect.setObjectName("btnConnect")
        self.gridlayout.addWidget(self.btnConnect, 0, 3, 1, 1)
        self.console = PyConsoleText(IpapConsole)
        self.console.setProperty("cursor", QtCore.QVariant(QtCore.Qt.IBeamCursor))
        self.console.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.console.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.console.setUndoRedoEnabled(False)
        self.console.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.console.setAcceptRichText(False)
        self.console.setCursorWidth(5)
        self.console.setObjectName("console")
        self.gridlayout.addWidget(self.console, 1, 0, 1, 5)

        self.retranslateUi(IpapConsole)
        QtCore.QMetaObject.connectSlotsByName(IpapConsole)
        IpapConsole.setTabOrder(self.txtHost, self.btnConnect)
        IpapConsole.setTabOrder(self.btnConnect, self.btnDisconnect)
        IpapConsole.setTabOrder(self.btnDisconnect, self.console)

    def retranslateUi(self, IpapConsole):
        IpapConsole.setWindowTitle(QtGui.QApplication.translate("IpapConsole", "Icepap Console", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IpapConsole", "Icepap host", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDisconnect.setText(QtGui.QApplication.translate("IpapConsole", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.btnConnect.setText(QtGui.QApplication.translate("IpapConsole", "Connect", None, QtGui.QApplication.UnicodeUTF8))

from pyconsoletext import PyConsoleText
import icepapcms_rc
