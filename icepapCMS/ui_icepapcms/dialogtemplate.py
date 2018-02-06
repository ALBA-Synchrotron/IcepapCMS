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
from ui_dialoghistoriccfg import Ui_DialogHistoricCfg
from messagedialogs import MessageDialogs
from  lib_icepapcms import MainManager
import os
import sys
from xml.dom import minidom, Node

class DialogTemplate(QtGui.QDialog):
    def __init__(self, parent, driver):
        QtGui.QDialog.__init__(self, parent)
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        self.config_template = path+'/templates/driverparameters.xml'
        self.ui = Ui_DialogHistoricCfg()
        self.modal = True
        self.ui.setupUi(self)
        self._driver = driver
        self.setObjectName("DialogTemplate")
        self.setWindowTitle(self.tr("Driver templates"))
        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(self.tr("Description"))
        self.ui.tableWidget.setHorizontalHeaderItem(1,headerItem)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self._manager = MainManager()
        self._templateList = self._manager.getDriverTemplateList()
        self.ui.tableWidgetCfg.horizontalHeader().setResizeMode(0, Qt.QHeaderView.Stretch)
        self.ui.tableWidgetCfg.horizontalHeader().setResizeMode(1, Qt.QHeaderView.Stretch)
        self._createTableCfgView()
        self._fillTable()
        self._fillTableCfg(self._driver.currentCfg)
        self.ui.saveButton.setEnabled(True)
        self.ui.loadButton.setEnabled(False)
        self.ui.deleteButton.setEnabled(False)
        QtCore.QObject.connect(self.ui.loadButton, QtCore.SIGNAL("clicked()"),self.loadButton_on_click)
        QtCore.QObject.connect(self.ui.saveButton, QtCore.SIGNAL("clicked()"),self.saveButton_on_click)
        QtCore.QObject.connect(self.ui.deleteButton, QtCore.SIGNAL("clicked()"),self.deleteButton_on_click)
        QtCore.QObject.connect(self.ui.tableWidget, QtCore.SIGNAL("cellClicked(int,int)"),self.tableCell_on_click)
        
    def _createTableCfgView(self):
        doc = minidom.parse(self.config_template)
        root  = doc.documentElement
        row = 0
        for section in root.getElementsByTagName("section"):
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    self.ui.tableWidgetCfg.insertRow(row)
                    parname =  pars.attributes.get('name').value
                    parname = parname.strip()
                    self._addItemToTable(self.ui.tableWidgetCfg, row, 0, parname, False)
                    row +=1
                    
    def tableCell_on_click(self, row, col):
        self.templatename = str(self.ui.tableWidget.item(row, 0).text())
        template = self._templateList[self.templatename]
        self.ui.txtName.setText(template.name)
        self.ui.txtDescription.clear()
        self.ui.txtDescription.insertPlainText(template.description)
        self.ui.saveButton.setEnabled(False)
        self.ui.txtName.setEnabled(False)
        self.ui.txtDescription.setEnabled(False)
        self.ui.loadButton.setEnabled(True)
        self.ui.deleteButton.setEnabled(True)
        self._fillTableCfg(template.cfg)
        
        
    def loadButton_on_click(self):
        template = self._templateList[self.templatename]
        self.loadcfg = template.cfg
        self.accept()
        
    def deleteButton_on_click(self):
        if MessageDialogs.showYesNoMessage(self, "Historic configuration", "Delete selected configuration ?"):
            self._manager.deleteDriverTemplate(self.templatename)
        self.ui.txtName.setText("")
        self.ui.txtDescription.clear()
        self._fillTable()
        self.selecteddate = ""
        for row in range(self.ui.tableWidgetCfg.rowCount()):
            self.ui.tableWidgetCfg.item(row,1).setText("")
        self.ui.loadButton.setEnabled(False)
        self.ui.deleteButton.setEnabled(False)
        
        
    def saveButton_on_click(self):
        name = str(self.ui.txtName.text())
        desc = str(self.ui.txtDescription.toPlainText())
        if name == "":
            MessageDialogs.showWarningMessage(self, "Driver template", "Fill all required data.")
        else:
            if self._templateList.has_key(name):
                MessageDialogs.showWarningMessage(self, "Driver template", "Choose another template name.")
            elif MessageDialogs.showYesNoMessage(self, "Store template configuration", "Save current configuration ?"):
                self._manager.saveDriverTemplate(name, desc, self._driver.currentCfg)
                self.close()
        
    def _fillTableCfg(self,cfg):
        for row in range(self.ui.tableWidgetCfg.rowCount()):
            name = str(self.ui.tableWidgetCfg.item(row,0).text())
            if self._driver.currentCfg.parList.has_key(name):
                stored_value = cfg.parList[name]
            else:
                stored_value = ""
            self._addItemToTable(self.ui.tableWidgetCfg, row, 1, stored_value, False)
            
    def _fillTable(self):
        self.ui.tableWidget.setRowCount(0)
        row = 0
        for name, template in self._templateList.items():
            self.ui.tableWidget.insertRow(row)
            self._addItemToTable(self.ui.tableWidget, row, 0, name, False)
            self._addItemToTable(self.ui.tableWidget, row, 1, template.description, False)
            row += 1
                
    def _addItemToTable(self, table, row, column, text, editable):
        item = QtGui.QTableWidgetItem()
        item.setText(text)
        if not editable:
            item.setFlags(Qt.Qt.ItemIsSelectable)
        else:
            item.setTextColor(QtGui.QColor(Qt.Qt.red))
        table.setItem(row, column, item)
    
    
    