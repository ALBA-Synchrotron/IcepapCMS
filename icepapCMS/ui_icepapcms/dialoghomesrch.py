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


from PyQt4.QtGui import QDialog, QGraphicsScene
from PyQt4.QtCore import QTimer
from ui_dialoghomesrch import Ui_DialogHomeSrch
from messagedialogs import MessageDialogs


class DialogHomeSrch(QDialog):

    def __init__(self, parent, axis):
        QDialog.__init__(self, parent)
        self.ui = Ui_DialogHomeSrch()
        self.ui.setupUi(self)
        self.parent = parent
        self.axis = axis
        self._setup_arrow()
        self.motor_moving = False
        self._set_go_stop_btn_layout()
        self._hs_changed()
        self.tick_interval = 200  # [milliseconds]
        self.ticker = QTimer()
        self._connect_signals()

    def _connect_signals(self):
        self.ui.cbHomeSearch.currentIndexChanged.connect(self._hs_changed)
        self.ui.cbHsOptions.currentIndexChanged.connect(self._hsopt_changed)
        self.ui.btnGoStop.clicked.connect(self._btn_go_stop_clicked)
        self.ticker.timeout.connect(self._tick_status)

    def _hs_changed(self):
        self._clear_indicator()
        home_selected = self.ui.cbHomeSearch.currentText() == 'HOME'
        if home_selected:
            items = ['-1', '0', '+1']
        else:
            items = ['Lim-', 'Lim+', 'Home', 'EncAux', 'InpAux']
        self.ui.cbHsOptions.clear()
        self.ui.cbHsOptions.addItems(items)
        self._hsopt_changed()

    def _hsopt_changed(self):
        self._clear_indicator()
        have_home = self.ui.cbHomeSearch.currentText() == 'HOME'
        have_limit = self.ui.cbHsOptions.currentText() in ['Lim-', 'Lim+']
        disable = have_home or have_limit
        self.ui.cbEdge.setDisabled(disable)
        self.ui.cbDirection.setDisabled(disable)

    def _set_go_stop_btn_layout(self):
        if self.motor_moving:
            self.ui.btnGoStop.setText('STOP')
        else:
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
        self.ui.cbHomeSearch.setDisabled(True)
        self.ui.cbHsOptions.setDisabled(True)
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
                self._draw_arrow(direction == -1)
            elif status == 'NOTFOUND':
                self.ticker.stop()
                ss = "background-color: red"
                self.ui.gvIndicator.setStyleSheet(ss)
                self._clear_arrow()
                self.motor_moving = False
                self._set_go_stop_btn_layout()
            elif status == 'FOUND':
                self.ticker.stop()
                ss = "background-color: green"
                self.ui.gvIndicator.setStyleSheet(ss)
                self._draw_arrow(direction == -1)
                self.motor_moving = False
                self._set_go_stop_btn_layout()
                self.ui.lcdPosAxis.display(f1('AXIS'))
                self.ui.lcdPosTgtenc.display(f1('TGTENC'))
                self.ui.lcdPosEncin.display(f1('ENCIN'))
                self.ui.lcdPosInpos.display(f1('INPOS'))
                self.ui.lcdPosAbsenc.display(f1('ABSENC'))
                self.ui.lcdEncAxis.display(f2('AXIS'))
                self.ui.lcdEncTgtenc.display(f2('TGTENC'))
                self.ui.lcdEncEncin.display(f2('ENCIN'))
                self.ui.lcdEncInpos.display(f2('INPOS'))
                self.ui.lcdEncAbsenc.display(f2('ABSENC'))
        except RuntimeError as e:
            msg = 'HOME/SRCH failed:\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'HOME/SRCH', msg)
            self.ticker.stop()
            self.axis.stop()
            self.motor_moving = False
            self._set_go_stop_btn_layout()
            self._clear_indicator()
        self.ui.cbHomeSearch.setDisabled(self.motor_moving)
        self.ui.cbHsOptions.setDisabled(self.motor_moving)

    def _setup_arrow(self):
        self.scene = QGraphicsScene()
        self.ui.gvIndicator.setScene(self.scene)

    def _draw_arrow(self, is_left):
        self._clear_arrow()
        if is_left:
            self.scene.addText("<--")
        else:
            self.scene.addText("-->")

    def _clear_arrow(self):
        self.scene.clear()

    def _clear_indicator(self):
        self.ui.gvIndicator.setStyleSheet("")
        self._clear_arrow()
