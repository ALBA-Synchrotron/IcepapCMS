#!/usr/bin/env python

# ------------------------------------------------------------------------------
# This file is part of icepapCMS (https://github.com/ALBA-Synchrotron/icepapcms)
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# ------------------------------------------------------------------------------


from PyQt4 import QtCore, QtGui
from .ui_dialognewdriver import Ui_DialogNewDriver
from ..lib_icepapcms import MainManager

class DialogNewDriver(QtGui.QDialog):
    def __init__(self, parent, more_info, expertFlag):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogNewDriver()
        self.modal = True
        self.ui.setupUi(self)
        self.more_info = more_info
        self.expertFlag = expertFlag
        self.ui.btnCancel.setDefault(True)
        self.user_result = "CANCEL"

        if not expertFlag:
            self.ui.lblExpertInfo.setVisible(False)
            self.ui.btnUseDriver.setVisible(False)
        self.connectSignals()


    def connectSignals(self):
        QtCore.QObject.connect(self.ui.btnUseDefaults,QtCore.SIGNAL("pressed()"),self.btnUseDefaults_clicked)
        QtCore.QObject.connect(self.ui.btnUseDriver,QtCore.SIGNAL("pressed()"),self.btnUseDriver_clicked)
        QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL("pressed()"),self.btnCancel_clicked)
        QtCore.QObject.connect(self.ui.btnMoreInfo,QtCore.SIGNAL("pressed()"),self.btnMoreInfo_clicked)


    def btnUseDefaults_clicked(self):
        self.user_result = "DEFAULT"
        self.accept()

    def btnUseDriver_clicked(self):
        self.user_result = "DRIVER"
        self.accept()

    def btnCancel_clicked(self):
        self.user_result = "CANCEL"
        self.reject()

    def btnMoreInfo_clicked(self):
        self.more_info.show()

    def result(self):
        return self.user_result
