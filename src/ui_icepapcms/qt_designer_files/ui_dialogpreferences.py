# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogpreferences.ui'
#
# Created: Mon Oct  8 18:22:28 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogPreferences(object):
    def setupUi(self, DialogPreferences):
        DialogPreferences.setObjectName("DialogPreferences")
        DialogPreferences.resize(QtCore.QSize(QtCore.QRect(0,0,558,468).size()).expandedTo(DialogPreferences.minimumSizeHint()))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(16,16,16))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.WindowText,brush)

        brush = QtGui.QBrush(QtGui.QColor(239,235,231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Button,brush)

        brush = QtGui.QBrush(QtGui.QColor(237,237,237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Light,brush)

        brush = QtGui.QBrush(QtGui.QColor(247,245,243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Midlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(119,117,115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Dark,brush)

        brush = QtGui.QBrush(QtGui.QColor(159,157,154))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Mid,brush)

        brush = QtGui.QBrush(QtGui.QColor(16,16,16))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.BrightText,brush)

        brush = QtGui.QBrush(QtGui.QColor(16,16,16))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.ButtonText,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(239,235,231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Shadow,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.HighlightedText,brush)

        brush = QtGui.QBrush(QtGui.QColor(0,0,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Link,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,0,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.LinkVisited,brush)

        brush = QtGui.QBrush(QtGui.QColor(232,232,232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.AlternateBase,brush)

        brush = QtGui.QBrush(QtGui.QColor(16,16,16))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.WindowText,brush)

        brush = QtGui.QBrush(QtGui.QColor(239,235,231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Button,brush)

        brush = QtGui.QBrush(QtGui.QColor(237,237,237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Light,brush)

        brush = QtGui.QBrush(QtGui.QColor(247,245,243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Midlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(119,117,115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Dark,brush)

        brush = QtGui.QBrush(QtGui.QColor(159,157,154))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Mid,brush)

        brush = QtGui.QBrush(QtGui.QColor(16,16,16))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.BrightText,brush)

        brush = QtGui.QBrush(QtGui.QColor(16,16,16))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.ButtonText,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(239,235,231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Shadow,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.HighlightedText,brush)

        brush = QtGui.QBrush(QtGui.QColor(0,0,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Link,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,0,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.LinkVisited,brush)

        brush = QtGui.QBrush(QtGui.QColor(232,232,232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.AlternateBase,brush)

        brush = QtGui.QBrush(QtGui.QColor(127,125,123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.WindowText,brush)

        brush = QtGui.QBrush(QtGui.QColor(239,235,231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Button,brush)

        brush = QtGui.QBrush(QtGui.QColor(237,237,237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Light,brush)

        brush = QtGui.QBrush(QtGui.QColor(247,245,243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Midlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(119,117,115))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Dark,brush)

        brush = QtGui.QBrush(QtGui.QColor(159,157,154))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Mid,brush)

        brush = QtGui.QBrush(QtGui.QColor(127,125,123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.BrightText,brush)

        brush = QtGui.QBrush(QtGui.QColor(127,125,123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.ButtonText,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(239,235,231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Shadow,brush)

        brush = QtGui.QBrush(QtGui.QColor(84,123,196))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.HighlightedText,brush)

        brush = QtGui.QBrush(QtGui.QColor(0,0,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Link,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,0,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.LinkVisited,brush)

        brush = QtGui.QBrush(QtGui.QColor(232,232,232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.AlternateBase,brush)
        DialogPreferences.setPalette(palette)
        DialogPreferences.setWindowIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/preferences-system.png"))

        self.gridlayout = QtGui.QGridLayout(DialogPreferences)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.stackedWidget = QtGui.QStackedWidget(DialogPreferences)
        self.stackedWidget.setObjectName("stackedWidget")

        self.pageStorage = QtGui.QWidget()
        self.pageStorage.setObjectName("pageStorage")

        self.gridlayout1 = QtGui.QGridLayout(self.pageStorage)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,4,0,1,1)

        self.lblModules = QtGui.QLabel(self.pageStorage)

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.WindowText,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.WindowText,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(127,125,123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.WindowText,brush)

        brush = QtGui.QBrush(QtGui.QColor(127,125,123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Text,brush)
        self.lblModules.setPalette(palette)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.lblModules.setFont(font)
        self.lblModules.setObjectName("lblModules")
        self.gridlayout1.addWidget(self.lblModules,3,0,1,1)

        self.gbLocal = QtGui.QGroupBox(self.pageStorage)
        self.gbLocal.setObjectName("gbLocal")

        self.hboxlayout = QtGui.QHBoxLayout(self.gbLocal)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(self.gbLocal)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.txtLocalFolder = QtGui.QLineEdit(self.gbLocal)
        self.txtLocalFolder.setMaximumSize(QtCore.QSize(1666666,16777215))
        self.txtLocalFolder.setObjectName("txtLocalFolder")
        self.hboxlayout.addWidget(self.txtLocalFolder)

        self.btnBrowser = QtGui.QToolButton(self.gbLocal)
        self.btnBrowser.setObjectName("btnBrowser")
        self.hboxlayout.addWidget(self.btnBrowser)
        self.gridlayout1.addWidget(self.gbLocal,1,0,1,1)

        self.gbRemote = QtGui.QGroupBox(self.pageStorage)
        self.gbRemote.setObjectName("gbRemote")

        self.gridlayout2 = QtGui.QGridLayout(self.gbRemote)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem1 = QtGui.QSpacerItem(71,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem1,1,5,1,1)

        self.txtPassword = QtGui.QLineEdit(self.gbRemote)
        self.txtPassword.setMinimumSize(QtCore.QSize(150,0))
        self.txtPassword.setMaximumSize(QtCore.QSize(150,16777215))
        self.txtPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.txtPassword.setObjectName("txtPassword")
        self.gridlayout2.addWidget(self.txtPassword,1,3,1,2)

        self.txtPort = QtGui.QLineEdit(self.gbRemote)
        self.txtPort.setMaximumSize(QtCore.QSize(50,16777215))
        self.txtPort.setObjectName("txtPort")
        self.gridlayout2.addWidget(self.txtPort,0,3,1,1)

        self.label_3 = QtGui.QLabel(self.gbRemote)
        self.label_3.setObjectName("label_3")
        self.gridlayout2.addWidget(self.label_3,0,2,1,1)

        self.txtHost = QtGui.QLineEdit(self.gbRemote)
        self.txtHost.setMaximumSize(QtCore.QSize(200,16777215))
        self.txtHost.setObjectName("txtHost")
        self.gridlayout2.addWidget(self.txtHost,0,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem2,0,4,1,2)

        self.label_2 = QtGui.QLabel(self.gbRemote)
        self.label_2.setObjectName("label_2")
        self.gridlayout2.addWidget(self.label_2,0,0,1,1)

        self.label_4 = QtGui.QLabel(self.gbRemote)
        self.label_4.setObjectName("label_4")
        self.gridlayout2.addWidget(self.label_4,1,0,1,1)

        self.txtUser = QtGui.QLineEdit(self.gbRemote)
        self.txtUser.setMaximumSize(QtCore.QSize(150,16777215))
        self.txtUser.setObjectName("txtUser")
        self.gridlayout2.addWidget(self.txtUser,1,1,1,1)

        self.txPasswo = QtGui.QLabel(self.gbRemote)
        self.txPasswo.setObjectName("txPasswo")
        self.gridlayout2.addWidget(self.txPasswo,1,2,1,1)
        self.gridlayout1.addWidget(self.gbRemote,2,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.rbsqlite = QtGui.QRadioButton(self.pageStorage)
        self.rbsqlite.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rbsqlite.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/sqlite.png"))
        self.rbsqlite.setIconSize(QtCore.QSize(50,50))
        self.rbsqlite.setObjectName("rbsqlite")
        self.hboxlayout1.addWidget(self.rbsqlite)

        self.rbmysql = QtGui.QRadioButton(self.pageStorage)
        self.rbmysql.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/mysql.gif"))
        self.rbmysql.setIconSize(QtCore.QSize(50,50))
        self.rbmysql.setObjectName("rbmysql")
        self.hboxlayout1.addWidget(self.rbmysql)

        self.rbpostgres = QtGui.QRadioButton(self.pageStorage)
        self.rbpostgres.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/postgresql.png"))
        self.rbpostgres.setIconSize(QtCore.QSize(40,40))
        self.rbpostgres.setObjectName("rbpostgres")
        self.hboxlayout1.addWidget(self.rbpostgres)
        self.gridlayout1.addLayout(self.hboxlayout1,0,0,1,1)
        self.stackedWidget.addWidget(self.pageStorage)

        self.pageUsers = QtGui.QWidget()
        self.pageUsers.setObjectName("pageUsers")
        self.stackedWidget.addWidget(self.pageUsers)
        self.gridlayout.addWidget(self.stackedWidget,1,0,1,1)

        self.listWidget = QtGui.QListWidget(DialogPreferences)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(0,70))
        self.listWidget.setMaximumSize(QtCore.QSize(16777215,60))
        self.listWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.listWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.listWidget.setIconSize(QtCore.QSize(44,44))
        self.listWidget.setFlow(QtGui.QListView.LeftToRight)
        self.listWidget.setViewMode(QtGui.QListView.IconMode)
        self.listWidget.setModelColumn(0)
        self.listWidget.setUniformItemSizes(False)
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,0,0,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem3 = QtGui.QSpacerItem(131,31,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem3)

        self.closeButton = QtGui.QPushButton(DialogPreferences)
        self.closeButton.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/close.png"))
        self.closeButton.setIconSize(QtCore.QSize(22,22))
        self.closeButton.setObjectName("closeButton")
        self.hboxlayout2.addWidget(self.closeButton)
        self.gridlayout.addLayout(self.hboxlayout2,2,0,1,1)

        self.retranslateUi(DialogPreferences)
        self.stackedWidget.setCurrentIndex(0)
        self.listWidget.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(DialogPreferences)
        DialogPreferences.setTabOrder(self.rbsqlite,self.rbmysql)
        DialogPreferences.setTabOrder(self.rbmysql,self.rbpostgres)
        DialogPreferences.setTabOrder(self.rbpostgres,self.txtLocalFolder)
        DialogPreferences.setTabOrder(self.txtLocalFolder,self.btnBrowser)
        DialogPreferences.setTabOrder(self.btnBrowser,self.txtHost)
        DialogPreferences.setTabOrder(self.txtHost,self.txtPort)
        DialogPreferences.setTabOrder(self.txtPort,self.txtUser)
        DialogPreferences.setTabOrder(self.txtUser,self.txtPassword)
        DialogPreferences.setTabOrder(self.txtPassword,self.closeButton)
        DialogPreferences.setTabOrder(self.closeButton,self.listWidget)

    def retranslateUi(self, DialogPreferences):
        DialogPreferences.setWindowTitle(QtGui.QApplication.translate("DialogPreferences", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.lblModules.setText(QtGui.QApplication.translate("DialogPreferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:8pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">import modules</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.gbLocal.setTitle(QtGui.QApplication.translate("DialogPreferences", "Local storage", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogPreferences", "Local folder", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowser.setText(QtGui.QApplication.translate("DialogPreferences", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.gbRemote.setTitle(QtGui.QApplication.translate("DialogPreferences", "Remote storage", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogPreferences", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogPreferences", "Host", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DialogPreferences", "User", None, QtGui.QApplication.UnicodeUTF8))
        self.txPasswo.setText(QtGui.QApplication.translate("DialogPreferences", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.rbsqlite.setText(QtGui.QApplication.translate("DialogPreferences", "Sqlite", None, QtGui.QApplication.UnicodeUTF8))
        self.rbmysql.setText(QtGui.QApplication.translate("DialogPreferences", "MySql", None, QtGui.QApplication.UnicodeUTF8))
        self.rbpostgres.setText(QtGui.QApplication.translate("DialogPreferences", "Postgres", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.clear()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setText(QtGui.QApplication.translate("DialogPreferences", "Storage", None, QtGui.QApplication.UnicodeUTF8))
        item.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/database.png"))
        self.closeButton.setText(QtGui.QApplication.translate("DialogPreferences", "Close", None, QtGui.QApplication.UnicodeUTF8))

import icepapcms_rc