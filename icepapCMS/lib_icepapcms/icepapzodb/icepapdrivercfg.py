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


from persistent import Persistent

class IcepapDriverCfg(Persistent):
    def __init__(self, parlist= None, name = None, description = None):
        self.parList = {}
        if not parlist == None:
            self.parList = parlist
        self.name = name
        self.description = description
        self.signature = None
    
    def setAttribute(self, name, value):
        self.parList[name] = value
        self._p_changed = True
    
    def getAttribute(self, name):
        return self.parList[name]
    
    def signConfig(self, signature):
        self.signature = signature
    
    def __str__(self):
        text = "Configuration"
        for name, value in self.parList.items():
             text = text + "\n" + name +":\t" +value
        return text
        
    
    def __cmp__(self, other):
        
        if len(other.parList) <> len(self.parList):
            return False
        
        equals = True
        for name, value in self.parList.items():
            if other.parList.has_key(name):
                if not value == other.parList[name]:
                    if name == "SD":
                        x = float(value)
                        y = float(other.parList[name])
                        if abs(x - y) > 3:
                            #print name + " = " + str(x) + " not " + str(y)
                            equals = False
                    else:
                        #print name + " = " + value + " not " + other.parList[name]
                        equals = False
            else:
                return False
                
        return equals
