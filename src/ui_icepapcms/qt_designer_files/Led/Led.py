# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unknown'
#
# Created: Fri Jul 21 15:28:08 2006
#      by: PyQt4 UI code generator 4.0
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui
from Ledqrc import *

class Led(QtGui.QWidget):

    BLUE, GREEN, RED, YELLOW, ORANGE = range(5)
    ON, OFF = range(2)
    S24, S48 = range(2)
    colors = ["ledblueoff", "ledblue", "ledgreenoff", "ledgreen", "ledredoff", "ledred", "ledyellowoff", "ledyellowon", "ledorangeoff", "ledorange"]
    directory = [":leds24/images24/", ":/leds48/images48/"]
    def __init__(self, parent = None, ledsize = S24, ledcolor = GREEN):
        

        QtGui.QWidget.__init__(self, parent)
        self.ledsize = ledsize
        if ledsize == Led.S48:
        	lsize = 48
        else:
        	lsize = 24
        
        self.setObjectName("Led")
        self.resize(QtCore.QSize(QtCore.QRect(0,0,lsize,lsize).size()).expandedTo(self.minimumSizeHint()))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(lsize,lsize))
        self.setMaximumSize(QtCore.QSize(lsize,lsize))
        
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0,0,lsize,lsize))
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        
        self.label.setSizePolicy(sizePolicy)
               
        self.label.setObjectName("label")
        self.changeColor(ledcolor)
        
        
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def tr(self, string):
        return QtGui.QApplication.translate("Led", string, None, QtGui.QApplication.UnicodeUTF8)

    def retranslateUi(self, Led):
        Led.setWindowTitle(self.tr("Form"))
    
    def on(self):
        self.status = Led.ON
        self.label.setPixmap(self.onled)
    
    def off(self):
        self.status = Led.OFF
        self.label.setPixmap(self.offled)  
    
    def changeColor(self,LedColor):
        ledoffcolor = int(LedColor) * 2
        ledoncolor = (int(LedColor) * 2 )+ 1  
        self.offled = QtGui.QPixmap(Led.directory[self.ledsize]+Led.colors[ledoffcolor]+".png")
        
        self.onled = QtGui.QPixmap(Led.directory[self.ledsize]+Led.colors[ledoncolor]+".png")

        self.off() 
        
#    def mousePressEvent(self, ev):
#        
#        if self.status == Led.ON:
#            self.off()
#        else:
#            self.on()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    lw = Led(None, Led.S24, Led.ORANGE)
    lw.show()
    sys.exit(app.exec_())
