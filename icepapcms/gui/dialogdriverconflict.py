#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of icepapcms https://github.com/ALBA-Synchrotron/icepapcms
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


from PyQt5 import QtWidgets, QtGui, Qt, uic
from pkg_resources import resource_filename
from xml.dom import minidom, Node
import logging
from .messagedialogs import MessageDialogs
from ..lib import MainManager, StormManager
from ..helpers import loggingInfo


class DialogDriverConflict(QtWidgets.QDialog):
    log = logging.getLogger('{}.DialogDriverConflict'.format(__name__))

    @loggingInfo
    def __init__(self, parent, driver, test_mode=False):
        QtWidgets.QDialog.__init__(self, parent)

        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'dialogdriverconflict.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)
        self.modal = True
        font = QtGui.QFont()
        font.setPointSize(7.5)
        self.setFont(font)
        self.config_template = resource_filename('icepapcms.templates',
                                                 'driverparameters.xml')
        if test_mode:
            return
        self._driver = driver
        self._manager = MainManager()
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(
            0, Qt.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(
            1, Qt.QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(
            2, Qt.QHeaderView.Stretch)
        self._fillTable()

        # Connect Signals
        self.ui.btnStored.clicked.connect(self.btnStored_on_click)
        self.ui.btnIcepap.clicked.connect(self.btnIcepap_on_click)

    @loggingInfo
    def _createTableView(self):
        self.var_dict = {}
        doc = minidom.parse(self.config_template)
        root = doc.documentElement
        row = 0
        for section in root.getElementsByTagName("section"):
            if section.nodeType == Node.ELEMENT_NODE:
                section_name = section.attributes.get('name').value
            inTestSection = (section_name == "test")
            if inTestSection:
                return
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    self.ui.tableWidget.insertRow(row)
                    parname = pars.attributes.get('name').value
                    parname = parname.strip()
                    self.var_dict[parname] = row
                    self._addItemToTable(row, 0, parname, False)
                    row = row + 1

    @loggingInfo
    def _fillTable(self):
        self._createTableView()
        self.icepap_values = self._manager.getDriverConfiguration(
            self._driver.icepapsystem_name, self._driver.addr)
        row = 0
        current = False

        for row in range(self.ui.tableWidget.rowCount()):
            name = str(self.ui.tableWidget.item(row, 0).text())

            if name == "NAME":
                name = str("IPAPNAME")

            stored_value = self._driver.current_cfg.getParameter(name, True)
            if stored_value is None:
                stored_value = ""

            icepap_value = self.icepap_values.getParameter(name, True)
            if icepap_value is None:
                icepap_value = ""
            color = stored_value != icepap_value

            self._addItemToTable(row, 1, stored_value, color)
            self._addItemToTable(row, 2, icepap_value, color)

        if current:
            MessageDialogs.showWarningMessage(
                self, "Driver conflict",
                "Warning!!\nCurrent values (IN, IB, II) have changed!!\n")

    @loggingInfo
    def btnIcepap_on_click(self):
        db = StormManager()
        db.store(self.icepap_values)
        # bug sqlite
        self._driver.addConfiguration(self.icepap_values)
        self.accept()

    @loggingInfo
    def btnStored_on_click(self):
        del self.icepap_values
        self._manager.saveValuesInIcepap(self._driver,
                                         self._driver.current_cfg.toList())
        self.accept()

    @loggingInfo
    def _addItemToTable(self, row, column, text, colored):
        item = QtWidgets.QTableWidgetItem()
        item.setText(text)
        item.setFlags(Qt.Qt.ItemIsSelectable)
        if colored:
            item.setTextColor(QtGui.QColor(Qt.Qt.red))
        self.ui.tableWidget.setItem(row, column, item)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = DialogDriverConflict(None, None, True)
    w.show()
    sys.exit(app.exec_())