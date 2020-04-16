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
from .ui_dialogaddlocation import Ui_DialogAddLocation
from .qrc_icepapcms import *


class DialogAddLocation(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogAddLocation()
        self.modal = True
        self.ui.setupUi(self)        

    def getData(self):
        name = str(self.ui.txtName.text())        
        return name
    def setData(self, name):
        self.ui.txtname.setText(name)
                