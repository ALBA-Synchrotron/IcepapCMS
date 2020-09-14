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


from storm.locals import Storm, Int, Unicode, ReferenceSet, Reference, DateTime
import datetime
import logging
from ..helpers import loggingInfo

__all__ = ['IcepapDriverCfg']


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
    icepap_driver = Reference((icepapsystem_name, driver_addr),
                              ("IcepapDriver.icepapsystem_name",
                               "IcepapDriver.addr"))
    parameters = ReferenceSet(id, "CfgParameter.cfg_id")

    log = logging.getLogger('{}.IcepapDriverCfg'.format(__name__))

    @loggingInfo
    def __init__(self, name, description=None):
        if description is None:
            description = str("")
        self.description = str(description)
        self.name = str(name)
        self.date = datetime.datetime.now()
        self.initialize()

    @loggingInfo
    def __storm_loaded__(self):
        self.initialize()
        for cfgpar in self.parameters:
            self._inmemory_parameters[cfgpar.name] = cfgpar

    @loggingInfo
    def initialize(self):
        self._inmemory_parameters = {}

    @loggingInfo
    def setDriver(self, driver):
        self.icepap_driver = driver

    @loggingInfo
    def resetDriver(self):
        self.icepap_driver = None
        self.icepapsystem_name = None
        self.driver_addr = None

    @loggingInfo
    def setSignature(self, signature):
        self.signature = str(signature)

    @loggingInfo
    def getSignature(self):
        return str(self.signature)

    @loggingInfo
    def setParameter(self, name, value):
        name = str(name)
        value = str(value)
        cfgpar = None
        try:
            cfgpar = self.parameters.find(CfgParameter.name == name).one()
        except Exception:
            pass
        if cfgpar is None:
            cfgpar = CfgParameter(self, name, value)
            self.parameters.add(cfgpar)
        else:
            cfgpar.value = value
        self._inmemory_parameters[str(name)] = cfgpar

    @loggingInfo
    def getParameter(self, name, in_memory=False):
        if in_memory:
            if str(name) in self._inmemory_parameters:
                return self._inmemory_parameters[str(name)].value
            else:
                return None
        else:
            cfgpar = self.parameters.find(CfgParameter.name == name).one()
            if cfgpar is not None:
                return cfgpar.value
            else:
                return None

    @loggingInfo
    def toList(self):
        l = []
        for cfgpar in self._inmemory_parameters.values():
            l.append((cfgpar.name, cfgpar.value))
        return l

    @loggingInfo
    def __str__(self):
        text = "Configuration"
        for par in self.parameters:
            text = text + "\n" + par.name + ":\t" + par.value
        return text

    @loggingInfo
    def __ne__(self, other):
        return not self.__eq__(other)

    @loggingInfo
    def __eq__(self, other):
        self_list = self.toList()

        for name, value in self_list:
            other_value = other.getParameter(name, True)
            if name == 'IPAPNAME' or name == 'VER' or name == 'ID':
                pass
            elif other_value is not None:
                if value != other_value:
                    return False
            else:
                return False

        return True


class CfgParameter(Storm):
    __storm_table__ = "cfgparameter"
    __storm_primary__ = ("name", "cfg_id")
    cfg_id = Int()
    name = Unicode()
    value = Unicode()
    """ references """
    driver_cfg = Reference(cfg_id, "IcepapDriverCfg.id")
    log = logging.getLogger('{}.CfgParameter'.format(__name__))

    @loggingInfo
    def __init__(self, cfg, name, value):
        self.driver_cfg = cfg
        self.name = str(name)
        self.value = str(value)
