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

__all__ = ['Conflict']


class Conflict:
    NO_CONFLICT, DRIVER_NOT_PRESENT, NEW_DRIVER, DRIVER_CHANGED, \
        NO_CONNECTION, DRIVER_CFG, DRIVER_MOVED, DRIVER_FROM_DB, \
        DRIVER_AUTOSOLVE, DRIVER_AUTOSOLVE_EXPERT = list(range(10))
