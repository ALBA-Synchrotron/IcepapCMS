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


from PyQt5 import QtCore, QtGui, Qt, QtWidgets, uic
from pkg_resources import resource_filename
import datetime
import tempfile
from icepap import State, Mode
from xml.dom import minidom, Node
from xml.dom.minidom import getDOMImplementation
import logging
from .Led import Led
from ..lib import MainManager, IcepapsManager, ConfigManager, \
    StormManager
from .messagedialogs import MessageDialogs
from ..helpers import loggingInfo
from .dialoghomesrch import DialogHomeSrch


class PageiPapDriver(QtWidgets.QWidget):
    """
    Widget that manages all the information related to an
    icepap driver. Configuration, testing and historic configurations
    """
    log = logging.getLogger('{}.PageiPapDriver'.format(__name__))

    @loggingInfo
    def __init__(self, mainwin, test_mode=False):
        QtWidgets.QWidget.__init__(self, None)
        self._mainwin = mainwin
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'pageipapdriver.ui')
        self.ui = self
        uic.loadUi(ui_filename, baseinstance=self.ui,
                   package='icepapcms.gui')

        self.signalMapper = QtCore.QSignalMapper(self)
        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'axis.ui')
        self.axis = QtWidgets.QDialog()
        uic.loadUi(ui_filename, baseinstance=self.axis,
                   package='icepapcms.gui')


        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'motor.ui')
        self.motor = QtWidgets.QDialog()
        uic.loadUi(ui_filename, baseinstance=self.motor,
                   package='icepapcms.gui')


        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'encoders.ui')
        self.encoders = QtWidgets.QDialog()
        uic.loadUi(ui_filename, baseinstance=self.encoders,
                   package='icepapcms.gui')

        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'closedloop.ui')
        self.closedloop = QtWidgets.QDialog()
        uic.loadUi(ui_filename, baseinstance=self.closedloop,
                   package='icepapcms.gui')

        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'homing.ui')
        self.homing = QtWidgets.QDialog()
        uic.loadUi(ui_filename, baseinstance=self.homing,
                   package='icepapcms.gui')

        ui_filename = resource_filename('icepapcms.gui.ui',
                                        'io.ui')
        self.io = QtWidgets.QDialog()
        uic.loadUi(ui_filename, baseinstance=self.io,
                   package='icepapcms.gui')


        self.param_to_widgets = {}
        self.ui_widgets = []

        self.param_to_unknown_widgets = {}

        self.tab_frames = [
            self.axis,
            self.motor,
            self.encoders,
            self.closedloop,
            self.homing,
            self.io]
        self.tab_labels = ["Axis", "Motor", "Encoders", "Closed loop",
                           "Homing", "I/O"]

        for index in range(len(self.tab_labels)):
            widget = self.tab_frames[index]
            label = self.tab_labels[index]
            self.ui.tabWidget.insertTab(index, widget, label)

        for index in range(self.ui.tabWidget.count()):
            page_widget = self.ui.tabWidget.widget(index)
            for widget in page_widget.findChildren(
                    QtWidgets.QWidget, QtCore.QRegExp('^cfg|^cmd|^txt|^chk')):
                widget_name = str(widget.objectName())
                param_name = str(widget_name[3:])
                if param_name in self.param_to_widgets:
                    self.param_to_widgets.get(param_name).append(widget)
                else:
                    self.param_to_widgets[param_name] = [widget]
                widget.param = param_name
                widget.defaultvalue = None
                widget.tab_index = index
                widget.isCommand = widget_name.startswith("cmd")
                self.ui_widgets.append(widget)
                self._connectWidgetToSignalMap(widget)

        # WE CREATE THE UNKNOWN_TAB FOR NEW_PARAMETERS THE APPLICATION DOES NOT
        # KNOW
        self.unknown_tab, self.unknown_table_widget = self.createTableWidget(
            ["Name", "Value", "New Value"])
        self.lastTabSelected = 0
        if test_mode:
            return

        self.widgets_modified = []
        # THIS LIST SHOULD BE POPULATED WITH DRIVERS BUT IT IS NOT SUFFICIENT
        # BECAUSE THE __cmp__ METHOD OF THE ICEPAPDRIVER SETS CONFLICTS AND WE
        # JUST WANT TO SEARCH, INSTEAD OF THE DRIVER OBJECT IT WILL BE
        # POPULATED BY THE KEY COMPOSED BY: ICEPAP_SYSTEM + "_" + DRIVER_ADDR
        self.saveConfigPending = []
        self.tabs_modified = {}
        self.tabs_configPending = {}
        self.ui.tabWidget.setCurrentIndex(self.lastTabSelected)

        self.refreshTimer = Qt.QTimer(self)
        self.sliderTimer = Qt.QTimer(self)
        self.sliderTimer.setInterval(100)

        self.signalConnections()

        self._setWidgetToolTips()

        self._manager = MainManager()
        self.ui.btnUndo.setEnabled(False)

        self.setLedsOff()
        self.icepap_driver = None
        self.inMotion = -1
        self.status = -1

        self.ui.historicWidget.setCfgPage(self)
        self.hideHistoricWidget()

        self.ui.sliderJog.setEnabled(False)

        # PALETTES TO HIGHLIGHT WIDGETS
        white_brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        grey_brush = QtGui.QBrush(QtGui.QColor(239, 235, 231))
        yellow_brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
        salmon_brush = QtGui.QBrush(QtGui.QColor(255, 206, 162))
        blue_brush = QtGui.QBrush(QtGui.QColor(135, 206, 250))

        self.base_white_palette = QtGui.QPalette()
        self.base_yellow_palette = QtGui.QPalette()
        self.base_salmon_palette = QtGui.QPalette()

        self.button_grey_palette = QtGui.QPalette()
        self.button_yellow_palette = QtGui.QPalette()
        self.button_salmon_palette = QtGui.QPalette()
        self.button_blue_palette = QtGui.QPalette()

        self.base_white_palette.setBrush(
            QtGui.QPalette.Active, QtGui.QPalette.Base, white_brush)
        self.base_white_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Base,
            white_brush)
        self.base_yellow_palette.setBrush(
            QtGui.QPalette.Active, QtGui.QPalette.Base, yellow_brush)
        self.base_yellow_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Base,
            yellow_brush)
        self.base_salmon_palette.setBrush(
            QtGui.QPalette.Active, QtGui.QPalette.Base, salmon_brush)
        self.base_salmon_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Base,
            salmon_brush)

        self.button_grey_palette.setBrush(
            QtGui.QPalette.Active, QtGui.QPalette.Button, grey_brush)
        self.button_grey_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Button,
            grey_brush)
        self.button_yellow_palette.setBrush(
            QtGui.QPalette.Active, QtGui.QPalette.Button, yellow_brush)
        self.button_yellow_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Button,
            yellow_brush)
        self.button_salmon_palette.setBrush(
            QtGui.QPalette.Active, QtGui.QPalette.Button, salmon_brush)
        self.button_salmon_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Button,
            salmon_brush)
        self.button_blue_palette.setBrush(
            QtGui.QPalette.Active, QtGui.QPalette.Button, blue_brush)
        self.button_blue_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Button,
            blue_brush)

        # PALETTES TO HIGHLIGHT THE DESCRIPTION QFRAME
        light_blue_brush = QtGui.QBrush(QtGui.QColor(224, 255, 255))
        self.qframe_lightblue_palette = QtGui.QPalette()
        self.qframe_salmon_palette = QtGui.QPalette()
        self.qframe_lightblue_palette.setBrush(
            QtGui.QPalette.Active, QtGui.QPalette.Window, light_blue_brush)
        self.qframe_lightblue_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Window,
            light_blue_brush)
        self.qframe_salmon_palette.setBrush(
            QtGui.QPalette.Active, QtGui.QPalette.Window, salmon_brush)
        self.qframe_salmon_palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.Window,
            salmon_brush)

        self.dbStartupConfig = None

    @loggingInfo
    def signalConnections(self):
        self.ui.btnBlink.pressed.connect(self.btnBlink_on_press)
        self.ui.tabWidget.currentChanged.connect(self.tabWidget_currentChanged)
        self.ui.btnSendCfg.clicked.connect(self.btnSendCfg_on_click)
        self.ui.btnSaveCfg.clicked.connect(self.btnSaveCfg_on_click)
        self.refreshTimer.timeout.connect(self.updateTestStatus)
        self.ui.btnEnable.clicked.connect(self.endisDriver)
        self.ui.txtSpeed.editingFinished.connect(self.setMotionValues)
        self.ui.txtAcceleration.editingFinished.connect(self.setMotionValues)
        self.ui.btnGO.clicked.connect(self.btnGO_on_click)
        self.ui.btnGORelativePos.clicked.connect(
            self.btnGORelativePos_on_click)
        self.ui.btnGORelativeNeg.clicked.connect(
            self.btnGORelativeNeg_on_click)
        self.ui.btnStopMotor.clicked.connect(self.btnStopMotor_on_click)
        self.ui.btnSetPos.clicked.connect(self.setPosition)
        self.ui.btnSetEnc.clicked.connect(self.setEncoder)
        self.ui.btnUndo.clicked.connect(self.btnUndo_on_click)
        self.ui.btnRestore.clicked.connect(self.btnRestore_on_click)
        self.ui.sliderJog.sliderMoved.connect(self.startJogging)
        self.ui.sliderJog.valueChanged.connect(self.sliderChanged)
        self.ui.sliderJog.sliderReleased.connect(self.stopJogging)
        self.ui.sliderJog.valueChanged.connect(self.sliderChanged)
        self.sliderTimer.timeout.connect(self.resetSlider)
        self.ui.cmdCSWITCH.currentIndexChanged.connect(
            self.changeSwitchesSetup)
        self.ui.btnHomeSrch.clicked.connect(self._display_home_srch_dialog)

    def enable_home_srch_button(self):
        """Enables the HOME/SRCH button."""
        self.ui.btnHomeSrch.setDisabled(False)

    def _display_home_srch_dialog(self):
        system = self.icepap_driver.icepapsystem_name
        addr = self.icepap_driver.addr
        axis = IcepapsManager().iPaps[system][addr]
        if Mode.CONFIG in axis.mode:
            msg = 'Axis is in config mode. Aborting'
            print(msg)
            MessageDialogs.showErrorMessage(None, 'HOME/SRCH', msg)
        dlg = DialogHomeSrch(self, axis)
        dlg.show()
        self.ui.btnHomeSrch.setDisabled(True)

    @loggingInfo
    def highlightWidget(self, widget):
        # AGAIN, COMMAND WIDGETS ARE ONLY CHECKED IN THE QCOMBOBOX
        # ELIF SECTION
        if not isinstance(widget, QtWidgets.QWidget):
            self.log.error("THIS WIDGET SHOULD NOT BE INTENDED TO "
                           "HIGHLIGHT... NOT A QWIDGET %s",
                           widget.objectName())
            return

        if widget.defaultvalue is None:
            widget_name = widget.objectName()
            if widget_name.startswith("txt"):
                # PASS IT IS NORMAL TO NOT HIGHLIGHT IT, JUST INFO
                # txtNCURR, txtPCLOOP
                pass
            elif widget_name.count("_") > 0:
                # IT IS A FLAG OF A FLAGS PARAMETER, SO IT'S PARENT SHOULD BE
                # HIGHLIGHTED
                self.highlightWidget(widget.parent())
            else:
                pass
            return

        highlight = False
        sendConfig = False
        saveConfig = False

        param = widget.param
        if param == "DriverName":
            param = "IPAPNAME"

        dbvalue = self.dbStartupConfig.getParameter(
            str(param), in_memory=False)
        if dbvalue is None:
            dbvalue = ""
            # SPECIAL CASE IS THE FLAGS PARAMETER WHICH IS STORED
        wvalue = self._getWidgetValue(widget)
        defvalue = widget.defaultvalue
        if defvalue is None:
            defvalue = ""

        try:
            if isinstance(widget, QtWidgets.QDoubleSpinBox) or isinstance(
                    widget, QtWidgets.QSpinBox):
                if widget.defaultvalue != wvalue:
                    highlight = True
                    sendConfig = True
                    widget.setPalette(self.base_yellow_palette)
                elif abs(float(wvalue) - float(dbvalue)) > 0.01:
                    saveConfig = True
                    widget.setPalette(self.base_salmon_palette)
                else:
                    widget.setPalette(self.base_white_palette)

            elif isinstance(widget, QtWidgets.QCheckBox):
                if widget.defaultvalue != wvalue:
                    highlight = True
                    sendConfig = True
                    widget.setPalette(self.base_yellow_palette)
                elif wvalue != dbvalue:
                    saveConfig = True
                    widget.setPalette(self.base_salmon_palette)
                else:
                    widget.setPalette(self.base_white_palette)

            elif isinstance(widget, QtWidgets.QComboBox):
                try:
                    dbvalue = dbvalue
                    wvalue = wvalue
                    defvalue = defvalue
                    if widget.defaultvalue is None:
                        widget.defaultvalue = ""
                    elif defvalue != wvalue:
                        highlight = True
                        sendConfig = True
                        widget.setPalette(self.button_yellow_palette)
                        # SPECIAL CASE WITH COMMAND WIDGETS
                        if widget.isCommand:
                            widget.setPalette(self.button_blue_palette)
                    elif wvalue != dbvalue:
                        saveConfig = True
                        widget.setPalette(self.button_salmon_palette)
                        # SPECIAL CASE WITH COMMAND WIDGETS
                        if widget.isCommand:
                            saveConfig = False
                            widget.setPalette(self.button_blue_palette)

                    else:
                        widget.setPalette(self.button_grey_palette)
                except Exception as e:
                    self.log.error("some exception found trying to "
                                   "highlight a QComboBox %s!: %s",
                                   widget.objectName(), e)

            elif isinstance(widget, QtWidgets.QLineEdit):
                if dbvalue is None:
                    dbvalue = ""
                dbvalue = dbvalue
                wvalue = wvalue
                defvalue = defvalue
                if defvalue is None:
                    widget.defaultvalue = ""
                    defvalue = ""

                if defvalue != wvalue:
                    highlight = True
                    sendConfig = True
                    widget.setPalette(self.base_yellow_palette)
                elif wvalue != dbvalue:
                    saveConfig = True
                    widget.setPalette(self.base_salmon_palette)
                else:
                    widget.setPalette(self.base_white_palette)

            elif isinstance(widget, QtWidgets.QFrame):
                regexp = QtCore.QRegExp('^' + widget.objectName() + "_")
                for w in self.ui.tabWidget.findChildren(QtWidgets.QWidget,
                                                        regexp):
                    w_param_str = str(w.objectName())
                    w_param = "_".join(w_param_str.split("_")[1:])
                    defvalue_count = defvalue.count(w_param)
                    dbvalue_count = dbvalue.count(w_param)
                    if (w.isChecked() and (defvalue_count == 0)) or (
                            not w.isChecked() and defvalue_count > 0):
                        highlight = True
                        sendConfig = True
                        w.setPalette(self.base_yellow_palette)
                    elif (w.isChecked() and (dbvalue_count == 0)) or \
                            (not w.isChecked() and dbvalue_count > 0):
                        saveConfig = True
                        w.setPalette(self.base_salmon_palette)
                    else:
                        w.setPalette(self.base_white_palette)

        except Exception as e:
            self.log.error("Some exception found with param %s on method "
                           "highlightWidget: %s", param, e)

        if highlight:
            if widget not in self.widgets_modified:
                self.widgets_modified.append(widget)
        else:
            if widget in self.widgets_modified:
                self.widgets_modified.remove(widget)

        driver_key = self.icepap_driver.icepapsystem_name + \
            "_" + str(self.icepap_driver.addr)
        if saveConfig and driver_key not in self.saveConfigPending:
            self.saveConfigPending.append(driver_key)

        tab_index = widget.tab_index
        index_in_tabs_modified = tab_index in self.tabs_modified
        index_in_tabs_configPending = tab_index in self.tabs_configPending
        if highlight:
            if index_in_tabs_modified:
                self.tabs_modified.get(tab_index).append(widget)
            else:
                self.tabs_modified[tab_index] = [widget]
        elif saveConfig:
            if index_in_tabs_configPending:
                self.tabs_configPending.get(tab_index).append(widget)
            else:
                self.tabs_configPending[tab_index] = [widget]
        else:
            if index_in_tabs_modified:
                widget_list = self.tabs_modified.get(tab_index)
                if widget in widget_list:
                    widget_list.remove(widget)
                    if len(widget_list) == 0:
                        self.tabs_modified.pop(tab_index)
            if index_in_tabs_configPending:
                widget_list = self.tabs_configPending.get(tab_index)
                if widget in widget_list:
                    widget_list.remove(widget)
                    if len(widget_list) == 0:
                        self.tabs_configPending.pop(tab_index)

        # ONLY ALLOW SEND/SAVE CONFIG BUTTONS IF CONFIG NEEDED
        # Change behaviour in version 1.23
        enable_send = len(self.widgets_modified) > 0
        enable_save = driver_key in self.saveConfigPending and not sendConfig
        self.ui.btnSendCfg.setEnabled(enable_send)
        self.ui.btnSaveCfg.setEnabled(enable_save)
        self._mainwin.ui.actionSaveConfig.setEnabled(enable_save)

    @loggingInfo
    def _connectHighlighting(self):
        self.signalMapper.mapped[QtWidgets.QWidget].connect(
            self.highlightWidget)

    @loggingInfo
    def _disconnectHighlighting(self):
        try:
            self.signalMapper.mapped[QtWidgets.QWidget].disconnect(
                self.highlightWidget)
        except Exception:
            pass

    @loggingInfo
    def _setWidgetToolTips(self):
        """ Reads the driverparameters file and sets the tooltips"""

        UI_PARS = list(self.param_to_widgets.keys())
        FOUND_PARS = []
        NOT_FOUND_PARS = []
        MISSING_TOOLTIPS = []

        driverparameters = resource_filename('icepapcms.templates',
                                             'driverparameters.xml')

        doc = minidom.parse(driverparameters)
        root = doc.documentElement
        for section in root.getElementsByTagName("section"):
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    parid = pars.attributes.get('id').value
                    parid = parid.strip()
                    parname = pars.attributes.get('name').value
                    parname = parname.strip()
                    pardesc = self._getText(
                        pars.getElementsByTagName("description")[0].firstChild)

                    # SHOULD I USE pardesc as the tooltip?
                    try:
                        if parid in self.param_to_widgets:
                            widgets = self.param_to_widgets[parid]
                            for w in widgets:
                                w.setToolTip(pardesc)
                            FOUND_PARS.append(parid)
                        else:
                            NOT_FOUND_PARS.append(parid)
                    except Exception as e:
                        self.log.error('Exception on _setWidgetToolTips: '
                                       '%s', e)
                else:
                    self.log.error('_setWidgetToolTips, what is happening?')

        DEBUG_MISSING_TOOLTIPS = False

        #TODO Evaluate how to integrate this code
        if DEBUG_MISSING_TOOLTIPS:
            for p in UI_PARS:
                if p not in FOUND_PARS and p not in NOT_FOUND_PARS:
                    MISSING_TOOLTIPS.append(p)
            print('\n\nfound:', FOUND_PARS)
            print('\n\nnot found:', NOT_FOUND_PARS)
            print('\n\nmissing:', MISSING_TOOLTIPS)

    @loggingInfo
    def createTableWidget(self, column_names):
        widget = QtWidgets.QWidget()
        table_widget = QtWidgets.QTableWidget(widget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(218, 224, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(218, 224, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Inactive,
            QtGui.QPalette.AlternateBase,
            brush)
        brush = QtGui.QBrush(QtGui.QColor(218, 224, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(
            QtGui.QPalette.Disabled,
            QtGui.QPalette.AlternateBase,
            brush)
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(Qt.Qt.black))
        table_widget.setPalette(palette)
        table_widget.setAlternatingRowColors(True)
        table_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        table_widget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems)
        table_widget.setGridStyle(QtCore.Qt.SolidLine)
        table_widget.horizontalHeader().setStretchLastSection(True)

        columns = len(column_names)
        table_widget.clear()
        table_widget.setColumnCount(columns)
        table_widget.setRowCount(0)

        for i in range(columns):
            item = QtWidgets.QTableWidgetItem()
            item.setText(column_names[i])
            table_widget.setHorizontalHeaderItem(i, item)

        vboxlayout = QtWidgets.QVBoxLayout(widget)
        vboxlayout.setContentsMargins(9, 9, 9, 9)
        vboxlayout.setSpacing(6)
        vboxlayout.addWidget(table_widget)
        widget.setLayout(vboxlayout)

        return (widget, table_widget)

    @loggingInfo
    def _addItemToTable(self, section, row, column, text, editable):
        pass

    @loggingInfo
    def _addWidgetToTable(self, section, row, column,
                          widget_type, min, max, unknownTab=False):
        pass

    @loggingInfo
    def setDescription(self):
        driver = self.icepap_driver
        signature = self.icepap_driver.current_cfg.signature
        desc_cfg_system = self.icepap_driver.icepapsystem_name
        desc_cfg_crate = self.icepap_driver.cratenr
        desc_cfg_addr = self.icepap_driver.addr
        desc_cfg_name = self.icepap_driver.name
        desc_cfg_version = self.icepap_driver.current_cfg.getParameter(
            'VER', True)
        hwversion = IcepapsManager().readIcepapParameters(
            desc_cfg_system, desc_cfg_addr, [['VER', 'PCB']])
        cfg_db = ConfigManager().config["database"]["database"]
        desc_cfg_hwversion = hwversion[0][1]
        desc_cfg_dbhost = ConfigManager().config["database"]["server"]
        if cfg_db == 'sqlite':
            desc_cfg_dbhost = ConfigManager().config["database"]["folder"]
        desc_cfg_date = 'NO_DATE'
        desc_cfg_user = 'NO_USER'
        desc_cfg_host = 'NO_HOST'
        if signature:
            try:
                aux = signature.split('_')
                desc_cfg_host = aux[0]
                # As from version 1.17, the signature includes the username
                user_and_host = aux[0]
                aux2 = user_and_host.split('@')
                if len(aux2) > 1:
                    desc_cfg_user = aux2[0]
                    desc_cfg_host = aux2[1]
                hex_epoch = aux[1]
                try:
                    desc_cfg_date = datetime.datetime.fromtimestamp(
                        int(hex_epoch, 16)).ctime()
                    # AS OF VERSION 1.20, SIGNATURE HAS NOT HEX TIMESTAMP BUT A
                    # MORE READABLE ONE
                except BaseException:
                    desc_cfg_date = datetime.datetime.strptime(
                        aux[1] + '_' + aux[2], '%Y/%m/%d_%H:%M:%S').ctime()

            except Exception:
                msg = 'Not standard signature of driver ' + \
                    str(desc_cfg_addr) + \
                    '.\nIt does not match (user@host_DATE).\nValue is:' + \
                    str(signature)
                MessageDialogs.showWarningMessage(
                    self, "Not standard signature", msg)
        else:
            signature = None

        self.ui.dscDriverName.setText(driver.name)
        self.ui.dscActive.setText(
            driver.current_cfg.getParameter(
                str('ACTIVE')))
        if signature is None:
            self.ui.dscSignature.setText('NO_CONFIG')
        else:
            self.ui.dscSignature.setText(desc_cfg_date)
            html_signature = '<HTML><BODY>'
            html_signature += '<H2>More info:</H2>\n'
            html_signature += '<TABLE>\n'
            html_signature += '<TR><H2>%s/%s/%s</H2></TR>\n' % (
                desc_cfg_system, desc_cfg_crate, desc_cfg_addr)
            html_signature += \
                '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % (
                    'Axis name', desc_cfg_name)
            html_signature += \
                '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % (
                    'Firmware version', desc_cfg_version)
            html_signature += \
                '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % (
                    'Hardware version', desc_cfg_hwversion)
            html_signature += \
                '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % (
                    'Database host', desc_cfg_dbhost)
            html_signature += \
                '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % (
                    'Last saved config', desc_cfg_date)
            html_signature += \
                '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % (
                    'User', desc_cfg_user)
            html_signature += \
                '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % (
                    'Host', desc_cfg_host)
            html_signature += \
                '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % (
                    'Raw', signature)
            html_signature += '</TABLE></BODY></HTML>\n'
            self.ui.dscSignature.setToolTip(html_signature)

        if self.ui.dscActive.text() == 'YES':
            self.ui.frame_description.setPalette(self.qframe_lightblue_palette)
        else:
            self.ui.frame_description.setPalette(self.qframe_salmon_palette)

    @loggingInfo
    def fillData(self, icepap_driver):
        """ TO-DO STORM review"""
        QtWidgets.QApplication.instance().setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.icepap_driver = icepap_driver
        self._disconnectHighlighting()

        self.widgets_modified = []
        self.tabs_modified = {}
        self.tabs_configPending = {}

        driver_key = self.icepap_driver.icepapsystem_name + \
            "_" + str(self.icepap_driver.addr)
        if driver_key in self.saveConfigPending:
            self.saveConfigPending.remove(driver_key)
        dbIcepapSystem = StormManager().getIcepapSystem(
            self.icepap_driver.icepapsystem_name)
        self.dbStartupConfig = dbIcepapSystem.getDriver(
            self.icepap_driver.addr, in_memory=False).startup_cfg
        self.icepap_driver.startup_cfg = self.dbStartupConfig

        unknownParams = False
        self.unknown_table_widget.clear()
        self.unknown_table_widget.setRowCount(0)

        for name, value in icepap_driver.current_cfg.toList():
            if name in self.param_to_widgets:
                widgets = self.param_to_widgets.get(name)
                self._setWidgetsValue(widgets, value)
            elif name in ['IPAPNAME', 'VER', 'ID']:
                # THESE PARAMS DO NOT COME FROM THE FIRMWARE
                # HARDCODED DRIVER NAME
                if name == 'IPAPNAME':
                    self._setWidgetsValue(
                        self.param_to_widgets.get('DriverName'), value)
                    self.icepap_driver.setName(value)
                    # WE SHOULD GET THE TREE NODE AND UPDATE IT'S LABEL
                    # WE SHOULD ALSO SET THE DRIVER NAME
                    modelindex = self._mainwin.ui.treeView.currentIndex()
                    drivernode = self._mainwin._tree_model.item(modelindex)
                    label = str(self.icepap_driver.addr) + \
                        " " + self.icepap_driver.name
                    if drivernode is not None:
                        drivernode.changeLabel([label])
            else:
                unknownParams = True
                self.addUnknownWidget(name, value)

        unknown_index = self.ui.tabWidget.indexOf(self.unknown_tab)

        if unknownParams:
            if unknown_index == -1:
                unknown_index = self.ui.tabWidget.count()
                self.ui.tabWidget.insertTab(
                    unknown_index, self.unknown_tab, "Unknown")
        elif unknown_index != -1:
            self.ui.tabWidget.removeTab(unknown_index)

        self.highlightTabs()

        self.startTesting()

        if self.ui.historicWidget.isVisible():
            self.ui.historicWidget.fillData(self.icepap_driver)

        self.ui.tabWidget.setCurrentIndex(self.lastTabSelected)
        self.setDescription()
        self._connectHighlighting()

        # ALWAYS PUT THE DRIVER IN CONFIG MODE
        # It may happen that the driver is in PROG MODE

        # NOT VALID ANY MORE (SINCE VERSION 1.23 ONLY IN CONFIG IF NECESSARY
        # mode = self._manager.startConfiguringDriver(self.icepap_driver)
        mode = self.icepap_driver.mode
        if mode != Mode.PROG:
            self.ui.tabWidget.setEnabled(True)
        else:
            # MAY BE ALSO GOOD FOR THE SHUTTER MODE
            MessageDialogs.showErrorMessage(
                None,
                'Start configuring driver',
                'It is not possible to configure the driver\n'
                'while it is in mode PROG.')
            self.ui.tabWidget.setEnabled(False)
        QtWidgets.QApplication.instance().restoreOverrideCursor()

    @loggingInfo
    def addUnknownWidget(self, param_name, param_value):
        # TODO Review this code
        cfginfo = IcepapsManager().icepap_cfginfos[
            self.icepap_driver.icepapsystem_name][
            self.icepap_driver.addr].get(param_name)

        if cfginfo is not None:
            row = self.unknown_table_widget.rowCount()
            self.unknown_table_widget.insertRow(row)

            widget = None
            if len(cfginfo) > 0:
                if "INTEGER" == cfginfo[0]:
                    widget = QtWidgets.QSpinBox()
                    widget.setMaximum(999999999)
                    widget.setMinimum(-999999999)
                elif "FLOAT" == cfginfo[0]:
                    widget = QtWidgets.QDoubleSpinBox()
                    widget.setMaximum(999999999)
                    widget.setMinimum(-999999999)
                elif cfginfo[0].startswith("["):
                    param_tooltip = "FLAGS:"
                    for flag in cfginfo:
                        # MORE EFFORT THAN NEEDED BUT...
                        flag.replace("[", "")
                        flag.replace("]", "")
                        param_tooltip += " " + flag
                    widget = QtWidgets.QLineEdit()
                    widget.setToolTip(param_tooltip)
                elif cfginfo[0].startswith("STRING"):
                    widget = QtWidgets.QLineEdit()
                    param_tooltip = str(cfginfo)
                    widget.setToolTip(param_tooltip)
                else:
                    widget = QtWidgets.QComboBox()
                    param_tooltip = str(cfginfo)
                    widget.setToolTip(param_tooltip)

            if widget is not None:
                widget.param = param_name
                widget.isCommand = False
                widget.tab_index = self.ui.tabWidget.indexOf(self.unknown_tab)
                param_item = QtWidgets.QTableWidgetItem()
                param_item.setText(param_name)
                param_item.setFlags(Qt.Qt.ItemIsSelectable)
                self.unknown_table_widget.setItem(row, 0, param_item)
                value_item = QtWidgets.QTableWidgetItem()
                value_item.setText(str(param_value))
                value_item.setFlags(Qt.Qt.ItemIsSelectable)
                self.unknown_table_widget.setItem(row, 1, value_item)

                self.unknown_table_widget.setCellWidget(row, 2, widget)

                self.param_to_unknown_widgets[param_name] = widget

                self._setWidgetsValue([widget], param_value)

                self._connectWidgetToSignalMap(widget)

    @loggingInfo
    def checkSaveConfigPending(self):
        # THIS METHOD IS CALLED WHEN THE USER WANTED TO
        if self.icepap_driver is not None:
            driver_key = self.icepap_driver.icepapsystem_name + \
                "_" + str(self.icepap_driver.addr)
            if driver_key in self.saveConfigPending:
                # IT SHOULD STILL BE EN CONFIG MODE BECAUSE SOME VALUES
                # MISMATCH FROM DATABASE
                return True
            else:
                self._manager.endConfiguringDriver(self.icepap_driver)
                return False

    @loggingInfo
    def _connectWidgetToSignalMap(self, widget):
        self.signalMapper.setMapping(widget, widget)
        if isinstance(widget, QtWidgets.QDoubleSpinBox) or isinstance(
                widget, QtWidgets.QSpinBox):
            widget.valueChanged.connect(self.signalMapper.map)
        elif isinstance(widget, QtWidgets.QCheckBox):
            widget.stateChanged.connect(self.signalMapper.map)
        elif isinstance(widget, QtWidgets.QComboBox):
            widget.currentIndexChanged.connect(self.signalMapper.map)
        elif isinstance(widget, QtWidgets.QLineEdit):
            widget.textChanged.connect(self.signalMapper.map)

    @loggingInfo
    def _setWidgetsValue(self, widgets, value, set_default=True):
        # THE CMD WIDGETS RIGHT NOW ARE ONLY QCOMBOBOXES SO THE SPECIAL CODE IS
        # JUST IN THAT ELIF SECTION
        for widget in widgets:
            try:
                system_name = self.icepap_driver.icepapsystem_name
                driver_addr = self.icepap_driver.addr
                if isinstance(widget, QtWidgets.QDoubleSpinBox) or isinstance(
                        widget, QtWidgets.QSpinBox):
                    widget.setValue(float(value))
                    if set_default:
                        widget.defaultvalue = widget.value()
                elif isinstance(widget, QtWidgets.QCheckBox):
                    state = (value == "1" or value == "YES")
                    widget.setChecked(state)
                    if set_default:
                        widget.defaultvalue = value
                elif isinstance(widget, QtWidgets.QComboBox):
                    widget.clear()
                    param = widget.param
                    controller = IcepapsManager()
                    driver_cfginfo = \
                        controller.icepap_cfginfos[system_name][driver_addr]
                    options = driver_cfginfo.get(param)
                    if options is not None:
                        for option in options:
                            widget.addItem(str(option))
                        # 20130412 IT SEEMS THAT INDEXER COMMAND SHOULD HAVE
                        #          ALSO LINKED AS AN OPTION, BUT IT IS NOT
                        #          PROVIDED BY CFGINFO... I WILL ADD IT
                        #          MANUALLY BUT IT MAY BE REMOVED LATER
                        # 20140219 IT SEEMS _NOW_ THAT IS NOT NEEDED ANY MORE
                        # widget.addItem('LINKED')

                    # SPECIAL CASE TO THE TEST WIDGETS
                    if widget.isCommand:
                        if controller.getDriverActiveStatus(
                                system_name, driver_addr) == "NO":
                            widget.setEnabled(False)
                        else:
                            widget.setEnabled(True)
                            # SHOULD RETRIEVE THE VALUE FROM THE DRIVER'S
                            # COMMAND
                            if param == 'AUXPS':
                                # THIS VALUE DOES NOT COME IN THE CONFIGURATION
                                pass
                            elif param == 'CSWITCH':
                                # THIS VALUE DOES NOT COME NEITHER IN THE
                                # CONFIGUARTION
                                self.log.error('_setWidgetsValue '
                                               'eo....cswitch')
                                pass
                            elif param == 'INDEXER':
                                values = controller.readIcepapParameters(
                                    system_name, driver_addr, ['INDEXER'])
                                indexer_answer = values[0]
                                value = indexer_answer[1]
                                # 20140219 IT SEEMS _NOW_ THAT LINKED IS STILL
                                # NEEDED
                                widget.addItem('LINKED')
                                widget.setEnabled(False)
                            elif param.startswith('INFOA'):
                                values = controller.readIcepapParameters(
                                    system_name, driver_addr, ['INFOA'])
                                infoa_values = values[0][1].split()
                                if param.endswith('SRC'):
                                    value = infoa_values[0]
                                else:
                                    value = infoa_values[1]
                            elif param.startswith('INFOB'):
                                values = controller.readIcepapParameters(
                                    system_name, driver_addr, ['INFOB'])
                                infob_values = values[0][1].split()
                                if param.endswith('SRC'):
                                    value = infob_values[0]
                                else:
                                    value = infob_values[1]
                            elif param.startswith('INFOC'):
                                values = controller.readIcepapParameters(
                                    system_name, driver_addr, ['INFOC'])
                                infoc_values = values[0][1].split()
                                if param.endswith('SRC'):
                                    value = infoc_values[0]
                                else:
                                    value = infoc_values[1]

                    widget.setCurrentIndex(
                        widget.findText(
                            str(value),
                            QtCore.Qt.MatchFixedString))
                    if set_default:
                        widget.defaultvalue = str(value)
                elif isinstance(widget, QtWidgets.QLineEdit):
                    widget.setText(str(value))
                    if set_default:
                        widget.defaultvalue = str(value)
                elif isinstance(widget, QtWidgets.QLabel):
                    widget.setText(str(value))
                elif isinstance(widget, QtWidgets.QFrame):
                    # WE NOW HAVE TO ITERATE THROUGOUT ALL THE CHECKBOXES:
                    if set_default:
                        widget.defaultvalue = value
                    regexp = QtCore.QRegExp('^' + widget.objectName() + "_")
                    for w in self.ui.tabWidget.findChildren(
                            QtWidgets.QWidget, regexp):
                        w_param = w.objectName().split("_")[1]
                        checked = False
                        if w_param in value:
                            checked = True
                        w.setChecked(checked)

                self.highlightWidget(widget)
            except Exception as e:
                self.log.error("_setWidgetValue %s error:", value, e)

    @loggingInfo
    def _getWidgetValue(self, widget):
        try:
            if isinstance(widget, QtWidgets.QDoubleSpinBox) or isinstance(
                    widget, QtWidgets.QSpinBox):
                return widget.value()
            elif isinstance(widget, QtWidgets.QCheckBox):
                if widget.isChecked():
                    return "YES"
                else:
                    return "NO"
            elif isinstance(widget, QtWidgets.QComboBox):
                return str(widget.currentText())
            elif isinstance(widget, QtWidgets.QLineEdit):
                # return str(widget.text()).upper()
                # FIX NON-ASCII ISSUES:
                text = str(widget.text())
                if not all(ord(c) < 128 for c in text):
                    text = repr(text)
                return text
            elif isinstance(widget, QtWidgets.QFrame):
                regexp = QtCore.QRegExp('^' + widget.objectName() + "_")
                flags_value = []
                for w in self.ui.tabWidget.findChildren(QtWidgets.QWidget,
                                                        regexp):
                    w_param_str = str(w.objectName())
                    w_param = "_".join(w_param_str.split("_")[1:])
                    if w.isChecked():
                        flags_value.append(w_param)
                return ' '.join(flags_value)
        except Exception as e:
            self.log.error("error in _getWidgetValue: %s", e)

    @loggingInfo
    def addNewCfg(self, cfg):
        QtWidgets.QApplication.instance().setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        for name, value in cfg.toList():
            if name in self.param_to_widgets:
                widgets = self.param_to_widgets.get(name)
                self._setWidgetsValue(widgets, value, set_default=False)
            elif name == 'IPAPNAME':
                self._setWidgetsValue(self.param_to_widgets.get(
                    'DriverName'), value, set_default=False)
        self.highlightTabs()
        QtWidgets.QApplication.instance().restoreOverrideCursor()

    @loggingInfo
    def _getText(self, node):
        rc = ""
        if node is not None:
            rc = str(node.data)
        return rc

    @loggingInfo
    def tabWidget_currentChanged(self, index):
        self.lastTabSelected = index
        self.highlightTabs()

    @loggingInfo
    def highlightTabs(self):
        tab_bar = self.ui.tabWidget.tabBar()
        for index in range(self.ui.tabWidget.count()):
            if index in self.tabs_modified:
                tab_bar.setTabIcon(index, QtGui.QIcon(
                    ":/icons/icons/ipapdrivermodified.png"))
            elif index in self.tabs_configPending:
                tab_bar.setTabIcon(index, QtGui.QIcon(
                    ":/icons/icons/ipapdrivercfg.png"))
            else:
                tab_bar.setTabIcon(index, QtGui.QIcon(""))

    @loggingInfo
    def btnSendCfg_on_click(self, checked=False, skip_fillData=False):
        if len(self.widgets_modified) == 0:
            return True
        self._mainwin.ui.actionHistoricCfg.setChecked(False)
        self.hideHistoricWidget()
        new_values = []
        new_command_values = []
        for widget in self.widgets_modified:
            # SPECIAL CASE TO THE DRIVER NAME THAT IS NOT A CONFIG PARAMETER
            # BUT IT IS TREATED AS SO, IT IS A COMMAND 'NAME' BUT IT IS STORED
            # IN THE DATABASE AS A CONFIGURATION PARAMETER
            param = widget.param
            value = self._getWidgetValue(widget)
            if not widget.isCommand:
                if param == 'DriverName':
                    param = 'IPAPNAME'
                new_values.append([param, value])
            else:
                # SINCE THE COMMAND PARAMS ARE NOT THE SAME AS THE CFG PARAMS
                # WE NEED A WORK-AROUND HERE AND FOR INFO COMMANDS ALWAYS
                # PROVIDE SRC AND POL IF BOTH SRC AND POL ARE MODIFIED,
                # WE WILL SENT TWICE THE COMMAND PAIR
                if widget.param.startswith('INFOA'):
                    param = 'INFOA'
                    src_value = None
                    pol_value = None
                    for w in self.param_to_widgets.get('INFOASRC'):
                        if w.isCommand:
                            src_value = self._getWidgetValue(w)
                    for w in self.param_to_widgets.get('INFOAPOL'):
                        if w.isCommand:
                            pol_value = self._getWidgetValue(w)
                    value = src_value + " " + pol_value
                elif widget.param.startswith('INFOB'):
                    param = 'INFOB'
                    src_value = None
                    pol_value = None
                    for w in self.param_to_widgets.get('INFOBSRC'):
                        if w.isCommand:
                            src_value = self._getWidgetValue(w)
                    for w in self.param_to_widgets.get('INFOBPOL'):
                        if w.isCommand:
                            pol_value = self._getWidgetValue(w)
                    value = src_value + " " + pol_value
                elif widget.param.startswith('INFOC'):
                    param = 'INFOC'
                    src_value = None
                    pol_value = None
                    for w in self.param_to_widgets.get('INFOCSRC'):
                        if w.isCommand:
                            src_value = self._getWidgetValue(w)
                    for w in self.param_to_widgets.get('INFOCPOL'):
                        if w.isCommand:
                            pol_value = self._getWidgetValue(w)
                    value = src_value + " " + pol_value
                else:
                    # THIS IS ANOTHER cmd that should be passed...
                    # AND BY DEFAULT DESIGN, param and value should be unique.
                    pass
                new_command_values.append([param, value])

        if len(new_values) > 0:
            setExpertFlag = self._mainwin.ui.actionSetExpertFlag.isChecked()
            send_ok = self._manager.saveValuesInIcepap(
                self.icepap_driver, new_values, expertFlag=setExpertFlag)
            if not send_ok:
                MessageDialogs.showWarningMessage(
                    self, "Driver configuration", "Wrong parameter format")
                return False

        if len(new_command_values) > 0:
            self._manager.writeIcepapParameters(
                self.icepap_driver.icepapsystem_name,
                self.icepap_driver.addr,
                new_command_values)

        if not skip_fillData:
            self.fillData(self.icepap_driver)

        if self.icepap_driver.hasUndoList():
            self.ui.btnUndo.setEnabled(True)
        else:
            self.ui.btnUndo.setEnabled(False)
        return True

    @loggingInfo
    def btnSaveCfg_on_click(self):
        save_ok = True
        if len(self.widgets_modified) > 0:
            save_ok = self.btnSendCfg_on_click(skip_fillData=True)
        if not save_ok:
            MessageDialogs.showWarningMessage(
                self, "Driver configuration",
                "Problems found saving the configuration")
            return
        self._mainwin.actionSaveConfigMth()

    @loggingInfo
    def btnUndo_on_click(self):
        self._manager.undoDriverConfiguration(self.icepap_driver)
        self.fillData(self.icepap_driver)
        if not self.icepap_driver.hasUndoList():
            self.ui.btnUndo.setEnabled(False)

    @loggingInfo
    def btnRestore_on_click(self):
        self.fillData(self.icepap_driver)

    @loggingInfo
    def doImport(self):
        filename = ""
        try:
            folder = ConfigManager().config["icepap"]["configs_folder"]
            fn = QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Config File", folder, "*.xml")
            if fn[0] == '':
                return
            filename = str(fn[0])
            self.fillFileData(filename)
        except Exception as e:
            msg = "Error reading file %s: %s".format(filename, e)
            self.log.warning(msg)
            MessageDialogs.showWarningMessage(self, "File", msg)

    @loggingInfo
    def fillFileData(self, filename):
        QtWidgets.QApplication.instance().setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        self._disconnectHighlighting()
        doc = minidom.parse(filename)
        for param_element in doc.getElementsByTagName("par"):
            param_name = param_element.attributes.get('name').value
            param_name = param_name.strip()
            param_value = param_element.attributes.get('value').value
            param_value = param_value.strip()
            if param_name in self.param_to_widgets:
                widgets = self.param_to_widgets.get(param_name)
                self._setWidgetsValue(widgets, param_value, set_default=False)
            elif param_name == 'IPAPNAME':
                self._setWidgetsValue(self.param_to_widgets.get(
                    'DriverName'), param_value, set_default=False)
            elif param_name in ['ID', 'VER']:
                pass
            else:
                # SINCE UNKNOWN WIDGETS ARE CREATED EVERY TIME, ANOTHER DICT
                # HAS TO BE AVAILABLE FOR THEM
                w = self.param_to_unknown_widgets.get(param_name)
                self._setWidgetsValue([w], param_value, set_default=False)

        self.highlightTabs()
        self._connectHighlighting()
        QtWidgets.QApplication.instance().restoreOverrideCursor()

    @loggingInfo
    def doExport(self):
        folder = ConfigManager().config["icepap"]["configs_folder"]
        fn = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Config File", folder, "*.xml")
        if fn[0] == '':
            return
        filename = str(fn[0])
        if filename.find('.xml') == -1:
            filename = filename + '.xml'
        self.exportToFile(filename)

    @loggingInfo
    def exportToFile(self, filename):
        with open(filename, 'w') as output:
            newdoc = self.getXmlData()
            data = newdoc.toprettyxml()
            output.write(data)

    @loggingInfo
    def getXmlData(self):
        doc = getDOMImplementation().createDocument(None, "Driver", None)
        dbIcepapSystem = StormManager().getIcepapSystem(
            self.icepap_driver.icepapsystem_name)
        dbConfig = dbIcepapSystem.getDriver(
            self.icepap_driver.addr, in_memory=False).startup_cfg
        config_list = sorted(dbConfig.toList())
        for param, value in config_list:
            param_element = doc.createElement("par")
            param_element.setAttribute("name", param)
            param_element.setAttribute("value", str(value))
            doc.documentElement.appendChild(param_element)
        return doc

    @loggingInfo
    def signDriver(self):
        self._disconnectHighlighting()
        self.icepap_driver.signDriver()
        self.fillData(self.icepap_driver)

    @loggingInfo
    def doCopy(self):
        self.temp_file = tempfile.TemporaryFile()
        data = self.getXmlData()
        self.temp_file.write(data.toprettyxml(encoding="utf-8"))
        self.temp_file.flush()
        self.temp_file.seek(0)

    @loggingInfo
    def doPaste(self):
        if self.temp_file is None:
            return
        self.temp_file.seek(0)
        self.fillFileData(self.temp_file)

