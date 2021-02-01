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


from PyQt5 import QtCore, QtWidgets, uic
from pkg_resources import resource_filename
import logging
from ..lib import MainManager
from ..helpers import loggingInfo


class DialogAddIcepap(QtWidgets.QDialog):
    log = logging.getLogger('{}.DialogAddIcepap'.format(__name__))

    @loggingInfo
    def __init__(self, parent, location, test_mode=False):
        QtWidgets.QDialog.__init__(self, parent)
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'dialogaddicepap.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)

        self.modal = True
        self.ui.txtPort.setText("5000")
        if test_mode:
            return
        self.buildLocationCombo(location)

    @loggingInfo
    def buildLocationCombo(self, location):
        for location_name in list(MainManager().locationList.keys()):
            self.ui.cbLocation.addItem(location_name)
        self.ui.cbLocation.setCurrentIndex(
            self.ui.cbLocation.findText(location, QtCore.Qt.MatchFixedString))

    @loggingInfo
    def getData(self):
        host = str(self.ui.txtHost.text())
        port = str(self.ui.txtPort.text())
        desc = str(self.ui.txtDescription.toPlainText())
        location = str(self.ui.cbLocation.currentText())
        return [host, port, desc, location]

    @loggingInfo
    def setData(self, name, host, port, description, location):
        self.ui.txtHost.setEnabled(False)
        self.ui.txtPort.setEnabled(False)
        self.ui.txtHost.setText(host)
        self.ui.txtPort.setText(str(port))
        self.ui.txtDescription.insertPlainText(description)
        self.ui.cbLocation.setCurrentIndex(
            self.ui.cbLocation.findText(location, QtCore.Qt.MatchFixedString))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = DialogAddIcepap(None, 'test', True)
    w.show()
    sys.exit(app.exec_())