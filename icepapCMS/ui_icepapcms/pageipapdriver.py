from PyQt4 import QtCore, QtGui, Qt
from pyIcePAP import *
from ui_pageipapdriver import Ui_PageiPapDriver
from ui_axis import Ui_axis
from ui_motor import Ui_motor
from ui_encoders import Ui_encoders
from ui_closedloop import Ui_closedloop
from ui_homing import Ui_homing
from ui_io import Ui_io

from qrc_icepapcms import *
from xml.dom import minidom, Node
from xml.dom.minidom import getDOMImplementation
from Led import Led
from lib_icepapcms import *
from messagedialogs import MessageDialogs
#from dialogtemplate import DialogTemplate
import sys
import os
from qvalidatelineedit import QValidateLineEdit
import time
import datetime
import tempfile
from historiccfgwidget import HistoricCfgWidget
from dialogcurves import DialogCurves
from dialogstatusinfo import DialogStatusInfo


class PageiPapDriver(QtGui.QWidget):
    """ Widget that manages all the information related to an icepap driver. Configuration, testing and historic configurations """

    def __init__(self, mainwin):
        QtGui.QWidget.__init__(self, None)
        self._mainwin = mainwin
        self.ui = Ui_PageiPapDriver()
        self.ui.setupUi(self)


        self.signalMapper = QtCore.QSignalMapper(self)

        self.axis = Ui_axis()
        axis_frame = QtGui.QFrame()
        self.axis.setupUi(axis_frame)

        self.motor = Ui_motor()
        motor_frame = QtGui.QFrame()
        self.motor.setupUi(motor_frame)

        self.encoders = Ui_encoders()
        encoders_frame = QtGui.QFrame()
        self.encoders.setupUi(encoders_frame)

        self.closedloop = Ui_closedloop()
        closedloop_frame = QtGui.QFrame()
        self.closedloop.setupUi(closedloop_frame)

        self.homing = Ui_homing()
        homing_frame = QtGui.QFrame()
        self.homing.setupUi(homing_frame)

        self.io = Ui_io()
        io_frame = QtGui.QFrame()
        self.io.setupUi(io_frame)

        self.param_to_widgets = {}
        self.ui_widgets = []

        self.param_to_unknown_widgets = {}

        self.tab_frames = [axis_frame,motor_frame,encoders_frame,closedloop_frame,homing_frame,io_frame]
        self.tab_labels = ["Axis","Motor","Encoders","Closed loop","Homing","I/O"]

        for index in range(len(self.tab_labels)):
            widget = self.tab_frames[index]
            label = self.tab_labels[index]
            self.ui.tabWidget.insertTab(index,widget,label)

            ###### PUT THE WIDGET INSIDE A SCROLL AREA
            ##########
            #####sa_layout = QtGui.QGridLayout()
            #####sa_widget = QtGui.QScrollArea()
            #####sa_widget.setWidget(widget)
            #####sa_widget.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
            #####sa_widget.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
            #####sa_widget.setFrameStyle(QtGui.QFrame.NoFrame)
            #####sa_layout.addWidget(sa_widget)
            #####self.ui.tabWidget.insertTab(index,sa_widget,label)

        for index in range(self.ui.tabWidget.count()):
            page_widget = self.ui.tabWidget.widget(index)
            for widget in page_widget.findChildren(QtGui.QWidget,QtCore.QRegExp('^cfg|^cmd|^txt|^chk')):
                widget_name = str(widget.objectName())
                param_name = str(widget_name[3:])
                if self.param_to_widgets.has_key(param_name):
                    self.param_to_widgets.get(param_name).append(widget)
                else:
                    self.param_to_widgets[param_name] = [widget]
                widget.param = param_name
                widget.defaultvalue = None
                widget.tab_index = index
                widget.isCommand = widget_name.startswith("cmd")
                self.ui_widgets.append(widget)
                self._connectWidgetToSignalMap(widget)

        # WE CREATE THE UNKNOWN_TAB FOR NEW_PARAMETERS THE APPLICATION DOES NOT KNOW
        self.unknown_tab, self.unknown_table_widget = self.createTableWidget(["Name", "Value", "New Value"])
        self.lastTabSelected = 0

        self.widgets_modified = []
        # THIS LIST SHOULD BE POPULATED WITH DRIVERS BUT IT IS NOT SUFFICIENT
        # BECAUSE THE __cmp__ METHOD OF THE ICEPAPDRIVER SETS CONFLICTS AND WE
        # JUST WANT TO SEARCH, INSTEAD OF THE DRIVER OBJECT IT WILL BE POPULATED
        # BY THE KEY COMPOSED BY: ICEPAP_SYSTEM + "_" + DRIVER_ADDR
        self.saveConfigPending = []
        self.tabs_modified = {}
        self.tabs_configPending = {}
        self.ui.tabWidget.setCurrentIndex(self.lastTabSelected)

        #self.ui.toolBox.setItemIcon(self.ui.toolBox.indexOf(self.ui.page_test), QtGui.QIcon(":/icons/IcepapCfg Icons/ipapdriver.png"))
        #self.ui.toolBox.setItemIcon(self.ui.toolBox.indexOf(self.ui.page_cfg), QtGui.QIcon(":/icons/IcepapCfg Icons/preferences-system.png"))
        #self.ui.tabWidget.removeTab(0)


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
        white_brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        grey_brush =  QtGui.QBrush(QtGui.QColor(239,235,231))
        yellow_brush = QtGui.QBrush(QtGui.QColor(255,255,0))
        salmon_brush = QtGui.QBrush(QtGui.QColor(255,206,162))
        blue_brush = QtGui.QBrush(QtGui.QColor(135,206,250))

        self.base_white_palette = QtGui.QPalette()
        self.base_yellow_palette = QtGui.QPalette()
        self.base_salmon_palette = QtGui.QPalette()

        self.button_grey_palette = QtGui.QPalette()
        self.button_yellow_palette = QtGui.QPalette()
        self.button_salmon_palette = QtGui.QPalette()
        self.button_blue_palette = QtGui.QPalette()

        self.base_white_palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,white_brush)
        self.base_white_palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,white_brush)
        self.base_yellow_palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,yellow_brush)
        self.base_yellow_palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,yellow_brush)
        self.base_salmon_palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,salmon_brush)
        self.base_salmon_palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,salmon_brush)

        self.button_grey_palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Button,grey_brush)
        self.button_grey_palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Button,grey_brush)
        self.button_yellow_palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Button,yellow_brush)
        self.button_yellow_palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Button,yellow_brush)
        self.button_salmon_palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Button,salmon_brush)
        self.button_salmon_palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Button,salmon_brush)
        self.button_blue_palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Button,blue_brush)
        self.button_blue_palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Button,blue_brush)

        # PALETTES TO HIGHLIGHT THE DESCRIPTION QFRAME
        light_blue_brush = QtGui.QBrush(QtGui.QColor(224,255,255))
        self.qframe_lightblue_palette = QtGui.QPalette()
        self.qframe_salmon_palette = QtGui.QPalette()
        self.qframe_lightblue_palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,light_blue_brush)
        self.qframe_lightblue_palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,light_blue_brush)
        self.qframe_salmon_palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Window,salmon_brush)
        self.qframe_salmon_palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Window,salmon_brush)


        self.dbStartupConfig = None

        self.ecpmt_just_enabled = False
        self.step_ini = 0
        self.enc_ini = 0

    def signalConnections(self):
        QtCore.QObject.connect(self.ui.btnBlink,QtCore.SIGNAL("pressed()"),self.btnBlink_on_press)

        QtCore.QObject.connect(self.ui.tabWidget,QtCore.SIGNAL("currentChanged(int)"),self.tabWidget_currentChanged)
        QtCore.QObject.connect(self.ui.btnSendCfg,QtCore.SIGNAL("clicked()"),self.btnSendCfg_on_click)
        QtCore.QObject.connect(self.ui.btnSaveCfg,QtCore.SIGNAL("clicked()"),self.btnSaveCfg_on_click)

        QtCore.QObject.connect(self.refreshTimer,QtCore.SIGNAL("timeout()"),self.updateTestStatus)
        QtCore.QObject.connect(self.ui.btnEnable,QtCore.SIGNAL("clicked(bool)"),self.endisDriver)
        QtCore.QObject.connect(self.ui.txtSpeed,QtCore.SIGNAL("editingFinished()"),self.setMotionValues)
        QtCore.QObject.connect(self.ui.txtAcceleration,QtCore.SIGNAL("editingFinished()"),self.setMotionValues)
        QtCore.QObject.connect(self.ui.btnGO,QtCore.SIGNAL("clicked()"),self.btnGO_on_click)
        QtCore.QObject.connect(self.ui.btnGORelativePos,QtCore.SIGNAL("clicked()"),self.btnGORelativePos_on_click)
        QtCore.QObject.connect(self.ui.btnGORelativeNeg,QtCore.SIGNAL("clicked()"),self.btnGORelativeNeg_on_click)
        QtCore.QObject.connect(self.ui.btnStopMotor,QtCore.SIGNAL("clicked()"),self.btnStopMotor_on_click)

        QtCore.QObject.connect(self.ui.btnSetPos,QtCore.SIGNAL("clicked()"),self._set_position)
        QtCore.QObject.connect(self.ui.btnSetEnc,QtCore.SIGNAL("clicked()"),self._set_encoder)


        #QtCore.QObject.connect(self.ui.btnHistoric,QtCore.SIGNAL("clicked()"),self.Historic_on_click)
        #QtCore.QObject.connect(self.ui.btnTemplates,QtCore.SIGNAL("clicked()"),self.btnTemplates_on_click)

        QtCore.QObject.connect(self.ui.btnUndo,QtCore.SIGNAL("clicked()"),self.btnUndo_on_click)
        QtCore.QObject.connect(self.ui.btnRestore,QtCore.SIGNAL("clicked()"),self.btnRestore_on_click)

        #QtCore.QObject.connect(self.ui.chbSyncIn, QtCore.SIGNAL("stateChanged(int)"), self.chbSyncInChanged)
        #QtCore.QObject.connect(self.ui.chbSyncOut, QtCore.SIGNAL("stateChanged(int)"), self.chbSyncOutChanged)

        #QtCore.QObject.connect(self.ui.listPredefined, QtCore.SIGNAL("currentTextChanged (const QString&)"), self.loadPredefinedSignalCfg)
        #QtCore.QObject.connect(self.ui.btnClear,QtCore.SIGNAL("clicked()"),self.resetSignalsTab)

        QtCore.QObject.connect(self.ui.sliderJog,QtCore.SIGNAL("sliderMoved(int)"),self.startJogging)
        QtCore.QObject.connect(self.ui.sliderJog,QtCore.SIGNAL("valueChanged(int)"),self.sliderChanged)
        QtCore.QObject.connect(self.ui.sliderJog,QtCore.SIGNAL("sliderReleased()"),self.stopJogging)
        QtCore.QObject.connect(self.ui.sliderJog,QtCore.SIGNAL("valueChanged(int)"),self.sliderChanged)

        QtCore.QObject.connect(self.sliderTimer,QtCore.SIGNAL("timeout()"),self.resetSlider)

        QtCore.QObject.connect(self.ui.cmdCSWITCH,QtCore.SIGNAL("currentIndexChanged(QString)"),self.changeSwitchesSetup)

        self.ui.btnCurves.clicked.connect(self.addDialogCurves)
        self.ui.btnStatus.clicked.connect(self.addDialogStatus)
        self.ui.cbHomeSrch1.currentIndexChanged.connect(self.cbHomeSrch1Changed)
        self.ui.cbHomeSrch2.currentIndexChanged.connect(self.cbHomeSrch2Changed)
        self.ui.btnHomeSrchGo.clicked.connect(self.doHomeSrch)
        self.ui.btnHomeStat.clicked.connect(self.doHomeStat)
        self.ui.chkEctsTurn.stateChanged.connect(self.enableEctsPerTurnCalculation)

    def highlightWidget(self, widget):
        # AGAIN, COMMAND WIDGETS ARE ONLY CHECKED IN THE QCOMBOBOX ELIF SECTION
        if not isinstance(widget,QtGui.QWidget):
            print "THIS WIDGET SHOULD NOT BE INTENDED TO HIGHLIGHT... NOT A QWIDGET",widget.objectName()
            return

        if widget.defaultvalue is None:
            widget_name = widget.objectName()
            if widget_name.startsWith("txt"):
                # PASS IT IS NORMAL TO NOT HIGHLIGHT IT, JUST INFO
                # txtNCURR, txtPCLOOP
                pass
            elif widget_name.count("_") > 0:
                # IT IS A FLAG OF A FLAGS PARAMETER, SO IT'S PARENT SHOULD BE HIGHLIGHTED
                self.highlightWidget(widget.parent())
            else:
                #print "THIS WIDGET SHOULD NOT BE INTENDED TO HIGHLIGHT... NO DEFAULT VALUE",widget_name
                pass
            return

        highlight = False
        sendConfig = False
        saveConfig = False

        param = widget.param
        if param == "DriverName":
            param = "IPAPNAME"

        dbvalue = self.dbStartupConfig.getParameter(unicode(param),in_memory=False)
        if dbvalue is None:
            dbvalue = ""
            # SPECIAL CASE IS THE FLAGS PARAMETER WHICH IS STORED
        wvalue = self._getWidgetValue(widget)
        defvalue = widget.defaultvalue
        if defvalue is None:
            defvalue = ""


        #if param == 'CATENTRY':
        #    print "WIDGET:%s PARAM:%s DB(%s) DEFAULT(%s) WIDGET(%s)" % (widget.objectName(),param,str(dbvalue),str(defvalue),str(wvalue))

        try:
            if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
                if widget.defaultvalue != wvalue:
                    highlight = True
                    sendConfig = True
                    widget.setPalette(self.base_yellow_palette)
                elif abs(float(wvalue) - float(dbvalue)) > 0.01:
                    saveConfig = True
                    widget.setPalette(self.base_salmon_palette)
                else:
                    widget.setPalette(self.base_white_palette)

            elif isinstance(widget, QtGui.QCheckBox):
                if widget.defaultvalue != wvalue:
                    highlight = True
                    sendConfig = True
                    widget.setPalette(self.base_yellow_palette)
                elif wvalue != dbvalue:
                    saveConfig = True
                    widget.setPalette(self.base_salmon_palette)
                else:
                    widget.setPalette(self.base_white_palette)

            elif isinstance(widget, QtGui.QComboBox):
                try:
                    #dbvalue = dbvalue.upper()
                    #wvalue = wvalue.upper()
                    #defvalue = defvalue.upper()
                    dbvalue = dbvalue
                    wvalue = wvalue
                    defvalue = defvalue
                    if widget.defaultvalue == None:
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
                except Exception,e:
                    print "some exception found trying to highlight a QComboBox!",e
                    print "widget was %s" % widget.objectName()

            elif isinstance(widget, QtGui.QLineEdit):
                if dbvalue == None:
                    dbvalue = ""
                #dbvalue = dbvalue.upper()
                #wvalue = wvalue.upper()
                #defvalue = defvalue.upper()
                dbvalue = dbvalue
                wvalue = wvalue
                defvalue = defvalue
                if defvalue == None:
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

            elif isinstance(widget, QtGui.QFrame):
                regexp = QtCore.QRegExp('^'+widget.objectName()+"_")
                for w in self.ui.tabWidget.findChildren(QtGui.QWidget,regexp):
                    w_param_str = str(w.objectName())
                    #w_param = w_param_str.split("_")[1]
                    w_param = "_".join(w_param_str.split("_")[1:])
                    defvalue_count = defvalue.count(w_param)
                    dbvalue_count = dbvalue.count(w_param)
                    if (w.isChecked() and (defvalue_count == 0)) or (not w.isChecked() and defvalue_count > 0):
                        highlight = True
                        sendConfig = True
                        w.setPalette(self.base_yellow_palette)
                    elif (w.isChecked() and (dbvalue_count == 0)) or (not w.isChecked() and dbvalue_count > 0):
                        saveConfig = True
                        w.setPalette(self.base_salmon_palette)
                    else:
                        w.setPalette(self.base_white_palette)


        except Exception,e:
            print "Some exception found with param",param,":",e

        if highlight:
            if not widget in self.widgets_modified:
                self.widgets_modified.append(widget)
        else:
            if widget in self.widgets_modified:
                self.widgets_modified.remove(widget)

        driver_key = self.icepap_driver.icepapsystem_name+"_"+str(self.icepap_driver.addr)
        if saveConfig and driver_key not in self.saveConfigPending:
            self.saveConfigPending.append(driver_key)

        tab_index = widget.tab_index
        index_in_tabs_modified = self.tabs_modified.has_key(tab_index)
        index_in_tabs_configPending = self.tabs_configPending.has_key(tab_index)
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
        #enable_send_and_save = (len(self.widgets_modified) > 0) or (driver_key in self.saveConfigPending)
        #self.ui.btnSendCfg.setEnabled(enable_send_and_save)
        #self.ui.btnSaveCfg.setEnabled(enable_send_and_save)
        #self._mainwin.ui.actionSaveConfig.setEnabled(enable_send_and_save)
        # Change behaviour in version 1.23
        enable_send = len(self.widgets_modified) > 0
        enable_save = driver_key in self.saveConfigPending and not sendConfig
        self.ui.btnSendCfg.setEnabled(enable_send)
        self.ui.btnSaveCfg.setEnabled(enable_save)
        self._mainwin.ui.actionSaveConfig.setEnabled(enable_save)


    def _connectHighlighting(self):
        #clear previous state
