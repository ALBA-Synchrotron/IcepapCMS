#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of icepapCMS https://github.com/ALBA-Synchrotron/icepapcms
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


from PyQt5 import QtWidgets, uic
from pkg_resources import resource_filename


class DialogNewDriver(QtWidgets.QDialog):
    def __init__(self, parent, more_info, expertFlag):
        QtWidgets.QDialog.__init__(self, parent)
        ui_filename = resource_filename('icepapCMS.ui_icepapcms.ui',
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

    def connectSignals(self):
        self.ui.btnUseDefaults.clicked.connect(self.btnUseDefaults_clicked)
        self.ui.btnUseDriver.clicked.connect(self.btnUseDriver_clicked)
        self.ui.btnCancel.clicked.connect(self.btnCancel_clicked)
        self.ui.btnMoreInfo.clicked.connect(self.btnMoreInfo_clicked)

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


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    d = QtWidgets.QWidget()
    w = DialogNewDriver(None, d, expertFlag=True)
    w.show()
    sys.exit(app.exec_())
