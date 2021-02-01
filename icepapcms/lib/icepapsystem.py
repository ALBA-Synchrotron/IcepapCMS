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


from storm.locals import Storm, Unicode, ReferenceSet, Int
import logging
from .conflict import Conflict
from .stormmanager import StormManager
from .icepapdriver import IcepapDriver
from ..helpers import loggingInfo

__all__ = ['IcepapSystem', 'Location']


class Location(Storm):
    __storm_table__ = "location"
    name = Unicode(primary=True)
    systems = ReferenceSet(name, "IcepapSystem.location_name")
    log = logging.getLogger('{}.Location'.format(__name__))

    @loggingInfo
    def __init__(self, name):
        self.name = name
        self.initialize()

    @loggingInfo
    def initialize(self):
        self._inmemory_systems = {}

    @loggingInfo
    def __storm_loaded__(self):
        self.initialize()

    @loggingInfo
    def loadSystemsfromDB(self):
        for system in self.systems:
            self._inmemory_systems[system.name] = system

    @loggingInfo
    def addSystem(self, system):
        self.systems.add(system)
        self._inmemory_systems[system.name] = system

    @loggingInfo
    def deleteSystem(self, name):
        system = self.systems.find(IcepapSystem.name == name).one()
        for driver in system.getDrivers():
            system.removeDriver(driver.addr)
        StormManager().deleteIcepapSystem(system)
        try:
            del self._inmemory_systems[name]
            self._inmemory_drivers = {}
        except Exception:
            pass


