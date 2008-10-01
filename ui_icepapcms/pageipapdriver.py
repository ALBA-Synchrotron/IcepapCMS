from PyQt4 import QtCore, QtGui, Qt
from ui_pageipapdriver import Ui_PageiPapDriver
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
from historiccfgwidget import HistoricCfgWidget

class PageiPapDriver(QtGui.QWidget):
    """ Widget that manages all the information related to an icepap driver. Configuration, testing and historic configurations """
    
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
        self.unknown_var_dict = {}
        
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

        # PALETTES TO HIGHLIGHT WIDGETS
        white_brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        grey_brush =  QtGui.QBrush(QtGui.QColor(239,235,231))
        yellow_brush = QtGui.QBrush(QtGui.QColor(255,255,0))
        salmon_brush = QtGui.QBrush(QtGui.QColor(255,206,162))
        
        self.base_white_palette = QtGui.QPalette()
        self.base_yellow_palette = QtGui.QPalette()
        self.base_salmon_palette = QtGui.QPalette()

        self.button_grey_palette = QtGui.QPalette()
        self.button_yellow_palette = QtGui.QPalette()
        self.button_salmon_palette = QtGui.QPalette()
        
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

        self.dbStartupConfig = None


        
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
        
        #self.ui.sahboxlayout3 = QtGui.QHBoxLayout(self.ui.tab_2)
        ##self.ui.sahboxlayout3.setMargin(9)
        ##self.ui.sahboxlayout3.setSpacing(6)
        #self.ui.sahboxlayout3.setObjectName("sahboxlayout3")
        #self.ui.sa3 = QtGui.QScrollArea(self.ui.tab_2) 
        ##self.ui.sa3.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter)
        #self.ui.driver_widget.setParent(None)
        #self.ui.sa3.setWidget(self.ui.driver_widget)
        #self.ui.sa3.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
        #self.ui.sa3.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
        #self.ui.sa3.setFrameStyle(QtGui.QFrame.NoFrame)
        #self.ui.sahboxlayout3.addWidget(self.ui.sa3)
        

        
        #self.ui.txtDriverName.setValidator(QtGui.QIntValidator(1,100,self))
        
    def signalConnections(self):
        QtCore.QObject.connect(self.ui.btnSendCfg,QtCore.SIGNAL("clicked()"),self.btnSendCfg_on_click)
        QtCore.QObject.connect(self.ui.btnSaveCfg,QtCore.SIGNAL("clicked()"),self.btnSaveCfg_on_click)
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
        ############################################
        #DEBUG GCUNI
        ############################################
        #
        #param = ""
        #if len(self.var_dict) > 0:
        #    for name, dict_widget in self.var_dict.items():
        #        if dict_widget == widget:
        #            param = name
        #            break
        #if param == "" and len(self.test_var_dict) > 0:
        #    for name, dict_widget in self.test_var_dict.items():
        #        if dict_widget == widget:
        #            param = name
        #            break
        #print param+" db("+str(startupConfig.getParameter(param))+") widget("+str(self._getWidgetValue(widget))+")"
        
        if not isinstance(widget,QtGui.QWidget):
            return

        ###
        # Tiago's idea to try to highlight at better speed...
        # def threadQSpinBoxPE(self,event):
        #     self.setPalette(self.pal)
        #     QtGUI.QSpinBox.paintEvent(event)
        # widget.pal = self.base_yellow_palette
        # widget.paintEvent =  threadQSpinBoxPE
        # widget.repaint()
        ###

        highlight = False
        param = str(widget.objectName())
        if param == "txtDriverName":
            param = "IPAPNAME"
        dbvalue = self.dbStartupConfig.getParameter(unicode(param),in_memory=False)
        wvalue = self._getWidgetValue(widget)

        #print "DB("+str(dbvalue)+") W("+str(wvalue)+")"
        try:
            if isinstance(widget, QtGui.QDoubleSpinBox) or isinstance(widget, QtGui.QSpinBox):
                if widget.defaultvalue != widget.value():
                    highlight = True
                    widget.setPalette(self.base_yellow_palette)
                elif abs(float(wvalue) - float(dbvalue)) > 0.01:
                    highlight = True
                    widget.setPalette(self.base_salmon_palette)
                
            elif isinstance(widget, QtGui.QCheckBox):
                if widget.defaultvalue != widget.isChecked():
                    highlight = True
                    widget.setPalette(self.base_yellow_palette)
                elif wvalue != dbvalue:
                    highlight = True
                    widget.setPalette(self.base_salmon_palette)
            
            elif isinstance(widget, QtGui.QComboBox):
                dbvalue = dbvalue.upper()
                wvalue = wvalue.upper()
                if widget.defaultvalue == None:
                    widget.defaultvalue = ""
                if widget.defaultvalue.upper() != str(widget.currentText()).upper():
                    highlight = True
                    widget.setPalette(self.button_yellow_palette)
                elif wvalue != dbvalue:
                    highlight = True
                    widget.setPalette(self.button_salmon_palette)
            
            elif isinstance(widget, QtGui.QLineEdit):
                if dbvalue == None:
                    dbvalue = ""
                dbvalue = dbvalue.upper()
                wvalue = wvalue.upper()
                if widget.defaultvalue == None:
                    widget.defaultvalue = ""
                wdvalue = widget.defaultvalue

                if wdvalue.upper() != wvalue:
                    highlight = True
                    widget.setPalette(self.base_yellow_palette)
                elif wvalue != dbvalue:
                    highlight = True
                    widget.setPalette(self.base_salmon_palette)

        except:
            pass
        
        if highlight:
            if widget.isTest:
                if not widget in self.test_var_modified:
                    self.test_var_modified.append(widget)
            else:
                if not widget in self.main_modified:
                    self.main_modified.append(widget)
        else:
            if widget.isTest:
                if self.test_var_modified.count(widget) > 0:
                    self.test_var_modified.remove(widget)
            else:
                if self.main_modified.count(widget) > 0:
                    self.main_modified.remove(widget)

            if isinstance(widget,QtGui.QComboBox):
                widget.setPalette(self.button_grey_palette)
            else:
                widget.setPalette(self.base_white_palette)


    def _connectHighlighting(self):
        #clear previous state
        self.main_modified = []
        self.test_var_modified = []
        QtCore.QObject.connect(self.signalMapper, QtCore.SIGNAL("mapped(QWidget*)"), self.highlightWidget)
        ### # HIGHLIGHT AGAIN
        for name, [nsection, widget] in self.var_dict.items():
            self.highlightWidget(widget)

        ### highlight the txtDriverName widget
        self.highlightWidget(self.ui.txtDriverName)



    
    def _disconnectHighlighting(self):
        for nsection, widget in self.var_dict.itervalues():
            if nsection == 0:
                if isinstance(widget,QtGui.QComboBox):
                    widget.setPalette(self.button_grey_palette)
                else:
                    widget.setPalette(self.base_white_palette)
        aux = []
        for widget in self.test_var_dict.itervalues():
            if type(widget) == type(aux):
                for w in widget:
                    if isinstance(w,QtGui.QComboBox):
                        w.setPalette(self.button_grey_palette)
                    else:
                        w.setPalette(sefl.base_white_palette)
            else:
                if isinstance(widget,QtGui.QComboBox):
                    widget.setPalette(self.button_grey_palette)
                else:
                    widget.setPalette(self.base_white_palette)

        QtCore.QObject.disconnect(self.signalMapper, QtCore.SIGNAL("mapped(QWidget*)"),self.highlightWidget)
          
