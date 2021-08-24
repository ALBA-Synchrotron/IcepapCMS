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


from PyQt5 import QtWidgets, uic
from pkg_resources import resource_filename
import logging
from ..lib import ConfigManager
from .messagedialogs import MessageDialogs
from ..helpers import loggingInfo
import os

# TODO Change to properties
MYSQL_PORT = 3306
POSTGRES_PORT = 5432


# TODO: Change Debug Level widget to use more levels
class DialogPreferences(QtWidgets.QDialog):
    log = logging.getLogger('{}.DialogPreferences'.format(__name__))

    @loggingInfo
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)

        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'dialogpreferences.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)
        self.modal = True
        self.StorageChanged = False
        self.selectedDB = ""

        # Connect Signals
        self.ui.listWidget.itemClicked.connect(self.listWidget_on_click)
        self.ui.btnBrowser.clicked.connect(self.btnBrowse_on_click)
        self.ui.btnLogBrowser.clicked.connect(self.btnLogBrowse_on_click)
        self.ui.btnFirmwareBrowser.clicked.connect(
            self.btnFirmwareBrowse_on_click)
        self.ui.btnTemplatesBrowser.clicked.connect(
            self.btnTemplatesBrowse_on_click)
        self.ui.closeButton.clicked.connect(self.closeButton_on_click)
        self.ui.rbmysql.toggled.connect(self.rbMySql_toogled)
        self.ui.rbpostgres.toggled.connect(self.rbPostgres_toogled)
        self.ui.rbsqlite.toggled.connect(self.rbSqlite_toogled)
        self.ui.btnSnapshotsBrowser.clicked.connect(self.snapshots_browser)

        self._config = ConfigManager()
        self.fillConfig()
        self.ui.listWidget.item(0).setSelected(True)
        """ check imports for dbs to disable errors """

    @loggingInfo
    def closeButton_on_click(self):
        if not os.path.exists(self._config.config_filename):
            if os.access(self._config.configs_folder, os.W_OK):
                print("Creating new config file:", self._config.config_filename)
                open(self._config.config_filename, 'a').close()
        if os.access(self._config.config_filename, os.W_OK):
            if self.checkPreferences():
                print("Writing config to:", self._config.config_filename)
                self._config.saveConfig()
                self.close()
            else:
                MessageDialogs.showWarningMessage(self, "Preferences", 
                    "Check configuration parameters")
        else:
            MessageDialogs.showWarningMessage(self, "Preferences", 
                "You must run IcePAPCMS as superuser to change"
                " the configuration parameters.")

    @loggingInfo
    def listWidget_on_click(self, item):
        index = self.ui.listWidget.row(item)
        self.ui.stackedWidget.setCurrentIndex(index)

    @loggingInfo
    def rbSqlite_toogled(self, checked):
        if checked:
            self.selectedDB = self._config.Sqlite
            self.ui.gbLocal.setEnabled(True)
            self.ui.gbRemote.setEnabled(False)

    @loggingInfo
    def rbPostgres_toogled(self, checked):
        if checked:
            self.selectedDB = self._config.Postgres
            self.ui.gbLocal.setEnabled(False)
            self.ui.gbRemote.setEnabled(True)
            self.ui.txtPort.setText(str(POSTGRES_PORT))

    @loggingInfo
    def rbMySql_toogled(self, checked):
        if checked:
            self.selectedDB = self._config.MySql
            self.ui.gbLocal.setEnabled(False)
            self.ui.gbRemote.setEnabled(True)
            self.ui.txtPort.setText(str(MYSQL_PORT))

    @loggingInfo
    def btnBrowse_on_click(self):
        current_folder = self._config.config[self._config.database]["folder"]
        fn = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open Folder", current_folder)
        if fn == '':
            return
        folder = str(fn)
        self.ui.txtLocalFolder.setText(folder)

    @loggingInfo
    def btnLogBrowse_on_click(self):
        current_folder = self._config.config[self._config.icepap]["log_folder"]
        fn = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open Log Folder", current_folder)
        if fn == '':
            return
        folder = str(fn)
        self.ui.txtLogFolder.setText(folder)

    @loggingInfo
    def btnFirmwareBrowse_on_click(self):
        current_folder = \
            self._config.config[self._config.icepap]["firmware_folder"]
        fn = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open Firmware Folder", current_folder)
        if fn == '':
            return
        folder = str(fn)
        self.ui.txtFirmwareFolder.setText(folder)

    @loggingInfo
    def btnTemplatesBrowse_on_click(self):
        current_folder = \
            self._config.config[self._config.icepap]["templates_folder"]
        fn = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open Templates Folder", current_folder)
        if fn == '':
            return
        folder = str(fn)
        self.ui.txtTemplatesFolder.setText(folder)

    def snapshots_browser(self):
        current_folder = \
            self._config.config[self._config.icepap]["snapshots_folder"]
        fn = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open Snapshots Folder", current_folder)
        if fn == '':
            return
        folder = str(fn)
        self.ui.txtSnapshotsFolder.setText(folder)

    @loggingInfo
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
                module_errors = module_errors + \
                    "Sqlite storage not available, requires one of the modules 'pysqlite2' or 'sqlite3'\n"
        self.ui.rbsqlite.setEnabled(ok_sqlite)

        postgres = True
        try:
            import psycopg2
            import psycopg2.extensions
        except BaseException:
            postgres = False
            module_errors += "Postgres storage not available, requires module 'psycopg2'\n"
        self.ui.rbpostgres.setEnabled(postgres)

        mysql = True
        try:
            import MySQLdb
            import MySQLdb.converters
        except BaseException:
            module_errors += "MySQL storage not available, requires module 'MySQLdb'\n"
            mysql = False
        if module_errors != "":
            module_errors += "Check IcepapCMS user manual to solve these " \
                             "issues"
        self.ui.lblModules.setText(module_errors)
        self.ui.rbmysql.setEnabled(mysql)

    @loggingInfo
    def fillConfig(self):
        ''' storage configuration'''
        self.checkDbEngines()
        db = self._config.config[self._config.database]["database"]
        rb = getattr(self.ui, "rb" + db)
        rb.setChecked(True)
        self.ui.txtLocalFolder.setText(
            self._config.config[self._config.database]["folder"])
        server = self._config.config[self._config.database]["server"]
        server = server.split(':')
        self.ui.txtHost.setText(server[0])
        self.ui.txtPort.setText(server[1])
        user = self._config.config[self._config.database]["user"]
        pwd = self._config.config[self._config.database]["password"]
        self.ui.txtUser.setText(user)
        self.ui.txtPassword.setText(pwd)

        ''' icepap configuration'''
        config = self._config.config[self._config.icepap]
        debug_enabled = config["debug_enabled"]
        debug_level = config["debug_level"]
        log_folder = config["log_folder"]
        firmware_folder = config["firmware_folder"]
        configs_folder = self._config.configs_folder
        templates_folder = config["templates_folder"]
        snapshots_folder = config['snapshots_folder']

        self.ui.chkDebug.setChecked(debug_enabled == str(True))
        self.ui.sbDebugLevel.setValue(int(debug_level))
        self.ui.txtLogFolder.setText(log_folder)
        self.ui.txtFirmwareFolder.setText(firmware_folder)
        self.ui.txtConfigsFolder.setText(configs_folder)
        self.ui.txtTemplatesFolder.setText(templates_folder)
        self.ui.txtSnapshotsFolder.setText(snapshots_folder)

    @loggingInfo
    def checkPreferences(self):
        try:
            ''' Storage Configuration '''
            config_db = self._config.config[self._config.database]
            if config_db["database"] != str(self.selectedDB):
                self.StorageChanged = True
                config_db["database"] = str(self.selectedDB)

            if self.ui.rbsqlite.isChecked():
                local_folder = str(self.ui.txtLocalFolder.text())
                if config_db["folder"] != local_folder:
                    config_db["folder"] = local_folder
                    self.StorageChanged = True
            else:
                host = str(self.ui.txtHost.text()).strip()
                port = str(self.ui.txtPort.text()).strip()
                user = str(self.ui.txtUser.text()).strip()
                pwd = str(self.ui.txtPassword.text()).strip()
                if host == "" or port == "":
                    return False
                remote_server = host + ":" + port
                if config_db["server"] != remote_server:
                    self.StorageChanged = True
                    config_db["server"] = remote_server
                if user != config_db["user"] or pwd != config_db["password"]:
                    self.StorageChanged = True
                    config_db["user"] = user
                    config_db["password"] = pwd

            ''' icepap configuration'''
            config_ipap = self._config.config[self._config.icepap]
            config_ipap["debug_enabled"] = str(self.ui.chkDebug.isChecked())
            config_ipap["debug_level"] = int(self.ui.sbDebugLevel.value())
            config_ipap["log_folder"] = self.ui.txtLogFolder.text()
            config_ipap["firmware_folder"] = self.ui.txtFirmwareFolder.text()
            config_ipap["templates_folder"] = self.ui.txtTemplatesFolder.text()
            config_ipap["snapshots_folder"] = self.ui.txtSnapshotsFolder.text()

            return True
        except BaseException as e:
            self.log.error("Unexpected error on checkPreferences: %s", e)
            return False


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = DialogPreferences(None)
    w.show()
    sys.exit(app.exec_())