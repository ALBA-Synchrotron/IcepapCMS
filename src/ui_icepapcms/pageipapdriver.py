from PyQt4 import QtCore, QtGui, Qt
from ui_pageipapdriver import Ui_PageiPapDriver
from qrc_icepapcms import *
from xml.dom import minidom, Node
from xml.dom.minidom import getDOMImplementation
from Led import Led
from lib_icepapcms import *
from messagedialogs import MessageDialogs
from dialoghistoriccfg import DialogHistoricCfg
from dialogtemplate import DialogTemplate
import sys
import os
from qvalidatelineedit import QValidateLineEdit
import time
from historiccfgwidget import HistoricCfgWidget

class PageiPapDriver(QtGui.QWidget):
    def __init__(self, mainwin):
        QtGui.QWidget.__init__(self, None)
        self._mainwin = mainwin
        self.ui = Ui_PageiPapDriver()
        self.ui.setupUi(self)
        
        #self.ui.toolBox.setItemIcon(self.ui.toolBox.indexOf(self.ui.page_test), QtGui.QIcon(":/icons/IcepapCfg Icons/ipapdriver.png"))
        #self.ui.toolBox.setItemIcon(self.ui.toolBox.indexOf(self.ui.page_cfg), QtGui.QIcon(":/icons/IcepapCfg Icons/preferences-system.png"))
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        #self.ui.tabWidget.removeTab(0)
        self.config_template = path+'/templates/driverparameters.xml'
        self.sectionTables = {}
        
        # Dictionary of input/output signals configurations
        # key = configuration name
        # item = [[type, [cfg]], ...] 
        self.inout_cfgs = {}
        # Dictionary of variables
        # key = variable name
        # item = [section, widget (section = 0) or row (section > 0)
        self.var_dict = {}
        self.test_var_dict = {}
        
        self.main_modified = []
        self.test_var_modified = []
        
        self.refreshTimer = Qt.QTimer(self)
        self.sliderTimer = Qt.QTimer(self)
        self.sliderTimer.setInterval(100)
        
        self.signalConnections()
        self.signalMapper = QtCore.QSignalMapper(self)
        
        self._readConfigTemplate()
        self._manager = MainManager()
        self.ui.btnUndo.setEnabled(False)
        

        self.setLedsOff()
        self.icepap_driver = None
        self.inMotion = -1
        self.status = -1
        self.setScrollBars()  
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.historicWidget.setCfgPage(self)
        self.hideHistoricWidget()
        self.ui.sliderJog.setEnabled(False)
        
    def setScrollBars(self):
        self.ui.sahboxlayout = QtGui.QHBoxLayout(self.ui.tab_connectors)
        self.ui.sahboxlayout.setMargin(9)
        self.ui.sahboxlayout.setSpacing(6)
        self.ui.sahboxlayout.setObjectName("sahboxlayout")
        self.ui.sa = QtGui.QScrollArea(self.ui.tab_connectors) 
        self.ui.sa.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
        self.ui.labels_widget.setParent(None)
        self.ui.sa.setWidget(self.ui.labels_widget)
        self.ui.sa.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
        self.ui.sa.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
        self.ui.sa.setFrameStyle(QtGui.QFrame.NoFrame)
        self.ui.sahboxlayout.addWidget(self.ui.sa)
        
        
        self.ui.sahboxlayout2 = QtGui.QHBoxLayout(self.ui.tab_InOut)
        self.ui.sahboxlayout2.setMargin(9)
        self.ui.sahboxlayout2.setSpacing(6)
        self.ui.sahboxlayout2.setObjectName("sahboxlayout2")
        self.ui.sa2 = QtGui.QScrollArea(self.ui.tab_InOut) 
        self.ui.sa2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
        self.ui.inOut_widget.setParent(None)
        self.ui.sa2.setWidget(self.ui.inOut_widget)
        self.ui.sa2.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
        self.ui.sa2.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
        self.ui.sa2.setFrameStyle(QtGui.QFrame.NoFrame)
        self.ui.sahboxlayout2.addWidget(self.ui.sa2)
        
        

        
        #self.ui.txtDriverName.setValidator(QtGui.QIntValidator(1,100,self))
        
    def signalConnections(self):
        QtCore.QObject.connect(self.ui.btnApplyCfg,QtCore.SIGNAL("clicked()"),self.btnApplyCfg_on_click)
        #QtCore.QObject.connect(self.ui.btnHistoric,QtCore.SIGNAL("clicked()"),self.Historic_on_click)
        #QtCore.QObject.connect(self.ui.btnTemplates,QtCore.SIGNAL("clicked()"),self.btnTemplates_on_click)
        QtCore.QObject.connect(self.ui.btnUndo,QtCore.SIGNAL("clicked()"),self.btnUndo_on_click)
        QtCore.QObject.connect(self.ui.btnRestore,QtCore.SIGNAL("clicked()"),self.btnRestore_on_click)
        QtCore.QObject.connect(self.ui.btnGO,QtCore.SIGNAL("clicked()"),self.btnGO_on_click)
        QtCore.QObject.connect(self.ui.btnGORelativePos,QtCore.SIGNAL("clicked()"),self.btnGORelativePos_on_click)
        QtCore.QObject.connect(self.ui.btnGORelativeNeg,QtCore.SIGNAL("clicked()"),self.btnGORelativeNeg_on_click)
        QtCore.QObject.connect(self.ui.btnEnable,QtCore.SIGNAL("clicked(bool)"),self.endisDriver)
        QtCore.QObject.connect(self.ui.btnStopMotor,QtCore.SIGNAL("clicked()"),self.btnStopMotor_on_click)
        QtCore.QObject.connect(self.ui.btnSetPos,QtCore.SIGNAL("clicked()"),self.setPosition)
        QtCore.QObject.connect(self.ui.btnSetEnc,QtCore.SIGNAL("clicked()"),self.setEncoder)
        #QtCore.QObject.connect(self.ui.toolBox,QtCore.SIGNAL("currentChanged(int)"),self.toolBox_current_changed)
        QtCore.QObject.connect(self.ui.txtSpeed,QtCore.SIGNAL("editingFinished()"),self.setMotionValues)
        QtCore.QObject.connect(self.ui.txtAcceleration,QtCore.SIGNAL("editingFinished()"),self.setMotionValues)
        QtCore.QObject.connect(self.refreshTimer,QtCore.SIGNAL("timeout()"),self.updateTestStatus)
        #QtCore.QObject.connect(self.ui.chbSyncIn, QtCore.SIGNAL("stateChanged(int)"), self.chbSyncInChanged)
        #QtCore.QObject.connect(self.ui.chbSyncOut, QtCore.SIGNAL("stateChanged(int)"), self.chbSyncOutChanged)
        
        #QtCore.QObject.connect(self.ui.listPredefined, QtCore.SIGNAL("currentTextChanged (const QString&)"), self.loadPredefinedSignalCfg)
        #QtCore.QObject.connect(self.ui.btnClear,QtCore.SIGNAL("clicked()"),self.resetSignalsTab)
        
        #QtCore.QObject.connect(self.ui.sliderJog,QtCore.SIGNAL("sliderMoved(int)"),self.startJogging)
        QtCore.QObject.connect(self.ui.sliderJog,QtCore.SIGNAL("valueChanged(int)"),self.sliderChanged)
        QtCore.QObject.connect(self.ui.sliderJog,QtCore.SIGNAL("sliderReleased()"),self.stopJogging)
        
        QtCore.QObject.connect(self.sliderTimer,QtCore.SIGNAL("timeout()"),self.resetSlider)
        
        #QtCore.QObject.connect(self.signalMapper, QtCore.SIGNAL("mapped(int)"), self.highlightWidget)
    
    

    def highlightWidget(self, widget):
        highlight = False
        if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
                if widget.defaultvalue != widget.value():
                    highlight = True
                    widget.setStyleSheet("background-color: rgb(255, 255, 0)")
        elif isinstance(widget, QtGui.QCheckBox):
                if widget.defaultvalue != widget.isChecked():
                    highlight = True
                    widget.setStyleSheet("background-color: rgb(255, 255, 0)")
        elif isinstance(widget, QtGui.QComboBox):
            if widget.defaultvalue != str(widget.currentText()).upper():
                highlight = True
                widget.setStyleSheet(" QComboBox::drop-down {background-color: yellow;}")
        elif isinstance(widget, QtGui.QLineEdit):
                if widget.defaultvalue != str(widget.text()):
                    highlight = True
                    widget.setStyleSheet("background-color: rgb(255, 255, 0)")
                             
        if highlight:
            if widget.isTest:
                if not widget in self.test_var_modified:
                    self.test_var_modified.append(widget)
            else:
                if not widget in self.main_modified:
                    self.main_modified.append(widget)
            
        else:
            if widget.isTest:
                self.test_var_modified.remove(widget)
            else:
                self.main_modified.remove(widget)
            widget.setStyleSheet("")
        

    def _connectHighlighting(self):
        #clear previous state
        self.main_modified = []
        self.test_var_modified = []
        QtCore.QObject.connect(self.signalMapper, QtCore.SIGNAL("mapped(QWidget*)"), self.highlightWidget)
    
    def _disconnectHighlighting(self):
        for nsection, widget in self.var_dict.itervalues():
            if nsection == 0:
                widget.setStyleSheet("")
        aux = []
        for widget in self.test_var_dict.itervalues():
            if type(widget) == type(aux):
                for w in widget:
                    w.setStyleSheet("")
            else:
                widget.setStyleSheet("")
        QtCore.QObject.disconnect(self.signalMapper, QtCore.SIGNAL("mapped(QWidget*)"),self.highlightWidget)
          
