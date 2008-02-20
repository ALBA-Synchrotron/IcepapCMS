# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ipapconsole.ui'
#
# Created: Wed Feb 20 15:23:24 2008
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IpapConsole(object):
    def setupUi(self, IpapConsole):
        IpapConsole.setObjectName("IpapConsole")
        IpapConsole.resize(QtCore.QSize(QtCore.QRect(0,0,648,477).size()).expandedTo(IpapConsole.minimumSizeHint()))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Shadow,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Shadow,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Shadow,brush)

        brush = QtGui.QBrush(QtGui.QColor(127,125,123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Highlight,brush)
        IpapConsole.setPalette(palette)
        IpapConsole.setWindowIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-terminal.png"))

        self.gridlayout = QtGui.QGridLayout(IpapConsole)
        self.gridlayout.setMargin(3)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(IpapConsole)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,0,2,1,1)

        self.txtHost = QtGui.QLineEdit(IpapConsole)
        self.txtHost.setObjectName("txtHost")
        self.gridlayout.addWidget(self.txtHost,0,1,1,1)

        self.btnDisconnect = QtGui.QPushButton(IpapConsole)
        self.btnDisconnect.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/disconnect.png"))
        self.btnDisconnect.setIconSize(QtCore.QSize(24,24))
        self.btnDisconnect.setObjectName("btnDisconnect")
        self.gridlayout.addWidget(self.btnDisconnect,0,4,1,1)

        self.btnConnect = QtGui.QPushButton(IpapConsole)
        self.btnConnect.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/connect.png"))
        self.btnConnect.setIconSize(QtCore.QSize(24,24))
        self.btnConnect.setObjectName("btnConnect")
        self.gridlayout.addWidget(self.btnConnect,0,3,1,1)

        self.console = PyConsoleText(IpapConsole)
        self.console.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.console.setUndoRedoEnabled(False)
        self.console.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        self.console.setAcceptRichText(False)
        self.console.setObjectName("console")
        self.gridlayout.addWidget(self.console,1,0,1,5)

        self.retranslateUi(IpapConsole)
        QtCore.QMetaObject.connectSlotsByName(IpapConsole)
        IpapConsole.setTabOrder(self.txtHost,self.btnConnect)
        IpapConsole.setTabOrder(self.btnConnect,self.btnDisconnect)
        IpapConsole.setTabOrder(self.btnDisconnect,self.console)

    def retranslateUi(self, IpapConsole):
        IpapConsole.setWindowTitle(QtGui.QApplication.translate("IpapConsole", "Icepap Console", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IpapConsole", "Icepap host", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDisconnect.setText(QtGui.QApplication.translate("IpapConsole", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.btnConnect.setText(QtGui.QApplication.translate("IpapConsole", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.console.setStyleSheet(QtGui.QApplication.translate("IpapConsole", "QTextEdit { \n"
        "background-color: rgba(0, 0, 0, 100%)\n"
        "}", None, QtGui.QApplication.UnicodeUTF8))

from pyconsoletext import PyConsoleText
import icepapcms_rc
