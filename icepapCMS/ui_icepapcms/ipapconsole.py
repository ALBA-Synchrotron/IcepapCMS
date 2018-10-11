#!/usr/bin/env python

# ------------------------------------------------------------------------------
# This file is part of icepapCMS (https://github.com/ALBA-Synchrotron/icepapcms)
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# ------------------------------------------------------------------------------


from PyQt4 import QtCore, QtGui, Qt
from ui_ipapconsole import Ui_IpapConsole
from messagedialogs import MessageDialogs
from lib_icepapcms import ConfigManager, IcepapController
from pyIcePAP import EthIcePAPController
import sys
import os
from qrc_icepapcms import *


class IcepapConsole(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.Window)
        
        self.ui = Ui_IpapConsole()
        
        self.ui.setupUi(self)        
        self.ui.btnDisconnect.setDisabled(True)
        self.ui.console.setDisabled(True)
        QtCore.QObject.connect(self.ui.btnConnect, QtCore.SIGNAL("clicked()"), self.btn_connect_on_click)
        QtCore.QObject.connect(self.ui.btnDisconnect, QtCore.SIGNAL("clicked()"), self.btn_disconnect_on_click)
        QtCore.QObject.connect(self.ui.console, QtCore.SIGNAL("commandReceived(const QString &)"), self._execute_command)

        self.ipap = None
        self.prompt = "icepap:>"
        font = QtGui.QFont()
        font.setPointSize(8)
        self.setFont(font)
        self.ui.console.setPrompt(self.prompt)
        self.log_folder = None
        self._config = ConfigManager()
        try:
            self.debug = self._config.config[self._config.icepap]["debug_enabled"] == str(True)
            self.log_folder = self._config.config[self._config.icepap]["log_folder"]
            if not os.path.exists(self.log_folder):
                os.mkdir(self.log_folder)
        except Exception as e:
            msg = "icepapconsole_init():{}\n{}".format(sys.exc_info(), e)
            print(msg)

    def btn_connect_on_click(self):
        addr = str(self.ui.txtHost.text())
        try:
            if addr == '':
                MessageDialogs.showErrorMessage(None, 'Host connection', 'Please, write a host name to connect to.')
                return
            if addr.find(':') >= 0:
                str_list = addr.split(':')
                host = str_list[0]
                port = int(str_list[1])
            else:
                host = addr
                port = 5000

            if hasattr(self._config, '_options'):
                ipapcontroller = IcepapController()
                if not ipapcontroller.host_in_same_subnet(host):
                    msg = "It is not allowed to connect to {}".format(host)
                    MessageDialogs.showInformationMessage(None, "Host connection", msg)
                    return
            else:
                # JUST RUNNING AS A STAND-ALONE
                pass
            self.prompt = str(host) + " > "   
            self.ipap = EthIcePAPController(host, port)
            self.ui.btnDisconnect.setDisabled(False)
            self.ui.btnConnect.setDisabled(True)
            self.ui.console.setDisabled(False)
            self.ui.console.setFocus()
            self.ui.console.clear()
            self.write_console("Connected to Icepap :  " + addr)
            self.ui.console.setPrompt(self.prompt)
            self.write_prompt()
        except Exception, e:
            MessageDialogs.showErrorMessage(None, "Connection error", "Error connecting to " + addr + "\n" + str(e))

    def btn_disconnect_on_click(self):
        del self.ipap
        self.ipap = None
        self.ui.btnDisconnect.setDisabled(True)
        self.ui.btnConnect.setDisabled(False)
        self.ui.console.clear()
        self.ui.console.setDisabled(True)
        self.ui.txtHost.setFocus()

    def write_console(self, txt):
        self.ui.console.write(txt + "\n")
    
    def write_prompt(self):
        self.ui.console.write(self.prompt)
        
    def _execute_command(self, cmd):
        try:
            cmd = str(cmd)
            if len(cmd) == 0:
                return
            cmd = cmd.upper()
            if cmd == "QUIT" or cmd == "CLOSE" or cmd == "EXIT":
                self.btn_disconnect_on_click()
                self.close()
                return
            if cmd.find("?") >= 0 or cmd.find("#") >= 0:
                list = self.ipap.send_cmd(cmd)
                res = ''
                for i in list:
                    res += '{}\n'.format(i)
                self.write_console(res)
            else:
                self.ipap.send_cmd(cmd)
        except Exception as e:
            self.write_console("Some exception issuing command '%s'." % cmd)
            self.write_console("                 Error is: '%s'." % str(e))

    def closeEvent(self, event):
        self.btn_disconnect_on_click()
        event.accept()       
