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



from .configmanager import ConfigManager
from storm.locals import *
from .singleton import Singleton
import os, re
import sys
import time


class StormManager(Singleton):
    def __init__(self):
        pass

    def init(self, *args):
        self.dbOK = False
        self.openDB()
    
    def reset(self):
        self.closeDB()
        self.openDB()
                
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
                self._database =  create_database("%s:%s" % (self.db, loc))
            else:
                server = self._config.config[self._config.database]["server"]
                user = self._config.config[self._config.database]["user"]
                pwd = self._config.config[self._config.database]["password"]
                self._database =  create_database("%s://%s:%s@%s/icepapcms" % (self.db, user, pwd, server))
                
            self._store = Store(self._database)
            if create_db:                
                self.dbOK = self.createSqliteDB()
            else:
                self.dbOK = True
        except:
            print("Unexpected error:", sys.exc_info())
            self.dbOK = False
    
    def createSqliteDB(self):
        try:
            pathname = os.path.dirname(sys.argv[0])
            path = os.path.abspath(pathname)
            sql_file = path+'/db/creates_sqlite.sql'
            f = file(sql_file,'rb')
            sql_script = f.read()
            f.close()
            statements = re.compile(r";[ \t]*$", re.M)
            # Find custom SQL, if it's available.
            for statement in statements.split(sql_script):
                # Remove any comments from the file
                statement = re.sub(r"--.*[\n\Z]", "", statement)
                if statement.strip():
                    create = statement + ";"                        
                    self._store.execute(create)
            self._store.commit()
            return True
        except:
            print("Unexpected error:", sys.exc_info())
            return False
        
    def closeDB(self):
        try:
            if self.dbOK:
                #self._store.commit()
                self._store.close()
            return True
        except:
            print("Unexpected error:", sys.exc_info())
            self.dbOK = False
            return False
            
        
    def store(self, obj):
        self._store.add(obj)
    
    def remove(self, obj):
        self._store.remove(obj)
        
    
                   
    def addIcepapSystem(self, icepap_system):
        try:
            self._store.add(icepap_system)
            self.commitTransaction()
            return True
        except Exception as e:
            print("some exception trying to store the icepap system",e)
            return False
    
    def deleteLocation(self, location):
        if self.db == self._config.Sqlite:
            for system in location.systems:
                self.deleteIcepapSystem(system)          
        self._store.remove(location)
        self.commitTransaction()
    
    def deleteIcepapSystem(self, icepap_system):
        if self.db == self._config.Sqlite:
            for driver in icepap_system.drivers:
                self.deleteDriver(driver)          
        self._store.remove(icepap_system)
        self.commitTransaction()
    
    def deleteDriver(self, driver):
        for cfg in driver.historic_cfgs:
            for par in cfg.parameters:
                self._store.remove(par)
            self._store.remove(cfg)
        self._store.remove(driver)
        self.commitTransaction()  
    
    def getAllLocations(self):
        try:
            locations = self._store.find(Location)
            location_dict = {}
            for l in locations:
                location_dict[l.name] = l
            return location_dict
        except:
            print("getAllLocations:", sys.exc_info()[1])
            return {}
   
    def getLocation(self, name):
        return self._store.get(Location, name)   
    
    def getIcepapSystem(self, icepap_name):
        return self._store.get(IcepapSystem, icepap_name)
    
    def existsDriver(self, mydriver, id):
        drivers = self._store.find(IcepapDriver, IcepapDriver.addr == IcepapDriverCfg.driver_addr,
                            IcepapDriverCfg.id == CfgParameter.cfg_id,
                            CfgParameter.name == str("ID"), CfgParameter.value == id)
        if drivers:
            for driver in drivers:                
                if driver.addr != mydriver.addr: 
                    return driver
            return None
        else:
            return None
       
    def getLocationIcepapSystem(self, location):
        try:
            icepaps = self._store.find(IcepapSystem, IcepapSystem.location_name == location)
            icepaps.order_by(IcepapSystem.name)
            ipapdict = {}
            for ipap_sys in icepaps:
                ipapdict[ipap_sys.name] = ipap_sys
            return ipapdict
        except:
            print("getLocationIcepapSystem:", sys.exc_info()[1])
            return {}
    
    
    def rollback(self):
        self._store.rollback()
            
    def commitTransaction(self):
        try:
            self._store.commit()
            return True
        except:
            return False

from .icepapsystem import *
from .icepapdriver import *
from .icepapdrivercfg import *

    
    
        
        
