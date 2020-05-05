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
import datetime
import logging
# TODO use threading
import _thread
from .messagedialogs import MessageDialogs
from ..lib_icepapcms import IcepapController, ConfigManager
from ..helpers import loggingInfo


class DialogIcepapProgram(QtWidgets.QDialog):
    log = logging.getLogger('{}.DialogIcepapProgram'.format(__name__))

    @loggingInfo
    def __init__(self, parent, test_mode=False):
        QtWidgets.QDialog.__init__(self, parent)
        ui_filename = resource_filename('icepapCMS.ui_icepapcms.ui',
                                        'dialogipapprogram.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)

        # Signals
        self.ui.btnBrowser.clicked.connect(self.btnBrowse_on_click)
        self.ui.btnClose.clicked.connect(self.btnClose_on_click)
        self.ui.btnTest.clicked.connect(self.btnTest_on_click)
        self.ui.btnProgram.clicked.connect(self.btnProgram_on_click)
        self.ui.cbProgram.currentIndexChanged.connect(self.cbProgram_changed)
        self.ui.rbSerial.toggled.connect(self.rbSerial_toogled)
        self.ui.rbEth.toggled.connect(self.rbEth_toogled)

        self.ui.sbAddr.setDisabled(True)
        self.ui.rbEth.setChecked(True)
        # BY DEFAULT, PROGRAMM ALL INSTEAD OF NONE
        self.ui.cbProgram.setCurrentIndex(1)

        if test_mode:
            return
        self._ipapctrl = IcepapController()
        self.ui.cbSerial.addItems(self._ipapctrl.getSerialPorts())

    @loggingInfo
    def btnBrowse_on_click(self):
        folder = ConfigManager().config["icepap"]["firmware_folder"]
        fn = QtWidgets.QFileDialog.getOpenFileName(self, "Open Firmware File",
            str(folder), str("*.*"))
        if fn[0] == '':
            return
        filename = str(fn[0])
        self.ui.txtFirmwareFile.setText(filename)

    @loggingInfo
    def cbProgram_changed(self, text):
        if text == "ADDR":
            self.ui.sbAddr.setEnabled(True)
        else:
            self.ui.sbAddr.setDisabled(True)

    @loggingInfo
    def rbEth_toogled(self, state):
        self.ui.txtHost.setEnabled(state)
        self.ui.cbSerial.setEnabled(not state)

    @loggingInfo
    def rbSerial_toogled(self, state):
        self.ui.cbSerial.setEnabled(state)
        self.ui.txtHost.setEnabled(not state)

    @loggingInfo
    def btnClose_on_click(self):
        self.close()

    @loggingInfo
    def btnTest_on_click(self):
        serial = self.ui.rbSerial.isChecked()
        dst = str(self.ui.txtHost.text())
        if serial:
            dst = self.ui.cbSerial.currentText()
        if self._ipapctrl.testConnection(serial, dst):
            self.addToLog("Connection OK")
        else:
            self.addToLog("Connection error")
            MessageDialogs.showWarningMessage(
                self, "Connection error", "Icepap not reachable.")

    @loggingInfo
    def btnProgram_on_click(self):
        try:
            _thread.start_new_thread(self.startProgramming, ())
        except BaseException:
            self.addToLog(str(sys.exc_info()[0]))

    @loggingInfo
    def startProgramming(self):
        filename = str(self.ui.txtFirmwareFile.text())
        serial = self.ui.rbSerial.isChecked()
        dst = str(self.ui.txtHost.text())
        if serial:
            dst = self.ui.cbSerial.currentText()
        addr = self.ui.cbProgram.currentText()
        if addr == "ADDR":
            addr = str(self.ui.sbAddr.value())
        options = self.ui.cbOptions.currentText()

        if self.ui.chkForce.isChecked():
            options = options + " FORCE"
        self._ipapctrl.upgradeFirmware(
            serial, dst, filename, addr, options, self)

    @loggingInfo
    def addToLog(self, text):
        t = datetime.datetime.now().strftime("%H:%M:%S")
        self.ui.txtLog.append(t + "> " + text)
        self.ui.txtLog.ensureCursorVisible()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = DialogIcepapProgram(None, True)
    w.show()
    sys.exit(app.exec_())