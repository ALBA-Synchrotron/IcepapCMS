#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of icepapcms https://github.com/ALBA-Synchrotron/icepapcms
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


from PyQt5 import QtWidgets, uic
from pkg_resources import resource_filename
import logging
from ..helpers import loggingInfo

class DialogConflictExpert(QtWidgets.QDialog):
    log = logging.getLogger('{}.DialogConflictExpert'.format(__name__))

    @loggingInfo
    def __init__(self, parent, more_info):
        QtWidgets.QDialog.__init__(self, parent)
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'dialogconflictdriver_expert.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)
        self.modal = True
        self.more_info = more_info
        self.ui.btnCancel.setDefault(True)

        self.connectSignals()

    @loggingInfo
    def connectSignals(self):
        self.ui.btnUpdate.clicked.connect(self.btnUpdate_clicked)
        self.ui.btnCancel.clicked.connect(self.btnCancel_clicked)
        self.ui.btnMoreInfo.clicked.connect(self.btnMoreInfo_clicked)

    @loggingInfo
    def btnUpdate_clicked(self):
        self.accept()

    @loggingInfo
    def btnCancel_clicked(self):
        self.reject()

    @loggingInfo
    def btnMoreInfo_clicked(self):
        self.more_info.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    d = QtWidgets.QWidget()
    w = DialogConflictExpert(None, d)
    w.show()
    sys.exit(app.exec_())