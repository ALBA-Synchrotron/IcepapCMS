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

__all__ = ['Singleton']


class Singleton(object):
    def __new__(cls, *p, **k):
        if '_the_instance' not in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            cls._the_instance.init(*p)
        return cls._the_instance

    def init(self, *p):
        pass
