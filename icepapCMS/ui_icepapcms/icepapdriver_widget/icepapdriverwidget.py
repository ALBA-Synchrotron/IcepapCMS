#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of icepapCMS https://github.com/ALBA-Synchrotron/icepapcms
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------


from PyQt4 import QtCore, QtGui, Qt
from .ui_icepapdriverwidget import Ui_IcePapDriverWidget
from .ui_icepapdriverwidgetsmall import Ui_IcePapDriverWidgetSmall
# from ...ui_icepapcms.qrc_icepapcms import *
from ...ui_icepapcms.Led import Led
from ...lib_icepapcms import MainManager, Conflict
from icepap import Mode, State


class IcePapDriverWidget(QtGui.QWidget):
    def __init__(self, parent=None, BigSize=True):
        QtGui.QWidget.__init__(self, parent)
        self.initView(BigSize)
        self.MaxCurrent = 7
        self._driver = None
        self.setMouseTracking(True)
        self.status = -1
        self.ready = -1
        self.power = -1
        self.mode = -1

    def initView(self, Big):
        self.BigSize = Big
        self.coloroff = QtGui.QColor(225, 255, 200)
        self.colorerror = QtGui.QColor(255, 179, 179)
        self.colorok = QtGui.QColor(223, 223, 237)
        self.colorwarning = QtGui.QColor(255, 255, 0)
        self.colorconfig = QtGui.QColor(255, 206, 162)

        if Big:
            self.ui = Ui_IcePapDriverWidget()
            self.ui.setupUi(self)
            self.setPaletteColor(self.ui.lcdCurrent, self.coloroff,
                                 QtGui.QColor(Qt.Qt.white))
        else:
            self.ui = Ui_IcePapDriverWidgetSmall()
            self.ui.setupUi(self)

        self.ui.ledStatus.changeColor(Led.YELLOW)
        self.ui.ledLimitPos.changeColor(Led.ORANGE)
        self.ui.ledLimitNeg.changeColor(Led.GREEN)
        self._manager = MainManager()

        self.setAutoFillBackground(True)

        QtCore.QObject.connect(self.ui.pushButton,
                               QtCore.SIGNAL("clicked(""bool)"),
                               self.btnEnDis_on_click)

    def mouseDoubleClickEvent(self, event):
        self.emit(QtCore.SIGNAL("icepapDoubleClicked(PyQt_PyObject)"),
                  self._driver)
        event.accept()

    def mousePressEvent(self, event):
        tooltip = str(self._driver.current_cfg)
        QtGui.QToolTip.showText(event.globalPos(), tooltip)
        event.accept()

    def mouseMoveEvent(self, event):
        event.accept()

    def btnEnDis_on_click(self, bool):
        if bool:
            self.ui.pushButton.setText("power OFF")
            self._manager.enableDriver(self._driver.icepapsystem_name,
                                       self._driver.addr)
        else:
            self.ui.pushButton.setText("power ON")
            self._manager.disableDriver(self._driver.icepapsystem_name,
                                        self._driver.addr)

    def getDriver(self):
        return self._driver

    def fillData(self, driver):
        self._driver = driver
        if driver is None:
            self.ui.lblName.setText("")
            self.ui.frame.setEnabled(False)
            return False
        else:
            return self.fillStatus()

    def refresh(self):
        if self._driver is not None:
            return self.fillStatus()
        else:
            return True

    def fillStatus(self):
        if self._driver.getName() is None:
            self.ui.lblName.setText("- %d -" % self._driver.addr)
        elif self._driver.getName() != "":
            self.ui.lblName.setText("%d- %s" % (self._driver.addr,
                                                self._driver.getName()))
        else:
            self.ui.lblName.setText("- %d -" % self._driver.addr)

        if self._driver.conflict == Conflict.DRIVER_NOT_PRESENT:
            self.setPaletteColor(self.ui.frame, self.colorerror, Qt.Qt.black)
        elif self._driver.conflict == Conflict.DRIVER_CHANGED:
            self.setPaletteColor(self.ui.frame, self.colorwarning, Qt.Qt.black)
        elif self._driver.mode == Mode.CONFIG:
            self.setPaletteColor(self.ui.frame, self.colorconfig, Qt.Qt.black)
        else:
            self.setPaletteColor(self.ui.frame, self.colorok, Qt.Qt.black)

        (status, power, current) = self._manager.getDriverStatus(
            self._driver.icepapsystem_name, self._driver.addr)
        if status == -1:
            self.ui.pushButton.setEnabled(False)
            self.ui.ledStatus.changeColor(Led.RED)
            self.ui.ledStatus.on()
            return

        axis_state = State(status)
        disabled = axis_state.get_disable_code()
        # TODO: use boolean instead of integers
        ready = int(axis_state.is_ready())
        mode = int(axis_state.get_mode_code())
        if self.status != disabled or self.mode != mode or \
                self.power != power or self.ready != ready:
            if disabled == 0:
                if power:
                    self.ui.ledStatus.changeColor(Led.GREEN)
                    self.ui.ledStatus.on()
                    self.ui.pushButton.setText("power OFF")
                    self.ui.pushButton.setChecked(True)
                    self.ui.pushButton.setEnabled(True)
                    self.mode = mode
                else:
                    self.ui.pushButton.setEnabled(True)
                    self.ui.pushButton.setText("power ON")
                    self.ui.pushButton.setChecked(False)
                    self.ui.ledStatus.changeColor(Led.RED)
                    self.ui.ledStatus.on()
            elif disabled == 1:
                # driver is not active disable motion and enable
                self.ui.pushButton.setEnabled(False)
                self.ui.ledStatus.changeColor(Led.RED)
                self.ui.ledStatus.on()
            else:
                self.ui.pushButton.setEnabled(True)
                self.ui.pushButton.setText("power ON")
                self.ui.pushButton.setChecked(False)
                self.ui.ledStatus.changeColor(Led.RED)
                self.ui.ledStatus.on()

        if status == -1:
            self.ui.pushButton.setEnabled(False)
            self.ui.ledStatus.changeColor(Led.RED)
            self.ui.ledStatus.on()

        self.status = disabled
        self.ready = ready
        self.power = power

        lower = axis_state.is_limit_negative()
        upper = axis_state.is_limit_positive()
        if lower:
            self.ui.ledLimitNeg.on()
        else:
            self.ui.ledLimitNeg.off()

        if upper:
            self.ui.ledLimitPos.on()
        else:
            self.ui.ledLimitPos.off()

        if self.BigSize:
            self.setCurrent(current)
        return True

    def setCurrent(self, current):
        self.ui.lcdCurrent.display(current)
        color = QtGui.QColor()
        if current < 0 or current > 7:
            color = self.coloroff
        else:
            percentage = ((self.MaxCurrent)-current) / self.MaxCurrent

            S = 255 - abs(int(128*percentage))
            H = abs(int(180*percentage))
            V = 255 - abs(int(60*percentage))
            color.setHsv(H, S, V)
        self.setPaletteColor(self.ui.lcdCurrent, color,
                             QtGui.QColor(Qt.Qt.black))

    def setPaletteColor(self, widget, backcolor, forecolor):
        palette = widget.palette()
        widget.setAutoFillBackground(True)
        palette.setColor(QtGui.QPalette.Base, backcolor)
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text, forecolor)
        widget.setPalette(palette)
        widget.show()
