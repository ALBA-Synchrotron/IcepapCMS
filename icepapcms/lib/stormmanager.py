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

from pkg_resources import resource_filename
from storm.locals import Store, create_database
import os
import re
import logging
from .singleton import Singleton
from .configmanager import ConfigManager
from ..helpers import loggingInfo
from .stormmysql import MySQL

__all__ = ['StormManager']


class StormManager(Singleton):
    log = logging.getLogger('{}.StormManager'.format(__name__))

    def __init__(self):
        pass

    @loggingInfo
    def init(self, *args):
        self.dbOK = False
        self.openDB()

    @loggingInfo
    def reset(self):
        self.closeDB()
        self.openDB()

    @loggingInfo
    def openDB(self):
        try:
            self._config = ConfigManager()
            self.db = self._config.config[self._config.database]["database"]
            create_db = False
            if self.db == self._config.Sqlite:
                folder = self._config.config[self._config.database]["folder"]
                loc = folder + '/icepapcms.db'
                create_db = not os.path.exists(loc)
                if create_db:
                    if not os.path.exists(folder):
                        os.mkdir(folder)
                self._database = create_database("%s:%s" % (self.db, loc))
            else:
                server = self._config.config[self._config.database]["server"]
                user = self._config.config[self._config.database]["user"]
                pwd = self._config.config[self._config.database]["password"]
                scheme = "{}://{}:{}@{}/icepapcms" .format(self.db, user, pwd,
                                                           server)

                if self.db == 'mysql':
                    self._database = MySQL(scheme)
                else:
                    self._database = create_database(scheme)

            self._store = Store(self._database)
            if create_db:
                self.dbOK = self.createSqliteDB()
            else:
                self.dbOK = True
        except Exception as e:
            self.log.error("Unexpected error on openDB: %s", e)
            self.dbOK = False

    @loggingInfo
    def createSqliteDB(self):
        try:
            sql_file = resource_filename('icepapcms.db',
                                         'creates_sqlite.sql')
            with open(sql_file, 'rb') as f:
                sql_script = f.read().decode()
            statements = re.compile(r";[ \t]*$", re.M)

            for statement in statements.split(sql_script):
                # Remove any comments from the file
                statement = re.sub(r"--.*[\n\\Z]", "", statement)
                if statement.strip():
                    create = statement + ";"
                    self._store.execute(create)
            self._store.commit()
            return True
        except Exception as e:
            self.log.error("Unexpected error on createSqliteDB: %s", e)
            return False

    @loggingInfo
    def closeDB(self):
        try:
            if self.dbOK:
                self._store.close()
            return True
        except Exception as e:
            self.log.error("Unexpected error on closeDB:", e)
            self.dbOK = False
            return False

    @loggingInfo
    def store(self, obj):
        self._store.add(obj)

    @loggingInfo
    def remove(self, obj):
        self._store.remove(obj)

    @loggingInfo
    def addIcepapSystem(self, icepap_system):
        try:
            self._store.add(icepap_system)
            self.commitTransaction()
            return True
        except Exception as e:
            self.log.error("some exception trying to store the icepap system "
                           "%s: %s", icepap_system, e)
            return False

    @loggingInfo
    def deleteLocation(self, location):
        if self.db == self._config.Sqlite:
            for system in location.systems:
                self.deleteIcepapSystem(system)
        self._store.remove(location)
        self.commitTransaction()

    @loggingInfo
    def deleteIcepapSystem(self, icepap_system):
        if self.db == self._config.Sqlite:
            for driver in icepap_system.drivers:
                self.deleteDriver(driver)
        self._store.remove(icepap_system)
        self.commitTransaction()

    @loggingInfo
    def deleteDriver(self, driver):

        for cfg in driver.historic_cfgs:
            for par in cfg.parameters:
                self._store.remove(par)
            self._store.remove(cfg)
        self._store.remove(driver)
        self.commitTransaction()

    @loggingInfo
    def getAllLocations(self):
        try:
            locations = self._store.find(Location)
            location_dict = {}
            for location in locations:
                location_dict[location.name] = location
            return location_dict
        except Exception as e:
            self.log.error("Unexpected error on getAllLocations: %s", e)
            return {}

    @loggingInfo
    def getLocation(self, name):
        return self._store.get(Location, name)

    @loggingInfo
    def getIcepapSystem(self, icepap_name):
        return self._store.get(IcepapSystem, icepap_name)

    @loggingInfo
    def existsDriver(self, mydriver, id):

        drivers = self._store.find(
            IcepapDriver, IcepapDriver.addr == IcepapDriverCfg.driver_addr,
            IcepapDriverCfg.id == CfgParameter.cfg_id,
            CfgParameter.name == str("ID"), CfgParameter.value == id)
        if drivers:
            for driver in drivers:
                if driver.addr != mydriver.addr:
                    return driver
            return None
        else:
            return None

    @loggingInfo
    def getLocationIcepapSystem(self, location):
        try:
            icepaps = self._store.find(IcepapSystem,
                                       IcepapSystem.location_name == location)
            icepaps.order_by(IcepapSystem.name)
            ipapdict = {}
            for ipap_sys in icepaps:
                ipapdict[ipap_sys.name] = ipap_sys
            return ipapdict
        except Exception as e:
            self.log.error("Unexpected error on getLocationIcepapSystem: "
                           "%s", e)
            return {}

    @loggingInfo
    def rollback(self):
        self._store.rollback()

    @loggingInfo
    def commitTransaction(self):
        try:
            self._store.commit()
            return True
        except Exception:
            return False


# TODO Avoid circular imports
from .icepapsystem import Location, IcepapSystem
from .icepapdriver import IcepapDriver
from .icepapdrivercfg import CfgParameter, IcepapDriverCfg
