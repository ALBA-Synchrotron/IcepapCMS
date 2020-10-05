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


from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from ui_dialoghomesrch import Ui_DialogHomeSrch
#from ..lib_icepapcms import MainManager


class DialogHomeSrch(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.ui = Ui_DialogHomeSrch()
        self.ui.setupUi(self)
        self.parent = parent
        self.close_button = self.ui.bbClose.button(QDialogButtonBox.Close)
        self._connect_signals()

    def _connect_signals(self):
        self.close_button.clicked.connect(self._close_down)

    def _close_down(self):
        self.parent.enable_home_srch_button()
