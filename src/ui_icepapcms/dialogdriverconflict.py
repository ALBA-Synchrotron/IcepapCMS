from PyQt4 import QtCore, QtGui, Qt
from ui_dialogdriverconflict import Ui_DialogDriverConflict
from messagedialogs import MessageDialogs
from lib_icepapcms import MainManager
from xml.dom import minidom, Node
import os
import sys


class DialogDriverConflict(QtGui.QDialog):
    def __init__(self, parent, driver):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogDriverConflict()
        self.modal = True
        self.ui.setupUi(self)
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        self.config_template = path+'/templates/driverparameters.xml'
        self._driver = driver
        self._manager = MainManager()
        self.ui.tableWidget.horizontalHeader().setResizeMode(0, Qt.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setResizeMode(1, Qt.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setResizeMode(2, Qt.QHeaderView.Stretch)
        self._fillTable()
        QtCore.QObject.connect(self.ui.btnStored, QtCore.SIGNAL("clicked()"),self.btnStored_on_click)
        QtCore.QObject.connect(self.ui.btnIcepap, QtCore.SIGNAL("clicked()"),self.btnIcepap_on_click)
        
        
    def _createTableView(self):
        self.var_dict = {}
        doc = minidom.parse(self.config_template)
        root  = doc.documentElement
        row = 0
        for section in root.getElementsByTagName("section"):
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    self.ui.tableWidget.insertRow(row)
                    parname =  pars.attributes.get('name').value
                    parname = parname.strip()
                    self.var_dict[parname] = row
                    self._addItemToTable(row, 0, parname, False)
    
    def _fillTable(self):
        self._createTableView()
        self.icepap_values = self._manager.getDriverConfiguration(self._driver.icepap_name, self._driver.addr)
        row = 0
        current = False
        
        for row in range(self.ui.tableWidget.rowCount()):
            name = str(self.ui.tableWidget.item(row,0).text())

            if self._driver.currentCfg.parList.has_key(name):
                stored_value = self._driver.currentCfg.parList[name]
            else:
                stored_value = ""
            
            if self.icepap_values.parList.has_key(name):
                icepap_value = self.icepap_values.parList[name]
            else:
                icepap_value = ""
            color = False
            
            if name == "SD":
                x = float(stored_value)
                y = float(icepap_value)
                if abs(x - y) > 3:
                    color = True
            elif stored_value <> icepap_value:
                color = True
                if name == "IN" or name == "II" or name == "IB":
                    current = True
                   
            self._addItemToTable(row, 1, stored_value, color)
            self._addItemToTable(row, 2, icepap_value, color)
        
        if current:
            MessageDialogs.showWarningMessage(self, "Driver conflict", "Warning!!\nCurrent values (IN, IB, II) have changed!!\n")
    
    def btnIcepap_on_click(self):
        self._driver.setConfiguration(self.icepap_values)
        self.accept()
    
    def btnStored_on_click(self):
        self._manager.saveValuesInIcepap(self._driver, self._driver.currentCfg.parList.items())
        self.accept()
           
    def _addItemToTable(self, row, column, text, colored):
        item = QtGui.QTableWidgetItem()
        item.setText(text)
        item.setFlags(Qt.Qt.ItemIsSelectable)
        if colored:
            item.setTextColor(QtGui.QColor(Qt.Qt.red))
        self.ui.tableWidget.setItem(row, column, item)
    
    
    