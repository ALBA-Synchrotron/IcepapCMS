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


from singleton import Singleton
#from icepapsystem import *
#from icepapdriver import *
#from icepapcontroller import IcepapController
#from icepapdrivertemplate import IcepapDriverTemplate
#from zodbmanager import ZODBManager
from PyQt4 import QtCore
from PyQt4 import QtGui

#from conflict import Conflict
from pyIcePAP import *

from ..ui_icepapcms.messagedialogs import MessageDialogs
import sys
from stormmanager import StormManager
from configmanager import ConfigManager

class MainManager(Singleton):

    def __init__(self, form = None):
        pass

    def init(self, *args):
        self.IcepapSystemList = {}
        
        self._ctrl_icepap = IcepapController()
        self._db = StormManager()
        
        self.dbStatusOK = self._db.dbOK        

        self._form = args[0]
        self.locationList = self._db.getAllLocations()
        self.location = None
        self.IcepapSystemList = {}

    
    def addLocation(self, location_name):
        """ Adds a location in the database """
        try:
            if self.locationList.has_key(unicode(location_name)):
                return False
            location = Location(unicode(location_name))
            self._db.store(location)
            self._db.commitTransaction()
            self.locationList[unicode(location_name)] = location
            return True
        except:
            print "addLocation:", sys.exc_info()
            return False
        
        
    def deleteLocation(self, location_name):
        """ Deletes a location in the database """
        location = self.locationList[unicode(location_name)]
        self._db.deleteLocation(location) 
        del self.locationList[unicode(location_name)]
        self.IcepapSystemList = {}
        
    def changeLocation(self, location):
        """ Close the connection from all the icepaps in one location.
        And gets all the icepaps from the selected location """
        
        self.location = self.locationList[unicode(location)]
        self._ctrl_icepap.closeAllConnections()
        self.IcepapSystemList = self._db.getLocationIcepapSystem(unicode(location))
        
    def reset(self, form):
        self._ctrl_icepap.reset()
        self._db.reset()
        self.dbStatusOK = self._db.dbOK
        self.location = None
        self.IcepapSystemList = {}
        self._form = form
        self.locationList = self._db.getAllLocations()
        
        
    def addIcepapSystem(self, host, port, description = None):
        """ Adds a new Icepap in the current location, 
        the parameters are the hostname, port and description, 
        this function checks if the icepap is available, the gets all the configuration 
        of all the driver and stores all these information in the database """
        QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            icepap_name = host
            """ *TO-DO STORM review"""
            if self.IcepapSystemList.has_key(icepap_name):
                return None            
            location = self.location.name
            try:
                icepap_system = IcepapSystem(icepap_name, host, port, location, description)

                # JUST IN CASE A USER WANTS TO RE-ADD A SYSTEM !?!?!?!?
                # A QUANTUM PROBABILITY TO BE ON TWO LOCATIONS AT THE SAME TIME... :-D
                db_icepap_system = self._db.getIcepapSystem(icepap_name)
                if db_icepap_system != None:
                    MessageDialogs.showErrorMessage(self._form, "Adding Icepap System error", "The icepap system is already in location: '%s'" % (db_icepap_system.location_name))
                    QtGui.QApplication.instance().restoreOverrideCursor()
                    return None
            
                self._ctrl_icepap.openConnection(icepap_name, host, port)
                driver_list = self._ctrl_icepap.scanIcepapSystem(icepap_name)
                self._db.addIcepapSystem(icepap_system)
                self.IcepapSystemList[icepap_name] = icepap_system
                self.location.addSystem(icepap_system)
                for driver in driver_list.values():
                    icepap_system.addDriver(driver)
                    self._db.store(driver)
                self._db.commitTransaction()
                QtGui.QApplication.instance().restoreOverrideCursor()
                if len(driver_list) == 0:
                    MessageDialogs.showWarningMessage(None, "Scanning Icepap Warning", "The icepap system '"+icepap_name+"' has ZERO drivers.\nPlease make sure that the CAN BUS TERMINATOR is connected.")
                return icepap_system
            except IcePAPException,ie:
                MessageDialogs.showErrorMessage(None, "Scanning Icepap Error", "Could not scan the '"+icepap_name+"' Icepap System.\nPlease make sure that the system '"+(icepap_name)+"' is in your subnetwork.\nException:\n\t"+str(ie))
            except Exception,e:
                print "Unknown exception:",e
            
        except:
            print "addIcepapSystem:", sys.exc_info()[1]
        QtGui.QApplication.instance().restoreOverrideCursor()
        return None

        
    def deleteIcepapSystem(self, icepap_name):
        """ deletes and Icepap in the database """
        del self.IcepapSystemList[icepap_name]
        self.location.deleteSystem(icepap_name)
        #self._db.deleteIcepapSystem(self.IcepapSystemList[icepap_name])        
        
           
    def closeAllConnections(self):
        """ Close all the openned connections to the icepaps """
        self._ctrl_icepap.closeAllConnections()
        return self._db.closeDB()
            
    
    def getIcepapSystem(self, icepap_name):
        if self.IcepapSystemList.has_key(icepap_name):
            return self.IcepapSystemList[icepap_name]
        return None
    

    
    def checkIcepapSystems(self):
        """ Checks if the icepaps for the current location are available over the
        network or not. These function is used to perform automatic reconnection """
        
        changed_list = []
        for icepap_system in self.IcepapSystemList.values():            
            connected = self._ctrl_icepap.checkIcepapStatus(icepap_system.name)

            if connected:                
                if icepap_system.conflict == Conflict.NO_CONNECTION:
                    icepap_system.conflict = Conflict.NO_CONFLICT
                    changed_list.append(icepap_system)
            else:
                if icepap_system.conflict != Conflict.NO_CONFLICT and icepap_system.conflict != Conflict.NO_CONNECTION:
                    icepap_system.conflict = Conflict.NO_CONNECTION
                    changed_list.append(icepap_system)
        return changed_list
            
    def stopIcepap(self, icepap_system):    
        """ Close the connection to an icepap. And commits all the changes in the database """
        try:
            self._ctrl_icepap.closeConnection(icepap_system.name)
            self._db.commitTransaction()
        except IcePAPException,error:
            MessageDialogs.showErrorMessage(self._form, "Stop Icepap error", "%s Connection error:%s" % (icepap_name,error.msg))
        except:
            print "mainmanager:stopIcepap:Unexpected error:", sys.exc_info()   
                
    def scanIcepap(self, icepap_system):
        """ Searches for configuration conflicts.
        Returns the conflicts list. That is composed by elements of [Conflict code, icepap_system, icepap_driver_addr] """
        QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        icepap_name = icepap_system.name
        conflictsList = []
        try:
            if self._ctrl_icepap.openConnection(icepap_name, icepap_system.host, icepap_system.port):
                driver_list = self._ctrl_icepap.scanIcepapSystem(icepap_name,True)
                conflictsList = icepap_system.compareDriverList(driver_list)
            else:
                conflictsList.append([Conflict.NO_CONNECTION, icepap_system, 0])
        except IcePAPException,error:
            MessageDialogs.showErrorMessage(None, "Scanning Icepap Error", "Could not scan the '"+icepap_name+"' Icepap System.\nPlease make sure that the system '"+(icepap_name)+"' is in your subnetwork.\nException:"+str(error))
        except:
            print "mainmanager:scanIcepap:Unexpected error:", sys.exc_info()
            conflictsList.append([Conflict.NO_CONNECTION, icepap_system, 0])

        QtGui.QApplication.instance().restoreOverrideCursor()

        return conflictsList


    def checkFirmwareVersions(self, icepap_system):
        config = ConfigManager()
        if config._options.skipversioncheck == True:
            print "Firmware versions are not checked."
            return
        try:
            icepap_name = icepap_system.name
            master_version = self._ctrl_icepap.iPaps[icepap_name].getVersion(0,"DRIVER")
            master_version = str(master_version)
            mismatched_drivers = []
            for driver in icepap_system.getDrivers():
                #####################################################################
                driver_version = self._ctrl_icepap.iPaps[icepap_name].getVersion(driver.addr,"DRIVER")
                # If the driver has been temporary removed, the error should
                if driver_version.count("ERROR") > 0:
                    driver_version = master_version
                if master_version != driver_version:
                    mismatched_drivers.append((driver.addr,str(driver_version)))
            
            if len(mismatched_drivers) > 0:
                msg = "Some drivers do not have the MASTER's firmware version (%s):\n" % (master_version)
                for driver,version in mismatched_drivers:
                    msg = msg + "driver %d: %s\n" % (driver,version)
                saved_version = self._ctrl_icepap.iPaps[icepap_name].getVersionSaved()
                msg = msg + "Board saved version: %s\n" % (saved_version)
                msg = msg + "Would you like to upgrade these drivers?\n"
                upgrade = MessageDialogs.showYesNoMessage(self._form, "Firmware mismatch", msg)
                if upgrade:
                    progress_dialog = QtGui.QProgressDialog(self._form)
                    progress_dialog.setLabel(QtGui.QLabel("Icepap: %s\nUpgrading drivers' firmware to %s" % (icepap_name,saved_version)))
                    progress_dialog.setCancelButton(None)
                    progress_dialog.setMaximum(100)
                    upgrading = self._ctrl_icepap.upgradeDrivers(icepap_name,progress_dialog)
                    if not upgrading:
                        progress_dialog.cancel()
                        msg = "Sorry, problems found while upgrading. Please try it manually :-("
                        MessageDialogs.showErrorMessage(None,"Firmware upgrade error",msg)
        except:
            pass


    def importMovedDriver(self, icepap_driver, from_to = False):
        """ function to import the information from a moved driver, to avoid losing historic cfgs"""
        id = icepap_driver.current_cfg.getParameter("ID", True)
        got_driver = self._db.existsDriver(icepap_driver, id)
        if from_to:
            if got_driver:
                src_driver = icepap_driver
                dst_driver = got_driver                
            else:
                delete = MessageDialogs.showYesNoMessage(self._form, "Driver error", "Driver not present.\nRemove driver from DB?")
                if delete:
                    icepap_driver.icepap_system.removeDriver(icepap_driver.addr)
                return None
        else:
            src_driver = got_driver
            dst_driver = icepap_driver  
                      
        move = MessageDialogs.showYesNoMessage(self._form, "Import moved driver", "Import all historic configurations from %s:axis %d to %s:axis %d" % (src_driver.icepapsystem_name, src_driver.addr, dst_driver.icepapsystem_name, dst_driver.addr))
        src_sys = src_driver.icepap_system
        if move:
            for cfg in src_driver.historic_cfgs:
                cfg.setDriver(dst_driver)
                dst_driver.historic_cfgs.add(cfg)
        src_driver.icepap_system.removeDriver(src_driver.addr)     
        return src_sys
        

        
    def getDriversToSign(self):
        """ Gets the all drivers to be signed """
        signList = []
        for icepap_system in self.IcepapSystemList.values():
            """ TO-DO STORM review"""
            for driver in icepap_system.getDrivers():
                if driver.mode == IcepapMode.CONFIG:
                    signList.append(driver)
        return signList
         
        
    
    def getDriverConfiguration(self, icepap_name, addr):
        try:
            config = self._ctrl_icepap.getDriverConfiguration(icepap_name, addr)
            return config
        
        except:
            MessageDialogs.showErrorMessage(self._form, "GetDriverConfiguration Icepap error", "%s Connection error" % icepap_name)
            #self._form.checkIcepapConnection()
            
    
    def getDriverStatus(self, icepap_name, addr):
        """ Driver Status used in the System and crate view
            Returns [status register, power status, current ]"""
        icepap_system = self.getIcepapSystem(icepap_name)
        if icepap_system == None:
            return (-1,False,-1)
        try:
            driver = icepap_system.getDriver(addr)
            if driver is None:
                return (-1,False,-1)
            if driver.conflict == Conflict.DRIVER_NOT_PRESENT or driver.conflict == Conflict.NO_CONNECTION:
                #print "OUPS! THIS DRIVER SHOULD NOT BE SCANNED"
                return (-1,False,-1)
            status = self._ctrl_icepap.getDriverStatus(icepap_name, addr)
            return status
        except IcePAPException, error:
            MessageDialogs.showErrorMessage(self._form, "GetDriverStatus Icepap error", "%s,%d Connection timeout" % (icepap_name,addr))
            self._form.refreshTree()
            return (-1, False, -1) 
        except Exception,e:
            MessageDialogs.showWarningMessage(self._form, "GetDriverStatus error", "Connection error")
            self._form.checkIcepapConnection()
            #print "Unexpected error:", sys.exc_info()
            #print "error getting status : %s %d" % (icepap_name,addr) 
            return (-1, False, -1)
    
    def getDriverTestStatus(self, icepap_name, addr, pos_sel, enc_sel):
        """ Driver Status used in the System and crate view
            Returns [status register, power state, [position register value, encoder register value]"""
        try:
            return self._ctrl_icepap.getDriverTestStatus(icepap_name, addr, pos_sel, enc_sel)
        except IcePAPException, error:
            MessageDialogs.showErrorMessage(self._form, "GetDriverTestStatus Icepap error", "%s Connection error:%s" % (icepap_name,error.msg))
            self._form.refreshTree() 
            return (-1,-1, [-1,-1])        
        except Exception,e:
            print "mainmanager:getDriverTestStatus:Unexpected error while getting driver test status.\n",str(e)
            #print "mainmanager:getDriverTestStatus:Unexpected error:", sys.exc_info()
            return (-1,-1, [-1,-1])
            
    def readIcepapParameters(self, icepap_name, addr, par_list):
        """ Gets from adriver the values of the parameters in par_list """
        try:
            return self._ctrl_icepap.readIcepapParameters(icepap_name, addr, par_list)
        except IcePAPException, error:
            MessageDialogs.showErrorMessage(self._form, "ReadIcepapParamenters Icepap error", "%s Connection error:%s" % (icepap_name,error.msg))
        except:
            print "mainmanager:readIcepapParameters:Unexpected error:", sys.exc_info()
            print "error in : %s %d" % (icepap_name,addr)
            return []
        
    
    def writeIcepapParameters(self, icepap_name, addr, par_var_list):
        """ Writes to a driver the values in the par_var_list """
        try:
            self._ctrl_icepap.writeIcepapParameters(icepap_name, addr, par_var_list)
        except:
            pass
    
            
    def getDriverMotionValues(self, icepap_name, addr):
        """ Returns speed and acceleration of a driver """
        try:
            return self._ctrl_icepap.getDriverMotionValues(icepap_name, addr)
        except:
            return (-1,-1)
            
    def setDriverMotionValues(self, icepap_name, addr, values):
        """ Sets speed and acceleration to a driver """
        try:
            return self._ctrl_icepap.setDriverMotionValues(icepap_name, addr, values)
        except:
            MessageDialogs.showWarningMessage(self._form, "SetDriverMotionValues Icepap error", "Connection error")
    
    def setDriverPosition(self, icepap_name, addr, pos_sel, position):
        return self._ctrl_icepap.setDriverPosition(icepap_name, addr, pos_sel, position)
    
    def setDriverEncoder(self, icepap_name, addr, pos_sel, position):
        return self._ctrl_icepap.setDriverEncoder(icepap_name, addr, pos_sel, position)
    
    def moveDriver(self, icepap_name, addr, steps):
        try:
            self._ctrl_icepap.moveDriver(icepap_name, addr, steps)
        except IcePAPException,error:
            MessageDialogs.showErrorMessage(self._form, "MoveDriver Icepap error", "%s Connection error:%s" % (icepap_name,error.msg))
        except:
            print "mainmanager:moveDriver:Unexpected error:", sys.exc_info()
            MessageDialogs.showWarningMessage(self._form, "MoveDriver error", "Connection error")
            
    def moveDriverAbsolute(self, icepap_name, addr, position):
        try:
            self._ctrl_icepap.moveDriverAbsolute(icepap_name, addr, position)
        except IcePAPException,error:
            MessageDialogs.showErrorMessage(self._form, "MoveDriverAbsolute Icepap error", "%s Connection error:%s" % (icepap_name,error.msg))
        except:
            print "mainmanager:moveDriverAbsolute:Unexpected error:", sys.exc_info()
            MessageDialogs.showWarningMessage(self._form, "MoveDriverAbsolute error", "Connection error")
    
    def stopDriver(self, icepap_name, addr):
        try:
            self._ctrl_icepap.stopDriver(icepap_name, addr)
        except:
            MessageDialogs.showWarningMessage(self._form, "StopDriver Icepap error", "Connection error")

    def blinkDriver(self, icepap_name, driver_addr,secs):
        self._ctrl_icepap.blinkDriver(icepap_name, driver_addr,secs)


    def jogDriver(self, icepap_name, addr, speed):
        self._ctrl_icepap.jogDriver(icepap_name, addr, speed)
            
    
    def enableDriver(self, icepap_name, driver_addr):
        self._ctrl_icepap.enableDriver(icepap_name, driver_addr)

    def disableDriver(self, icepap_name, driver_addr):
        self._ctrl_icepap.disableDriver(icepap_name, driver_addr)

    def saveValuesInIcepap(self, icepap_driver, new_values, expertFlag = False, ignore_values=[]):
        """ Stores the new configuration in the icepap, and sets the mode of the driver to CONFIG """
        for param,db_value in ignore_values:
            new_values.remove((param,db_value))
        new_cfg = self._ctrl_icepap.setDriverConfiguration(icepap_driver.icepapsystem_name, icepap_driver.addr, new_values, expertFlag = expertFlag)
        if new_cfg is None:
            #self._form.checkIcepapConnection()
            return False
        else:
            icepap_driver.mode = unicode(IcepapMode.CONFIG)
            icepap_driver.addConfiguration(new_cfg)
            return True

    def startConfiguringDriver(self, icepap_driver):
        return self._ctrl_icepap.startConfiguringDriver(icepap_driver.icepapsystem_name, icepap_driver)

    def endConfiguringDriver(self, icepap_driver):
        self._ctrl_icepap.endConfiguringDriver(icepap_driver.icepapsystem_name, icepap_driver)
        
    def discardDriverChanges(self, icepap_driver):
        icepap_driver.setStartupCfg()
        self._ctrl_icepap.setDriverConfiguration(icepap_driver.icepapsystem_name, icepap_driver.addr, icepap_driver.current_cfg.toList())

        #self._ctrl_icepap.discardDriverCfg(icepap_driver.icepapsystem_name, icepap_driver.addr)
        pass
        
        
    def undoDriverConfiguration(self, icepap_driver):
        undo_cfg = icepap_driver.getUndoList()
        new_cfg = self._ctrl_icepap.setDriverConfiguration(icepap_driver.icepapsystem_name, icepap_driver.addr, undo_cfg.toList())
        if new_cfg is None:
            MessageDialogs.showWarningMessage(self._form, "undoDriverConfig error", "Connection error")
            #self._form.checkIcepapConnection()
        else:
            icepap_driver.undo(new_cfg)
            return True
    
    def getIcepapList(self):
        return self.IcepapSystemList
    
    def getDriverTemplateList(self):
        return self._zodb.getAllDriverTemplate()
    
    def saveDriverTemplate(self, name, desc, cfg):
        self._zodb.addDriverTemplate(IcepapDriverTemplate(name, desc, cfg))
    
    def deleteDriverTemplate(self, name):
        self._zodb.deleteDriverTemplate(name)

    def configDriverToDefaults(self,icepap_driver):
        icepap_name = icepap_driver.icepapsystem_name
        addr = icepap_driver.addr
        self._ctrl_icepap.configDriverToDefaults(icepap_name, addr)

    def updateDriverConfig(self,icepap_driver):
        icepap_name = icepap_driver.icepapsystem_name
        addr = icepap_driver.addr
        driver_cfg = self.getDriverConfiguration(icepap_name, addr)
        icepap_driver.addConfiguration(driver_cfg)


from icepapsystem import IcepapSystem, Location
from icepapdriver import IcepapDriver
from conflict import *
from icepapcontroller import *    




    

