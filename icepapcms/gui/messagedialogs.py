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


from PyQt5.QtWidgets import QMessageBox


class MessageDialogs:

    def showYesNoMessage(self, parent, caption, question):
        answer = QMessageBox.question(parent, caption, question,
                                      QMessageBox.Yes | QMessageBox.No,
                                      defaultButton=QMessageBox.No)
        return answer == QMessageBox.Yes
    showYesNoMessage = classmethod(showYesNoMessage)

    def showWarningMessage(self, parent, caption, warning):
        QMessageBox.warning(parent, caption, warning)
    showWarningMessage = classmethod(showWarningMessage)

    def showInformationMessage(self, parent, caption, info):
        QMessageBox.information(parent, caption, info)
    showInformationMessage = classmethod(showInformationMessage)

    def showErrorMessage(self, parent, caption, error):
        QMessageBox.critical(parent, caption, error)
    showErrorMessage = classmethod(showErrorMessage)


