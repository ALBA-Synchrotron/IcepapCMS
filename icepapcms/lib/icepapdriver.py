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


from storm.locals import Storm, Int, Unicode, Reference, ReferenceSet
import time
from datetime import datetime
import socket
from icepap import Mode
import logging
from .conflict import Conflict
from .configmanager import ConfigManager
from .icepapsmanager import IcepapsManager
from .stormmanager import StormManager
from ..helpers import loggingInfo


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

    log = logging.getLogger('{}.IcepapDriver'.format(__name__))

    @loggingInfo
    def __init__(self, icepap_name, addr):
        self.icepapsystem_name = str(icepap_name)
        self.addr = addr
        self.current_cfg = None
        self.initialize()

    @loggingInfo
    def __storm_loaded__(self):
        self.current_cfg = self.historic_cfgs.order_by("date").last()
        self.initialize()

    @loggingInfo
    def initialize(self):
        self.drivernr = self.addr % 10
        self.cratenr = self.addr // 10
        self._undo_list = []
        self.startup_cfg = self.current_cfg
        self.conflict = Conflict.NO_CONFLICT

    @loggingInfo
    def addConfiguration(self, cfg, current=True):
        if current:
            if self.current_cfg is not None:
                self._undo_list.append(self.current_cfg)
            else:
                self.startup_cfg = cfg
            self.current_cfg = cfg
            cfg.setDriver(self)
        self.historic_cfgs.add(cfg)

    @loggingInfo
    def setConflict(self, conflict):
        self.conflict = conflict

    @loggingInfo
    def getName(self):
        return self.name

    @loggingInfo
    def setName(self, name):
        self.name = str(name)

    @loggingInfo
    def setMode(self, mode):
        self.mode = str(mode)

    @loggingInfo
    def signDriver(self):
        # AS ESRF SAYS, WHEN SIGNING THE DRIVER CONFIG, THE COMMIT SHOULD
        # BE DONE IN THE DATABASE FIRST, AND IF NO ERRORS, THEN COMMUNICATE
        # THE DRIVER THAT THE VALUES SHOULD BE SIGNED.
        try:
            user = ConfigManager().username
            host = socket.gethostname()
            signature = user + "@" + host + "_" + \
                datetime.now().strftime('%Y/%m/%d_%H:%M:%S')
            IcepapsManager().signDriverConfiguration(
                self.icepapsystem_name, self.addr, signature)
            self.mode = str(Mode.OPER)
            db = StormManager()
            db.commitTransaction()
            self.current_cfg.name = str(time.ctime())
            self.current_cfg.setSignature(signature)
            self.startup_cfg = self.current_cfg
            self.conflict = Conflict.NO_CONFLICT
        except Exception as e:
            self.log.error("some exception while trying to sign the driver %s",
                           e)

    @loggingInfo
    def setStartupCfg(self):
        self.current_cfg = self.startup_cfg
        self.conflict = Conflict.NO_CONFLICT

    @loggingInfo
    def undo(self, config):
        self.addConfiguration(config)
        # THE CURRENT CONFIGURATION SHOULD NOT BE IN THE UNDO LIST
        return self._undo_list.pop()

    @loggingInfo
    def getUndoList(self):
        return self._undo_list.pop()

    @loggingInfo
    def hasUndoList(self):
        return len(self._undo_list) > 0

    @loggingInfo
    def saveHistoricCfg(self, now, name, desc):
        self.current_cfg.name = str(name)
        self.current_cfg.description = str(desc)

    @loggingInfo
    def deleteHistoricCfg(self, cfg):
        self.historic_cfgs.remove(cfg)

    @loggingInfo
    def __ne__(self, other):
        return not self.__eq__(other)

    @loggingInfo
    def __eq__(self, other):
        if self.current_cfg == other.current_cfg:
            self.setConflict(Conflict.NO_CONFLICT)
            return True

        self.setConflict(Conflict.DRIVER_CHANGED)

        return False

    # TO SORT THE ICEPAP DRIVERS IN THE TREE
    @loggingInfo
    def __lt__(self, other):
        if isinstance(other, IcepapDriver):
            return self.addr < other.addr
