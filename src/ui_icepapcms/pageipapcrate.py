from PyQt4 import QtCore, QtGui, Qt
from qrc_icepapcms import *
from icepapdriver_widget import IcePapDriverWidget


class PageiPapCrate(QtGui.QWidget):
    def __init__(self, mainwin):
        QtGui.QWidget.__init__(self, None)
        #self.resize(QtCore.QSize(QtCore.QRect(0,0,800,607).size()).expandedTo(self.minimumSizeHint()))
        #sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        #self.setMinimumSize(QtCore.QSize(800,201))
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        #self.setSizePolicy(sizePolicy)
        self.mainwin = mainwin  
        self.vboxlayout = QtGui.QVBoxLayout(self)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        
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
        self.tableWidget.setMinimumSize(QtCore.QSize(40,248))
        self.tableWidget.setMaximumSize(QtCore.QSize(112333,248))
        
        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)
        self.vboxlayout.addWidget(self.tableWidget)
        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)

    
    def fillData(self, icepap_system, selected_crate):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setUpdatesEnabled(False)
        self.tableWidget.verticalHeader().setUpdatesEnabled(False)
        
        for i in range(8):
            headerItem = QtGui.QTableWidgetItem()
            headerItem.setText(str(i+1))
            self.tableWidget.setHorizontalHeaderItem(i,headerItem)
            self.tableWidget.horizontalHeader().resizeSection(i,94)
            self.tableWidget.horizontalHeader().setResizeMode(i, Qt.QHeaderView.Custom)
            
        self.icepap_system = icepap_system
        self.cratenr = selected_crate
        self.driverswidgets = {}
        crate = -1
        
        for addr, driver in icepap_system.IcepapDriverList.items():
            if driver.cratenr == selected_crate:
                crate = driver.cratenr 
                self.tableWidget.insertRow(crate)
                headerItem = QtGui.QTableWidgetItem()
                headerItem.setText("Crate %d" %crate)
                self.tableWidget.setVerticalHeaderItem(crate,headerItem) 
                self.tableWidget.verticalHeader().resizeSection(crate,200)
                self.tableWidget.verticalHeader().setResizeMode(crate, Qt.QHeaderView.Custom)
                for drivernr in range(8):  
                    addr = crate*10+ drivernr +1                                           
                    adriver = icepap_system.getDriver(crate*10+ drivernr +1)
                    if not adriver is None:                                         
                        wdriver = IcePapDriverWidget(self)
                        wdriver.fillData(adriver)
                        #if not wdriver.fillData(adriver):
                        #    return
                        self.driverswidgets[addr]  = wdriver
                        self.tableWidget.setCellWidget(crate, drivernr, wdriver)
                        QtCore.QObject.connect(wdriver,QtCore.SIGNAL("icepapDoubleClicked(PyQt_PyObject)"),self.driverDoubleclick)
                break
        
        self.tableWidget.horizontalHeader().setUpdatesEnabled(True)
        self.tableWidget.verticalHeader().setUpdatesEnabled(True)
        
    def driverDoubleclick(self, driver):
        if not driver is None:
            location = "%s/%d/%d" % (driver.icepap_name, driver.cratenr, driver.drivernr)
            self.mainwin.treeSelectByLocation(location)
            
    def refresh(self):
        for col in range(self.tableWidget.columnCount()):
            for row in range(self.tableWidget.rowCount()):
                driver_widget =  self.tableWidget.cellWidget(row, col)
                if not driver_widget is None:
                    if not driver_widget.refresh():
                        return
        
            