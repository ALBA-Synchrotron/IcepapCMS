# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historiccfgwidget.ui'
#
# Created: Tue Sep  4 09:41:29 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_HistoricCfgWidget(object):
    def setupUi(self, HistoricCfgWidget):
        HistoricCfgWidget.setObjectName("HistoricCfgWidget")
        HistoricCfgWidget.resize(QtCore.QSize(QtCore.QRect(0,0,220,420).size()).expandedTo(HistoricCfgWidget.minimumSizeHint()))

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HistoricCfgWidget.sizePolicy().hasHeightForWidth())
        HistoricCfgWidget.setSizePolicy(sizePolicy)
        HistoricCfgWidget.setMinimumSize(QtCore.QSize(220,420))
        HistoricCfgWidget.setMaximumSize(QtCore.QSize(220,420))
        HistoricCfgWidget.setAutoFillBackground(True)

        self.gridlayout = QtGui.QGridLayout(HistoricCfgWidget)
        self.gridlayout.setMargin(2)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.label_4 = QtGui.QLabel(HistoricCfgWidget)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,0,0,1,3)

        self.txtName = QtGui.QLineEdit(HistoricCfgWidget)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.txtName.setFont(font)
        self.txtName.setObjectName("txtName")
        self.gridlayout.addWidget(self.txtName,3,2,1,1)

        self.label_3 = QtGui.QLabel(HistoricCfgWidget)
        self.label_3.setPixmap(QtGui.QPixmap(":/small_icons/IcepapCfg Icons/redpixel.png"))
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,3,1,1,1)

        self.label = QtGui.QLabel(HistoricCfgWidget)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,3,0,1,1)

        self.label_2 = QtGui.QLabel(HistoricCfgWidget)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,4,0,1,2)

        self.txtDescription = QtGui.QTextEdit(HistoricCfgWidget)
        self.txtDescription.setMaximumSize(QtCore.QSize(16777215,100))

        font = QtGui.QFont()
        font.setPointSize(8)
        self.txtDescription.setFont(font)
        self.txtDescription.setObjectName("txtDescription")
        self.gridlayout.addWidget(self.txtDescription,5,0,1,3)

        self.stackedWidget = QtGui.QStackedWidget(HistoricCfgWidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.page_calendar = QtGui.QWidget()
        self.page_calendar.setObjectName("page_calendar")

        self.gridlayout1 = QtGui.QGridLayout(self.page_calendar)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(0)
        self.gridlayout1.setObjectName("gridlayout1")

        self.calendarWidget = QtGui.QCalendarWidget(self.page_calendar)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
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
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridlayout1.addWidget(self.calendarWidget,0,0,1,1)
        self.stackedWidget.addWidget(self.page_calendar)

        self.page_day = QtGui.QWidget()
        self.page_day.setObjectName("page_day")

        self.gridlayout2 = QtGui.QGridLayout(self.page_day)
        self.gridlayout2.setMargin(0)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.listWidget = QtGui.QListWidget(self.page_day)
        self.listWidget.setObjectName("listWidget")
        self.gridlayout2.addWidget(self.listWidget,1,0,1,2)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem,0,1,1,1)

        self.btnBack = QtGui.QPushButton(self.page_day)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(1))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnBack.sizePolicy().hasHeightForWidth())
        self.btnBack.setSizePolicy(sizePolicy)
        self.btnBack.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/go-relative2.png"))
        self.btnBack.setObjectName("btnBack")
        self.gridlayout2.addWidget(self.btnBack,0,0,1,1)
        self.stackedWidget.addWidget(self.page_day)
        self.gridlayout.addWidget(self.stackedWidget,2,0,1,3)

        self.line_2 = QtGui.QFrame(HistoricCfgWidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout.addWidget(self.line_2,7,0,1,3)

        self.line = QtGui.QFrame(HistoricCfgWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,1,0,1,3)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.saveButton = QtGui.QPushButton(HistoricCfgWidget)
        self.saveButton.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/save.png"))
        self.saveButton.setObjectName("saveButton")
        self.hboxlayout.addWidget(self.saveButton)

        self.deleteButton = QtGui.QPushButton(HistoricCfgWidget)
        self.deleteButton.setIcon(QtGui.QIcon(":/small_icons/IcepapCFG Icons Petits/process-stop.png"))
        self.deleteButton.setObjectName("deleteButton")
        self.hboxlayout.addWidget(self.deleteButton)
        self.gridlayout.addLayout(self.hboxlayout,6,0,1,3)

        self.retranslateUi(HistoricCfgWidget)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HistoricCfgWidget)

    def retranslateUi(self, HistoricCfgWidget):
        self.label_4.setText(QtGui.QApplication.translate("HistoricCfgWidget", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Historic Configuration Tool</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("HistoricCfgWidget", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("HistoricCfgWidget", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("HistoricCfgWidget", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("HistoricCfgWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))

import icepapcms_rc
