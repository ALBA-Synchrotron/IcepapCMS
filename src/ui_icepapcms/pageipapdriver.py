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
        self._createTableView()
        self._manager = MainManager()
        self.ui.btnUndo.setEnabled(False)
        self.refreshTimer = Qt.QTimer(self)
        self.signalConnections()
        self.setLedsOff()
        self.icepap_driver = None
        self.inMotion = -1
        self.status = -1  
        
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
        
        
        self.ui.tabWidget.setCurrentIndex(0)
        
        #self.ui.txtDriverName.setValidator(QtGui.QIntValidator(1,100,self))
         

    
    def signalConnections(self):
        QtCore.QObject.connect(self.ui.btnApplyCfg,QtCore.SIGNAL("clicked()"),self.btnApplyCfg_on_click)
        QtCore.QObject.connect(self.ui.btnHistoric,QtCore.SIGNAL("clicked()"),self.Historic_on_click)
        QtCore.QObject.connect(self.ui.btnTemplates,QtCore.SIGNAL("clicked()"),self.btnTemplates_on_click)
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
         
# ------------------------------  Configuration ----------------------------------------------------------    
    def _createTableView(self):
        self.var_dict = {}
        doc = minidom.parse(self.config_template)
        root  = doc.documentElement
        row = 0
        nsection = 0
        for section in root.getElementsByTagName("section"):
            if section.nodeType == Node.ELEMENT_NODE:
                    section_name =  section.attributes.get('name').value
            self.addSectionTab(section_name)
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    self.sectionTables[nsection].insertRow(row)
                    parname =  pars.attributes.get('name').value
                    parname = parname.strip()
                    self.var_dict[parname] = [nsection, row]
                    self._addItemToTable(nsection, row, 0, parname, False)
                    partype =  pars.attributes.get('type').value
                    partype = partype.strip()
                    parmin =  pars.attributes.get('min').value
                    parmin = parmin.strip()
                    parmax =  pars.attributes.get('max').value
                    parmax = parmax.strip()
                    self._addWidgetToTable(nsection, row, 2, partype, parmin, parmax)
                    pardesc = self._getText(pars.getElementsByTagName("description")[0].firstChild)
                    self._addItemToTable(nsection, row, 3, pardesc, False)
                    row = row + 1
            row = 0
            nsection = nsection + 1
        

    def addSectionTab(self, section_name):
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
        self.ui.tabWidget.setCurrentIndex(0)
        self.resetSignalsTab()
        self.icepap_driver = icepap_driver
        self.ui.txtDriverName.setText(self.icepap_driver.name)
        self.ui.txtDriverNemonic.setText(self.icepap_driver.nemonic)
        for name, value in icepap_driver.currentCfg.parList.items():
            if self.var_dict.has_key(name):
                [nsection, row] = self.var_dict[name]
                self._addItemToTable(nsection, row, 1, value, False)
                self.sectionTables[nsection].cellWidget(row,2).setText("")
                #self._addItemToTable(nsection, row, 2, "", True)
        
    
    def addNewCfg(self, cfg):
        #self.ui.toolBox.setCurrentIndex(0)
        for name, value in cfg.parList.items():
            if self.var_dict.has_key(name):
                [nsection, row] = self.var_dict[name]
                self.sectionTables[nsection].cellWidget(row,2).setText(value)
                #self._addItemToTable(nsection, row, 2, value, True)

        

    def _getText(self, node):
        rc = ""
        if node != None:
                rc = str(node.data)
        return rc              
    

        
    def btnApplyCfg_on_click(self):
        self.icepap_driver.name = str(self.ui.txtDriverName.text())
        self.icepap_driver.nemonic = str(self.ui.txtDriverNemonic.text())
        new_values = []
        values_ok = True
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
            else:
                MessageDialogs.showWarningMessage(self, "Driver configuration", "Error saving configuration")
        elif not values_ok:
            MessageDialogs.showWarningMessage(self, "Driver configuration", "Wrong parameter format")
    
    def configureSignals(self):
        
        # Configure Inputs
        
        if self.ui.chbInPos.isChecked():
            mode = self.ui.cbInPosMode.currentIndex()
            edge = self.ui.cbInPosEdge.currentIndex()
            dir = self.ui.cbInPosDir.currentIndex()
            print "inpos here"
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
            src = self.ui.cbAuxPos1.currentIndex()
            self._manager.setCounterSource(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignalSrc.AuxPos1, src)
        
        if self.ui.chbAuxPos2.isChecked():
            src = self.ui.cbAuxPos2.currentIndex()
            self._manager.setCounterSource(self.icepap_driver.icepap_name, self.icepap_driver.addr, IcepapSignalSrc.AuxPos2, src)
        
        
    def btnUndo_on_click(self):
        self._manager.undoDriverConfiguration(self.icepap_driver)
        self.fillData(self.icepap_driver)
        if not self.icepap_driver.hasUndoList():
            self.ui.btnUndo.setEnabled(False)    
    
    def Historic_on_click(self):
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
                    [nsection, row] = self.var_dict[parname]
                    #self._addItemToTable(nsection, row, 2, parval, True)
                    self.sectionTables[nsection].cellWidget(row,2).setText(parval)
                    
                     
                    
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
        try:
            new_position = float(new_position)
            
            new_position = new_position * self.StepSize
            (status, switches, position) = self._manager.getDriverTestStatus(self.icepap_driver.icepap_name, self.icepap_driver.addr)
            position =  float(position)
            
            if ((new_position-float(new_position)) >= 0.5):
                new_position = new_position + 0.5
        
            steps = float(position) - new_position
            
            
            direction = steps < 0
            if steps != 0:
                self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
                self._manager.moveDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr, abs(int(steps)), direction)
        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")
            
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
                self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
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
                self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
                self._manager.moveDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr, abs(int(steps)), direction)

        except:
            MessageDialogs.showWarningMessage(self, "Driver testing", "Wrong parameter format")
        
    def btnStopMotor_on_click(self):
        self._manager.stopDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
        
    def BtnSetPos_on_click(self):
        self._manager.setDriverPosition(self.icepap_driver.icepap_name, self.icepap_driver.addr, self.ui.sbPosition.value())
    
    def endisDriver(self, bool):
         if bool:
            self.ui.btnEnable.setText("disable")
            self._manager.enableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
         else:
            self.ui.btnEnable.setText("enable")
            self._manager.disableDriver(self.icepap_driver.icepap_name, self.icepap_driver.addr)
        
