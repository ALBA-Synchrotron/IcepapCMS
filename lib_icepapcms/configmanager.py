from singleton import Singleton
import os
import sys
from configobj import ConfigObj
from validate import Validator

class ConfigManager(Singleton):
    Sqlite = "sqlite"
    MySql = "mysql"
    Postgres = "postgres"
    database = "database"
    icepap = "icepap"
    folder = os.path.expanduser('~/.icepapcms/sqlitedb')
    log_folder = os.path.expanduser('~/.icepapcms/log')
        
    defaults = '''
    [database]
    password = string(default=configure)
    folder = string(default=''' + folder +  ''')
    server = string(default=localhost:3306)
    user = string(default=icepapcms)
    database = string(default=sqlite)
    [icepap]
    debug_enabled = string(default=True)
    debug_level = string(default=1)
    log_folder = string(default=''' + log_folder + ''')
    conflict_solve= string(default=True)     
    '''
    
    defaults = defaults.splitlines()
    
    def __init__(self):
        pass
    
    
    def init(self, *args):
        if not os.path.exists(os.path.expanduser('~/.icepapcms')):
            os.mkdir(os.path.expanduser('~/.icepapcms'))
        self.config_filename = os.path.expanduser('~/.icepapcms/icepapcms.conf')
        self.configure()
    
    def configure(self):        
        self.configspec = ConfigObj(self.defaults)
        self.config = ConfigObj(self.config_filename, configspec = self.configspec)
        vdt = Validator()
        self.config.validate(vdt, copy=True)
        
    def saveConfig(self):
        self.config.write()
