#!/usr/bin/env python

# ------------------------------------------------------------------------------
# This file is part of icepapCMS (https://github.com/ALBA-Synchrotron/icepapcms)
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# ------------------------------------------------------------------------------


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
    folder = "sqlitedb"
    log_folder = "log"
    firmware_folder = "firmware"
    configs_folder = "configs"
    templates_folder = "templates"
    docs_folder = "doc" 

    base_folder = None
    config_filename = None
    conf_path_list = ["./", os.path.expanduser("~/.icepapcms"), "/etc/icepapcms"]
    exe_folder = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    username = 'NotValidated'
        
    defaults = '''
    [database]
    password = string(default=configure)
    folder = string(default=''' + folder +  ''')
    server = string(default=localhost:3306)
    user = string(default=icepapcms)
    database = string(default=sqlite)
    [icepap]
    debug_enabled = string(default=False)
    debug_level = string(default=1)
    log_folder = string(default=''' + log_folder + ''')
    firmware_folder = string(default=''' + firmware_folder + ''')
    configs_folder = string(default=''' + configs_folder + ''')
    templates_folder = string(default=''' + templates_folder + ''')
    docs_folder = string(default=''' + docs_folder + ''')
    '''
    
    defaults = defaults.splitlines()
    
    def __init__(self, options=None):
        pass
    
    def init(self, *args):
        # Manage command line arguments and options
        if len(args):
            options = args[0]
            if options.config_path:
                self.conf_path_list.insert(0,os.path.expanduser(options.config_path))
                    
        self.configure()
    
    def configure(self):
        # General configuration
        for loc in self.conf_path_list:
            if os.path.exists(os.path.join(loc,"icepapcms.conf")):
                self.base_folder = loc
                self.config_filename = os.path.join(loc,"icepapcms.conf")
                break
        vdt = Validator()
        self.configspec = ConfigObj(self.defaults)
        self.config = ConfigObj(self.config_filename, configspec = self.configspec)
        self.config.validate(vdt, copy=True)

	#Force the absolute path
	self.config["database"]["folder"] = os.path.expanduser(self.config["database"]["folder"])

        # Other User configuration
        # always create base folder if not found.
        if self.base_folder is None:
            self.base_folder = os.path.expanduser("~/.icepapcms")
        if self.config_filename is None:
            self.config_filename = os.path.join(self.base_folder, "icepapcms.conf")
            if not os.path.exists(self.base_folder):
                os.mkdir(self.base_folder)        
            for folder in "log_folder","firmware_folder","configs_folder","templates_folder", "docs_folder":
                directory = os.path.join(self.base_folder, self.config["icepap"][folder])
                if not os.path.exists(directory):
                    os.makedirs(directory)

    def saveConfig(self):
        self.config.write()
