# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pageipapdriver.ui'
#
# Created: Wed Aug 29 15:53:34 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from Led import Led

class Ui_PageiPapDriver(object):
    def setupUi(self, PageiPapDriver):
        PageiPapDriver.setObjectName("PageiPapDriver")
        PageiPapDriver.resize(QtCore.QSize(QtCore.QRect(0,0,734,604).size()).expandedTo(PageiPapDriver.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PageiPapDriver.sizePolicy().hasHeightForWidth())
        PageiPapDriver.setSizePolicy(sizePolicy)
        PageiPapDriver.setMinimumSize(QtCore.QSize(665,604))

        self.gridlayout = QtGui.QGridLayout(PageiPapDriver)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(PageiPapDriver)
        self.tabWidget.setMinimumSize(QtCore.QSize(421,505))
        self.tabWidget.setObjectName("tabWidget")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout1 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,4,3,1,1)

        self.groupBox_6 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_6.setFlat(True)
        self.groupBox_6.setObjectName("groupBox_6")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_6)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.label_16 = QtGui.QLabel(self.groupBox_6)
        self.label_16.setObjectName("label_16")
        self.gridlayout2.addWidget(self.label_16,0,0,1,1)

        self.IB = QtGui.QDoubleSpinBox(self.groupBox_6)
        self.IB.setSingleStep(0.1)
        self.IB.setObjectName("IB")
        self.gridlayout2.addWidget(self.IB,2,1,1,1)

        self.II = QtGui.QDoubleSpinBox(self.groupBox_6)
        self.II.setSingleStep(0.1)
        self.II.setObjectName("II")
        self.gridlayout2.addWidget(self.II,0,1,1,1)

        self.IN = QtGui.QDoubleSpinBox(self.groupBox_6)
        self.IN.setSingleStep(0.1)
        self.IN.setObjectName("IN")
        self.gridlayout2.addWidget(self.IN,1,1,1,1)

        self.label_17 = QtGui.QLabel(self.groupBox_6)
        self.label_17.setObjectName("label_17")
        self.gridlayout2.addWidget(self.label_17,2,0,1,1)

        self.groupBox_7 = QtGui.QGroupBox(self.groupBox_6)
        self.groupBox_7.setFlat(True)
        self.groupBox_7.setCheckable(False)
        self.groupBox_7.setObjectName("groupBox_7")

        self.gridlayout3 = QtGui.QGridLayout(self.groupBox_7)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.IREGP = QtGui.QDoubleSpinBox(self.groupBox_7)
        self.IREGP.setMaximum(1000.0)
        self.IREGP.setSingleStep(1.0)
        self.IREGP.setObjectName("IREGP")
        self.gridlayout3.addWidget(self.IREGP,0,1,1,1)

        self.IREGI = QtGui.QDoubleSpinBox(self.groupBox_7)
        self.IREGI.setDecimals(4)
        self.IREGI.setMaximum(1000.0)
        self.IREGI.setSingleStep(0.1)
        self.IREGI.setObjectName("IREGI")
        self.gridlayout3.addWidget(self.IREGI,1,1,1,1)

        self.label_21 = QtGui.QLabel(self.groupBox_7)
        self.label_21.setObjectName("label_21")
        self.gridlayout3.addWidget(self.label_21,1,0,1,1)

        self.label_23 = QtGui.QLabel(self.groupBox_7)
        self.label_23.setObjectName("label_23")
        self.gridlayout3.addWidget(self.label_23,0,0,1,1)
        self.gridlayout2.addWidget(self.groupBox_7,0,3,3,1)

        self.label_18 = QtGui.QLabel(self.groupBox_6)
        self.label_18.setObjectName("label_18")
        self.gridlayout2.addWidget(self.label_18,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem1,1,2,1,1)
        self.gridlayout1.addWidget(self.groupBox_6,1,0,1,2)

        spacerItem2 = QtGui.QSpacerItem(151,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem2,0,1,1,2)

        spacerItem3 = QtGui.QSpacerItem(181,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem3,2,1,1,3)

        self.frame_2 = QtGui.QFrame(self.tab_2)
        self.frame_2.setMinimumSize(QtCore.QSize(16,43))
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.hboxlayout = QtGui.QHBoxLayout(self.frame_2)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_22 = QtGui.QLabel(self.frame_2)
        self.label_22.setObjectName("label_22")
        self.hboxlayout.addWidget(self.label_22)

        self.MICRO = QtGui.QSpinBox(self.frame_2)
        self.MICRO.setMaximum(256)
        self.MICRO.setObjectName("MICRO")
        self.hboxlayout.addWidget(self.MICRO)

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem4)

        self.AUXPS = QtGui.QCheckBox(self.frame_2)
        self.AUXPS.setObjectName("AUXPS")
        self.hboxlayout.addWidget(self.AUXPS)
        self.gridlayout1.addWidget(self.frame_2,4,0,1,3)

        self.groupBox_9 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_9.setFlat(True)
        self.groupBox_9.setObjectName("groupBox_9")

        self.gridlayout4 = QtGui.QGridLayout(self.groupBox_9)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.SD = QtGui.QDoubleSpinBox(self.groupBox_9)
        self.SD.setSingleStep(1.0)
        self.SD.setProperty("value",QtCore.QVariant(0.0))
        self.SD.setObjectName("SD")
        self.gridlayout4.addWidget(self.SD,0,1,1,1)

        self.label_19 = QtGui.QLabel(self.groupBox_9)
        self.label_19.setObjectName("label_19")
        self.gridlayout4.addWidget(self.label_19,0,0,1,1)

        self.SDMAX = QtGui.QDoubleSpinBox(self.groupBox_9)
        self.SDMAX.setSingleStep(0.1)
        self.SDMAX.setProperty("value",QtCore.QVariant(0.0))
        self.SDMAX.setObjectName("SDMAX")
        self.gridlayout4.addWidget(self.SDMAX,1,1,1,1)

        self.label_20 = QtGui.QLabel(self.groupBox_9)
        self.label_20.setObjectName("label_20")
        self.gridlayout4.addWidget(self.label_20,1,0,1,1)
        self.gridlayout1.addWidget(self.groupBox_9,0,0,1,1)

        self.groupBox_8 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_8.setFlat(True)
        self.groupBox_8.setObjectName("groupBox_8")

        self.gridlayout5 = QtGui.QGridLayout(self.groupBox_8)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.TDIR = QtGui.QCheckBox(self.groupBox_8)
        self.TDIR.setObjectName("TDIR")
        self.gridlayout5.addWidget(self.TDIR,2,0,1,1)

        self.PSW = QtGui.QCheckBox(self.groupBox_8)
        self.PSW.setObjectName("PSW")
        self.gridlayout5.addWidget(self.PSW,1,0,1,1)

        self.ESW = QtGui.QCheckBox(self.groupBox_8)
        self.ESW.setObjectName("ESW")
        self.gridlayout5.addWidget(self.ESW,0,0,1,1)
        self.gridlayout1.addWidget(self.groupBox_8,2,0,1,1)

        spacerItem5 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem5,1,2,1,2)

        spacerItem6 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem6,5,1,1,1)

        self.line_2 = QtGui.QFrame(self.tab_2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout1.addWidget(self.line_2,3,0,1,1)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.tab)
        self.hboxlayout1.setMargin(9)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

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

        self.gridlayout6 = QtGui.QGridLayout(self.inOut_widget)
        self.gridlayout6.setMargin(2)
        self.gridlayout6.setSpacing(2)
        self.gridlayout6.setObjectName("gridlayout6")

        self.groupBox_3 = QtGui.QGroupBox(self.inOut_widget)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout7 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.label_13 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridlayout7.addWidget(self.label_13,0,5,1,1)

        self.cbSyncOutPulse = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutPulse.setObjectName("cbSyncOutPulse")
        self.gridlayout7.addWidget(self.cbSyncOutPulse,2,5,1,1)

        self.cbOutPosPulse = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosPulse.setObjectName("cbOutPosPulse")
        self.gridlayout7.addWidget(self.cbOutPosPulse,1,5,1,1)

        self.label_9 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridlayout7.addWidget(self.label_9,0,4,1,1)

        self.chbSyncOut = QtGui.QCheckBox(self.groupBox_3)
        self.chbSyncOut.setObjectName("chbSyncOut")
        self.gridlayout7.addWidget(self.chbSyncOut,2,0,1,1)

        self.cbSyncOutDir = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutDir.setObjectName("cbSyncOutDir")
        self.gridlayout7.addWidget(self.cbSyncOutDir,2,4,1,1)

        self.cbSyncOutEdge = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutEdge.setObjectName("cbSyncOutEdge")
        self.gridlayout7.addWidget(self.cbSyncOutEdge,2,3,1,1)

        self.cbSyncOutMode = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutMode.setObjectName("cbSyncOutMode")
        self.gridlayout7.addWidget(self.cbSyncOutMode,2,2,1,1)

        self.cbSyncOutSrc = QtGui.QComboBox(self.groupBox_3)
        self.cbSyncOutSrc.setObjectName("cbSyncOutSrc")
        self.gridlayout7.addWidget(self.cbSyncOutSrc,2,1,1,1)

        self.chbOutPos = QtGui.QCheckBox(self.groupBox_3)
        self.chbOutPos.setObjectName("chbOutPos")
        self.gridlayout7.addWidget(self.chbOutPos,1,0,1,1)

        self.cbOutPosSrc = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosSrc.setObjectName("cbOutPosSrc")
        self.gridlayout7.addWidget(self.cbOutPosSrc,1,1,1,1)

        self.label_12 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setTextFormat(QtCore.Qt.PlainText)
        self.label_12.setObjectName("label_12")
        self.gridlayout7.addWidget(self.label_12,0,1,1,1)

        self.label_11 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridlayout7.addWidget(self.label_11,0,2,1,1)

        self.cbOutPosMode = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosMode.setMinimumSize(QtCore.QSize(0,0))
        self.cbOutPosMode.setObjectName("cbOutPosMode")
        self.gridlayout7.addWidget(self.cbOutPosMode,1,2,1,1)

        self.cbOutPosEdge = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosEdge.setObjectName("cbOutPosEdge")
        self.gridlayout7.addWidget(self.cbOutPosEdge,1,3,1,1)

        self.cbOutPosDir = QtGui.QComboBox(self.groupBox_3)
        self.cbOutPosDir.setObjectName("cbOutPosDir")
        self.gridlayout7.addWidget(self.cbOutPosDir,1,4,1,1)

        self.label_10 = QtGui.QLabel(self.groupBox_3)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridlayout7.addWidget(self.label_10,0,3,1,1)
        self.gridlayout6.addWidget(self.groupBox_3,3,0,1,3)

        self.groupBox_4 = QtGui.QGroupBox(self.inOut_widget)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")

        self.gridlayout8 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout8.setMargin(9)
        self.gridlayout8.setSpacing(6)
        self.gridlayout8.setObjectName("gridlayout8")

        self.chbAuxPos2 = QtGui.QCheckBox(self.groupBox_4)
        self.chbAuxPos2.setObjectName("chbAuxPos2")
        self.gridlayout8.addWidget(self.chbAuxPos2,3,0,1,1)

        self.chbAuxPos1 = QtGui.QCheckBox(self.groupBox_4)
        self.chbAuxPos1.setObjectName("chbAuxPos1")
        self.gridlayout8.addWidget(self.chbAuxPos1,2,0,1,1)

        self.chbTarget = QtGui.QCheckBox(self.groupBox_4)
        self.chbTarget.setObjectName("chbTarget")
        self.gridlayout8.addWidget(self.chbTarget,1,0,1,1)

        self.cbTargetSrc = QtGui.QComboBox(self.groupBox_4)
        self.cbTargetSrc.setObjectName("cbTargetSrc")
        self.gridlayout8.addWidget(self.cbTargetSrc,1,1,1,1)

        self.label_14 = QtGui.QLabel(self.groupBox_4)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.gridlayout8.addWidget(self.label_14,0,1,1,1)

        self.cbAuxPos1Src = QtGui.QComboBox(self.groupBox_4)
        self.cbAuxPos1Src.setObjectName("cbAuxPos1Src")
        self.gridlayout8.addWidget(self.cbAuxPos1Src,2,1,1,1)

        self.cbAuxPos2Src = QtGui.QComboBox(self.groupBox_4)
        self.cbAuxPos2Src.setObjectName("cbAuxPos2Src")
        self.gridlayout8.addWidget(self.cbAuxPos2Src,3,1,1,1)
        self.gridlayout6.addWidget(self.groupBox_4,2,2,1,1)

        self.label_15 = QtGui.QLabel(self.inOut_widget)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.gridlayout6.addWidget(self.label_15,0,0,1,1)

        spacerItem7 = QtGui.QSpacerItem(121,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem7,1,1,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.inOut_widget)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout9 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout9.setMargin(9)
        self.gridlayout9.setSpacing(6)
        self.gridlayout9.setObjectName("gridlayout9")

        self.label_8 = QtGui.QLabel(self.groupBox_2)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridlayout9.addWidget(self.label_8,0,3,1,1)

        self.label_7 = QtGui.QLabel(self.groupBox_2)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridlayout9.addWidget(self.label_7,0,2,1,1)

        self.label_6 = QtGui.QLabel(self.groupBox_2)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridlayout9.addWidget(self.label_6,0,1,1,1)

        self.cbInPosDir = QtGui.QComboBox(self.groupBox_2)
        self.cbInPosDir.setObjectName("cbInPosDir")
        self.gridlayout9.addWidget(self.cbInPosDir,1,3,1,1)

        self.cbEncInDir = QtGui.QComboBox(self.groupBox_2)
        self.cbEncInDir.setObjectName("cbEncInDir")
        self.gridlayout9.addWidget(self.cbEncInDir,2,3,1,1)

        self.cbSyncInDir = QtGui.QComboBox(self.groupBox_2)
        self.cbSyncInDir.setObjectName("cbSyncInDir")
        self.gridlayout9.addWidget(self.cbSyncInDir,3,3,1,1)

        self.cbEncInEdge = QtGui.QComboBox(self.groupBox_2)
        self.cbEncInEdge.setObjectName("cbEncInEdge")
        self.gridlayout9.addWidget(self.cbEncInEdge,2,2,1,1)

        self.cbSyncInEdge = QtGui.QComboBox(self.groupBox_2)
        self.cbSyncInEdge.setObjectName("cbSyncInEdge")
        self.gridlayout9.addWidget(self.cbSyncInEdge,3,2,1,1)

        self.cbInPosEdge = QtGui.QComboBox(self.groupBox_2)
        self.cbInPosEdge.setObjectName("cbInPosEdge")
        self.gridlayout9.addWidget(self.cbInPosEdge,1,2,1,1)

        self.cbInPosMode = QtGui.QComboBox(self.groupBox_2)
        self.cbInPosMode.setMinimumSize(QtCore.QSize(0,0))
        self.cbInPosMode.setObjectName("cbInPosMode")
        self.gridlayout9.addWidget(self.cbInPosMode,1,1,1,1)

        self.chbInPos = QtGui.QCheckBox(self.groupBox_2)
        self.chbInPos.setObjectName("chbInPos")
        self.gridlayout9.addWidget(self.chbInPos,1,0,1,1)

        self.chbEncIn = QtGui.QCheckBox(self.groupBox_2)
        self.chbEncIn.setObjectName("chbEncIn")
        self.gridlayout9.addWidget(self.chbEncIn,2,0,1,1)

        self.chbSyncIn = QtGui.QCheckBox(self.groupBox_2)
        self.chbSyncIn.setObjectName("chbSyncIn")
        self.gridlayout9.addWidget(self.chbSyncIn,3,0,1,1)

        self.cbSyncInMode = QtGui.QComboBox(self.groupBox_2)
        self.cbSyncInMode.setObjectName("cbSyncInMode")
        self.gridlayout9.addWidget(self.cbSyncInMode,3,1,1,1)

        self.cbEncInMode = QtGui.QComboBox(self.groupBox_2)
        self.cbEncInMode.setObjectName("cbEncInMode")
        self.gridlayout9.addWidget(self.cbEncInMode,2,1,1,1)
        self.gridlayout6.addWidget(self.groupBox_2,2,0,1,2)

        self.listPredefined = QtGui.QListWidget(self.inOut_widget)
        self.listPredefined.setMaximumSize(QtCore.QSize(16777215,100))
        self.listPredefined.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.listPredefined.setObjectName("listPredefined")
        self.gridlayout6.addWidget(self.listPredefined,1,0,1,1)

        self.btnClear = QtGui.QPushButton(self.inOut_widget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClear.sizePolicy().hasHeightForWidth())
        self.btnClear.setSizePolicy(sizePolicy)
        self.btnClear.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-session-halt.png"))
        self.btnClear.setObjectName("btnClear")
        self.gridlayout6.addWidget(self.btnClear,0,1,1,1)
        self.tabSignals.addTab(self.tab_InOut,"")

        self.tab_aux = QtGui.QWidget()
        self.tab_aux.setObjectName("tab_aux")

        self.aux_widget = QtGui.QWidget(self.tab_aux)
        self.aux_widget.setGeometry(QtCore.QRect(10,20,524,240))
        self.aux_widget.setObjectName("aux_widget")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.aux_widget)
        self.hboxlayout2.setMargin(9)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.groupBox_5 = QtGui.QGroupBox(self.aux_widget)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")

        self.gridlayout10 = QtGui.QGridLayout(self.groupBox_5)
        self.gridlayout10.setMargin(9)
        self.gridlayout10.setSpacing(6)
        self.gridlayout10.setObjectName("gridlayout10")

        self.chbSyncAuxIn = QtGui.QCheckBox(self.groupBox_5)
        self.chbSyncAuxIn.setObjectName("chbSyncAuxIn")
        self.gridlayout10.addWidget(self.chbSyncAuxIn,6,0,1,1)

        self.cbSyncAuxInPol = QtGui.QComboBox(self.groupBox_5)
        self.cbSyncAuxInPol.setObjectName("cbSyncAuxInPol")
        self.gridlayout10.addWidget(self.cbSyncAuxInPol,6,1,1,1)

        self.label_24 = QtGui.QLabel(self.groupBox_5)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.gridlayout10.addWidget(self.label_24,0,1,1,1)

        self.chbInPosAux = QtGui.QCheckBox(self.groupBox_5)
        self.chbInPosAux.setObjectName("chbInPosAux")
        self.gridlayout10.addWidget(self.chbInPosAux,1,0,1,1)

        self.cbInPosAuxPol = QtGui.QComboBox(self.groupBox_5)
        self.cbInPosAuxPol.setObjectName("cbInPosAuxPol")
        self.gridlayout10.addWidget(self.cbInPosAuxPol,1,1,1,1)

        self.cbEncAuxPol = QtGui.QComboBox(self.groupBox_5)
        self.cbEncAuxPol.setObjectName("cbEncAuxPol")
        self.gridlayout10.addWidget(self.cbEncAuxPol,2,1,1,1)

        self.chbEncAux = QtGui.QCheckBox(self.groupBox_5)
        self.chbEncAux.setObjectName("chbEncAux")
        self.gridlayout10.addWidget(self.chbEncAux,2,0,1,1)

        self.cbLimitNegPol = QtGui.QComboBox(self.groupBox_5)
        self.cbLimitNegPol.setObjectName("cbLimitNegPol")
        self.gridlayout10.addWidget(self.cbLimitNegPol,4,1,1,1)

        self.chbLimitNeg = QtGui.QCheckBox(self.groupBox_5)
        self.chbLimitNeg.setObjectName("chbLimitNeg")
        self.gridlayout10.addWidget(self.chbLimitNeg,4,0,1,1)

        self.chbLimitPos = QtGui.QCheckBox(self.groupBox_5)
        self.chbLimitPos.setObjectName("chbLimitPos")
        self.gridlayout10.addWidget(self.chbLimitPos,3,0,1,1)

        self.cbLimitPosPol = QtGui.QComboBox(self.groupBox_5)
        self.cbLimitPosPol.setObjectName("cbLimitPosPol")
        self.gridlayout10.addWidget(self.cbLimitPosPol,3,1,1,1)

        self.cbHomePol = QtGui.QComboBox(self.groupBox_5)
        self.cbHomePol.setObjectName("cbHomePol")
        self.gridlayout10.addWidget(self.cbHomePol,5,1,1,1)

        self.chbHome = QtGui.QCheckBox(self.groupBox_5)
        self.chbHome.setObjectName("chbHome")
        self.gridlayout10.addWidget(self.chbHome,5,0,1,1)
        self.hboxlayout2.addWidget(self.groupBox_5)

        self.groupBox_10 = QtGui.QGroupBox(self.aux_widget)

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.groupBox_10.setFont(font)
        self.groupBox_10.setObjectName("groupBox_10")

        self.gridlayout11 = QtGui.QGridLayout(self.groupBox_10)
        self.gridlayout11.setMargin(9)
        self.gridlayout11.setSpacing(6)
        self.gridlayout11.setObjectName("gridlayout11")

        self.chbInfoA = QtGui.QCheckBox(self.groupBox_10)
        self.chbInfoA.setObjectName("chbInfoA")
        self.gridlayout11.addWidget(self.chbInfoA,2,0,1,1)

        self.cbInfoASrc = QtGui.QComboBox(self.groupBox_10)
        self.cbInfoASrc.setObjectName("cbInfoASrc")
        self.gridlayout11.addWidget(self.cbInfoASrc,2,1,1,1)

        self.cbInfoAPol = QtGui.QComboBox(self.groupBox_10)
        self.cbInfoAPol.setObjectName("cbInfoAPol")
        self.gridlayout11.addWidget(self.cbInfoAPol,2,2,1,1)

        self.cbOutPosAuxPol = QtGui.QComboBox(self.groupBox_10)
        self.cbOutPosAuxPol.setObjectName("cbOutPosAuxPol")
        self.gridlayout11.addWidget(self.cbOutPosAuxPol,1,2,1,1)

        self.cbOutPosAuxSrc = QtGui.QComboBox(self.groupBox_10)
        self.cbOutPosAuxSrc.setObjectName("cbOutPosAuxSrc")
        self.gridlayout11.addWidget(self.cbOutPosAuxSrc,1,1,1,1)

        self.chbOutPosAux = QtGui.QCheckBox(self.groupBox_10)
        self.chbOutPosAux.setObjectName("chbOutPosAux")
        self.gridlayout11.addWidget(self.chbOutPosAux,1,0,1,1)

        self.cbInfoBPol = QtGui.QComboBox(self.groupBox_10)
        self.cbInfoBPol.setObjectName("cbInfoBPol")
        self.gridlayout11.addWidget(self.cbInfoBPol,3,2,1,1)

        self.cbInfoBSrc = QtGui.QComboBox(self.groupBox_10)
        self.cbInfoBSrc.setObjectName("cbInfoBSrc")
        self.gridlayout11.addWidget(self.cbInfoBSrc,3,1,1,1)

        self.chbInfoB = QtGui.QCheckBox(self.groupBox_10)
        self.chbInfoB.setObjectName("chbInfoB")
        self.gridlayout11.addWidget(self.chbInfoB,3,0,1,1)

        self.chbInfoC = QtGui.QCheckBox(self.groupBox_10)
        self.chbInfoC.setObjectName("chbInfoC")
        self.gridlayout11.addWidget(self.chbInfoC,4,0,1,1)

        self.chbSyncAuxOut = QtGui.QCheckBox(self.groupBox_10)
        self.chbSyncAuxOut.setObjectName("chbSyncAuxOut")
        self.gridlayout11.addWidget(self.chbSyncAuxOut,5,0,1,1)

        self.cbInfoCSrc = QtGui.QComboBox(self.groupBox_10)
        self.cbInfoCSrc.setObjectName("cbInfoCSrc")
        self.gridlayout11.addWidget(self.cbInfoCSrc,4,1,1,1)

        self.cbInfoCPol = QtGui.QComboBox(self.groupBox_10)
        self.cbInfoCPol.setObjectName("cbInfoCPol")
        self.gridlayout11.addWidget(self.cbInfoCPol,4,2,1,1)

        self.cbSyncAuxOutPol = QtGui.QComboBox(self.groupBox_10)
        self.cbSyncAuxOutPol.setObjectName("cbSyncAuxOutPol")
        self.gridlayout11.addWidget(self.cbSyncAuxOutPol,5,2,1,1)

        self.cbSyncAuxOutSrc = QtGui.QComboBox(self.groupBox_10)
        self.cbSyncAuxOutSrc.setObjectName("cbSyncAuxOutSrc")
        self.gridlayout11.addWidget(self.cbSyncAuxOutSrc,5,1,1,1)

        self.label_26 = QtGui.QLabel(self.groupBox_10)

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.gridlayout11.addWidget(self.label_26,0,2,1,1)

        self.label_27 = QtGui.QLabel(self.groupBox_10)

        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_27.setFont(font)
        self.label_27.setTextFormat(QtCore.Qt.PlainText)
        self.label_27.setObjectName("label_27")
        self.gridlayout11.addWidget(self.label_27,0,1,1,1)
        self.hboxlayout2.addWidget(self.groupBox_10)
        self.tabSignals.addTab(self.tab_aux,"")

        self.tab_connectors = QtGui.QWidget()
        self.tab_connectors.setObjectName("tab_connectors")

        self.labels_widget = QtGui.QWidget(self.tab_connectors)
        self.labels_widget.setGeometry(QtCore.QRect(30,20,451,525))
        self.labels_widget.setObjectName("labels_widget")

        self.gridlayout12 = QtGui.QGridLayout(self.labels_widget)
        self.gridlayout12.setMargin(2)
        self.gridlayout12.setSpacing(2)
        self.gridlayout12.setObjectName("gridlayout12")

        self.label_5 = QtGui.QLabel(self.labels_widget)
        self.label_5.setPixmap(QtGui.QPixmap(":/images/IcepapCfg Icons/encoder.png"))
        self.label_5.setObjectName("label_5")
        self.gridlayout12.addWidget(self.label_5,1,1,1,1)

        self.label_4 = QtGui.QLabel(self.labels_widget)
        self.label_4.setPixmap(QtGui.QPixmap(":/images/IcepapCfg Icons/axis.png"))
        self.label_4.setObjectName("label_4")
        self.gridlayout12.addWidget(self.label_4,0,1,1,1)

        spacerItem8 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout12.addItem(spacerItem8,0,2,1,1)

        spacerItem9 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout12.addItem(spacerItem9,0,0,1,1)
        self.tabSignals.addTab(self.tab_connectors,"")
        self.hboxlayout1.addWidget(self.tabSignals)
        self.tabWidget.addTab(self.tab,"")
        self.gridlayout.addWidget(self.tabWidget,1,0,1,1)

        self.frame_3 = QtGui.QFrame(PageiPapDriver)
        self.frame_3.setMinimumSize(QtCore.QSize(16,75))

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(224,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(224,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,brush)

        brush = QtGui.QBrush(QtGui.QColor(224,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(224,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Window,brush)
        self.frame_3.setPalette(palette)
        self.frame_3.setAutoFillBackground(True)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        self.gridlayout13 = QtGui.QGridLayout(self.frame_3)
        self.gridlayout13.setMargin(9)
        self.gridlayout13.setSpacing(6)
        self.gridlayout13.setObjectName("gridlayout13")

        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setObjectName("label_2")
        self.gridlayout13.addWidget(self.label_2,2,0,1,1)

        self.txtDriverName = QtGui.QLineEdit(self.frame_3)
        self.txtDriverName.setMinimumSize(QtCore.QSize(125,25))
        self.txtDriverName.setMaximumSize(QtCore.QSize(125,16777215))
        self.txtDriverName.setObjectName("txtDriverName")
        self.gridlayout13.addWidget(self.txtDriverName,2,1,1,1)

        spacerItem10 = QtGui.QSpacerItem(240,16,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout13.addItem(spacerItem10,2,2,1,1)

        self.line = QtGui.QFrame(self.frame_3)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout13.addWidget(self.line,1,0,1,3)

        self.txtDescription = QtGui.QLabel(self.frame_3)
        self.txtDescription.setObjectName("txtDescription")
        self.gridlayout13.addWidget(self.txtDescription,0,0,1,3)
        self.gridlayout.addWidget(self.frame_3,0,0,1,1)

        self.frame_right = QtGui.QFrame(PageiPapDriver)
        self.frame_right.setMinimumSize(QtCore.QSize(220,499))
        self.frame_right.setMaximumSize(QtCore.QSize(220,16777215))
        self.frame_right.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_right.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_right.setObjectName("frame_right")

        self.vboxlayout = QtGui.QVBoxLayout(self.frame_right)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(self.frame_right)
        self.label.setPixmap(QtGui.QPixmap(":/logos/IcepapCfg Icons/Icepap.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        spacerItem11 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem11)

        self.frame_test = QtGui.QFrame(self.frame_right)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_test.sizePolicy().hasHeightForWidth())
        self.frame_test.setSizePolicy(sizePolicy)
        self.frame_test.setMinimumSize(QtCore.QSize(202,319))
        self.frame_test.setMaximumSize(QtCore.QSize(250,16777215))
        self.frame_test.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_test.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_test.setObjectName("frame_test")

        self.gridlayout14 = QtGui.QGridLayout(self.frame_test)
        self.gridlayout14.setMargin(9)
        self.gridlayout14.setSpacing(6)
        self.gridlayout14.setObjectName("gridlayout14")

        self.btnGO = QtGui.QPushButton(self.frame_test)
        self.btnGO.setMaximumSize(QtCore.QSize(24,24))
        self.btnGO.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/go-absolute.png"))
        self.btnGO.setIconSize(QtCore.QSize(22,22))
        self.btnGO.setObjectName("btnGO")
        self.gridlayout14.addWidget(self.btnGO,7,6,1,1)

        self.frame_4 = QtGui.QFrame(self.frame_test)
        self.frame_4.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

        self.hboxlayout3 = QtGui.QHBoxLayout(self.frame_4)
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(0)
        self.hboxlayout3.setObjectName("hboxlayout3")

        spacerItem12 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem12)

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

        self.gridlayout15 = QtGui.QGridLayout(self.frame_leds)
        self.gridlayout15.setMargin(2)
        self.gridlayout15.setSpacing(2)
        self.gridlayout15.setObjectName("gridlayout15")

        self.textLabel1_6_4 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6_4.setFont(font)
        self.textLabel1_6_4.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1_6_4.setObjectName("textLabel1_6_4")
        self.gridlayout15.addWidget(self.textLabel1_6_4,1,1,1,1)

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
        self.gridlayout15.addWidget(self.LedLimitPos,0,3,1,1)

        self.textLabel1_6_5 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6_5.setFont(font)
        self.textLabel1_6_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.textLabel1_6_5.setObjectName("textLabel1_6_5")
        self.gridlayout15.addWidget(self.textLabel1_6_5,1,0,1,1)

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
        self.gridlayout15.addWidget(self.LedHome,0,2,1,1)

        self.textLabel1_6_3 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6_3.setFont(font)
        self.textLabel1_6_3.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1_6_3.setObjectName("textLabel1_6_3")
        self.gridlayout15.addWidget(self.textLabel1_6_3,1,2,1,1)

        self.textLabel1_6 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6.setFont(font)
        self.textLabel1_6.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1_6.setObjectName("textLabel1_6")
        self.gridlayout15.addWidget(self.textLabel1_6,1,3,1,1)

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
        self.gridlayout15.addWidget(self.LedStep,0,1,1,1)

        self.textLabel1_6_2 = QtGui.QLabel(self.frame_leds)

        font = QtGui.QFont()
        font.setPointSize(7)
        self.textLabel1_6_2.setFont(font)
        self.textLabel1_6_2.setAlignment(QtCore.Qt.AlignCenter)
        self.textLabel1_6_2.setObjectName("textLabel1_6_2")
        self.gridlayout15.addWidget(self.textLabel1_6_2,1,4,1,1)

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
        self.gridlayout15.addWidget(self.LedLimitNeg,0,4,1,1)

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
        self.gridlayout15.addWidget(self.LedError,0,0,1,1)
        self.hboxlayout3.addWidget(self.frame_leds)

        spacerItem13 = QtGui.QSpacerItem(21,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem13)
        self.gridlayout14.addWidget(self.frame_4,5,0,1,7)

        self.textLabel1_3_3_2 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3_3_2.setFont(font)
        self.textLabel1_3_3_2.setObjectName("textLabel1_3_3_2")
        self.gridlayout14.addWidget(self.textLabel1_3_3_2,2,0,1,5)

        self.txtAcceleration = QtGui.QLineEdit(self.frame_test)
        self.txtAcceleration.setMaximumSize(QtCore.QSize(16777215,24))

        font = QtGui.QFont()
        font.setPointSize(8)
        self.txtAcceleration.setFont(font)
        self.txtAcceleration.setObjectName("txtAcceleration")
        self.gridlayout14.addWidget(self.txtAcceleration,2,5,1,2)

        self.textLabel3 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel3.setFont(font)
        self.textLabel3.setObjectName("textLabel3")
        self.gridlayout14.addWidget(self.textLabel3,6,0,1,1)

        self.btnStopMotor = QtGui.QPushButton(self.frame_test)
        self.btnStopMotor.setMaximumSize(QtCore.QSize(24,24))
        self.btnStopMotor.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-session-halt.png"))
        self.btnStopMotor.setIconSize(QtCore.QSize(22,22))
        self.btnStopMotor.setObjectName("btnStopMotor")
        self.gridlayout14.addWidget(self.btnStopMotor,8,1,1,2)

        self.txtMvAbsolute = QtGui.QLineEdit(self.frame_test)
        self.txtMvAbsolute.setMaximumSize(QtCore.QSize(100,24))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.txtMvAbsolute.setFont(font)
        self.txtMvAbsolute.setObjectName("txtMvAbsolute")
        self.gridlayout14.addWidget(self.txtMvAbsolute,7,4,1,2)

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
        self.gridlayout14.addWidget(self.sbFactor,0,5,1,2)

        self.textLabel1_3_3 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3_3.setFont(font)
        self.textLabel1_3_3.setObjectName("textLabel1_3_3")
        self.gridlayout14.addWidget(self.textLabel1_3_3,1,0,1,5)

        self.frame = QtGui.QFrame(self.frame_test)
        self.frame.setFrameShape(QtGui.QFrame.HLine)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridlayout14.addWidget(self.frame,4,0,1,7)

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
        self.gridlayout14.addWidget(self.LCDPosition,6,1,1,6)

        self.sbPosition = QtGui.QSpinBox(self.frame_test)
        self.sbPosition.setMaximumSize(QtCore.QSize(16777215,24))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.sbPosition.setFont(font)
        self.sbPosition.setMaximum(99999)
        self.sbPosition.setProperty("value",QtCore.QVariant(0))
        self.sbPosition.setObjectName("sbPosition")
        self.gridlayout14.addWidget(self.sbPosition,3,5,1,2)

        self.textLabel1_3_4 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3_4.setFont(font)
        self.textLabel1_3_4.setObjectName("textLabel1_3_4")
        self.gridlayout14.addWidget(self.textLabel1_3_4,3,0,1,2)

        self.textLabel1_3_3_2_2 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3_3_2_2.setFont(font)
        self.textLabel1_3_3_2_2.setObjectName("textLabel1_3_3_2_2")
        self.gridlayout14.addWidget(self.textLabel1_3_3_2_2,0,0,1,5)

        self.txtSpeed = QtGui.QLineEdit(self.frame_test)
        self.txtSpeed.setMaximumSize(QtCore.QSize(16777215,24))

        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.txtSpeed.setFont(font)
        self.txtSpeed.setObjectName("txtSpeed")
        self.gridlayout14.addWidget(self.txtSpeed,1,5,1,2)

        self.BtnSetPos = QtGui.QPushButton(self.frame_test)
        self.BtnSetPos.setMaximumSize(QtCore.QSize(40,24))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.BtnSetPos.setFont(font)
        self.BtnSetPos.setObjectName("BtnSetPos")
        self.gridlayout14.addWidget(self.BtnSetPos,3,3,1,2)

        self.btnEnable = QtGui.QPushButton(self.frame_test)
        self.btnEnable.setMaximumSize(QtCore.QSize(50,16777215))

        font = QtGui.QFont()
        font.setFamily("Sans Serif")
        font.setPointSize(8)
        self.btnEnable.setFont(font)
        self.btnEnable.setCheckable(True)
        self.btnEnable.setChecked(False)
        self.btnEnable.setObjectName("btnEnable")
        self.gridlayout14.addWidget(self.btnEnable,8,0,1,1)

        self.btnGORelativePos = QtGui.QPushButton(self.frame_test)
        self.btnGORelativePos.setMaximumSize(QtCore.QSize(24,24))
        self.btnGORelativePos.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/go-relative.png"))
        self.btnGORelativePos.setIconSize(QtCore.QSize(22,22))
        self.btnGORelativePos.setObjectName("btnGORelativePos")
        self.gridlayout14.addWidget(self.btnGORelativePos,8,6,1,1)

        self.btnGORelativeNeg = QtGui.QPushButton(self.frame_test)
        self.btnGORelativeNeg.setMaximumSize(QtCore.QSize(24,24))
        self.btnGORelativeNeg.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/go-relative2.png"))
        self.btnGORelativeNeg.setIconSize(QtCore.QSize(22,22))
        self.btnGORelativeNeg.setObjectName("btnGORelativeNeg")
        self.gridlayout14.addWidget(self.btnGORelativeNeg,8,3,1,1)

        self.textLabel1_3 = QtGui.QLabel(self.frame_test)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.textLabel1_3.setFont(font)
        self.textLabel1_3.setObjectName("textLabel1_3")
        self.gridlayout14.addWidget(self.textLabel1_3,7,0,1,4)

        self.txtGORelative = QtGui.QLineEdit(self.frame_test)
        self.txtGORelative.setMaximumSize(QtCore.QSize(100,24))

        font = QtGui.QFont()
        font.setPointSize(7)
        self.txtGORelative.setFont(font)
        self.txtGORelative.setObjectName("txtGORelative")
        self.gridlayout14.addWidget(self.txtGORelative,8,4,1,2)

        self.groupBox = QtGui.QGroupBox(self.frame_test)
        self.groupBox.setMinimumSize(QtCore.QSize(0,40))
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")

        self.hboxlayout4 = QtGui.QHBoxLayout(self.groupBox)
        self.hboxlayout4.setMargin(2)
        self.hboxlayout4.setSpacing(2)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.sliderJog = QtGui.QSlider(self.groupBox)
        self.sliderJog.setMouseTracking(False)
        self.sliderJog.setMinimum(-4)
        self.sliderJog.setMaximum(4)
        self.sliderJog.setPageStep(1)
        self.sliderJog.setProperty("value",QtCore.QVariant(0))
        self.sliderJog.setSliderPosition(0)
        self.sliderJog.setOrientation(QtCore.Qt.Horizontal)
        self.sliderJog.setInvertedAppearance(False)
        self.sliderJog.setInvertedControls(False)
        self.sliderJog.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sliderJog.setTickInterval(2)
        self.sliderJog.setObjectName("sliderJog")
        self.hboxlayout4.addWidget(self.sliderJog)
        self.gridlayout14.addWidget(self.groupBox,9,0,1,7)
        self.vboxlayout.addWidget(self.frame_test)

        spacerItem14 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem14)

        self.btnApplyCfg = QtGui.QPushButton(self.frame_right)
        self.btnApplyCfg.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/gnome-dev-floppy.png"))
        self.btnApplyCfg.setIconSize(QtCore.QSize(20,20))
        self.btnApplyCfg.setObjectName("btnApplyCfg")
        self.vboxlayout.addWidget(self.btnApplyCfg)

        self.btnUndo = QtGui.QPushButton(self.frame_right)
        self.btnUndo.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/undo.png"))
        self.btnUndo.setIconSize(QtCore.QSize(20,20))
        self.btnUndo.setObjectName("btnUndo")
        self.vboxlayout.addWidget(self.btnUndo)

        self.btnTemplates = QtGui.QPushButton(self.frame_right)
        self.btnTemplates.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/notes.png"))
        self.btnTemplates.setIconSize(QtCore.QSize(20,20))
        self.btnTemplates.setObjectName("btnTemplates")
        self.vboxlayout.addWidget(self.btnTemplates)

        self.btnHistoric = QtGui.QPushButton(self.frame_right)
        self.btnHistoric.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btnHistoric.setIcon(QtGui.QIcon(":/icons/IcepapCfg Icons/calendar.png"))
        self.btnHistoric.setIconSize(QtCore.QSize(20,20))
        self.btnHistoric.setObjectName("btnHistoric")
        self.vboxlayout.addWidget(self.btnHistoric)
        self.gridlayout.addWidget(self.frame_right,0,1,2,1)

        self.retranslateUi(PageiPapDriver)
        self.tabWidget.setCurrentIndex(0)
        self.tabSignals.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PageiPapDriver)

    def retranslateUi(self, PageiPapDriver):
        PageiPapDriver.setWindowTitle(QtGui.QApplication.translate("PageiPapDriver", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Current", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("PageiPapDriver", "Idle", None, QtGui.QApplication.UnicodeUTF8))
        self.IB.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "current to the motor when the motor is at rest", None, QtGui.QApplication.UnicodeUTF8))
        self.II.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "current to the motor when the motor is at rest", None, QtGui.QApplication.UnicodeUTF8))
        self.IN.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "current to the motor during steady rate speed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("PageiPapDriver", "Boost", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_7.setTitle(QtGui.QApplication.translate("PageiPapDriver", "PI Current Regulation", None, QtGui.QApplication.UnicodeUTF8))
        self.IREGP.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "proportional constant in the PI current regulator", None, QtGui.QApplication.UnicodeUTF8))
        self.IREGI.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "integral constant in the PI current regulator", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("PageiPapDriver", "Integral", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("PageiPapDriver", "Proportional", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("PageiPapDriver", "Nominal", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("PageiPapDriver", "Micro Stepping", None, QtGui.QApplication.UnicodeUTF8))
        self.AUXPS.setText(QtGui.QApplication.translate("PageiPapDriver", "Aux Supply 5V", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_9.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Voltage", None, QtGui.QApplication.UnicodeUTF8))
        self.SD.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "Vcc to the motor phases when motor is in rest", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("PageiPapDriver", "Stand-by Voltage", None, QtGui.QApplication.UnicodeUTF8))
        self.SDMAX.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "Vcc to the motor phases when motor is moving", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("PageiPapDriver", "Drive Voltage", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_8.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Limit switches", None, QtGui.QApplication.UnicodeUTF8))
        self.TDIR.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "change if there is a mismatch between dir and limits", None, QtGui.QApplication.UnicodeUTF8))
        self.TDIR.setText(QtGui.QApplication.translate("PageiPapDriver", "Reverse direction", None, QtGui.QApplication.UnicodeUTF8))
        self.PSW.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "limit switches polarity", None, QtGui.QApplication.UnicodeUTF8))
        self.PSW.setText(QtGui.QApplication.translate("PageiPapDriver", "Reverse polarity", None, QtGui.QApplication.UnicodeUTF8))
        self.ESW.setToolTip(QtGui.QApplication.translate("PageiPapDriver", "enable/disable hardware limit switches protection", None, QtGui.QApplication.UnicodeUTF8))
        self.ESW.setText(QtGui.QApplication.translate("PageiPapDriver", "Enabled", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("PageiPapDriver", "Driver", None, QtGui.QApplication.UnicodeUTF8))
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
        self.btnClear.setText(QtGui.QApplication.translate("PageiPapDriver", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.tabSignals.setTabText(self.tabSignals.indexOf(self.tab_InOut), QtGui.QApplication.translate("PageiPapDriver", "Input/Output", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Input Signals", None, QtGui.QApplication.UnicodeUTF8))
        self.chbSyncAuxIn.setText(QtGui.QApplication.translate("PageiPapDriver", "SyncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxInPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxInPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setText(QtGui.QApplication.translate("PageiPapDriver", "Polarity", None, QtGui.QApplication.UnicodeUTF8))
        self.chbInPosAux.setText(QtGui.QApplication.translate("PageiPapDriver", "InPosAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInPosAuxPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInPosAuxPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbEncAuxPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbEncAuxPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.chbEncAux.setText(QtGui.QApplication.translate("PageiPapDriver", "EncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbLimitNegPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbLimitNegPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.chbLimitNeg.setText(QtGui.QApplication.translate("PageiPapDriver", "Limit-", None, QtGui.QApplication.UnicodeUTF8))
        self.chbLimitPos.setText(QtGui.QApplication.translate("PageiPapDriver", "Limit+", None, QtGui.QApplication.UnicodeUTF8))
        self.cbLimitPosPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbLimitPosPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbHomePol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbHomePol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.chbHome.setText(QtGui.QApplication.translate("PageiPapDriver", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_10.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Output Signals", None, QtGui.QApplication.UnicodeUTF8))
        self.chbInfoA.setText(QtGui.QApplication.translate("PageiPapDriver", "InfoA", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoASrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 0", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoASrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 1", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoASrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit-", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoASrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit+", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoASrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoASrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoASrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "InposAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoASrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoAPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoAPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 0", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 1", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit-", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit+", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "InposAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbOutPosAuxSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.chbOutPosAux.setText(QtGui.QApplication.translate("PageiPapDriver", "OutPosAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 0", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 1", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit-", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit+", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "InposAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoBSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.chbInfoB.setText(QtGui.QApplication.translate("PageiPapDriver", "InfoB", None, QtGui.QApplication.UnicodeUTF8))
        self.chbInfoC.setText(QtGui.QApplication.translate("PageiPapDriver", "InfoC", None, QtGui.QApplication.UnicodeUTF8))
        self.chbSyncAuxOut.setText(QtGui.QApplication.translate("PageiPapDriver", "SyncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 0", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 1", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit-", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit+", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "InposAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbInfoCPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutPol.addItem(QtGui.QApplication.translate("PageiPapDriver", "Inverted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 0", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Fixed 1", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit-", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Limit+", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "EncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "InposAux", None, QtGui.QApplication.UnicodeUTF8))
        self.cbSyncAuxOutSrc.addItem(QtGui.QApplication.translate("PageiPapDriver", "SyncAux", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("PageiPapDriver", "Polarity", None, QtGui.QApplication.UnicodeUTF8))
        self.label_27.setText(QtGui.QApplication.translate("PageiPapDriver", "Source", None, QtGui.QApplication.UnicodeUTF8))
        self.tabSignals.setTabText(self.tabSignals.indexOf(self.tab_aux), QtGui.QApplication.translate("PageiPapDriver", "Aux signals", None, QtGui.QApplication.UnicodeUTF8))
        self.tabSignals.setTabText(self.tabSignals.indexOf(self.tab_connectors), QtGui.QApplication.translate("PageiPapDriver", "Connectors", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("PageiPapDriver", "Signals", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PageiPapDriver", "Driver name", None, QtGui.QApplication.UnicodeUTF8))
        self.txtDescription.setText(QtGui.QApplication.translate("PageiPapDriver", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6_4.setText(QtGui.QApplication.translate("PageiPapDriver", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:7pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Step</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6_5.setText(QtGui.QApplication.translate("PageiPapDriver", "Stat", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6_3.setText(QtGui.QApplication.translate("PageiPapDriver", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6.setText(QtGui.QApplication.translate("PageiPapDriver", "Limit+", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_6_2.setText(QtGui.QApplication.translate("PageiPapDriver", "Limit-", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3_3_2.setText(QtGui.QApplication.translate("PageiPapDriver", "Acceleration", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel3.setText(QtGui.QApplication.translate("PageiPapDriver", "Position", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3_3.setText(QtGui.QApplication.translate("PageiPapDriver", "Speed (steps/sec)", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3_4.setText(QtGui.QApplication.translate("PageiPapDriver", "Position", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3_3_2_2.setText(QtGui.QApplication.translate("PageiPapDriver", "Steps x mm/degree", None, QtGui.QApplication.UnicodeUTF8))
        self.BtnSetPos.setText(QtGui.QApplication.translate("PageiPapDriver", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.btnEnable.setText(QtGui.QApplication.translate("PageiPapDriver", "enable", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1_3.setText(QtGui.QApplication.translate("PageiPapDriver", "Move absolute", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("PageiPapDriver", "Jog", None, QtGui.QApplication.UnicodeUTF8))
        self.btnApplyCfg.setText(QtGui.QApplication.translate("PageiPapDriver", "Apply Config", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUndo.setText(QtGui.QApplication.translate("PageiPapDriver", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.btnTemplates.setText(QtGui.QApplication.translate("PageiPapDriver", "Driver Templates", None, QtGui.QApplication.UnicodeUTF8))
        self.btnHistoric.setText(QtGui.QApplication.translate("PageiPapDriver", "Historic Cfgs", None, QtGui.QApplication.UnicodeUTF8))