###        self.main_modified = []
###        self.test_var_modified = []
        QtCore.QObject.connect(self.signalMapper, QtCore.SIGNAL("mapped(QWidget*)"), self.highlightWidget)

###        ### # HIGHLIGHT AGAIN
###        for name, [nsection, widget] in self.var_dict.items():
###            self.highlightWidget(widget)
###
###        ### # HIGHLIGHT UNKNOWN TAB
###        for param in self.unknown_var_dict.keys():
###            widget_type,widget = self.unknown_var_dict[param]
###            self.highlightWidget(widget)
###
###        ### highlight the txtDriverName widget
###        self.highlightWidget(self.ui.txtDriverName)
###        self.setDescription(self.icepap_driver)




    def _disconnectHighlighting(self):
###        for nsection, widget in self.var_dict.itervalues():
###            if nsection == 0:
###                self._setNoHighlightingPalette(widget)
###        aux = []
###        for widget in self.test_var_dict.itervalues():
###            if type(widget) == type(aux):
###                for w in widget:
###                    self._setNoHighlightingPalette(w)
###            else:
###                self._setNoHighlightingPalette(widget)
###
###        for param in self.unknown_var_dict.keys():
###            widget_type,widget = self.unknown_var_dict[param]
###            self._setNoHighlightingPalette(widget)
###
        QtCore.QObject.disconnect(self.signalMapper, QtCore.SIGNAL("mapped(QWidget*)"),self.highlightWidget)


