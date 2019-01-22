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
        self.setup_arrow()
        self.set_go_stop_btn_layout()
        self.hs_changed()
        self.tick_interval = 200  # [milliseconds]
        self.ticker = QTimer()
        self.connect_signals()
        self.parent.enable_home_srch_button(False)

    def connect_signals(self):
        self.ui.cbHomeSearch.currentIndexChanged.connect(self.hs_changed)
        self.ui.btnGoStop.clicked.connect(self.btn_go_stop_clicked)
        self.ticker.timeout.connect(self.tick_status)

    def done(self, r):
        self.parent.enable_home_srch_button(True)
        QDialog.done(self, r)

    def hs_changed(self):
        home_selected = self.ui.cbHomeSearch.currentText() == 'HOME'
        if home_selected:
            items = ['-1', '0', '+1']
        else:
            items = ['Lim-', 'Lim+', 'Home', 'EncAux', 'InpAux']
        self.ui.cbHsOptions.clear()
        self.ui.cbHsOptions.addItems(items)
        self.ui.cbEdge.setDisabled(home_selected)
        self.ui.cbDirection.setDisabled(home_selected)

    def set_selectors(self):
        if self.axis.state_moving:
            self.ui.cbHomeSearch.setDisabled(True)
            self.ui.cbHsOptions.setDisabled(True)
            self.ui.cbEdge.setDisabled(True)
            self.ui.cbDirection.setDisabled(True)
        else:
            self.ui.cbHomeSearch.setDisabled(False)
            self.ui.cbHsOptions.setDisabled(False)
            home_selected = self.ui.cbHomeSearch.currentText() == 'HOME'
            self.ui.cbEdge.setDisabled(home_selected)
            self.ui.cbDirection.setDisabled(home_selected)

    def set_go_stop_btn_layout(self):
        if self.axis.state_moving:
            self.ui.btnGoStop.setText('STOP')
        else:
            self.ui.btnGoStop.setText('GO')

    def btn_go_stop_clicked(self):
        if self.axis.state_moving:
            self.axis.stop()
        else:
            self.start_motor()
        self.set_go_stop_btn_layout()

    def start_motor(self):
        cmd = self.ui.cbHomeSearch.currentText()
        opt = self.ui.cbHsOptions.currentText()
        try:
            if cmd == 'HOME':
                direction = int(opt)
                self.axis.home(direction)
            else:
                edge = self.ui.cbEdge.currentText()
                direction = int(self.ui.cbDirection.currentText())
                self.axis.srch(opt, edge, direction)
        except RuntimeError as e:
            msg = 'HOME/SRCH failed:\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'HOME/SRCH', msg)
            return
        self.set_selectors()
        self.ticker.start(self.tick_interval)

    def tick_status(self):
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
                self.draw_arrow(direction == -1)
            elif status == 'NOTFOUND':
                self.ticker.stop()
                ss = "background-color: red"
                self.ui.gvIndicator.setStyleSheet(ss)
                self.clear_arrow()
                self.set_go_stop_btn_layout()
            elif status == 'FOUND':
                self.ticker.stop()
                ss = "background-color: green"
                self.ui.gvIndicator.setStyleSheet(ss)
                self.draw_arrow(direction == -1)
                self.set_go_stop_btn_layout()
                self.ui.lcdPosAxis.display(f1('AXIS'))
                self.ui.lcdEncAxis.display(f2('AXIS'))
                if self.axis.get_cfg('SHFTENC')['SHFTENC'] == 'NONE':
                    self.ui.lcdPosShftenc.setDisabled(True)
                    self.ui.lcdEncShftenc.setDisabled(True)
                else:
                    self.ui.lcdPosShftenc.setDisabled(False)
                    self.ui.lcdEncShftenc.setDisabled(False)
                    self.ui.lcdPosShftenc.display(f1('SHFTENC'))
                    self.ui.lcdEncShftenc.display(f2('SHFTENC'))
                if self.axis.get_cfg('TGTENC')['TGTENC'] == 'NONE':
                    self.ui.lcdPosTgtenc.setDisabled(True)
                    self.ui.lcdEncTgtenc.setDisabled(True)
                else:
                    self.ui.lcdPosTgtenc.setDisabled(False)
                    self.ui.lcdEncTgtenc.setDisabled(False)
                    self.ui.lcdPosTgtenc.display(f1('TGTENC'))
                    self.ui.lcdEncTgtenc.display(f2('TGTENC'))
                self.ui.lcdPosEncin.display(f1('ENCIN'))
                self.ui.lcdEncEncin.display(f2('ENCIN'))
                self.ui.lcdPosInpos.display(f1('INPOS'))
                self.ui.lcdEncInpos.display(f2('INPOS'))
                self.ui.lcdPosAbsenc.display(f1('ABSENC'))
                self.ui.lcdEncAbsenc.display(f2('ABSENC'))
                self.ui.lcdPosMotor.display(f1('MOTOR'))
                self.ui.lcdEncMotor.display(f2('MOTOR'))
        except RuntimeError as e:
            msg = 'HOME/SRCH failed:\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'HOME/SRCH', msg)
            self.ticker.stop()
            self.axis.stop()
            self.set_go_stop_btn_layout()
            self.clear_indicator()
        self.set_selectors()

    def setup_arrow(self):
        self.scene = QGraphicsScene()
        self.ui.gvIndicator.setScene(self.scene)

    def draw_arrow(self, is_left):
        self.clear_arrow()
        if is_left:
            self.scene.addText("<--")
        else:
            self.scene.addText("-->")

    def clear_arrow(self):
        self.scene.clear()

    def clear_indicator(self):
        self.ui.gvIndicator.setStyleSheet("")
        self.clear_arrow()
