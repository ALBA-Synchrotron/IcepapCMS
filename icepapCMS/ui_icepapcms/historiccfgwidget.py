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


from PyQt4 import QtCore, QtGui, Qt
from ui_historiccfgwidget import Ui_HistoricCfgWidget
from messagedialogs import MessageDialogs
import datetime, time
import os
import sys
from qrc_icepapcms import *

class HistoricCfgWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_HistoricCfgWidget()
        self.ui.setupUi(self)
        self.icepap_driver = None
        self.selectedCfg = None
        self.selectedDays = {}
        
        QtCore.QObject.connect(self.ui.calendarWidget, QtCore.SIGNAL("clicked(const QDate&)"),self.daySelected)
        QtCore.QObject.connect(self.ui.btnBack, QtCore.SIGNAL("clicked()"),self.btnBackClicked)
        QtCore.QObject.connect(self.ui.listWidget, QtCore.SIGNAL("currentTextChanged (const QString&)"),self.listWidgetChanged)
        QtCore.QObject.connect(self.ui.saveButton, QtCore.SIGNAL("clicked()"),self.saveButton_on_click)
        QtCore.QObject.connect(self.ui.deleteButton, QtCore.SIGNAL("clicked()"),self.deleteButton_on_click)
    
    def setCfgPage(self, pagedriver):
        self.pagedriver = pagedriver
        
    def fillData(self, driver):
        """ TO-DO STORM review"""
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.saveButton.setEnabled(False)
        self.ui.deleteButton.setEnabled(False)
        
        for date in self.ui.calendarWidget.dateTextFormat():
            self.ui.calendarWidget.setDateTextFormat(date, QtGui.QTextCharFormat())
        self.selectedDays = {}
        self.icepap_driver = driver
        self.ui.txtName.setText("")
        self.ui.txtDescription.setText("")
        for cfg in self.icepap_driver.historic_cfgs:
            datetime = cfg.date            
            
            qdate = QtCore.QDate(datetime.year,datetime.month,datetime.day)
            cfgdate = qdate.toPyDate().ctime()
            if self.selectedDays.has_key(cfgdate):
                self.selectedDays[cfgdate].append([cfg.date, cfg])
            else:
                format=QtGui.QTextCharFormat()
                format.setBackground(QtGui.QColor(255,255,0))
                self.ui.calendarWidget.setDateTextFormat(qdate, format)
                self.selectedDays[cfgdate] = [[cfg.date, cfg]]
        self.daySelected(self.ui.calendarWidget.selectedDate())
    
    def daySelected(self, qdate):
        date = qdate.toPyDate().ctime()
        if self.selectedDays.has_key(date):
            daylist = self.selectedDays[date]
            if len(daylist) == 1:
                self.fillCfgData(daylist[0])
            else:
                self.ui.stackedWidget.setCurrentIndex(1)
                self.fillDayCfgs(daylist)
                
    def fillDayCfgs(self,cfgs):
        self.ui.listWidget.clear()
        self.listDict = {}
        for date, cfg in cfgs:
            key = date.ctime()
            self.listDict[key] = [date, cfg]
            self.ui.listWidget.addItem(key)
            
    def listWidgetChanged(self, name):
        name = str(name)
        if self.listDict.has_key(name): 
            self.fillCfgData(self.listDict[name])
    
    def fillCfgData(self, cfg):
        self.ui.saveButton.setEnabled(True)
        if self.icepap_driver.current_cfg.name == cfg[1].name:
            self.ui.deleteButton.setEnabled(False)
        else:
            self.ui.deleteButton.setEnabled(True)
        self.selectedCfg = cfg
        self.ui.txtName.setText(cfg[1].name)
        self.ui.txtDescription.setText(str(cfg[1].description))
        self.pagedriver.addNewCfg(self.selectedCfg[1])
    
    def btnBackClicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    
    
    def deleteButton_on_click(self):
        if MessageDialogs.showYesNoMessage(self, "Historic configuration", "Delete selected configuration ?"):
            self.icepap_driver.deleteHistoricCfg(self.selectedCfg[1])
            self.fillData(self.icepap_driver)
        self.ui.txtName.setText("")
        self.ui.txtDescription.clear()
        self.ui.deleteButton.setEnabled(False)
        
    def saveButton_on_click(self):
        name = unicode(self.ui.txtName.text())
        desc = unicode(self.ui.txtDescription.toPlainText())
        if name == "" or not self.selectedCfg:
            MessageDialogs.showWarningMessage(self, "Store historic configuration", "Fill all required data.")
            return
        if MessageDialogs.showYesNoMessage(self, "Store historic configuration", "Save configuration information?"):
            self.selectedCfg[1].name = name
            self.selectedCfg[1].description = desc

        
        
        
    
            