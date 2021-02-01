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

from PyQt5 import QtCore, QtGui, Qt, QtWidgets
import logging
from .icepapdriverwidget import IcePapDriverWidget
from ..helpers import loggingInfo


class PageiPapSystem(QtWidgets.QWidget):
    log = logging.getLogger('{}.PageiPapSystem'.format(__name__))

    @loggingInfo
    def __init__(self, mainwin):
        QtWidgets.QWidget.__init__(self, None)
        self._colSize = [94, 94]
        self._rowSize = [74, 200]
        self.mainwin = mainwin
        self.hboxlayout = QtWidgets.QVBoxLayout(self)
        self.hboxlayout.setContentsMargins(9, 9, 9, 9)
        self.hboxlayout.setSpacing(6)
        self.cmbIconSize = QtWidgets.QComboBox()
        self.cmbIconSize.addItems(["Big icons", "Small Icons"])
        self.cmbIconSize.setMaximumWidth(100)
        self.hboxlayout.addWidget(self.cmbIconSize)

        self.tableWidget = QtWidgets.QTableWidget(self)
        palette = QtGui.QPalette()
        # Palette Active colors
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(0),
                         QtGui.QColor(16, 16, 16))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(1),
                         QtGui.QColor(226, 228, 252))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(2),
                         QtGui.QColor(237, 237, 237))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(3),
                         QtGui.QColor(247, 245, 243))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(4),
                         QtGui.QColor(119, 117, 115))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(5),
                         QtGui.QColor(159, 157, 154))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(6),
                         QtGui.QColor(16, 16, 16))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(7),
                         QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(8),
                         QtGui.QColor(16, 16, 16))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(9),
                         QtGui.QColor(239, 235, 231))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(10),
                         QtGui.QColor(239, 235, 231))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(11),
                         QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(12),
                         QtGui.QColor(101, 148, 235))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(13),
                         QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(14),
                         QtGui.QColor(0, 0, 255))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(15),
                         QtGui.QColor(255, 0, 255))
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.ColorRole(16),
                         QtGui.QColor(247, 245, 243))

        # Palette Inactive colors
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(0),
                         QtGui.QColor(16, 16, 16))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(1),
                         QtGui.QColor(226, 228, 252))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(2),
                         QtGui.QColor(237, 237, 237))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(3),
                         QtGui.QColor(247, 245, 243))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(4),
                         QtGui.QColor(119, 117, 115))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(5),
                         QtGui.QColor(159, 157, 154))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(6),
                         QtGui.QColor(16, 16, 16))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(7),
                         QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(8),
                         QtGui.QColor(16, 16, 16))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(9),
                         QtGui.QColor(239, 235, 231))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(10),
                         QtGui.QColor(239, 235, 231))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(11),
                         QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(12),
                         QtGui.QColor(101, 148, 235))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(13),
                         QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(14),
                         QtGui.QColor(0, 0, 255))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(15),
                         QtGui.QColor(255, 0, 255))
        palette.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.ColorRole(16),
                         QtGui.QColor(247, 245, 243))

        # Palette Disabled colors
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(0),
                         QtGui.QColor(127, 125, 123))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(1),
                         QtGui.QColor(226, 228, 252))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(2),
                         QtGui.QColor(237, 237, 237))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(3),
                         QtGui.QColor(247, 245, 243))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(4),
                         QtGui.QColor(119, 117, 115))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(5),
                         QtGui.QColor(159, 157, 154))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(6),
                         QtGui.QColor(127, 125, 123))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(7),
                         QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(8),
                         QtGui.QColor(127, 125, 123))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(9),
                         QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(10),
                         QtGui.QColor(239, 235, 231))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(11),
                         QtGui.QColor(0, 0, 0))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(12),
                         QtGui.QColor(84, 123, 196))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(13),
                         QtGui.QColor(255, 255, 255))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(14),
                         QtGui.QColor(0, 0, 255))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(15),
                         QtGui.QColor(255, 0, 255))
        palette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ColorRole(16),
                         QtGui.QColor(247, 245, 243))
        self.tableWidget.setPalette(palette)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.hboxlayout.addWidget(self.tableWidget)
        self.cmbIconSize.currentIndexChanged.connect(self.changeSize)
        self.icepap_system = None

    @loggingInfo
    def fillData(self, icepap_system):
        """ TO-DO STORM review"""
        if self.icepap_system == icepap_system:
            self.refresh()
            return
        size = not(self.cmbIconSize.currentIndex())
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setUpdatesEnabled(False)
        self.tableWidget.verticalHeader().setUpdatesEnabled(False)

        for i in range(8):
            headerItem = QtWidgets.QTableWidgetItem()
            headerItem.setText(str(i + 1))
            self.tableWidget.setHorizontalHeaderItem(i, headerItem)
            self.tableWidget.horizontalHeader().resizeSection(
                i, self._colSize[size])

            self.tableWidget.horizontalHeader().setSectionResizeMode(
                i, Qt.QHeaderView.Custom)

        self.icepap_system = icepap_system
        self.driverswidgets = {}
        crate = -1
        row = 0
        for driver in icepap_system.getDrivers():
            if driver.cratenr != crate:
                crate = driver.cratenr
                self.tableWidget.insertRow(row)
                headerItem = QtWidgets.QTableWidgetItem()
                headerItem.setText("Crate %d" % crate)
                self.tableWidget.setVerticalHeaderItem(row, headerItem)
                self.tableWidget.verticalHeader().resizeSection(
                    row, self._rowSize[size])
                self.tableWidget.verticalHeader().setSectionResizeMode(
                    row, Qt.QHeaderView.Custom)

                for drivernr in range(8):
                    addr = crate * 10 + drivernr + 1
                    adriver = icepap_system.getDriver(
                        crate * 10 + drivernr + 1)
                    if adriver is not None:
                        wdriver = IcePapDriverWidget(self, size)
                        wdriver.fillData(adriver)
                        self.driverswidgets[addr] = wdriver
                        self.tableWidget.setCellWidget(row, drivernr, wdriver)
                        wdriver.icepapDoubleClicked.connect(
                            self.driverDoubleclick)
                row += 1

        self.tableWidget.horizontalHeader().setUpdatesEnabled(True)
        self.tableWidget.verticalHeader().setUpdatesEnabled(True)

    @loggingInfo
    def driverDoubleclick(self, driver):
        if driver is not None:
            location = "%s/%d/%d" % (driver.icepapsystem_name,
                                     driver.cratenr, driver.drivernr)
            self.mainwin.locationsPrevious.extend(self.mainwin.locationsNext)
            self.mainwin.locationsNext = []
            self.mainwin.addToPrevious(self.mainwin.currentLocation)
            self.mainwin.treeSelectByLocation(location)

    @loggingInfo
    def changeSize(self, index):
        self.refresh(not(index))

    @loggingInfo
    def refresh(self, size=None):
        self.tableWidget.setUpdatesEnabled(False)
        self.tableWidget.horizontalHeader().setUpdatesEnabled(False)
        self.tableWidget.verticalHeader().setUpdatesEnabled(False)
        for col in range(self.tableWidget.columnCount()):
            for row in range(self.tableWidget.rowCount()):
                driver_widget = self.tableWidget.cellWidget(row, col)
                if driver_widget is not None:
                    if size is not None:
                        driver = driver_widget.getDriver()
                        driver_widget = IcePapDriverWidget(self, size)
                        driver_widget.fillData(driver)
                        if not driver_widget.fillData(driver):
                            return
                        driver_widget.show()
                        self.tableWidget.setCellWidget(row, col, driver_widget)
                        driver_widget.icepapDoubleClicked.connect(
                            self.driverDoubleclick)

                    else:
                        if not driver_widget.refresh():
                            break
        if size is not None:
            for col in range(self.tableWidget.columnCount()):
                self.tableWidget.horizontalHeader().resizeSection(
                    col, self._colSize[size])
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.verticalHeader().resizeSection(
                    row, self._rowSize[size])
        self.tableWidget.setUpdatesEnabled(True)
        self.tableWidget.horizontalHeader().setUpdatesEnabled(True)
        self.tableWidget.verticalHeader().setUpdatesEnabled(True)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    w = PageiPapSystem(main_window)
    w.show()
    sys.exit(app.exec_())