#import icepapsystem
from configmanager import ConfigManager
from storm.locals import *
from singleton import Singleton
import os
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
            db = self._config.config[self._config.database]["database"]
                        
            if db == self._config.Sqlite:
                folder = self._config.config[self._config.database]["folder"]
                loc = folder + '/icepapcms.db'
                self._database =  create_database("%s:%s" % (db, loc))
            else:
                server = self._config.config[self._config.database]["server"]
                user = self._config.config[self._config.database]["user"]
                pwd = self._config.config[self._config.database]["password"]
                self._database =  create_database("%s://%s:%s@%s/icepapcms" % (db, user, pwd, server))
                        
            self._store = Store(self._database)
            self.dbOK = True
        except:
            print "Unexpected error:", sys.exc_info()
            self.dbOK = False

        
    def closeDB(self):
        try:
            if self.dbOK:
                self._store.commit()
                self._store.close()
            return True
        except:
            self.dbOK = False
            return False
            
        
    def store(self, obj):
        self._store.add(obj)
    
    def remove(self, obj):
        self._store.remove(obj)
        
    def addIcepapSystem(self, icepap_system):
        try:
            self._store.add(icepap_system)
            return True
        except:
            return False
    
    def deleteIcepapSystem(self, icepap_system):
        self._store.remove(icepap_system)
        self.commitTransaction()
    
    def getIcepapSystem(self, icepap_name):
        return self._store.get(IcepapSystem, icepap_name)
    
    def getAllIcepapSystem(self):
        try:
            icepaps = self._store.find(IcepapSystem)
            ipapdict = {}
            for ipap_sys in icepaps:
                ipapdict[ipap_sys.name] = ipap_sys
            return ipapdict
        except:
            print "Unexpected error:", sys.exc_info()[1]
            return {}
       
    
    def commitTransaction(self):
        try:
            self._store.commit()
            self._store.flush()
            return True
        except:
            return False

from icepapsystem import *

    
    
        
        
