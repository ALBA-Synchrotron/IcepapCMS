#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of icepapCMS https://github.com/ALBA-Synchrotron/icepapcms
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


from storm.locals import Storm, Int, Unicode, Reference, ReferenceSet
from .conflict import Conflict
from .configmanager import ConfigManager
from .icepapcontroller import IcepapController
from .stormmanager import StormManager
import time
from datetime import datetime
import socket
from icepap import Mode

__all__ = ['IcepapDriver']


class IcepapDriver(Storm):
    __storm_table__ = "icepapdriver"
    __storm_primary__ = ("icepapsystem_name", "addr")
    icepapsystem_name = Unicode()
    addr = Int()
    name = Unicode()
    mode = Unicode()
    """ references """
    icepap_system = Reference(icepapsystem_name, "IcepapSystem.name")
    historic_cfgs = ReferenceSet((icepapsystem_name, addr),
                                 ("IcepapDriverCfg.icepapsystem_name",
                                  "IcepapDriverCfg.driver_addr"))

    def __init__(self, icepap_name, addr):
        self.icepapsystem_name = str(icepap_name)
        self.addr = addr
        self.current_cfg = None
        self.initialize()

    def __storm_loaded__(self):
        self.current_cfg = self.historic_cfgs.order_by("date").last()
        self.initialize()

    def initialize(self):
        self.drivernr = self.addr % 10
        self.cratenr = self.addr / 10
        self._undo_list = []
        self.startup_cfg = self.current_cfg
        self.conflict = Conflict.NO_CONFLICT

    def addConfiguration(self, cfg, current=True):
        if current:
            if self.current_cfg is not None:
                self._undo_list.append(self.current_cfg)
            else:
                self.startup_cfg = cfg
            self.current_cfg = cfg
            cfg.setDriver(self)
        self.historic_cfgs.add(cfg)

    def setConflict(self, conflict):
        self.conflict = conflict

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = str(name)

    def setMode(self, mode):
        self.mode = str(mode)

    def signDriver(self):
        # AS ESRF SAYS, WHEN SIGNING THE DRIVER CONFIG, THE COMMIT SHOULD
        # BE DONE IN THE DATABASE FIRST, AND IF NO ERRORS, THEN COMMUNICATE
        # THE DRIVER THAT THE VALUES SHOULD BE SIGNED.
        try:
            user = ConfigManager().username
            host = socket.gethostname()
            signature = user + "@" + host + "_" + \
                datetime.now().strftime('%Y/%m/%d_%H:%M:%S')
            IcepapController().signDriverConfiguration(
                self.icepapsystem_name, self.addr, signature)
            self.mode = str(Mode.OPER)
            db = StormManager()
            db.commitTransaction()
            self.current_cfg.name = str(time.ctime())
            self.current_cfg.setSignature(signature)
            self.startup_cfg = self.current_cfg
            self.conflict = Conflict.NO_CONFLICT
        except Exception as e:
            print("some exception while trying to sign the driver", e)

    def setStartupCfg(self):
        self.current_cfg = self.startup_cfg
        self.conflict = Conflict.NO_CONFLICT

    def undo(self, config):
        self.addConfiguration(config)
        # THE CURRENT CONFIGURATION SHOULD NOT BE IN THE UNDO LIST
        return self._undo_list.pop()

    def getUndoList(self):
        return self._undo_list.pop()

    def hasUndoList(self):
        return len(self._undo_list) > 0

    def saveHistoricCfg(self, now, name, desc):
        self.current_cfg.name = str(name)
        self.current_cfg.description = str(desc)

    def deleteHistoricCfg(self, cfg):
        self.historic_cfgs.remove(cfg)

    def __cmp__(self, other):
        if self.current_cfg == other.current_cfg:
            self.setConflict(Conflict.NO_CONFLICT)
            return 0

        self.setConflict(Conflict.DRIVER_CHANGED)

        return -1

    # TO SORT THE ICEPAP DRIVERS IN THE TREE
    def __lt__(self, other):
        if isinstance(other, IcepapDriver):
            return self.addr < other.addr
