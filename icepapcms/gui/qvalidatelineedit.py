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


from PyQt5 import QtGui, QtWidgets
import logging
from ..helpers import loggingInfo


class QValidateLineEdit(QtWidgets.QLineEdit):
    INTEGER, DOUBLE = list(range(2))
    log = logging.getLogger('{}.QValidateLineEdit'.format(__name__))

    @loggingInfo
    def __init__(self, parent, type, min, max):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.type = type
        if type == QValidateLineEdit.INTEGER:
            self.myValidator = QtGui.QIntValidator(int(min),
                                                   int(max), self)
        elif type == QValidateLineEdit.DOUBLE:
            self.myValidator = QtGui.QDoubleValidator(float(min),
                                                      float(max), 2, self)
        else:
            self.myValidator = None

    @loggingInfo
    def keyPressEvent(self, event):
        QtWidgets.QLineEdit.keyPressEvent(self, event)
        self.setValidator(self.myValidator)
        if self.validator() != 0:
            palette = self.palette()
            if not self.hasAcceptableInput():
                palette.setColor(QtGui.QPalette.Text, QtGui.QColor('red'))
                self.setPalette(palette)
            else:
                palette.setColor(QtGui.QPalette.Text, QtGui.QColor('black'))
                self.setPalette(palette)
        self.setValidator(None)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    m = QtWidgets.QWidget()
    w = QValidateLineEdit(m, QValidateLineEdit.INTEGER, -10, 10)
    m.show()
    sys.exit(app.exec_())