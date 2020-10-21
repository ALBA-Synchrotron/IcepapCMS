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
    folder = os.path.expanduser('~/.icepapcms/sqlitedb')
    log_folder = os.path.expanduser('~/.icepapcms/log')
    firmware_folder = os.path.expanduser('~/.icepapcms/firmware')
    configs_folder = os.path.expanduser('~/.icepapcms/configs')
    templates_folder = os.path.expanduser('~/.icepapcms/templates')
    snapshots_folder = os.path.expanduser('~/.icepapcms/snapshots')
    username = 'NotValidated'

    defaults = '''
    [database]
    password = string(default=configure)
    folder = string(default=''' + folder + ''')
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

    def __init__(self):
        pass

    @loggingInfo
    def init(self, *args):
        if not os.path.exists(os.path.expanduser('~/.icepapcms')):
            os.mkdir(os.path.expanduser('~/.icepapcms'))
        self.config_filename = os.path.expanduser(
            '~/.icepapcms/icepapcms.conf')
        self.configure()

    @loggingInfo
    def configure(self):
        self.configspec = ConfigObj(self.defaults)
        self.config = ConfigObj(self.config_filename,
                                configspec=self.configspec)
        vdt = Validator()
        self.config.validate(vdt, copy=True)
        for folder in "log_folder", "firmware_folder", "configs_folder",\
                      "templates_folder", "snapshots_folder":
            directory = self.config["icepap"][folder]
            if not os.path.exists(directory):
                os.mkdir(directory)

    @loggingInfo
    def saveConfig(self):
        self.config.write()
