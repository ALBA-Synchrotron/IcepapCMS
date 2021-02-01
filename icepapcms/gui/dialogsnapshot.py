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


from PyQt5 import QtWidgets, uic
from pkg_resources import resource_filename
import os
import time
import logging
import threading
from ..lib.sanpshot import IcepapSnapshot
from ..lib.configmanager import ConfigManager
from .messagedialogs import MessageDialogs


class DialogSnapshot(QtWidgets.QDialog):

    def __init__(self, parent, host='', port=5000):
        QtWidgets.QDialog.__init__(self, parent)

        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'snapshot.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui)
        self.modal = True
        self._config = ConfigManager()
        self.ui.host.setText(host)
        self.ui.port.setText(str(port))
        self.set_filename()

        self.ui.browser.clicked.connect(self.set_filename)
        self.ui.take_snapshot.clicked.connect(self.take_snapshot_clicked)

    def set_filename(self):
        if self.ui.filename.text() == '':
            name = 'snapshot_{}.yaml'.format(time.strftime('%Y%m%d_%H%M%S'))
            snapshots_folder = \
                self._config.config[self._config.icepap]['snapshots_folder']
            directory = os.path.join(snapshots_folder, name)
        else:
            directory = self.ui.filename.text()
        fn = QtWidgets.QFileDialog.getSaveFileName(
            self, "Take Snapshot",
            directory=directory,
            filter='*.yaml')[0]
        self.ui.filename.setText(fn)

    def update_progress_bar(self, ipap_snapshot):
        while ipap_snapshot.done != 100:
            self.ui.progress_bar.setValue(ipap_snapshot.done)
            time.sleep(1)
        self.ui.progress_bar.setValue(ipap_snapshot.done)

    def take_snapshot_clicked(self):
        try:
            host = self.ui.host.text()
            if host == '':
                MessageDialogs.showErrorMessage(
                    self, 'Error', 'You should introduce a valid host')
            port = int(self.ui.port.text())
            filename = self.ui.filename.text()
            try:
                with open(filename, 'w'):
                    pass
            except Exception as e:
                MessageDialogs.showErrorMessage(
                    self, 'Error on file creation', str(e))
                return

            try:
                ipap_snapshot = IcepapSnapshot(host, port)
            except Exception as e:
                MessageDialogs.showErrorMessage(self, 'Error connecting',
                                                str(e))
                return
            thread = threading.Thread(target=self.update_progress_bar,
                                      args=[ipap_snapshot])

            self.ui.take_snapshot.setEnabled(False)
            thread.start()
            ipap_snapshot.create_snapshot(filename)
            thread.join()
        finally:
            self.ui.take_snapshot.setEnabled(True)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = DialogSnapshot(None)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
