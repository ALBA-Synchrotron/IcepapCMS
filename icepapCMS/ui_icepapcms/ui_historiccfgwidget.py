# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historiccfgwidget.ui'
#
# Created: Fri Feb  9 13:20:39 2018
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_HistoricCfgWidget(object):
    def setupUi(self, HistoricCfgWidget):
        HistoricCfgWidget.setObjectName(_fromUtf8("HistoricCfgWidget"))
        HistoricCfgWidget.resize(220, 420)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HistoricCfgWidget.sizePolicy().hasHeightForWidth())
        HistoricCfgWidget.setSizePolicy(sizePolicy)
        HistoricCfgWidget.setMinimumSize(QtCore.QSize(220, 420))
        HistoricCfgWidget.setMaximumSize(QtCore.QSize(220, 420))
        HistoricCfgWidget.setWindowTitle(_fromUtf8(""))
        HistoricCfgWidget.setAutoFillBackground(True)
        self.gridlayout = QtGui.QGridLayout(HistoricCfgWidget)
        self.gridlayout.setMargin(2)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label_4 = QtGui.QLabel(HistoricCfgWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 0, 0, 1, 3)
        self.txtName = QtGui.QLineEdit(HistoricCfgWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.txtName.setFont(font)
        self.txtName.setObjectName(_fromUtf8("txtName"))
        self.gridlayout.addWidget(self.txtName, 3, 2, 1, 1)
        self.label_3 = QtGui.QLabel(HistoricCfgWidget)
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(":/small_icons/IcepapCfg Icons/redpixel.png")))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout.addWidget(self.label_3, 3, 1, 1, 1)
        self.label = QtGui.QLabel(HistoricCfgWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 3, 0, 1, 1)
        self.label_2 = QtGui.QLabel(HistoricCfgWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 4, 0, 1, 2)
        self.txtDescription = QtGui.QTextEdit(HistoricCfgWidget)
        self.txtDescription.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.txtDescription.setFont(font)
        self.txtDescription.setObjectName(_fromUtf8("txtDescription"))
        self.gridlayout.addWidget(self.txtDescription, 5, 0, 1, 3)
        self.stackedWidget = QtGui.QStackedWidget(HistoricCfgWidget)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.page_calendar = QtGui.QWidget()
        self.page_calendar.setObjectName(_fromUtf8("page_calendar"))
        self.gridlayout1 = QtGui.QGridLayout(self.page_calendar)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(0)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.calendarWidget = QtGui.QCalendarWidget(self.page_calendar)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget.sizePolicy().hasHeightForWidth())
        self.calendarWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.gridlayout1.addWidget(self.calendarWidget, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_calendar)
        self.page_day = QtGui.QWidget()
        self.page_day.setObjectName(_fromUtf8("page_day"))
        self.gridlayout2 = QtGui.QGridLayout(self.page_day)
        self.gridlayout2.setMargin(0)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName(_fromUtf8("gridlayout2"))
        self.listWidget = QtGui.QListWidget(self.page_day)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridlayout2.addWidget(self.listWidget, 1, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem, 0, 1, 1, 1)
        self.btnBack = QtGui.QPushButton(self.page_day)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBack.sizePolicy().hasHeightForWidth())
        self.btnBack.setSizePolicy(sizePolicy)
        self.btnBack.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/small_icons/IcepapCFG Icons Petits/go-relative2.png"))
        self.btnBack.setIcon(icon)
        self.btnBack.setObjectName(_fromUtf8("btnBack"))
        self.gridlayout2.addWidget(self.btnBack, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_day)
        self.gridlayout.addWidget(self.stackedWidget, 2, 0, 1, 3)
        self.line_2 = QtGui.QFrame(HistoricCfgWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridlayout.addWidget(self.line_2, 7, 0, 1, 3)
        self.line = QtGui.QFrame(HistoricCfgWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridlayout.addWidget(self.line, 1, 0, 1, 3)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.saveButton = QtGui.QPushButton(HistoricCfgWidget)
        icon1 = QtGui.QIcon()
        icon1.addFile(_fromUtf8(":/small_icons/IcepapCFG Icons Petits/save.png"))
        self.saveButton.setIcon(icon1)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.hboxlayout.addWidget(self.saveButton)
        self.deleteButton = QtGui.QPushButton(HistoricCfgWidget)
        icon2 = QtGui.QIcon()
        icon2.addFile(_fromUtf8(":/small_icons/IcepapCFG Icons Petits/process-stop.png"))
        self.deleteButton.setIcon(icon2)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.hboxlayout.addWidget(self.deleteButton)
        self.gridlayout.addLayout(self.hboxlayout, 6, 0, 1, 3)

        self.retranslateUi(HistoricCfgWidget)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HistoricCfgWidget)

    def retranslateUi(self, HistoricCfgWidget):
        self.label_4.setText(_translate("HistoricCfgWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Historic Configuration Tool</span></p></body></html>", None))
        self.label.setText(_translate("HistoricCfgWidget", "Name", None))
        self.label_2.setText(_translate("HistoricCfgWidget", "Description", None))
        self.saveButton.setText(_translate("HistoricCfgWidget", "Update", None))
        self.deleteButton.setText(_translate("HistoricCfgWidget", "Delete", None))

import icepapcms_rc
