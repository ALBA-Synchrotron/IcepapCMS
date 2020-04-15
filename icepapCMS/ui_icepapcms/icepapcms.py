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


import sys, os, webbrowser
from PyQt4 import QtCore, QtGui, Qt
from .ui_icepapcms import Ui_IcepapCMS
from qrc_icepapcms import *
from ..lib_icepapcms import MainManager, Conflict, ConfigManager, StormManager, Timer
from icepap_treemodel import IcepapTreeModel
from pageipapdriver import PageiPapDriver
from pageipapcrate import PageiPapCrate
from pageipapsystem import PageiPapSystem
from dialogaddicepap import DialogAddIcepap
from dialogaddlocation import DialogAddLocation
from dialogdriverconflict import DialogDriverConflict

from dialogconflictdriver_nonexpert import DialogConflictNonExpert
from dialogconflictdriver_expert import DialogConflictExpert
from dialognewdriver import DialogNewDriver

from dialogpreferences import DialogPreferences
from dialogipapprogram import DialogIcepapProgram
from ipapconsole import IcepapConsole
from messagedialogs import MessageDialogs
from templatescatalogwidget import TemplatesCatalogWidget
from optparse import OptionParser

__version__ = '2.3.6'

class IcepapApp(QtGui.QApplication):    
    def __init__(self, *args):

        # from http://docs.python.org/library/optparse.html
        usage = "usage: %prog [options] arg"
        parser = OptionParser(usage)
        parser.add_option("-e", "--expert",
                          action="store_true", dest="expert", help="Full expert interface. False by default")
        parser.add_option("-s", "--skip-versioncheck",
                          action="store_true", dest="skipversioncheck", help="Skip the version mismatch check. False by default")
        parser.add_option("","--all-networks",
                          action="store_true", dest="allnets", help="Allow all available icepap systems. False by default")
        parser.add_option("","--ldap",
                          action="store_true", dest="ldap", help="Force LDAP login to get username. False by default")
        (options, args) = parser.parse_args()


        QtGui.QApplication.__init__(self,[])
        self.setStyle("plastique")
        splash_pxmap = QtGui.QPixmap(":/logos/icons/IcepapMed.png")
        splash = QtGui.QSplashScreen(splash_pxmap)
        splash.show()
        icepapcms = IcepapCMS(options,args)
        icepapcms.show()
        splash.finish(icepapcms)
        self.exec_()
        
