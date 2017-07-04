from PyQt4 import QtCore, QtGui, Qt

class MessageDialogs:

    def showYesNoMessage(self, parent, caption, question):
        return not QtGui.QMessageBox.question(parent,caption, question, "Yes", "No")
    showYesNoMessage = classmethod(showYesNoMessage)
    
    def showWarningMessage(self, parent, caption, warning):
        QtGui.QMessageBox.warning(parent,caption, warning)
    showWarningMessage = classmethod(showWarningMessage)
    
    def showInformationMessage(self, parent, caption, info):
        QtGui.QMessageBox.information(parent,caption, info)
    showInformationMessage = classmethod(showInformationMessage)
    
    def showErrorMessage(self, parent, caption, error):
        QtGui.QMessageBox.critical(parent,caption, error)
    showErrorMessage = classmethod(showErrorMessage)