# ------------------------------  Configuration ----------------------------------------------------------    
    def _readConfigTemplate(self):
        """ Reads the configuration template file to map the different widgets of the user interface,
        with the configuration parameters"""
        
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
                    # SHOULD I USE pardesc as the tooltip?
                    if inMainSection or inTestSection:
                        widget = None
                        try:
                            widget = getattr(self.ui, parid)
                        except:
                            pass

                        if widget == None:
                            print "THE GUI ELEMENT '"+str(parid)+"' DOES NOT EXIST"
                        else:
                            widget.setToolTip(pardesc)
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
        return self.ui.tabWidget.indexOf(tab)
        

           
    def _addItemToTable(self, section, row, column, text, editable):
        item = QtGui.QTableWidgetItem()
        item.setText(text)
        if not editable:
            item.setFlags(Qt.Qt.ItemIsSelectable)
        else:
            item.setTextColor(QtGui.QColor(Qt.Qt.red))
        table = self.sectionTables[section]
        
        table.setItem(row, column, item)
        
    def _addWidgetToTable(self, section, row, column, widget_type, min, max,unknownTab=False):
        table = self.sectionTables[section]
        #le = QtGui.QLineEdit(table)
        widget = QtGui.QLineEdit()
        if widget_type == "INTEGER":
            widget = QValidateLineEdit(table,QValidateLineEdit.INTEGER,min,max)
        elif widget_type == "DOUBLE":
            widget = QValidateLineEdit(table,QValidateLineEdit.DOUBLE,min,max)
        elif widget_type == "QCOMBOSTRING":
            options = table.item(row,3).text()
            options = options.replace("[","")
            options = options.replace("]","")
            options = options.replace("'","")
            options = options.replace(" ","")
            options_list = options.split(",")
            widget = QtGui.QComboBox(table)
            widget.insertItems(0,options_list)
            # SET THE DESCRIPTION TO "LIST value"
            table.item(row,3).setText("LIST value")
            

        widget.defaultvalue = None
        widget.isTest = False
            
        table.setCellWidget(row, column, widget)
        self._connectWidgetToSignalMap(widget)

        if unknownTab:
            parname = str(table.item(row,0).text())
            widget.setObjectName(parname)
            widget_value = str(table.item(row,1).text())
            widget.defaultvalue = widget_value
            if widget_type == "QCOMBOSTRING":
                widget.setCurrentIndex(widget.findText(widget_value))
            else:
                widget.setText(widget_value)

            self.unknown_var_dict[parname] = (widget_type,widget)

    
    def fillData(self, icepap_driver):
        """ TO-DO STORM review"""

        QtGui.QApplication.instance().setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        #self.ui.tabWidget.setCurrentIndex(0)
        self._disconnectHighlighting()
        #self.resetSignalsTab()
        self.icepap_driver = icepap_driver
        description = "Icepap: %s  -  Crate: %s  -  Addr: %s  -  Firmware version: %s\n" % (icepap_driver.icepapsystem_name, icepap_driver.cratenr, icepap_driver.addr, icepap_driver.current_cfg.getParameter("VER", True))
        if self.icepap_driver.current_cfg.signature:
            signature = self.icepap_driver.current_cfg.signature
            description = description + "Last signature '%s' " % signature
            try:
                aux = signature.split('_')
                host = aux[0]
                hex_epoch = aux[1]
                description = description + "Host: '%s' Date: '%s'" % (host,datetime.datetime.fromtimestamp(int(hex_epoch,16)).ctime())
            except:
                pass
        else:            
            description = description + "Current configuration not signed"

        if self.icepap_driver.mode == IcepapMode.CONFIG:
            self._mainwin.addDriverToSign(self.icepap_driver)
        self.ui.txtDescription.setText(description)

        # THIS IS OVERWRITTEN LATER
        #self.ui.txtDriverName.setText(self.icepap_driver.name)
        #self.ui.txtDriverNemonic.setText(self.icepap_driver.nemonic)


        # BEFORE STARTING WITH PARAMETERS, IN CASE THE UNKNOWN TAB EXIST, IT SHOULD BE CLEARED
        unknown = "Unknown"
        tab_unknown = "tab_"+unknown
        for i in range(self.ui.tabWidget.count()):
            widget = self.ui.tabWidget.widget(i)
            if str(widget.objectName()) == tab_unknown:
                self.sectionTables[i].setRowCount(0)
                break


        for name, value in icepap_driver.current_cfg.toList():
            if self.var_dict.has_key(name):
                [nsection, element] = self.var_dict[name]
                if nsection == 0:
                    # In main tab
                    self._setWidgetValue(element, value)
                else:
                    self._addItemToTable(nsection, element, 1, value, False)
                    self.sectionTables[nsection].cellWidget(element,2).setText("")
                #self._addItemToTable(nsection, row, 2, "", True)
            else:
                cfginfo = IcepapController().icepap_cfginfos[self.icepap_driver.icepapsystem_name][self.icepap_driver.addr].get(name)
                if cfginfo != None:
                    indexUnknownTab = -1
                    for i in range(self.ui.tabWidget.count()):
                        widget = self.ui.tabWidget.widget(i)
                        if str(widget.objectName()) == tab_unknown:
                            indexUnknownTab = i
                            break
                    
                    if indexUnknownTab == -1:
                        indexUnknownTab = self._addSectionTab(unknown)
                
                    unknown_table_widget = self.sectionTables[indexUnknownTab]

                    row = unknown_table_widget.rowCount()
                    unknown_table_widget.insertRow(row)
                    self._addItemToTable(indexUnknownTab, row, 0, name, False)
                    self._addItemToTable(indexUnknownTab, row, 1, value, False)
                    partype = "STRING"
                    pardesc = str(cfginfo)
                    if len(cfginfo) > 0:
                        if "INTEGER" == cfginfo[0]:
                            partype = "INTEGER"
                            pardesc = "INTEGER value"
                        elif "FLOAT" == cfginfo[0]:
                            partype = "DOUBLE"
                            pardesc = "DOUBLE value"
                        else:
                            partype = "QCOMBOSTRING"
                    self._addItemToTable(indexUnknownTab, row, 3, pardesc, False)
                    # DESCRIPTION (col 3) BEFORE WIDGET (col 2) TO BE ABLE TO CREATE QCOMBOXES
                    # THE DESCRIPTION IS USED TO PARSE THE VALUES
                    self._addWidgetToTable(indexUnknownTab, row, 2, partype, 0, 9999999,unknownTab=True)


        # get testing values
        self.startTesting()
        if not (self.status == -1 or self.status == 1):
            result = self._manager.readIcepapParameters(self.icepap_driver.icepapsystem_name,self.icepap_driver.addr, self.test_var_dict.keys())
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
                else:
                    print "FOUND THE UNKNOWN PARAMETER '"+str(name)+"'"
           
        # SET THE CORRECT DRIVER NAME
        self.icepap_driver.name = unicode(self.ui.txtDriverName.text())
        self.icepap_driver.current_cfg.setParameter("IPAPNAME",self.icepap_driver.name)

        
        # CHECK THE ACTIVE FLAG
        # IN CASE OF NO-ACTIVE DRIVER,
        # UNCHECK THE ACTIVE CFG PARAMETER
        activeStatus = IcepapController().getDriverActiveStatus(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
        # WHY SOMETIMES THE ANSWER OF THE DRIVER IS '???'?
        if activeStatus.upper() == "NO":
            self.ui.ACTIVE.setChecked(False)


        # PREPARE DATA FOR HIGHLIGHTING
        dbIcepapSystem = StormManager().getIcepapSystem(self.icepap_driver.icepapsystem_name)
        self.dbStartupConfig = dbIcepapSystem.getDriver(self.icepap_driver.addr,in_memory=False).startup_cfg
        self._connectHighlighting()

        if self.ui.historicWidget.isVisible():
            self.ui.historicWidget.fillData(self.icepap_driver)

        QtGui.QApplication.instance().restoreOverrideCursor()


    
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
                widget.clear()
                param = str(widget.objectName())
                # WORKAROUND FOR QCOMBOBOX WIDGETS IN THE TEST TAB"
                if param in ("TINFOASRC","TINFOAPOL","TINFOBSRC","TINFOBPOL","TINFOCSRC","TINFOCPOL","TINDEXER"):
                    param = param[1:]
                controller = IcepapController()
                driver_cfginfo = controller.icepap_cfginfos[self.icepap_driver.icepapsystem_name][self.icepap_driver.addr]
                options = driver_cfginfo.get(param)
                if options != None:
                    for option in options:
                        widget.addItem(QtCore.QString(option))
                widget.setCurrentIndex(widget.findText(str(value), QtCore.Qt.MatchFixedString))

                if default:
                    widget.defaultvalue = str(value)
            elif isinstance(widget, QtGui.QLineEdit):
                widget.setText(str(value))
                if default:
                    widget.defaultvalue = str(value)
                
        except:           
            pass
            #print "_setWidgetValue():", sys.exc_info() , " " , value 
    
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
        for name, value in cfg.toList():
            if self.var_dict.has_key(name):
                [nsection, element] = self.var_dict[name]
                if nsection == 0:
                    self._setWidgetValue(element, value, False) 
                else:
                    self.sectionTables[nsection].cellWidget(element,2).setText(value)
                    #self._addItemToTable(nsection, row, 2, value, True)

        # THE ICEPAP NAME IN THE CONFIG SHOULD BE RESTORED
        try:
            ipap_name = cfg.getParameter(unicode("IPAPNAME"))
            self.ui.txtDriverName.setText(ipap_name)
        except:
            #print "oups, this config had not the ipapname yet..."
            pass
        

        

    def _getText(self, node):
        rc = ""
        if node != None:
                rc = str(node.data)
        return rc              
    

    def btnSendCfg_on_click(self):
        # SHOULD NOT CHANGE THE DRIVER NAME
        #self.icepap_driver.name = unicode(self.ui.txtDriverName.text())
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
                widget = tableWidget.cellWidget(row,2)
                val = ""
                if isinstance(widget,QValidateLineEdit):
                   val = widget.text()
                elif isinstance(widget,QtGui.QComboBox):
                    val = str(widget.currentText()).upper()
                if val != "":
                    try:
                        name = str(tableWidget.item(row,0).text())
                        if isinstance(widget, QValidateLineEdit):
                            if widget.type == QValidateLineEdit.INTEGER:
                                val = int(widget.text())
                            elif widget.type == QValidateLineEdit.DOUBLE:
                                val = float(widget.text())
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
            
            self._manager.writeIcepapParameters(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, test_values_list)

        #self.configureSignals()
        if save_ok and test_values_ok:
            self.fillData(self.icepap_driver)
            self.ui.btnUndo.setEnabled(True)
        else:
            MessageDialogs.showWarningMessage(self, "Driver configuration", "Error saving configuration")
        

    def btnSaveCfg_on_click(self):
        self._mainwin.actionSaveConfig()
        
    def btnUndo_on_click(self):
        self._manager.undoDriverConfiguration(self.icepap_driver)
        self.fillData(self.icepap_driver)
        if not self.icepap_driver.hasUndoList():
            self.ui.btnUndo.setEnabled(False)    
    
    def btnRestore_on_click(self):
        self.addNewCfg(self.icepap_driver.current_cfg)
        #.fillData(self.icepap_driver)
        
    
    def doImport(self):
        try:
            fn = QtGui.QFileDialog.getOpenFileName(self)
            if fn.isEmpty():
                return
            filename = str(fn)
            self.fillFileData(filename)
        except Exception,e:
            MessageDialogs.showWarningMessage(self, "File", "Error reading file\n")
            print "exception: "+str(e)
    
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
                    if self.var_dict.has_key(parname):
                        [nsection, element] = self.var_dict[parname]
                        #self._addItemToTable(nsection, row, 2, parval, True)
                        if nsection == 0:
                            self._setWidgetValue(element, parval) 
                        else:
                            self.sectionTables[nsection].cellWidget(element,2).setText(parval)
                    else:
                        # THE VALUES SHOULD BE FILLED IN THE UNKNOWN TAB IF THE var_dic IS
                        # FILLED CORRECTLY
                        widget_type,widget = self.unknown_var_dict[parname]
                        if widget_type == "QCOMBOSTRING":
                            widget.setCurrentIndex(widget.findText(parval))
                        else:
                            widget.setText(parval)
                        pass
                    
                     
                    
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
        self._disconnectHighlighting()
        self.icepap_driver.signDriver()
        # PREPARE DATA FOR HIGHLIGHTING
        dbIcepapSystem = StormManager().getIcepapSystem(self.icepap_driver.icepapsystem_name)
        self.dbStartupConfig = dbIcepapSystem.getDriver(self.icepap_driver.addr,in_memory=False).current_cfg
        self._connectHighlighting()
               
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
            self.refreshTimer.start(1500)
        
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
            speed = "100"
            self.ui.txtSpeed.setText(speed)
        if acc == "":
            acc = "1"
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
        self.ui.tab_3.setEnabled(False)
    
    def enableAllControl(self):
        self.ui.txtSpeed.setEnabled(True)
        self.ui.txtAcceleration.setEnabled(True)
        
        self.ui.btnGORelativeNeg.setEnabled(True)
        self.ui.btnGORelativePos.setEnabled(True)
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
        (status, power, position) = self._manager.getDriverTestStatus(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, pos_sel, enc_sel)
        
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
        
    
    
    def sliderChanged(self, div):
        if self.ui.sliderJog.isSliderDown() or not self.sliderTimer.isActive():
            self.startJogging(div)
            
    def startJogging(self, div):
        #try:
        if div <> 0:
            if not self.ui.btnEnable.isChecked():
                self._manager.enableDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
            speed = float(self.ui.txtSpeed.text())
            factor = (self.ui.sliderJog.maximum() - abs(div)) + 1 
            speed = int(speed / factor)
            dir = (div > 0)
            self._manager.jogDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, str(speed), dir)
        else:
            self.stopJogging()
        #except:
        #    pass
    
    def stopJogging(self):
        self._manager.jogDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, "0", True)
        #self._manager.stopDriver(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr)
        
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
            self._manager.setDriverPosition(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, pos_sel, position)
        except:
            print "Unexpected error:", sys.exc_info()
            MessageDialogs.showWarningMessage(self, "Set driver position", "Wrong parameter format")
        
    
    def setEncoder(self):
        enc_sel = str(self.ui.cb_enc_sel.currentText()).upper()
        try:
            position = int(self.ui.txtEnc.text())
            self._manager.setDriverPosition(self.icepap_driver.icepapsystem_name, self.icepap_driver.addr, enc_sel, position)
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
        

    # ---------------------- Historic Widget -------------------
    def showHistoricWidget(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.historicWidget.fillData(self.icepap_driver)
        
    def hideHistoricWidget(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    # ---------------------- Motor Types Catalog Widget -------------------
    def setMotorTypeParams(self,motor_type,params):
        for param in params.keys():
            value = params.get(param)
            if self.var_dict.has_key(param):
                [nsection, element] = self.var_dict[param]
                self._setWidgetValue(element, value)
        #print "THE MOTOR TYPE LABEL IS NOT YET IMPLEMENTED. Selected type: '%s'" % motor_type
