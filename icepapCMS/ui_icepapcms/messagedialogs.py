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


from PyQt5 import QtWidgets


class MessageDialogs:

    def showYesNoMessage(self, parent, caption, question):
        return not QtWidgets.QMessageBox.question(parent, caption, question,
                                                  "Yes", "No")
    showYesNoMessage = classmethod(showYesNoMessage)

    def showWarningMessage(self, parent, caption, warning):
        QtWidgets.QMessageBox.warning(parent, caption, warning)
    showWarningMessage = classmethod(showWarningMessage)

    def showInformationMessage(self, parent, caption, info):
        QtWidgets.QMessageBox.information(parent, caption, info)
    showInformationMessage = classmethod(showInformationMessage)

    def showErrorMessage(self, parent, caption, error):
        QtWidgets.QMessageBox.critical(parent, caption, error)
    showErrorMessage = classmethod(showErrorMessage)
