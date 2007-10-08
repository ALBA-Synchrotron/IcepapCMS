from PyQt4 import QtCore, QtGui
from ui_dialogaddicepap import Ui_DialogAddIcepap
from lib_icepapcms import MainManager

class DialogAddIcepap(QtGui.QDialog):
    def __init__(self, parent, location):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogAddIcepap()
        self.modal = True
        self.ui.setupUi(self)
        self.ui.txtPort.setText("5000")
        self.buildLocationCombo(location)                
        
    
    def buildLocationCombo(self, location):        
        for location_name in MainManager().locationList.keys():
            self.ui.cbLocation.addItem(location_name)
        self.ui.cbLocation.setCurrentIndex(self.ui.cbLocation.findText(location, QtCore.Qt.MatchFixedString))  

    def getData(self):
        host = unicode(self.ui.txtHost.text())
        port = unicode(self.ui.txtPort.text())
        desc = unicode(self.ui.txtDescription.toPlainText())
        location = unicode(self.ui.cbLocation.currentText())
        return [host, port, desc, location]
    
    def setData(self, name, host, port, description, location):
        self.ui.txtHost.setEnabled(False)
        self.ui.txtPort.setEnabled(False)
        self.ui.txtHost.setText(host)
        self.ui.txtPort.setText(str(port))
        self.ui.txtDescription.insertPlainText(description)
        self.ui.cbLocation.setCurrentIndex(self.ui.cbLocation.findText(location, QtCore.Qt.MatchFixedString))
        