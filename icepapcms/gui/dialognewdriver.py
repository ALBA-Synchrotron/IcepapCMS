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


class DialogNewDriver(QtWidgets.QDialog):
    log = logging.getLogger('{}.DialogNewDriver'.format(__name__))

    @loggingInfo
    def __init__(self, parent, more_info, expertFlag):
        QtWidgets.QDialog.__init__(self, parent)
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'dialognewdriver.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)

        self.modal = True
        self.more_info = more_info
        self.expertFlag = expertFlag
        self.ui.btnCancel.setDefault(True)
        self.user_result = "CANCEL"

        if not expertFlag:
            self.ui.lblExpertInfo.setVisible(False)
            self.ui.btnUseDriver.setVisible(False)
        self.connectSignals()

    @loggingInfo
    def connectSignals(self):
        self.ui.btnUseDefaults.clicked.connect(self.btnUseDefaults_clicked)
        self.ui.btnUseDriver.clicked.connect(self.btnUseDriver_clicked)
        self.ui.btnCancel.clicked.connect(self.btnCancel_clicked)
        self.ui.btnMoreInfo.clicked.connect(self.btnMoreInfo_clicked)

    @loggingInfo
    def btnUseDefaults_clicked(self):
        self.user_result = "DEFAULT"
        self.accept()

    @loggingInfo
    def btnUseDriver_clicked(self):
        self.user_result = "DRIVER"
        self.accept()

    @loggingInfo
    def btnCancel_clicked(self):
        self.user_result = "CANCEL"
        self.reject()

    @loggingInfo
    def btnMoreInfo_clicked(self):
        self.more_info.show()

    @loggingInfo
    def result(self):
        return self.user_result


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    d = QtWidgets.QWidget()
    w = DialogNewDriver(None, d, expertFlag=True)
    w.show()
    sys.exit(app.exec_())
