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
        self.selectedDays = {}

        # Connect Signals
        self.ui.calendarWidget.clicked.connect(self.daySelected)
        self.ui.btnBack.clicked.connect(self.btnBackClicked)
        self.ui.listWidget.currentTextChanged.connect(self.listWidgetChanged)
        self.ui.saveButton.clicked.connect(self.saveButton_on_click)
        self.ui.deleteButton.clicked.connect(self.deleteButton_on_click)

    @loggingInfo
    def setCfgPage(self, pagedriver):
        self.pagedriver = pagedriver

    @loggingInfo
    def fillData(self, driver):
        """ TO-DO STORM review"""
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.saveButton.setEnabled(False)
        self.ui.deleteButton.setEnabled(False)

        for date in self.ui.calendarWidget.dateTextFormat():
            self.ui.calendarWidget.setDateTextFormat(
                date, QtGui.QTextCharFormat())
        self.selectedDays = {}
        self.icepap_driver = driver
        self.ui.txtName.setText("")
        self.ui.txtDescription.setText("")
        for cfg in self.icepap_driver.historic_cfgs:
            datetime = cfg.date

            qdate = QtCore.QDate(datetime.year, datetime.month, datetime.day)
            cfgdate = qdate.toPyDate().ctime()
            if cfgdate in self.selectedDays:
                self.selectedDays[cfgdate].append([cfg.date, cfg])
            else:
                format = QtGui.QTextCharFormat()
                format.setBackground(QtGui.QColor(255, 255, 0))
                self.ui.calendarWidget.setDateTextFormat(qdate, format)
                self.selectedDays[cfgdate] = [[cfg.date, cfg]]
        self.daySelected(self.ui.calendarWidget.selectedDate())

    @loggingInfo
    def daySelected(self, qdate):
        date = qdate.toPyDate().ctime()
        if date in self.selectedDays:
            daylist = self.selectedDays[date]
            if len(daylist) == 1:
                self.fillCfgData(daylist[0])
            else:
                self.ui.stackedWidget.setCurrentIndex(1)
                self.fillDayCfgs(daylist)

    @loggingInfo
    def fillDayCfgs(self, cfgs):
        self.ui.listWidget.clear()
        self.listDict = {}
        for date, cfg in cfgs:
            key = date.ctime()
            self.listDict[key] = [date, cfg]
            self.ui.listWidget.addItem(key)

    @loggingInfo
    def listWidgetChanged(self, name):
        name = str(name)
        if name in self.listDict:
            self.fillCfgData(self.listDict[name])

    @loggingInfo
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

    @loggingInfo
    def btnBackClicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    @loggingInfo
    def deleteButton_on_click(self):
        if MessageDialogs.showYesNoMessage(
                self, "Historic configuration",
                "Delete selected configuration ?"):
            self.icepap_driver.deleteHistoricCfg(self.selectedCfg[1])
            self.fillData(self.icepap_driver)
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
            self.selectedCfg[1].name = name
            self.selectedCfg[1].description = desc


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = HistoricCfgWidget(None)
    w.show()
    sys.exit(app.exec_())