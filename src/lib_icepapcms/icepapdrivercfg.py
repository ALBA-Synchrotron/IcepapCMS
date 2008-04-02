from storm.locals import *
import datetime


class IcepapDriverCfg(Storm):
    __storm_table__ = "icepapdrivercfg"
    id = Int(primary=True)
    icepapsystem_name = Unicode()
    driver_addr = Int()        
    name = Unicode()
    description = Unicode()
    signature = Unicode()
    date = DateTime()
    """ references """
    icepap_driver = Reference((icepapsystem_name, driver_addr), ("IcepapDriver.icepapsystem_name", "IcepapDriver.addr"))
    parameters = ReferenceSet(id, "CfgParameter.cfg_id")
    
    def __init__(self,name, description = None):
        #self.icepapsystem_name = icepapsystem_name
        #self.driver_addr = driver_addr
        if description == None:
            description = unicode("")
        self.description = unicode(description)
        self.name = unicode(name)
        self.date = datetime.datetime.now()
        self.initialize()
    
    def __storm_loaded__(self):
        self.initialize()
        for cfgpar in self.parameters:
            self._inmemory_parameters[cfgpar.name] = cfgpar
        
    def initialize(self):
        self._inmemory_parameters = {}
        
    def setDriver(self, driver):
        self.icepap_driver = driver
    
    def resetDriver(self):
        self.icepap_driver = None
        self.icepapsystem_name = None
        self.driver_addr = None
        
    def setSignature(self, signature):
        self.signature = unicode(signature)
    
    def getSignature(self):
        return str(self.signature)
    
    def setParameter(self, name, value):
        name = unicode(name)
        value = unicode(value)        
        cfgpar = None
        try:
            cfgpar = self.parameters.find(CfgParameter.name == name).one()
        except:
            pass
        if cfgpar is None:
            cfgpar = CfgParameter(self, name, value)
            self.parameters.add(cfgpar)
        else:            
            cfgpar.value = value        
        self._inmemory_parameters[unicode(name)] = cfgpar
    
    def getParameter(self, name, in_memory = False):
        if in_memory:
            if self._inmemory_parameters.has_key(unicode(name)):                
                return self._inmemory_parameters[unicode(name)].value
            else:
                return None
        else:
            cfgpar = self.parameters.find(CfgParameter.name == name).one()
            if not cfgpar is None:
                return cfgpar.value
            else:
                return None
    
    def toList(self):
        list = []
        for cfgpar in self._inmemory_parameters.values():
            list.append((cfgpar.name, cfgpar.value))
        return list
    
    def __str__(self):
        text = "Configuration"
        for par in self.parameters:
             text = text + "\n" + par.name +":\t" + par.value
        return text
        
    
    def __cmp__(self, other):
        other_list = other.toList()
        self_list = self.toList()
        equals = True
        if len(other_list) <> len(self_list):
            return -1
            
        for name, value in self_list:
            other_value = other.getParameter(name, True)
            if other_value:
                if not value == other_value:
                    return -1
            elif name != "IPAPNAME":
                return -1
            else:
                # THE IPAPNAME IS AN INTERNAL CONFIG PARAMETER
                pass

        return 0
        
#        if other.parameters.count() <> self.parameters.count():
#            return False 
#        
#        equals = True
#        for par in self.parameters:
#            name = par.name
#            value = par.value
#            otherpar = other.parameters.find(CfgParameter.name == name).one()
#            if otherpar:
#                if not value == otherpar.value:
#                    equals = False
#            else:
#                return False                
#        return equals
        

            
class CfgParameter(Storm):
    __storm_table__ = "cfgparameter"
    __storm_primary__ = ("name", "cfg_id")
    cfg_id = Int()
    name = Unicode()
    value = Unicode()
    """ references """
    driver_cfg = Reference(cfg_id, "IcepapDriverCfg.id")    
    def __init__(self, cfg, name, value):
        self.driver_cfg = cfg
        self.name = unicode(name)
        self.value = unicode(value)

from icepapdriver import *
        
        
