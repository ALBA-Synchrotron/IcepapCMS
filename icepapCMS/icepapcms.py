#!/usr/bin/env python

import os
import sys
import imp
import ConfigParser
from ui_icepapcms import IcepapApp


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": "YES",
             "y": "YES",
             "no": "NO",
             "n": "NO"}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def main():
    args = sys.argv
    args[0] = os.path.abspath(__file__)
    print args
    home = os.path.expanduser('~')
    icepapcms_ini = os.path.join(home, '.config', 'icepapcms', 'icepapcms.ini')
    config_file = ConfigParser.RawConfigParser()
    if not os.path.isfile(icepapcms_ini):
        directory = os.path.dirname(icepapcms_ini)
        if not os.path.exists(directory):
            os.mkdir(directory)
        print('The configuration file does not exist {0}'.format(icepapcms_ini))
        q = 'Whould you like to use "all_networks" options?'
        default_all_networks = query_yes_no(q)
        q = 'Whould you like to use "ldap" options?'
        default_ldap = query_yes_no(q)
        config_file.add_section('icepapcms')
        config_file.set('icepapcms', 'ldap', default_ldap)
        config_file.set('icepapcms', 'all_networks', default_all_networks)
        with open(icepapcms_ini,'w') as f:
            config_file.write(f)
    else:
        print('Using {0} configuration file'.format(icepapcms_ini))
        config_file.read(icepapcms_ini)
        default_ldap = str(config_file.get('icepapcms', 'ldap'))
        default_all_networks = config_file.get('icepapcms', 'all_networks')

    # Check env. var.
    ldap = os.environ.get('ICEPAP_LDAP', default_ldap)
    all_networks = os.environ.get('ICEPAP_ALL_NETWORKS', default_all_networks)

    if ldap.lower() == "yes":
        args.append("--ldap")

    if all_networks.lower() == "yes":
        args.append("--all-networks")

    app = IcepapApp(args)

if __name__ == "__main__":
    main()

