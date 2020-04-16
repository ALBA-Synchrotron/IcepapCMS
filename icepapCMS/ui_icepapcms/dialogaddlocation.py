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


class DialogAddLocation(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        ui_filename = resource_filename('icepapCMS.ui_icepapcms.ui',
                                        'dialogaddlocation.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)
        self.modal = True

    def getData(self):
        name = str(self.ui.txtName.text())
        return name

    def setData(self, name):
        self.ui.txtname.setText(name)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = DialogAddLocation(None)
    w.show()
    sys.exit(app.exec_())