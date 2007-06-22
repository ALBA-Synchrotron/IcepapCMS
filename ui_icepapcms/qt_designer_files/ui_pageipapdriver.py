# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pageipapdriver.ui'
#
# Created: Wed Jun 13 10:36:02 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PageiPapDriver(object):
    def setupUi(self, PageiPapDriver):
        PageiPapDriver.setObjectName("PageiPapDriver")
        PageiPapDriver.resize(QtCore.QSize(QtCore.QRect(0,0,803,733).size()).expandedTo(PageiPapDriver.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PageiPapDriver.sizePolicy().hasHeightForWidth())
        PageiPapDriver.setSizePolicy(sizePolicy)

        self.vboxlayout = QtGui.QVBoxLayout(PageiPapDriver)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.groupBox = QtGui.QGroupBox(PageiPapDriver)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215,69))
        self.groupBox.setObjectName("groupBox")

        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)

        self.txtDriverName = QtGui.QLineEdit(self.groupBox)
        self.txtDriverName.setObjectName("txtDriverName")
        self.hboxlayout.addWidget(self.txtDriverName)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.hboxlayout.addWidget(self.label_3)

        self.txtDriverNemonic = QtGui.QLineEdit(self.groupBox)
        self.txtDriverNemonic.setObjectName("txtDriverNemonic")
        self.hboxlayout.addWidget(self.txtDriverNemonic)
        self.vboxlayout.addWidget(self.groupBox)

        self.frame_main = QtGui.QFrame(PageiPapDriver)
        self.frame_main.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_main.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_main.setObjectName("frame_main")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.frame_main)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.tabWidget = QtGui.QTabWidget(self.frame_main)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.tabSignals = QtGui.QTabWidget(self.tab)
        self.tabSignals.setObjectName("tabSignals")

        self.tab_InOut = QtGui.QWidget()
        self.tab_InOut.setObjectName("tab_InOut")

        self.inOut_widget = QtGui.QWidget(self.tab_InOut)
        self.inOut_widget.setGeometry(QtCore.QRect(20,30,528,388))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inOut_widget.sizePolicy().hasHeightForWidth())
        self.inOut_widget.setSizePolicy(sizePolicy)
        self.inOut_widget.setObjectName("inOut_widget")

        self.gridlayout = QtGui.QGridLayout(self.inOut_widget)
        self.gridlayout.setMargin(2)
        self.gridlayout.setSpacing(2)
        self.gridlayout.setObjectName("gridlayout")

        self.groupBox_3 = QtGui.QGroupBox(self.inOut_widget)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_13 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridlayout1.addWidget(self.label_13,0,5,1,1)

        self.cbSyncOutPulse = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutPulse.setObjectName("cbSyncOutPulse")
        self.gridlayout1.addWidget(self.cbSyncOutPulse,2,5,1,1)

        self.cbOutPosPulse = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosPulse.setObjectName("cbOutPosPulse")
        self.gridlayout1.addWidget(self.cbOutPosPulse,1,5,1,1)

        self.label_9 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridlayout1.addWidget(self.label_9,0,4,1,1)

        self.chbSyncOut = QtGui.QCheckBox(self.groupBox_3)
        self.chbSyncOut.setObjectName("chbSyncOut")
        self.gridlayout1.addWidget(self.chbSyncOut,2,0,1,1)

        self.cbSyncOutDir = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutDir.setObjectName("cbSyncOutDir")
        self.gridlayout1.addWidget(self.cbSyncOutDir,2,4,1,1)

        self.cbSyncOutEdge = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutEdge.setObjectName("cbSyncOutEdge")
        self.gridlayout1.addWidget(self.cbSyncOutEdge,2,3,1,1)

        self.cbSyncOutMode = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutMode.setObjectName("cbSyncOutMode")
        self.gridlayout1.addWidget(self.cbSyncOutMode,2,2,1,1)

        self.cbSyncOutSrc = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutSrc.setObjectName("cbSyncOutSrc")
        self.gridlayout1.addWidget(self.cbSyncOutSrc,2,1,1,1)

        self.chbOutPos = QtGui.QCheckBox(self.groupBox_3)
        self.chbOutPos.setObjectName("chbOutPos")
        self.gridlayout1.addWidget(self.chbOutPos,1,0,1,1)

        self.cbOutPosSrc = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosSrc.setObjectName("cbOutPosSrc")
        self.gridlayout1.addWidget(self.cbOutPosSrc,1,1,1,1)

        self.label_12 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setTextFormat(QtCore.Qt.PlainText)
        self.label_12.setObjectName("label_12")
        self.gridlayout1.addWidget(self.label_12,0,1,1,1)

        self.label_11 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridlayout1.addWidget(self.label_11,0,2,1,1)

        self.cbOutPosMode = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosMode.setMinimumSize(QtCore.QSize(0,0))
        self.cbOutPosMode.setObjectName("cbOutPosMode")
        self.gridlayout1.addWidget(self.cbOutPosMode,1,2,1,1)

        self.cbOutPosEdge = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosEdge.setObjectName("cbOutPosEdge")
        self.gridlayout1.addWidget(self.cbOutPosEdge,1,3,1,1)

        self.cbOutPosDir = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosDir.setObjectName("cbOutPosDir")
        self.gridlayout1.addWidget(self.cbOutPosDir,1,4,1,1)

        self.label_10 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridlayout1.addWidget(self.label_10,0,3,1,1)
        self.gridlayout.addWidget(self.groupBox_3,3,0,1,3)

        self.groupBox_4 = QtGui.QGroupBox(self.inOut_widget)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.chbAuxPos2 = QtGui.QCheckBox(self.groupBox_4)
        self.chbAuxPos2.setObjectName("chbAuxPos2")
        self.gridlayout2.addWidget(self.chbAuxPos2,3,0,1,1)

        self.chbAuxPos1 = QtGui.QCheckBox(self.groupBox_4)
        self.chbAuxPos1.setObjectName("chbAuxPos1")
        self.gridlayout2.addWidget(self.chbAuxPos1,2,0,1,1)

        self.chbTarget = QtGui.QCheckBox(self.groupBox_4)
        self.chbTarget.setObjectName("chbTarget")
        self.gridlayout2.addWidget(self.chbTarget,1,0,1,1)

        self.cbTargetSrc = QtGui.QComboBox(self.groupBox_4)
        self.cbTargetSrc.setObjectName("cbTargetSrc")
        self.gridlayout2.addWidget(self.cbTargetSrc,1,1,1,1)

        self.label_14 = QtGui.QLabel(self.groupBox_4)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridlayout2.addWidget(self.label_14,0,1,1,1)

        self.cbAuxPos1Src = QtGui.QComboBox(self.groupBox_4)
        self.cbAuxPos1Src.setObjectName("cbAuxPos1Src")
        self.gridlayout2.addWidget(self.cbAuxPos1Src,2,1,1,1)

        self.cbAuxPos2Src = QtGui.QComboBox(self.groupBox_4)
        self.cbAuxPos2Src.setObjectName("cbAuxPos2Src")
        self.gridlayout2.addWidget(self.cbAuxPos2Src,3,1,1,1)
        self.gridlayout.addWidget(self.groupBox_4,2,2,1,1)

        self.label_15 = QtGui.QLabel(self.inOut_widget)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridlayout.addWidget(self.label_15,0,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(121,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,1,1,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.inOut_widget)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label_8 = QtGui.QLabel(self.groupBox_2)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridlayout3.addWidget(self.label_8,0,3,1,1)

        self.label_7 = QtGui.QLabel(self.groupBox_2)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridlayout3.addWidget(self.label_7,0,2,1,1)

        self.label_6 = QtGui.QLabel(self.groupBox_2)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridlayout3.addWidget(self.label_6,0,1,1,1)

        self.cbInPosDir = QtGui.QComboBox(self.groupBox_2)
        self.cbInPosDir.setObjectName("cbInPosDir")
        self.gridlayout3.addWidget(self.cbInPosDir,1,3,1,1)

        self.cbEncInDir = QtGui.QComboBox(self.groupBox_2)
        self.cbEncInDir.setObjectName("cbEncInDir")
        self.gridlayout3.addWidget(self.cbEncInDir,2,3,1,1)

        self.cbSyncInDir = QtGui.QComboBox(self.groupBox_2)
        self.cbSyncInDir.setObjectName("cbSyncInDir")
        self.gridlayout3.addWidget(self.cbSyncInDir,3,3,1,1)

        self.cbEncInEdge = QtGui.QComboBox(self.groupBox_2)
        self.cbEncInEdge.setObjectName("cbEncInEdge")
        self.gridlayout3.addWidget(self.cbEncInEdge,2,2,1,1)

        self.cbSyncInEdge = QtGui.QComboBox(self.groupBox_2)
        self.cbSyncInEdge.setObjectName("cbSyncInEdge")
        self.gridlayout3.addWidget(self.cbSyncInEdge,3,2,1,1)

        self.cbInPosEdge = QtGui.QComboBox(self.groupBox_2)
        self.cbInPosEdge.setObjectName("cbInPosEdge")
        self.gridlayout3.addWidget(self.cbInPosEdge,1,2,1,1)

        self.cbInPosMode = QtGui.QComboBox(self.groupBox_2)
        self.cbInPosMode.setMinimumSize(QtCore.QSize(0,0))
        self.cbInPosMode.setObjectName("cbInPosMode")
        self.gridlayout3.addWidget(self.cbInPosMode,1,1,1,1)

        self.chbInPos = QtGui.QCheckBox(self.groupBox_2)
        self.chbInPos.setObjectName("chbInPos")
        self.gridlayout3.addWidget(self.chbInPos,1,0,1,1)

        self.chbEncIn = QtGui.QCheckBox(self.groupBox_2)
        self.chbEncIn.setObjectName("chbEncIn")
        self.gridlayout3.addWidget(self.chbEncIn,2,0,1,1)

        self.chbSyncIn = QtGui.QCheckBox(self.groupBox_2)
        self.chbSyncIn.setObjectName("chbSyncIn")
        self.gridlayout3.addWidget(self.chbSyncIn,3,0,1,1)

        self.cbSyncInMode = QtGui.QComboBox(self.groupBox_2)
        self.cbSyncInMode.setObjectName("cbSyncInMode")
        self.gridlayout3.addWidget(self.cbSyncInMode,3,1,1,1)

        self.cbEncInMode = QtGui.QComboBox(self.groupBox_2)
        self.cbEncInMode.setObjectName("cbEncInMode")
        self.gridlayout3.addWidget(self.cbEncInMode,2,1,1,1)
        self.gridlayout.addWidget(self.groupBox_2,2,0,1,2)

        self.listPredefined = QtGui.QListWidget(self.inOut_widget)
        self.listPredefined.setMaximumSize(QtCore.QSize(16777215,100))
        self.listPredefined.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listPredefined.setObjectName("listPredefined")
        self.gridlayout.addWidget(self.listPredefined,1,0,1,1)
        self.tabSignals.addTab(self.tab_InOut,"")

        self.tab_aux = QtGui.QWidget()
        self.tab_aux.setObjectName("tab_aux")
        self.tabSignals.addTab(self.tab_aux,"")

        self.tab_connectors = QtGui.QWidget()
        self.tab_connectors.setObjectName("tab_connectors")

        self.labels_widget = QtGui.QWidget(self.tab_connectors)
        self.labels_widget.setGeometry(QtCore.QRect(30,20,451,525))
        self.labels_widget.setObjectName("labels_widget")

        self.gridlayout4 = QtGui.QGridLayout(self.labels_widget)
        self.gridlayout4.setMargin(2)
        self.gridlayout4.setSpacing(2)
        self.gridlayout4.setObjectName("gridlayout4")

        self.label_5 = QtGui.QLabel(self.labels_widget)
        self.label_5.setPixmap(QtGui.QPixmap(":/images/IcepapCfg Icons/encoder.png"))
        self.label_5.setObjectName("label_5")
        self.gridlayout4.addWidget(self.label_5,1,1,1,1)

        self.label_4 = QtGui.QLabel(self.labels_widget)
        self.label_4.setPixmap(QtGui.QPixmap(":/images/IcepapCfg Icons/axis.png"))
        self.label_4.setObjectName("label_4")
        self.gridlayout4.addWidget(self.label_4,0,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem2,0,2,1,1)

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem3,0,0,1,1)
        self.tabSignals.addTab(self.tab_connectors,"")
        self.vboxlayout1.addWidget(self.tabSignals)
        self.tabWidget.addTab(self.tab,"")
        self.hboxlayout1.addWidget(self.tabWidget)

        self.frame_right = QtGui.QFrame(self.frame_main)
        self.frame_right.setMinimumSize(QtCore.QSize(220,499))
        self.frame_right.setMaximumSize(QtCore.QSize(220,16777215))
        self.frame_right.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_right.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_right.setObjectName("frame_right")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.frame_right)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.label = QtGui.QLabel(self.frame_right)
        self.label.setPixmap(QtGui.QPixmap(":/logos/IcepapCfg Icons/Icepap.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout2.addWidget(self.label)

        spacerItem4 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem4)

        self.frame_test = QtGui.QFrame(self.frame_right)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_test.sizePolicy().hasHeightForWidth())
        self.frame_test.setSizePolicy(sizePolicy)
        self.frame_test.setMinimumSize(QtCore.QSize(202,280))
        self.frame_test.setMaximumSize(QtCore.QSize(250,16777215))
        self.frame_test.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_test.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_test.setObjectName("frame_test")

        self.gridlayout5 = QtGui.QGridLayout(self.frame_test)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.frame_4 = QtGui.QFrame(self.frame_test)
        self.frame_4.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.frame_4)
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(0)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem5 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem5)

        self.frame_leds = QtGui.QFrame(self.frame_4)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_leds.sizePolicy().hasHeightForWidth())
        self.frame_leds.setSizePolicy(sizePolicy)
        self.frame_leds.setMinimumSize(QtCore.QSize(171,48))
        self.frame_leds.setMaximumSize(QtCore.QSize(171,48))
        self.frame_leds.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_leds.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_leds.setObjectName("frame_leds")

        self.gridlayout6 = QtGui.QGridLayout(self.frame_leds)
        self.gridlayout6.setMargin(2)
        self.gridlayout6.setSpacing(2)
        self.gridlayout6.setObjectName("gridlayout6")

        self.textLabel1_6_4 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6_4.setFont(font)
        self.textLabel1_6_4.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1_6_4.setObjectName("textLabel1_6_4")
        self.gridlayout6.addWidget(self.textLabel1_6_4,1,1,1,1)

        self.LedLimitPos = Led(self.frame_leds)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LedLimitPos.sizePolicy().hasHeightForWidth())
        self.LedLimitPos.setSizePolicy(sizePolicy)
        self.LedLimitPos.setMinimumSize(QtCore.QSize(24,24))
        self.LedLimitPos.setMaximumSize(QtCore.QSize(24,24))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(85,255,127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(85,255,127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(85,255,127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(85,255,127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Window,brush)
        self.LedLimitPos.setPalette(palette)
        self.LedLimitPos.setObjectName("LedLimitPos")
        self.gridlayout6.addWidget(self.LedLimitPos,0,3,1,1)

        self.textLabel1_6_5 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6_5.setFont(font)
        self.textLabel1_6_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.textLabel1_6_5.setObjectName("textLabel1_6_5")
        self.gridlayout6.addWidget(self.textLabel1_6_5,1,0,1,1)

        self.LedHome = Led(self.frame_leds)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LedHome.sizePolicy().hasHeightForWidth())
        self.LedHome.setSizePolicy(sizePolicy)
        self.LedHome.setMinimumSize(QtCore.QSize(24,24))
        self.LedHome.setMaximumSize(QtCore.QSize(24,24))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Window,brush)
        self.LedHome.setPalette(palette)
        self.LedHome.setObjectName("LedHome")
        self.gridlayout6.addWidget(self.LedHome,0,2,1,1)

        self.textLabel1_6_3 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6_3.setFont(font)
        self.textLabel1_6_3.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1_6_3.setObjectName("textLabel1_6_3")
        self.gridlayout6.addWidget(self.textLabel1_6_3,1,2,1,1)

        self.textLabel1_6 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6.setFont(font)
        self.textLabel1_6.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1_6.setObjectName("textLabel1_6")
        self.gridlayout6.addWidget(self.textLabel1_6,1,3,1,1)

        self.LedStep = Led(self.frame_leds)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LedStep.sizePolicy().hasHeightForWidth())
        self.LedStep.setSizePolicy(sizePolicy)
        self.LedStep.setMinimumSize(QtCore.QSize(24,24))
        self.LedStep.setMaximumSize(QtCore.QSize(24,24))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(85,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(85,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(85,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(85,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Window,brush)
        self.LedStep.setPalette(palette)
        self.LedStep.setObjectName("LedStep")
        self.gridlayout6.addWidget(self.LedStep,0,1,1,1)

        self.textLabel1_6_2 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6_2.setFont(font)
        self.textLabel1_6_2.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1_6_2.setObjectName("textLabel1_6_2")
        self.gridlayout6.addWidget(self.textLabel1_6_2,1,4,1,1)

        self.LedLimitNeg = Led(self.frame_leds)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LedLimitNeg.sizePolicy().hasHeightForWidth())
        self.LedLimitNeg.setSizePolicy(sizePolicy)
        self.LedLimitNeg.setMinimumSize(QtCore.QSize(24,24))
        self.LedLimitNeg.setMaximumSize(QtCore.QSize(24,24))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,85,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,85,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,85,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,85,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Window,brush)
        self.LedLimitNeg.setPalette(palette)
        self.LedLimitNeg.setObjectName("LedLimitNeg")
        self.gridlayout6.addWidget(self.LedLimitNeg,0,4,1,1)

        self.LedError = Led(self.frame_leds)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LedError.sizePolicy().hasHeightForWidth())
        self.LedError.setSizePolicy(sizePolicy)
        self.LedError.setMinimumSize(QtCore.QSize(24,24))
        self.LedError.setMaximumSize(QtCore.QSize(24,24))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(101,148,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Window,brush)
        self.LedError.setPalette(palette)
        self.LedError.setObjectName("LedError")
        self.gridlayout6.addWidget(self.LedError,0,0,1,1)
        self.hboxlayout2.addWidget(self.frame_leds)

        spacerItem6 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem6)
        self.gridlayout5.addWidget(self.frame_4,5,0,1,7)

        self.BtnSetPos = QtGui.QPushButton(self.frame_test)
        self.BtnSetPos.setMaximumSize(QtCore.QSize(40,24))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.BtnSetPos.setFont(font)
        self.BtnSetPos.setObjectName("BtnSetPos")
        self.gridlayout5.addWidget(self.BtnSetPos,3,3,1,2)

        self.btnEnable = QtGui.QPushButton(self.frame_test)
        self.btnEnable.setMaximumSize(QtCore.QSize(50,16777215))

        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(8)
        self.btnEnable.setFont(font)
        self.btnEnable.setCheckable(True)
        self.btnEnable.setChecked(False)
        self.btnEnable.setObjectName("btnEnable")
        self.gridlayout5.addWidget(self.btnEnable,8,0,1,1)

        self.btnGORelativeNeg = QtGui.QPushButton(self.frame_test)
        self.btnGORelativeNeg.setMaximumSize(QtCore.QSize(24,24))
        self.btnGORelativeNeg.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/go-relative2.png"))
        self.btnGORelativeNeg.setIconSize(QtCore.QSize(22,22))
        self.btnGORelativeNeg.setObjectName("btnGORelativeNeg")
        self.gridlayout5.addWidget(self.btnGORelativeNeg,8,3,1,1)

        self.textLabel1_3_4 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3_4.setFont(font)
        self.textLabel1_3_4.setObjectName("textLabel1_3_4")
        self.gridlayout5.addWidget(self.textLabel1_3_4,3,0,1,2)

        self.textLabel1_3_3_2 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3_3_2.setFont(font)
        self.textLabel1_3_3_2.setObjectName("textLabel1_3_3_2")
        self.gridlayout5.addWidget(self.textLabel1_3_3_2,2,0,1,5)

        self.txtSpeed = QtGui.QLineEdit(self.frame_test)
        self.txtSpeed.setMaximumSize(QtCore.QSize(16777215,24))

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.txtSpeed.setFont(font)
        self.txtSpeed.setObjectName("txtSpeed")
        self.gridlayout5.addWidget(self.txtSpeed,1,5,1,2)

        self.LCDPosition = QtGui.QLCDNumber(self.frame_test)
        self.LCDPosition.setMinimumSize(QtCore.QSize(0,24))
        self.LCDPosition.setMaximumSize(QtCore.QSize(16777215,50))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(40,59,93))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.WindowText,brush)

        brush = QtGui.QBrush(QtGui.QColor(45,68,106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(178,200,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(40,59,93))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.WindowText,brush)

        brush = QtGui.QBrush(QtGui.QColor(45,68,106))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(178,200,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(118,116,113))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.WindowText,brush)

        brush = QtGui.QBrush(QtGui.QColor(118,116,113))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Text,brush)

        brush = QtGui.QBrush(QtGui.QColor(178,200,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(178,200,235))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Window,brush)
        self.LCDPosition.setPalette(palette)

        font = QtGui.QFont()
        font.setPointSize(9)
        self.LCDPosition.setFont(font)
        self.LCDPosition.setAutoFillBackground(True)
        self.LCDPosition.setFrameShape(QtGui.QFrame.Panel)
        self.LCDPosition.setFrameShadow(QtGui.QFrame.Raised)
        self.LCDPosition.setNumDigits(9)
        self.LCDPosition.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.LCDPosition.setObjectName("LCDPosition")
        self.gridlayout5.addWidget(self.LCDPosition,6,1,1,6)

        self.btnStopMotor = QtGui.QPushButton(self.frame_test)
        self.btnStopMotor.setMaximumSize(QtCore.QSize(24,24))
        self.btnStopMotor.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-session-halt.png"))
        self.btnStopMotor.setIconSize(QtCore.QSize(22,22))
        self.btnStopMotor.setObjectName("btnStopMotor")
        self.gridlayout5.addWidget(self.btnStopMotor,8,1,1,2)

        self.textLabel3 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel3.setFont(font)
        self.textLabel3.setObjectName("textLabel3")
        self.gridlayout5.addWidget(self.textLabel3,6,0,1,1)

        self.textLabel1_3 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3.setFont(font)
        self.textLabel1_3.setObjectName("textLabel1_3")
        self.gridlayout5.addWidget(self.textLabel1_3,7,0,1,4)

        self.txtGORelative = QtGui.QLineEdit(self.frame_test)
        self.txtGORelative.setMaximumSize(QtCore.QSize(100,24))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.txtGORelative.setFont(font)
        self.txtGORelative.setObjectName("txtGORelative")
        self.gridlayout5.addWidget(self.txtGORelative,8,4,1,2)

        self.sbFactor = QtGui.QSpinBox(self.frame_test)
        self.sbFactor.setEnabled(True)
        self.sbFactor.setMaximumSize(QtCore.QSize(16777215,24))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.sbFactor.setFont(font)
        self.sbFactor.setMaximum(99999)
        self.sbFactor.setMinimum(1)
        self.sbFactor.setProperty("value",QtCore.QVariant(1))
        self.sbFactor.setObjectName("sbFactor")
        self.gridlayout5.addWidget(self.sbFactor,0,5,1,2)

        self.sbPosition = QtGui.QSpinBox(self.frame_test)
        self.sbPosition.setMaximumSize(QtCore.QSize(16777215,24))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.sbPosition.setFont(font)
        self.sbPosition.setMaximum(99999)
        self.sbPosition.setProperty("value",QtCore.QVariant(0))
        self.sbPosition.setObjectName("sbPosition")
        self.gridlayout5.addWidget(self.sbPosition,3,5,1,2)

        self.txtMvAbsolute = QtGui.QLineEdit(self.frame_test)
        self.txtMvAbsolute.setMaximumSize(QtCore.QSize(100,24))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.txtMvAbsolute.setFont(font)
        self.txtMvAbsolute.setObjectName("txtMvAbsolute")
        self.gridlayout5.addWidget(self.txtMvAbsolute,7,4,1,2)

        self.textLabel1_3_3_2_2 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3_3_2_2.setFont(font)
        self.textLabel1_3_3_2_2.setObjectName("textLabel1_3_3_2_2")
        self.gridlayout5.addWidget(self.textLabel1_3_3_2_2,0,0,1,5)

        self.textLabel1_3_3 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3_3.setFont(font)
        self.textLabel1_3_3.setObjectName("textLabel1_3_3")
        self.gridlayout5.addWidget(self.textLabel1_3_3,1,0,1,5)

        self.btnGO = QtGui.QPushButton(self.frame_test)
        self.btnGO.setMaximumSize(QtCore.QSize(24,24))
        self.btnGO.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/go-absolute.png"))
        self.btnGO.setIconSize(QtCore.QSize(22,22))
        self.btnGO.setObjectName("btnGO")
        self.gridlayout5.addWidget(self.btnGO,7,6,1,1)

        self.btnGORelativePos = QtGui.QPushButton(self.frame_test)
        self.btnGORelativePos.setMaximumSize(QtCore.QSize(24,24))
        self.btnGORelativePos.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/go-relative.png"))
        self.btnGORelativePos.setIconSize(QtCore.QSize(22,22))
        self.btnGORelativePos.setObjectName("btnGORelativePos")
        self.gridlayout5.addWidget(self.btnGORelativePos,8,6,1,1)

        self.txtAcceleration = QtGui.QLineEdit(self.frame_test)
        self.txtAcceleration.setMaximumSize(QtCore.QSize(16777215,24))

        font = QtGui.QFont()
        font.setPointSize(8)
        self.txtAcceleration.setFont(font)
        self.txtAcceleration.setObjectName("txtAcceleration")
        self.gridlayout5.addWidget(self.txtAcceleration,2,5,1,2)

        self.frame = QtGui.QFrame(self.frame_test)
        self.frame.setFrameShape(QtGui.QFrame.HLine)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridlayout5.addWidget(self.frame,4,0,1,7)
        self.vboxlayout2.addWidget(self.frame_test)

        spacerItem7 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem7)

        self.btnApplyCfg = QtGui.QPushButton(self.frame_right)
        self.btnApplyCfg.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-dev-floppy.png"))
        self.btnApplyCfg.setIconSize(QtCore.QSize(20,20))
        self.btnApplyCfg.setObjectName("btnApplyCfg")
        self.vboxlayout2.addWidget(self.btnApplyCfg)

        self.btnUndo = QtGui.QPushButton(self.frame_right)
        self.btnUndo.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/undo.png"))
        self.btnUndo.setIconSize(QtCore.QSize(20,20))
        self.btnUndo.setObjectName("btnUndo")
        self.vboxlayout2.addWidget(self.btnUndo)

        self.btnTemplates = QtGui.QPushButton(self.frame_right)
        self.btnTemplates.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/notes.png"))
        self.btnTemplates.setIconSize(QtCore.QSize(20,20))
        self.btnTemplates.setObjectName("btnTemplates")
        self.vboxlayout2.addWidget(self.btnTemplates)

        self.btnHistoric = QtGui.QPushButton(self.frame_right)
        self.btnHistoric.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnHistoric.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/calendar.png"))
        self.btnHistoric.setIconSize(QtCore.QSize(20,20))
        self.btnHistoric.setObjectName("btnHistoric")
        self.vboxlayout2.addWidget(self.btnHistoric)
        self.hboxlayout1.addWidget(self.frame_right)
        self.vboxlayout.addWidget(self.frame_main)

        self.retranslateUi(PageiPapDriver)
        self.tabWidget.setCurrentIndex(0)
        self.tabSignals.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PageiPapDriver)

    def retranslateUi(self, PageiPapDriver):
        PageiPapDriver.setWindowTitle(QtGui.QApplication.translate("PageiPapDriver", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Driver Description", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PageiPapDriver", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PageiPapDriver", "Nemonic", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Output Signals", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("PageiPapDriver", "Pulse width", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutPulse.addItem(QtGui.QApplication.translate("PageiPapDriver", "50ns", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutPulse.addItem(QtGui.QApplication.translate("PageiPapDriver", "200ns", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutPulse.addItem(QtGui.QApplication.translate("PageiPapDriver", "2us", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutPulse.addItem(QtGui.QApplication.translate("PageiPapDriver", "20us", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosPulse.addItem(QtGui.QApplication.translate("PageiPapDriver", "50ns", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosPulse.addItem(QtGui.QApplication.translate("PageiPapDriver", "200ns", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosPulse.addItem(QtGui.QApplication.translate("PageiPapDriver", "2us", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosPulse.addItem(QtGui.QApplication.translate("PageiPapDriver", "20us", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("PageiPapDriver", "Direction", None, QtGui.QApplication.UnicodeUTF8))
        self.chbSyncOut.setText(QtGui.QApplication.translate("PageiPapDriver", "SyncOut", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Rising", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Falling", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Quadrature", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Step/Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "InPos", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "DSPin", None, QtGui.QApplication.UnicodeUTF8))
        self.chbOutPos.setText(QtGui.QApplication.translate("PageiPapDriver", "OutPos", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "InPos", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "DSPin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("PageiPapDriver", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("PageiPapDriver", "Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Quadrature", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Step/Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Rising", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Falling", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("PageiPapDriver", "Edge", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Counter registers", None, QtGui.QApplication.UnicodeUTF8))
        self.chbAuxPos2.setText(QtGui.QApplication.translate("PageiPapDriver", "AuxPos2", None, QtGui.QApplication.UnicodeUTF8))
        self.chbAuxPos1.setText(QtGui.QApplication.translate("PageiPapDriver", "AuxPos1", None, QtGui.QApplication.UnicodeUTF8))
        self.chbTarget.setText(QtGui.QApplication.translate("PageiPapDriver", "Target", None, QtGui.QApplication.UnicodeUTF8))
        self.cbTargetSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbTargetSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "InPos", None, QtGui.QApplication.UnicodeUTF8))
        self.cbTargetSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbTargetSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "DSPin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("PageiPapDriver", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:8pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Source</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.cbAuxPos1Src.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbAuxPos1Src.addItem(QtGui.QApplication.translate("PageiPapDriver", "InPos", None, QtGui.QApplication.UnicodeUTF8))
        self.cbAuxPos1Src.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbAuxPos1Src.addItem(QtGui.QApplication.translate("PageiPapDriver", "DSPin", None, QtGui.QApplication.UnicodeUTF8))
        self.cbAuxPos2Src.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbAuxPos2Src.addItem(QtGui.QApplication.translate("PageiPapDriver", "InPos", None, QtGui.QApplication.UnicodeUTF8))
        self.cbAuxPos2Src.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbAuxPos2Src.addItem(QtGui.QApplication.translate("PageiPapDriver", "DSPin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("PageiPapDriver", "Predefined configurations", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Input Signals", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("PageiPapDriver", "Direction", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("PageiPapDriver", "Edge", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PageiPapDriver", "Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInPosDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInPosDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbEncInDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbEncInDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncInDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncInDir.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbEncInEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Rising", None, QtGui.QApplication.UnicodeUTF8))
        self.cbEncInEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Falling", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncInEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Rising", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncInEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Falling", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInPosEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Rising", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInPosEdge.addItem(QtGui.QApplication.translate("PageiPapDriver", "Falling", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInPosMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Quadrature", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInPosMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Step/Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.chbInPos.setText(QtGui.QApplication.translate("PageiPapDriver", "InPos", None, QtGui.QApplication.UnicodeUTF8))
        self.chbEncIn.setText(QtGui.QApplication.translate("PageiPapDriver", "EncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.chbSyncIn.setText(QtGui.QApplication.translate("PageiPapDriver", "SyncIn", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncInMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Quadrature", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncInMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Step/Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.cbEncInMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Quadrature", None, QtGui.QApplication.UnicodeUTF8))
        self.cbEncInMode.addItem(QtGui.QApplication.translate("PageiPapDriver", "Step/Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.tabSignals.setTabText(self.tabSignals.indexOf(self.tab_InOut), QtGui.QApplication.translate("PageiPapDriver", "Input/Output", None, QtGui.QApplication.UnicodeUTF8))
        self.tabSignals.setTabText(self.tabSignals.indexOf(self.tab_aux), QtGui.QApplication.translate("PageiPapDriver", "Aux signals", None, QtGui.QApplication.UnicodeUTF8))
        self.tabSignals.setTabText(self.tabSignals.indexOf(self.tab_connectors), QtGui.QApplication.translate("PageiPapDriver", "Connectors", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("PageiPapDriver", "signals", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6_4.setText(QtGui.QApplication.translate("PageiPapDriver", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:7pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Step</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6_5.setText(QtGui.QApplication.translate("PageiPapDriver", "Stat", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6_3.setText(QtGui.QApplication.translate("PageiPapDriver", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6.setText(QtGui.QApplication.translate("PageiPapDriver", "Limit+", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6_2.setText(QtGui.QApplication.translate("PageiPapDriver", "Limit-", None, QtGui.QApplication.UnicodeUTF8))
        self.BtnSetPos.setText(QtGui.QApplication.translate("PageiPapDriver", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.btnEnable.setText(QtGui.QApplication.translate("PageiPapDriver", "enable", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3_4.setText(QtGui.QApplication.translate("PageiPapDriver", "Position", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3_3_2.setText(QtGui.QApplication.translate("PageiPapDriver", "Acceleration", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3.setText(QtGui.QApplication.translate("PageiPapDriver", "Position", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3.setText(QtGui.QApplication.translate("PageiPapDriver", "Move absolute", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3_3_2_2.setText(QtGui.QApplication.translate("PageiPapDriver", "Steps x mm/degree", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3_3.setText(QtGui.QApplication.translate("PageiPapDriver", "Speed (steps/sec)", None, QtGui.QApplication.UnicodeUTF8))
        self.btnApplyCfg.setText(QtGui.QApplication.translate("PageiPapDriver", "Apply Config", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUndo.setText(QtGui.QApplication.translate("PageiPapDriver", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.btnTemplates.setText(QtGui.QApplication.translate("PageiPapDriver", "Driver Templates", None, QtGui.QApplication.UnicodeUTF8))
        self.btnHistoric.setText(QtGui.QApplication.translate("PageiPapDriver", "Historic Cfgs", None, QtGui.QApplication.UnicodeUTF8))

from Led import Led
import icepapcms_rc
