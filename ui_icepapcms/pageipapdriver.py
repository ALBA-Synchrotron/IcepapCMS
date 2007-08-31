from PyQt4 import QtCore, QtGui, Qt
from ui_pageipapdriver import Ui_PageiPapDriver
from qrc_icepapcms import *
from xml.dom import minidom, Node
from xml.dom.minidom import getDOMImplementation
from Led import Led
from  lib_icepapcms import MainManager, IcepapSignal, IcepapSignalCfg, IcepapSignalSrc
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
        self.main_modified = []
        
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
        
        self.ui.sahboxlayout3 = QtGui.QHBoxLayout(self.ui.tab_aux)
        self.ui.sahboxlayout3.setMargin(9)
        self.ui.sahboxlayout3.setSpacing(6)
        self.ui.sahboxlayout3.setObjectName("sahboxlayout3")
        self.ui.sa3 = QtGui.QScrollArea(self.ui.tab_aux) 
        self.ui.sa3.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
        self.ui.aux_widget.setParent(None)
        self.ui.sa3.setWidget(self.ui.aux_widget)
        self.ui.sa3.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
        self.ui.sa3.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
        self.ui.sa3.setFrameStyle(QtGui.QFrame.NoFrame)
        self.ui.sahboxlayout3.addWidget(self.ui.sa3)

        
        #self.ui.txtDriverName.setValidator(QtGui.QIntValidator(1,100,self))
        
    def signalConnections(self):
        QtCore.QObject.connect(self.ui.btnApplyCfg,QtCore.SIGNAL("clicked()"),self.btnApplyCfg_on_click)
        #QtCore.QObject.connect(self.ui.btnHistoric,QtCore.SIGNAL("clicked()"),self.Historic_on_click)
        #QtCore.QObject.connect(self.ui.btnTemplates,QtCore.SIGNAL("clicked()"),self.btnTemplates_on_click)
        QtCore.QObject.connect(self.ui.btnUndo,QtCore.SIGNAL("clicked()"),self.btnUndo_on_click)
        QtCore.QObject.connect(self.ui.btnGO,QtCore.SIGNAL("clicked()"),self.btnGO_on_click)
        QtCore.QObject.connect(self.ui.btnGORelativePos,QtCore.SIGNAL("clicked()"),self.btnGORelativePos_on_click)
        QtCore.QObject.connect(self.ui.btnGORelativeNeg,QtCore.SIGNAL("clicked()"),self.btnGORelativeNeg_on_click)
        QtCore.QObject.connect(self.ui.btnEnable,QtCore.SIGNAL("clicked(bool)"),self.endisDriver)
        QtCore.QObject.connect(self.ui.btnStopMotor,QtCore.SIGNAL("clicked()"),self.btnStopMotor_on_click)
        QtCore.QObject.connect(self.ui.BtnSetPos,QtCore.SIGNAL("clicked()"),self.BtnSetPos_on_click)
        #QtCore.QObject.connect(self.ui.toolBox,QtCore.SIGNAL("currentChanged(int)"),self.toolBox_current_changed)
        QtCore.QObject.connect(self.ui.txtSpeed,QtCore.SIGNAL("editingFinished()"),self.setMotionValues)
        QtCore.QObject.connect(self.ui.txtAcceleration,QtCore.SIGNAL("editingFinished()"),self.setMotionValues)
        QtCore.QObject.connect(self.refreshTimer,QtCore.SIGNAL("timeout()"),self.updateTestStatus)
        QtCore.QObject.connect(self.ui.chbSyncIn, QtCore.SIGNAL("stateChanged(int)"), self.chbSyncInChanged)
        QtCore.QObject.connect(self.ui.chbSyncOut, QtCore.SIGNAL("stateChanged(int)"), self.chbSyncOutChanged)
        
        QtCore.QObject.connect(self.ui.listPredefined, QtCore.SIGNAL("currentTextChanged (const QString&)"), self.loadPredefinedSignalCfg)
        QtCore.QObject.connect(self.ui.btnClear,QtCore.SIGNAL("clicked()"),self.resetSignalsTab)
        
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
        elif isinstance(widget, QtGui.QCheckBox):
                if widget.defaultvalue != widget.isChecked():
                    highlight = True
        if highlight:
            widget.setStyleSheet("background-color: rgb(255, 255, 0)")
            if not widget in self.main_modified:
                self.main_modified.append(widget)
            
        else:
            self.main_modified.remove(widget)
            widget.setStyleSheet("")
        

    def _connectHighlighting(self):
        #clear previous state
        QtCore.QObject.connect(self.signalMapper, QtCore.SIGNAL("mapped(QWidget*)"), self.highlightWidget)
    
    def _disconnectHighlighting(self):
        for nsection, widget in self.var_dict.itervalues():
            if nsection == 0:
                widget.setStyleSheet("")
        QtCore.QObject.disconnect(self.signalMapper, QtCore.SIGNAL("mapped(QWidget*)"),self.highlightWidget)
          
    def toolBox_current_changed(self, index):
        if index == 0:
            self.stopTesting()
        else:
            self.startTesting()
    
    def chbSyncInChanged(self, st):
        if st:
            self.ui.chbSyncOut.setChecked(False)
            
    def chbSyncOutChanged(self, st):
        if st:
            self.ui.chbSyncIn.setChecked(False)
        
    def resetSignalsTab(self):
         self.ui.chbInPos.setChecked(False)
         self.ui.chbEncIn.setChecked(False)
         self.ui.chbSyncIn.setChecked(False)
         self.ui.chbSyncOut.setChecked(False)
         self.ui.chbOutPos.setChecked(False)
         self.ui.chbTarget.setChecked(False)
         self.ui.chbAuxPos1.setChecked(False)
         self.ui.chbAuxPos2.setChecked(False)
         self.ui.listPredefined.clearSelection()
         #self.ui.listPredefined.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
         
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
            if not inMainSection:
                self._addSectionTab(section_name)
                
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    parid =  pars.attributes.get('id').value
                    parid = parid.strip()
                    parname =  pars.attributes.get('name').value
                    parname = parname.strip()
                    partype =  pars.attributes.get('type').value
                    partype = partype.strip()
                    if partype != "BOOL":
                        parmin =  pars.attributes.get('min').value
                        parmin = parmin.strip()
                        parmax =  pars.attributes.get('max').value
                        parmax = parmax.strip()
                    pardesc = self._getText(pars.getElementsByTagName("description")[0].firstChild)
                    if inMainSection:
                        widget = getattr(self.ui, parid)
                        self._connectWidgetToSignalMap(widget)
                        if widget == None:
                            print parid + " not found in GUI"
                        else:                            
                            self.var_dict[parname] = [nsection, widget]
                    else:
                        self.var_dict[parname] = [nsection, row]
                    
                    if not inMainSection:
                        
                        self.sectionTables[nsection].insertRow(row)
                        self._addItemToTable(nsection, row, 0, parname, False)
                        self._addWidgetToTable(nsection, row, 2, partype, parmin, parmax)
                        self._addItemToTable(nsection, row, 3, pardesc, False)
                        row = row + 1
            row = 0
            nsection = nsection + 1
            
        for inout in root.getElementsByTagName("inout"):
            for cfg in inout.getElementsByTagName("cfg"):
                if cfg.nodeType == Node.ELEMENT_NODE:
                    cfgname =  cfg.attributes.get('name').value
                    self.ui.listPredefined.addItem(cfgname)
                    cfg_list = []
                    
                    for input in cfg.getElementsByTagName("input"):
                        if input.nodeType == Node.ELEMENT_NODE:
                            name =  input.attributes.get('name').value
                            mode =  input.attributes.get('mode').value
                            edge =  input.attributes.get('edge').value
                            direction =  input.attributes.get('direction').value
                            cfg_list.append(["input", name, [int(mode),int(edge),int(direction)]])
                            
                    
                    for output in cfg.getElementsByTagName("output"):
                        if output.nodeType == Node.ELEMENT_NODE:
                            name =  output.attributes.get('name').value
                            src =  output.attributes.get('src').value
                            mode =  output.attributes.get('mode').value
                            edge =  output.attributes.get('edge').value
                            pulse_width =  output.attributes.get('pulse_width').value
                            direction =  output.attributes.get('direction').value
                            cfg_list.append(["output", name, [int(src), int(mode),int(edge),int(direction), int(pulse_width)]])
                            
                    
                    for counter in cfg.getElementsByTagName("counter"):
                        if counter.nodeType == Node.ELEMENT_NODE:
                            name = counter.attributes.get('name').value
                            src = counter.attributes.get('src').value
                            cfg_list.append(["counter", name , [int(src)]])
                            
                    self.inout_cfgs[cfgname] = cfg_list
        
            
        

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
            
        le = QValidateLineEdit(table, type , min, max)
        table.setCellWidget(row, column, le)
            
        
        #table.setItem(row, column, item)
    
    def fillData(self, icepap_driver):
        #self.ui.tabWidget.setCurrentIndex(0)
        self._disconnectHighlighting()
        self.resetSignalsTab()
        self.icepap_driver = icepap_driver
        description = "Icepap: %s  -  Crate: %s  -  Addr: %s  -  Firmware version: %s\n" % (icepap_driver.icepap_name, icepap_driver.cratenr, icepap_driver.addr, icepap_driver.currentCfg.getAttribute("VER"))
        if self.icepap_driver.currentCfg.signature:
            aux = self.icepap_driver.currentCfg.signature.split('_')
            description = description + "Signed on %s %s" % (aux[0], time.ctime(float(aux[1])))
        else:
            self._mainwin.addDriverToSign(self.icepap_driver)
            description = description + "Current configuration not signed"
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
        self._connectHighlighting()
        if self.ui.historicWidget.isVisible():
            self.ui.historicWidget.fillData(self.icepap_driver)
    
    def _connectWidgetToSignalMap(self, widget):
        self.signalMapper.setMapping(widget, widget)
        if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("valueChanged (const QString&)"), self.signalMapper, QtCore.SLOT("map()"))
        elif isinstance(widget, QtGui.QCheckBox):
            QtCore.QObject.connect(widget, QtCore.SIGNAL("stateChanged(int)"), self.signalMapper, QtCore.SLOT("map()"))
    
    def _setWidgetValue(self, widget, value, default=True):
        try:
            if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
                widget.setValue(float(value))
                if default:
                    widget.defaultvalue = widget.value()
            elif isinstance(widget, QtGui.QCheckBox):
                state = value == "1"
                if default:
                    widget.defaultvalue = state 
                widget.setChecked(state)
        except:
            print "error in _setWidgetValue"
    
    def _getWidgetValue(self, widget):
        try:
            if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
                return widget.value()
            elif isinstance(widget, QtGui.QCheckBox):
                if widget.isChecked():
                    return 1
                else:
                    return 0
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
        # First get modified items in main section
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
        self.configureSignals()
        if values_ok and len(new_values) > 0:
            
            ok = self._manager.saveValuesInIcepap(self.icepap_driver, new_values)
            
            if ok:
                self.fillData(self.icepap_driver)
                self.ui.btnUndo.setEnabled(True)
                self._disconnectHighlighting()
                self._connectHighlighting()
                #self._mainwin.addDriverToSign(self.icepap_driver)                
            else:
                MessageDialogs.showWarningMessage(self, "Driver configuration", "Error saving configuration")
        elif not values_ok:
            MessageDialogs.showWarningMessage(self, "Driver configuration", "Wrong parameter format")
    
    def loadPredefinedSignalCfg(self, cfg_name):
        if self.inout_cfgs.has_key(str(cfg_name)):
            self.resetSignalsTab()
            cfg_list = self.inout_cfgs[str(cfg_name)]
            for cfg in cfg_list:
                type = cfg[0]
                name = cfg[1]
                if type == "input":
                    self.loadInputSignalCfg(name, cfg[2])
                elif type == "output":
                    self.loadOutputSignalCfg(name, cfg[2])
                elif type == "counter":
                    self.loadCounterSignalCfg(name, cfg[2])

    def loadInputSignalCfg(self, name, cfg):
        getattr(self.ui, "chb"+name).setChecked(True)        
        getattr(self.ui, "cb"+name+"Mode").setCurrentIndex(cfg[0])
        getattr(self.ui, "cb"+name+"Edge").setCurrentIndex(cfg[1])
        getattr(self.ui, "cb"+name+"Dir").setCurrentIndex(cfg[2])
    
    def loadOutputSignalCfg(self, name, cfg):
        getattr(self.ui, "chb"+name).setChecked(True)        
        getattr(self.ui, "cb"+name+"Src").setCurrentIndex(cfg[0])
        getattr(self.ui, "cb"+name+"Mode").setCurrentIndex(cfg[1])
        getattr(self.ui, "cb"+name+"Edge").setCurrentIndex(cfg[2])
        getattr(self.ui, "cb"+name+"Dir").setCurrentIndex(cfg[3])
        getattr(self.ui, "cb"+name+"Pulse").setCurrentIndex(cfg[4])
        
    def loadCounterSignalCfg(self, name, cfg):
        getattr(self.ui, "chb"+name).setChecked(True)        
        getattr(self.ui, "cb"+name+"Src").setCurrentIndex(cfg[0])
            
    def configureSignals(self):
        
        # Configure Inputs        
        if self.ui.chbInPos.isChecked():
            mode = self.ui.cbInPosMode.currentIndex()
            edge = self.ui.cbInPosEdge.currentIndex()
            dir = self.ui.cbInPosDir.currentIndex()
            self._manager.configureInputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.InPos, mode, edge, dir)
        
        if self.ui.chbEncIn.isChecked():
            mode = self.ui.cbEncInMode.currentIndex()
            edge = self.ui.cbEncInEdge.currentIndex()
            dir = self.ui.cbEncInDir.currentIndex()
            self._manager.configureInputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.EncIn, mode, edge, dir)
        
        if self.ui.chbSyncIn.isChecked():
            mode = self.ui.cbSyncInMode.currentIndex()
            edge = self.ui.cbSyncInEdge.currentIndex()
            dir = self.ui.cbSyncInDir.currentIndex()
            self._manager.configureInputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.SyncIn, mode, edge, dir)
        
        # Configure Outputs
        if self.ui.chbSyncOut.isChecked():
            mode = self.ui.cbSyncOutMode.currentIndex()
            src = self.ui.cbSyncOutSrc.currentIndex()
            edge = self.ui.cbSyncOutEdge.currentIndex()
            dir = self.ui.cbSyncOutDir.currentIndex()
            pulse = self.ui.cbSyncOutPulse.currentIndex()
            self._manager.configureOutputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.SyncOut, src, mode, edge, dir, pulse)
        
        if self.ui.chbOutPos.isChecked():
            src = self.ui.cbOutPosSrc.currentIndex()
            mode = self.ui.cbOutPosMode.currentIndex()
            edge = self.ui.cbOutPosEdge.currentIndex()
            dir = self.ui.cbOutPosDir.currentIndex()
            pulse = self.ui.cbOutPosPulse.currentIndex()
            self._manager.configureOutputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.OutPos, src, mode, edge, dir, pulse)
        
        
        # Configure Counters
        if self.ui.chbTarget.isChecked():
            src = self.ui.cbTargetSrc.currentIndex()
            self._manager.setCounterSource(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignalSrc.Target, src)
            
        
        if self.ui.chbAuxPos1.isChecked():
            src = self.ui.cbAuxPos1Src.currentIndex()
            self._manager.setCounterSource(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignalSrc.AuxPos1, src)
        
        if self.ui.chbAuxPos2.isChecked():
            src = self.ui.cbAuxPos2Src.currentIndex()
            self._manager.setCounterSource(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignalSrc.AuxPos2, src)
        
        self.configureAuxSignals()
    
    def configureSignals(self):
        # Configure Aux Inputs        
        if self.ui.chbInPosAux.isChecked():
            polarity = self.ui.cbInPosPol.currentIndex()
            self._manager.configureAuxInputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.InPosAux, polarity)
        
        if self.ui.chbEncAux.isChecked():
            polarity = self.ui.cbEncAuxPol.currentIndex()
            self._manager.configureAuxInputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.EncAux, polarity)
        
        if self.ui.chbLimitPos.isChecked():
            polarity = self.ui.cbLimitPosPol.currentIndex()
            self._manager.configureAuxInputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.LimitPos, polarity)
        
        if self.ui.chbLimitNeg.isChecked():
            polarity = self.ui.cbLimitNegPol.currentIndex()
            self._manager.configureAuxInputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.LimitNeg, polarity)
        
        if self.ui.chbHome.isChecked():
            polarity = self.ui.cbHomePol.currentIndex()
            self._manager.configureAuxInputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.Home, polarity)
        
        if self.ui.chbSyncAuxIn.isChecked():
            polarity = self.ui.cbSyncAuxInPol.currentIndex()
            self._manager.configureAuxInputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.SyncAuxIn, polarity)
        
        # Configure Aux Inputs        
        if self.ui.chbSyncAuxOut.isChecked():
            polarity = self.ui.cbSyncAuxOutPol.currentIndex()
            src = self.ui.cbSyncAuxOutSrc.currentIndex()
            self._manager.configureAuxOutputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.SyncAuxOut, src, polarity)
        
        if self.ui.chbOutPosAux.isChecked():
            polarity = self.ui.cbOutPosAuxPol.currentIndex()
            src = self.ui.cbOutPosAuxSrc.currentIndex()
            self._manager.configureAuxOutputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.OutPosAux, src, polarity)
               
        if self.ui.chbInfoA.isChecked():
            polarity = self.ui.cbInfoAPol.currentIndex()
            src = self.ui.cbInfoASrc.currentIndex()
            self._manager.configureAuxOutputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.InfoA, src, polarity)
        
        if self.ui.chbInfoB.isChecked():
            polarity = self.ui.cbInfoBPol.currentIndex()
            src = self.ui.cbInfoBSrc.currentIndex()
            self._manager.configureAuxOutputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.InfoB, src, polarity)
        
        if self.ui.chbInfoC.isChecked():
            polarity = self.ui.cbInfoCPol.currentIndex()
            src = self.ui.cbInfoCSrc.currentIndex()
            self._manager.configureAuxOutputSignal(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignal.InfoC, src, polarity)
        
           
    def btnUndo_on_click(self):
        self._manager.undoDriverConfiguration(self.icepap_driver)
        self.fillData(self.icepap_driver)
        if not self.icepap_driver.hasUndoList():
            self.ui.btnUndo.setEnabled(False)    
    
    def Historic_on_click(self):
        MessageDialogs.showWarningMessage(self, "HistoricCfg", "Historic configurations are in a implmentation upgrade \n")
        return
        dlg = DialogHistoricCfg(self, self.icepap_driver)
        dlg.exec_()
        if dlg.result():
            self.addNewCfg(dlg.loadcfg)
    
    def btnTemplates_on_click(self):
        dlg = DialogTemplate(self, self.icepap_driver)
        dlg.exec_()
        if dlg.result():
            self.addNewCfg(dlg.loadcfg)
    
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
            self.getMotionValues()
            self.inMotion = -1
            self.status = -1
            #self._manager.enableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
            self.updateTestStatus()
            self.refreshTimer.start(1500)
        
    def stopTesting(self):
        if not self.icepap_driver is None:
            self.refreshTimer.stop()
            #self._manager.disableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
            self.setLedsOff()
    
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
        self.ui.sbFactor.setValue(1)
        
    def updateTestStatus(self):
        (disabled, moving, switches, position) = self._manager.getDriverTestStatus(self.icepap_driver.icepap_name, self.icepap_driver.addr)
        self.StepSize = self.ui.sbFactor.value()           
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
        if self.status <> disabled:
            if disabled == 0:
                self.ui.LedError.changeColor(Led.GREEN)
                self.ui.btnEnable.setText("disable")
                self.ui.btnEnable.setChecked(True)
                self.ui.LedError.on()
            else:
                self.ui.LedError.changeColor(Led.RED)
                self.ui.LedError.on()
                self.ui.btnEnable.setText("enable")
                self.ui.btnEnable.setChecked(False)
        
        self.status = disabled
            
            
        position =  position / self.StepSize
        if int(position) == 0:
            self.ui.LedHome.on()
        else:
            self.ui.LedHome.off()
        if switches == 0:
            self.ui.LedLimitNeg.off()
            self.ui.LedLimitPos.off()
        elif switches == 2:
            self.ui.LedLimitNeg.on()
            self.ui.LedLimitPos.off()
        elif switches == 4:
            self.ui.LedLimitPos.on()
            self.ui.LedLimitNeg.off()
        elif switches == 6:
            self.ui.LedLimitPos.on()
            self.ui.LedLimitNeg.on()            
        self.ui.LCDPosition.display(position)

                
    def btnGO_on_click(self):
        new_position = self.ui.txtMvAbsolute.text()
        #try:
        new_position = float(new_position)
        
        new_position = new_position * self.StepSize
        (disabled, moving, switches, position) = self._manager.getDriverTestStatus(self.icepap_driver.icepap_name, self.icepap_driver.addr)

        
        if ((new_position-float(new_position)) >= 0.5):
            new_position = new_position + 0.5
    
        steps = int(position) - new_position
        
        
        direction = steps < 0
        if steps != 0:
            #self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
            self._manager.moveDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr, abs(int(steps)), direction)
        #except:
        #    MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")
            
    def btnGORelativePos_on_click(self):
        distance = self.ui.txtGORelative.text()
        try:
            direction = True
            distance = abs(float(distance))
            distance = distance * self.StepSize
            if ((distance-float(distance)) >= 0.5):
                distance = distance + 0.5
        
            steps = distance

            if steps != 0:
                #self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
                self._manager.moveDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr, abs(int(steps)), direction)

        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")
            
    
    def btnGORelativeNeg_on_click(self):
        distance = self.ui.txtGORelative.text()
        try:
            direction = False
            distance = abs(float(distance))
            distance = distance * self.StepSize
            if ((distance-float(distance)) >= 0.5):
                distance = distance + 0.5
        
            steps = distance
	    
            if steps != 0:
                #self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
                self._manager.moveDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr, abs(int(steps)), direction)

        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")
        
    def btnStopMotor_on_click(self):
        self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
        
    def BtnSetPos_on_click(self):
        self._manager.setDriverPosition(self.icepap_driver.icepap_name, self.icepap_driver.addr, self.ui.sbPosition.value())
    
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
        
    def endisDriver(self, bool):
         if bool:
            self.ui.btnEnable.setText("disable")
            self._manager.enableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
         else:
            self.ui.btnEnable.setText("enable")
            self._manager.disableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
        

    # ---------------------- Historic Widget -------------------
    def showHistoricWidget(self):
        self.ui.frame_test.hide()
        self.ui.historicWidget.show()
        self.ui.historicWidget.fillData(self.icepap_driver)
    def hideHistoricWidget(self):
        self.ui.historicWidget.hide()
        self.ui.frame_test.show()