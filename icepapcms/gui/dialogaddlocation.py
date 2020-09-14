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


class DialogAddLocation(QtWidgets.QDialog):
    log = logging.getLogger('{}.DialogAddLocation'.format(__name__))

    @loggingInfo
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'dialogaddlocation.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)
        self.modal = True

    @loggingInfo
    def getData(self):
        name = str(self.ui.txtName.text())
        return name

    @loggingInfo
    def setData(self, name):
        self.ui.txtname.setText(name)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = DialogAddLocation(None)
    w.show()
    sys.exit(app.exec_())