class IcepapSystem(Storm):
    __storm_table__ = "icepapsystem"
    name = Unicode(primary=True)
    host = Unicode()
    port = Int()
    description = Unicode()
    version = Unicode()
    location_name = Unicode()
    """ references """
    drivers = ReferenceSet(name, "IcepapDriver.icepapsystem_name")
    location = ReferenceSet(location_name, "Location.name")
    log = logging.getLogger('{}.IcepapSystem'.format(__name__))

    @loggingInfo
    def __init__(self, name, host, port, location_name, description=None):
        self.name = str(name)
        if description is None:
            description = str("")
        self.description = str(description)
        self.location_name = location_name
        self.host = str(host)
        self.port = int(port)
        self.initialize()

    @loggingInfo
    def __storm_loaded__(self):
        self.initialize()

    @loggingInfo
    def loadDriversfromDB(self):
        for driver in self.drivers:
            self._inmemory_drivers[driver.addr] = driver

    @loggingInfo
    def initialize(self):
        self._inmemory_drivers = {}
        self.conflict = Conflict.NO_CONFLICT
        self.child_conflicts = 0

    @loggingInfo
    def getDriver(self, addr, in_memory=True):
        if in_memory:
            if addr in self._inmemory_drivers:
                return self._inmemory_drivers[addr]
            else:
                return None
        else:
            return self.drivers.find(IcepapDriver.addr == addr).one()

    @loggingInfo
    def getDrivers(self, in_memory=True):
        if in_memory:
            if len(self._inmemory_drivers) == 0:
                self.loadDriversfromDB()
            return list(self._inmemory_drivers.values())
        else:
            return self.drivers

    @loggingInfo
    def addDriver(self, driver):
        self.drivers.add(driver)
        self._inmemory_drivers[driver.addr] = driver

    @loggingInfo
    def addDriverList(self, driver_list):
        for driver in list(driver_list.values()):
            self.addDriver(driver)

    @loggingInfo
    def removeDriver(self, addr):
        driver = self.drivers.find(IcepapDriver.addr == addr).one()
        StormManager().deleteDriver(driver)
        del self._inmemory_drivers[addr]

    @loggingInfo
    def setConflict(self, conflict):
        self.conflict = conflict

    @loggingInfo
    def signSystem(self):
        for driver in self.getDrivers():
            driver.signDriver()

    @loggingInfo
    def signCrate(self, cratenr):
        min_addr = cratenr * 10
        max_addr = (cratenr + 1) * 10
        for driver in self.drivers.find(IcepapDriver.addr > min_addr,
                                        IcepapDriver.addr < max_addr):
            driver.signDriver()

    @loggingInfo
    def compareDriverList(self, driver_list):
        self.child_conflicts = 0
        conflictsList = []
        self.conflict = Conflict.NO_CONFLICT
        ''' comparing drivers '''
        for driver in self.drivers:
            addr = driver.addr
            if addr not in driver_list:
                conflictsList.append([Conflict.DRIVER_NOT_PRESENT, self, addr])
                self.child_conflicts += 1
            else:
                driver_cmp = driver_list[addr]
                if driver != driver_cmp:

                    # HOOK TO CHECK AUTO-SOLVE CONFLICTS
                    dsp_cfg = driver_cmp.current_cfg
                    db_cfg = driver.current_cfg
                    conflict = self.checkAutoSolvedConflict(dsp_cfg, db_cfg)
                    conflictsList.append([conflict, self, addr])
                    self.child_conflicts += 1

        # checking for new drivers
        for addr, driver in list(driver_list.items()):
            if self.drivers.find(IcepapDriver.addr == addr).count() == 0:
                self.addDriver(driver)
                # determine if it is a new driver or if it has been moved
                # ALWAYS TREAT AS NEW DRIVER, 'MOVED' HAS NO SENSE
                conflictsList.append([Conflict.NEW_DRIVER, self, addr])

        return conflictsList

    @loggingInfo
    def checkAutoSolvedConflict(self, dsp_cfg, db_cfg):
        # 20130710 ESRF ASKED FOR A HOOK TO 'SKIP' SOME CONFLICTS
        # ISSUE 053 in WIKI MINUTES
        # http://wikiserv.esrf.fr/esl/index.php/IcePAP_minute_130708
        #
        # TWO NEW CONFLICT TYPES ADDED: DRIVER_AUTOSOLVE,
        # DRIVER_AUTOSOLVE_EXPERT
        # Since there is the possibility to keep current behaviour,
        # the method can return also DRIVER_CHANGED

        # NOTE: u'VER' and u'IPAPNAME' are also available to resolve
        # conflicts...

        # NOTE: configs have the .getParameter(par) method
        #       BUT dsp values are not stored in the database, so in_memory
        #       has to be set to True
        # ## par = u'VER'
        # ## print 'dsp', par, dsp_cfg.getParameter(par, in_memory=True)
        # ## print 'db', par, db_cfg.getParameter(par)

        # NOTE: it is also possible to operate with lists:
        # ##dsp_values = dsp_cfg.toList()
        # ##db_values = db_cfg.toList()
        # ##for p,v in dsp_values:
        # ##    if p == par:
        # ##        print 'dsp', p, v
        # ##for p,v in db_values:
        # ##    if p == par:
        # ##        print 'db', p, v

        try:
            dsp_cfg_ver = float(dsp_cfg.getParameter(str("VER"),
                                                     in_memory=True))
        except Exception:
            self.log.error("%s: missing VERsion parameter in DSP config",
                           self.name)
            return Conflict.DRIVER_CHANGED

        try:
            db_cfg_ver = float(db_cfg.getParameter(str("VER")))
        except Exception:
            self.log.error("%s: missing VERsion parameter in database config",
                           self.name)
            return Conflict.DRIVER_CHANGED

        if(dsp_cfg_ver == 2.0) and (db_cfg_ver < 2.0) and (db_cfg_ver >= 1.22):
            dsp_values = dsp_cfg.toList()
            db_values = db_cfg.toList()
            diff_values = set(dsp_values).difference(db_values)
            for p, v in diff_values:
                if p == 'VER':
                    continue

                if p not in ['EXTDISABLE', 'PCLMODE', 'EXTBUSY',
                             'POSUPDATE', 'LNKNAME', 'EXTPOWER', 'OUTPSRC']:
                    return Conflict.DRIVER_CHANGED
            return Conflict.DRIVER_AUTOSOLVE

        if(dsp_cfg_ver > 3.14) and (db_cfg_ver <= 3.14) and \
                (db_cfg_ver >= 2.0):
            dsp_values = dsp_cfg.toList()
            db_values = db_cfg.toList()
            diff_values = set(dsp_values).difference(db_values)
            for p, v in diff_values:
                # ignore new parameters or parameters that normally change
                if (p == 'VER') or (p == 'HOLDTIME') or (p == 'EXTHOLD'):
                    continue

                # parameters which value is not backward compatible
                if p not in ['INFOASRC', 'INFOBSRC', 'INFOCSRC']:
                    return Conflict.DRIVER_CHANGED

            return Conflict.DRIVER_AUTOSOLVE_EXPERT

        return Conflict.DRIVER_CHANGED