class IcepapCMS(QtGui.QMainWindow):
    def __init__(self, options,args,parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.ui = Ui_IcepapCMS()
        self.ui.setupUi(self)
        self._config = ConfigManager()
        self._config._options = options
        self._config._args = args

        default_user = 'NotValidated'
        self._config.username = default_user
        if os.name is 'posix': #this works for linux and macOSX
            self._config.username = os.getenv('USER', default_user)
        elif os.name is 'nt': #win NT, XP... (and Vista?)
            self._config.username = os.getenv('USERNAME', default_user)

        if self._config._options.ldap:
            # FORCE AN LDAP LOGIN TO GET CORRECT USER NAMES IN THE DRIVER SIGNATURES
            try:
                import ldap_login
                login_dlg = ldap_login.LdapLogin(self)
                login_dlg.exec_()
                valid_ldap_login = False
                if login_dlg.result() == QtGui.QDialog.Accepted:
                    if login_dlg.username.lower() not in ('sicilia', 'operator'):
                        self._config.username = login_dlg.username
                        valid_ldap_login = True
                if not valid_ldap_login:
                    print '\n\nSorry, we only allow validated users to save configs to Icepap drivers.\n'
                    sys.exit(-1)
            except Exception,e:
                print 'Using IcepapCMS with the system\'s username: %s' % self._config.username
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
        QtCore.QObject.connect(self.checkTimer,QtCore.SIGNAL("timeout()"),self.checkIcepapConnection)
               
    
    def signalConnections(self):
        QtCore.QObject.connect(self.ui.actionQuit,QtCore.SIGNAL("triggered()"),self.close)
        QtCore.QObject.connect(self.ui.actionPreferences,QtCore.SIGNAL("triggered()"),self.actionPreferences)
        QtCore.QObject.connect(self.ui.actionGoNext,QtCore.SIGNAL("triggered()"),self.actionGoNext)
        QtCore.QObject.connect(self.ui.actionTree_Explorer,QtCore.SIGNAL("triggered()"),self.actionTreeExplorer)
        QtCore.QObject.connect(self.ui.actionToolbar,QtCore.SIGNAL("triggered()"),self.actionToolbar)                
        QtCore.QObject.connect(self.ui.actionGoPrevious,QtCore.SIGNAL("triggered()"),self.actionGoPrevious)
        QtCore.QObject.connect(self.ui.actionGoUp,QtCore.SIGNAL("triggered()"),self.actionGoUp)       
        QtCore.QObject.connect(self.ui.actionRefresh,QtCore.SIGNAL("triggered()"),self.actionRefresh)         
        QtCore.QObject.connect(self.ui.actionExport,QtCore.SIGNAL("triggered()"),self.actionExport)         
        QtCore.QObject.connect(self.ui.actionImport,QtCore.SIGNAL("triggered()"),self.actionImport)         
        QtCore.QObject.connect(self.ui.actionConsole,QtCore.SIGNAL("triggered()"),self.actionConsole)         
        QtCore.QObject.connect(self.ui.actionFirmwareUpgrade,QtCore.SIGNAL("triggered()"),self.actionFimwareUpgrade)         
        QtCore.QObject.connect(self.ui.actionSaveConfig,QtCore.SIGNAL("triggered()"),self.actionSaveConfig)
        QtCore.QObject.connect(self.ui.actionHistoricCfg,QtCore.SIGNAL("triggered()"),self.actionHistoricCfg)
        QtCore.QObject.connect(self.ui.actionCopy,QtCore.SIGNAL("triggered()"),self.actionCopy)
        QtCore.QObject.connect(self.ui.actionPaste,QtCore.SIGNAL("triggered()"),self.actionPaste)

        QtCore.QObject.connect(self.ui.actionHelp,QtCore.SIGNAL("triggered()"),self.actionHelp)
        QtCore.QObject.connect(self.ui.actionUser_manual,QtCore.SIGNAL("triggered()"),self.actionUser_Manual)
        QtCore.QObject.connect(self.ui.actionHardware_manual,QtCore.SIGNAL("triggered()"),self.actionHardware_Manual)
        QtCore.QObject.connect(self.ui.actionTemplates,QtCore.SIGNAL("triggered()"),self.actionTemplates)
        QtCore.QObject.connect(self.ui.treeView,QtCore.SIGNAL("clicked(QModelIndex)"),self.treeview_on_click)
        QtCore.QObject.connect(self.ui.treeView,QtCore.SIGNAL("doubleClicked(QModelIndex)"),self.treeview_on_doubleclick)
        self.ui.treeView.setContextMenuPolicy(Qt.Qt.CustomContextMenu)
        self.connect(self.ui.treeView, 
                     QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self.__contextMenu)
        QtCore.QObject.connect(self.ui.btnTreeAdd,QtCore.SIGNAL("clicked()"),self.btnTreeAdd_on_click)
        QtCore.QObject.connect(self.ui.btnTreeRemove,QtCore.SIGNAL("clicked()"),self.btnTreeRemove_on_click)
        QtCore.QObject.connect(self.ui.actionAddIcepap ,QtCore.SIGNAL("triggered()"),self.btnTreeAdd_on_click)         
        QtCore.QObject.connect(self.ui.actionDeleteIcepap,QtCore.SIGNAL("triggered()"),self.btnTreeRemove_on_click)
        QtCore.QObject.connect(self.ui.menuView,QtCore.SIGNAL("aboutToShow()"),self.menuView_before_show)
        QtCore.QObject.connect(self.ui.cbLocation,QtCore.SIGNAL("activated  (const QString&)"),self.locationChanged)
        QtCore.QObject.connect(self.ui.actionAddLocation,QtCore.SIGNAL("triggered()"),self.addLocation)
        QtCore.QObject.connect(self.ui.actionDeleteLocation,QtCore.SIGNAL("triggered()"),self.deleteLocation)
        QtCore.QObject.connect(self.ui.actionAbout,QtCore.SIGNAL("triggered()"),self.about)
        

    def initGUI(self):
        self._manager = MainManager(self)
        if not self._manager.dbStatusOK:
            MessageDialogs.showErrorMessage(self, "Storage", "Error accessing database.\nCheck storage preferences.")
        

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
        self.ui.actionSetExpertFlag.setEnabled(False)
        self.ui.actionTemplates.setEnabled(False)
        self.ui.treeView.setItemsExpandable(True)        
        self.ui.actionSaveConfig.setEnabled(False)
        self.ui.stackedWidget.setCurrentIndex(0)


    def about(self):
        MessageDialogs.showInformationMessage(self,"IcepapCMS Version","IcepapCMS version "+__version__)
        
    def addLocation(self):
        dlg = DialogAddLocation(self)
        dlg.exec_()
        if dlg.result():
            location = dlg.getData()
            if location == '':
                MessageDialogs.showErrorMessage(self, "Add location", "Location must have a name")
                return
            if self._manager.addLocation(location):
                self.ui.cbLocation.addItem(location)
                if self.ui.cbLocation.count() == 1:
                    self.ui.btnTreeAdd.setEnabled(True)
                    self.ui.btnTreeRemove.setEnabled(True)
                self.ui.cbLocation.setCurrentIndex(self.ui.cbLocation.findText(location, QtCore.Qt.MatchFixedString))
                self.locationChanged(location)
            else:
                MessageDialogs.showErrorMessage(self, "Add location", "Error adding location")
    
    def deleteLocation(self):
        location = self.ui.cbLocation.currentText()
        delete = MessageDialogs.showYesNoMessage(self, "Delete location", "Remove " + location + " and all the Icepaps inside?")
        if delete:
            self._manager.deleteLocation(location)
            self.ui.cbLocation.removeItem(self.ui.cbLocation.currentIndex())
            self.buildLocationCombo()
        
    def buildLocationCombo(self):
        self.ui.cbLocation.clear()
        self.ui.treeView.setModel(None)

        keys = self._manager.locationList.keys()
        keys.sort()                
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
    
    def locationChanged(self, location):
        self._manager.changeLocation(location)
        self.buildInitialTree()
        for icepap_system in self._manager.IcepapSystemList.values():
            self.stopIcepap(icepap_system)

    def buildInitialTree(self):        
        self._tree_model = IcepapTreeModel(self._manager.IcepapSystemList, True)
        self.ui.treeView.setModel(self._tree_model)
        self.context_menu_item = None    
    
    def __contextMenu(self, point):
        modelindex = self.ui.treeView.indexAt(point)
        item = self._tree_model.item(modelindex)                
        if item:
            actions = [
            """self.menu.addAction("Sign driver configuration", self.actionSaveConfig)""",
            """self.menu.addAction("Solve driver configuration conflict", self.contextSolveConflict)""",
            """self.menu.addAction("Delete driver not present", self.contextDeleteDriverError)""",
            """self.menu.addAction("New driver. Keep or set to default", self.contextSolveNewDriver)""",
            """self.menu.addSeparator()""",
            """self.menu.addAction("Start Icepap system configuration", self.contextIcepapStart)""",
            """self.menu.addAction("Rescan Icepap system", self.contextIcepapStart)""",
            """self.menu.addAction("Finish Icepap system configuration", self.contextIcepapStop)""",
            """self.menu.addSeparator()""",
            """self.menu.addAction("Edit Icepap system information", self.contextEditIcepap)""",
            """self.menu.addAction("Delete Icepap system configuration", self.btnTreeRemove_on_click)""",
            ]
            self.menu = Qt.QMenu(self)
            font = QtGui.QFont()
            font.setPointSize(8)
            self.menu.setFont(font)                    
            self.context_menu_item = item
            shown_actions = []            
            if item.role == IcepapTreeModel.SYSTEM_OFFLINE:
                shown_actions = [5,8,9,10]
            if item.role == IcepapTreeModel.DRIVER:
                shown_actions = [6,7,8,9,10]
            elif item.role == IcepapTreeModel.DRIVER_CFG:
                shown_actions = [0,4,6,7,8,9,10]
            elif item.role == IcepapTreeModel.DRIVER_ERROR:
                shown_actions = [2,4,6,7,8,9,10]
            elif item.role == IcepapTreeModel.DRIVER_WARNING:
                shown_actions = [1,4,6,7,8,9,10]                    
            elif item.role == IcepapTreeModel.DRIVER_NEW:
                shown_actions = [3,4,6,7,8,9,10]
            elif item.role == IcepapTreeModel.SYSTEM or item.role == IcepapTreeModel.CRATE or item.role == IcepapTreeModel.SYSTEM_ERROR or item.role == IcepapTreeModel.SYSTEM_WARNING:
                shown_actions = [6,7,8,9,10]             
            for i in shown_actions:
                exec(actions[i])
            self.menu.popup(self.cursor().pos())
    
    def contextIcepapStart(self):        
        if self.context_menu_item:
            item = self.context_menu_item
            self.scanIcepap(item.getIcepapSystem())       
        self.context_menu_item = None
    
    def contextIcepapStop(self):        
        if self.context_menu_item:
            item = self.context_menu_item
            self.stopIcepap(item.getIcepapSystem())       
        self.context_menu_item = None  
    
    def contextEditIcepap(self):        
        if self.context_menu_item:
            item = self.context_menu_item
            self.editIcepap(item)       
        self.context_menu_item = None        
        
    def contextSolveConflict(self): 
        if self.context_menu_item:
            item = self.context_menu_item
            self.solveConflict(item)       
        self.context_menu_item = None
    
    def contextDeleteDriverError(self):
        if self.context_menu_item:
            item = self.context_menu_item
            self.deleteDriverError(item)
        self.context_menu_item = None
        
    def contextSolveNewDriver(self):
        if self.context_menu_item:
            item = self.context_menu_item
            self.solveNewDriver(item)       
        self.context_menu_item = None
       
    def btnTreeAdd_on_click(self):
        location = self.ui.cbLocation.currentText()
        dlg = DialogAddIcepap(self, location)
        dlg.exec_()
        if dlg.result():
            data = dlg.getData()
            self.ui.cbLocation.setCurrentIndex(self.ui.cbLocation.findText(data[3], QtCore.Qt.MatchFixedString))
            icepap_system = self._manager.addIcepapSystem(data[0], data[1], data[2])
            if icepap_system is not None:
                self._tree_model.addIcepapSystem(icepap_system.name, icepap_system, False)
                self._manager.checkFirmwareVersions(icepap_system)
                self.expandAll(icepap_system.name)

    def actionCopy(self):
        self.ui.pageiPapDriver.doCopy()
        
    def actionPaste(self):
        self.ui.pageiPapDriver.doPaste()
        
    def editIcepap(self, item):
        location = self.ui.cbLocation.currentText()
        dlg = DialogAddIcepap(self, location)
        dlg.setData(item.itemData.name, item.itemData.host, item.itemData.port, item.itemData.description, location)
        dlg.exec_()
        if dlg.result():            
            data = dlg.getData()   
            item.itemData.description = unicode(data[2])
            item.itemData.location_name = unicode(data[3])
            item.changeLabel([data[0], data[2]])
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.cbLocation.setCurrentIndex(self.ui.cbLocation.findText(data[3], QtCore.Qt.MatchFixedString))            

    def checkIcepapConnection(self):
        """ this function checks the icepap connection, notifying the user for
        losing or getting connection """
        icepap_systems_changed = self._manager.checkIcepapSystems()
        for icepap_system in icepap_systems_changed:
            #if icepap_system.conflict != Conflict.NO_CONFLICT:
            self.scanIcepap(icepap_system)
            

    def stopIcepap(self, icepap_system):
        try: 
            self.ui.pageiPapDriver.stopTesting()
            if not self.refreshTimer is None:
                self.refreshTimer.stop()
                self.ui.stackedWidget.setCurrentIndex(0)
                self._manager.stopIcepap(icepap_system)
                self._tree_model.updateIcepapSystem(icepap_system, True)
                self.treeSelectByLocation(icepap_system.name)
        except:
            pass
                       
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
                    self.setStatusMessage(icepap_system.name + ": Connection Error")

                elif conflict[0] in [Conflict.DRIVER_AUTOSOLVE, Conflict.DRIVER_AUTOSOLVE_EXPERT]:
                    driver = icepap_system.getDriver(conflict[2])

                    if conflict[0] == Conflict.DRIVER_AUTOSOLVE:
                        params_modified,params_new_in_driver,params_old_in_db = self.get_driver_param_conflicts(driver.icepapsystem_name, driver.addr)
                        self._manager.saveValuesInIcepap(driver,driver.current_cfg.toList(), ignore_values=params_old_in_db)
                        solved_drivers = solved_drivers + "%s:%d DB->DSP\n" % (driver.icepapsystem_name, driver.addr)
                        
                    elif conflict[0] == Conflict.DRIVER_AUTOSOLVE_EXPERT:
                        driver_values = self.getDriverValues(driver.icepapsystem_name, driver.addr)
                        driver.addConfiguration(driver_values)
                        db = StormManager()
                        db.store(driver_values)
                        solved_drivers = solved_drivers + "%s:%d DB<-DSP\n" % (driver.icepapsystem_name, driver.addr)
                        # @TODO NOTE: I KNOW IT IS STILL PENDING TO UPDATE THE LABEL AUTOMATICALLY
                        # BUT YOU WILL GET THE NEW NAME BY JUST CLICKING ON THE TREE ITEM
                        ### current_cfg = driver.current_cfg
                        ### label = str(driver.addr)+" "+current_cfg.getParameter(unicode("IPAPNAME"), True)
                        ### item.changeLabel([label])
                        
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
        #####################################################################################################################################################
        ## THE LOOP MAY BE DONE ONLY ONCE
        self._tree_model.updateIcepapSystem(icepap_system)
        ## SOMETHING SHOULD BE DONE HERE
        self.expandAll(icepap_system.name)
        self.treeSelectByLocation(icepap_system.name)
        if solved_drivers != "":
            MessageDialogs.showInformationMessage(self, "Solved conflicts", "Auto-solved conflicts in drivers:\n"+ solved_drivers)

    def getDriverDBValues(self,icepap_system,driver_addr):
        dbIcepapSystem = StormManager().getIcepapSystem(icepap_system)
        return dbIcepapSystem.getDriver(driver_addr,in_memory=False).startup_cfg


    def getDriverValues(self,icepap_system,driver_addr):
        return self._manager.getDriverConfiguration(icepap_system,driver_addr)

    def get_driver_param_conflicts(self,icepap_system,driver_addr):
        # Get the parameters that have raised the conflict
        driver_values = self.getDriverValues(icepap_system,driver_addr)
        driver_db_values = self.getDriverDBValues(icepap_system,driver_addr)

        params_modified = []
        params_new_in_driver = []
        params_old_in_db = []

        for db_param,db_value in driver_db_values.toList():
            driver_value = driver_values.getParameter(db_param,True)
            if db_value == driver_value:
                pass
            elif driver_value == None:
                params_old_in_db.append((str(db_param),str(db_value)))
            else:
                params_modified.append((str(db_param),str(db_value),str(driver_value)))

        for driver_param,driver_value in driver_values.toList():
            db_value = driver_db_values.getParameter(driver_param,True)
            if db_value == None:
                params_new_in_driver.append((str(driver_param),str(driver_value)))

        return params_modified,params_new_in_driver,params_old_in_db

    def solveConflict(self, item):
        driver = item.itemData
        system = driver.icepapsystem_name
        addr = driver.addr
        expert = self._manager._ctrl_icepap.isExpertFlagSet(system, addr)
        expertFlag = (expert == 'YES')
        message = "%s.%d: Set DataBase values?" % (system, addr)
        if expertFlag:
            message = "%s.%d: Set Driver Values?\n" %(system,addr)
            message = message + "FOUND CONFIG WITH EXPERT = YES"


        params_modified,params_new_in_driver,params_old_in_db = self.get_driver_param_conflicts(system,addr)

        widget, table = self.ui.pageiPapDriver.createTableWidget(["Parameter\nname","Value in\ndatabase","Value in\ndriver board"])
        more_info_dialog = QtGui.QDialog(self)
        more_info_dialog.resize(420,300)
        grid_layout = QtGui.QGridLayout()
        grid_layout.addWidget(widget)
        more_info_dialog.setModal(True)
        more_info_dialog.setLayout(grid_layout)

        if len(params_modified)>0:
            for param,db_value,driver_value in params_modified:
                row = table.rowCount()
                table.insertRow(row)

                param_item = QtGui.QTableWidgetItem()
                param_item.setText(param)
                table.setItem(row, 0, param_item)

                db_item = QtGui.QTableWidgetItem()
                db_item.setText(db_value)
                table.setItem(row, 1, db_item)

                driver_item = QtGui.QTableWidgetItem()
                driver_item.setText(driver_value)
                table.setItem(row, 2, driver_item)

        if len(params_new_in_driver)>0:
            for param,driver_value in params_new_in_driver:
                row = table.rowCount()
                table.insertRow(row)

                param_item = QtGui.QTableWidgetItem()
                param_item.setText(param)
                table.setItem(row, 0, param_item)

                db_item = QtGui.QTableWidgetItem()
                db_item.setText("---")
                table.setItem(row, 1, db_item)

                driver_item = QtGui.QTableWidgetItem()
                driver_item.setText(driver_value)
                table.setItem(row, 2, driver_item)
                
        if len(params_old_in_db)>0:
            for param,db_value in params_old_in_db:
                row = table.rowCount()
                table.insertRow(row)

                param_item = QtGui.QTableWidgetItem()
                param_item.setText(param)
                table.setItem(row, 0, param_item)

                db_item = QtGui.QTableWidgetItem()
                db_item.setText(db_value)
                table.setItem(row, 1, db_item)

                driver_item = QtGui.QTableWidgetItem()
                driver_item.setText("---")
                table.setItem(row, 2, driver_item)
        
        dialog = None
        if not expertFlag:
            dialog = DialogConflictNonExpert(self, more_info_dialog)
        else:
            dialog = DialogConflictExpert(self, more_info_dialog)

        dialog.exec_()

        yes = dialog.result()

        if yes:
            if expert == 'YES':
                driver_values = self.getDriverValues(system,addr)
                driver.addConfiguration(driver_values)
                db = StormManager()
                db.store(driver_values)
            else:
                self._manager.saveValuesInIcepap(driver,driver.current_cfg.toList(), ignore_values=params_old_in_db)
            driver.signDriver()
            item.solveConflict()

        # BY NOW, UPDATE THE ICEPAP NAME MANUALLY
        current_cfg = driver.current_cfg
        label = str(driver.addr)+" "+current_cfg.getParameter(unicode("IPAPNAME"), True)
        item.changeLabel([label])

        icepap_system = item.itemData.icepap_system
        for driver in icepap_system.drivers:
            if driver.conflict != Conflict.NO_CONFLICT:
                return
        self.setStatusMessage("")
        

    def solveNewDriver(self, item):
        driver = item.itemData
        system = driver.icepapsystem_name
        addr = driver.addr

        widget, table = self.ui.pageiPapDriver.createTableWidget(["Parameter\nname","Value in\ndriver board"])
        more_info_dialog = QtGui.QDialog(self)
        more_info_dialog.resize(320,600)
        grid_layout = QtGui.QGridLayout()
        grid_layout.addWidget(widget)
        more_info_dialog.setModal(True)
        more_info_dialog.setLayout(grid_layout)

        driver_values = self.getDriverValues(system,addr)
        driver_values_list = driver_values.toList()
        if len(driver_values_list)>0:
            for param,driver_value in driver_values_list:
                row = table.rowCount()
                table.insertRow(row)

                param_item = QtGui.QTableWidgetItem()
                param_item.setText(param)
                table.setItem(row, 0, param_item)

                driver_item = QtGui.QTableWidgetItem()
                driver_item.setText(driver_value)
                table.setItem(row, 1, driver_item)
        
        expert = self._manager._ctrl_icepap.isExpertFlagSet(system, addr)
        expertFlag = (expert == 'YES')
        dialog = DialogNewDriver(self, more_info_dialog, expertFlag)
        dialog.exec_()

        answer = dialog.result()
        if answer not in ["DEFAULT","DRIVER"]:
            # Since version 1.23, cancelling new driver keeps the system as before
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
    
    def deleteDriverError(self, item):
        delete = MessageDialogs.showYesNoMessage(self, "Driver error", "Driver not present.\nRemove driver from DB?")
        if delete:
            icepap_system = item.getIcepapSystem()
            icepap_system.removeDriver(item.itemData.addr)
            item.solveConflict()
            self._tree_model.deleteItem(item)    
    
    def refreshTree(self):
        self.ui.pageiPapDriver.stopTesting()
        if not self.refreshTimer is None:
            self.refreshTimer.stop()
        self._manager.reset(self)
        self.initGUI()
        self.ui.stackedWidget.setCurrentIndex(0)

    def btnTreeRemove_on_click(self):
        selectmodel = self.ui.treeView.selectionModel()
        indexes = selectmodel.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            item = self._tree_model.item(index)
            icepap_system = item.getIcepapSystem()
            delete = MessageDialogs.showYesNoMessage(self, "Remove Icepap System", "Remove " + icepap_system.name + "?")
            if delete:
                self._tree_model.deleteIcepapSystem(icepap_system.name)
                self._manager.deleteIcepapSystem(icepap_system.name)
                self.clearLocationBar()
                self.refreshTimer.stop()
                

            
    def treeview_on_doubleclick(self, modelindex):
        self.locationsPrevious.extend(self.locationsNext)
        item = self._tree_model.item(modelindex)
        if item.role == IcepapTreeModel.DRIVER_WARNING:
            userContinues = self.solveConflict(item)
        elif item.role == IcepapTreeModel.DRIVER_NEW:
            solved = self.solveNewDriver(item)
            if not solved:
                return
        elif item.role == IcepapTreeModel.DRIVER_ERROR:
            self.deleteDriverError(item)
        elif item.role == IcepapTreeModel.SYSTEM_OFFLINE or item.role == IcepapTreeModel.SYSTEM_ERROR:
            self.scanIcepap(item.itemData)

        if item.role == IcepapTreeModel.DRIVER and item.itemData.conflict == Conflict.NO_CONFLICT:
            self.treeview_on_click(modelindex)
            
        
    def treeview_on_click(self, modelindex):
        self.locationsPrevious.extend(self.locationsNext)
        self.locationsNext =  []
        self.addToPrevious(self.currentLocation)
        self.treeSelectByIndex(modelindex)
            
    def treeSelectByLocation(self, location):
        self.currentLocation = location
        modelindex = self._tree_model.indexByLocation(location)
        if not modelindex is None:
            selection = QtGui.QItemSelection(modelindex, modelindex)
            selectmodel = self.ui.treeView.selectionModel()
            selectmodel.clear()
            selectmodel.select(selection, QtGui.QItemSelectionModel.Select)
            self.treeSelectByIndex(modelindex)
        
    
    def treeSelectByIndex(self, modelindex):
        item = self._tree_model.item(modelindex)
        self.currentLocation = item.location
        self.ui.actionExport.setEnabled(False)
        self.ui.actionImport.setEnabled(False)
        self.ui.actionHistoricCfg.setEnabled(False)
        self.ui.actionTemplates.setEnabled(False)
        self.ui.actionSaveConfig.setEnabled(False)
        self.ui.actionSetExpertFlag.setEnabled(False)
        self.ui.actionCopy.setEnabled(False)
        self.ui.actionPaste.setEnabled(False)
        self.ui.pageiPapDriver.stopTesting()
        if not self.refreshTimer is None:
            self.refreshTimer.stop()

        # BEFORE CHANGING THE TREE NODE, WE SHOULD CHECK IF THE LAST DRIVER
        # CAN BE SET BACK TO MODE 'OPER' OR NOT
        if self.ui.pageiPapDriver.checkSaveConfigPending():
            self.ui.actionSaveConfig.setEnabled(True)

        if item.role == IcepapTreeModel.DRIVER or item.role == IcepapTreeModel.DRIVER_CFG:

            # THE FILLDATA METHOD KNOWS IF THE BUTTON HAS TO BE ENABLED OR NOT
            self.ui.actionSaveConfig.setEnabled(False)
            self.ui.pageiPapDriver.fillData(item.itemData)
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.actionExport.setEnabled(True)
            self.ui.actionImport.setEnabled(True)
            self.ui.actionHistoricCfg.setEnabled(True)
            self.ui.actionTemplates.setEnabled(True)
            self.ui.actionSetExpertFlag.setEnabled(True)
            # ENABLE THE COPY & PASTE ACTIONS
            self.ui.actionCopy.setEnabled(True)
            self.ui.actionPaste.setEnabled(True)

        elif item.role == IcepapTreeModel.SYSTEM or item.role == IcepapTreeModel.SYSTEM_WARNING:
            self.ui.pageiPapSystem.fillData(item.itemData)      
            self.ui.stackedWidget.setCurrentIndex(1)
            QtCore.QObject.disconnect(self.refreshTimer,QtCore.SIGNAL("timeout()"),self.ui.pageiPapSystem.refresh)
            QtCore.QObject.connect(self.refreshTimer,QtCore.SIGNAL("timeout()"),self.ui.pageiPapSystem.refresh)
            self.refreshTimer.start(2000)
        elif item.role == IcepapTreeModel.CRATE:
            self.ui.pageiPapCrate.fillData(item.getIcepapSystem(), int(item.itemLabel[0].toString()))
            self.ui.stackedWidget.setCurrentIndex(2)
            QtCore.QObject.disconnect(self.refreshTimer,QtCore.SIGNAL("timeout()"),self.ui.pageiPapCrate.refresh)
            QtCore.QObject.connect(self.refreshTimer,QtCore.SIGNAL("timeout()"),self.ui.pageiPapCrate.refresh)
            self.refreshTimer.start(2000)
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

        self.expandIndex(modelindex)
           
    
    def actionGoPrevious(self):
        location = self.locationsPrevious.pop()
        self.addToNext(self.currentLocation)
        self.treeSelectByLocation(location)        
    
    def actionGoNext(self):
        location = self.locationsNext.pop()
        self.addToPrevious(self.currentLocation)
        self.treeSelectByLocation(location)
    
    def addToPrevious(self, location):
        if not location == "":
            self.locationsPrevious.append(location)
        self.checkGoPreviousActions()
    
    def addToNext(self, location):
        if not location == "":
            self.locationsNext.append(location)
        self.checkGoPreviousActions()
        
    def clearLocationBar(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.currentLocation = 0
        self.locationsPrevious = []
        self.locationsNext = []
        self.checkGoPreviousActions()

    def checkGoPreviousActions(self):
        if len(self.locationsPrevious) == 0:
            self.ui.actionGoPrevious.setEnabled(False)
        else:
            self.ui.actionGoPrevious.setEnabled(True)
        
        if len(self.locationsNext) == 0:
            self.ui.actionGoNext.setEnabled(False)
        else:
            self.ui.actionGoNext.setEnabled(True)
        
    def actionGoUp(self):
        selectmodel = self.ui.treeView.selectionModel()
        indexes = selectmodel.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            modelindex  = self._tree_model.parent(index)
            if modelindex.row() > -1:
                self.addToPrevious(self.currentLocation)
                selection = QtGui.QItemSelection(modelindex, modelindex)
                selectmodel = self.ui.treeView.selectionModel()
                selectmodel.clear()
                selectmodel.select(selection, QtGui.QItemSelectionModel.Select)
                self.treeSelectByIndex(modelindex)
            
        
    def actionRefresh(self):
        refresh = MessageDialogs.showYesNoMessage(self, "Init CMS", "Get all data from Database and lose changes?")
        if refresh:
            self.refreshTree()
                    
            
    def closeEvent(self, event):
        for child in self.children():
            if isinstance(child,QtGui.QDialog):
                child.done(0)
      
        self.refreshTimer.stop()
        self.ui.stackedWidget.setCurrentIndex(0)
        # Before closing, if any driver was in config mode, be sure if it can be set back to oper mode
        # or some signature is pending

        if self.ui.pageiPapDriver.checkSaveConfigPending():
            signList = self._manager.getDriversToSign()
            if MessageDialogs.showYesNoMessage(self, "Validate Drivers config", "There are driver configurations pending to be validated.\nAll changes may be lost\nValidate driver configs?."):
                for driver in signList:
                    driver.signDriver()
            else:
                for driver in signList:
                    self._manager.discardDriverChanges(driver)
                    self._manager.endConfiguringDriver(driver)

        

        if not self._manager.closeAllConnections():
            if MessageDialogs.showYesNoMessage(self, "Storage", "Error closing storage.\nDiscard changes and close?."):
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    
    def setStatusMessage(self, message):
        self.ui.statusbar.showMessage(message)
        
        
    def expandAll(self, location):
        parent = self._tree_model.indexByLocation(location)
        if parent:
            childs = self._tree_model.rowCount(parent)
            for row in range(childs):
                index = self._tree_model.index(row, 0, parent)
                self.expandIndex(index)
                item = self._tree_model.item(index)
                self.expandAll(item.location)
    
    def expandIndex(self, modelindex):
        index = self._tree_model.parent(modelindex)
        while(index.row() > -1):
            self.ui.treeView.expand(index)
            index = self._tree_model.parent(index)       
    
    def actionImport(self): 
        if self.ui.stackedWidget.currentIndex() == 3:
            self.ui.pageiPapDriver.doImport()
        
    def actionExport(self): 
        if self.ui.stackedWidget.currentIndex() == 3:
            self.ui.pageiPapDriver.doExport()
    
    def actionConsole(self):
        dlg = IcepapConsole(self)
        dlg.show()
        
    def actionPreferences(self):
        dlg = DialogPreferences(self)
        dlg.exec_()
        if dlg.StorageChanged:
            self._manager.reset(self)
            self.initGUI()
    
    def actionFimwareUpgrade(self):
        self.clearLocationBar()
        dlg = DialogIcepapProgram(self)
        dlg.exec_()

    def actionSaveConfig(self):
        QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            if self.ui.stackedWidget.currentIndex() == 0:
                #sign all drivers
                icepap_list = self._manager.getIcepapList()
                for icepap_name, icepap_system in icepap_list.items():
                    icepap_system.signSystem()
                    self._tree_model.emit(QtCore.SIGNAL('layoutChanged ()'))
            elif self.ui.stackedWidget.currentIndex() == 1:        
                #sign all icepap system
                self.ui.pageiPapSystem.icepap_system.signSystem()
                self._tree_model.emit(QtCore.SIGNAL('layoutChanged ()'))
            elif self.ui.stackedWidget.currentIndex() == 2:
                #sign all icepap crate
                self.ui.pageiPapCrate.icepap_system.signCrate(self.ui.pageiPapCrate.cratenr)
                self._tree_model.emit(QtCore.SIGNAL('layoutChanged ()'))
            elif self.ui.stackedWidget.currentIndex() == 3:
                #sign driver
                self.ui.pageiPapDriver.signDriver()
                self.ui.actionSaveConfig.setEnabled(False)

        except Exception,e:
            print "some exception while saving config:",e
            MessageDialogs.showInformationMessage(self, "Signature", "Some problems saving driver's configuration")
        QtGui.QApplication.instance().restoreOverrideCursor()

    
    def actionHistoricCfg(self):
        if self.ui.actionHistoricCfg.isChecked():
            self.ui.pageiPapDriver.showHistoricWidget()
        else:
            self.ui.pageiPapDriver.hideHistoricWidget()

    def actionTemplates(self):
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        # The master catalog file
        master_catalog_file = path+'/templates/catalog.xml'

        dlg = TemplatesCatalogWidget(master_catalog_file,self.ui.pageiPapDriver,self)
        dlg.show()
    
    def actionHelp(self):
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        webbrowser.open(path+'/doc/IcepapCMSUserManual.pdf')      
    
    def actionUser_Manual(self):
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        webbrowser.open(path+'/doc/IcePAP_UserManual.pdf')
    
    def actionHardware_Manual(self):
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        webbrowser.open(path+'/doc/IcePAP_HardwareManual.pdf')    
    

                
    def menuView_before_show(self):
        self.ui.actionToolbar.setChecked(not self.ui.toolBar.isHidden())
        self.ui.actionTree_Explorer.setChecked(not self.ui.dockTree.isHidden())
        
    def actionToolbar(self):
        self.ui.actionToolbar.setChecked(not self.ui.toolBar.isHidden())
        if not self.ui.actionToolbar.isChecked():
            self.ui.toolBar.show()
        else:
            self.ui.toolBar.close()
            
    def actionTreeExplorer(self):
        self.ui.actionTree_Explorer.setChecked(not self.ui.dockTree.isHidden())
        if not self.ui.actionTree_Explorer.isChecked():
            self.ui.dockTree.show()
        else:
            self.ui.dockTree.close()
  

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ipapcfg = IcepapCMS()
    ipapcfg.show()
    sys.exit(app.exec_())        