###    def _setNoHighlightingPalette(self,widget):
###        if isinstance(widget,QtGui.QComboBox):
###            widget.setPalette(self.button_grey_palette)
###        else:
###            widget.setPalette(self.base_white_palette)


    def _setWidgetToolTips(self):
        """ Reads the driverparameters file and sets the tooltips"""

        UI_PARS = self.param_to_widgets.keys()
        FOUND_PARS = []
        NOT_FOUND_PARS = []
        MISSING_TOOLTIPS = []

        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        driverparameters = path+'/../share/icepapcms/templates/driverparameters.xml'

        doc = minidom.parse(driverparameters)
        root  = doc.documentElement
        for section in root.getElementsByTagName("section"):
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    parid =  pars.attributes.get('id').value
                    parid = parid.strip()
                    parname =  pars.attributes.get('name').value
                    parname = parname.strip()
                    pardesc = self._getText(pars.getElementsByTagName("description")[0].firstChild)

                    # SHOULD I USE pardesc as the tooltip?
                    try:
                        if self.param_to_widgets.has_key(parid):
                            widgets = self.param_to_widgets[parid]
                            for w in widgets:
                                w.setToolTip(pardesc)
                            FOUND_PARS.append(parid)
                        else:
                            NOT_FOUND_PARS.append(parid)
                    except Exception,e:
                        print 'Exception was',e
                else:
                    print 'what is happening?'

        DEBUG_MISSING_TOOLTIPS = False

        if DEBUG_MISSING_TOOLTIPS:
            for p in UI_PARS:
                if p not in FOUND_PARS and p not in NOT_FOUND_PARS:
                    MISSING_TOOLTIPS.append(p)
            print '\n\nfound:',FOUND_PARS
            print '\n\nnot found:',NOT_FOUND_PARS
            print '\n\nmissing:',MISSING_TOOLTIPS




    def createTableWidget(self, column_names):
        widget = QtGui.QWidget()
        table_widget = QtGui.QTableWidget(widget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(218,224,234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.AlternateBase,brush)
        brush = QtGui.QBrush(QtGui.QColor(218,224,234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.AlternateBase,brush)
        brush = QtGui.QBrush(QtGui.QColor(218,224,234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.AlternateBase,brush)
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor(Qt.Qt.black))
        table_widget.setPalette(palette)
        table_widget.setAlternatingRowColors(True)
        table_widget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        table_widget.setGridStyle(QtCore.Qt.SolidLine)
        table_widget.horizontalHeader().setStretchLastSection(True)

        columns = len(column_names)
        table_widget.clear()
        table_widget.setColumnCount(columns)
        table_widget.setRowCount(0)

        for i in range(columns):
            item = QtGui.QTableWidgetItem()
            item.setText(column_names[i])
            table_widget.setHorizontalHeaderItem(i,item)

        vboxlayout = QtGui.QVBoxLayout(widget)
        vboxlayout.setMargin(9)
        vboxlayout.setSpacing(6)
        vboxlayout.addWidget(table_widget)
        widget.setLayout(vboxlayout)

        return (widget, table_widget)


    def _addItemToTable(self, section, row, column, text, editable):
###        item = QtGui.QTableWidgetItem()
###        item.setText(text)
###        if not editable:
###            item.setFlags(Qt.Qt.ItemIsSelectable)
###        else:
###            item.setTextColor(QtGui.QColor(Qt.Qt.red))
###        table = self.sectionTables[section]
###
###        table.setItem(row, column, item)
        pass

    def _addWidgetToTable(self, section, row, column, widget_type, min, max,unknownTab=False):
###        table = self.sectionTables[section]
###        #le = QtGui.QLineEdit(table)
###        widget = QtGui.QLineEdit()
###        if widget_type == "INTEGER":
###            widget = QValidateLineEdit(table,QValidateLineEdit.INTEGER,min,max)
###        elif widget_type == "DOUBLE":
###            widget = QValidateLineEdit(table,QValidateLineEdit.DOUBLE,min,max)
###        elif widget_type == "QCOMBOSTRING":
###            options = table.item(row,3).text()
###            options = options.replace("[","")
###            options = options.replace("]","")
###            options = options.replace("'","")
###            options = options.replace(" ","")
###            options_list = options.split(",")
###            widget = QtGui.QComboBox(table)
###            widget.insertItems(0,options_list)
###            # SET THE DESCRIPTION TO "LIST value"
###            table.item(row,3).setText("LIST value")
###
###
###        widget.defaultvalue = None
###        widget.isTest = False
###
###        table.setCellWidget(row, column, widget)
###        self._connectWidgetToSignalMap(widget)
###
###        if unknownTab:
###            parname = str(table.item(row,0).text())
###            widget.setObjectName(parname)
###            widget_value = str(table.item(row,1).text())
###            widget.defaultvalue = widget_value
###            if widget_type == "QCOMBOSTRING":
###                widget.setCurrentIndex(widget.findText(widget_value))
###            else:
###                widget.setText(widget_value)
###
###            self.unknown_var_dict[parname] = (widget_type,widget)
        pass


    def setDescription(self):
        driver = self.icepap_driver
        signature = self.icepap_driver.current_cfg.signature
        desc_cfg_system = self.icepap_driver.icepapsystem_name
        desc_cfg_crate = self.icepap_driver.cratenr
        desc_cfg_addr = self.icepap_driver.addr
        desc_cfg_name = self.icepap_driver.name
        desc_cfg_version = self.icepap_driver.current_cfg.getParameter('VER',True)
        cfg_db = ConfigManager().config["database"]["database"]
        desc_cfg_hwversion = IcepapController().read_icepap_pcb_version(desc_cfg_system, desc_cfg_addr)
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
                    desc_cfg_date = datetime.datetime.fromtimestamp(int(hex_epoch,16)).ctime()
                    # AS OF VERSION 1.20, SIGNATURE HAS NOT HEX TIMESTAMP BUT A MORE READABLE ONE
                except:
                    desc_cfg_date = datetime.datetime.strptime(aux[1]+'_'+aux[2],'%Y/%m/%d_%H:%M:%S').ctime()

            except Exception,e:
                msg = 'Not standard signature of driver '+str(desc_cfg_addr)+'.\nIt does not match (user@host_DATE).\nValue is:'+str(signature)
                MessageDialogs.showWarningMessage(self, "Not standard signature", msg)
        else:
            signature = None

        self.ui.dscDriverName.setText(driver.name)
        self.ui.dscActive.setText(driver.current_cfg.getParameter(unicode('ACTIVE')))
        if signature is None:
            self.ui.dscSignature.setText('NO_CONFIG')
        else:
            self.ui.dscSignature.setText(desc_cfg_date)
            html_signature = '<HTML><BODY>'
            html_signature += '<H2>More info:</H2>\n'
            html_signature += '<TABLE>\n'
            html_signature += '<TR><H2>%s/%s/%s</H2></TR>\n' % (desc_cfg_system,desc_cfg_crate,desc_cfg_addr)
            html_signature += '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % ('Axis name',desc_cfg_name)
            html_signature += '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % ('Firmware version',desc_cfg_version)
            html_signature += '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % ('Hardware version',desc_cfg_hwversion)
            html_signature += '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % ('Database host',desc_cfg_dbhost)
            html_signature += '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % ('Last saved config',desc_cfg_date)
            html_signature += '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % ('User',desc_cfg_user)
            html_signature += '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % ('Host',desc_cfg_host)
            html_signature += '<TR><TD> </TD><TD><B>%s</B></TD><TD>%s</TD></TR>\n' % ('Raw',signature)
            html_signature +='</TABLE></BODY></HTML>\n'
            self.ui.dscSignature.setToolTip(html_signature)


        if self.ui.dscActive.text() == 'YES':
            self.ui.frame_description.setPalette(self.qframe_lightblue_palette)
        else:
            self.ui.frame_description.setPalette(self.qframe_salmon_palette)

    def fillData(self, icepap_driver):
        """ TO-DO STORM review"""
        QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
#        #self.ui.tabWidget.setCurrentIndex(0)
        self.icepap_driver = icepap_driver
        self._disconnectHighlighting()

        self.widgets_modified = []
        self.tabs_modified = {}
        self.tabs_configPending = {}

        driver_key = self.icepap_driver.icepapsystem_name+"_"+str(self.icepap_driver.addr)
        if driver_key in self.saveConfigPending:
            self.saveConfigPending.remove(driver_key)
#        #self.resetSignalsTab()
        dbIcepapSystem = StormManager().getIcepapSystem(self.icepap_driver.icepapsystem_name)
        self.dbStartupConfig = dbIcepapSystem.getDriver(self.icepap_driver.addr,in_memory=False).startup_cfg
        self.icepap_driver.startup_cfg = self.dbStartupConfig

###
###        # THIS IS OVERWRITTEN LATER
###        driver_name = self._manager.readIcepapParameters(icepap_driver.icepapsystem_name,icepap_driver.addr,["NAME"])[0][1]
###        icepap_driver.setName(driver_name)
###        self.ui.txtDriverName.setText(self.icepap_driver.name)
###        self.ui.txtDriverName.defaultvalue = self.icepap_driver.name
###        #self.ui.txtDriverNemonic.setText(self.icepap_driver.nemonic)
###
###
###        # BEFORE STARTING WITH PARAMETERS, IN CASE THE UNKNOWN TAB EXIST, IT SHOULD BE CLEARED
###        unknown = "Unknown"
###        tab_unknown = "tab_"+unknown
###        for i in range(self.ui.tabWidget.count()):
###            widget = self.ui.tabWidget.widget(i)
###            if str(widget.objectName()) == tab_unknown:
###                self.sectionTables[i].setRowCount(0)
###                break
###
###
        unknownParams = False
        self.unknown_table_widget.clear()
        self.unknown_table_widget.setRowCount(0)

        ## WE ADD THE UNKNOWN TAB SO THE WIDGETS HAVE A CORRECT widget.tab_index VALUE
        #unknown_index = self.ui.tabWidget.indexOf(self.unknown_tab)
        #if unknown_index == -1:
        #    unknown_index = self.ui.tabWidget.count()
        #self.ui.tabWidget.insertTab(unknown_index, self.unknown_tab, "Unknown")

        for name, value in icepap_driver.current_cfg.toList():
            if self.param_to_widgets.has_key(name):
                #print "SUCCESS!",name,'->',self.param_to_widgets.get(name)
                widgets = self.param_to_widgets.get(name)
                self._setWidgetsValue(widgets,value)
            elif name in ['IPAPNAME','VER','ID']:
                # THESE PARAMS DO NOT COME FROM THE FIRMWARE
                # HARDCODED DRIVER NAME
                if name == 'IPAPNAME':
                    self._setWidgetsValue(self.param_to_widgets.get('DriverName'), value)
                    self.icepap_driver.setName(value)
                    # WE SHOULD GET THE TREE NODE AND UPDATE IT'S LABEL
                    ## WE SHOULD ALSO SET THE DRIVER NAME
                    modelindex = self._mainwin.ui.treeView.currentIndex()
                    drivernode = self._mainwin._tree_model.item(modelindex)
                    label = str(self.icepap_driver.addr)+" "+self.icepap_driver.name
                    if drivernode is not None:
                        drivernode.changeLabel([label])
            else:
                unknownParams = True
                self.addUnknownWidget(name, value)


        unknown_index = self.ui.tabWidget.indexOf(self.unknown_tab)

        if unknownParams:
            if unknown_index == -1:
                unknown_index = self.ui.tabWidget.count()
                self.ui.tabWidget.insertTab(unknown_index, self.unknown_tab, "Unknown")
        elif unknown_index != -1:
            self.ui.tabWidget.removeTab(unknown_index)

        self.highlightTabs()




###            if self.var_dict.has_key(name):
###                [nsection, element] = self.var_dict[name]
###                if nsection == 0:
###                    # In main tab
###                    self._setWidgetValue(element, value)
###                else:
###                    self._addItemToTable(nsection, element, 1, value, False)
###                    self.sectionTables[nsection].cellWidget(element,2).setText("")
###                #self._addItemToTable(nsection, row, 2, "", True)
###            else:
###                cfginfo = IcepapController().icepap_cfginfos[self.icepap_driver.icepapsystem_name][self.icepap_driver.addr].get(name)
###                if cfginfo != None:
###                    indexUnknownTab = -1
###                    for i in range(self.ui.tabWidget.count()):
###                        widget = self.ui.tabWidget.widget(i)
###                        if str(widget.objectName()) == tab_unknown:
###                            indexUnknownTab = i
###                            break
###
###                    if indexUnknownTab == -1:
###                        indexUnknownTab = self._addSectionTab(unknown)
###
###                    unknown_table_widget = self.sectionTables[indexUnknownTab]
###
###                    row = unknown_table_widget.rowCount()
###                    unknown_table_widget.insertRow(row)
###                    self._addItemToTable(indexUnknownTab, row, 0, name, False)
###                    self._addItemToTable(indexUnknownTab, row, 1, value, False)
###                    partype = "STRING"
###                    pardesc = str(cfginfo)
###                    if len(cfginfo) > 0:
###                        if "INTEGER" == cfginfo[0]:
###                            partype = "INTEGER"
###                            pardesc = "INTEGER value"
###                        elif "FLOAT" == cfginfo[0]:
###                            partype = "DOUBLE"
###                            pardesc = "DOUBLE value"
###                        else:
###                            partype = "QCOMBOSTRING"
###                    self._addItemToTable(indexUnknownTab, row, 3, pardesc, False)
###                    # DESCRIPTION (col 3) BEFORE WIDGET (col 2) TO BE ABLE TO CREATE QCOMBOXES
###                    # THE DESCRIPTION IS USED TO PARSE THE VALUES
###                    self._addWidgetToTable(indexUnknownTab, row, 2, partype, 0, 9999999,unknownTab=True)
###
###
###        # get testing values
        self.startTesting()
###        if not (self.status == -1 or self.status == 1):
###            result = self._manager.readIcepapParameters(self.icepap_driver.icepapsystem_name,self.icepap_driver.addr, self.test_var_dict.keys())
###            for [name, value] in result:
###                if self.test_var_dict.has_key(name):
###                    widget = self.test_var_dict[name]
###                    try:
###                        if type(widget) == type(result):
###                            value = value.split()
###                            i = 0
###                            for w in widget:
###                                self._setWidgetValue(w, value[i])
###                                i = i +1
###                        else:
###                            self._setWidgetValue(widget, value)
###                    except:
###                        pass
###                else:
###                    print "FOUND THE UNKNOWN PARAMETER '"+str(name)+"'"
###
###        # SET THE CORRECT DRIVER NAME
###
###        self.icepap_driver.name = unicode(self.ui.txtDriverName.text())
###        #self.icepap_driver.current_cfg.setParameter(unicode("IPAPNAME"),self.icepap_driver.getName())
###
###
###        # CHECK THE ACTIVE FLAG
###        # IN CASE OF NO-ACTIVE DRIVER,
###        # UNCHECK THE ACTIVE CFG PARAMETER
###        activeStatus = IcepapController().getDriverActiveStatus(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
###        # WHY SOMETIMES THE ANSWER OF THE DRIVER IS '???'?
###        if activeStatus.upper() == "NO":
###            print "CAREFUL, THE activeStatus OF THE DRIVER IS 'NO'"
###            self.param_to_widgets.get("ACTIVE")[0].setChecked(False)

        if self.ui.historicWidget.isVisible():
            self.ui.historicWidget.fillData(self.icepap_driver)

        self.ui.tabWidget.setCurrentIndex(self.lastTabSelected)
        self.setDescription()
        self._connectHighlighting()

        # ALWAYS PUT THE DRIVER IN CONFIG MODE
        # It may happen that the driver is in PROG MODE

        # NOT VALID ANY MORE (SINCE VERSION 1.23 ONLY IN CONFIG IF NECESSARY
        #mode = self._manager.startConfiguringDriver(self.icepap_driver)
        mode = self.icepap_driver.mode
        if mode != IcepapMode.PROG:
            self.ui.tabWidget.setEnabled(True)
        else:
            # MAY BE ALSO GOOD FOR THE SHUTTER MODE
            MessageDialogs.showErrorMessage(None,'Start configuring driver','It is not possible to configure the driver\nwhile it is in mode PROG.')
            self.ui.tabWidget.setEnabled(False)
        QtGui.QApplication.instance().restoreOverrideCursor()



    def addUnknownWidget(self, param_name, param_value):
        cfginfo = IcepapController().icepap_cfginfos[self.icepap_driver.icepapsystem_name][self.icepap_driver.addr].get(param_name)
        cfginfo = cfginfo.split()

        if cfginfo != None:
            row = self.unknown_table_widget.rowCount()
            self.unknown_table_widget.insertRow(row)

            #self._addItemToTable(indexUnknownTab, row, 0, name, False)
            #self._addItemToTable(indexUnknownTab, row, 1, value, False)
            param_desc = ""
            widget = None
            if len(cfginfo) > 0:
                if "INTEGER" == cfginfo[0]:
                    #param_desc = "INTEGER value"
                    widget = QtGui.QSpinBox()
                    widget.setMaximum(999999999)
                    widget.setMinimum(-999999999)
                elif "FLOAT" == cfginfo[0]:
                    #param_desc = "DOUBLE value"
                    widget = QtGui.QDoubleSpinBox()
                    widget.setMaximum(999999999)
                    widget.setMinimum(-999999999)
                elif cfginfo[0].startswith("["):
                    #param_desc = "FLAGS value"
                    param_tooltip = "FLAGS:"
                    for flag in cfginfo:
                        # MORE EFFORT THAN NEEDED BUT...
                        flag.replace("[","")
                        flag.replace("]","")
                        param_tooltip += " "+flag
                    widget = QtGui.QLineEdit()
                    widget.setToolTip(param_tooltip)
                elif cfginfo[0].startswith("STRING"):
                    widget = QtGui.QLineEdit()
                    param_tooltip = str(cfginfo)
                    widget.setToolTip(param_tooltip)
                else:
                    #param_desc = "OPTIONS value"
                    widget = QtGui.QComboBox()
                    param_tooltip = str(cfginfo)
                    widget.setToolTip(param_tooltip)


            #widget = self.createUnknownParamWidget(param_type, cfginfo)


            if widget != None:
                widget.param = param_name
                widget.isCommand = False
                widget.tab_index = self.ui.tabWidget.indexOf(self.unknown_tab)
                param_item = QtGui.QTableWidgetItem()
                param_item.setText(param_name)
                param_item.setFlags(Qt.Qt.ItemIsSelectable)
                self.unknown_table_widget.setItem(row, 0, param_item)
                value_item = QtGui.QTableWidgetItem()
                value_item.setText(str(param_value))
                value_item.setFlags(Qt.Qt.ItemIsSelectable)
                self.unknown_table_widget.setItem(row, 1, value_item)

                self.unknown_table_widget.setCellWidget(row, 2, widget)

                self.param_to_unknown_widgets[param_name] = widget

                self._setWidgetsValue([widget],param_value)

                self._connectWidgetToSignalMap(widget)





        #self._connectWidgetToSignalMap(widget)


        ###table = self.sectionTables[section]
        ####le = QtGui.QLineEdit(table)
        ###widget = QtGui.QLineEdit()
        ###if widget_type == "INTEGER":
        ###    widget = QValidateLineEdit(table,QValidateLineEdit.INTEGER,min,max)
        ###elif widget_type == "DOUBLE":
        ###    widget = QValidateLineEdit(table,QValidateLineEdit.DOUBLE,min,max)
        ###elif widget_type == "QCOMBOSTRING":
        ###    options = table.item(row,3).text()
        ###    options = options.replace("[","")
        ###    options = options.replace("]","")
        ###    options = options.replace("'","")
        ###    options = options.replace(" ","")
        ###    options_list = options.split(",")
        ###    widget = QtGui.QComboBox(table)
        ###    widget.insertItems(0,options_list)
        ###    # SET THE DESCRIPTION TO "LIST value"
        ###    table.item(row,3).setText("LIST value")
        ###
        ###
        ###
        ###if unknownTab:
        ###    parname = str(table.item(row,0).text())
        ###    widget.setObjectName(parname)
        ###    widget_value = str(table.item(row,1).text())
        ###    widget.defaultvalue = widget_value
        ###    if widget_type == "QCOMBOSTRING":
        ###        widget.setCurrentIndex(widget.findText(widget_value))
        ###    else:
        ###        widget.setText(widget_value)
        ###
        ###    self.unknown_var_dict[parname] = (widget_type,widget)






    def checkSaveConfigPending(self):
        # THIS METHOD IS CALLED WHEN THE USER WANTED TO
        if self.icepap_driver is not None:
            driver_key = self.icepap_driver.icepapsystem_name+"_"+str(self.icepap_driver.addr)
            if driver_key in self.saveConfigPending:
                # IT SHOULD STILL BE EN CONFIG MODE BECAUSE SOME VALUES MISMATCH FROM DATABASE
                return True
            else:
                self._manager.endConfiguringDriver(self.icepap_driver)
                return False

    def _connectWidgetToSignalMap(self, widget):
        self.signalMapper.setMapping(widget, widget)
        if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("valueChanged (const QString&)"), self.signalMapper, QtCore.SLOT("map()"))
        elif isinstance(widget, QtGui.QCheckBox):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("stateChanged(int)"), self.signalMapper, QtCore.SLOT("map()"))
        elif isinstance(widget, QtGui.QComboBox):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.signalMapper, QtCore.SLOT("map()"))
        elif isinstance(widget, QtGui.QLineEdit):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("textChanged(const QString&)"), self.signalMapper, QtCore.SLOT("map()"))

    def _setWidgetsValue(self, widgets, value, set_default = True):
        ### THE CMD WIDGETS RIGHT NOW ARE ONLY QCOMBOBOXES SO THE SPECIAL CODE IS JUST IN THAT ELIF SECTION
        for widget in widgets:
            try:
                system_name = self.icepap_driver.icepapsystem_name
                driver_addr = self.icepap_driver.addr
                if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
                    widget.setValue(float(value))
                    if set_default:
                        widget.defaultvalue = widget.value()
                elif isinstance(widget, QtGui.QCheckBox):
                    state = (value == "1" or value == "YES")
                    widget.setChecked(state)
                    if set_default:
                        widget.defaultvalue = value
                elif isinstance(widget, QtGui.QComboBox):
                    widget.clear()
                    param = widget.param
                    controller = IcepapController()
                    driver_cfginfo = controller.icepap_cfginfos[system_name][driver_addr]
                    options = driver_cfginfo.get(param).split()
                    if options != None:
                        for option in options:
                            widget.addItem(QtCore.QString(option))
                        # 20130412 IT SEEMS THAT INDEXER COMMAND SHOULD HAVE ALSO LINKED
                        #          AS AN OPTION, BUT IT IS NOT PROVIDED BY CFGINFO...
                        #          I WILL ADD IT MANUALLY BUT IT MAY BE REMOVED LATER
                        # 20140219 IT SEEMS _NOW_ THAT IS NOT NEEDED ANY MORE
                        #widget.addItem('LINKED')

                    # SPECIAL CASE TO THE TEST WIDGETS
                    if widget.isCommand:
                        is_active = controller.is_driver_active(system_name, driver_addr)
                        widget.setEnabled(is_active)
                        if is_active:
                            # SHOULD RETRIEVE THE VALUE FROM THE DRIVER'S COMMAND
                            if param == 'AUXPS':
                                ## THIS VALUE DOES NOT COME IN THE CONFIGURATION
                                pass
                            elif param == 'CSWITCH':
                                ## THIS VALUE DOES NOT COME NEITHER IN THE CONFIGUARTION
                                print 'eo....cswitch'
                                pass
                            elif param == 'INDEXER':
                                value = controller.read_icepap_indexer(system_name, driver_addr)
                                widget.addItem('LINKED')
                                widget.setEnabled(False)
                            elif param[:5] in ['INFOA', 'INFOB', 'INFOC']:
                                values = controller.read_icepap_infox(system_name, driver_addr, param)
                                if param.endswith('SRC'):
                                    value = values[0]
                                else:
                                    value = values[1]
                    widget.setCurrentIndex(widget.findText(str(value), QtCore.Qt.MatchFixedString))
                    if set_default:
                        widget.defaultvalue = str(value)
                elif isinstance(widget, QtGui.QLineEdit):
                    widget.setText(str(value))
                    if set_default:
                        widget.defaultvalue = str(value)
                elif isinstance(widget, QtGui.QLabel):
                    widget.setText(str(value))
                elif isinstance(widget, QtGui.QFrame):
                    # WE NOW HAVE TO ITERATE THROUGOUT ALL THE CHECKBOXES:
                    if set_default:
                        widget.defaultvalue = value
                    regexp = QtCore.QRegExp('^'+widget.objectName()+"_")
                    for w in self.ui.tabWidget.findChildren(QtGui.QWidget,regexp):
                        w_param = w.objectName().split("_")[1]
                        checked = False
                        if w_param in value:
                            checked = True
                        w.setChecked(checked)

                self.highlightWidget(widget)
            except Exception,e:
                print "_setWidgetValue():", sys.exc_info() , " " , value
                print "Some exception setting value",e



    def _getWidgetValue(self, widget):
        try:
            if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
                return widget.value()
            elif isinstance(widget, QtGui.QCheckBox):
                if widget.isChecked():
                    return "YES"
                else:
                    return "NO"
            elif isinstance(widget, QtGui.QComboBox):
                return str(widget.currentText())
            elif isinstance(widget, QtGui.QLineEdit):
                #return str(widget.text()).upper()
                return str(widget.text())
            elif isinstance(widget, QtGui.QFrame):
                regexp = QtCore.QRegExp('^'+widget.objectName()+"_")
                flags_value = []
                for w in self.ui.tabWidget.findChildren(QtGui.QWidget,regexp):
                    #w_param = w.objectName().split("_")[1]
                    w_param_str = str(w.objectName())
                    #w_param = w_param_str.split("_")[1]
                    w_param = "_".join(w_param_str.split("_")[1:])
                    if w.isChecked():
                        flags_value.append(w_param)
                return ' '.join(flags_value)
        except Exception,e:
            print "error in _getWidgetValue",e


    def addNewCfg(self, cfg):
        QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        for name, value in cfg.toList():
            if self.param_to_widgets.has_key(name):
                widgets = self.param_to_widgets.get(name)
                self._setWidgetsValue(widgets, value, set_default=False)
            elif name == 'IPAPNAME':
                self._setWidgetsValue(self.param_to_widgets.get('DriverName'), value, set_default=False)
        self.highlightTabs()
        QtGui.QApplication.instance().restoreOverrideCursor()


    def _getText(self, node):
        rc = ""
        if node != None:
                rc = str(node.data)
        return rc


    def tabWidget_currentChanged(self,index):
        self.lastTabSelected = index
        self.highlightTabs()

    def highlightTabs(self):
        tab_bar = self.ui.tabWidget.tabBar()
        for index in range(self.ui.tabWidget.count()):
            if self.tabs_modified.has_key(index):
                #tab_bar.setTabTextColor(index,QtGui.QColor(255,255,0))
                tab_bar.setTabIcon(index, QtGui.QIcon(":/icons/IcepapCfg Icons/ipapdrivermodified.png"))
            elif self.tabs_configPending.has_key(index):
                #tab_bar.setTabTextColor(index,QtGui.QColor(255,206,162))
                tab_bar.setTabIcon(index, QtGui.QIcon(":/icons/IcepapCfg Icons/ipapdrivercfg.png"))
            else:
                #tab_bar.setTabTextColor(index,QtGui.QColor(0,0,0))
                tab_bar.setTabIcon(index, QtGui.QIcon(""))


    def btnSendCfg_on_click(self, skip_fillData=False):
        if len(self.widgets_modified) == 0:
            return True
        self._mainwin.ui.actionHistoricCfg.setChecked(False)
        self.hideHistoricWidget()
        new_values = []
        new_command_values = []
        for widget in self.widgets_modified:
            # SPECIAL CASE TO THE DRIVER NAME THAT IS NOT A CONFIG PARAMETER BUT
            # IT IS TREATED AS SO, IT IS A COMMAND 'NAME' BUT IT IS STORED
            # IN THE DATABASE AS A CONFIGURATION PARAMETER
            param = widget.param
            value = self._getWidgetValue(widget)
            if not widget.isCommand:
                if param == 'DriverName':
                    param = 'IPAPNAME'
                new_values.append([param, value])
            else:
                # SINCE THE COMMAND PARAMS ARE NOT THE SAME AS THE CFG PARAMS
                # WE NEED A WORK-AROUND HERE AND FOR INFO COMMANDS ALWAYS PROVIDE SRC AND POL
                # IF BOTH SRC AND POL ARE MODIFIED, WE WILL SENT TWICE THE COMMAND PAIR
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
                    #THIS IS ANOTHER cmd that should be passed...
                    # AND BY DEFAULT DESIGN, param and value should be unique.
                    pass
                new_command_values.append([param, value])


