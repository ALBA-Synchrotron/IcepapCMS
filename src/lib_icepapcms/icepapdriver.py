from persistent import Persistent
from icepapdrivercfg import IcepapDriverCfg
from conflict import Conflict

class IcepapDriver(Persistent):
    def __init__(self, icepap_name, addr, cratenr, drivernr, name = None, nemonic = None):
        if name == None:
            name = ""
        if nemonic == None:
            nemonic = ""
        self.icepap_name = icepap_name
        self.name = name
        self.nemonic = nemonic
        self.addr = addr
        self.cratenr = cratenr
        self.drivernr = drivernr
        self.currentCfg = None
        self.historicCfg = {}
        self.conflict = Conflict.NO_CONFLICT
        
    def setConflict(self, conflict):
        self.conflict = conflict
        self._p_changed = True
        
    def setConfiguration(self, config):
        if not hasattr(self, '_v_undoCfg'):
            self._v_undoCfg = []
        if not self.currentCfg is None:
            self._v_undoCfg.append(self.currentCfg)
        self.currentCfg = config
        self._p_changed = True        
    
    def undo(self, config):
        self.currentCfg = config
        self._p_changed = True
        
    def getUndoList(self):
        if not hasattr(self, '_v_undoCfg'):
            self._v_undoCfg = []    
        return self._v_undoCfg.pop()
    
    def hasUndoList(self):
        if not hasattr(self, '_v_undoCfg'):
            self._v_undoCfg = []    
        return len(self._v_undoCfg) > 0
    
    def saveHistoricCfg(self, now, name, desc):
        driver_cfg = IcepapDriverCfg(self.currentCfg.parList, name, desc)
        self.historicCfg[now] = driver_cfg
        self._p_changed = True
    
    def deleteHistoricCfg(self, date):
        del self.historicCfg[date]
        self._p_changed = True
        
    def __cmp__(self, other):
        res = (self.currentCfg == other.currentCfg)
        if not res:
            self.setConflict(Conflict.NO_CONFLICT)

        return res
        
