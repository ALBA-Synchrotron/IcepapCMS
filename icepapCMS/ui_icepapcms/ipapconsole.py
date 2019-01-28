#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of icepapCMS
# (https://github.com/ALBA-Synchrotron/icepapcms)
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


from PyQt4 import QtGui, QtCore
from ui_ipapconsole import Ui_IpapConsole
from messagedialogs import MessageDialogs
from ..lib_icepapcms import ConfigManager, IcepapController
from pyIcePAP import EthIcePAPController
import sys
import os


class IcepapConsole(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.Window)

        self.ui = Ui_IpapConsole()

        self.ui.setupUi(self)
        self.ui.btnDisconnect.setDisabled(True)
        self.ui.console.setDisabled(True)
        QtCore.QObject.connect(self.ui.btnConnect,
                               QtCore.SIGNAL("clicked()"),
                               self.btnConnect_on_click)
        QtCore.QObject.connect(self.ui.btnDisconnect,
                               QtCore.SIGNAL("clicked()"),
                               self.btnDisconnect_on_click)
        QtCore.QObject.connect(self.ui.console,
                               QtCore.SIGNAL("commandReceived(const "
                                             "QString &)"),
                               self.send_command)

        self.ipap = None
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
        except Exception:
            print "icepapconsole_init():", sys.exc_info()

    def btnConnect_on_click(self):
        addr = str(self.ui.txtHost.text())
        try:
            if addr == '':
                MessageDialogs.showErrorMessage(None, 'Host connection',
                                                'Please, write a host '
                                                'name to connect to.')
                return
            if addr.find(":") >= 0:
                aux = addr.split(':')
                host = aux[0]
                port = int(aux[1])
            else:
                host = addr
                port = 5000

            if hasattr(self._config, '_options'):
                ipapcontroller = IcepapController()
                if not ipapcontroller.host_in_same_subnet(host):
                    MessageDialogs.showInformationMessage(None,
                                                          "Host connection",
                                                          "It is not allowed "
                                                          "to connect to %s. "
                                                          "(Check "
                                                          "subnet)" % host)
                    return
            else:
                # JUST RUNNING AS A STAND-ALONE
                pass
            self.prompt = str(host) + " > "

            try:
                self.ipap = EthIcePAPController(host, port, timeout=3)
            except Exception as e:
                msg = 'Failed to instantiate master controller.\nHost: ' \
                      '{}\nPort: {}\n{}'.format(host, port, e)
                raise Exception(msg)
            if not self.ipap:
                msg = 'IcePAP system {} has no active drivers! ' \
                      'Aborting.'.format(host)
                raise Exception(msg)

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

    def writeConsole(self, txt):
        self.ui.console.write(txt + "\n")

    def writePrompt(self):
        self.ui.console.write(self.prompt)

    def send_command(self, cmd):
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
            if cmd.find("?") >= 0 or cmd.find("#") >= 0:
                res = self.ipap.send_cmd(cmd)
                for r in res:
                    self.writeConsole(r)
            else:
                self.ipap.send_cmd(cmd)
        except Exception as e:
            self.writeConsole("Some exception issuing command '%s'." % cmd)
            self.writeConsole("                 Error is: '%s'." % str(e))

    def closeEvent(self, event):
        self.btnDisconnect_on_click()
        event.accept()