###        # SHOULD NOT CHANGE THE DRIVER NAME
###        #self.icepap_driver.name = unicode(self.ui.txtDriverName.text())
###        #self.icepap_driver.nemonic = str(self.ui.txtDriverNemonic.text())
###        new_values = []
###        values_ok = True
###        save_ok = True
###        test_values_ok = True
###        # First get modified items in main section
###        for name, [nsection, widget] in self.var_dict.items():
###            if nsection == 0:
###                if widget in self.main_modified:
###                    value = self._getWidgetValue(widget)
###                    new_values.append([name, value])
###
###        for tableWidget in self.sectionTables.itervalues():
###            for row in range(tableWidget.rowCount()):
###                #val = tableWidget.item(row,2).text()
###                widget = tableWidget.cellWidget(row,2)
###                val = ""
###                if isinstance(widget,QValidateLineEdit):
###                   val = widget.text()
###                elif isinstance(widget,QtGui.QComboBox):
###                    val = str(widget.currentText()).upper()
###                if val != "":
###                    try:
###                        name = str(tableWidget.item(row,0).text())
###                        default_val = str(tableWidget.item(row,1).text())
###                        if isinstance(widget, QValidateLineEdit):
###                            if widget.type == QValidateLineEdit.INTEGER:
###                                val = int(widget.text())
###                                default_val = int(default_val)
###                            elif widget.type == QValidateLineEdit.DOUBLE:
###                                val = float(widget.text())
###                                default_val = float(default_val)
###
###                        if val != default_val:
###                            new_values.append([name, val])
###                    except Exception,e:
###                        print "Unexpected error:",e, sys.exc_info()[0]
###                        values_ok = False
###                        break
###

        if len(new_values) > 0:
            setExpertFlag = self._mainwin.ui.actionSetExpertFlag.isChecked()
            send_ok = self._manager.saveValuesInIcepap(self.icepap_driver, new_values, expertFlag = setExpertFlag)
            if not send_ok:
                MessageDialogs.showWarningMessage(self, "Driver configuration", "Wrong parameter format")
                return False

        if len(new_command_values) > 0:
            self._manager.writeIcepapParameters(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, new_command_values)

