from PyQt4 import QtCore, QtGui
from ui_dialogaddlocation import Ui_DialogAddLocation
from qrc_icepapcms import *

class DialogAddLocation(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogAddLocation()
        self.modal = True
        self.ui.setupUi(self)        

    def getData(self):
        name = unicode(self.ui.txtName.text())        
        return name
    def setData(self, name):
        self.ui.txtname.setText(name)
                