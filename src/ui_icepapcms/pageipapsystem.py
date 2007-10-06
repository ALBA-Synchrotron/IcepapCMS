from PyQt4 import QtCore, QtGui, Qt
from qrc_icepapcms import *
from icepapdriver_widget import IcePapDriverWidget
from  lib_icepapcms import IcepapDriver


class PageiPapSystem(QtGui.QWidget):
    def __init__(self, mainwin):
        QtGui.QWidget.__init__(self, None)
        #self.resize(QtCore.QSize(QtCore.QRect(0,0,800,607).size()).expandedTo(self.minimumSizeHint()))
        #sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        #self.setMinimumSize(QtCore.QSize(800,201))
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        #self.setSizePolicy(sizePolicy)
        self._colSize = [94, 94]
        self._rowSize = [74, 200]
        self.mainwin = mainwin       
        self.hboxlayout = QtGui.QVBoxLayout(self)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.cmbIconSize = QtGui.QComboBox()
        self.cmbIconSize.addItems(QtCore.QStringList(["Big icons", "Small Icons"]))
        self.cmbIconSize.setMaximumWidth(100)
        self.hboxlayout.addWidget(self.cmbIconSize)

        self.tableWidget = QtGui.QTableWidget(self)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(0),QtGui.QColor(16,16,16))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(1),QtGui.QColor(226,228,252))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(2),QtGui.QColor(237,237,237))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(3),QtGui.QColor(247,245,243))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(4),QtGui.QColor(119,117,115))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(5),QtGui.QColor(159,157,154))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(6),QtGui.QColor(16,16,16))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(7),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(8),QtGui.QColor(16,16,16))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(9),QtGui.QColor(239,235,231))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(10),QtGui.QColor(239,235,231))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(11),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(12),QtGui.QColor(101,148,235))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(13),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(14),QtGui.QColor(0,0,255))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(15),QtGui.QColor(255,0,255))
        palette.setColor(QtGui.QPalette.Active,QtGui.QPalette.ColorRole(16),QtGui.QColor(247,245,243))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(0),QtGui.QColor(16,16,16))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(1),QtGui.QColor(226,228,252))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(2),QtGui.QColor(237,237,237))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(3),QtGui.QColor(247,245,243))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(4),QtGui.QColor(119,117,115))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(5),QtGui.QColor(159,157,154))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(6),QtGui.QColor(16,16,16))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(7),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(8),QtGui.QColor(16,16,16))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(9),QtGui.QColor(239,235,231))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(10),QtGui.QColor(239,235,231))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(11),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(12),QtGui.QColor(101,148,235))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(13),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(14),QtGui.QColor(0,0,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(15),QtGui.QColor(255,0,255))
        palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.ColorRole(16),QtGui.QColor(247,245,243))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(0),QtGui.QColor(127,125,123))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(1),QtGui.QColor(226,228,252))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(2),QtGui.QColor(237,237,237))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(3),QtGui.QColor(247,245,243))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(4),QtGui.QColor(119,117,115))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(5),QtGui.QColor(159,157,154))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(6),QtGui.QColor(127,125,123))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(7),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(8),QtGui.QColor(127,125,123))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(9),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(10),QtGui.QColor(239,235,231))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(11),QtGui.QColor(0,0,0))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(12),QtGui.QColor(84,123,196))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(13),QtGui.QColor(255,255,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(14),QtGui.QColor(0,0,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(15),QtGui.QColor(255,0,255))
        palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.ColorRole(16),QtGui.QColor(247,245,243))
        self.tableWidget.setPalette(palette)
        self.tableWidget.setObjectName("tableWidget")      
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.hboxlayout.addWidget(self.tableWidget)
        QtCore.QObject.connect(self.cmbIconSize,QtCore.SIGNAL("currentIndexChanged(int)"),self.changeSize)
        self.icepap_system = None

        
    def fillData(self, icepap_system):
        """ TO-DO STORM review"""
        if self.icepap_system == icepap_system:
            self.refresh()
            return
        size = not(self.cmbIconSize.currentIndex())
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setUpdatesEnabled(False)
        self.tableWidget.verticalHeader().setUpdatesEnabled(False)
        
        for i in range(8):
            headerItem = QtGui.QTableWidgetItem()
            headerItem.setText(str(i+1))
            self.tableWidget.setHorizontalHeaderItem(i,headerItem)
            self.tableWidget.horizontalHeader().resizeSection(i,self._colSize[size])
            
            self.tableWidget.horizontalHeader().setResizeMode(i, Qt.QHeaderView.Custom)
            
        self.icepap_system = icepap_system
        self.driverswidgets = {}
        crate = -1
        for driver in icepap_system.getDrivers():
            addr = driver.addr
            print addr
            if driver.cratenr  <> crate:
                crate = driver.cratenr 
                self.tableWidget.insertRow(crate)
                headerItem = QtGui.QTableWidgetItem()
                headerItem.setText("Crate %d" %crate)
                self.tableWidget.setVerticalHeaderItem(crate,headerItem)
                self.tableWidget.verticalHeader().resizeSection(crate,self._rowSize[size])
                self.tableWidget.verticalHeader().setResizeMode(crate, Qt.QHeaderView.Custom)
                for drivernr in range(8):
                    addr = crate*10+ drivernr +1                                           
                    adriver = icepap_system.getDriver(crate*10+ drivernr +1)
                    if not adriver is None:
                        wdriver = IcePapDriverWidget(self, size)
                        wdriver.fillData(adriver)
                        #if not wdriver.fillData(adriver):
                        #    return
                        self.driverswidgets[addr]  = wdriver
                        self.tableWidget.setCellWidget(crate, drivernr, wdriver)
                        QtCore.QObject.connect(wdriver,QtCore.SIGNAL("icepapDoubleClicked(PyQt_PyObject)"),self.driverDoubleclick)
 
            
        self.tableWidget.horizontalHeader().setUpdatesEnabled(True)
        self.tableWidget.verticalHeader().setUpdatesEnabled(True)
    
    def driverDoubleclick(self, driver):
        if not driver is None:
            location = "%s/%d/%d" % (driver.icepap_name, driver.cratenr, driver.drivernr)
            self.mainwin.locationsPrevious.extend(self.mainwin.locationsNext)
            self.mainwin.locationsNext =  []
            self.mainwin.addToPrevious(self.mainwin.currentLocation)
            self.mainwin.treeSelectByLocation(location)
    
            
    def changeSize(self, index):
        self.refresh(not(index))
    
    def refresh(self, size = None):
        
        self.tableWidget.setUpdatesEnabled(False)
        self.tableWidget.horizontalHeader().setUpdatesEnabled(False)
        self.tableWidget.verticalHeader().setUpdatesEnabled(False)
        for col in range(self.tableWidget.columnCount()):
            for row in range(self.tableWidget.rowCount()):
                driver_widget =  self.tableWidget.cellWidget(row, col)
                if not driver_widget is None:
                    if not size == None:
                        driver = driver_widget.getDriver()
                        driver_widget = IcePapDriverWidget(self, size)
                        driver_widget.fillData(driver)
                        #if not driver_widget.fillData(driver):
                        #    return
                        driver_widget.show()
                        self.tableWidget.setCellWidget(row, col, driver_widget)
                        QtCore.QObject.connect(driver_widget,QtCore.SIGNAL("icepapDoubleClicked(PyObject *)"),self.driverDoubleclick)
           
    
                    else:
                        if not driver_widget.refresh():
                            return
        if not size == None:
            for col in range(self.tableWidget.columnCount()):
                self.tableWidget.horizontalHeader().resizeSection(col,self._colSize[size])
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.verticalHeader().resizeSection(row,self._rowSize[size])
        self.tableWidget.setUpdatesEnabled(True)
        self.tableWidget.horizontalHeader().setUpdatesEnabled(True)
        self.tableWidget.verticalHeader().setUpdatesEnabled(True)
        
                

        
            