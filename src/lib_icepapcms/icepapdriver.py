from storm.locals import *
from icepapdrivercfg import IcepapDriverCfg
from conflict import Conflict
from configmanager import ConfigManager
from icepapcontroller import IcepapController
from stormmanager import StormManager
import time
import socket
from pyIcePAP import IcepapMode


class IcepapDriver(Storm):
    __storm_table__ = "icepapdriver"
    __storm_primary__ = ("icepapsystem_name", "addr")
    icepapsystem_name = Unicode()
    addr = Int()
    name = Unicode()
    mode = Unicode()
    #currentcfg_id = Int()
    """ references """
    icepap_system = Reference(icepapsystem_name, "IcepapSystem.name")
    historic_cfgs = ReferenceSet((icepapsystem_name, addr), ("IcepapDriverCfg.icepapsystem_name", "IcepapDriverCfg.driver_addr"))
    #current_cfg = Reference(currentcfg_id, "IcepapDriverCfg.id")
    
    
    def __init__(self, icepap_name, addr):
        self.icepapsystem_name = unicode(icepap_name)        
        self.addr = addr
        self.current_cfg = None                 
        self.initialize()
        
    
    def __storm_loaded__(self):
        self.current_cfg = self.historic_cfgs.order_by("date").last()
        #print "%d : %s" %(self.addr, str(self.current_cfg.date))        
        self.initialize()
    
    def initialize(self):
        self.drivernr = self.addr % 10
        self.cratenr = self.addr / 10 
        self._undo_list = []
        self.startup_cfg = self.current_cfg
        self.conflict = Conflict.NO_CONFLICT
        
    def addConfiguration(self, cfg, current = True):
        if current:
            if not self.current_cfg is None:
                self._undo_list.append(self.current_cfg)
            else:
                self.startup_cfg = cfg
            self.current_cfg = cfg
            cfg.setDriver(self)
        self.historic_cfgs.add(cfg)
        #db = StormManager()
        #db.commitTransaction()
    
    def setConflict(self, conflict):
        self.conflict = conflict
        
    def getName(self):
        return self.name
        #return self.current_cfg.getParameter(unicode("IPAPNAME"))
    
    def setName(self, name):
        self.name = unicode(name)
    
    def setMode(self, mode):
        self.mode = unicode(mode)
    
    def signDriver(self):
        # AS ESRF SAYS, WHEN SIGNING THE DRIVER CONFIG, THE COMMIT SHOULD BE DONE
        # IN THE DATABASE FIRST, AND IF NO ERRORS, THEN COMMUNICATE THE DRIVER
        # THAT THE VALUES SHOULD BE SIGNED.
        try:
            db = StormManager()
            db.commitTransaction()
            #signature = socket.gethostname() #+ "_" + str(time.time())
            signature = socket.gethostname()+"_"+str(hex(int(time.time())))
            IcepapController().signDriverConfiguration(self.icepapsystem_name, self.addr, signature)
            self.current_cfg.name = unicode(time.ctime())
            self.current_cfg.setSignature(signature)        
            self.startup_cfg = self.current_cfg
            self.conflict = Conflict.NO_CONFLICT
            self.mode = unicode(IcepapMode.OPER)
        except Exception,e:
            print "some exception while trying to sign the driver",e
    
    def setStartupCfg(self):
        self.current_cfg = self.startup_cfg
        self.conflict = Conflict.NO_CONFLICT
    
    def undo(self, config):
        self.addConfiguration(config)
        # THE CURRENT CONFIGURATION SHOULD NOT BE IN THE UNDO LIST
        return self._undo_list.pop()
        #self.current_cfg = config    
        
    def getUndoList(self):
        return self._undo_list.pop()
    
    def hasUndoList(self):
        return len(self._undo_list) > 0
    
    def saveHistoricCfg(self, now, name, desc):
        self.current_cfg.name = unicode(name)
        self.current_cfg.description = unicode(desc)

    
    def deleteHistoricCfg(self, cfg):
        #self.historic_cfgs.remove(self.historic_cfgs.find(IcepapDriverCfg.date == date).one())
        self.historic_cfgs.remove(cfg)

    def __cmp__(self, other):
        #self.mode = other.mode
        #db = StormManager()
        #cfg = other.current_cfg
        #cfg.resetDriver()
        #other.historic_cfgs.remove(cfg)
        #db.store(cfg)
        if self.current_cfg == other.current_cfg:
            self.setConflict(Conflict.NO_CONFLICT)
            return 0

        config = ConfigManager()
        """solve_conflicts: If true if conflict appears, automatically will load data from db """
        solve_conflicts = config.config[config.icepap]["conflict_solve"] == str(True)
        if solve_conflicts:
            from mainmanager import MainManager
            MainManager().saveValuesInIcepap(self, self.current_cfg.toList())
            self.signDriver()
            self.setConflict(Conflict.DRIVER_FROM_DB)
            return 0
        else:
            self.setConflict(Conflict.DRIVER_CHANGED)

        return -1
     

    # TO SORT THE ICEPAP DRIVERS IN THE TREE
    def __lt__(self,other):
        if isinstance(other,IcepapDriver):
            return self.addr < other.addr
