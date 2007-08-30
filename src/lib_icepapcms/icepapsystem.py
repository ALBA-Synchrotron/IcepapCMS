from persistent import Persistent
from icepapdriver import IcepapDriver
from conflict import Conflict

class IcepapSystem(Persistent):
    def __init__(self, name, host, port, description = None):
        self.name = name
        if description == None:
            description = ""
        self.description = description
        self.host = host
        self.port = port
        self.IcepapDriverList = {}
        self.conflict = Conflict.NO_CONFLICT
        self.child_conflicts = 0
        
    def setConflict(self, conflict):
        self.conflict = conflict
    
    def addDriver(self, addr, driver):
        self.IcepapDriverList[addr] = driver
    
    def removeDriver(self, addr):
        del self.IcepapDriverList[addr]
        self._p_changed = True
    
    def addDriverList(self, driver_list):
        self.IcepapDriverList = driver_list
    
    def getDriver(self, addr):
        if self.IcepapDriverList.has_key(addr):
            return self.IcepapDriverList[addr]
        else:
            return None
    
    def signSystem(self):
        for addr, driver in self.IcepapDriverList.items():
            driver.signDriver()
    
    def signCrate(self, cratenr):
        min = cratenr * 10
        max =  (cratenr + 1)* 10 
        for addr, driver in self.IcepapDriverList.items():
            if addr > min and addr < max:
                driver.signDriver()            
            if addr > max:
                return
        
    
    def compareDriverList(self, driver_list):
        self.child_conflicts = 0
        conflictsList = []
        self.conflict = Conflict.NO_CONFLICT
        ''' comparing drivers '''
        for addr, driver in self.IcepapDriverList.items():
            if not driver_list.has_key(addr):
                conflictsList.append([Conflict.DRIVER_NOT_PRESENT, self, addr])
                self.child_conflicts += 1
            else:
                driver_cmp = driver_list[addr]
                if not driver == driver_cmp:
                    conflictsList.append([Conflict.DRIVER_CHANGED, self, addr])
                    self.child_conflicts += 1
                    
        ''' checking for new drivers '''
        for addr, driver in driver_list.items():
            if not self.IcepapDriverList.has_key(addr):
                self.addDriver(addr, driver)
                conflictsList.append([Conflict.NEW_DRIVER, self, addr])

        return conflictsList