from PyQt4 import QtCore, QtGui, Qt
from ui_dialoghistoriccfg import Ui_DialogHistoricCfg
from messagedialogs import MessageDialogs
import datetime, time
import os
import sys
from xml.dom import minidom, Node

class DialogHistoricCfg(QtGui.QDialog):
    def __init__(self, parent, pagedriver):
        QtGui.QDialog.__init__(self, parent)
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        self.config_template = path+'/templates/driverparameters.xml'
        self.ui = Ui_DialogHistoricCfg()
        self.modal = False
        self.ui.setupUi(self)
        self._pagedriver = pagedriver
        self._driver = None
        
        self.ui.saveButton.setEnabled(True)
        self.ui.loadButton.setEnabled(False)
        self.ui.deleteButton.setEnabled(False)
        QtCore.QObject.connect(self.ui.loadButton, QtCore.SIGNAL("clicked()"),self.loadButton_on_click)
        QtCore.QObject.connect(self.ui.saveButton, QtCore.SIGNAL("clicked()"),self.saveButton_on_click)
        QtCore.QObject.connect(self.ui.deleteButton, QtCore.SIGNAL("clicked()"),self.deleteButton_on_click)
        
    def fillDriverData(self, driver):
        self._driver = driver
        description = "Icepap: %s  -  Crate: %s  -  Addr: %s %s  -  Firmware version: %s\n" % (self._driver.icepap_name, self._driver.cratenr, self._driver.addr, self._driver.name, self._driver.currentCfg.getAttribute("VER"))
        if self._driver.currentCfg.signature:
            aux = self._driver.currentCfg.signature.split('_')
            description = description + "Current configuration signed on %s %s" % (aux[0], time.ctime(float(aux[1])))
        else:
            description = description + "Current configuration not signed"
        self.ui.txtDriverDescription.setText(description)
    
    def loadButton_on_click(self):
        self.loadcfg = self._driver.historicCfg[self.selecteddate]
        self.accept()
        
    def deleteButton_on_click(self):
        if MessageDialogs.showYesNoMessage(self, "Historic configuration", "Delete selected configuration ?"):
            self._driver.deleteHistoricCfg(self.selecteddate)
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
            MessageDialogs.showWarningMessage(self, "Store historic configuration", "Fill all required data.")
        #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if MessageDialogs.showYesNoMessage(self, "Store historic configuration", "Save current configuration ?"):
            self._driver.saveHistoricCfg(str(time.time()), name, desc)
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
        for date, cfg in self._driver.historicCfg.items():
            self.ui.tableWidget.insertRow(row)
            self._addItemToTable(self.ui.tableWidget, row, 1, str(date), False)
            self._addItemToTable(self.ui.tableWidget, row, 0, cfg.name, False)
            row += 1
                
    def _addItemToTable(self, table, row, column, text, editable):
        item = QtGui.QTableWidgetItem()
        item.setText(text)
        if not editable:
            item.setFlags(Qt.Qt.ItemIsSelectable)
        else:
            item.setTextColor(QtGui.QColor(Qt.Qt.red))
        table.setItem(row, column, item)
    
    
    