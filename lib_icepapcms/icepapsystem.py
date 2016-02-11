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

    def loadSystemsfromDB(self):
        for system in self.systems:
            self._inmemory_systems[system.name] = system
    
    def addSystem(self, system):
        self.systems.add(system)
        self._inmemory_systems[system.name] = system
    
    def deleteSystem(self, name):
        system = self.systems.find(IcepapSystem.name == name).one()
        StormManager().deleteIcepapSystem(system)
        try: del self._inmemory_systems[name]
        except: pass


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

        
    def loadDriversfromDB(self):
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
            if len(self._inmemory_drivers) == 0:
                self.loadDriversfromDB()
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
                    # HOOK TO CHECK AUTO-SOLVE CONFLICTS
                    #conflictsList.append([Conflict.DRIVER_CHANGED, self, addr])
                    dsp_cfg = driver_cmp.current_cfg
                    db_cfg = driver.current_cfg
                    conflict = self.checkAutoSolvedConflict(dsp_cfg, db_cfg)
                    conflictsList.append([conflict, self, addr])
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

    def checkAutoSolvedConflict(self, dsp_cfg, db_cfg):
        # 20130710 ESRF ASKED FOR A HOOK TO 'SKIP' SOME CONFLICTS
        # ISSUE 053 in WIKI MINUTES
        # http://wikiserv.esrf.fr/esl/index.php/IcePAP_minute_130708
        #
        # TWO NEW CONFLICT TYPES ADDED: DRIVER_AUTOSOLVE, DRIVER_AUTOSOLVE_EXPERT
        # Since there is the possibility to keep current behaviour, the method can return also DRIVER_CHANGED

        # NOTE: u'VER' and u'IPAPNAME' are also available to resolve conflicts...

        # NOTE: configs have the .getParameter(par) method
        #       BUT dsp values are not stored in the database, so in_memory has to be set to True
        ### par = u'VER'
        ### print 'dsp', par, dsp_cfg.getParameter(par, in_memory=True)
        ### print 'db', par, db_cfg.getParameter(par)

        # NOTE: it is also possible to operate with lists:
        ###dsp_values = dsp_cfg.toList()
        ###db_values = db_cfg.toList()
        ###for p,v in dsp_values:
        ###    if p == par:
        ###        print 'dsp', p, v
        ###for p,v in db_values:
        ###    if p == par:
        ###        print 'db', p, v

        try:
            dsp_cfg_ver = float(dsp_cfg.getParameter(unicode("VER"), 
                                                     in_memory=True))
        except:
            print "ERROR: missing VERsion parameter in DSP config"
            return Conflict.DRIVER_CHANGED

        try:
            db_cfg_ver  = float(db_cfg.getParameter(unicode("VER")))
        except:
            print "ERROR: missing VERsion parameter in database config"
            return Conflict.DRIVER_CHANGED

        #
        if((dsp_cfg_ver==2.0) and (db_cfg_ver<2.0) and (db_cfg_ver>=1.22)):
            dsp_values  = dsp_cfg.toList()
            db_values   = db_cfg.toList()
            diff_values = set(dsp_values).difference(db_values)
            for p,v in diff_values:
                if p == 'VER':
                   continue

                if not p in ['EXTDISABLE','PCLMODE','EXTBUSY','POSUPDATE','LNKNAME','EXTPOWER','OUTPSRC']:
                   #print "DSP VERSION: ",dsp_cfg_ver
                   #print "DB  VERSION: ",db_cfg_ver
                   #print "Auto resolving conflicts: Unexpected paramater: ",p
                   return Conflict.DRIVER_CHANGED
            return Conflict.DRIVER_AUTOSOLVE


        #
        if((dsp_cfg_ver>3.14) and (db_cfg_ver<=3.14) and (db_cfg_ver>=2.0)):
            print "DSP VERSION: ",dsp_cfg_ver
            print "DB  VERSION: ",db_cfg_ver
            dsp_values  = dsp_cfg.toList()
            db_values   = db_cfg.toList()
            diff_values = set(dsp_values).difference(db_values)
            print "diff_values", diff_values
            for p,v in diff_values:
                # ignore new parameters or parameters that normally change
                if ((p == 'VER') or (p == 'HOLDTIME') or (p == 'EXTHOLD')):
                   continue

                # parameters which value is not backward compatible
                if not p in ['INFOASRC','INFOBSRC','INFOCSRC']:
                   return Conflict.DRIVER_CHANGED

            return Conflict.DRIVER_AUTOSOLVE_EXPERT

        # parameter value in DB goes to DRIVER
        # return Conflict.DRIVER_AUTOSOLVE

        # parameter value in DRIVER goes to DB
        # return Conflict.DRIVER_AUTOSOLVE_EXPERT

        # no action, prompt the user to resolve conflict
        return Conflict.DRIVER_CHANGED

from icepapdriver import IcepapDriver