###
###        # save testing values
###        #print "with testing",self.status,"and the test_var_dict",self.test_var_dict.keys()

###        if not (self.status == -1 or self.status == 1):
###            test_values_list = []
###            for name, widget in self.test_var_dict.items():
###                try:
###                    if type(widget) == type(test_values_list):
###                        add = False
###                        value = ""
###                        for w in widget:
###                            if w in self.test_var_modified:
###                                add = True
###                            value = value + str(self._getWidgetValue(w)) + " "
###                        if add:
###                            test_values_list.append([name, value])
###                    else:
###                        if widget in self.test_var_modified:
###                            value = self._getWidgetValue(widget)
###                            test_values_list.append([name, value])
###                except Exception,e:
###                    print "Some exception getting test values",e
###                    test_values_ok = False
###                    break
###
###            self._manager.writeIcepapParameters(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, test_values_list)
###
        if not skip_fillData:
            self.fillData(self.icepap_driver)

        if self.icepap_driver.hasUndoList():
            self.ui.btnUndo.setEnabled(True)
        else:
            self.ui.btnUndo.setEnabled(False)
        return True


    def btnSaveCfg_on_click(self):
        save_ok = True
        if len(self.widgets_modified) > 0:
            save_ok = self.btnSendCfg_on_click(skip_fillData=True)
        if not save_ok:
            MessageDialogs.showWarningMessage(self, "Driver configuration", "Problems found saving the configuration")
            return
        self._mainwin.actionSaveConfig()

    def btnUndo_on_click(self):
        self._manager.undoDriverConfiguration(self.icepap_driver)
        self.fillData(self.icepap_driver)
        if not self.icepap_driver.hasUndoList():
            self.ui.btnUndo.setEnabled(False)

    def btnRestore_on_click(self):
        #self.addNewCfg(self.icepap_driver.current_cfg)
        self.fillData(self.icepap_driver)

    def doImport(self):
        try:
            folder = ConfigManager().config["icepap"]["configs_folder"]
            fn = QtGui.QFileDialog.getOpenFileName(self,"Open Config File",QtCore.QString(folder),QtCore.QString("*.xml"))
            if fn.isEmpty():
                return
            filename = str(fn)
            self.fillFileData(filename)
        except Exception,e:
            MessageDialogs.showWarningMessage(self, "File", "Error reading file\n")
            print "exception: "+str(e)

    def fillFileData(self, filename):
        QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self._disconnectHighlighting()
        doc = minidom.parse(filename)
        root  = doc.documentElement
        for param_element in doc.getElementsByTagName("par"):
            param_name =  param_element.attributes.get('name').value
            param_name = param_name.strip()
            param_value =  param_element.attributes.get('value').value
            param_value = param_value.strip()
            if self.param_to_widgets.has_key(param_name):
                widgets = self.param_to_widgets.get(param_name)
                self._setWidgetsValue(widgets, param_value, set_default=False)
            elif param_name == 'IPAPNAME':
                self._setWidgetsValue(self.param_to_widgets.get('DriverName'), param_value, set_default=False)
            elif param_name in ['ID','VER']:
                pass
            else:
                # SINCE UNKNOWN WIDGETS ARE CREATED EVERY TIME, ANOTHER DICT HAS TO BE AVAILABLE FOR THEM
                w = self.param_to_unknown_widgets.get(param_name)
                self._setWidgetsValue([w], param_value, set_default=False)

        self.highlightTabs()
        self._connectHighlighting()
        QtGui.QApplication.instance().restoreOverrideCursor()

    def doExport(self):
        folder = ConfigManager().config["icepap"]["configs_folder"]
        fn = QtGui.QFileDialog.getSaveFileName(self,"Save Config File",QtCore.QString(folder),QtCore.QString("*.xml"))
        if fn.isEmpty():
            return
        filename = str(fn)
        if filename.find('.xml') == -1:
            filename = filename + '.xml'
        self.exportToFile(filename)

    def exportToFile(self, filename):
        output = open(filename, "w")
        newdoc = self.getXmlData()
        output.writelines(newdoc.toprettyxml())

    def getXmlData(self):
        doc = getDOMImplementation().createDocument(None, "Driver", None)
        dbIcepapSystem = StormManager().getIcepapSystem(self.icepap_driver.icepapsystem_name)
        dbConfig = dbIcepapSystem.getDriver(self.icepap_driver.addr,in_memory=False).startup_cfg
        config_list = dbConfig.toList()
        config_list.sort()
        for param,value in config_list:
            param_element = doc.createElement("par")
            param_element.setAttribute("name", param)
            param_element.setAttribute("value", str(value))
            doc.documentElement.appendChild(param_element)
        return doc

    def signDriver(self):
        self._disconnectHighlighting()
        self.icepap_driver.signDriver()
        self.fillData(self.icepap_driver)

    def doCopy(self):
        self.temp_file = tempfile.TemporaryFile()
        data = self.getXmlData()
        self.temp_file.writelines(data.toprettyxml())
        self.temp_file.flush()
        self.temp_file.seek(0)

    def doPaste(self):
        if self.temp_file == None:
            return
        self.temp_file.seek(0)
        self.fillFileData(self.temp_file)

