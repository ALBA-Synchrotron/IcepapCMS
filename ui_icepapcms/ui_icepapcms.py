# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icepapcms.ui'
#
# Created: Mon Aug  3 17:26:45 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IcepapCMS(object):
    def setupUi(self, IcepapCMS):
        IcepapCMS.setObjectName("IcepapCMS")
        IcepapCMS.resize(1100, 804)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(IcepapCMS.sizePolicy().hasHeightForWidth())
        IcepapCMS.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(101, 148, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(101, 148, 235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        IcepapCMS.setPalette(palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/small_icons/IcepapCfg Icons/Icepapicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        IcepapCMS.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(IcepapCMS)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setSpacing(1)
        self.vboxlayout.setMargin(1)
        self.vboxlayout.setObjectName("vboxlayout")
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setMinimumSize(QtCore.QSize(16, 16))
        self.stackedWidget.setObjectName("stackedWidget")
        self.StartPage = QtGui.QWidget()
        self.StartPage.setObjectName("StartPage")
        self.hboxlayout = QtGui.QHBoxLayout(self.StartPage)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.lblStartPage = QtGui.QLabel(self.StartPage)
        self.lblStartPage.setPixmap(QtGui.QPixmap(":/logos/IcepapCfg Icons/IcepapBig.png"))
        self.lblStartPage.setObjectName("lblStartPage")
        self.hboxlayout.addWidget(self.lblStartPage)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.StartPage)
        self.vboxlayout.addWidget(self.stackedWidget)
        IcepapCMS.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(IcepapCMS)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 24))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuDriver = QtGui.QMenu(self.menubar)
        self.menuDriver.setObjectName("menuDriver")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        IcepapCMS.setMenuBar(self.menubar)
        self.toolBar = QtGui.QToolBar(IcepapCMS)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setMovable(False)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        IcepapCMS.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockTree = QtGui.QDockWidget(IcepapCMS)
        self.dockTree.setMinimumSize(QtCore.QSize(260, 278))
        self.dockTree.setMaximumSize(QtCore.QSize(524287, 524287))
        self.dockTree.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.dockTree.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockTree.setObjectName("dockTree")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_2 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtGui.QFrame(self.dockWidgetContents)
        self.frame.setObjectName("frame")
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.frame)
        self.label.setMaximumSize(QtCore.QSize(51, 16777215))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.cbLocation = QtGui.QComboBox(self.frame)
        self.cbLocation.setMinimumSize(QtCore.QSize(100, 0))
        self.cbLocation.setMaximumSize(QtCore.QSize(141, 16777215))
        self.cbLocation.setEditable(False)
        self.cbLocation.setObjectName("cbLocation")
        self.horizontalLayout.addWidget(self.cbLocation)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.btnTreeAdd = QtGui.QToolButton(self.frame)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/small_icons/IcepapCFG Icons Petits/list-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnTreeAdd.setIcon(icon1)
        self.btnTreeAdd.setIconSize(QtCore.QSize(16, 16))
        self.btnTreeAdd.setObjectName("btnTreeAdd")
        self.horizontalLayout_2.addWidget(self.btnTreeAdd)
        self.btnTreeRemove = QtGui.QToolButton(self.frame)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/small_icons/IcepapCFG Icons Petits/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnTreeRemove.setIcon(icon2)
        self.btnTreeRemove.setIconSize(QtCore.QSize(16, 16))
        self.btnTreeRemove.setObjectName("btnTreeRemove")
        self.horizontalLayout_2.addWidget(self.btnTreeRemove)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.line = QtGui.QFrame(self.frame)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.treeView = QtGui.QTreeView(self.dockWidgetContents)
        self.treeView.setIconSize(QtCore.QSize(22, 22))
        self.treeView.setObjectName("treeView")
        self.gridLayout_2.addWidget(self.treeView, 1, 0, 1, 1)
        self.dockTree.setWidget(self.dockWidgetContents)
        IcepapCMS.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockTree)
        self.statusbar = QtGui.QStatusBar(IcepapCMS)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusbar.sizePolicy().hasHeightForWidth())
        self.statusbar.setSizePolicy(sizePolicy)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        IcepapCMS.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(IcepapCMS)
        self.actionAbout.setObjectName("actionAbout")
        self.actionTree_Explorer = QtGui.QAction(IcepapCMS)
        self.actionTree_Explorer.setCheckable(True)
        self.actionTree_Explorer.setChecked(True)
        self.actionTree_Explorer.setObjectName("actionTree_Explorer")
        self.actionGoNext = QtGui.QAction(IcepapCMS)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/go-next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoNext.setIcon(icon3)
        self.actionGoNext.setObjectName("actionGoNext")
        self.actionGoPrevious = QtGui.QAction(IcepapCMS)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/go-previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoPrevious.setIcon(icon4)
        self.actionGoPrevious.setObjectName("actionGoPrevious")
        self.actionGoUp = QtGui.QAction(IcepapCMS)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/go-up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGoUp.setIcon(icon5)
        self.actionGoUp.setObjectName("actionGoUp")
        self.actionRefresh = QtGui.QAction(IcepapCMS)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/view-refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon6)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionPreferences = QtGui.QAction(IcepapCMS)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/gnome-settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPreferences.setIcon(icon7)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionHelp = QtGui.QAction(IcepapCMS)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/help-browser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon8)
        self.actionHelp.setObjectName("actionHelp")
        self.actionExport = QtGui.QAction(IcepapCMS)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/gnome-dev-floppy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport.setIcon(icon9)
        self.actionExport.setObjectName("actionExport")
        self.actionImport = QtGui.QAction(IcepapCMS)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImport.setIcon(icon10)
        self.actionImport.setObjectName("actionImport")
        self.actionQuit = QtGui.QAction(IcepapCMS)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/gnome-logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon11)
        self.actionQuit.setObjectName("actionQuit")
        self.actionToolbar = QtGui.QAction(IcepapCMS)
        self.actionToolbar.setCheckable(True)
        self.actionToolbar.setChecked(True)
        self.actionToolbar.setObjectName("actionToolbar")
        self.actionSaveConfig = QtGui.QAction(IcepapCMS)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/sign.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveConfig.setIcon(icon12)
        self.actionSaveConfig.setObjectName("actionSaveConfig")
        self.actionFirmwareUpgrade = QtGui.QAction(IcepapCMS)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/gnome-cpu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFirmwareUpgrade.setIcon(icon13)
        self.actionFirmwareUpgrade.setObjectName("actionFirmwareUpgrade")
        self.actionConsole = QtGui.QAction(IcepapCMS)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/gnome-terminal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConsole.setIcon(icon14)
        self.actionConsole.setObjectName("actionConsole")
        self.actionHistoricCfg = QtGui.QAction(IcepapCMS)
        self.actionHistoricCfg.setCheckable(True)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/calendar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHistoricCfg.setIcon(icon15)
        self.actionHistoricCfg.setObjectName("actionHistoricCfg")
        self.actionTemplates = QtGui.QAction(IcepapCMS)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icons/IcepapCfg Icons/notes.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTemplates.setIcon(icon16)
        self.actionTemplates.setObjectName("actionTemplates")
        self.actionAddIcepap = QtGui.QAction(IcepapCMS)
        self.actionAddIcepap.setIcon(icon1)
        self.actionAddIcepap.setObjectName("actionAddIcepap")
        self.actionDeleteIcepap = QtGui.QAction(IcepapCMS)
        self.actionDeleteIcepap.setIcon(icon2)
        self.actionDeleteIcepap.setObjectName("actionDeleteIcepap")
        self.actionUser_manual = QtGui.QAction(IcepapCMS)
        self.actionUser_manual.setObjectName("actionUser_manual")
        self.actionHardware_manual = QtGui.QAction(IcepapCMS)
        self.actionHardware_manual.setObjectName("actionHardware_manual")
        self.actionAddLocation = QtGui.QAction(IcepapCMS)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/small_icons/IcepapCFG Icons Petits/template.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddLocation.setIcon(icon17)
        self.actionAddLocation.setObjectName("actionAddLocation")
        self.actionDeleteLocation = QtGui.QAction(IcepapCMS)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/small_icons/IcepapCFG Icons Petits/process-stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDeleteLocation.setIcon(icon18)
        self.actionDeleteLocation.setObjectName("actionDeleteLocation")
        self.actionSetExpertFlag = QtGui.QAction(IcepapCMS)
        self.actionSetExpertFlag.setCheckable(True)
        self.actionSetExpertFlag.setObjectName("actionSetExpertFlag")
        self.menuHelp.addAction(self.actionUser_manual)
        self.menuHelp.addAction(self.actionHardware_manual)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menuView.addAction(self.actionTree_Explorer)
        self.menuView.addAction(self.actionToolbar)
        self.menuDriver.addAction(self.actionSaveConfig)
        self.menuDriver.addSeparator()
        self.menuDriver.addAction(self.actionHistoricCfg)
        self.menuDriver.addAction(self.actionTemplates)
        self.menuDriver.addSeparator()
        self.menuDriver.addAction(self.actionExport)
        self.menuDriver.addAction(self.actionImport)
        self.menuDriver.addAction(self.actionSetExpertFlag)
        self.menuFile.addAction(self.actionAddLocation)
        self.menuFile.addAction(self.actionDeleteLocation)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAddIcepap)
        self.menuFile.addAction(self.actionDeleteIcepap)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionFirmwareUpgrade)
        self.menuFile.addAction(self.actionConsole)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPreferences)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDriver.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionGoPrevious)
        self.toolBar.addAction(self.actionGoNext)
        self.toolBar.addAction(self.actionGoUp)
        self.toolBar.addAction(self.actionRefresh)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExport)
        self.toolBar.addAction(self.actionImport)
        self.toolBar.addAction(self.actionSaveConfig)
        self.toolBar.addAction(self.actionHistoricCfg)
        self.toolBar.addAction(self.actionTemplates)
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
        self.menuHelp.setTitle(QtGui.QApplication.translate("IcepapCMS", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("IcepapCMS", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDriver.setTitle(QtGui.QApplication.translate("IcepapCMS", "Driver", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("IcepapCMS", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("IcepapCMS", "Toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.dockTree.setWindowTitle(QtGui.QApplication.translate("IcepapCMS", "Tree Explorer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IcepapCMS", "Location", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("IcepapCMS", "Add / Remove Icepap System", None, QtGui.QApplication.UnicodeUTF8))
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
        self.actionExport.setText(QtGui.QApplication.translate("IcepapCMS", "Export configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setIconText(QtGui.QApplication.translate("IcepapCMS", "Export configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Export driver configuration to file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setText(QtGui.QApplication.translate("IcepapCMS", "Import configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setIconText(QtGui.QApplication.translate("IcepapCMS", "Import configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Import driver configuration from file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("IcepapCMS", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToolbar.setText(QtGui.QApplication.translate("IcepapCMS", "Toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToolbar.setShortcut(QtGui.QApplication.translate("IcepapCMS", "F9", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveConfig.setText(QtGui.QApplication.translate("IcepapCMS", "Save Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveConfig.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Save driver configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveConfig.setStatusTip(QtGui.QApplication.translate("IcepapCMS", "Ctrl+s", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveConfig.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFirmwareUpgrade.setText(QtGui.QApplication.translate("IcepapCMS", "Firmware upgrade", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFirmwareUpgrade.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Open Firmware upgrade dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConsole.setText(QtGui.QApplication.translate("IcepapCMS", "Console", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConsole.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Icepap Console", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHistoricCfg.setText(QtGui.QApplication.translate("IcepapCMS", "Historic Configurations", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHistoricCfg.setIconText(QtGui.QApplication.translate("IcepapCMS", "Historic Configurations", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHistoricCfg.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Historic configurations per driver", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHistoricCfg.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Ctrl+H", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemplates.setText(QtGui.QApplication.translate("IcepapCMS", "Templates", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemplates.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Template managment", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemplates.setShortcut(QtGui.QApplication.translate("IcepapCMS", "Ctrl+T", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddIcepap.setText(QtGui.QApplication.translate("IcepapCMS", "Add Icepap", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddIcepap.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Add Icepap System to CMS Database", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteIcepap.setText(QtGui.QApplication.translate("IcepapCMS", "Delete Icepap", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteIcepap.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Delete Icepap System from the CMS Database", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUser_manual.setText(QtGui.QApplication.translate("IcepapCMS", "User manual", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHardware_manual.setText(QtGui.QApplication.translate("IcepapCMS", "Hardware manual", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddLocation.setText(QtGui.QApplication.translate("IcepapCMS", "Add location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddLocation.setIconText(QtGui.QApplication.translate("IcepapCMS", "Add location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddLocation.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Add location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteLocation.setText(QtGui.QApplication.translate("IcepapCMS", "Delete location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteLocation.setIconText(QtGui.QApplication.translate("IcepapCMS", "Delete location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDeleteLocation.setToolTip(QtGui.QApplication.translate("IcepapCMS", "Delete location", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetExpertFlag.setText(QtGui.QApplication.translate("IcepapCMS", "Set Expert Flag", None, QtGui.QApplication.UnicodeUTF8))

import icepapcms_rc
