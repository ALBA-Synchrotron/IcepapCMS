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


import sys
import os
import webbrowser
from PyQt5 import QtCore, QtGui, Qt, QtWidgets, uic
from pkg_resources import resource_filename, get_distribution, \
    DistributionNotFound
import subprocess
import logging
from ..lib import MainManager, Conflict, ConfigManager, \
    StormManager
from .icepap_treemodel import IcepapTreeModel
from .pageipapdriver import PageiPapDriver
from .pageipapcrate import PageiPapCrate
from .pageipapsystem import PageiPapSystem
from .dialogaddicepap import DialogAddIcepap
from .dialogaddlocation import DialogAddLocation

from .dialogconflictdriver_nonexpert import DialogConflictNonExpert
from .dialogconflictdriver_expert import DialogConflictExpert
from .dialognewdriver import DialogNewDriver

from .dialogpreferences import DialogPreferences
from .dialogipapprogram import DialogIcepapProgram
from .dialogsnapshot import DialogSnapshot
from .ipapconsole import IcepapConsole
from .messagedialogs import MessageDialogs
from .templatescatalogwidget import TemplatesCatalogWidget
from ..helpers import loggingInfo
from ..gui.ldap.login import DialogLdapLogin

__version__ = '3.2.0'


class IcepapApp(QtWidgets.QApplication):
    log = logging.getLogger('{}.IcepapApp'.format(__name__))

    def __init__(self,parent=None):
        QtWidgets.QApplication.__init__(self, [])

    @loggingInfo
    def start(self):
        self.setStyle("plastique")
        splash_pxmap = QtGui.QPixmap(":/logos/icons/IcepapMed.png")
        splash = QtWidgets.QSplashScreen(splash_pxmap)
        splash.show()
        icepapcms = IcepapCMS()
        icepapcms.show()
        splash.finish(icepapcms)
        self.exec_()


