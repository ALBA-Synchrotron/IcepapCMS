from PyQt4 import QtCore, QtGui
from ui_ipapconsole import Ui_IpapConsole
from messagedialogs import MessageDialogs
from lib_icepapcms import EthIcePAP, IcePAPException, IcePAP, IcepapStatus
import sys
from qrc_icepapcms import *




class IcepapConsole(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_IpapConsole()
        self.ui.setupUi(self)        
        self.ui.btnDisconnect.setDisabled(True)
        self.ui.console.setDisabled(True)
        QtCore.QObject.connect(self.ui.btnConnect,QtCore.SIGNAL("clicked()"),self.btnConnect_on_click)
        QtCore.QObject.connect(self.ui.btnDisconnect,QtCore.SIGNAL("clicked()"),self.btnDisconnect_on_click)
        QtCore.QObject.connect(self.ui.console,QtCore.SIGNAL("commandReceived(const QString &)"),self.sendWriteReadCommand)
        self.prompt = "icepap >"
        self.ui.console.setPrompt(self.prompt)
        
    def btnConnect_on_click(self):
        try:
            addr = str(self.ui.txtHost.text())
            if addr.find(":") >= 0:
                aux = addr.split(':')
                host = aux[0]
                port = aux[1]
            else:
                host = addr
                port = "5000"
                
            self.ipap = EthIcePAP(host , port)
            self.ipap.connect()
            self.ui.console.clear()
            self.writeConsole("Connected to Icepap :  " + addr)
            rsp = self.ipap.sendWriteReadCommand("help")
            self.writeConsole(rsp)
            rsp = self.ipap.sendWriteReadCommand( "sockhelp")
            self.writeConsole(rsp)
            self.ui.btnDisconnect.setDisabled(False)
            self.ui.btnConnect.setDisabled(True)
            self.ui.console.setDisabled(False)
            self.writePrompt()
            self.ui.console.setFocus()
        except:
            MessageDialogs.showErrorMessage(None, "Connection error", "Error connecting to " + addr)
            
    
    def btnDisconnect_on_click(self):
        try:
            self.ipap.disconnect()
        except:
            pass
        self.ui.btnDisconnect.setDisabled(True)
        self.ui.btnConnect.setDisabled(False)
        self.ui.console.setDisabled(True)
        self.ui.txtHost.setFocus()
        
    def writeConsole(self,txt):
        self.ui.console.write(txt+"\n")
    
    def writePrompt(self):
        self.ui.console.write(self.prompt)
        
    def sendWriteReadCommand(self, cmd):
        cmd = str(cmd)
        # determine if the command has an answer
        cmd = cmd.upper()
        if cmd == "QUIT" or cmd == "CLOSE" or cmd == "EXIT":
            self.btnDisconnect_on_click()
            self.close()
            return
        if cmd.find("?") >= 0 or cmd.find("#")>= 0:
            res = self.ipap.sendWriteReadCommand(cmd)
            self.writeConsole(res)
        elif cmd.find("HELP")>=0:
            res = self.ipap.sendWriteReadCommand(cmd)
            self.writeConsole(res)
        else:
             res = self.ipap.sendWriteCommand(cmd)

    
    def closeEvent(self, event):
        self.btnDisconnect_on_click()
        event.accept()
        
        
        
