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

# Led.py
# A led widget for PyQT4
# Author: Josep Joan Ribas Prats
# E-mail: jribas at cells DOT es


import sys
from PyQt5 import QtCore, QtWidgets, Qt
from pkg_resources import resource_filename


__all__ = ['Led']


LED_IMAGES = {}
LED_COLORS = ["ledblueoff", "ledblue", "ledgreenoff", "ledgreen",
              "ledredoff", "ledred", "ledyellowoff", "ledyellow",
              "ledorangeoff", "ledorange"]

# Load led images:
for size in ['s24', 's48']:
    LED_IMAGES[size] = {}
    if size == 's24':
        module_name = 'icepapcms.gui.Led.images24'
    else:
        module_name = 'icepapcms.gui.Led.images48'
    for color in LED_COLORS:
        image_filename = '{}.png'.format(color)
        LED_IMAGES[size][color] = Qt.QImage(resource_filename(module_name,
                                                              image_filename))


class Led(QtWidgets.QWidget):

    BLUE, GREEN, RED, YELLOW, ORANGE = list(range(5))
    ON, OFF = list(range(2))
    S24, S48 = list(range(2))
    colors = LED_COLORS

    def __init__(self, parent=None, ledsize=S24, ledcolor=GREEN):

        QtWidgets.QWidget.__init__(self, parent)
        self.ledsize = ledsize
        if ledsize == Led.S48:
            lsize = 48
        else:
            lsize = 24
        self.status = Led.OFF
        self.setObjectName("Led")
        size = QtCore.QSize(QtCore.QRect(0, 0, lsize, lsize).size())
        self.resize(size.expandedTo(self.minimumSizeHint()))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy(0),
                                           QtWidgets.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(lsize, lsize))
        self.setMaximumSize(QtCore.QSize(lsize, lsize))

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, lsize, lsize))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy(0),
                                           QtWidgets.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())

        self.label.setSizePolicy(sizePolicy)

        self.label.setObjectName("label")
        self.changeColor(ledcolor)

        self.retranslateUi(self)

        QtCore.QMetaObject.connectSlotsByName(self)

    # TODO investigate if this method is needed
    # def tr(self, string):
    #     return QtWidgets.QApplication.translate(
    #         "Led", string, None,)

    def retranslateUi(self, Led):
        Led.setWindowTitle(self.tr("Form"))

    def on(self):
        if self.status == Led.OFF:
            self.status = Led.ON
            self.label.setPixmap(Qt.QPixmap.fromImage(self.onled))

    def off(self):
        if self.status == Led.ON:
            self.status = Led.OFF
            self.label.setPixmap(Qt.QPixmap.fromImage(self.offled))

    def changeColor(self, LedColor):
        ledoffcolor = int(LedColor) * 2
        ledoncolor = (int(LedColor) * 2) + 1
        if self.ledsize == Led.S24:
            size = 's24'
        else:
            size = 's48'
        self.offled = LED_IMAGES[size][Led.colors[ledoffcolor]]
        self.onled = LED_IMAGES[size][Led.colors[ledoncolor]]

        if self.status == Led.OFF:
            self.status = Led.ON
            self.off()
        else:
            self.status = Led.OFF
            self.on()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    lw = Led(None, Led.S48, Led.ORANGE)
    lw.show()
    lw.on()
    sys.exit(app.exec_())
