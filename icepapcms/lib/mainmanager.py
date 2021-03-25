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

from .singleton import Singleton
from PyQt5 import QtCore, QtGui, QtWidgets
from icepap import Mode
import logging

from ..gui.messagedialogs import MessageDialogs
from .stormmanager import StormManager
from .configmanager import ConfigManager
from .icepapsystem import IcepapSystem, Location
from .conflict import Conflict
from .icepapsmanager import IcepapsManager
from ..helpers import loggingInfo

__all__ = ['MainManager']


class MainManager(Singleton):
    log = logging.getLogger('{}.MainManager'.format(__name__))

    def __init__(self, form=None):
        pass

    @loggingInfo
    def init(self, *args):
        self.IcepapSystemList = {}

        self._ctrl_icepap = IcepapsManager()
        self._db = StormManager()

        self.dbStatusOK = self._db.dbOK

        self._form = args[0]
        self.locationList = self._db.getAllLocations()
        self.location = None
        self.IcepapSystemList = {}


    @loggingInfo
    def addLocation(self, location_name):
        """ Adds a location in the database """
        try:
            if str(location_name) in self.locationList:
                return False
            location = Location(str(location_name))
            self._db.store(location)
            self._db.commitTransaction()
            self.locationList[str(location_name)] = location
            return True
        except Exception as e:
            self.log.error("Can not add location %s: %s", location_name, e)
            return False


    @loggingInfo
    def deleteLocation(self, location_name):
        """ Deletes a location in the database """
        location = self.locationList[str(location_name)]
        self._db.deleteLocation(location)
        del self.locationList[str(location_name)]
        self.IcepapSystemList = {}


    @loggingInfo
    def changeLocation(self, location):
        """ Close the connection from all the icepaps in one location.
        And gets all the icepaps from the selected location """

        self.location = self.locationList[str(location)]
        self._ctrl_icepap.closeAllConnections()
        self.IcepapSystemList = self._db.getLocationIcepapSystem(str(location))


    @loggingInfo
    def reset(self, form):
        self._ctrl_icepap.reset()
        self._db.reset()
        self.dbStatusOK = self._db.dbOK
        self.location = None
        self.IcepapSystemList = {}
        self._form = form
        self.locationList = self._db.getAllLocations()


    @loggingInfo
    def addIcepapSystem(self, host, port, description=None):
        """ Adds a new Icepap in the current location, the parameters are
        the hostname, port and description, this function checks if the
        icepap is available, the gets all the configuration of all the
        driver and stores all these information in the database """
        QtWidgets.QApplication.instance().setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            icepap_name = host
            """ *TO-DO STORM review"""
            if icepap_name in self.IcepapSystemList:
                return None
            location = self.location.name
            try:
                port = int(port)
                icepap_system = IcepapSystem(icepap_name, host,
                                             port, location, description)

                # JUST IN CASE A USER WANTS TO RE-ADD A SYSTEM !?!?!?!?
                # A QUANTUM PROBABILITY TO BE ON TWO LOCATIONS AT THE
                # SAME TIME... :-D
                db_icepap_system = self._db.getIcepapSystem(icepap_name)
                if db_icepap_system is not None:
                    MessageDialogs.showErrorMessage(
                        self._form, "Adding Icepap System error",
                        "The icepap system is already in "
                        "location: '%s'" % (db_icepap_system.location_name))
                    QtWidgets.QApplication.instance().restoreOverrideCursor()
                    return None

                self._ctrl_icepap.openConnection(icepap_name, host, port)
                driver_list = self._ctrl_icepap.scanIcepapSystem(icepap_name)
                self._db.addIcepapSystem(icepap_system)
                self.IcepapSystemList[icepap_name] = icepap_system
                self.location.addSystem(icepap_system)
                for driver in list(driver_list.values()):
                    icepap_system.addDriver(driver)
                    self._db.store(driver)
                self._db.commitTransaction()
                QtWidgets.QApplication.instance().restoreOverrideCursor()
                if len(driver_list) == 0:
                    msg = 'The icepap system "{}" has ZERO drivers.\n' \
                          'Please make sure sure that the CAN BUS TERMINATOR' \
                          ' is connected '.format(icepap_name)
                    self.log.warning(msg)
                    MessageDialogs.showWarningMessage(
                        None, "Scanning Icepap Warning", msg)
                return icepap_system
            except Exception as ie:
                msg = 'Could not scan the "{0}" Icepap System.\n' \
                      '1) Please make sure that the system "{0}" is in your ' \
                      'subnetwork.\n' \
                      '2) Run in debug mode to check communication: ' \
                      'icepapcms -d\n' \
                      'Exception: {1}'.format(icepap_name, str(ie))
                self.log.warning(msg)
                MessageDialogs.showErrorMessage(None, "Scanning Icepap Error",
                                                msg)

            except Exception as e:
                self.log.error("Error on adding Icepap System %s:%d: %s",
                               host, port, e)

        except Exception as e:
            self.log.error("Error on adding Icepap System %s:%d: %s",
                           host, port, e)
        QtWidgets.QApplication.instance().restoreOverrideCursor()
        return None

    @loggingInfo
    def deleteIcepapSystem(self, icepap_name):
        """ deletes and Icepap in the database """
        del self.IcepapSystemList[icepap_name]
        self.location.deleteSystem(icepap_name)

    @loggingInfo
    def closeAllConnections(self):
        """ Close all the openned connections to the icepaps """
        self._ctrl_icepap.closeAllConnections()
        return self._db.closeDB()

    @loggingInfo
    def getIcepapSystem(self, icepap_name):
        if icepap_name in self.IcepapSystemList:
            return self.IcepapSystemList[icepap_name]
        return None

    @loggingInfo
    def checkIcepapSystems(self):
        """ Checks if the icepaps for the current location are available over
        the network or not. These function is used to perform automatic
        reconnection """

        changed_list = []
        for icepap_system in list(self.IcepapSystemList.values()):
            connected = self._ctrl_icepap.checkIcepapStatus(icepap_system.name)

            if connected:
                if icepap_system.conflict == Conflict.NO_CONNECTION:
                    icepap_system.conflict = Conflict.NO_CONFLICT
                    changed_list.append(icepap_system)
            else:
                if icepap_system.conflict != Conflict.NO_CONFLICT and \
                        icepap_system.conflict != Conflict.NO_CONNECTION:
                    icepap_system.conflict = Conflict.NO_CONNECTION
                    changed_list.append(icepap_system)
        return changed_list

    @loggingInfo
    def stopIcepap(self, icepap_system):
        """ Close the connection to an icepap. And commits all the changes in
        the database """
        try:
            self._ctrl_icepap.closeConnection(icepap_system.name)
            self._db.commitTransaction()
        except Exception as e:
            msg = "Unexpected error on stop icepap_system {}: " \
                  "{}".format(icepap_system, e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(self._form, 'Unexpected error',
                                            msg)

    @loggingInfo
    def scanIcepap(self, icepap_system):
        """ Searches for configuration conflicts.
        Returns the conflicts list. That is composed by elements of
        [Conflict code, icepap_system, icepap_driver_addr] """
        QtWidgets.QApplication.instance().setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        icepap_name = icepap_system.name
        conflictsList = []
        try:
            if self._ctrl_icepap.openConnection(icepap_name,
                                                icepap_system.host,
                                                icepap_system.port):
                driver_list = self._ctrl_icepap.scanIcepapSystem(icepap_name,
                                                                 True)
                conflictsList = icepap_system.compareDriverList(driver_list)
            else:
                conflictsList.append([Conflict.NO_CONNECTION, icepap_system,
                                      0])
        except Exception as error:
            msg = 'Could not scan the "{0}" Icepap System.\n' \
                  '1) Please make sure that the system "{0}" is in your ' \
                  'subnetwork.\n' \
                  '2) Run in debug mode to check communication: ' \
                  'icepapcms -d\n' \
                  'Exception: {1}'.format(icepap_name, str(error))
            self.log.warning(msg)
            MessageDialogs.showErrorMessage(None, "Scanning Icepap Error",
                                            msg)

            conflictsList.append([Conflict.NO_CONNECTION, icepap_system, 0])

        QtWidgets.QApplication.instance().restoreOverrideCursor()

        return conflictsList

    @loggingInfo
    def checkFirmwareVersions(self, icepap_system):
        config = ConfigManager()
        if config._options.skipversioncheck is True:
            self.log.warning("Firmware versions are not checked.")
            return
        try:
            icepap_name = icepap_system.name
            ipap = self._ctrl_icepap.iPaps[icepap_name]
            master_version = ipap.fver
            mismatched_drivers = []
            for driver in icepap_system.getDrivers():
                # #############################################################
                try:
                    driver_version = ipap[driver.addr].fver
                except Exception:
                    # If the driver has been temporary removed,
                    # the error should
                    self.log.warning('%s[%d] is removed', icepap_name,
                                     driver.addr)
                    driver_version = master_version
                if master_version != driver_version:
                    mismatched_drivers.append((driver.addr,
                                               str(driver_version)))

            if len(mismatched_drivers) > 0:
                msg = "Some drivers do not have the MASTER's " \
                      "firmware version (%s):\n" % master_version
                for driver, version in mismatched_drivers:
                    msg = msg + "driver %d: %s\n" % (driver, version)
                saved_version = ipap.ver_saved.driver[0]
                msg = msg + "Board saved version: %s\n" % saved_version
                msg = msg + "Would you like to upgrade these drivers?\n"
                self.log.info(msg)
                upgrade = MessageDialogs.showYesNoMessage(
                    self._form, "Firmware mismatch", msg)
                if upgrade:
                    progress_dialog = QtWidgets.QProgressDialog(self._form)
                    progress_dialog.setLabel(QtWidgets.QLabel(
                        "Icepap: %s\nUpgrading drivers' firmware "
                        "to %s" % (icepap_name, saved_version)))
                    progress_dialog.setCancelButton(None)
                    progress_dialog.setMaximum(100)
                    upgrading = self._ctrl_icepap.upgradeDrivers(
                        icepap_name, progress_dialog)
                    if not upgrading:
                        progress_dialog.cancel()
                        msg = "Sorry, problems found while upgrading. " \
                              "Please try it manually :-("
                        self.log.error(msg)
                        MessageDialogs.showErrorMessage(
                            None, "Firmware upgrade error", msg)
        except Exception as e:
            self.log.error('Error on checking %s firmware version: %s',
                           icepap_name, e)

    @loggingInfo
    def importMovedDriver(self, icepap_driver, from_to=False):
        """ function to import the information from a moved driver,
        to avoid losing historic cfgs"""
        id = icepap_driver.current_cfg.getParameter("ID", True)
        got_driver = self._db.existsDriver(icepap_driver, id)
        if from_to:
            if got_driver:
                src_driver = icepap_driver
                dst_driver = got_driver
            else:
                delete = MessageDialogs.showYesNoMessage(
                    self._form, "Driver error",
                    "Driver not present.\nRemove driver from DB?")
                if delete:
                    icepap_driver.icepap_system.removeDriver(
                        icepap_driver.addr)
                return None
        else:
            src_driver = got_driver
            dst_driver = icepap_driver

        move = MessageDialogs.showYesNoMessage(
            self._form, "Import moved driver",
            "Import all historic configurations from %s:axis "
            "%d to %s:axis %d" % (
                src_driver.icepapsystem_name, src_driver.addr,
                dst_driver.icepapsystem_name, dst_driver.addr))
        src_sys = src_driver.icepap_system
        if move:
            for cfg in src_driver.historic_cfgs:
                cfg.setDriver(dst_driver)
                dst_driver.historic_cfgs.add(cfg)
        src_driver.icepap_system.removeDriver(src_driver.addr)
        return src_sys

    @loggingInfo
    def getDriversToSign(self):
        """ Gets the all drivers to be signed """
        signList = []
        for icepap_system in list(self.IcepapSystemList.values()):
            """ TO-DO STORM review"""
            for driver in icepap_system.getDrivers():
                if driver.mode == Mode.CONFIG:
                    signList.append(driver)
        return signList

    @loggingInfo
    def getDriverConfiguration(self, icepap_name, addr):
        try:
            config = self._ctrl_icepap.getDriverConfiguration(icepap_name,
                                                              addr)
            return config

        except Exception:
            MessageDialogs.showErrorMessage(
                self._form, "GetDriverConfiguration Icepap error",
                "%s Connection error" % icepap_name)

    @loggingInfo
    def getDriverStatus(self, icepap_name, addr):
        """ Driver Status used in the System and crate view
            Returns [status register, power status, current ]"""
        icepap_system = self.getIcepapSystem(icepap_name)
        if icepap_system is None:
            return -1, False, -1
        try:
            driver = icepap_system.getDriver(addr)
            if driver is None:
                return -1, False, -1
            if driver.conflict == Conflict.DRIVER_NOT_PRESENT or \
                    driver.conflict == Conflict.NO_CONNECTION:
                # print "OUPS! THIS DRIVER SHOULD NOT BE SCANNED"
                return -1, False, -1
            status = self._ctrl_icepap.getDriverStatus(icepap_name, addr)
            return status
        except Exception:
            msg = "{},{} Connection timeout".format(icepap_name, addr)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(self._form,
                                            'GetDriverStatus Icepap error ',
                                            msg)
            self._form.refreshTree()
            return -1, False, -1

    @loggingInfo
    def getDriverTestStatus(self, icepap_name, addr, pos_sel, enc_sel):
        """ Driver Status used in the System and crate view
            Returns [status register, power state, [position register value,
            encoder register value]"""
        try:
            return self._ctrl_icepap.getDriverTestStatus(icepap_name, addr,
                                                         pos_sel, enc_sel)
        except Exception as error:
            MessageDialogs.showErrorMessage(
                self._form, "GetDriverTestStatus Icepap error",
                "%s Connection error:%s" % (icepap_name, str(error)))
            self._form.refreshTree()
            return -1, -1, [-1, -1]
        except Exception as e:
            self.log.error("getDriverTestStatus:Unexpected error while "
                           "getting driver test status. %s", e)
            return -1, -1, [-1, -1]

    @loggingInfo
    def readIcepapParameters(self, icepap_name, addr, par_list):
        """ Gets from adriver the values of the parameters in par_list """
        try:
            return self._ctrl_icepap.readIcepapParameters(icepap_name,
                                                          addr, par_list)
        except Exception as error:
            msg = "{} Connection " \
                  "error: {}".format(icepap_name, error)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(
                self._form, 'ReadIcepapParamenters Icepap error ', msg)

    @loggingInfo
    def writeIcepapParameters(self, icepap_name, addr, par_var_list):
        """ Writes to a driver the values in the par_var_list """
        try:
            self._ctrl_icepap.writeIcepapParameters(icepap_name, addr,
                                                    par_var_list)
        except Exception:
            pass

    @loggingInfo
    def getDriverMotionValues(self, icepap_name, addr):
        """ Returns speed and acceleration of a driver """
        try:
            return self._ctrl_icepap.getDriverMotionValues(icepap_name, addr)
        except Exception:
            return -1, -1

    @loggingInfo
    def setDriverMotionValues(self, icepap_name, addr, values):
        """ Sets speed and acceleration to a driver """
        try:
            return self._ctrl_icepap.setDriverMotionValues(icepap_name,
                                                           addr, values)
        except Exception:
            MessageDialogs.showWarningMessage(
                self._form, "SetDriverMotionValues Icepap error",
                "Connection error")

    @loggingInfo
    def setDriverPosition(self, icepap_name, addr, pos_sel, position):
        return self._ctrl_icepap.setDriverPosition(icepap_name, addr,
                                                   pos_sel, position)

    @loggingInfo
    def setDriverEncoder(self, icepap_name, addr, pos_sel, position):
        return self._ctrl_icepap.setDriverEncoder(icepap_name, addr,
                                                  pos_sel, position)

    @loggingInfo
    def moveDriver(self, icepap_name, addr, steps):
        try:
            self._ctrl_icepap.moveDriver(icepap_name, addr, steps)
        except Exception as error:
            msg = "{} Connection error: {}".format(icepap_name, error)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(self._form,
                                            'MoveDriver Icepap error', msg)

    @loggingInfo
    def moveDriverAbsolute(self, icepap_name, addr, position):
        try:
            self._ctrl_icepap.moveDriverAbsolute(icepap_name, addr, position)
        except Exception as error:
            msg = "{} Connection error: {}".format(icepap_name, error)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(self._form,
                                            'MoveDriverAbsolute Icepap', msg)

    @loggingInfo
    def stopDriver(self, icepap_name, addr):
        try:
            self._ctrl_icepap.stopDriver(icepap_name, addr)
        except Exception as error:
            msg = "{} Connection error: {}".format(icepap_name, error)
            self.log.error(msg)
            MessageDialogs.showWarningMessage(self._form,
                                              'StopDriver Icepap error', msg)

    @loggingInfo
    def blinkDriver(self, icepap_name, driver_addr, secs):
        self._ctrl_icepap.blinkDriver(icepap_name, driver_addr, secs)


    @loggingInfo
    def jogDriver(self, icepap_name, addr, speed):
        self._ctrl_icepap.jogDriver(icepap_name, addr, speed)


    @loggingInfo
    def enableDriver(self, icepap_name, driver_addr):
        self._ctrl_icepap.enableDriver(icepap_name, driver_addr)


    @loggingInfo
    def disableDriver(self, icepap_name, driver_addr):
        self._ctrl_icepap.disableDriver(icepap_name, driver_addr)


    @loggingInfo
    def saveValuesInIcepap(self, icepap_driver, new_values,
                           expertFlag=False, ignore_values=[]):
        """ Stores the new configuration in the icepap, and sets the mode of
        the driver to CONFIG """
        for param, db_value in ignore_values:
            new_values.remove((param, db_value))
        try:
            new_cfg = self._ctrl_icepap.setDriverConfiguration(
                icepap_driver.icepapsystem_name, icepap_driver.addr,
                new_values, expertFlag=expertFlag)
        except Exception:
            new_cfg = None
        if new_cfg is None:
            return False
        else:
            icepap_driver.mode = str(Mode.CONFIG)
            icepap_driver.addConfiguration(new_cfg)
            return True


    @loggingInfo
    def startConfiguringDriver(self, icepap_driver):
        return self._ctrl_icepap.startConfiguringDriver(
            icepap_driver.icepapsystem_name, icepap_driver)

    @loggingInfo
    def endConfiguringDriver(self, icepap_driver):
        self._ctrl_icepap.endConfiguringDriver(icepap_driver.icepapsystem_name,
                                               icepap_driver)

    @loggingInfo
    def discardDriverChanges(self, icepap_driver):
        icepap_driver.setStartupCfg()
        self._ctrl_icepap.setDriverConfiguration(
            icepap_driver.icepapsystem_name, icepap_driver.addr,
            icepap_driver.current_cfg.toList())

        pass

    @loggingInfo
    def undoDriverConfiguration(self, icepap_driver):
        undo_cfg = icepap_driver.getUndoList()
        new_cfg = self._ctrl_icepap.setDriverConfiguration(
            icepap_driver.icepapsystem_name, icepap_driver.addr,
            undo_cfg.toList())
        if new_cfg is None:
            MessageDialogs.showWarningMessage(
                self._form, "undoDriverConfig error", "Connection error")
        else:
            icepap_driver.undo(new_cfg)
            return True

    @loggingInfo
    def getIcepapList(self):
        return self.IcepapSystemList

    @loggingInfo
    def getDriverTemplateList(self):
        return self._zodb.getAllDriverTemplate()

    @loggingInfo
    def saveDriverTemplate(self, name, desc, cfg):
        pass
        # TODO investigate IcepapDriverTemple
        # self._zodb.addDriverTemplate(IcepapDriverTemplate(name, desc, cfg))

    @loggingInfo
    def deleteDriverTemplate(self, name):
        self._zodb.deleteDriverTemplate(name)

    @loggingInfo
    def configDriverToDefaults(self, icepap_driver):
        icepap_name = icepap_driver.icepapsystem_name
        addr = icepap_driver.addr
        self._ctrl_icepap.configDriverToDefaults(icepap_name, addr)

    @loggingInfo
    def updateDriverConfig(self, icepap_driver):
        icepap_name = icepap_driver.icepapsystem_name
        addr = icepap_driver.addr
        driver_cfg = self.getDriverConfiguration(icepap_name, addr)
        icepap_driver.addConfiguration(driver_cfg)
