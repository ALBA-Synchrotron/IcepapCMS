from storm.locals import *
from conflict import Conflict
import sys
 

class IcepapSystem(Storm):
    __storm_table__ = "icepapsystem"
    name = Unicode(primary=True)
    host = Unicode()
    port = Int()
    description = Unicode()
    version = Unicode()
    """ references """
    drivers = ReferenceSet(name, "IcepapDriver.icepapsystem_name")
    
    def __init__(self, name, host, port, description = None):
        self.name = unicode(name)
        if description == None:
            description = unicode("")
        self.description = unicode(description)
        self.host = unicode(host)
        self.port = int(port)
        self.initialize()
    
    def __storm_loaded__(self):
        self.initialize()
        for driver in self.drivers:
            self._inmemory_drivers[driver.addr] = driver
        
    
    def initialize(self):
        self._inmemory_drivers = {}
        self.conflict = Conflict.NO_CONFLICT
        self.child_conflicts = 0
     
    def getDriver(self, addr, in_memory = True):
        if in_memory:
            if self._inmemory_drivers.has_key(addr):
                return self._inmemory_drivers[addr]
            else:
                return None
        else:
            return self.drivers.find(IcepapDriver.addr == addr).one()
    
    def getDrivers(self, in_memory = True):
        #return self.drivers.order_by(IcepapDriver.addr)
        if in_memory:
            return self._inmemory_drivers.values()
        else:
            return self.drivers
    
    def addDriver(self, driver):
        self.drivers.add(driver)
        self._inmemory_drivers[driver.addr] = driver
        
    def addDriverList(self, driver_list):
        for driver in driver_list.values():
            self.addDriver(driver)
    
    def removeDriver(self, addr):
        self.drivers.find(IcepapDriver.addr == addr).one().remove()
    
    def setConflict(self, conflict):
        self.conflict = conflict
    
    def signSystem(self):
        for driver in self.getDrivers():
            driver.signDriver()
    
    def signCrate(self, cratenr):
        min = cratenr * 10
        max =  (cratenr + 1)* 10         
        for driver in self.drivers.find(IcepapDriver.addr > min, IcepapDriver.addr < max):
            driver.signDriver()            
              
    def compareDriverList(self, driver_list):        
        self.child_conflicts = 0
        conflictsList = []
        self.conflict = Conflict.NO_CONFLICT
        ''' comparing drivers '''
        for driver in self.drivers:
            addr = driver.addr
            if not driver_list.has_key(addr):
                conflictsList.append([Conflict.DRIVER_NOT_PRESENT, self, addr])
                self.child_conflicts += 1
            else:
                driver_cmp = driver_list[addr]
                if not driver == driver_cmp :
                    conflictsList.append([Conflict.DRIVER_CHANGED, self, addr])
                    self.child_conflicts += 1                   
        ''' checking for new drivers '''        
        for addr, driver in driver_list.items():
            if self.drivers.find(IcepapDriver.addr == addr).count() == 0:
                self.addDriver(driver)
                conflictsList.append([Conflict.NEW_DRIVER, self, addr])
        return conflictsList

from icepapdriver import IcepapDriver