class IcepapCMS(QtWidgets.QMainWindow):
    log = logging.getLogger('{}.IcepapCMS'.format(__name__))

    @loggingInfo
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'icepapcms.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)

        self._config = ConfigManager()

        default_user = 'NotValidated'
        self._config.username = default_user
        if os.name == 'posix':  # this works for linux and macOSX
            self._config.username = os.getenv('USER', default_user)
        elif os.name == 'nt':  # win NT, XP... (and Vista?)
            self._config.username = os.getenv('USERNAME', default_user)

        if self._config.config['ldap']['use']:
            # FORCE AN LDAP LOGIN TO GET CORRECT USER NAMES IN THE DRIVER
            # SIGNATURES
            login = DialogLdapLogin(self, config=self._config.config['ldap'])
            accepted = login.exec()
            if not accepted:
                sys.exit(-1)
            self._config.username = login.username

        self.checkTimer = Qt.QTimer(self)

        self.initGUI()

        self.ui.pageiPapSystem = PageiPapSystem(self)
        self.ui.stackedWidget.addWidget(self.ui.pageiPapSystem)
        self.ui.pageiPapCrate = PageiPapCrate(self)
        self.ui.stackedWidget.addWidget(self.ui.pageiPapCrate)
        self.ui.pageiPapDriver = PageiPapDriver(self)
        self.ui.stackedWidget.addWidget(self.ui.pageiPapDriver)
        self.signalConnections()
        self.refreshTimer = Qt.QTimer(self)
        self.checkTimer.timeout.connect(self.checkIcepapConnection)

    @loggingInfo
    def signalConnections(self):
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionPreferences.triggered.connect(self.actionPreferenceMth)
        self.ui.actionGoNext.triggered.connect(self.actionGoNextMth)
        self.ui.actionTree_Explorer.triggered.connect(
            self.actionTreeExplorerMth)
        self.ui.actionToolbar.triggered.connect(self.actionToolbarMth)
        self.ui.actionGoPrevious.triggered.connect(self.actionGoPreviousMth)
        self.ui.actionGoUp.triggered.connect(self.actionGoUpMth)
        self.ui.actionRefresh.triggered.connect(self.actionRefreshMth)
        self.ui.actionExport.triggered.connect(self.actionExportMth)
        self.ui.actionImport.triggered.connect(self.actionImportMth)
        self.ui.actionConsole.triggered.connect(self.actionConsoleMth)
        self.ui.actionFirmwareUpgrade.triggered.connect(
            self.actionFirmwareUpgradeMth)
        self.ui.actionSaveConfig.triggered.connect(self.actionSaveConfigMth)
        self.ui.actionHistoricCfg.triggered.connect(self.actionHistoricCfgMth)
        self.ui.actionOscilloscope.triggered.connect(self.action_osc_clicked)
        self.ui.actionCopy.triggered.connect(self.actionCopyMth)
        self.ui.actionPaste.triggered.connect(self.actionPasteMth)
        self.ui.actionHelp.triggered.connect(self.actionHelpMth)
        self.ui.actionUser_manual.triggered.connect(self.actionUser_ManualMth)
        self.ui.actionHardware_manual.triggered.connect(
            self.actionHardware_ManualMth)
        self.ui.actionTemplates.triggered.connect(self.actionTemplatesMth)
        self.ui.treeView.clicked.connect(self.treeview_on_click)
        self.ui.treeView.doubleClicked.connect(self.treeview_on_doubleclick)
        self.ui.treeView.setContextMenuPolicy(Qt.Qt.CustomContextMenu)
        self.ui.treeView.customContextMenuRequested.connect(self.__contextMenu)
        self.ui.btnTreeAdd.clicked.connect(self.btnTreeAdd_on_click)
        self.ui.btnTreeRemove.clicked.connect(self.btnTreeRemove_on_click)
        self.ui.actionAddIcepap.triggered.connect(self.btnTreeAdd_on_click)
        self.ui.actionDeleteIcepap.triggered.connect(
            self.btnTreeRemove_on_click)
        self.ui.menuView.aboutToShow.connect(self.menuView_before_show)
        self.ui.cbLocation.activated.connect(self.locationChanged)
        self.ui.actionAddLocation.triggered.connect(self.addLocation)
        self.ui.actionDeleteLocation.triggered.connect(self.deleteLocation)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionSnapshot.triggered.connect(self.snapshot)

    @loggingInfo
    def initGUI(self):
        self._manager = MainManager(self)
        if not self._manager.dbStatusOK:
            MessageDialogs.showErrorMessage(
                self, "Storage",
                "Error accessing database.\nCheck storage preferences.")

        self.buildLocationCombo()
        self.checkTimer.start(5000)
        self.locationsNext = []
        self.locationsPrevious = []
        self.currentLocation = ""
        self.ui.actionGoNext.setEnabled(False)
        self.ui.actionGoPrevious.setEnabled(False)
        self.ui.actionExport.setEnabled(False)
        self.ui.actionImport.setEnabled(False)
        self.ui.actionHistoricCfg.setEnabled(False)
        self.ui.actionOscilloscope.setEnabled(False)
        self.ui.actionSetExpertFlag.setEnabled(False)
        self.ui.actionTemplates.setEnabled(False)
        self.ui.treeView.setItemsExpandable(True)
        self.ui.actionSaveConfig.setEnabled(False)
        self.ui.stackedWidget.setCurrentIndex(0)

    @loggingInfo
    def about(self):
        MessageDialogs.showInformationMessage(
            self, "IcepapCMS Version", "IcepapCMS version " + __version__)

    @loggingInfo
    def addLocation(self):
        dlg = DialogAddLocation(self)
        dlg.exec_()
        if dlg.result():
            location = dlg.getData()
            if location == '':
                MessageDialogs.showErrorMessage(
                    self, "Add location", "Location must have a name")
                return
            if self._manager.addLocation(location):
                self.ui.cbLocation.addItem(location)
                if self.ui.cbLocation.count() == 1:
                    self.ui.btnTreeAdd.setEnabled(True)
                    self.ui.btnTreeRemove.setEnabled(True)
                self.ui.cbLocation.setCurrentIndex(
                    self.ui.cbLocation.findText(
                        location, QtCore.Qt.MatchFixedString))
                self.locationChanged(location)
            else:
                MessageDialogs.showErrorMessage(
                    self, "Add location", "Error adding location")

    @loggingInfo
    def deleteLocation(self):
        location = self.ui.cbLocation.currentText()
        delete = MessageDialogs.showYesNoMessage(
            self,
            "Delete location",
            "Remove " +
            location +
            " and all the Icepaps inside?")
        if delete:
            self._manager.deleteLocation(location)
            self.ui.cbLocation.removeItem(self.ui.cbLocation.currentIndex())
            self.buildLocationCombo()

    @loggingInfo
    def buildLocationCombo(self):
        self.ui.cbLocation.clear()
        self.ui.treeView.setModel(None)

        keys = sorted(self._manager.locationList.keys())
        for location_name in keys:
            self.ui.cbLocation.addItem(location_name)
        first_location = self.ui.cbLocation.itemText(0)
        activate = False
        if self.ui.cbLocation.count() > 0:
            activate = True

        self.ui.btnTreeAdd.setEnabled(activate)
        self.ui.btnTreeRemove.setEnabled(activate)
        self.ui.actionAddIcepap.setEnabled(activate)
        self.ui.actionDeleteIcepap.setEnabled(activate)
        if first_location != "":
            self.locationChanged(first_location)

    @loggingInfo
    def locationChanged(self, index):
        location = self.ui.cbLocation.currentText()
        self._manager.changeLocation(location)
        self.buildInitialTree()
        for icepap_system in list(self._manager.IcepapSystemList.values()):
            self.stopIcepap(icepap_system)

    @loggingInfo
    def buildInitialTree(self):
        self._tree_model = IcepapTreeModel(
            self._manager.IcepapSystemList, True)
        self.ui.treeView.setModel(self._tree_model)
        self.context_menu_item = None

    @loggingInfo
    def __contextMenu(self, point):
        modelindex = self.ui.treeView.indexAt(point)
        item = self._tree_model.item(modelindex)
        if not item:
            return

        actions = [
            """self.menu.addAction("Sign driver configuration",
            self.actionSaveConfigMth)""",
            """self.menu.addAction("Solve driver configuration conflict",
            self.contextSolveConflict)""",
            """self.menu.addAction("Delete driver not present",
            self.contextDeleteDriverError)""",
            """self.menu.addAction("New driver. Keep or set to default",
            self.contextSolveNewDriver)""",
            """self.menu.addSeparator()""",
            """self.menu.addAction("Start Icepap system configuration",
            self.contextIcepapStart)""",
            """self.menu.addAction("Rescan Icepap system",
            self.contextIcepapStart)""",
            """self.menu.addAction("Finish Icepap system configuration",
            self.contextIcepapStop)""",
            """self.menu.addSeparator()""",
            """self.menu.addAction("Edit Icepap system information",
            self.contextEditIcepap)""",
            """self.menu.addAction("Delete Icepap system configuration",
            self.btnTreeRemove_on_click)""",
        ]
        self.menu = Qt.QMenu(self)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.menu.setFont(font)
        self.context_menu_item = item
        shown_actions = []
        if item.role == IcepapTreeModel.SYSTEM_OFFLINE:
            shown_actions = [5, 8, 9, 10]
        if item.role == IcepapTreeModel.DRIVER:
            shown_actions = [6, 7, 8, 9, 10]
        elif item.role == IcepapTreeModel.DRIVER_CFG:
            shown_actions = [0, 4, 6, 7, 8, 9, 10]
        elif item.role == IcepapTreeModel.DRIVER_ERROR:
            shown_actions = [2, 4, 6, 7, 8, 9, 10]
        elif item.role == IcepapTreeModel.DRIVER_WARNING:
            shown_actions = [1, 4, 6, 7, 8, 9, 10]
        elif item.role == IcepapTreeModel.DRIVER_NEW:
            shown_actions = [3, 4, 6, 7, 8, 9, 10]
        elif item.role == IcepapTreeModel.SYSTEM or \
                item.role == IcepapTreeModel.CRATE or \
                item.role == IcepapTreeModel.SYSTEM_ERROR or \
                item.role == IcepapTreeModel.SYSTEM_WARNING:
            shown_actions = [6, 7, 8, 9, 10]
        for i in shown_actions:
            exec(actions[i])
        self.menu.popup(self.cursor().pos())

    @loggingInfo
    def contextIcepapStart(self):
        if self.context_menu_item:
            item = self.context_menu_item
            self.scanIcepap(item.getIcepapSystem())
        self.context_menu_item = None

    @loggingInfo
    def contextIcepapStop(self):
        if self.context_menu_item:
            item = self.context_menu_item
            self.stopIcepap(item.getIcepapSystem())
        self.context_menu_item = None

    @loggingInfo
    def contextEditIcepap(self):
        if self.context_menu_item:
            item = self.context_menu_item
            self.editIcepap(item)
        self.context_menu_item = None

    @loggingInfo
    def contextSolveConflict(self):
        if self.context_menu_item:
            item = self.context_menu_item
            self.solveConflict(item)
        self.context_menu_item = None

    @loggingInfo
    def contextDeleteDriverError(self):
        if self.context_menu_item:
            item = self.context_menu_item
            self.deleteDriverError(item)
        self.context_menu_item = None

    @loggingInfo
    def contextSolveNewDriver(self):
        if self.context_menu_item:
            item = self.context_menu_item
            self.solveNewDriver(item)
        self.context_menu_item = None

    @loggingInfo
    def btnTreeAdd_on_click(self):
        location = self.ui.cbLocation.currentText()
        dlg = DialogAddIcepap(self, location)
        dlg.exec_()
        if dlg.result():
            data = dlg.getData()
            self.ui.cbLocation.setCurrentIndex(
                self.ui.cbLocation.findText(
                    data[3], QtCore.Qt.MatchFixedString))
            icepap_system = self._manager.addIcepapSystem(
                data[0], data[1], data[2])
            if icepap_system is not None:
                self._tree_model.addIcepapSystem(
                    icepap_system.name, icepap_system, False)
                self._manager.checkFirmwareVersions(icepap_system)
                self.expandAll(icepap_system.name)

    @loggingInfo
    def actionCopyMth(self):
        self.ui.pageiPapDriver.doCopy()

    @loggingInfo
    def actionPasteMth(self):
        self.ui.pageiPapDriver.doPaste()

    @loggingInfo
    def editIcepap(self, item):
        location = self.ui.cbLocation.currentText()
        dlg = DialogAddIcepap(self, location)
        icepap_system = item.getIcepapSystem()
        dlg.setData(icepap_system.name, icepap_system.host, icepap_system.port,
                    icepap_system.description, location)
        dlg.exec_()
        if dlg.result():
            data = dlg.getData()
            icepap_system.description = str(data[2])
            icepap_system.location_name = str(data[3])

            #item.changeLabel([data[0], data[2]])
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.cbLocation.setCurrentIndex(
                self.ui.cbLocation.findText(
                    data[3], QtCore.Qt.MatchFixedString))

    @loggingInfo
    def checkIcepapConnection(self):
        """ this function checks the icepap connection, notifying the user for
        losing or getting connection """
        icepap_systems_changed = self._manager.checkIcepapSystems()
        for icepap_system in icepap_systems_changed:
            # if icepap_system.conflict != Conflict.NO_CONFLICT:
            self.scanIcepap(icepap_system)

    @loggingInfo
    def stopIcepap(self, icepap_system):
        try:
            self.ui.pageiPapDriver.stopTesting()
            if self.refreshTimer is not None:
                self.refreshTimer.stop()
                self.ui.stackedWidget.setCurrentIndex(0)
                self._manager.stopIcepap(icepap_system)
                self._tree_model.updateIcepapSystem(icepap_system, True)
                self.treeSelectByLocation(icepap_system.name)
        except BaseException:
            pass

    @loggingInfo
    def scanIcepap(self, icepap_system):
        """This function scans and Icepap. This means comparing
        the database configurations and the ones in the hardware """
        self.setStatusMessage("Scanning ...")

        # STORM ACCESS TO ALL DRIVERS FROM THE SYSTEM
        icepap_system.loadDriversfromDB()

        conflicts_list = []
        solved_drivers = ""
        conflicts_list.extend(self._manager.scanIcepap(icepap_system))
        if len(conflicts_list) > 0:
            self.setStatusMessage("Configuration conflicts found.")
            for conflict in conflicts_list:
                icepap_system = conflict[1]
                if conflict[0] == Conflict.NO_CONNECTION:
                    icepap_system.setConflict(conflict[0])
                    self.setStatusMessage(
                        icepap_system.name + ": Connection Error")

                elif conflict[0] in [Conflict.DRIVER_AUTOSOLVE,
                                     Conflict.DRIVER_AUTOSOLVE_EXPERT]:
                    driver = icepap_system.getDriver(conflict[2])

                    if conflict[0] == Conflict.DRIVER_AUTOSOLVE:
                        params_modified, params_new_in_driver, \
                            params_old_in_db = \
                            self.get_driver_param_conflicts(
                                driver.icepapsystem_name, driver.addr)
                        self._manager.saveValuesInIcepap(
                            driver, driver.current_cfg.toList(),
                            ignore_values=params_old_in_db)
                        solved_drivers = solved_drivers + \
                            "%s:%d DB->DSP\n" % (driver.icepapsystem_name,
                                                 driver.addr)

                    elif conflict[0] == Conflict.DRIVER_AUTOSOLVE_EXPERT:
                        driver_values = self.getDriverValues(
                            driver.icepapsystem_name, driver.addr)
                        driver.addConfiguration(driver_values)
                        db = StormManager()
                        db.store(driver_values)
                        solved_drivers = solved_drivers + \
                            "%s:%d DB<-DSP\n" % (driver.icepapsystem_name,
                                                 driver.addr)
                        # @TODO NOTE: I KNOW IT IS STILL PENDING TO UPDATE THE
                        #  LABEL AUTOMATICALLY
                        # BUT YOU WILL GET THE NEW NAME BY JUST CLICKING ON
                        # THE TREE ITEM

                    driver.signDriver()
                    driver.setConflict(Conflict.NO_CONFLICT)
                    icepap_system.child_conflicts -= 1

                else:
                    if not conflict[2] is None:
                        self.setStatusMessage("Configuration conflicts found.")
                        driver = icepap_system.getDriver(conflict[2])
                        driver.setConflict(conflict[0])
        else:
            self.setStatusMessage("Scanning complete!. No conflicts found")

        self._manager.checkFirmwareVersions(icepap_system)
        #######################################################################
        # THE LOOP MAY BE DONE ONLY ONCE
        self._tree_model.updateIcepapSystem(icepap_system)
        # SOMETHING SHOULD BE DONE HERE
        self.expandAll(icepap_system.name)
        self.treeSelectByLocation(icepap_system.name)
        if solved_drivers != "":
            MessageDialogs.showInformationMessage(
                self,
                "Solved conflicts",
                "Auto-solved conflicts in drivers:\n" +
                solved_drivers)

    @loggingInfo
    def getDriverDBValues(self, icepap_system, driver_addr):
        dbIcepapSystem = StormManager().getIcepapSystem(icepap_system)
        return dbIcepapSystem.getDriver(
            driver_addr, in_memory=False).startup_cfg

    @loggingInfo
    def getDriverValues(self, icepap_system, driver_addr):
        return self._manager.getDriverConfiguration(icepap_system, driver_addr)

    @loggingInfo
    def get_driver_param_conflicts(self, icepap_system, driver_addr):
        # Get the parameters that have raised the conflict
        driver_values = self.getDriverValues(icepap_system, driver_addr)
        driver_db_values = self.getDriverDBValues(icepap_system, driver_addr)

        params_modified = []
        params_new_in_driver = []
        params_old_in_db = []

        for db_param, db_value in driver_db_values.toList():
            driver_value = driver_values.getParameter(db_param, True)
            if db_value == driver_value:
                pass
            elif driver_value is None:
                params_old_in_db.append((str(db_param), str(db_value)))
            else:
                params_modified.append(
                    (str(db_param), str(db_value), str(driver_value)))

        for driver_param, driver_value in driver_values.toList():
            db_value = driver_db_values.getParameter(driver_param, True)
            if db_value is None:
                params_new_in_driver.append(
                    (str(driver_param), str(driver_value)))

        return params_modified, params_new_in_driver, params_old_in_db

    @loggingInfo
    def solveConflict(self, item):
        driver = item.itemData
        system = driver.icepapsystem_name
        addr = driver.addr
        expert = self._manager._ctrl_icepap.isExpertFlagSet(system, addr)
        expertFlag = (expert == 'YES')
        message = "%s.%d: Set DataBase values?" % (system, addr)
        if expertFlag:
            message = "%s.%d: Set Driver Values?\n" % (system, addr)
            message = message + "FOUND CONFIG WITH EXPERT = YES"

        params_modified, params_new_in_driver, params_old_in_db = \
            self.get_driver_param_conflicts(system, addr)

        widget, table = self.ui.pageiPapDriver.createTableWidget(
            ["Parameter\nname", "Value in\ndatabase",
             "Value in\ndriver board"])
        more_info_dialog = QtWidgets.QDialog(self)
        more_info_dialog.resize(420, 300)
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(widget)
        more_info_dialog.setModal(True)
        more_info_dialog.setLayout(grid_layout)

        if len(params_modified) > 0:
            for param, db_value, driver_value in params_modified:
                row = table.rowCount()
                table.insertRow(row)

                param_item = QtWidgets.QTableWidgetItem()
                param_item.setText(param)
                table.setItem(row, 0, param_item)

                db_item = QtWidgets.QTableWidgetItem()
                db_item.setText(db_value)
                table.setItem(row, 1, db_item)

                driver_item = QtWidgets.QTableWidgetItem()
                driver_item.setText(driver_value)
                table.setItem(row, 2, driver_item)

        if len(params_new_in_driver) > 0:
            for param, driver_value in params_new_in_driver:
                row = table.rowCount()
                table.insertRow(row)

                param_item = QtWidgets.QTableWidgetItem()
                param_item.setText(param)
                table.setItem(row, 0, param_item)

                db_item = QtWidgets.QTableWidgetItem()
                db_item.setText("---")
                table.setItem(row, 1, db_item)

                driver_item = QtWidgets.QTableWidgetItem()
                driver_item.setText(driver_value)
                table.setItem(row, 2, driver_item)

        if len(params_old_in_db) > 0:
            for param, db_value in params_old_in_db:
                row = table.rowCount()
                table.insertRow(row)

                param_item = QtWidgets.QTableWidgetItem()
                param_item.setText(param)
                table.setItem(row, 0, param_item)

                db_item = QtWidgets.QTableWidgetItem()
                db_item.setText(db_value)
                table.setItem(row, 1, db_item)

                driver_item = QtWidgets.QTableWidgetItem()
                driver_item.setText("---")
                table.setItem(row, 2, driver_item)

        if not expertFlag:
            dialog = DialogConflictNonExpert(self, more_info_dialog)
        else:
            dialog = DialogConflictExpert(self, more_info_dialog)

        dialog.exec_()

        yes = dialog.result()

        if yes:
            if expert == 'YES':
                driver_values = self.getDriverValues(system, addr)
                driver.addConfiguration(driver_values)
                db = StormManager()
                db.store(driver_values)
            else:
                self._manager.saveValuesInIcepap(
                    driver, driver.current_cfg.toList(),
                    ignore_values=params_old_in_db)
            driver.signDriver()
            item.solveConflict()

        # BY NOW, UPDATE THE ICEPAP NAME MANUALLY
        current_cfg = driver.current_cfg
        label = str(driver.addr) + " " + \
            current_cfg.getParameter(str("IPAPNAME"), True)
        item.changeLabel([label])

        icepap_system = item.itemData.icepap_system
        for driver in icepap_system.drivers:
            if driver.conflict != Conflict.NO_CONFLICT:
                return
        self.setStatusMessage("")

    @loggingInfo
    def solveNewDriver(self, item):
        driver = item.itemData
        system = driver.icepapsystem_name
        addr = driver.addr

        widget, table = self.ui.pageiPapDriver.createTableWidget(
            ["Parameter\nname", "Value in\ndriver board"])
        more_info_dialog = QtWidgets.QDialog(self)
        more_info_dialog.resize(320, 600)
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(widget)
        more_info_dialog.setModal(True)
        more_info_dialog.setLayout(grid_layout)

        driver_values = self.getDriverValues(system, addr)
        driver_values_list = driver_values.toList()
        if len(driver_values_list) > 0:
            for param, driver_value in driver_values_list:
                row = table.rowCount()
                table.insertRow(row)

                param_item = QtWidgets.QTableWidgetItem()
                param_item.setText(param)
                table.setItem(row, 0, param_item)

                driver_item = QtWidgets.QTableWidgetItem()
                driver_item.setText(driver_value)
                table.setItem(row, 1, driver_item)

        expert = self._manager._ctrl_icepap.isExpertFlagSet(system, addr)
        expertFlag = (expert == 'YES')
        dialog = DialogNewDriver(self, more_info_dialog, expertFlag)
        dialog.exec_()

        answer = dialog.result()
        if answer not in ["DEFAULT", "DRIVER"]:
            # Since version 1.23, cancelling new driver keeps the system as
            # before
            icepap_system = item.getIcepapSystem()
            icepap_system.removeDriver(item.itemData.addr)
            item.solveConflict()
            self._tree_model.deleteItem(item)
            return False

        if answer == "DEFAULT":
            self._manager.configDriverToDefaults(item.itemData)

        self._manager.updateDriverConfig(item.itemData)
        item.solveConflict()
        driver = item.itemData
        driver.signDriver()
        return True

    @loggingInfo
    def deleteDriverError(self, item):
        delete = MessageDialogs.showYesNoMessage(
            self, "Driver error",
            "Driver not present.\nRemove driver from DB?")
        if delete:
            icepap_system = item.getIcepapSystem()
            icepap_system.removeDriver(item.itemData.addr)
            item.solveConflict()
            self._tree_model.deleteItem(item)

    @loggingInfo
    def refreshTree(self):
        self.ui.pageiPapDriver.stopTesting()
        if self.refreshTimer is not None:
            self.refreshTimer.stop()
        self._manager.reset(self)
        self.initGUI()
        self.ui.stackedWidget.setCurrentIndex(0)

    @loggingInfo
    def btnTreeRemove_on_click(self):
        selectmodel = self.ui.treeView.selectionModel()
        indexes = selectmodel.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            item = self._tree_model.item(index)
            icepap_system = item.getIcepapSystem()
            delete = MessageDialogs.showYesNoMessage(
                self, "Remove Icepap System",
                "Remove " + icepap_system.name + "?")
            if delete:
                self._tree_model.deleteIcepapSystem(icepap_system.name)
                self._manager.deleteIcepapSystem(icepap_system.name)
                self.clearLocationBar()
                self.refreshTimer.stop()

    @loggingInfo
    def treeview_on_doubleclick(self, modelindex):
        self.locationsPrevious.extend(self.locationsNext)
        item = self._tree_model.item(modelindex)
        if item.role == IcepapTreeModel.DRIVER_WARNING:
            # TODO Investigate why it is not used
            userContinues = self.solveConflict(item)
        elif item.role == IcepapTreeModel.DRIVER_NEW:
            solved = self.solveNewDriver(item)
            if not solved:
                return
        elif item.role == IcepapTreeModel.DRIVER_ERROR:
            self.deleteDriverError(item)
        elif item.role == IcepapTreeModel.SYSTEM_OFFLINE or \
                item.role == IcepapTreeModel.SYSTEM_ERROR:
            self.scanIcepap(item.itemData)

        if item.role == IcepapTreeModel.DRIVER and \
                item.itemData.conflict == Conflict.NO_CONFLICT:
            self.treeview_on_click(modelindex)

    @loggingInfo
    def treeview_on_click(self, modelindex):
        self.locationsPrevious.extend(self.locationsNext)
        self.locationsNext = []
        self.addToPrevious(self.currentLocation)
        self.treeSelectByIndex(modelindex)

    @loggingInfo
    def treeSelectByLocation(self, location):
        self.currentLocation = location
        modelindex = self._tree_model.indexByLocation(location)
        if modelindex is not None:
            selection = Qt.QItemSelection(modelindex, modelindex)
            selectmodel = self.ui.treeView.selectionModel()
            selectmodel.clear()
            selectmodel.select(selection, Qt.QItemSelectionModel.Select)
            self.treeSelectByIndex(modelindex)

    @loggingInfo
    def treeSelectByIndex(self, modelindex):
        item = self._tree_model.item(modelindex)
        self.currentLocation = item.location
        self.ui.actionExport.setEnabled(False)
        self.ui.actionImport.setEnabled(False)
        self.ui.actionHistoricCfg.setEnabled(False)
        self.ui.actionOscilloscope.setEnabled(False)
        self.ui.actionTemplates.setEnabled(False)
        self.ui.actionSaveConfig.setEnabled(False)
        self.ui.actionSetExpertFlag.setEnabled(False)
        self.ui.actionCopy.setEnabled(False)
        self.ui.actionPaste.setEnabled(False)
        self.ui.pageiPapDriver.stopTesting()
        if self.refreshTimer is not None:
            self.refreshTimer.stop()

        # BEFORE CHANGING THE TREE NODE, WE SHOULD CHECK IF THE LAST DRIVER
        # CAN BE SET BACK TO MODE 'OPER' OR NOT
        if self.ui.pageiPapDriver.checkSaveConfigPending():
            self.ui.actionSaveConfig.setEnabled(True)

        if item.role == IcepapTreeModel.DRIVER or \
                item.role == IcepapTreeModel.DRIVER_CFG:

            # THE FILLDATA METHOD KNOWS IF THE BUTTON HAS TO BE ENABLED OR NOT
            self.ui.actionSaveConfig.setEnabled(False)
            self.ui.pageiPapDriver.fillData(item.itemData)
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.actionExport.setEnabled(True)
            self.ui.actionImport.setEnabled(True)
            self.ui.actionHistoricCfg.setEnabled(True)
            self.ui.actionOscilloscope.setEnabled(True)
            self._axis_selected = item.itemData
            self.ui.actionTemplates.setEnabled(True)
            self.ui.actionSetExpertFlag.setEnabled(True)
            # ENABLE THE COPY & PASTE ACTIONS
            self.ui.actionCopy.setEnabled(True)
            self.ui.actionPaste.setEnabled(True)

        elif item.role == IcepapTreeModel.SYSTEM or \
                item.role == IcepapTreeModel.SYSTEM_WARNING:
            self.ui.pageiPapSystem.fillData(item.itemData)
            self.ui.stackedWidget.setCurrentIndex(1)
            try:
                self.refreshTimer.timeout.disconnect(
                    self.ui.pageiPapSystem.refresh)
            except Exception:
                pass
            self.refreshTimer.timeout.connect(self.ui.pageiPapSystem.refresh)
            self.refreshTimer.start(2000)
        elif item.role == IcepapTreeModel.CRATE:
            self.ui.pageiPapCrate.fillData(
                item.getIcepapSystem(), int(
                    item.itemLabel[0].value()))
            self.ui.stackedWidget.setCurrentIndex(2)
            try:
                self.refreshTimer.timeout.disconnect(
                    self.ui.pageiPapCrate.refresh)
            except Exception:
                pass
            self.refreshTimer.timeout.connect(self.ui.pageiPapCrate.refresh)
            self.refreshTimer.start(2000)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

        self.expandIndex(modelindex)

    @loggingInfo
    def actionGoPreviousMth(self):
        location = self.locationsPrevious.pop()
        self.addToNext(self.currentLocation)
        self.treeSelectByLocation(location)

    @loggingInfo
    def actionGoNextMth(self):
        location = self.locationsNext.pop()
        self.addToPrevious(self.currentLocation)
        self.treeSelectByLocation(location)

    @loggingInfo
    def addToPrevious(self, location):
        if not location == "":
            self.locationsPrevious.append(location)
        self.checkGoPreviousActions()

    @loggingInfo
    def addToNext(self, location):
        if not location == "":
            self.locationsNext.append(location)
        self.checkGoPreviousActions()

    @loggingInfo
    def clearLocationBar(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.currentLocation = 0
        self.locationsPrevious = []
        self.locationsNext = []
        self.checkGoPreviousActions()

    @loggingInfo
    def checkGoPreviousActions(self):
        if len(self.locationsPrevious) == 0:
            self.ui.actionGoPrevious.setEnabled(False)
        else:
            self.ui.actionGoPrevious.setEnabled(True)

        if len(self.locationsNext) == 0:
            self.ui.actionGoNext.setEnabled(False)
        else:
            self.ui.actionGoNext.setEnabled(True)

    @loggingInfo
    def actionGoUpMth(self):
        selectmodel = self.ui.treeView.selectionModel()
        indexes = selectmodel.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            modelindex = self._tree_model.parent(index)
            if modelindex.row() > -1:
                self.addToPrevious(self.currentLocation)
                selection = Qt.QItemSelection(modelindex, modelindex)
                selectmodel = self.ui.treeView.selectionModel()
                selectmodel.clear()
                selectmodel.select(selection, Qt.QItemSelectionModel.Select)
                self.treeSelectByIndex(modelindex)

    @loggingInfo
    def actionRefreshMth(self):
        refresh = MessageDialogs.showYesNoMessage(
            self, "Init CMS", "Get all data from Database and lose changes?")
        if refresh:
            self.refreshTree()

    @loggingInfo
    def closeEvent(self, event):
        for child in self.children():
            if isinstance(child, QtWidgets.QDialog):
                child.done(0)

        self.refreshTimer.stop()
        self.ui.stackedWidget.setCurrentIndex(0)
        # Before closing, if any driver was in config mode, be sure if it can
        # be set back to oper mode or some signature is pending

        if self.ui.pageiPapDriver.checkSaveConfigPending():
            signList = self._manager.getDriversToSign()
            if MessageDialogs.showYesNoMessage(
                    self, "Validate Drivers config",
                    "There are driver configurations pending to be "
                    "validated.\nAll changes may be lost\nValidate "
                    "driver configs?."):
                for driver in signList:
                    driver.signDriver()
            else:
                for driver in signList:
                    self._manager.discardDriverChanges(driver)
                    self._manager.endConfiguringDriver(driver)

        if not self._manager.closeAllConnections():
            if MessageDialogs.showYesNoMessage(
                    self, "Storage",
                    "Error closing storage.\nDiscard changes and close?."):
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    @loggingInfo
    def setStatusMessage(self, message):
        self.ui.statusbar.showMessage(message)

    @loggingInfo
    def expandAll(self, location):
        parent = self._tree_model.indexByLocation(location)
        if parent:
            childs = self._tree_model.rowCount(parent)
            for row in range(childs):
                index = self._tree_model.index(row, 0, parent)
                self.expandIndex(index)
                item = self._tree_model.item(index)
                self.expandAll(item.location)

    @loggingInfo
    def expandIndex(self, modelindex):
        index = self._tree_model.parent(modelindex)
        while(index.row() > -1):
            self.ui.treeView.expand(index)
            index = self._tree_model.parent(index)

    @loggingInfo
    def actionImportMth(self):
        if self.ui.stackedWidget.currentIndex() == 3:
            self.ui.pageiPapDriver.doImport()

    @loggingInfo
    def actionExportMth(self):
        if self.ui.stackedWidget.currentIndex() == 3:
            self.ui.pageiPapDriver.doExport()

    @loggingInfo
    def actionConsoleMth(self):
        dlg = IcepapConsole(self)
        dlg.show()

    @loggingInfo
    def actionPreferenceMth(self):
        dlg = DialogPreferences(self)
        dlg.exec_()
        if dlg.StorageChanged:
            self._manager.reset(self)
            self.initGUI()

    @loggingInfo
    def actionFirmwareUpgradeMth(self):
        self.clearLocationBar()
        dlg = DialogIcepapProgram(self)
        dlg.exec_()

    def action_osc_clicked(self):
        print(self._axis_selected.icepapsystem_name, self._axis_selected.addr)
        try:
            get_distribution('icepaposc')
        except DistributionNotFound:

            MessageDialogs.showErrorMessage(self, 'IcepapOSC Error',
                                            'IcepapOSC is not installed')
            return

        subprocess.Popen(['icepaposc', '--axis', str(self._axis_selected.addr),
                          self._axis_selected.icepapsystem_name])


    @loggingInfo
    def actionSaveConfigMth(self):
        QtWidgets.QApplication.instance().setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            if self.ui.stackedWidget.currentIndex() == 0:
                # sign all drivers
                icepap_list = self._manager.getIcepapList()
                for icepap_name, icepap_system in list(icepap_list.items()):
                    icepap_system.signSystem()
                    self._tree_model.layoutChanged.emit()
            elif self.ui.stackedWidget.currentIndex() == 1:
                # sign all icepap system
                self.ui.pageiPapSystem.icepap_system.signSystem()
                self._tree_model.layoutChanged.emit()
            elif self.ui.stackedWidget.currentIndex() == 2:
                # sign all icepap crate
                self.ui.pageiPapCrate.icepap_system.signCrate(
                    self.ui.pageiPapCrate.cratenr)
                self._tree_model.layoutChanged.emit()
            elif self.ui.stackedWidget.currentIndex() == 3:
                # sign driver
                self.ui.pageiPapDriver.signDriver()
                self.ui.actionSaveConfig.setEnabled(False)

        except Exception as e:
            msg = "Some problems saving driver's configuration: {}".format(e)
            self.log.error(msg)
            MessageDialogs.showInformationMessage(self, "Signature", msg)
        QtWidgets.QApplication.instance().restoreOverrideCursor()

    @loggingInfo
    def actionHistoricCfgMth(self):
        if self.ui.actionHistoricCfg.isChecked():
            self.ui.pageiPapDriver.showHistoricWidget()
        else:
            self.ui.pageiPapDriver.hideHistoricWidget()

    @loggingInfo
    def actionTemplatesMth(self):

        # The master catalog file
        master_catalog_file = resource_filename('icepapcms.templates',
                                                'catalog.xml')

        dlg = TemplatesCatalogWidget(
            master_catalog_file, self.ui.pageiPapDriver, self)
        dlg.show()

    @loggingInfo
    def actionHelpMth(self):
        filename = resource_filename('icepapcms.doc',
                                     'IcepapCMSUserManual.pdf')
        webbrowser.open(filename)

    @loggingInfo
    def actionUser_ManualMth(self):
        file_name = resource_filename('icepapcms.doc',
                                      'IcePAP_UserManual.pdf')
        webbrowser.open(file_name)

    @loggingInfo
    def actionHardware_ManualMth(self):
        file_name = resource_filename('icepapcms.doc',
                                      'IcePAP_HardwareManual.pdf')
        webbrowser.open(file_name)

    @loggingInfo
    def menuView_before_show(self):
        self.ui.actionToolbar.setChecked(not self.ui.toolBar.isHidden())
        self.ui.actionTree_Explorer.setChecked(not self.ui.dockTree.isHidden())

    @loggingInfo
    def actionToolbarMth(self):
        self.ui.actionToolbar.setChecked(not self.ui.toolBar.isHidden())
        if not self.ui.actionToolbar.isChecked():
            self.ui.toolBar.show()
        else:
            self.ui.toolBar.close()

    @loggingInfo
    def actionTreeExplorerMth(self):
        self.ui.actionTree_Explorer.setChecked(not self.ui.dockTree.isHidden())
        if not self.ui.actionTree_Explorer.isChecked():
            self.ui.dockTree.show()
        else:
            self.ui.dockTree.close()

    def snapshot(self):
        selected_index = self.ui.treeView.selectedIndexes()
        if selected_index:
            modelindex = selected_index[0]
            item = self._tree_model.item(modelindex)
            icepap_system = item.getIcepapSystem()
            host = icepap_system.host
            port = icepap_system.port
        else:
            host = ''
            port = 5000
        snapshot = DialogSnapshot(self, host, port)
        snapshot.setModal(True)
        snapshot.show()


