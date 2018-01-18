#!/usr/bin/env python

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

