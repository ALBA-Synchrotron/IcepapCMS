from storm.locals import *
from conflict import Conflict
import sys
from stormmanager import StormManager

 
class Location(Storm):
    __storm_table__ = "location"
    name = Unicode(primary=True)
    systems = ReferenceSet(name, "IcepapSystem.location_name")
    def __init__(self, name):
        self.name = name
        self.initialize()
        
    def initialize(self):
        self._inmemory_systems = {}
        
    def __storm_loaded__(self):
        self.initialize()
        for system in self.systems:
            self._inmemory_systems[system.name] = system
    
    def addSystem(self, system):
        self.systems.add(system)
        self._inmemory_systems[system.name] = system
    
    def deleteSystem(self, name):
        system = self.systems.find(IcepapSystem.name == name).one()
        StormManager().deleteIcepapSystem(system)
        del self._inmemory_systems[name]
        
            

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
    
    def __init__(self, name, host, port, location_name, description = None):
        self.name = unicode(name)
        if description == None:
            description = unicode("")
        self.description = unicode(description)
        self.location_name = location_name
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
        driver = self.drivers.find(IcepapDriver.addr == addr).one()
        StormManager().deleteDriver(driver)
        del self._inmemory_drivers[addr]
    
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
                ''' determine if it is a new driver or if it has been moved '''
                # ALWAYS TREAT AS NEW DRIVER, 'MOVED' HAS NO SENSE
                conflictsList.append([Conflict.NEW_DRIVER, self, addr])
                ###id = driver.current_cfg.getParameter("ID", True)
                ###db = StormManager()
                ###if db.existsDriver(driver, id):                    
                ###    conflictsList.append([Conflict.DRIVER_MOVED, self, addr])                
                ###else:                    
                ###    conflictsList.append([Conflict.NEW_DRIVER, self, addr])

            ##if addr == 12:
            ##    print "SETTING NEW_DRIVER CONFLICTS... THIS IS JUST FOR TESTING THE CFG DEFAULT"
            ##    conflictsList.append([Conflict.NEW_DRIVER, self, addr])
            
        return conflictsList

from icepapdriver import IcepapDriver

