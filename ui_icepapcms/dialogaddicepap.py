from PyQt4 import QtCore, QtGui
from ui_dialogaddicepap import Ui_DialogAddIcepap


class DialogAddIcepap(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogAddIcepap()
        self.modal = True
        self.ui.setupUi(self)
        self.ui.txtPort.setText("5000")

    def getData(self):
        host = str(self.ui.txtHost.text())
        port = str(self.ui.txtPort.text())
        desc = str(self.ui.txtDescription.toPlainText())
        return [host, port, desc]
    
    def setData(self, name, host, port, description):
        self.ui.txtHost.setEnabled(False)
        self.ui.txtPort.setEnabled(False)
        self.ui.txtHost.setText(host)
        self.ui.txtPort.setText(port)
        self.ui.txtDescription.insertPlainText(description)
        