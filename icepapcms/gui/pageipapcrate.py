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
from ..helpers import loggingInfo
from .icepapdriverwidget import IcePapDriverWidget


class PageiPapCrate(QtWidgets.QWidget):
    log = logging.getLogger('{}.PageiPapCrate'.format(__name__))

    @loggingInfo
    def __init__(self, mainwin):
        QtWidgets.QWidget.__init__(self, None)
        self.mainwin = mainwin
        self.vboxlayout = QtWidgets.QVBoxLayout(self)
        # TODO check if the margin is for all
        self.vboxlayout.setContentsMargins(9, 9, 9, 9)
        self.vboxlayout.setSpacing(6)

        self.tableWidget = QtWidgets.QTableWidget(self)
        palette = QtGui.QPalette()

        # Configure Palette Color Active
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

        # Configure Palette Color Inactive
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

        # Configure Palette Color Disabled
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
        self.tableWidget.setMinimumSize(QtCore.QSize(40, 248))
        self.tableWidget.setMaximumSize(QtCore.QSize(112333, 248))

        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)
        self.vboxlayout.addWidget(self.tableWidget)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)

    @loggingInfo
    def fillData(self, icepap_system, selected_crate):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setUpdatesEnabled(False)
        self.tableWidget.verticalHeader().setUpdatesEnabled(False)

        for i in range(8):
            headerItem = QtWidgets.QTableWidgetItem()
            headerItem.setText(str(i + 1))
            self.tableWidget.setHorizontalHeaderItem(i, headerItem)
            self.tableWidget.horizontalHeader().resizeSection(i, 94)
            self.tableWidget.horizontalHeader().setSectionResizeMode(
                i, Qt.QHeaderView.Custom)

        self.icepap_system = icepap_system
        self.cratenr = selected_crate
        self.driverswidgets = {}
        crate = -1
        row = 0
        """ TO-DO STORM review"""
        for driver in icepap_system.getDrivers():
            addr = driver.addr
            if driver.cratenr == selected_crate:
                crate = driver.cratenr
                self.tableWidget.insertRow(row)
                headerItem = QtWidgets.QTableWidgetItem()
                headerItem.setText("Crate %d" % crate)
                self.tableWidget.setVerticalHeaderItem(row, headerItem)
                self.tableWidget.verticalHeader().resizeSection(row, 200)
                self.tableWidget.verticalHeader().setSectionResizeMode(
                    row, Qt.QHeaderView.Custom)
                for drivernr in range(8):
                    addr = crate * 10 + drivernr + 1
                    adriver = icepap_system.getDriver(
                        crate * 10 + drivernr + 1)
                    if adriver is not None:
                        wdriver = IcePapDriverWidget(self)
                        wdriver.fillData(adriver)
                        self.driverswidgets[addr] = wdriver
                        self.tableWidget.setCellWidget(row, drivernr, wdriver)
                        wdriver.icepapDoubleClicked.connect(
                            self.driverDoubleclick)
                break

        self.tableWidget.horizontalHeader().setUpdatesEnabled(True)
        self.tableWidget.verticalHeader().setUpdatesEnabled(True)

    @loggingInfo
    def driverDoubleclick(self, driver):
        if driver is not None:
            location = "%s/%d/%d" % (driver.icepapsystem_name,
                                     driver.cratenr, driver.drivernr)
            self.mainwin.treeSelectByLocation(location)

    @loggingInfo
    def refresh(self):
        for col in range(self.tableWidget.columnCount()):
            for row in range(self.tableWidget.rowCount()):
                driver_widget = self.tableWidget.cellWidget(row, col)
                if driver_widget is not None:
                    if not driver_widget.refresh():
                        return


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    w = PageiPapCrate(main_window)
    w.show()
    sys.exit(app.exec_())