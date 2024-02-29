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


from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pkg_resources import resource_filename
import logging
from ..helpers import loggingInfo
from .messagedialogs import MessageDialogs
from ..lib.stormmanager import StormManager


class HistoricCfgWidget(QtWidgets.QWidget):
    log = logging.getLogger('{}.HistoricCfgWidget'.format(__name__))

    @loggingInfo
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'historiccfgwidget.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)
        self.icepap_driver = None
        self.selectedCfg = None
        self.allCfgs = {}
        self.filteredCfgs = {}
        self.selectedDay = None

        # Connect Signals
        # self.ui.calendarWidget.clicked.connect(self.daySelected)
        self.ui.listAllCfgs.itemDoubleClicked.connect(self.daySelected)
        self.ui.btnBack.clicked.connect(self.btnBackClicked)
        self.ui.listDayCfgs.currentTextChanged.connect(self.selectCfg)
        self.ui.saveButton.clicked.connect(self.saveButton_on_click)
        self.ui.deleteButton.clicked.connect(self.deleteButton_on_click)
        self.ui.cbxFilter.stateChanged.connect(self.applyFilter)
        self.ui.txtDescription.textChanged.connect(self.descriptionChanged)

    @loggingInfo
    def setCfgPage(self, pagedriver):
        self.pagedriver = pagedriver

    def applyFilter(self, state):
        if self.ui.stackedWidget.currentIndex() == 0:
            self.fillData()
        else:
            self.fillDayCfgs()

    def is_applied_filter(self):
        return self.ui.cbxFilter.checkState() == QtCore.Qt.Checked

    @loggingInfo
    def fillData(self, driver=None):
        """ TO-DO STORM review"""
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.saveButton.setEnabled(False)
        self.ui.deleteButton.setEnabled(False)
        self.ui.txtName.setText("")
        self.ui.txtDescription.setText("")
        if driver is not None:
            self.icepap_driver = driver
            self.selectedCfg = None
            self.selectedDay = None
            self.update_data()

        self.ui.listAllCfgs.clear()
        if self.is_applied_filter():
            cfgdate_list = self.filteredCfgs.keys()
        else:
            cfgdate_list = self.allCfgs.keys()

        for cfgdate in cfgdate_list:
            self.ui.listAllCfgs.addItem(cfgdate)
        self.ui.listAllCfgs.sortItems(QtCore.Qt.DescendingOrder)

    def update_data(self):
        self.allCfgs = {}
        self.filteredCfgs = {}
        for cfg in self.icepap_driver.historic_cfgs:
            datetime = cfg.date
            cfgdate = datetime.strftime("%Y-%m-%d")
            if cfgdate not in self.allCfgs:
                self.allCfgs[cfgdate] = []
            self.allCfgs[cfgdate].append([cfg.date, cfg])
            if cfg.description:
                if cfgdate not in self.filteredCfgs:
                    self.filteredCfgs[cfgdate] = []
                self.filteredCfgs[cfgdate].append([cfg.date, cfg])

    def selectLastCfg(self, driver):
        self.ui.cbxFilter.setCheckState(QtCore.Qt.Unchecked)
        self.fillData(driver)
        self.ui.listAllCfgs.setCurrentRow(0)
        self.daySelected(self.ui.listAllCfgs.item(0))
        self.ui.listDayCfgs.setCurrentRow(0)
        self.selectCfg(self.ui.listDayCfgs.item(0).text())

    @loggingInfo
    def daySelected(self, item):
        self.selectedDay = item.text()
        self.ui.stackedWidget.setCurrentIndex(1)
        self.fillDayCfgs()


    @loggingInfo
    def fillDayCfgs(self):
        self.ui.listDayCfgs.clear()
        self.listDict = {}
        if self.is_applied_filter():
            if self.selectedDay not in self.filteredCfgs:
                self.btnBackClicked()
                return
            cfgs = self.filteredCfgs[self.selectedDay]
        else:
            cfgs = self.allCfgs[self.selectedDay]

        for date, cfg in cfgs:
            key = date.strftime("%Y-%m-%d %H:%M:%S.%f")
            self.listDict[key] = cfg
            self.ui.listDayCfgs.addItem(key)
        self.ui.listDayCfgs.sortItems(QtCore.Qt.DescendingOrder)

    @loggingInfo
    def selectCfg(self, name):
        name = str(name)
        if name in self.listDict:
            self.fillCfgData(self.listDict[name])

    @loggingInfo
    def fillCfgData(self, cfg):
        self.ui.saveButton.setEnabled(True)
        if self.icepap_driver.current_cfg.name == cfg.name:
            self.ui.deleteButton.setEnabled(False)
        else:
            self.ui.deleteButton.setEnabled(True)
        self.selectedCfg = cfg
        self.ui.txtName.setText(cfg.name)
        self.ui.txtDescription.setText(str(cfg.description))
        self.pagedriver.addNewCfg(self.selectedCfg)

    @loggingInfo
    def btnBackClicked(self):
        self.fillData()

    @loggingInfo
    def deleteButton_on_click(self):
        if MessageDialogs.showYesNoMessage(
                self, "Historic configuration",
                "Delete selected configuration ?"):
            self.icepap_driver.deleteHistoricCfg(self.selectedCfg)
            self.update_data()
            self.fillData()
        self.ui.txtName.setText("")
        self.ui.txtDescription.clear()
        self.ui.deleteButton.setEnabled(False)

    @loggingInfo
    def saveButton_on_click(self):
        name = str(self.ui.txtName.text())
        desc = str(self.ui.txtDescription.toPlainText())
        if name == "" or not self.selectedCfg:
            MessageDialogs.showWarningMessage(
                self, "Store historic configuration",
                "Fill all required data.")
            return
        if MessageDialogs.showYesNoMessage(
                self, "Store historic configuration",
                "Save configuration information?"):
            self.selectedCfg.name = name
            self.selectedCfg.description = desc
            db = StormManager()
            db.commitTransaction()
            self.update_data()

    def descriptionChanged(self):
        txt = self.ui.txtDescription.toPlainText()
        if len(txt) > 255:
           MessageDialogs.showWarningMessage(
               self,"Description too long.",
               "Max 254 characters allowed. "
               "Excess characters will be deleted")
           self.ui.txtDescription.setPlainText(txt[:255])


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = HistoricCfgWidget(None)
    w.show()
    sys.exit(app.exec_())