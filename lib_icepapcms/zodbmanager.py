from singleton import Singleton
from icepapsystem import IcepapSystem
from ZODB import FileStorage, DB, config
from ZODB.POSException import ConflictError
from ZEO.ClientStorage import ClientStorage
from configmanager import ConfigManager
import os
import sys
import transaction
import time

class ZODBManager(Singleton):
    def __init__(self):
        pass

    def init(self, *args):
        self.dbOK = False
        self.openDB()
    
    def reset(self):
        self.closeDB()
        self._icepap_system_db = {}
        self.openDB()
        if self.dbOK:
            transaction.abort()
                
    def openDB(self):
        try:
          self._icepap_system_db = {}
          self._config = ConfigManager()
          self.createStorage()
          self._db = DB(self._storage)
          self._conn = self._db.open()
          self._dbroot = self._conn.root()
          if not self._dbroot.has_key('icepap_systems'):
              #from BTrees.OOBTree import OOBTree
              self._dbroot['icepap_systems'] = {}
          self._icepap_system_db = self._dbroot['icepap_systems']
          
          if not self._dbroot.has_key('driver_templates'):
              #from BTrees.OOBTree import OOBTree
              self._dbroot['driver_templates'] = {}
          self._driver_template_db = self._dbroot['driver_templates']
          self.dbOK = True
        except:
            self.dbOK = False

    
    def createStorage(self):
        remote = self._config.config["zodb"]["remote_storage"] == "True"
        if remote:
            server = self._config.config["zodb"]["remote_server"]
            cfg =  """\
            <zeoclient>
            server %s
            wait false
            </zeoclient>""" % server            
            #self._storage = config.storageFromString(cfg)
            s = server.split(':')
            self._storage = ClientStorage((s[0],int(s[1])), wait = False)
        else:
            path = self._config.config["zodb"]["local_folder"]
            self._storage = FileStorage.FileStorage(path + '/zodbdatabase.fs')

    def closeDB(self):
        
        try:
            if self.dbOK:
                transaction.commit()
                self._conn.close()
                self._db.close()
                self._storage.close()
            return True
        except:
            self.dbOK = False
            return False
            
        
    
    def addIcepapSystem(self, icepap_system):
        self._icepap_system_db[icepap_system.name] = icepap_system
        self._dbroot._p_changed = True
        self.commitTransaction()
    
    def deleteIcepapSystem(self, icepap_system):
        if self._icepap_system_db.has_key(icepap_system.name):
            self._dbroot._p_changed = True
            del self._icepap_system_db[icepap_system.name]
            self.commitTransaction()
    
    def getIcepapSystem(self, icepap_name):
        return self._icepap_system_db[icepap_name]
    
    def getAllIcepapSystem(self):
        return self._icepap_system_db
    
    def addDriverTemplate(self, driver_template):
        self._driver_template_db[driver_template.name] = driver_template
        self._dbroot._p_changed = True
        self.commitTransaction()
    
    def deleteDriverTemplate(self, template_name):
        if self._driver_template_db.has_key(template_name):
            self._dbroot._p_changed = True
            del self._driver_template_db[template_name]
            self.commitTransaction()
    
    def getDriverTemplate(self, template_name):
        return self._driver_template_db[template_name]
    
    def getAllDriverTemplate(self):
        return self._driver_template_db
    
    
    def commitTransaction(self):
        while 1:
            try:
                transaction.commit()
            except ConflictError:
                time.sleep(.2)
                pass
            except:
                return False
            else:
                break
        return True
    
    
    
        
        
