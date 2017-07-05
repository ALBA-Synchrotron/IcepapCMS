#!/usr/bin/python

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
