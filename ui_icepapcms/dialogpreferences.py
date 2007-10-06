from PyQt4 import QtCore, QtGui
from ui_dialogpreferences import Ui_DialogPreferences
from lib_icepapcms import ConfigManager
from messagedialogs import MessageDialogs
from qrc_icepapcms import *
import sys

MYSQL_PORT =  3306
POSTGRES_PORT = 5432

class DialogPreferences(QtGui.QDialog):    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogPreferences()
        self.modal = True
        self.ui.setupUi(self)
        self.StorageChanged = False
        self.selectedDB = ""
        QtCore.QObject.connect(self.ui.listWidget,QtCore.SIGNAL("itemClicked(QListWidgetItem*)"),self.listWidget_on_click)
        QtCore.QObject.connect(self.ui.btnBrowser,QtCore.SIGNAL("clicked()"),self.btnBrowse_on_click)
        QtCore.QObject.connect(self.ui.closeButton,QtCore.SIGNAL("clicked()"),self.closeButton_on_click)
        QtCore.QObject.connect(self.ui.rbmysql,QtCore.SIGNAL("toggled(bool)"),self.rbMySql_toogled)
        QtCore.QObject.connect(self.ui.rbpostgres,QtCore.SIGNAL("toggled(bool)"),self.rbPostgres_toogled)
        QtCore.QObject.connect(self.ui.rbsqlite,QtCore.SIGNAL("toggled(bool)"),self.rbSqlite_toogled)
        self._config = ConfigManager()
        self.fillConfig()
        self.ui.listWidget.setItemSelected(self.ui.listWidget.item(0), True)
        """ check imports for dbs to disable errors """
    
    def closeButton_on_click(self):
        if self.checkPreferences():
            self._config.saveConfig()
            self.close()
        else:
            MessageDialogs.showWarningMessage(self, "Preferences", "Check configuration parameters")
    

    def listWidget_on_click(self, item):
        index = self.ui.listWidget.row(item)
        self.ui.stackedWidget.setCurrentIndex(index)
    
    def rbSqlite_toogled(self, checked):
        if checked:
            self.selectedDB = self._config.Sqlite
            self.ui.gbLocal.setEnabled(True)
            self.ui.gbRemote.setEnabled(False)

    def rbPostgres_toogled(self, checked):
        if checked:
            self.selectedDB = self._config.Postgres
            self.ui.gbLocal.setEnabled(False)
            self.ui.gbRemote.setEnabled(True)
            self.ui.txtPort.setText(str(POSTGRES_PORT))
    
    def rbMySql_toogled(self, checked):
        if checked:
            self.selectedDB = self._config.MySql
            self.ui.gbLocal.setEnabled(False)
            self.ui.gbRemote.setEnabled(True)
            self.ui.txtPort.setText(str(MYSQL_PORT))
    
    def btnBrowse_on_click(self):
        fn = QtGui.QFileDialog.getExistingDirectory(self)
        if fn.isEmpty():
            return
        folder = str(fn)
        self.ui.txtLocalFolder.setText(folder)
    
    def checkDbEngines(self):
        module_errors = ""
        ok_sqlite = True
        try:
            from pysqlite2 import dbapi2 as sqlite
        except ImportError:
            try:
                from sqlite3 import dbapi2 as sqlite
            except ImportError:
                ok_sqlite = False
                module_errors  = module_errors + "Failed to import Sqlite Modules: pysqlite2, sqlite3 modules\n"
        self.ui.rbsqlite.setEnabled(ok_sqlite)
        
        postgres = True
        try:
            import psycopg2
            import psycopg2.extensions
        except:
            postgres = False
            module_errors  = module_errors + "Failed to import Postgres modules:psycopg2\n"
        self.ui.rbpostgres.setEnabled(postgres)
        
        mysql = True
        try:
            import MySQLdb
            import MySQLdb.converters
        except:
            module_errors  = module_errors + "Failed to import MySQL modules: MySQLdb\n"
            mysql = False
        if module_errors != "":
            module_errors = module_errors + "Check IcepapCMS user manual to solve these issues"
        self.ui.lblModules.setText(module_errors)
        self.ui.rbmysql.setEnabled(mysql)
                
    def fillConfig(self):
        self.checkDbEngines()
        db = self._config.config[self._config.database]["database"]
        rb = getattr(self.ui, "rb"+db)
        rb.setChecked(True)
        self.ui.txtLocalFolder.setText(self._config.config[self._config.database]["folder"])
        server = self._config.config[self._config.database]["server"]
        server = server.split(':')
        self.ui.txtHost.setText(server[0])
        self.ui.txtPort.setText(server[1])
        user = self._config.config[self._config.database]["user"]
        pwd = self._config.config[self._config.database]["password"]
        self.ui.txtUser.setText(user)
        self.ui.txtPassword.setText(pwd)
    
    def checkPreferences(self):
        try:
            ''' Storage Configuration '''
            if not self._config.config[self._config.database]["database"] == str(self.selectedDB):
                self.StorageChanged = True
                self._config.config[self._config.database]["database"] = str(self.selectedDB)
                              
                
            if self.ui.rbsqlite.isChecked():
                local_folder = str(self.ui.txtLocalFolder.text())
                if not self._config.config[self._config.database]["folder"] == local_folder:
                    self._config.config[self._config.database]["folder"] = local_folder
                    self.StorageChanged = True
            else:
                host = str(self.ui.txtHost.text()).strip() 
                port = str(self.ui.txtPort.text()).strip()
                user = str(self.ui.txtUser.text()).strip()
                pwd = str(self.ui.txtPassword.text()).strip()
                iport = int(port)
                if host == "" or port == "":
                    return False
                remote_server = host + ":" + port
                if not self._config.config[self._config.database]["server"] == remote_server:
                    self.StorageChanged = True
                    self._config.config[self._config.database]["server"] = remote_server
                if user != self._config.config[self._config.database]["user"] or pwd != self._config.config[self._config.database]["password"]:
                    self.StorageChanged = True
                    self._config.config[self._config.database]["user"] = user
                    self._config.config[self._config.database]["password"] = pwd                         
            
            return True
        except:
            print "Unexpected error:", sys.exc_info()[1]
            return False
            
            
        
        
        