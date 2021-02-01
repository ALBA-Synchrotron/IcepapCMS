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


from PyQt5 import QtGui, Qt, QtWidgets, uic, QtCore
from pkg_resources import resource_filename
from icepap import Mode, State
import logging
from .Led import Led
from ..lib import MainManager, Conflict
from ..helpers import loggingInfo


class IcePapDriverWidget(QtWidgets.QWidget):
    icepapDoubleClicked = QtCore.pyqtSignal(object)
    log = logging.getLogger('{}.IcePapDriverWidget'.format(__name__))

    @loggingInfo
    def __init__(self, parent=None, BigSize=True, test_mode=False):
        QtWidgets.QWidget.__init__(self, parent)
        self.initView(BigSize, test_mode)
        self.MaxCurrent = 7
        self._driver = None
        self.setMouseTracking(True)
        self.status = -1
        self.ready = -1
        self.power = -1
        self.mode = -1

    @loggingInfo
    def initView(self, Big, test_mode=False):
        self.BigSize = Big
        self.coloroff = QtGui.QColor(225, 255, 200)
        self.colorerror = QtGui.QColor(255, 179, 179)
        self.colorok = QtGui.QColor(223, 223, 237)
        self.colorwarning = QtGui.QColor(255, 255, 0)
        self.colorconfig = QtGui.QColor(255, 206, 162)
        self.ui = QtWidgets.QWidget(self)

        if Big:
            ui_filename = resource_filename('icepapcms.gui.ui',
                                            'icepapdriverwidget.ui')
        else:
            ui_filename = resource_filename('icepapcms.gui.ui',
                                            'icepapdriverwidgetsmall.ui')

        uic.loadUi(ui_filename, baseinstance=self.ui,
                   package='icepapcms.gui.Led')
        if Big:
            self.setPaletteColor(self.ui.lcdCurrent, self.coloroff,
                                 QtGui.QColor(Qt.Qt.white))

        self.ui.ledStatus.changeColor(Led.YELLOW)
        self.ui.ledLimitPos.changeColor(Led.ORANGE)
        self.ui.ledLimitNeg.changeColor(Led.GREEN)
        if test_mode:
            return
        self._manager = MainManager()

        self.setAutoFillBackground(True)
        # Signals
        self.ui.pushButton.clicked.connect(self.btnEnDis_on_click)

    @loggingInfo
    def mouseDoubleClickEvent(self, event):
        self.icepapDoubleClicked.emit(event)
        event.accept()

    @loggingInfo
    def mousePressEvent(self, event):
        tooltip = str(self._driver.current_cfg)
        QtWidgets.QToolTip.showText(event.globalPos(), tooltip)
        event.accept()

    @loggingInfo
    def mouseMoveEvent(self, event):
        event.accept()

    @loggingInfo
    def btnEnDis_on_click(self, bool):
        if bool:
            self.ui.pushButton.setText("power OFF")
            self._manager.enableDriver(self._driver.icepapsystem_name,
                                       self._driver.addr)
        else:
            self.ui.pushButton.setText("power ON")
            self._manager.disableDriver(self._driver.icepapsystem_name,
                                        self._driver.addr)

    @loggingInfo
    def getDriver(self):
        return self._driver

    @loggingInfo
    def fillData(self, driver):
        self._driver = driver
        if driver is None:
            self.ui.lblName.setText("")
            self.ui.frame.setEnabled(False)
            return False
        else:
            return self.fillStatus()

    @loggingInfo
    def refresh(self):
        if self._driver is not None:
            return self.fillStatus()
        else:
            return True

    @loggingInfo
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

    @loggingInfo
    def setCurrent(self, current):
        self.ui.lcdCurrent.display(current)
        current = float(current)
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

    @loggingInfo
    def setPaletteColor(self, widget, backcolor, forecolor):
        palette = widget.palette()
        widget.setAutoFillBackground(True)
        palette.setColor(QtGui.QPalette.Base, backcolor)
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text, forecolor)
        widget.setPalette(palette)
        widget.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    lw = IcePapDriverWidget(BigSize=True, test_mode=True)
    lw.show()
    sys.exit(app.exec_())