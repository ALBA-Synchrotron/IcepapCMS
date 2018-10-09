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
from ui_dialogconflictdriver_expert import Ui_DialogConflictExpert
from lib_icepapcms import MainManager

class DialogConflictExpert(QtGui.QDialog):
    def __init__(self, parent, more_info):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogConflictExpert()
        self.modal = True
        self.ui.setupUi(self)
        self.more_info = more_info
        self.ui.btnCancel.setDefault(True)

        self.connectSignals()


    def connectSignals(self):
        QtCore.QObject.connect(self.ui.btnUpdate,QtCore.SIGNAL("pressed()"),self.btnUpdate_clicked)
        QtCore.QObject.connect(self.ui.btnCancel,QtCore.SIGNAL("pressed()"),self.btnCancel_clicked)
        QtCore.QObject.connect(self.ui.btnMoreInfo,QtCore.SIGNAL("pressed()"),self.btnMoreInfo_clicked)


    def btnUpdate_clicked(self):
        self.accept()

    def btnCancel_clicked(self):
        self.reject()

    def btnMoreInfo_clicked(self):
        self.more_info.show()
