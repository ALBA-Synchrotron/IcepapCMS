import sys, os, webbrowser
from PyQt4 import QtCore, QtGui, Qt
from ui_icepapcms import Ui_IcepapCMS
from qrc_icepapcms import *
from lib_icepapcms import MainManager, Conflict, ConfigManager, Timer
from icepap_treemodel import IcepapTreeModel
from pageipapdriver import PageiPapDriver
from pageipapcrate import PageiPapCrate
from pageipapsystem import PageiPapSystem
from dialogaddicepap import DialogAddIcepap
from dialogaddlocation import DialogAddLocation
from dialogdriverconflict import DialogDriverConflict
from dialogpreferences import DialogPreferences
from dialogipapprogram import DialogIcepapProgram
from ipapconsole import IcepapConsole
from messagedialogs import MessageDialogs
#from dialoghistoriccfg import DialogHistoricCfg
#from dialogtemplate import DialogTemplate


class IcepapCMS(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_IcepapCMS()
        self.ui.setupUi(self)
        self._config = ConfigManager()        
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
        QtCore.QObject.connect(self.ui.actionQuit,QtCore.SIGNAL("activated()"),self.close)
        QtCore.QObject.connect(self.ui.actionPreferences,QtCore.SIGNAL("activated()"),self.actionPreferences)
        QtCore.QObject.connect(self.ui.actionGoNext,QtCore.SIGNAL("activated()"),self.actionGoNext)
        QtCore.QObject.connect(self.ui.actionTree_Explorer,QtCore.SIGNAL("activated()"),self.actionTreeExplorer)
        QtCore.QObject.connect(self.ui.actionToolbar,QtCore.SIGNAL("activated()"),self.actionToolbar)                
        QtCore.QObject.connect(self.ui.actionGoPrevious,QtCore.SIGNAL("activated()"),self.actionGoPrevious)
        QtCore.QObject.connect(self.ui.actionGoUp,QtCore.SIGNAL("activated()"),self.actionGoUp)       
        QtCore.QObject.connect(self.ui.actionRefresh,QtCore.SIGNAL("activated()"),self.actionRefresh)         
        QtCore.QObject.connect(self.ui.actionExport,QtCore.SIGNAL("activated()"),self.actionExport)         
        QtCore.QObject.connect(self.ui.actionImport,QtCore.SIGNAL("activated()"),self.actionImport)         
        QtCore.QObject.connect(self.ui.actionConsole,QtCore.SIGNAL("activated()"),self.actionConsole)         
        QtCore.QObject.connect(self.ui.actionFirmwareUpgrade,QtCore.SIGNAL("activated()"),self.actionFimwareUpgrade)         
        QtCore.QObject.connect(self.ui.actionSignConfig,QtCore.SIGNAL("activated()"),self.actionSignConfig)
        QtCore.QObject.connect(self.ui.actionHistoricCfg,QtCore.SIGNAL("activated()"),self.actionHistoricCfg)
        QtCore.QObject.connect(self.ui.actionHelp,QtCore.SIGNAL("activated()"),self.actionHelp)
        QtCore.QObject.connect(self.ui.actionUser_manual,QtCore.SIGNAL("activated()"),self.actionUser_Manual)
        QtCore.QObject.connect(self.ui.actionHardware_manual,QtCore.SIGNAL("activated()"),self.actionHardware_Manual)
        QtCore.QObject.connect(self.ui.actionTemplates,QtCore.SIGNAL("activated()"),self.actionTemplates)
        QtCore.QObject.connect(self.ui.treeView,QtCore.SIGNAL("clicked(QModelIndex)"),self.treeview_on_click)
        QtCore.QObject.connect(self.ui.treeView,QtCore.SIGNAL("doubleClicked(QModelIndex)"),self.treeview_on_doubleclick)
        self.ui.treeView.setContextMenuPolicy(Qt.Qt.CustomContextMenu)
        self.connect(self.ui.treeView, 
                     QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self.__contextMenu)
        QtCore.QObject.connect(self.ui.txtLocation,QtCore.SIGNAL("returnPressed()"),self.txtLocation_on_return)
        QtCore.QObject.connect(self.ui.btnTreeAdd,QtCore.SIGNAL("clicked()"),self.btnTreeAdd_on_click)
        QtCore.QObject.connect(self.ui.btnTreeRemove,QtCore.SIGNAL("clicked()"),self.btnTreeRemove_on_click)
        QtCore.QObject.connect(self.ui.actionAddIcepap ,QtCore.SIGNAL("activated()"),self.btnTreeAdd_on_click)         
        QtCore.QObject.connect(self.ui.actionDeleteIcepap,QtCore.SIGNAL("activated()"),self.btnTreeRemove_on_click)
        #QtCore.QObject.connect(self.ui.btnTreeRefresh,QtCore.SIGNAL("clicked()"),self.btnTreeRefresh_on_click)
        QtCore.QObject.connect(self.ui.menuView,QtCore.SIGNAL("aboutToShow()"),self.menuView_before_show)
        QtCore.QObject.connect(self.ui.cbLocation,QtCore.SIGNAL("activated  (const QString&)"),self.locationChanged)
        QtCore.QObject.connect(self.ui.btnAddLocation,QtCore.SIGNAL("clicked()"),self.addLocation)
        QtCore.QObject.connect(self.ui.btnDeleteLocation,QtCore.SIGNAL("clicked()"),self.deleteLocation)
        QtCore.QObject.connect(self.ui.actionAddLocation,QtCore.SIGNAL("activated()"),self.addLocation)         
        QtCore.QObject.connect(self.ui.actionDeleteLocation,QtCore.SIGNAL("activated()"),self.deleteLocation)
        
    def initGUI(self):
        self._manager = MainManager(self)
        if not self._manager.dbStatusOK:
            MessageDialogs.showErrorMessage(self, "Storage", "Error accessing database.\nCheck storage preferences.")
        
        #self.buildTree()
        
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
        self.ui.actionTemplates.setEnabled(False)
        self.ui.treeView.setItemsExpandable(True)        
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.txtLocation.setText("")
     
#    def buildTree(self):
#        expand_system = self.performSystemScan()
#        self._tree_model = IcepapTreeModel(self._manager.IcepapSystemList)
#        self.ui.treeView.setModel(self._tree_model)
#        for name in expand_system.keys():
#            self.expandAll(name)


    def addLocation(self):
        dlg = DialogAddLocation(self)
        dlg.exec_()
        if dlg.result():
            location = dlg.getData()
            if self._manager.addLocation(location):
                self.ui.cbLocation.addItem(location)
                self.ui.cbLocation.setCurrentIndex(self.ui.cbLocation.findText(location, QtCore.Qt.MatchFixedString))
                self.locationChanged (location) 
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
        #self.ui.treeView.reset()               
        for location_name in self._manager.locationList.keys():
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
    
    def buildInitialTree(self):        
        self._tree_model = IcepapTreeModel(self._manager.IcepapSystemList, True)
        self.ui.treeView.setModel(self._tree_model)
        self.context_menu_item = None    
    
    def __contextMenu(self, point):
        modelindex = self.ui.treeView.indexAt(point)
        item = self._tree_model.item(modelindex)                
        if item:
            actions = [
            """self.menu.addAction("Sign driver configuration", self.actionSignConfig)""",
            """self.menu.addAction("Solve driver configuration conflict", self.contextSolveConflict)""",
            """self.menu.addAction("Delete driver not present", self.contextDeleteDriverError)""",
            """self.menu.addAction("Driver moved. Import configurations", self.contextSolveDriverMoved)""",
            """self.menu.addSeparator()""",
            """self.menu.addAction("Start Icepap systen configuration", self.contextIcepapStart)""",
            """self.menu.addAction("Rescan Icepap systen", self.contextIcepapStart)""",
            """self.menu.addAction("Finish Icepap systen configuration", self.contextIcepapStop)""",
            """self.menu.addSeparator()""",
            """self.menu.addAction("Edit Icepap systen information", self.contextEditIcepap)""",
            """self.menu.addAction("Delete Icepap systen configuration", self.btnTreeRemove_on_click)"""  
            ]
            self.menu= Qt.QMenu(self)
            font = QtGui.QFont()
            font.setPointSize(8)
            self.menu.setFont(font)                    
            self.context_menu_item = item
            shown_actions = []            
            if item.role == IcepapTreeModel.SYSTEM_OFFLINE:
                shown_actions = [5,8,9,10]
            if item.role == IcepapTreeModel.DRIVER or item.role == IcepapTreeModel.DRIVER_NEW:
                shown_actions = [6,7,8,9,10]
            elif item.role == IcepapTreeModel.DRIVER_CFG:
                shown_actions = [0,4,6,7,8,9,10]
            elif item.role == IcepapTreeModel.DRIVER_ERROR:
                shown_actions = [2,4,6,7,8,9,10]
            elif item.role == IcepapTreeModel.DRIVER_WARNING:
                shown_actions = [1,4,6,7,8,9,10]                    
            elif item.role == IcepapTreeModel.DRIVER_MOVED:
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
        
    def contextSolveDriverMoved(self):
        if self.context_menu_item:
            item = self.context_menu_item
            self.solveDriverMoved(item)       
        self.context_menu_item = None
       
    def btnTreeAdd_on_click(self):
        location = self.ui.cbLocation.currentText()
        dlg = DialogAddIcepap(self, location)
        dlg.exec_()
        if dlg.result():
            data = dlg.getData()
            self.ui.cbLocation.setCurrentIndex(self.ui.cbLocation.findText(data[3], QtCore.Qt.MatchFixedString))
            icepap_system = self._manager.addIcepapSystem(data[0], data[1], data[2])
            if icepap_system is None:
                MessageDialogs.showErrorMessage(self, "Add Icepap", "Error adding Icepap")
            else:
                                
                self._tree_model.addIcepapSysten(icepap_system.name, icepap_system, False)
                self.expandAll(icepap_system.name)
    
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
                      
#    def performSystemScan(self):
#        icepap_list = self._manager.getIcepapList()
#        self.current_icepap = 0
#        expand_system = {}
#        conflicts_list = []
#        for icepap_name, icepap_system in icepap_list.items():
#            self.setStatusMessage("Scanning ... " + icepap_name)
#            expand_system[icepap_system.name] = icepap_system            
#            conflicts_list.extend(self._manager.scanIcepap(icepap_system))
#        
#        if len(conflicts_list) > 0:
#            self.setStatusMessage("Configuration conflics found.")
#            for conflict in conflicts_list:
#                icepap_system = conflict[1]
#                #expand_system[icepap_system.name] = icepap_system
#                if conflict[0] == Conflict.NO_CONNECTION:
#                    icepap_system.setConflict(conflict[0])
#                    self.setStatusMessage(icepap_system.name + ": Connection Error")
#                else:
#                    if not conflict[2] is None:
#                        self.setStatusMessage("Configuration conflics found.")
#                        driver = icepap_system.getDriver(conflict[2])
#                        driver.setConflict(conflict[0])
#        else:
#            self.setStatusMessage("Scanning complete!. No conflicts found")
#        return expand_system
    
    def checkIcepapConnection(self):
        """ this function checks the icepap connection, notifying the user for
        losing or getting connection """
        
        icepap_systems_changed = self._manager.checkIcepapSystems()
        for icepap_system in icepap_systems_changed:
            print icepap_system
            #if icepap_system.conflict != Conflict.NO_CONFLICT:
            self.scanIcepap(icepap_system)
            

    def stopIcepap(self, icepap_system):
        self.ui.pageiPapDriver.stopTesting()
        if not self.refreshTimer is None:
            self.refreshTimer.stop()
        self.ui.txtLocation.setText("")
        self.ui.stackedWidget.setCurrentIndex(0)
        self._manager.stopIcepap(icepap_system)
        self._tree_model.updateIcepapSystem(icepap_system, True)
                       
    def scanIcepap(self, icepap_system):
        """This function scans and Icepap. This means comparing 
        the database configurations and the ones in the hardware """
        self.setStatusMessage("Scanning ...")
        conflicts_list = []
        conflicts_list.extend(self._manager.scanIcepap(icepap_system))
        if len(conflicts_list) > 0:
            self.setStatusMessage("Configuration conflics found.")
            for conflict in conflicts_list:
                icepap_system = conflict[1]
                #expand_system[icepap_system.name] = icepap_system
                if conflict[0] == Conflict.NO_CONNECTION:
                    icepap_system.setConflict(conflict[0])
                    self.setStatusMessage(icepap_system.name + ": Connection Error")
                else:
                    if not conflict[2] is None:
                        self.setStatusMessage("Configuration conflics found.")
                        driver = icepap_system.getDriver(conflict[2])
                        driver.setConflict(conflict[0])
        else:
            self.setStatusMessage("Scanning complete!. No conflicts found")
        self._tree_model.updateIcepapSystem(icepap_system)
        self.expandAll(icepap_system.name)
          
    def solveConflict(self, item):
        dlg = DialogDriverConflict(self, item.itemData)
        dlg.exec_()
        if dlg.result():
            item.solveConflict()
    
    def solveDriverMoved(self, item):
        moved_sys = self._manager.importMovedDriver(item.itemData)
        imported_sys = item.itemData.icepap_system
        if moved_sys != imported_sys:
            self.scanIcepap(moved_sys)         
        self.scanIcepap(imported_sys)
    
    def deleteDriverError(self, item):
        moved_sys = self._manager.importMovedDriver(item.itemData, True)
        or_sys = item.itemData.icepap_system
        if moved_sys != or_sys:
            self.scanIcepap(moved_sys)         
        self.scanIcepap(or_sys)
#        delete = MessageDialogs.showYesNoMessage(self, "Driver error", "Driver not present.\nRemove driver from DB?")
#        if delete:
#            icepap_system = item.getIcepapSystem()
#            icepap_system.removeDriver(item.itemData.addr)
#            item.solveConflict()
#            self._tree_model.deleteItem(item)    
    
    def refreshTree(self):
        self.ui.pageiPapDriver.stopTesting()
        if not self.refreshTimer is None:
            self.refreshTimer.stop()
        self.ui.txtLocation.setText("")
        self._manager.reset(self)
        #if not self._manager.dbStatusOK:
        #    MessageDialogs.showErrorMessage(self, "Storage", "Error accessing storage.\nCheck storage preferences.")
        self.initGUI()        
        #self.buildTree()
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
            self.solveConflict(item)
        elif item.role == IcepapTreeModel.DRIVER_MOVED:
            self.solveDriverMoved(item)
        elif item.role == IcepapTreeModel.DRIVER_ERROR:
            self.deleteDriverError(item)
        elif item.role == IcepapTreeModel.SYSTEM_OFFLINE or item.role == IcepapTreeModel.SYSTEM_ERROR:
            self.scanIcepap(item.itemData)
            
        
    def treeview_on_click(self, modelindex):
        self.locationsPrevious.extend(self.locationsNext)
        self.locationsNext =  []
        self.addToPrevious(self.currentLocation)
        self.treeSelectByIndex(modelindex)
            
    def txtLocation_on_return(self):
        self.locationsPrevious.extend(self.locationsNext)
        self.locationsNext =  []
        self.addToPrevious(self.currentLocation)
        location = str(self.ui.txtLocation.text())
        location = location.rstrip('/')
        self.treeSelectByLocation(location)
     
    
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
        self.ui.txtLocation.setText(item.location) 
        self.currentLocation = item.location
        self.ui.actionExport.setEnabled(False)
        self.ui.actionImport.setEnabled(False)
        self.ui.actionHistoricCfg.setEnabled(False)
        self.ui.actionTemplates.setEnabled(False)
        self.ui.actionSignConfig.setEnabled(True)
        self.ui.pageiPapDriver.stopTesting()
        if not self.refreshTimer is None:
            self.refreshTimer.stop()
        if item.role == IcepapTreeModel.DRIVER or item.role == IcepapTreeModel.DRIVER_NEW or item.role == IcepapTreeModel.DRIVER_CFG:
            self.ui.pageiPapDriver.fillData(item.itemData)
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.actionExport.setEnabled(True)
            self.ui.actionImport.setEnabled(True)
            self.ui.actionHistoricCfg.setEnabled(True)
            self.ui.actionTemplates.setEnabled(True)
            #if self.historicDlg.isVisible():
            #    self.historicDlg.fillDriverData(item.itemData)
            if item.role == IcepapTreeModel.DRIVER_CFG:
                self.ui.actionSignConfig.setEnabled(True)
            else:
                self.ui.actionSignConfig.setEnabled(False)
        elif item.role == IcepapTreeModel.SYSTEM or item.role == IcepapTreeModel.SYSTEM_WARNING:
            self.ui.pageiPapSystem.fillData(item.itemData)      
            self.ui.stackedWidget.setCurrentIndex(1)
            QtCore.QObject.connect(self.refreshTimer,QtCore.SIGNAL("timeout()"),self.ui.pageiPapSystem.refresh)
            self.refreshTimer.start(2000)
        elif item.role == IcepapTreeModel.CRATE:
            self.ui.pageiPapCrate.fillData(item.getIcepapSystem(), int(item.itemLabel[0].toString()))
            self.ui.stackedWidget.setCurrentIndex(2)
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
        self.ui.txtLocation.setText("") 
    
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
        self.refreshTimer.stop()
        self.ui.stackedWidget.setCurrentIndex(0)
        signList = self._manager.getDriversToSign()
        if len(signList) > 0:
            if MessageDialogs.showYesNoMessage(self, "Sign Drivers", "The are drivers pending to be signed.\nAll changes will be lost\nSign drivers?."):
                for driver in signList:
                    driver.signDriver()
            else:
                for driver in signList:
                    self._manager.discardDriverChanges(driver)
        

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
        dlg.exec_()
        
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
    
    def addDriverToSign(self, driver):
        location = str(self.ui.txtLocation.text())
        location = location.rstrip('/')
        self._tree_model.changeItemIcon(location, IcepapTreeModel.DRIVER_CFG)
        #driver.conflict = Conflict.DRIVER_CFG
        self.ui.actionSignConfig.setEnabled(True)
         
    def actionSignConfig(self):
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
            location = str(self.ui.txtLocation.text())
            location = location.rstrip('/')
            self._tree_model.changeItemIcon(location, IcepapTreeModel.DRIVER)
            self.ui.actionSignConfig.setEnabled(False)
        MessageDialogs.showInformationMessage(self, "Signature", "Driver/s signed succesfully")
    
    def actionHistoricCfg(self):
        if self.ui.actionHistoricCfg.isChecked():
            self.ui.pageiPapDriver.showHistoricWidget()
        else:
            self.ui.pageiPapDriver.hideHistoricWidget()
            
    def actionTemplates(self):
        pass
    
    def actionHelp(self):
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        webbrowser.open(path+'/doc/IcepapCMSUserManual.pdf')      
    
    def actionUser_Manual(self):
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        webbrowser.open(path+'/doc/IcePAP_UserManual_working.pdf')
    
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
