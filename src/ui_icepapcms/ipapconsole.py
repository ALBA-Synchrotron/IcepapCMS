from PyQt4 import QtCore, QtGui, Qt
from ui_ipapconsole import Ui_IpapConsole
from messagedialogs import MessageDialogs
from lib_icepapcms import ConfigManager,IcepapController
from pyIcePAP import EthIcePAP, IcePAPException, IcePAP, IcepapStatus
import sys, os
from qrc_icepapcms import *


class IcepapConsole(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.Window)
        
        self.ui = Ui_IpapConsole()
        
        self.ui.setupUi(self)        
        self.ui.btnDisconnect.setDisabled(True)
        self.ui.console.setDisabled(True)
        QtCore.QObject.connect(self.ui.btnConnect,QtCore.SIGNAL("clicked()"),self.btnConnect_on_click)
        QtCore.QObject.connect(self.ui.btnDisconnect,QtCore.SIGNAL("clicked()"),self.btnDisconnect_on_click)
        QtCore.QObject.connect(self.ui.console,QtCore.SIGNAL("commandReceived(const QString &)"),self.sendWriteReadCommand)

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
        except:
            print "icepapconsole_init():", sys.exc_info()
        
    def btnConnect_on_click(self):
        try:
            addr = str(self.ui.txtHost.text())
            if addr == '':
                MessageDialogs.showErrorMessage(None,'Host connection','Please, write a host name to connect to.')
                return
            if addr.find(":") >= 0:
                aux = addr.split(':')
                host = aux[0]
                port = aux[1]
            else:
                host = addr
                port = "5000"

            if hasattr(self._config,'_options'):
                ipapcontroller = IcepapController()
                if not ipapcontroller.host_in_same_subnet(host):
                    MessageDialogs.showInformationMessage(None,"Host connection","It is not allowed to connect to %s"%host)
                    return
            else:
                # JUST RUNNING AS A STAND-ALONE
                pass
            self.prompt = str(host) + " > "   
            log_folder = None
            if self.debug:
                log_folder = self.log_folder
            self.ipap = EthIcePAP(host , port, log_path = log_folder)
            self.ipap.connect()
            #try:
            #    rsp = self.ipap.sendWriteReadCommand("?_help")
            #    self.writeConsole(rsp)
            #except:
            #    MessageDialogs.showWarningMessage(None,"Command error", "The ?_help command is not supported at "+addr)
            self.ui.btnDisconnect.setDisabled(False)
            self.ui.btnConnect.setDisabled(True)
            self.ui.console.setDisabled(False)
            self.ui.console.setFocus()
            self.ui.console.clear()
            self.writeConsole("Connected to Icepap :  " + addr)
            self.ui.console.setPrompt(self.prompt)
            self.writePrompt()
        except Exception,e:
            MessageDialogs.showErrorMessage(None, "Connection error", "Error connecting to " + addr+"\n"+str(e))
            
    
    def btnDisconnect_on_click(self):
        try:
            self.ipap.disconnect()
        except:
            pass
        self.ui.btnDisconnect.setDisabled(True)
        self.ui.btnConnect.setDisabled(False)
        self.ui.console.clear()
        self.ui.console.setDisabled(True)
        self.ui.txtHost.setFocus()
        
    def writeConsole(self,txt):
        self.ui.console.write(txt+"\n")
    
    def writePrompt(self):
        self.ui.console.write(self.prompt)
        
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
            if cmd.find("?") >= 0 or cmd.find("#")>= 0:
                res = self.ipap.sendWriteReadCommand(cmd)
                self.writeConsole(res)
            elif cmd.find("HELP")>=0:
                res = self.ipap.sendWriteReadCommand(cmd)
                self.writeConsole(res)
            else:
                self.ipap.sendWriteCommand(cmd)
        except Exception,e:
            self.writeConsole("Some exception issuing command '%s'." % cmd)
            self.writeConsole("                 Error is: '%s'." % str(e))

    
    def closeEvent(self, event):
        self.btnDisconnect_on_click()
        event.accept()       
