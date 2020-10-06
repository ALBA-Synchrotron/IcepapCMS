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

from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from pkg_resources import resource_filename
from .messagedialogs import MessageDialogs


class DialogHomeSrch(QDialog):

    def __init__(self, parent, axis):
        QDialog.__init__(self, parent)
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'dialoghomesrch.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)
        self.parent = parent
        self.axis = axis
        self.close_button = self.ui.bbClose.button(QDialogButtonBox.Close)
        self.motor_moving = False
        self._set_go_stop_btn_layout()
        self._cb_hs_changed()
        self.tick_interval = 200  # [milliseconds]
        self.ticker = QTimer()
        self._connect_signals()

    def _connect_signals(self):
        self.ui.cbHomeSearch.currentIndexChanged.connect(self._cb_hs_changed)
        self.ui.cbHsOptions.currentIndexChanged.connect(self._update_access)
        self.ui.btnGoStop.clicked.connect(self._btn_go_stop_clicked)
        self.close_button.clicked.connect(self.close)
        self.ticker.timeout.connect(self._tick_status)

    def _update_access(self):
        have_home = self.ui.cbHomeSearch.currentText() == 'HOME'
        have_limit = self.ui.cbHsOptions.currentText() in ['Lim-', 'Lim+']
        disable = have_home or have_limit
        self.ui.cbEdge.setDisabled(disable)
        self.ui.cbDirection.setDisabled(disable)

    def _cb_hs_changed(self):
        home_selected = self.ui.cbHomeSearch.currentText() == 'HOME'
        if home_selected:
            items = ['-1', '0', '+1']
        else:
            items = ['Lim-', 'Lim+', 'Home', 'EncAux', 'InpAux']
        self.ui.cbHsOptions.clear()
        self.ui.cbHsOptions.addItems(items)
        self._update_access()

    def _set_go_stop_btn_layout(self):
        if self.motor_moving:
            self.ui.btnGoStop.setStyleSheet("background-color: red")
            self.ui.btnGoStop.setText('STOP')
        else:
            self.ui.btnGoStop.setStyleSheet("background-color: green")
            self.ui.btnGoStop.setText('GO')

    def _btn_go_stop_clicked(self):
        if self.motor_moving:
            self.motor_moving = False
            self.axis.stop()
        else:
            self.motor_moving = True
            self._start_motor()
        self._set_go_stop_btn_layout()

    def _start_motor(self):
        cmd = self.ui.cbHomeSearch.currentText()
        opt = self.ui.cbHsOptions.currentText()
        try:
            if cmd == 'HOME':
                direction = int(opt)
                self.axis.home(direction)
            else:
                edge = self.ui.cbEdge.currentText()
                direction = self.ui.cbDirection.currentText()
                self.axis.srch(opt, edge, direction)
        except RuntimeError as e:
            msg = 'HOME/SRCH failed:\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'HOME/SRCH', msg)
            return
        self.ticker.start(self.tick_interval)

    def _tick_status(self):
        try:
            if self.ui.cbHomeSearch.currentText() == 'HOME':
                status, direction = self.axis.homestat
                f1 = self.axis.get_home_position
                f2 = self.axis.get_home_encoder
            else:
                status, direction = self.axis.srchstat
                f1 = self.axis.get_srch_position
                f2 = self.axis.get_srch_encoder
            if status == 'MOVING':
                ss = "background-color: yellow"
                self.ui.gvIndicator.setStyleSheet(ss)
                if direction == -1:
                    pass
                elif direction == 1:
                    pass
                else:
                    self.axis.stop()
                    msg = 'Internal Error: Bad direction'
                    print(msg)
                    MessageDialogs.showErrorMessage(None, 'HOME/SRCH', msg)
                    return
                self.ticker.start(self.tick_interval)
            elif status == 'NOTFOUND':
                ss = "background-color: red"
                self.ui.gvIndicator.setStyleSheet(ss)
                self.motor_moving = False
                self._set_go_stop_btn_layout()
            else:
                ss = "background-color: green"
                self.ui.gvIndicator.setStyleSheet(ss)
                self.motor_moving = False
                self._set_go_stop_btn_layout()
                self.ui.lcdPosAxis.display(f1('AXIS'))
                self.ui.lcdPosTgtenc.display(f1('INPOS'))
                self.ui.lcdPosEncin.display(f1('TGTENC'))
                self.ui.lcdPosInpos.display(f1('ENCIN'))
                self.ui.lcdPosAbsenc.display(f1('ABSENC'))
                self.ui.lcdEncAxis.display(f2('AXIS'))
                self.ui.lcdEncTgtenc.display(f2('INPOS'))
                self.ui.lcdEncEncin.display(f2('TGTENC'))
                self.ui.lcdEncInpos.display(f2('ENCIN'))
                self.ui.lcdEncAbsenc.display(f2('ABSENC'))
        except RuntimeError as e:
            msg = 'HOME/SRCH failed:\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'HOME/SRCH', msg)

    def closeEvent(self, event):
        self.parent.enable_home_srch_button()
        event.accept()
