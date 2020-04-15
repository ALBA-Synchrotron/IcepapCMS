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

# Led.py
# A led widget for PyQT4
# Author: Josep Joan Ribas Prats
# E-mail: jribas at cells DOT es


import sys
from PyQt4 import QtCore, QtGui
from .Ledqrc import *

class Led(QtGui.QWidget):

    BLUE, GREEN, RED, YELLOW, ORANGE = list(range(5))
    ON, OFF = list(range(2))
    S24, S48 = list(range(2))
    colors = ["ledblueoff", "ledblue", "ledgreenoff", "ledgreen", "ledredoff", "ledred", "ledyellowoff", "ledyellow", "ledorangeoff", "ledorange"]
    directory = [":leds24/images24/", ":/leds48/images48/"]
    def __init__(self, parent = None, ledsize = S24, ledcolor = GREEN):
        

        QtGui.QWidget.__init__(self, parent)
        self.ledsize = ledsize
        if ledsize == Led.S48:
        	lsize = 48
        else:
        	lsize = 24
        self.status = Led.OFF
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
        if self.status == Led.OFF:
	    self.status = Led.ON
            self.label.setPixmap(self.onled)
    
    def off(self):
        if self.status == Led.ON:
	    self.status = Led.OFF
            self.label.setPixmap(self.offled)  
    
    def changeColor(self,LedColor):
        ledoffcolor = int(LedColor) * 2
        ledoncolor = (int(LedColor) * 2 )+ 1  
        self.offled = QtGui.QPixmap(Led.directory[self.ledsize]+Led.colors[ledoffcolor]+".png")
        
        self.onled = QtGui.QPixmap(Led.directory[self.ledsize]+Led.colors[ledoncolor]+".png")
    	if self.status == Led.OFF:
    	     self.status = Led.ON
             self.off()
    	else:
    	     self.status = Led.OFF
    	     self.on() 
        
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