# ------------------------------  Configuration ----------------------------------------------------------    
    def _readConfigTemplate(self):
        doc = minidom.parse(self.config_template)
        root  = doc.documentElement
        row = 0
        nsection = 0
        for section in root.getElementsByTagName("section"):
            if section.nodeType == Node.ELEMENT_NODE:
                    section_name =  section.attributes.get('name').value
            inMainSection = (section_name == "main")
            inTestSection =  (section_name == "test")
            if not inMainSection and not inTestSection:
                self._addSectionTab(section_name)
                
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    parid =  pars.attributes.get('id').value
                    parid = parid.strip()
                    parname =  pars.attributes.get('name').value
                    parname = parname.strip()
                    partype =  pars.attributes.get('type').value
                    partype = partype.strip()
                    if partype != "BOOL" and partype != "STRING" and partype != "ARRAY":
                        parmin =  pars.attributes.get('min').value
                        parmin = parmin.strip()
                        parmax =  pars.attributes.get('max').value
                        parmax = parmax.strip()
                        
                    pardesc = self._getText(pars.getElementsByTagName("description")[0].firstChild)
                    if inMainSection or inTestSection:
                        widget = getattr(self.ui, parid)
                        if widget == None:
                            print parid + " not found in GUI"
                        else:
                            self._connectWidgetToSignalMap(widget)
                            if inMainSection:
                                widget.isTest = False                            
                                self.var_dict[parname] = [nsection, widget]
                            else:
                                widget.isTest = True
                                if partype == "ARRAY":
                                    if not self.test_var_dict.has_key(parname):
                                        widget_list = []
                                        widget_list.append(widget)
                                    else:
                                        widget_list = self.test_var_dict[parname]
                                        widget_list.append(widget)
                                    self.test_var_dict[parname] = widget_list
                                else:
                                    self.test_var_dict[parname] = widget
                    else:
                        self.var_dict[parname] = [nsection, row]
                        
                    
                    if not inMainSection and not inTestSection:
                        self.sectionTables[nsection].insertRow(row)
                        self._addItemToTable(nsection, row, 0, parname, False)
                        self._addWidgetToTable(nsection, row, 2, partype, parmin, parmax)
                        self._addItemToTable(nsection, row, 3, pardesc, False)
                        row = row + 1
            row = 0
            nsection = nsection + 1
          
            
        

    def _addSectionTab(self, section_name):
        tab = QtGui.QWidget()
        tab.setObjectName("tab_"+section_name)

        vboxlayout = QtGui.QVBoxLayout(tab)
        vboxlayout.setMargin(9)
        vboxlayout.setSpacing(6)
        vboxlayout.setObjectName("vboxlayout"+section_name)

        tableWidget = QtGui.QTableWidget(tab)
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
        tableWidget.setPalette(palette)
        tableWidget.setAlternatingRowColors(True)
        tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        tableWidget.setObjectName(section_name)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        vboxlayout.addWidget(tableWidget)
        tab.setLayout(vboxlayout)
        #self.ui.tabWidget.addTab(tab,"")        
        self.ui.tabWidget.insertTab(self.ui.tabWidget.count()-1, tab,"")        
        tableWidget.clear()
        tableWidget.setColumnCount(4)
        tableWidget.setRowCount(0)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("PageiPapDriver", "Name", None, QtGui.QApplication.UnicodeUTF8))
        tableWidget.setHorizontalHeaderItem(0,headerItem)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("PageiPapDriver", "Value", None, QtGui.QApplication.UnicodeUTF8))
        tableWidget.setHorizontalHeaderItem(1,headerItem1)

        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("PageiPapDriver", "New Value", None, QtGui.QApplication.UnicodeUTF8))
        tableWidget.setHorizontalHeaderItem(2,headerItem2)

        headerItem3 = QtGui.QTableWidgetItem()
        headerItem3.setText(QtGui.QApplication.translate("PageiPapDriver", "Description", None, QtGui.QApplication.UnicodeUTF8))
        tableWidget.setHorizontalHeaderItem(3,headerItem3)
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(tab), section_name)
        
        
        self.sectionTables[self.ui.tabWidget.indexOf(tab)] = tableWidget
        

           
    def _addItemToTable(self, section, row, column, text, editable):
        item = QtGui.QTableWidgetItem()
        item.setText(text)
        if not editable:
            item.setFlags(Qt.Qt.ItemIsSelectable)
        else:
            item.setTextColor(QtGui.QColor(Qt.Qt.red))
        table = self.sectionTables[section]
        
        table.setItem(row, column, item)
        
    def _addWidgetToTable(self, section, row, column, type, min, max):
        table = self.sectionTables[section]
        
        if type == "INTEGER":
            type = QValidateLineEdit.INTEGER
        elif type == "DOUBLE":
            type = QValidateLineEdit.DOUBLE
        elif type == "STRING":
            le = QtGui.QLineEdit(Table)
            table.setCellWidget(row, column, le)
            return
        le = QValidateLineEdit(table, type , min, max)
        table.setCellWidget(row, column, le)
            
        
        #table.setItem(row, column, item)
    
    def fillData(self, icepap_driver):
        #self.ui.tabWidget.setCurrentIndex(0)
        self._disconnectHighlighting()
        #self.resetSignalsTab()
        self.icepap_driver = icepap_driver
        description = "Icepap: %s  -  Crate: %s  -  Addr: %s  -  Firmware version: %s\n" % (icepap_driver.icepap_name, icepap_driver.cratenr, icepap_driver.addr, icepap_driver.currentCfg.getAttribute("VER"))
        if self.icepap_driver.currentCfg.signature:
            description = description + "Last signature %s " % self.icepap_driver.currentCfg.signature
            #aux = self.icepap_driver.currentCfg.signature.split('_')
            #description = description + "Signed on %s %s" % (aux[0], time.ctime(float(aux[1])))
        else:            
            description = description + "Current configuration not signed"
        if self.icepap_driver.mode == IcepapMode.CONFIG:
            self._mainwin.addDriverToSign(self.icepap_driver)
        self.ui.txtDescription.setText(description)
        self.ui.txtDriverName.setText(self.icepap_driver.name)
        #self.ui.txtDriverNemonic.setText(self.icepap_driver.nemonic)
        for name, value in icepap_driver.currentCfg.parList.items():
            if self.var_dict.has_key(name):
                [nsection, element] = self.var_dict[name]
                if nsection == 0:
                    # In main tab
                    self._setWidgetValue(element, value)                    
                else:
                    self._addItemToTable(nsection, element, 1, value, False)
                    self.sectionTables[nsection].cellWidget(element,2).setText("")
                #self._addItemToTable(nsection, row, 2, "", True)
        # get testing values
        self.startTesting()
        if not (self.status == -1 or self.status == 1):
            result = self._manager.readIcepapParameters(self.icepap_driver.icepap_name,self.icepap_driver.addr, self.test_var_dict.keys())
            for [name, value] in result:
                if self.test_var_dict.has_key(name):
                    widget = self.test_var_dict[name]
                    try:
                        if type(widget) == type(result):
                            value = value.split()
                            i = 0
                            for w in widget:
                                self._setWidgetValue(w, value[i])
                                i = i +1
                        else:
                            self._setWidgetValue(widget, value)
                    except:             
                        pass           
        
        self._connectHighlighting()
        if self.ui.historicWidget.isVisible():
            self.ui.historicWidget.fillData(self.icepap_driver)
    
    def _connectWidgetToSignalMap(self, widget):
        self.signalMapper.setMapping(widget, widget)
        if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("valueChanged (const QString&)"), self.signalMapper, QtCore.SLOT("map()"))
        elif isinstance(widget, QtGui.QCheckBox):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("stateChanged(int)"), self.signalMapper, QtCore.SLOT("map()"))
        elif isinstance(widget, QtGui.QComboBox):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("editTextChanged(const QString&)"), self.signalMapper, QtCore.SLOT("map()"))
            QtCore.QObject.connect(widget, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.signalMapper, QtCore.SLOT("map()"))
        elif isinstance(widget, QtGui.QLineEdit):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("textChanged(const QString&)"), self.signalMapper, QtCore.SLOT("map()"))
    
    def _setWidgetValue(self, widget, value, default=True):
        try:
            if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
                widget.setValue(float(value))
                if default:
                    widget.defaultvalue = widget.value()
            elif isinstance(widget, QtGui.QCheckBox):
                state = (value == "1" or value == "YES" or value =="ON")
                if default:
                    widget.defaultvalue = state 
                widget.setChecked(state)
            elif isinstance(widget, QtGui.QComboBox):
                widget.setCurrentIndex(widget.findText(value, QtCore.Qt.MatchFixedString))
                if default:
                    widget.defaultvalue = str(value)                
            elif isinstance(widget, QtGui.QLineEdit):
                widget.setText(str(value))
                if default:
                    widget.defaultvalue = str(value)
                
                
        except:
            print "error in _setWidgetValue"
    
    def _getWidgetValue(self, widget):
        try:
            if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
                return widget.value()
            elif isinstance(widget, QtGui.QCheckBox):
                if widget.isChecked():
                    if widget.isTest:
                        return "ON"
                    else:
                        return "YES"
                else:
                    if widget.isTest:
                        return "OFF"
                    else:
                        return "NO"
            elif isinstance(widget, QtGui.QComboBox):
                return str(widget.currentText()).upper()
            elif isinstance(widget, QtGui.QLineEdit):
                return str(widget.text()).upper()
        except:
            print "error in _getWidgetValue"
        
    
    def addNewCfg(self, cfg):
        #self.ui.toolBox.setCurrentIndex(0)
        for name, value in cfg.parList.items():
            if self.var_dict.has_key(name):
                [nsection, element] = self.var_dict[name]
                if nsection == 0:
                    self._setWidgetValue(element, value, False) 
                else:
                    self.sectionTables[nsection].cellWidget(element,2).setText(value)
                    #self._addItemToTable(nsection, row, 2, value, True)
        

        

    def _getText(self, node):
        rc = ""
        if node != None:
                rc = str(node.data)
        return rc              
    

        
    def btnApplyCfg_on_click(self):
        self.icepap_driver.name = str(self.ui.txtDriverName.text())
        #self.icepap_driver.nemonic = str(self.ui.txtDriverNemonic.text())
        new_values = []
        values_ok = True
        save_ok = True
        test_values_ok = True
        # First get modified items in main section
        self._mainwin.ui.actionHistoricCfg.setChecked(False)
        self.hideHistoricWidget()
        for name, [nsection, widget] in self.var_dict.items():
            if nsection == 0:
                if widget in self.main_modified:
                    value = self._getWidgetValue(widget)
                    new_values.append([name, value])
                  
        
        for tableWidget in self.sectionTables.itervalues():
            for row in range(tableWidget.rowCount()):
                #val = tableWidget.item(row,2).text()
                le = tableWidget.cellWidget(row,2)
                val = le.text()
                if not val == "":
                    try:
                        name = str(tableWidget.item(row,0).text())
                        #print str(le.type)
                        if isinstance(le, QValidateLineEdit):
                            if le.type == 0:
                            #if name == "MICRO" or name =="PSW":
                                val = int(val)
                            else:
                                val = float(val)
                        new_values.append([name, val])                    
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        values_ok = False
                        break
        
        if values_ok and len(new_values) > 0:
            save_ok = self._manager.saveValuesInIcepap(self.icepap_driver, new_values)
        elif not values_ok:
            save_ok = False
            MessageDialogs.showWarningMessage(self, "Driver configuration", "Wrong parameter format")
        
        # save testing values
        if not (self.status == -1 or self.status == 1):
            test_values_list = []
            for name, widget in self.test_var_dict.items():
                try:
                    if type(widget) == type(test_values_list):
                        add = False
                        value = ""
                        for w in widget:
                            if w in self.test_var_modified:
                                add = True
                            value = value + str(self._getWidgetValue(w)) + " "
                        if add:
                            test_values_list.append([name, value])                                    
                    else:
                        if widget in self.test_var_modified:
                            value = self._getWidgetValue(widget)
                            test_values_list.append([name, value])
                except:
                    test_values_ok = False
                    break
                    
            self._manager.writeIcepapParameters(self.icepap_driver.icepap_name, self.icepap_driver.addr, test_values_list)
        
        #self.configureSignals()
        if save_ok and test_values_ok:
            self.fillData(self.icepap_driver)
            self.ui.btnUndo.setEnabled(True)
        else:
            MessageDialogs.showWarningMessage(self, "Driver configuration", "Error saving configuration")
        
        
        
        
        self._disconnectHighlighting()
        self._connectHighlighting()
    
              
    def btnUndo_on_click(self):
        self._manager.undoDriverConfiguration(self.icepap_driver)
        self.fillData(self.icepap_driver)
        if not self.icepap_driver.hasUndoList():
            self.ui.btnUndo.setEnabled(False)    
    
    def btnRestore_on_click(self):
        self.addNewCfg(self.icepap_driver.currentCfg)
        #.fillData(self.icepap_driver)
        
    
    def doImport(self):
        try:
            fn = QtGui.QFileDialog.getOpenFileName(self)
            if fn.isEmpty():
                return
            filename = str(fn)
            
            self.fillFileData(filename)
        except:
            MessageDialogs.showWarningMessage(self, "File", "Error reading file\n")
    
    def fillFileData(self, filename):
        #self.ui.toolBox.setCurrentIndex(0)
        doc = minidom.parse(filename)
        root  = doc.documentElement
        for section in root.getElementsByTagName("section"):
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    parname =  pars.attributes.get('name').value
                    parname = parname.strip()
                    parval =  pars.attributes.get('value').value
                    parval = parval.strip()
                    [nsection, element] = self.var_dict[parname]
                    #self._addItemToTable(nsection, row, 2, parval, True)
                    if nsection == 0:
                        self._setWidgetValue(element, parval) 
                    else:
                        self.sectionTables[nsection].cellWidget(element,2).setText(parval)
                    
                     
                    
    def doExport(self):        
        #try:
            fn = QtGui.QFileDialog.getSaveFileName(self)
            if fn.isEmpty():
                return
            filename = str(fn)
            self.exportToFile(filename)
        #except:
        #    MessageDialogs.showWarningMessage(self, "File", "Error saving file\n")
    
    def exportToFile(self, filename):
        output = open(filename, "w")
        newdoc = self.getXmlData()
        output.writelines(newdoc.toprettyxml())
        
    def getXmlData(self):
        impl = getDOMImplementation()
        newdoc = impl.createDocument(None, "Driver", None)
        esection = newdoc.createElement("section")
        esection.setAttribute("name", "main")
        for name, [nsection, widget] in self.var_dict.items():
            if nsection == 0:
                value = self._getWidgetValue(widget)
                print name + " _ " + str(value)
                epar = newdoc.createElement("par")
                epar.setAttribute("name", name)
                epar.setAttribute("value", str(value))
                esection.appendChild(epar)
        newdoc.documentElement.appendChild(esection)
         
        for tableWidget in self.sectionTables.itervalues():
            esection = newdoc.createElement("section")
            esection.setAttribute("name", tableWidget.objectName())
            for row in range(tableWidget.rowCount()):
                val = tableWidget.item(row,1).text()
                if not val == "":
                    name = str(tableWidget.item(row,0).text())
                epar = newdoc.createElement("par")
                epar.setAttribute("name", name)
                epar.setAttribute("value", val)
                esection.appendChild(epar)
            newdoc.documentElement.appendChild(esection)    
        return newdoc
            
    def signDriver(self):
        self.icepap_driver.signDriver()
               