# ------------------------------  Testing ----------------------------------------------------------
    def startTesting(self):
        if not self.icepap_driver is None:
            self.inMotion = -1
            self.status = -1
            self.ready = -1
            self.mode = -1
            self.power = -1
            #self._manager.enableDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
            self.updateTestStatus()
            self.refreshTimer.start(1000)

    def stopTesting(self):
        try:
            self.refreshTimer.stop()
            #self._manager.disableDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
            self.setLedsOff()
        except:
            print "Unexpected error:", sys.exc_info()



    def getMotionValues(self):
        (speed, acc) = self._manager.getDriverMotionValues(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
        self.ui.txtSpeed.setText(str(speed))
        self.ui.txtAcceleration.setText(str(acc))


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
            self._manager.setDriverMotionValues(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, [float(speed), float(acc)])
        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")

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
        #self.ui.sbFactor.setValue(1)

    def disableAllControl(self):
        self.ui.txtSpeed.setEnabled(False)
        self.ui.txtAcceleration.setEnabled(False)
        self.ui.btnGO.setEnabled(False)
        self.ui.btnGORelativeNeg.setEnabled(False)
        self.ui.btnGORelativePos.setEnabled(False)
        self.ui.sliderJog.setEnabled(False)
        self.ui.btnEnable.setEnabled(False)
        self.ui.btnStopMotor.setEnabled(False)
        ## BTW, tab_3 has been renamed to tab_TuneAndTesting
        #self.ui.tab_3.setEnabled(False)

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


    def updateTestStatus(self):
        #pos_sel = str(self.ui.cb_pos_sel.currentText()).upper()
        #enc_sel = str(self.ui.cb_enc_sel.currentText()).upper()
        pos_sel = str(self.ui.cb_pos_sel.currentText())
        enc_sel = str(self.ui.cb_enc_sel.currentText())
        (status, power, position) = self._manager.getDriverTestStatus(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, pos_sel, enc_sel)

        step_now = position[0]
        enc_now = position[1]
        if self.ecpmt_just_enabled:
            self.step_ini = position[0]
            self.enc_ini = position[1]
            self.ecpmt_just_enabled = False
            print self.step_ini, self.enc_ini
        if self.ui.chkEctsTurn.isChecked():
            #print "upd"
            if (step_now - self.step_ini) != 0:
                enc_cts_per_motor_turn = (enc_now - self.enc_ini) * int(self.axis.cfgANSTEP.value()) / ((step_now - self.step_ini) * int(self.axis.cfgANTURN.value()))
            else:
                enc_cts_per_motor_turn = 0
            self.ui.txtEctsTurn.setText(str(enc_cts_per_motor_turn))

        #self.StepSize = self.ui.sbFactor.value()
        disabled = IcepapStatus.isDisabled(status)
        moving = IcepapStatus.isMoving(status)
        ready = IcepapStatus.isReady(status)
        mode = IcepapStatus.getMode(status)
        if self.inMotion <> moving:
            if moving == 1:
                self.refreshTimer.setInterval(700)
                self.ui.LedStep.on()
            elif moving == -1:
                self.refreshTimer.stop()
            else:
                self.refreshTimer.setInterval(1000)
                self.ui.LedStep.off()
        self.inMotion = moving

        if self.status <> disabled or self.mode <> mode or self.power <> power or self.ready <> ready:
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

        #position =  position / self.StepSize
        if IcepapStatus.inHome(status):
            self.ui.LedHome.on()
        else:
            self.ui.LedHome.off()

        lower = IcepapStatus.getLimitNegative(status)
        upper = IcepapStatus.getLimitPositive(status)
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

        # update Position and Encoder calcs
        self.calculatePositionAndEncoderUnits(position[0], position[1])

    def enableEctsPerTurnCalculation(self):
        self.ecpmt_just_enabled = True
        #print "ecpt " + str(self.ecpmt_just_enabled)

    def calculatePositionAndEncoderUnits(self, pos, enc):
        if self.ui.txtSpu.text() in ['', None]:
            self.ui.txtSpu.setText('1')
        if self.ui.txtEpu.text() in ['', None]:
            self.ui.txtEpu.setText('1')
        if self.ui.txtOffset.text() in ['', None]:
            self.ui.txtOffset.setText('0')
        self.ui.txtPosition.setText(str(float(self.ui.txtOffset.text()) + float(pos)/float(self.ui.txtSpu.text())))
        self.ui.txtEncoder.setText(str(float(self.ui.txtOffset.text()) + float(enc)/float(self.ui.txtEpu.text())))

    def addDialogCurves(self):
        d = DialogCurves(self, self.icepap_driver)
        d.show()

    def addDialogStatus(self):
        d = DialogStatusInfo(self, self.icepap_driver)
        d.show()

    def cbHomeSrch1Changed(self):
        self.ui.cbHomeSrch3.setDisabled(True)
        self.ui.cbHomeSrch4.setDisabled(True)
        self.ui.cbHomeSrch2.clear()
        if self.ui.cbHomeSrch1.currentText() == 'HOME':
            self.ui.cbHomeSrch2.addItems(['+1', '0', '-1'])
        else:
            self.ui.cbHomeSrch2.addItems(['Lim-', 'Lim+', 'Home', 'EncAux', 'InpAux'])

    def cbHomeSrch2Changed(self):
        if self.ui.cbHomeSrch1.currentText() == 'SRCH':
            #disable = self.ui.cbHomeSrch2.currentText() in ['Lim-', 'Lim+']
            disable = False
            self.ui.cbHomeSrch3.setDisabled(disable)
            self.ui.cbHomeSrch4.setDisabled(disable)
            if self.ui.cbHomeSrch2.currentText() == 'Lim-':
                self.ui.cbHomeSrch4.setCurrentIndex(1)
            elif self.ui.cbHomeSrch2.currentText() == 'Lim+':
                self.ui.cbHomeSrch4.setCurrentIndex(0)

    def doHomeSrch(self):
        axis = IcepapController().iPaps[self.icepap_driver.icepapsystem_name][self.icepap_driver.addr]
        txt1 = self.ui.cbHomeSrch1.currentText()
        txt2 = self.ui.cbHomeSrch2.currentText()
        cmd = '{} {}'.format(txt1, txt2)
        try:
            if txt1 == 'HOME':
                direction = int(txt2)
                axis.home(direction)
            else:
                if txt2 not in ['Lim-', 'Lim+']:
                    txt3 = self.ui.cbHomeSrch3.currentText()
                    txt4 = self.ui.cbHomeSrch4.currentText()
                    cmd = '{} {} {}'.format(cmd, txt3, txt4)
                axis.send_cmd(cmd)
        except RuntimeError as e:
            msg = 'Function doHomeSrch failed:\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Home Srch', msg)
        print(cmd)

    def doHomeStat(self):
        axis = IcepapController().iPaps[self.icepap_driver.icepapsystem_name][self.icepap_driver.addr]
        try:
            txt = ''
            if Mode.CONFIG in axis.mode:
                msg = 'Axis is in config mode. Aborting'
                print(msg)
                MessageDialogs.showErrorMessage(None, 'Home Stat', msg)
                return
            if self.ui.cbHomeSrch1.currentText() == 'HOME':
                status, direction = axis.homestat
                txt += '{} {}\n'.format(status, direction)
                try:
                    hp_axis = axis.get_home_position()
                except RuntimeError as e:
                    t = 'ERROR Last home search was not successful'
                    if t in str(e):
                        txt += 'PAxis {}\n'.format(t)
                        self.ui.homeBrowser.setText(txt)
                        return
                    else:
                        raise e
                txt += 'PAxis {}\n'.format(hp_axis)  # Todo: From here on never tested. Must do successful homing first.
                hp_tgtenc = axis.get_home_position('TGTENC')
                txt += 'PTgt {}\n'.format(hp_tgtenc)
                hp_shftenc = axis.get_home_position('SHFTENC')
                txt += 'PShft {}\n'.format(hp_shftenc)
                he_tgtenc = axis.get_home_encoder('TGTENC')
                txt += 'ETgt {}\n'.format(he_tgtenc)
                he_shftenc = axis.get_home_encoder('SHFTENC')
                txt += 'EShft {}'.format(he_shftenc)
            else:
                cmd = '{}:?SRCHSTAT'.format(self.icepap_driver.addr)
                ans = axis.send_cmd(cmd)  # Todo: This command fails! "Communication error"
                txt += ans  # Todo: Probably a list. Must fix!
            self.ui.homeBrowser.setText(txt)
        except RuntimeError as e:
            msg = 'Function doHomeStat failed:\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Home Stat', msg)

    def btnGO_on_click(self):
        new_position = self.ui.txtMvAbsolute.text()
        try:
            new_position = int(new_position)
            self._manager.moveDriverAbsolute(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, new_position)
        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")

    def btnGORelativePos_on_click(self):
        distance = self.ui.txtGORelative.text()
        try:
            distance = int(distance)
            steps = +distance
            self._manager.moveDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, steps)

        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")


    def btnGORelativeNeg_on_click(self):
        distance = self.ui.txtGORelative.text()
        try:
            distance = int(distance)
            steps = -distance
            self._manager.moveDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, steps)

        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")

    def btnStopMotor_on_click(self):
        self._manager.stopDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
        self.ui.sliderJog.setValue(0)


    def btnBlink_on_press(self):
        secs = 600
        if self.ui.btnBlink.isChecked():
            secs = 0
        self._manager.blinkDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr,secs)

    def sliderChanged(self, div):
        if self.ui.sliderJog.isSliderDown() or not self.sliderTimer.isActive():
            self.startJogging(div)

    def startJogging(self, div):
        if div <> 0:
            if not self.ui.btnEnable.isChecked():
                self._manager.enableDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
            speed = float(self.ui.txtSpeed.text())
            factor = (self.ui.sliderJog.maximum() - abs(div)) + 1
            speed = int(speed / factor)
            if div < 0:
                speed = -1 * speed
            try:
                QtGui.QToolTip.showText(self.cursor().pos(),str(speed),self.ui.sliderJog)
                self._manager.jogDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, speed)
            except Exception,e:
                MessageDialogs.showWarningMessage(self, "Jog Driver", "Error while trying to jog:\n"+str(e))
                self.ui.sliderJog.setValue(0)
        else:
            self.stopJogging()

    def stopJogging(self):
        self._manager.stopDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
        self.ui.sliderJog.setValue(0)
        self.sliderTimer.start()


    def resetSlider(self):
        value = self.ui.sliderJog.value()
        if value == 0:
            self.sliderTimer.stop()
        elif value > 0:
            self.ui.sliderJog.triggerAction(QtGui.QSlider.SliderSingleStepSub)
        else:
            self.ui.sliderJog.triggerAction(QtGui.QSlider.SliderSingleStepAdd)

    def _set_position(self):
        #pos_sel = str(self.ui.cb_pos_sel.currentText()).upper()
        pos_sel = str(self.ui.cb_pos_sel.currentText())
        try:
            position = int(self.ui.txtPos.text())
            self._manager.setDriverPosition(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, pos_sel, position)
        except:
            print "Unexpected error:", sys.exc_info()
            MessageDialogs.showWarningMessage(self, "Set driver position", "Wrong parameter format")


    def _set_encoder(self):
        #enc_sel = str(self.ui.cb_enc_sel.currentText()).upper()
        enc_sel = str(self.ui.cb_enc_sel.currentText())
        try:
            position = int(self.ui.txtEnc.text())
            self._manager.setDriverEncoder(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, enc_sel, position)
        except:
            print "Unexpected error:", sys.exc_info()
            MessageDialogs.showWarningMessage(self, "Set driver encoderposition", "Wrong parameter format")

    def endisDriver(self, bool):
         if bool:
            self.ui.btnEnable.setText("OFF")
            self._manager.enableDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
         else:
            self.ui.btnEnable.setText("ON")
            self._manager.disableDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)


    def changeSwitchesSetup(self, mode):
        return
        # SHOULD CHANGE SWITCHES SETUP... HOW? NOT IN CONFIG MODE...
        #try:
        #    pass
        #    #self._manager.jogDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, speed)
        #except Exception,e:
        #    MessageDialogs.showWarningMessage(self, "Switches setup", "Error while trying to change switches setup:\n"+str(e))


    # ---------------------- Historic Widget -------------------
    def showHistoricWidget(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.historicWidget.fillData(self.icepap_driver)

    def hideHistoricWidget(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    # ---------------------- Templates Catalog Widget -------------------
    def setTemplateParams(self,template_name,params):
        QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self._disconnectHighlighting()
        for param in params.keys():
            value = params.get(param)
            if self.param_to_widgets.has_key(param):
                widgets = self.param_to_widgets.get(param)
                self._setWidgetsValue(widgets, value, set_default=False)
            elif param == 'IPAPNAME':
                self._setWidgetsValue(self.param_to_widgets.get('DriverName'), value, set_default=False)
        # SHOULD DO SOMETHING WITH THE TEMPLATE NAME
        self.highlightTabs()
        self._connectHighlighting()
        QtGui.QApplication.instance().restoreOverrideCursor()
         ##   if self.var_dict.has_key(param):
         ##       [nsection, element] = self.var_dict[param]
         ##       self._setWidgetValue(element, value)
         ###print "THE TEMPLATE LABEL IS NOT YET IMPLEMENTED. Selected type: '%s'" % template_name
