#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of icepapcms https://github.com/ALBA-Synchrotron/icepapcms
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


from .singleton import Singleton
import os
import sys
from configobj import ConfigObj
from validate import Validator
import logging
from ..helpers import loggingInfo

__all__ = ['ConfigManager']


class ConfigManager(Singleton):
    Sqlite = "sqlite"
    MySql = "mysql"
    Postgres = "postgres"
    database = "database"
    icepap = "icepap"
    sqlite_folder = os.path.expanduser('~/.icepapcms/sqlitedb')
    log_folder = os.path.expanduser('~/.icepapcms/log')
    firmware_folder = os.path.expanduser('~/.icepapcms/firmware')
    configs_folder = ""
    templates_folder = os.path.expanduser('~/.icepapcms/templates')
    snapshots_folder = os.path.expanduser('~/.icepapcms/snapshots')
    base_folder = os.path.expanduser('~/.icepapcms')
    config_filename = None
    config_filename_override = None
    use_user_config = False

    conf_path_list = ["/etc/icepapcms", "./configs", os.path.expanduser("~/.icepapcms/configs")]
    exe_folder = os.path.abspath(os.path.dirname(sys.argv[0]))

    username = 'NotValidated'

    defaults = '''
    [database]
    password = string(default=configure)
    folder = string(default=''' + sqlite_folder + ''')
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
    snapshots_folder = string(default=''' + snapshots_folder + ''')
    [ldap]
    use = boolean(default=False)
    not_allowed = string(default='List of users no allowed to use the GUI')
    servers = string(default='list of servers')
    user_template=string(default='string with the configuration')
    [all_networks]
    use = boolean(default=False)
    
    
    '''

    defaults = defaults.splitlines()
    log = logging.getLogger('{}.ConfigManager'.format(__name__))

    def __init__(self, options=None):
        pass

    @loggingInfo
    def init(self, *args):
        # Manage command line arguments and options
        print("check args")
        if len(args):
            options = args[0]
            print(options)
            if options.config_file:
                self.config_filename_override = os.path.expanduser(options.config_file)
            if options.user_config:
                self.use_user_config = True
        self.configure()

    @loggingInfo
    def configure(self):
        # General configuration
        if self.config_filename_override:
            if os.path.exists(self.config_filename_override):
                self.config_filename = self.config_filename_override
                self.configs_folder = self.config_filename_override
            else:
                raise RuntimeError("Specified config file not found!")
        else:
            if self.use_user_config:
                self.conf_path_list = [os.path.expanduser("~/.icepapcms/configs")]
            for loc in self.conf_path_list:
                print("loc", loc)
                if os.path.exists(os.path.join(loc,"icepapcms.conf")):
                    self.configs_folder = loc
                    self.config_filename = os.path.join(self.configs_folder, "icepapcms.conf")
                    print("found:", self.config_filename, "in:", self.configs_folder)
                    break
        vdt = Validator()
        self.configspec = ConfigObj(self.defaults)
        self.config = ConfigObj(self.config_filename,
                                configspec=self.configspec)
        self.config.validate(vdt, copy=True)

        #Force the absolute path
        self.config["database"]["folder"] = os.path.expanduser(self.config["database"]["folder"])

        # Other User configuration
        # always create base folder if not found.
        # Using the recursive "makedirs" to create the full path.
        for folder in "log_folder", "snapshots_folder", "firmware_folder", "templates_folder":
            print(self.config["icepap"][folder])
            directory = os.path.expanduser(self.config["icepap"][folder])
            if not os.path.exists(directory):
                print("Create missing directory:", directory)
                os.makedirs(directory)
        if self.config_filename is None:
            print("ggggg")
            self.configs_folder = os.path.expanduser("~/.icepapcms/configs")
            self.config_filename = os.path.join(self.configs_folder, "icepapcms.conf")
            if not os.path.exists(self.configs_folder):
                os.makedirs(self.configs_folder)
        self.config.filename = self.config_filename
        self.config["icepap"]["configs_folder"] = self.configs_folder

        print("base folder", self.base_folder)
        #directory = os.path.join(self.base_folder, self.config["icepap"]["configs_folder"])
        #self.config["icepap"]["configs_folder"] = directory
        if os.access(self.config["icepap"]["configs_folder"], os.W_OK):
            if not os.path.exists(self.config["icepap"]["configs_folder"]):
                print("create conf folder")
                os.makedirs(self.config["icepap"]["configs_folder"])
        
        print("Using config folder:", self.config["icepap"]["configs_folder"])


    @loggingInfo
    def saveConfig(self):
        self.config.write()