# ------------------------------  Testing --------------------------------

    @loggingInfo
    def startTesting(self):
        if self.icepap_driver is not None:
            self.inMotion = -1
            self.status = -1
            self.ready = -1
            self.mode = -1
            self.power = -1
            self.updateTestStatus()
            self.refreshTimer.start(1000)

    @loggingInfo
    def stopTesting(self):
        try:
            self.refreshTimer.stop()
            self.setLedsOff()
        except BaseException  as e:
            self.log.error("Unexpected error on stopTesting: %s", e)

    @loggingInfo
    def getMotionValues(self):
        (speed, acc) = self._manager.getDriverMotionValues(
            self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
        self.ui.txtSpeed.setText(str(speed))
        self.ui.txtAcceleration.setText(str(acc))

    @loggingInfo
    def setMotionValues(self):
        speed = self.ui.txtSpeed.text()
        acc = self.ui.txtAcceleration.text()
        if speed == "":
            speed = "1000"
            self.ui.txtSpeed.setText(speed)
        if acc == "":
            acc = "0.25"
            self.ui.txtAcceleration.setText(acc)
        try:
            self._manager.setDriverMotionValues(
                self.icepap_driver.icepapsystem_name, self.icepap_driver.addr,
                [float(speed), float(acc)])
        except BaseException:
            MessageDialogs.showWarningMessage(
                self, "Driver testing", "Wrong parameter format")

    @loggingInfo
    def setLedsOff(self):
        self.ui.LedError.changeColor(Led.RED)
        self.ui.LedStep.changeColor(Led.YELLOW)
        self.ui.LedHome.changeColor(Led.BLUE)
        self.ui.LedLimitPos.changeColor(Led.ORANGE)
        self.ui.LedLimitNeg.changeColor(Led.GREEN)
        self.ui.LedError.off()
        self.ui.LedStep.off()
        self.ui.LedHome.off()
        self.ui.LedLimitPos.off()
        self.ui.LedLimitNeg.off()
        self.ui.LCDPosition.display(0)

    @loggingInfo
    def disableAllControl(self):
        self.ui.txtSpeed.setEnabled(False)
        self.ui.txtAcceleration.setEnabled(False)
        self.ui.btnGO.setEnabled(False)
        self.ui.btnGORelativeNeg.setEnabled(False)
        self.ui.btnGORelativePos.setEnabled(False)
        self.ui.sliderJog.setEnabled(False)
        self.ui.btnEnable.setEnabled(False)
        self.ui.btnStopMotor.setEnabled(False)

    @loggingInfo
    def enableAllControl(self):
        self.ui.txtSpeed.setEnabled(True)
        self.ui.txtAcceleration.setEnabled(True)

        self.ui.btnGORelativeNeg.setEnabled(True)
        self.ui.btnGORelativePos.setEnabled(True)
        if self.mode == 0:
            self.ui.btnGO.setEnabled(True)
            self.ui.sliderJog.setEnabled(True)
        else:
            self.ui.btnGO.setEnabled(False)
            self.ui.sliderJog.setEnabled(False)
        self.ui.btnEnable.setEnabled(True)
        self.ui.btnStopMotor.setEnabled(True)

    @loggingInfo
    def updateTestStatus(self):
        pos_sel = str(self.ui.cb_pos_sel.currentText())
        enc_sel = str(self.ui.cb_enc_sel.currentText())
        (status, power, position) = self._manager.getDriverTestStatus(
            self.icepap_driver.icepapsystem_name, self.icepap_driver.addr,
            pos_sel, enc_sel)

        axis_state = State(status)
        disabled = axis_state.get_disable_code()
        # TODO: use boolean instead of integers
        moving = int(axis_state.is_moving())
        ready = int(axis_state.is_ready())
        mode = axis_state.get_mode_code()
        if self.inMotion != moving:
            if moving == 1:
                self.refreshTimer.setInterval(700)
                self.ui.LedStep.on()
            elif moving == -1:
                self.refreshTimer.stop()
            else:
                self.refreshTimer.setInterval(1000)
                self.ui.LedStep.off()
        self.inMotion = moving

        if self.status != disabled or self.mode != mode or \
                self.power != power or self.ready != ready:
            if disabled == 0:
                if power:
                    self.ui.LedError.changeColor(Led.GREEN)
                    self.ui.LedError.on()
                    self.ui.btnEnable.setEnabled(True)
                    self.getMotionValues()
                    self.mode = mode
                    self.enableAllControl()
                    self.ui.btnEnable.setText("OFF")
                    self.ui.btnEnable.setChecked(True)
                else:
                    self.ui.btnEnable.setEnabled(True)
                    self.ui.btnEnable.setText("ON")
                    self.ui.btnEnable.setChecked(False)
                    self.ui.LedError.changeColor(Led.RED)
                    self.ui.LedError.on()
            elif disabled == 1:
                # driver is not active disable motion and enable
                self.disableAllControl()
                self.ui.LedError.changeColor(Led.RED)
                self.ui.LedError.on()
            else:
                self.ui.btnEnable.setEnabled(True)
                self.ui.btnEnable.setText("ON")
                self.ui.btnEnable.setChecked(False)
                self.ui.LedError.changeColor(Led.RED)
                self.ui.LedError.on()

        self.status = disabled
        self.ready = ready
        self.power = power

        if axis_state.is_inhome():
            self.ui.LedHome.on()
        else:
            self.ui.LedHome.off()

        lower = axis_state.is_limit_negative()
        upper = axis_state.is_limit_positive()
        if lower:
            self.ui.LedLimitNeg.on()
        else:
            self.ui.LedLimitNeg.off()

        if upper:
            self.ui.LedLimitPos.on()
        else:
            self.ui.LedLimitPos.off()

        # read position and encoder

        self.ui.LCDPosition.display(position[0])
        self.ui.LCDPositionTest.display(position[0])
        self.ui.LCDEncoder.display(position[1])

    @loggingInfo
    def btnGO_on_click(self):
        new_position = self.ui.txtMvAbsolute.text()
        try:
            new_position = int(new_position)
            self._manager.moveDriverAbsolute(
                self.icepap_driver.icepapsystem_name,
                self.icepap_driver.addr,
                new_position)
        except BaseException:
            MessageDialogs.showWarningMessage(
                self, "Driver testing", "Wrong parameter format")

    @loggingInfo
    def btnGORelativePos_on_click(self):
        distance = self.ui.txtGORelative.text()
        try:
            distance = int(distance)
            steps = +distance
            self._manager.moveDriver(
                self.icepap_driver.icepapsystem_name,
                self.icepap_driver.addr,
                steps)

        except BaseException:
            MessageDialogs.showWarningMessage(
                self, "Driver testing", "Wrong parameter format")

    @loggingInfo
    def btnGORelativeNeg_on_click(self):
        distance = self.ui.txtGORelative.text()
        try:
            distance = int(distance)
            steps = -distance
            self._manager.moveDriver(
                self.icepap_driver.icepapsystem_name,
                self.icepap_driver.addr,
                steps)

        except BaseException:
            MessageDialogs.showWarningMessage(
                self, "Driver testing", "Wrong parameter format")

    @loggingInfo
    def btnStopMotor_on_click(self):
        self._manager.stopDriver(
            self.icepap_driver.icepapsystem_name,
            self.icepap_driver.addr)
        self.ui.sliderJog.setValue(0)

    @loggingInfo
    def btnBlink_on_press(self):
        secs = 600
        if self.ui.btnBlink.isChecked():
            secs = 0
        self._manager.blinkDriver(
            self.icepap_driver.icepapsystem_name,
            self.icepap_driver.addr,
            secs)

    @loggingInfo
    def sliderChanged(self, div):
        if self.ui.sliderJog.isSliderDown() or not self.sliderTimer.isActive():
            self.startJogging(div)

    @loggingInfo
    def startJogging(self, div):
        if div != 0:
            if not self.ui.btnEnable.isChecked():
                self._manager.enableDriver(
                    self.icepap_driver.icepapsystem_name,
                    self.icepap_driver.addr)
            speed = float(self.ui.txtSpeed.text())
            factor = (self.ui.sliderJog.maximum() - abs(div)) + 1
            speed = int(speed / factor)
            if div < 0:
                speed = -1 * speed
            try:
                QtWidgets.QToolTip.showText(
                    self.cursor().pos(), str(speed), self.ui.sliderJog)
                self._manager.jogDriver(
                    self.icepap_driver.icepapsystem_name,
                    self.icepap_driver.addr,
                    speed)
            except Exception as e:
                MessageDialogs.showWarningMessage(
                    self, "Jog Driver",
                    "Error while trying to jog:\n" + str(e))
                self.ui.sliderJog.setValue(0)
        else:
            self.stopJogging()

    @loggingInfo
    def stopJogging(self):
        self._manager.stopDriver(
            self.icepap_driver.icepapsystem_name,
            self.icepap_driver.addr)
        self.ui.sliderJog.setValue(0)
        self.sliderTimer.start()

    @loggingInfo
    def resetSlider(self):
        value = self.ui.sliderJog.value()
        if value == 0:
            self.sliderTimer.stop()
        elif value > 0:
            self.ui.sliderJog.triggerAction(
                QtWidgets.QSlider.SliderSingleStepSub)
        else:
            self.ui.sliderJog.triggerAction(
                QtWidgets.QSlider.SliderSingleStepAdd)

    @loggingInfo
    def setPosition(self):
        pos_sel = str(self.ui.cb_pos_sel.currentText())
        try:
            position = int(self.ui.txtPos.text())
            self._manager.setDriverPosition(
                self.icepap_driver.icepapsystem_name,
                self.icepap_driver.addr,
                pos_sel,
                position)
        except BaseException as e:
            self.log.error("Unexpected error on setPosition: %s", e)
            MessageDialogs.showWarningMessage(
                self, "Set driver position", "Wrong parameter format")

    @loggingInfo
    def setEncoder(self):
        enc_sel = str(self.ui.cb_enc_sel.currentText())
        try:
            position = int(self.ui.txtEnc.text())
            self._manager.setDriverEncoder(
                self.icepap_driver.icepapsystem_name,
                self.icepap_driver.addr,
                enc_sel,
                position)
        except BaseException as e:
            self.log.error("Unexpected error on setEncoder: %s", e)
            MessageDialogs.showWarningMessage(
                self, "Set driver encoderposition", "Wrong parameter format")

    @loggingInfo
    def endisDriver(self, bool):
        if bool:
            self.ui.btnEnable.setText("OFF")
            self._manager.enableDriver(
                self.icepap_driver.icepapsystem_name,
                self.icepap_driver.addr)
        else:
            self.ui.btnEnable.setText("ON")
            self._manager.disableDriver(
                self.icepap_driver.icepapsystem_name,
                self.icepap_driver.addr)

    @loggingInfo
    def changeSwitchesSetup(self, mode):
        return
        # SHOULD CHANGE SWITCHES SETUP... HOW? NOT IN CONFIG MODE...

    # ---------------------- Historic Widget -------------------

    @loggingInfo
    def showHistoricWidget(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.historicWidget.fillData(self.icepap_driver)

    @loggingInfo
    def hideHistoricWidget(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    # ---------------------- Templates Catalog Widget -------------------

    @loggingInfo
    def setTemplateParams(self, template_name, params):
        QtWidgets.QApplication.instance().setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        self._disconnectHighlighting()
        for param in list(params.keys()):
            value = params.get(param)
            if param in self.param_to_widgets:
                widgets = self.param_to_widgets.get(param)
                self._setWidgetsValue(widgets, value, set_default=False)
            elif param == 'IPAPNAME':
                self._setWidgetsValue(self.param_to_widgets.get(
                    'DriverName'), value, set_default=False)
        # SHOULD DO SOMETHING WITH THE TEMPLATE NAME
        self.highlightTabs()
        self._connectHighlighting()
        QtWidgets.QApplication.instance().restoreOverrideCursor()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = PageiPapDriver(None, True)
    w.show()
    sys.exit(app.exec_())