# ------------------------------  Testing ----------------------------------------------------------            
    def startTesting(self):
        if not self.icepap_driver is None:
            self.inMotion = -1
            self.status = -1
            self.ready = -1
            self.mode = -1
            self.power = -1
            #self._manager.enableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
            self.updateTestStatus()
            self.refreshTimer.start(1500)
        
    def stopTesting(self):
        try:
            self.refreshTimer.stop()
            #self._manager.disableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
            self.setLedsOff()
        except:
            print "Unexpected error:", sys.exc_info()
            
        
        
    def getMotionValues(self):
        (speed, acc) = self._manager.getDriverMotionValues(self.icepap_driver.icepap_name, self.icepap_driver.addr)
        
        self.ui.txtSpeed.setText(str(speed))
        self.ui.txtAcceleration.setText(str(acc))
    
    
    def setMotionValues(self):
        speed = self.ui.txtSpeed.text()
        acc = self.ui.txtAcceleration.text()
        try:
            self._manager.setDriverMotionValues(self.icepap_driver.icepap_name, self.icepap_driver.addr, [float(speed), float(acc)])
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
        self.ui.tab_3.setEnabled(False)
    
    def enableAllControl(self):
        self.ui.txtSpeed.setEnabled(True)
        self.ui.txtAcceleration.setEnabled(True)
        self.ui.btnGO.setEnabled(True)
        self.ui.btnGORelativeNeg.setEnabled(True)
        if self.mode == 0:
            self.ui.btnGO.setEnabled(True)
            """ Jog not working now """
            #self.ui.sliderJog.setEnabled(True)
        else:
            self.ui.btnGO.setEnabled(False)
            self.ui.sliderJog.setEnabled(False)
        self.ui.btnEnable.setEnabled(True)
        self.ui.btnStopMotor.setEnabled(True)
        self.ui.tab_3.setEnabled(True)
        
                
    def updateTestStatus(self):  
        pos_sel = str(self.ui.cb_pos_sel.currentText()).upper()
        enc_sel = str(self.ui.cb_enc_sel.currentText()).upper()
        (status, power, position) = self._manager.getDriverTestStatus(self.icepap_driver.icepap_name, self.icepap_driver.addr, pos_sel, enc_sel)
        
        #self.StepSize = self.ui.sbFactor.value()           
        disabled = IcepapStatus.isDisabled(status)
        moving = IcepapStatus.isMoving(status)
        ready = IcepapStatus.isReady(status)
        mode = IcepapStatus.getMode(status)
        if self.inMotion <> moving:
            if moving == 1:
                self.refreshTimer.setInterval(750)
                self.ui.LedStep.on()
            elif moving == -1:
                self.refreshTimer.stop()
            else:
                self.refreshTimer.setInterval(1500)
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
                    self.ui.btnEnable.setText("disable")
                    self.ui.btnEnable.setChecked(True)
                else:
                    self.ui.btnEnable.setEnabled(True)
                    self.ui.btnEnable.setText("enable")
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
                self.ui.btnEnable.setText("enable")
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

                
    def btnGO_on_click(self):
        new_position = self.ui.txtMvAbsolute.text()
        try:
            new_position = int(new_position)
            self._manager.moveDriverAbsolute(self.icepap_driver.icepap_name, self.icepap_driver.addr, new_position)
        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")
            
    def btnGORelativePos_on_click(self):
        distance = self.ui.txtGORelative.text()
        try:
            distance = int(distance)
            steps = +distance
            self._manager.moveDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr, steps)

        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")
            
    
    def btnGORelativeNeg_on_click(self):
        distance = self.ui.txtGORelative.text()
        try:
            distance = int(distance)
            steps = -distance
            self._manager.moveDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr, steps)

        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")
        
    def btnStopMotor_on_click(self):
        self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
        
    
    
    def sliderChanged(self, div):
        if self.ui.sliderJog.isSliderDown() or not self.sliderTimer.isActive():
            self.startJogging(div)
            
    def startJogging(self, div):
        #try:
        if div <> 0:
            if not self.ui.btnEnable.isChecked():
                self._manager.enableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
            speed = float(self.ui.txtSpeed.text())
            factor = (self.ui.sliderJog.maximum() - abs(div)) + 1 
            speed = int(speed / factor)
            dir = (div > 0)
            self._manager.jogDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr, str(speed), dir)
        else:
            self.stopJogging()
        #except:
        #    pass
    
    def stopJogging(self):
        self._manager.jogDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr, "0", True)
        #self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
        
        self.sliderTimer.start()
        
    
    def resetSlider(self):
        value = self.ui.sliderJog.value()
        if value == 0:
            self.sliderTimer.stop()
        elif value > 0:
            self.ui.sliderJog.triggerAction(QtGui.QSlider.SliderSingleStepSub)
        else:
            self.ui.sliderJog.triggerAction(QtGui.QSlider.SliderSingleStepAdd)
    
    def setPosition(self):
        pos_sel = str(self.ui.cb_pos_sel.currentText()).upper()
        try:
            position = int(self.ui.txtPos.text())
            self._manager.setDriverPosition(self.icepap_driver.icepap_name, self.icepap_driver.addr, pos_sel, position)
        except:
            print "Unexpected error:", sys.exc_info()
            MessageDialogs.showWarningMessage(self, "Set driver position", "Wrong parameter format")
        
    
    def setEncoder(self):
        enc_sel = str(self.ui.cb_enc_sel.currentText()).upper()
        try:
            position = int(self.ui.txtEnc.text())
            self._manager.setDriverPosition(self.icepap_driver.icepap_name, self.icepap_driver.addr, enc_sel, position)
        except:
            print "Unexpected error:", sys.exc_info()
            MessageDialogs.showWarningMessage(self, "Set driver encoderposition", "Wrong parameter format")
            
    def endisDriver(self, bool):
         if bool:
            self.ui.btnEnable.setText("disable")
            self._manager.enableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
         else:
            self.ui.btnEnable.setText("enable")
            self._manager.disableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
        

    # ---------------------- Historic Widget -------------------
    def showHistoricWidget(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.historicWidget.fillData(self.icepap_driver)
    def hideHistoricWidget(self):
        self.ui.stackedWidget.setCurrentIndex(0)