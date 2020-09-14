#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of icepapcms
# (https://github.com/ALBA-Synchrotron/icepapcms)
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


from PyQt5 import QtGui, QtCore, QtWidgets, uic
from pkg_resources import resource_filename
from icepap import IcePAPController
import os
import logging
from .messagedialogs import MessageDialogs
from ..lib import ConfigManager, IcepapsManager
from ..helpers import loggingInfo


class IcepapConsole(QtWidgets.QDialog):
    log = logging.getLogger('{}.IcepapConsole'.format(__name__))

    @loggingInfo
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent, QtCore.Qt.Window)
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'ipapconsole.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui,
                   package='icepapcms.gui')
        self.ui.btnDisconnect.setDisabled(True)
        self.ui.console.setDisabled(True)

        # Connect Signals
        self.ui.btnConnect.clicked.connect(self.btnConnect_on_click)
        self.ui.btnDisconnect.clicked.connect(self.btnDisconnect_on_click)
        self.ui.console.commandReceived.connect(self.sendWriteReadCommand)

        self.prompt = "icepap:>"
        font = QtGui.QFont()
        font.setPointSize(8)
        self.setFont(font)
        self.ui.console.setPrompt(self.prompt)
        self.log_folder = None
        self._config = ConfigManager()
        try:
            ipap_cfg = self._config.config[self._config.icepap]
            self.debug = ipap_cfg["debug_enabled"] == str(True)
            self.log_folder = ipap_cfg["log_folder"]
            if not os.path.exists(self.log_folder):
                os.mkdir(self.log_folder)
        except Exception as e:
            self.log.error("icepapconsole_init(): %s", e)

    @loggingInfo
    def btnConnect_on_click(self):
        try:
            addr = str(self.ui.txtHost.text())
            if addr == '':
                MessageDialogs.showErrorMessage(None, 'Host connection',
                                                'Please, write a host '
                                                'name to connect to.')
                return
            if addr.find(":") >= 0:
                aux = addr.split(':')
                host = aux[0]
                port = aux[1]
            else:
                host = addr
                port = "5000"

            if hasattr(self._config, '_options'):
                ipapcontroller = IcepapsManager()
                if not ipapcontroller.host_in_same_subnet(host):
                    MessageDialogs.showInformationMessage(
                        None, "Host connection",
                        "It is not allowed to connect to {}. "
                        "(Check subnet)".format(host))
                    return
            else:
                # JUST RUNNING AS A STAND-ALONE
                pass
            self.prompt = str(host) + " > "
            log_folder = None
            if self.debug:
                log_folder = self.log_folder
            # TODO configure debug folder and level
            self.ipap = IcePAPController(host, int(port))

            self.ui.btnDisconnect.setDisabled(False)
            self.ui.btnConnect.setDisabled(True)
            self.ui.console.setDisabled(False)
            self.ui.console.setFocus()
            self.ui.console.clear()
            self.writeConsole("Connected to Icepap :  " + addr)
            self.ui.console.setPrompt(self.prompt)
            self.writePrompt()
        except Exception as e:
            MessageDialogs.showErrorMessage(None, "Connection error",
                                            "Error connecting "
                                            "to " + addr + "\n" + str(e))

    @loggingInfo
    def btnDisconnect_on_click(self):
        try:
            self.ipap.disconnect()
        except Exception:
            pass
        self.ui.btnDisconnect.setDisabled(True)
        self.ui.btnConnect.setDisabled(False)
        self.ui.console.clear()
        self.ui.console.setDisabled(True)
        self.ui.txtHost.setFocus()

    @loggingInfo
    def writeConsole(self, txt):
        self.ui.console.write(txt + "\n")

    @loggingInfo
    def writePrompt(self):
        self.ui.console.write(self.prompt)

    @loggingInfo
    def sendWriteReadCommand(self, cmd):
        try:
            cmd = str(cmd)
            # determine if the command has an answer
            if len(cmd) == 0:
                # DO NOTHING...
                return
            cmd = cmd.upper()
            if cmd == "QUIT" or cmd == "CLOSE" or cmd == "EXIT":
                self.btnDisconnect_on_click()
                self.close()
                return
            answer = self.ipap.send_cmd(cmd)
            self.log.debug('cmd: %s, answer: %s', cmd, answer)
            if answer is None:
                return
            else:
                res = '\n'.join(answer)
                self.writeConsole(res)

        except Exception as e:
            self.writeConsole("Some exception issuing command "
                              "'{}'.".format(cmd))
            self.writeConsole("               Error is: '{}'.".format(str(e)))

    @loggingInfo
    def closeEvent(self, event):
        self.btnDisconnect_on_click()
        event.accept()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    console = IcepapConsole(None)
    console.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
