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


from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from ui_dialoghomesrch import Ui_DialogHomeSrch
from messagedialogs import MessageDialogs
#from ..lib_icepapcms import MainManager


class DialogHomeSrch(QDialog):

    def __init__(self, parent, axis):
        QDialog.__init__(self, parent)
        self.ui = Ui_DialogHomeSrch()
        self.ui.setupUi(self)
        self.parent = parent
        self.axis = axis
        self.close_button = self.ui.bbClose.button(QDialogButtonBox.Close)
        self._connect_signals()
        self._cb_hs_changed()

    def _connect_signals(self):
        self.ui.cbHomeSearch.currentIndexChanged.connect(self._cb_hs_changed)
        self.ui.cbHsOptions.currentIndexChanged.connect(self._update_access)
        self.ui.btnGo.clicked.connect(self._move_motor)
        self.close_button.clicked.connect(self._close_dialog)

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

    def _move_motor(self):
        axis = self.axis
        cmd = self.ui.cbHomeSearch.currentText()
        opt = self.ui.cbHsOptions.currentText()
        try:
            if cmd == 'HOME':
                direction = int(opt)
                axis.home(direction)
            else:
                edge = self.ui.cbEdge.currentText()
                direction = self.ui.cbDirection.currentText()
                axis.srch(opt, edge, direction)
        except RuntimeError as e:
            msg = 'HOME/SRCH failed:\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'HOME/SRCH', msg)





        #addr = axis.addr
        #try:
        #    if self.ui.cbHomeSearch.currentText() == 'HOME':
        #        txt = '{}:?HOMESTAT\n'.format(addr)
        #        status, direction = axis.homestat
        #        f1 = axis.get_home_position
        #        f2 = axis.get_home_encoder
        #    else:
        #        txt = '{}:?SRCHSTAT\n'.format(addr)
        #        status, direction = axis.srchstat
        #        f1 = axis.get_srch_position
        #        f2 = axis.get_srch_encoder
        #    if status == 'MOVING':
        #        txt += 'Status: MOVING\n'
        #        txt += 'Direction: {}\n'.format(direction)
        #    elif status == 'NOTFOUND':
        #        txt += 'Status: NOTFOUND\n'
        #    else:
        #        txt += 'Pos AXIS  : {}\n'.format(f1('AXIS'))
        #        txt += 'Pos INPOS : {}\n'.format(f1('INPOS'))
        #        txt += 'Pos TGTENC: {}\n'.format(f1('TGTENC'))
        #        txt += 'Pos ENCIN : {}\n'.format(f1('ENCIN'))
        #        txt += 'Pos ABSENC: {}\n'.format(f1('ABSENC'))
        #        txt += 'Enc AXIS  : {}\n'.format(f2('AXIS'))
        #        txt += 'Enc INPOS : {}\n'.format(f2('INPOS'))
        #        txt += 'Enc TGTENC: {}\n'.format(f2('TGTENC'))
        #        txt += 'Enc ENCIN : {}\n'.format(f2('ENCIN'))
        #        txt += 'Enc ABSENC: {}\n'.format(f2('ABSENC'))
        #    self.ui.homeBrowser.clear()
        #    self.ui.homeBrowser.setText(txt)
        #except RuntimeError as e:
        #    msg = 'HOME/SRCH failed:\n{}'.format(e)
        #    print(msg)
        #    MessageDialogs.showErrorMessage(None, 'HOME/SRCH', msg)

    def _close_dialog(self):
        self.parent.enable_home_srch_button()
