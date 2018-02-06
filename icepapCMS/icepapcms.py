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


import os
import sys
from ui_icepapcms import IcepapApp


def main():
    args = sys.argv
    args[0] = os.path.abspath(__file__)

    # Check env. var.
    ldap = os.environ.get('ICEPAP_LDAP', "")
    all_networks = os.environ.get('ICEPAP_ALL_NETWORKS', "")

    if ldap.lower() == "yes":
        args.append("--ldap")

    if all_networks.lower() == "yes":
        args.append("--all-networks")

    app = IcepapApp(args)

if __name__ == "__main__":
    main()

