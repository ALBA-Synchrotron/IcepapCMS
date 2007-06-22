# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icepapcms.ui'
#
# Created: Mon Jun 11 16:03:53 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IcepapCMS(object):
    def setupUi(self, IcepapCMS):
        IcepapCMS.setObjectName("IcepapCMS")
        IcepapCMS.resize(QtCore.QSize(QtCore.QRect(0,0,1100,801).size()).expandedTo(IcepapCMS.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(IcepapCMS.sizePolicy().hasHeightForWidth())
        IcepapCMS.setSizePolicy(sizePolicy)

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Highlight,brush)

        brush = QtGui.QBrush(QtGui.QColor(127,125,123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Highlight,brush)
        IcepapCMS.setPalette(palette)
        IcepapCMS.setWindowIcon(QtGui.QIcon(":/small_icons/IcepapCfg Icons/Icepapicon.png"))

        self.centralwidget = QtGui.QWidget(IcepapCMS)
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setMargin(1)
        self.vboxlayout.setSpacing(1)
        self.vboxlayout.setObjectName("vboxlayout")

        self.frLocationBar = QtGui.QFrame(self.centralwidget)
        self.frLocationBar.setFrameShape(QtGui.QFrame.NoFrame)
        self.frLocationBar.setFrameShadow(QtGui.QFrame.Raised)
        self.frLocationBar.setObjectName("frLocationBar")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.frLocationBar)
        self.vboxlayout1.setMargin(1)
        self.vboxlayout1.setSpacing(1)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.frLocationBarText = QtGui.QFrame(self.frLocationBar)
        self.frLocationBarText.setMinimumSize(QtCore.QSize(16,40))
        self.frLocationBarText.setFrameShape(QtGui.QFrame.NoFrame)
        self.frLocationBarText.setFrameShadow(QtGui.QFrame.Raised)
        self.frLocationBarText.setObjectName("frLocationBarText")

        self.hboxlayout = QtGui.QHBoxLayout(self.frLocationBarText)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.lblLocation = QtGui.QLabel(self.frLocationBarText)
        self.lblLocation.setMaximumSize(QtCore.QSize(58,16777215))
        self.lblLocation.setObjectName("lblLocation")
        self.hboxlayout.addWidget(self.lblLocation)

        self.txtLocation = QtGui.QLineEdit(self.frLocationBarText)
        self.txtLocation.setObjectName("txtLocation")
        self.hboxlayout.addWidget(self.txtLocation)
        self.vboxlayout1.addWidget(self.frLocationBarText)

        self.line = QtGui.QFrame(self.frLocationBar)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout1.addWidget(self.line)
        self.vboxlayout.addWidget(self.frLocationBar)

        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setMinimumSize(QtCore.QSize(16,16))
        self.stackedWidget.setObjectName("stackedWidget")

        self.StartPage = QtGui.QWidget()
        self.StartPage.setObjectName("StartPage")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.StartPage)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.lblStartPage = QtGui.QLabel(self.StartPage)
        self.lblStartPage.setPixmap(QtGui.QPixmap(":/logos/IcepapCfg Icons/IcepapBig.png"))
        self.lblStartPage.setObjectName("lblStartPage")
        self.hboxlayout1.addWidget(self.lblStartPage)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.StartPage)
        self.vboxlayout.addWidget(self.stackedWidget)
        IcepapCMS.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(IcepapCMS)
        self.menubar.setGeometry(QtCore.QRect(0,0,1100,29))
        self.menubar.setObjectName("menubar")

        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        self.menuGo = QtGui.QMenu(self.menubar)
        self.menuGo.setObjectName("menuGo")

        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        IcepapCMS.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(IcepapCMS)
        self.statusbar.setObjectName("statusbar")
        IcepapCMS.setStatusBar(self.statusbar)

        self.toolBar = QtGui.QToolBar(IcepapCMS)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMovable(False)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(32,32))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        IcepapCMS.addToolBar(self.toolBar)

        self.dockTree = QtGui.QDockWidget(IcepapCMS)
        self.dockTree.setMinimumSize(QtCore.QSize(150,16))
        self.dockTree.setMaximumSize(QtCore.QSize(350,16777215))
        self.dockTree.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.dockTree.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockTree.setObjectName("dockTree")

        self.dockWidgetContents = QtGui.QWidget(self.dockTree)
        self.dockWidgetContents.setObjectName("dockWidgetContents")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.frame = QtGui.QFrame(self.dockWidgetContents)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.frame)
        self.hboxlayout2.setMargin(4)
        self.hboxlayout2.setSpacing(4)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.btnTreeRefresh = QtGui.QToolButton(self.frame)
        self.btnTreeRefresh.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/view-refresh.png"))
        self.btnTreeRefresh.setIconSize(QtCore.QSize(16,16))
        self.btnTreeRefresh.setObjectName("btnTreeRefresh")
        self.hboxlayout2.addWidget(self.btnTreeRefresh)

        self.btnTreeAdd = QtGui.QToolButton(self.frame)
        self.btnTreeAdd.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/list-add.png"))
        self.btnTreeAdd.setIconSize(QtCore.QSize(16,16))
        self.btnTreeAdd.setObjectName("btnTreeAdd")
        self.hboxlayout2.addWidget(self.btnTreeAdd)

        self.btnTreeRemove = QtGui.QToolButton(self.frame)
        self.btnTreeRemove.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/list-remove.png"))
        self.btnTreeRemove.setIconSize(QtCore.QSize(16,16))
        self.btnTreeRemove.setObjectName("btnTreeRemove")
        self.hboxlayout2.addWidget(self.btnTreeRemove)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem2)
        self.vboxlayout2.addWidget(self.frame)

        self.treeView = QtGui.QTreeView(self.dockWidgetContents)
        self.treeView.setIconSize(QtCore.QSize(22,22))
        self.treeView.setObjectName("treeView")
        self.vboxlayout2.addWidget(self.treeView)
        self.dockTree.setWidget(self.dockWidgetContents)
        IcepapCMS.addDockWidget(QtCore.Qt.DockWidgetArea(1),self.dockTree)

        self.actionAbout = QtGui.QAction(IcepapCMS)
        self.actionAbout.setObjectName("actionAbout")

        self.actionTree_Explorer = QtGui.QAction(IcepapCMS)
        self.actionTree_Explorer.setCheckable(True)
        self.actionTree_Explorer.setChecked(True)
        self.actionTree_Explorer.setObjectName("actionTree_Explorer")

        self.actionGoNext = QtGui.QAction(IcepapCMS)
        self.actionGoNext.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/go-next.png"))
        self.actionGoNext.setObjectName("actionGoNext")

        self.actionGoPrevious = QtGui.QAction(IcepapCMS)
        self.actionGoPrevious.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/go-previous.png"))
        self.actionGoPrevious.setObjectName("actionGoPrevious")

        self.actionGoUp = QtGui.QAction(IcepapCMS)
        self.actionGoUp.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/go-up.png"))
        self.actionGoUp.setObjectName("actionGoUp")

        self.actionRefresh = QtGui.QAction(IcepapCMS)
        self.actionRefresh.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/view-refresh.png"))
        self.actionRefresh.setObjectName("actionRefresh")

        self.actionPreferences = QtGui.QAction(IcepapCMS)
        self.actionPreferences.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-settings.png"))
        self.actionPreferences.setObjectName("actionPreferences")

        self.actionHelp = QtGui.QAction(IcepapCMS)
        self.actionHelp.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/help-browser.png"))
        self.actionHelp.setObjectName("actionHelp")

        self.actionExport = QtGui.QAction(IcepapCMS)
        self.actionExport.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-dev-floppy.png"))
        self.actionExport.setObjectName("actionExport")

        self.actionImport = QtGui.QAction(IcepapCMS)
        self.actionImport.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/folder.png"))
        self.actionImport.setObjectName("actionImport")

        self.actionQuit = QtGui.QAction(IcepapCMS)
        self.actionQuit.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-logout.png"))
        self.actionQuit.setObjectName("actionQuit")

        self.actionToolbar = QtGui.QAction(IcepapCMS)
        self.actionToolbar.setCheckable(True)
        self.actionToolbar.setChecked(True)
        self.actionToolbar.setObjectName("actionToolbar")

        self.actionSignConfig = QtGui.QAction(IcepapCMS)
        self.actionSignConfig.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/keys.png"))
        self.actionSignConfig.setObjectName("actionSignConfig")

        self.actionFirmwareUpgrade = QtGui.QAction(IcepapCMS)
        self.actionFirmwareUpgrade.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-cpu.png"))
        self.actionFirmwareUpgrade.setObjectName("actionFirmwareUpgrade")

        self.actionConsole = QtGui.QAction(IcepapCMS)
        self.actionConsole.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-terminal.png"))
        self.actionConsole.setObjectName("actionConsole")
        self.menuEdit.addAction(self.actionPreferences)
        self.menuGo.addAction(self.actionGoPrevious)
        self.menuGo.addAction(self.actionGoNext)
        self.menuGo.addAction(self.actionGoUp)
        self.menuGo.addAction(self.actionRefresh)
        self.menuView.addAction(self.actionTree_Explorer)
        self.menuView.addAction(self.actionToolbar)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionFirmwareUpgrade)
        self.menuFile.addAction(self.actionConsole)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuGo.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionGoPrevious)
        self.toolBar.addAction(self.actionGoNext)
        self.toolBar.addAction(self.actionGoUp)
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExport)
        self.toolBar.addAction(self.actionImport)
        self.toolBar.addAction(self.actionSignConfig)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPreferences)
        self.toolBar.addAction(self.actionConsole)
        self.toolBar.addAction(self.actionHelp)
        self.toolBar.addAction(self.actionQuit)

        self.retranslateUi(IcepapCMS)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(IcepapCMS)

    def retranslateUi(self, IcepapCMS):
        IcepapCMS.setWindowTitle(QtGui.QApplication.translate("IcepapCMS", "Icepap configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.lblLocation.setText(QtGui.QApplication.translate("IcepapCMS", "Location:", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("IcepapCMS", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGo.setTitle(QtGui.QApplication.translate("IcepapCMS", "Go", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("IcepapCMS", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("IcepapCMS", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("IcepapCMS", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("IcepapCMS", "Toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.dockTree.setWindowTitle(QtGui.QApplication.translate("IcepapCMS", "Tree Explorer", None, QtGui.QApplication.UnicodeUTF8))
        self.btnTreeRefresh.setText(QtGui.QApplication.translate("IcepapCMS", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnTreeAdd.setText(QtGui.QApplication.translate("IcepapCMS", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.btnTreeRemove.setText(QtGui.QApplication.translate("IcepapCMS", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("IcepapCMS", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTree_Explorer.setText(QtGui.QApplication.translate("IcepapCMS", "Tree Explorer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTree_Explorer.setShortcut(QtGui.QApplication.translate("IcepapCMS", "F8", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoNext.setText(QtGui.QApplication.translate("IcepapCMS", "Go Next", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoNext.setStatusTip(QtGui.QApplication.translate("IcepapCMS", "444", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoNext.setWhatsThis(QtGui.QApplication.translate("IcepapCMS", "5555", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoNext.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Alt+Right", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoPrevious.setText(QtGui.QApplication.translate("IcepapCMS", "Go Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoPrevious.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Alt+Left", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoUp.setText(QtGui.QApplication.translate("IcepapCMS", "Go Up", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoUp.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Alt+Up", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setText(QtGui.QApplication.translate("IcepapCMS", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRefresh.setShortcut(QtGui.QApplication.translate("IcepapCMS", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("IcepapCMS", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("IcepapCMS", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setShortcut(QtGui.QApplication.translate("IcepapCMS", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(QtGui.QApplication.translate("IcepapCMS", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setText(QtGui.QApplication.translate("IcepapCMS", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("IcepapCMS", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToolbar.setText(QtGui.QApplication.translate("IcepapCMS", "Toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToolbar.setShortcut(QtGui.QApplication.translate("IcepapCMS", "F9", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSignConfig.setText(QtGui.QApplication.translate("IcepapCMS", "Sign Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFirmwareUpgrade.setText(QtGui.QApplication.translate("IcepapCMS", "Firmware upgrade", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConsole.setText(QtGui.QApplication.translate("IcepapCMS", "Console", None, QtGui.QApplication.UnicodeUTF8))

import qrc_icepapcms
