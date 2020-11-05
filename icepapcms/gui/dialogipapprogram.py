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


from PyQt5 import QtWidgets, uic, Qt
from pkg_resources import resource_filename
import sys
import datetime
import logging
from icepap import IcePAPController
import threading
import queue
from .messagedialogs import MessageDialogs
from ..lib import IcepapsManager, ConfigManager
from ..helpers import loggingInfo


class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


class DialogIcepapProgram(QtWidgets.QDialog):
    log = logging.getLogger('{}.DialogIcepapProgram'.format(__name__))

    @loggingInfo
    def __init__(self, parent, test_mode=False):
        QtWidgets.QDialog.__init__(self, parent)
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'dialogipapprogram.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)

        self.timer = Qt.QTimer(self)
        self.ui.btnAbort.setStyleSheet('text-align:left;')

        # Signals
        self.ui.btnBrowser.clicked.connect(self.btnBrowse_on_click)
        self.ui.btnClose.clicked.connect(self.close)
        self.ui.btnTest.clicked.connect(self.btnTest_on_click)
        self.ui.btnProgram.clicked.connect(self.btnProgram_on_click)
        self.ui.cbProgram.currentTextChanged.connect(self.cbProgram_changed)
        self.ui.btnAbort.clicked.connect(self.abort_clicked)
        self.ui.btnSnapshot.clicked.connect(self.take_snapshot)
        self.timer.timeout.connect(self._check_queue)

        self.ui.sbAddr.setDisabled(True)
         # BY DEFAULT, PROGRAMM ALL INSTEAD OF NONE
        self.ui.cbProgram.setCurrentIndex(1)
        self.ui.expert.setChecked(False)
        if test_mode:
            return
        self._ipapctrl = IcepapsManager()
        self.log_queue = queue.Queue()
        self.programming = False
        self._btn_enables(True)
        self._thread = None
        self.flg_abort = False

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

    def closeEvent(self, event) -> None:
        if self.programming:
            self.abort_clicked()
            if self.programming:
                event.ignore()
        else:
            self.timer.stop()

    @loggingInfo
    def btnTest_on_click(self):
        host = self.ui.txtHost.text()
        if self._ipapctrl.testConnection(host, 5000):
            self.addToLog("Connection OK")
        else:
            self.addToLog("Connection error")
            MessageDialogs.showWarningMessage(
                self, "Connection error", "Icepap not reachable.")

    @loggingInfo
    def btnProgram_on_click(self):
        try:
            self.programming = True
            self._btn_enables(False)
            self.timer.start(2000)
            self._thread = thread_with_trace(target=self.startProgramming)
            self._thread.daemon = True
            self._thread.start()
        except Exception as e:
            self.addToLog(str(e))

    def _btn_enables(self, enabled):
        self.ui.btnProgram.setEnabled(enabled)
        self.ui.btnSnapshot.setEnabled(enabled)
        self.ui.btnTest.setEnabled(enabled)
        self.ui.btnBrowser.setEnabled(enabled)
        self.ui.txtHost.setEnabled(enabled)
        self.ui.txtFirmwareFile.setEnabled(enabled)
        self.ui.expert.setEnabled(enabled)
        self.ui.btnAbort.setEnabled(not enabled)

    def _check_queue(self):
        while not self.log_queue.empty():
            try:
                value = self.log_queue.get()
                self.addToLog(value)
            except queue.Empty:
                pass

        if not self.programming:
            while not self.log_queue.empty():
                try:
                    value = self.log_queue.get()
                    self.addToLog(value)
                except queue.Empty:
                    pass
            self.timer.stop()
            self._btn_enables(True)
            self._thread = None

    def take_snapshot(self):
        self.parent().actionSnapshot.trigger()

    def abort_clicked(self):
        if self._thread is None or not self.programming:
            return

        msg = Qt.QMessageBox(self)
        msg.setIcon(Qt.QMessageBox.Question)
        msg.setText('Are you sure to abort the programming?\n'
                    'It can leave the icepap in bad condition')
        msg.setWindowTitle("Warning")
        msg.addButton(Qt.QMessageBox.Yes)
        msg.addButton(Qt.QMessageBox.No)
        result = msg.exec_()
        if result == Qt.QMessageBox.Yes:
            self._thread.kill()
            self._thread.join()
            self.programming = False

    @loggingInfo
    def startProgramming(self):
        try:
            filename = self.ui.txtFirmwareFile.text()
            host = self.ui.txtHost.text()
            if host == '':
                MessageDialogs.showErrorMessage(
                    self, 'Empty hostname', 'You must enter a valid hostname')
                return
            port = 5000
            if self.ui.expert.isChecked():
                component = self.ui.cbProgram.currentText()
                if component == "ADDR":
                    addr = self.ui.sbAddr.value()
                    if addr not in IcePAPController.ALL_AXES_VALID:
                        MessageDialogs.showErrorMessage(self, 'Wrong Axis',
                                                        'Axis value not valid')
                    component = str(addr)

                options = self.ui.cbOptions.currentText()
                force = False
                if self.ui.chkForce.isChecked():
                    force = True
                self._ipapctrl.upgradeFirmware(host, port, filename, component,
                                               options, force, self.log_queue)
            else:
                self._ipapctrl.upgradeAutomaticFirmware(host, port, filename,
                                                        self.log_queue)
        except Exception as e:
            MessageDialogs.showErrorMessage(None, 'Error programming', str(e))
        finally:
            self.programming = False

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