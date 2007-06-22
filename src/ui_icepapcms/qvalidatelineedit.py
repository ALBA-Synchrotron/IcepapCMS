from PyQt4 import QtCore, QtGui, Qt

class QValidateLineEdit(QtGui.QLineEdit):
    INTEGER, DOUBLE = range(2)
    def __init__(self, parent, type, min, max):
        QtGui.QLineEdit.__init__(self,parent)
        self.type = type
        if type == QValidateLineEdit.INTEGER:
            self.myValidator = QtGui.QIntValidator(int(min),int(max),self)
        elif type == QValidateLineEdit.DOUBLE:
            self.myValidator = QtGui.QDoubleValidator(float(min), float(max), 2, self)
        else:
            self.myValidator = None
    
    
    def keyPressEvent(self,event):       
        QtGui.QLineEdit.keyPressEvent(self,event)
        self.setValidator(self.myValidator)
        if self.validator() <> 0:
            if not self.hasAcceptableInput():
                self.palette().setColor(QtGui.QPalette.Text, QtGui.QColor(Qt.Qt.red))
            else:
                self.palette().setColor(QtGui.QPalette.Text, QtGui.QColor(Qt.Qt.black))
        self.setValidator(None)

    