# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogpreferences.ui'
#
# Created: Fri Aug 31 17:16:52 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogPreferences(object):
    def setupUi(self, DialogPreferences):
        DialogPreferences.setObjectName("DialogPreferences")
        DialogPreferences.resize(QtCore.QSize(QtCore.QRect(0,0,558,404).size()).expandedTo(DialogPreferences.minimumSizeHint()))

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

        self.vboxlayout = QtGui.QVBoxLayout(DialogPreferences)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

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
        self.vboxlayout.addWidget(self.listWidget)

        self.stackedWidget = QtGui.QStackedWidget(DialogPreferences)
        self.stackedWidget.setObjectName("stackedWidget")

        self.pageStorage = QtGui.QWidget()
        self.pageStorage.setObjectName("pageStorage")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.pageStorage)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.rbLocal = QtGui.QRadioButton(self.pageStorage)
        self.rbLocal.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rbLocal.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-dev-harddisk.png"))
        self.rbLocal.setIconSize(QtCore.QSize(40,40))
        self.rbLocal.setObjectName("rbLocal")
        self.hboxlayout.addWidget(self.rbLocal)

        self.rbRemote = QtGui.QRadioButton(self.pageStorage)
        self.rbRemote.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-dev-network.png"))
        self.rbRemote.setIconSize(QtCore.QSize(40,40))
        self.rbRemote.setObjectName("rbRemote")
        self.hboxlayout.addWidget(self.rbRemote)
        self.vboxlayout1.addLayout(self.hboxlayout)

        self.gbLocal = QtGui.QGroupBox(self.pageStorage)
        self.gbLocal.setObjectName("gbLocal")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.gbLocal)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(self.gbLocal)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.txtLocalFolder = QtGui.QLineEdit(self.gbLocal)
        self.txtLocalFolder.setMaximumSize(QtCore.QSize(1666666,16777215))
        self.txtLocalFolder.setObjectName("txtLocalFolder")
        self.hboxlayout1.addWidget(self.txtLocalFolder)

        self.btnBrowser = QtGui.QToolButton(self.gbLocal)
        self.btnBrowser.setObjectName("btnBrowser")
        self.hboxlayout1.addWidget(self.btnBrowser)
        self.vboxlayout1.addWidget(self.gbLocal)

        self.gbRemote = QtGui.QGroupBox(self.pageStorage)
        self.gbRemote.setObjectName("gbRemote")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.gbRemote)
        self.hboxlayout2.setMargin(9)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_2 = QtGui.QLabel(self.gbRemote)
        self.label_2.setObjectName("label_2")
        self.hboxlayout2.addWidget(self.label_2)

        self.txtHost = QtGui.QLineEdit(self.gbRemote)
        self.txtHost.setMaximumSize(QtCore.QSize(200,16777215))
        self.txtHost.setObjectName("txtHost")
        self.hboxlayout2.addWidget(self.txtHost)

        self.label_3 = QtGui.QLabel(self.gbRemote)
        self.label_3.setObjectName("label_3")
        self.hboxlayout2.addWidget(self.label_3)

        self.txtPort = QtGui.QLineEdit(self.gbRemote)
        self.txtPort.setMaximumSize(QtCore.QSize(50,16777215))
        self.txtPort.setObjectName("txtPort")
        self.hboxlayout2.addWidget(self.txtPort)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem)
        self.vboxlayout1.addWidget(self.gbRemote)

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.pageStorage)

        self.pageUsers = QtGui.QWidget()
        self.pageUsers.setObjectName("pageUsers")
        self.stackedWidget.addWidget(self.pageUsers)
        self.vboxlayout.addWidget(self.stackedWidget)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        spacerItem2 = QtGui.QSpacerItem(131,31,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem2)

        self.closeButton = QtGui.QPushButton(DialogPreferences)
        self.closeButton.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/close.png"))
        self.closeButton.setIconSize(QtCore.QSize(22,22))
        self.closeButton.setObjectName("closeButton")
        self.hboxlayout3.addWidget(self.closeButton)
        self.vboxlayout.addLayout(self.hboxlayout3)

        self.retranslateUi(DialogPreferences)
        self.listWidget.setCurrentRow(-1)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DialogPreferences)

    def retranslateUi(self, DialogPreferences):
        DialogPreferences.setWindowTitle(QtGui.QApplication.translate("DialogPreferences", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.clear()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setText(QtGui.QApplication.translate("DialogPreferences", "Storage", None, QtGui.QApplication.UnicodeUTF8))
        item.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/file-roller.png"))
        self.rbLocal.setText(QtGui.QApplication.translate("DialogPreferences", "Local storage", None, QtGui.QApplication.UnicodeUTF8))
        self.rbRemote.setText(QtGui.QApplication.translate("DialogPreferences", "Remote storage", None, QtGui.QApplication.UnicodeUTF8))
        self.gbLocal.setTitle(QtGui.QApplication.translate("DialogPreferences", "Local storage", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogPreferences", "Local folder", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowser.setText(QtGui.QApplication.translate("DialogPreferences", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.gbRemote.setTitle(QtGui.QApplication.translate("DialogPreferences", "Remote storage", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogPreferences", "Host", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogPreferences", "Port", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("DialogPreferences", "Close", None, QtGui.QApplication.UnicodeUTF8))

import icepapcms_rc
