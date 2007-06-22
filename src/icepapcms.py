import sys
from ui_icepapcms import IcepapCMS
from PyQt4 import QtCore, QtGui
from lib_icepapcms import *
 
ipapcms = None

if __name__ == "__main__":
    sys.argv[0] =  os.path.realpath(sys.argv[0])
    pathname = os.path.dirname(sys.argv[0])
    app = QtGui.QApplication(sys.argv)
    ipapcms = IcepapCMS()
    ipapcms.show()
    sys.exit(app.exec_())          