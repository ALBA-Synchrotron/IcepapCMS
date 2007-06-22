from PyQt4 import QtCore, QtGui
from ui_dialogpreferences import Ui_DialogPreferences
from lib_icepapcms import ConfigManager
from messagedialogs import MessageDialogs


class DialogPreferences(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogPreferences()
        self.modal = True
        self.ui.setupUi(self)
        self.StorageChanged = False
        QtCore.QObject.connect(self.ui.listWidget,QtCore.SIGNAL("itemClicked(QListWidgetItem*)"),self.listWidget_on_click)
        QtCore.QObject.connect(self.ui.btnBrowser,QtCore.SIGNAL("clicked()"),self.btnBrowse_on_click)
        QtCore.QObject.connect(self.ui.closeButton,QtCore.SIGNAL("clicked()"),self.closeButton_on_click)
        QtCore.QObject.connect(self.ui.rbLocal,QtCore.SIGNAL("toggled(bool)"),self.rbLocal_toogled)
        QtCore.QObject.connect(self.ui.rbRemote,QtCore.SIGNAL("toggled(bool)"),self.rbLocal_toogled)
        self._config = ConfigManager()
        self.fillConfig()
    
    def closeButton_on_click(self):
        if self.checkPreferences():
            self._config.saveConfig()
            self.close()
        else:
            MessageDialogs.showWarningMessage(self, "Preferences", "Check configuration parameters")
    

    def listWidget_on_click(self, item):
        index = self.ui.listWidget.row(item)
        self.ui.stackedWidget.setCurrentIndex(index)
    
    def rbLocal_toogled(self, checked):
        if self.ui.rbLocal.isChecked():
            self.ui.gbLocal.setEnabled(True)
            self.ui.gbRemote.setEnabled(False)
        else:
            self.ui.gbLocal.setEnabled(False)
            self.ui.gbRemote.setEnabled(True)
    
    def btnBrowse_on_click(self):
        fn = QtGui.QFileDialog.getExistingDirectory(self)
        if fn.isEmpty():
            return
        folder = str(fn)
        self.ui.txtLocalFolder.setText(folder)
    
    def fillConfig(self):
        remote = self._config.config["zodb"]["remote_storage"] == str(True)
        self.ui.rbLocal.setChecked(not(remote))
        self.ui.rbRemote.setChecked(remote)
        self.ui.txtLocalFolder.setText(self._config.config["zodb"]["local_folder"])
        server = self._config.config["zodb"]["remote_server"]
        server = server.split(':')
        self.ui.txtHost.setText(server[0])
        self.ui.txtPort.setText(server[1])
    
    def checkPreferences(self):
        try:
            ''' Storage Configuration '''
            if not self._config.config["zodb"]["remote_storage"] == str(self.ui.rbRemote.isChecked()):
                self.StorageChanged = True
                self._config.config["zodb"]["remote_storage"] = str(self.ui.rbRemote.isChecked())
                remote = self._config.config["zodb"]["remote_storage"]
                
                
            if self.ui.rbRemote.isChecked():
                host = str(self.ui.txtHost.text()).strip() 
                port = str(self.ui.txtPort.text()).strip()
                iport = int(port)
                if host == "" or port == "":
                    return False
                remote_server = host + ":" + port
                if not self._config.config["zodb"]["remote_server"] == remote_server:
                    self.StorageChanged = True
                    self._config.config["zodb"]["remote_server"] = remote_server
            else:
                local_folder = str(self.ui.txtLocalFolder.text())
                if not self._config.config["zodb"]["local_folder"] == local_folder:
                    self._config.config["zodb"]["local_folder"] = local_folder
                    self.StorageChanged = True
            
            return True
        except:
            return False
            
            
        
        
        