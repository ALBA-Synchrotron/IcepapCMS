# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'closedloop.ui'
#
# Created: Mon Aug  3 17:26:45 2009
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_closedloop(object):
    def setupUi(self, closedloop):
        closedloop.setObjectName("closedloop")
        closedloop.resize(291, 386)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(closedloop.sizePolicy().hasHeightForWidth())
        closedloop.setSizePolicy(sizePolicy)
        closedloop.setMinimumSize(QtCore.QSize(256, 259))
        self.gridlayout = QtGui.QGridLayout(closedloop)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")
        self.closedloop_frame = QtGui.QFrame(closedloop)
        self.closedloop_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.closedloop_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.closedloop_frame.setObjectName("closedloop_frame")
        self.vboxlayout = QtGui.QVBoxLayout(self.closedloop_frame)
        self.vboxlayout.setObjectName("vboxlayout")
        self.groupBox = QtGui.QGroupBox(self.closedloop_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(220, 161))
        self.groupBox.setObjectName("groupBox")
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setSpacing(0)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.chkClosedLoop = QtGui.QCheckBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkClosedLoop.sizePolicy().hasHeightForWidth())
        self.chkClosedLoop.setSizePolicy(sizePolicy)
        self.chkClosedLoop.setMinimumSize(QtCore.QSize(200, 16))
        self.chkClosedLoop.setMaximumSize(QtCore.QSize(16777215, 22))
        self.chkClosedLoop.setObjectName("chkClosedLoop")
        self.vboxlayout1.addWidget(self.chkClosedLoop)
        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setContentsMargins(20, -1, -1, -1)
        self.gridlayout1.setObjectName("gridlayout1")
        self.label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(100, 16))
        self.label.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label, 0, 0, 1, 1)
        self.cfgPCLOOP = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgPCLOOP.sizePolicy().hasHeightForWidth())
        self.cfgPCLOOP.setSizePolicy(sizePolicy)
        self.cfgPCLOOP.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgPCLOOP.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgPCLOOP.setObjectName("cfgPCLOOP")
        self.gridlayout1.addWidget(self.cfgPCLOOP, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(100, 16))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3, 1, 0, 1, 1)
        self.cfgPCLTAU = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgPCLTAU.sizePolicy().hasHeightForWidth())
        self.cfgPCLTAU.setSizePolicy(sizePolicy)
        self.cfgPCLTAU.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgPCLTAU.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgPCLTAU.setMaximum(999999999.0)
        self.cfgPCLTAU.setSingleStep(0.01)
        self.cfgPCLTAU.setObjectName("cfgPCLTAU")
        self.gridlayout1.addWidget(self.cfgPCLTAU, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(100, 16))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2, 2, 0, 1, 1)
        self.cfgPCLERROR = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgPCLERROR.sizePolicy().hasHeightForWidth())
        self.cfgPCLERROR.setSizePolicy(sizePolicy)
        self.cfgPCLERROR.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgPCLERROR.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgPCLERROR.setMaximum(999999999)
        self.cfgPCLERROR.setObjectName("cfgPCLERROR")
        self.gridlayout1.addWidget(self.cfgPCLERROR, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(100, 16))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4, 3, 0, 1, 1)
        self.cfgPCLDEADBD = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgPCLDEADBD.sizePolicy().hasHeightForWidth())
        self.cfgPCLDEADBD.setSizePolicy(sizePolicy)
        self.cfgPCLDEADBD.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgPCLDEADBD.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgPCLDEADBD.setMaximum(999999999)
        self.cfgPCLDEADBD.setObjectName("cfgPCLDEADBD")
        self.gridlayout1.addWidget(self.cfgPCLDEADBD, 3, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(100, 16))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_6.setObjectName("label_6")
        self.gridlayout1.addWidget(self.label_6, 4, 0, 1, 1)
        self.cfgPCLSETLW = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgPCLSETLW.sizePolicy().hasHeightForWidth())
        self.cfgPCLSETLW.setSizePolicy(sizePolicy)
        self.cfgPCLSETLW.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgPCLSETLW.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgPCLSETLW.setMaximum(999999999)
        self.cfgPCLSETLW.setObjectName("cfgPCLSETLW")
        self.gridlayout1.addWidget(self.cfgPCLSETLW, 4, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(100, 16))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5, 5, 0, 1, 1)
        self.cfgPCLSETLT = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgPCLSETLT.sizePolicy().hasHeightForWidth())
        self.cfgPCLSETLT.setSizePolicy(sizePolicy)
        self.cfgPCLSETLT.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgPCLSETLT.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgPCLSETLT.setMaximum(1000000000.0)
        self.cfgPCLSETLT.setSingleStep(0.01)
        self.cfgPCLSETLT.setObjectName("cfgPCLSETLT")
        self.gridlayout1.addWidget(self.cfgPCLSETLT, 5, 1, 1, 1)
        self.vboxlayout1.addLayout(self.gridlayout1)
        self.vboxlayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.closedloop_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(220, 92))
        self.groupBox_2.setObjectName("groupBox_2")
        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout2.setSpacing(5)
        self.vboxlayout2.setContentsMargins(-1, 10, -1, -1)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.chkPositionControl = QtGui.QCheckBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPositionControl.sizePolicy().hasHeightForWidth())
        self.chkPositionControl.setSizePolicy(sizePolicy)
        self.chkPositionControl.setMinimumSize(QtCore.QSize(200, 16))
        self.chkPositionControl.setMaximumSize(QtCore.QSize(16777215, 22))
        self.chkPositionControl.setObjectName("chkPositionControl")
        self.vboxlayout2.addWidget(self.chkPositionControl)
        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setContentsMargins(20, -1, -1, -1)
        self.gridlayout2.setObjectName("gridlayout2")
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(100, 16))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_7.setObjectName("label_7")
        self.gridlayout2.addWidget(self.label_7, 0, 0, 1, 1)
        self.cfgCTRLENC = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgCTRLENC.sizePolicy().hasHeightForWidth())
        self.cfgCTRLENC.setSizePolicy(sizePolicy)
        self.cfgCTRLENC.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgCTRLENC.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgCTRLENC.setObjectName("cfgCTRLENC")
        self.gridlayout2.addWidget(self.cfgCTRLENC, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(100, 16))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 22))
        self.label_8.setObjectName("label_8")
        self.gridlayout2.addWidget(self.label_8, 1, 0, 1, 1)
        self.cfgCTRLERROR = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cfgCTRLERROR.sizePolicy().hasHeightForWidth())
        self.cfgCTRLERROR.setSizePolicy(sizePolicy)
        self.cfgCTRLERROR.setMinimumSize(QtCore.QSize(70, 16))
        self.cfgCTRLERROR.setMaximumSize(QtCore.QSize(16777215, 22))
        self.cfgCTRLERROR.setMaximum(999999999)
        self.cfgCTRLERROR.setObjectName("cfgCTRLERROR")
        self.gridlayout2.addWidget(self.cfgCTRLERROR, 1, 1, 1, 1)
        self.vboxlayout2.addLayout(self.gridlayout2)
        self.vboxlayout.addWidget(self.groupBox_2)
        self.gridlayout.addWidget(self.closedloop_frame, 0, 0, 1, 1)

        self.retranslateUi(closedloop)
        QtCore.QMetaObject.connectSlotsByName(closedloop)

    def retranslateUi(self, closedloop):
        closedloop.setWindowTitle(QtGui.QApplication.translate("closedloop", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("closedloop", "Position closed loop", None, QtGui.QApplication.UnicodeUTF8))
        self.chkClosedLoop.setText(QtGui.QApplication.translate("closedloop", "Enable closed loop", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("closedloop", "Closed loop encoder", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("closedloop", "Time constant (s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("closedloop", "Maximum error (steps)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("closedloop", "Deadband (steps)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("closedloop", "Settle window (steps)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("closedloop", "Settle time (s)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("closedloop", "Position control", None, QtGui.QApplication.UnicodeUTF8))
        self.chkPositionControl.setText(QtGui.QApplication.translate("closedloop", "Enable position control", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("closedloop", "Control encoder", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("closedloop", "Maximum error (steps)", None, QtGui.QApplication.UnicodeUTF8))

