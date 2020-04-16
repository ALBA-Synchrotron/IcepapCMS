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


from PyQt4 import QtCore, QtGui
from .ui_dialogipapprogram import Ui_DialogIcepapProgram
from .messagedialogs import MessageDialogs
from ..lib_icepapcms import IcepapController,ConfigManager
import sys
from qrc_icepapcms import *
import time
import datetime
# TODO use threading
import _thread



class DialogIcepapProgram(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogIcepapProgram()
        self.ui.setupUi(self)        
        QtCore.QObject.connect(self.ui.btnBrowser,QtCore.SIGNAL("clicked()"),self.btnBrowse_on_click)
        QtCore.QObject.connect(self.ui.btnClose,QtCore.SIGNAL("clicked()"),self.btnClose_on_click)
        QtCore.QObject.connect(self.ui.btnTest,QtCore.SIGNAL("clicked()"),self.btnTest_on_click)
        QtCore.QObject.connect(self.ui.btnProgram,QtCore.SIGNAL("clicked()"),self.btnProgram_on_click)
        QtCore.QObject.connect(self.ui.cbProgram,QtCore.SIGNAL("currentIndexChanged(QString)"),self.cbProgram_changed)
        QtCore.QObject.connect(self.ui.rbSerial,QtCore.SIGNAL("toggled(bool)"),self.rbSerial_toogled)
        QtCore.QObject.connect(self.ui.rbEth,QtCore.SIGNAL("toggled(bool)"),self.rbEth_toogled)
        self.ui.sbAddr.setDisabled(True)
        self._ipapctrl = IcepapController() 
        self.ui.cbSerial.addItems(self._ipapctrl.getSerialPorts())
        self.ui.rbEth.setChecked(True)

        # BY DEFAULT, PROGRAMM ALL INSTEAD OF NONE
        self.ui.cbProgram.setCurrentIndex(1)
        
        
    def btnBrowse_on_click(self):
        folder = ConfigManager().config["icepap"]["firmware_folder"]
        fn = QtGui.QFileDialog.getOpenFileName(self,"Open Firmware File",QtCore.QString(folder),QtCore.QString("*.*"))
        if fn.isEmpty():
            return
        filename = str(fn)
        self.ui.txtFirmwareFile.setText(filename)
    
    def cbProgram_changed(self, text):
        if text == "ADDR":
            self.ui.sbAddr.setEnabled(True)
        else:
            self.ui.sbAddr.setDisabled(True)
    
    def rbEth_toogled(self, state):
        self.ui.txtHost.setEnabled(state)
        self.ui.cbSerial.setEnabled(not state)
    
    def rbSerial_toogled(self, state):
        self.ui.cbSerial.setEnabled(state)
        self.ui.txtHost.setEnabled(not state)
        
    def btnClose_on_click(self):
        self.close()
    
    def btnTest_on_click(self):
        serial = self.ui.rbSerial.isChecked()
        dst = str(self.ui.txtHost.text())
        if serial :
            dst = self.ui.cbSerial.currentText()
        if self._ipapctrl.testConnection(serial, dst):
            self.addToLog("Connection OK")
        else:
            self.addToLog("Connection error")
            MessageDialogs.showWarningMessage(self, "Connection error" , "Icepap not reachable.")
    
    def btnProgram_on_click(self):
        try:
            _thread.start_new_thread(self.startProgramming, ())
        except:
            self.addToLog(str(sys.exc_info()[0]))
    
    def startProgramming(self):
        filename = str(self.ui.txtFirmwareFile.text())
        serial = self.ui.rbSerial.isChecked()
        dst = str(self.ui.txtHost.text())
        if serial :
            dst = self.ui.cbSerial.currentText()
        addr = self.ui.cbProgram.currentText()
        if addr == "ADDR":
            addr = str(self.ui.sbAddr.value())
        options = self.ui.cbOptions.currentText()
        
        if self.ui.chkForce.isChecked():
            options = options + " FORCE"
        self._ipapctrl.upgradeFirmware(serial, dst, filename, addr, options, self)
        
    def addToLog(self, text):    
        t = datetime.datetime.now().strftime("%H:%M:%S")
        self.ui.txtLog.append(t+"> "+text)
        self.ui.txtLog.ensureCursorVisible()
