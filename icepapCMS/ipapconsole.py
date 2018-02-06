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


import sys
from PyQt4 import QtGui
from ui_icepapcms import ipapconsole


def main():
    app = QtGui.QApplication(sys.argv)
    console = ipapconsole.IcepapConsole(None)
    console.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
