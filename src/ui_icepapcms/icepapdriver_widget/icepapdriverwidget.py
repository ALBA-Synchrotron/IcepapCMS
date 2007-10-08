from PyQt4 import QtCore, QtGui, Qt
from ui_icepapdriverwidget import Ui_IcePapDriverWidget
from ui_icepapdriverwidgetsmall import Ui_IcePapDriverWidgetSmall
from ui_icepapcms.qrc_icepapcms import *
from ui_icepapcms.Led import Led
from  lib_icepapcms import MainManager, IcepapDriver, Conflict, IcepapMode, IcepapStatus

class IcePapDriverWidget(QtGui.QWidget):
    def __init__(self, parent=None, BigSize = True):
        QtGui.QWidget.__init__(self, parent)
        self.initView(BigSize)
        self.MaxCurrent = 7
        self._driver = None
        self.setMouseTracking(True)
        self.status = -1
        self.ready = -1   
        self.power = -1
        self.mode = -1
        
    def initView(self, Big):
        self.BigSize = Big
        self.coloroff = QtGui.QColor(225,255,200)
        self.colorerror = QtGui.QColor(255,179,179)
        self.colorok = QtGui.QColor(223,223,237)
        self.colorwarning = QtGui.QColor(255,255,0)
        self.colorconfig = QtGui.QColor(255,206,162)
        #self.colorconf = QtGui.QColor(0,255,255)
        if Big:
            self.ui = Ui_IcePapDriverWidget()
            self.ui.setupUi(self)
            self.setPaletteColor(self.ui.lcdCurrent, self.coloroff, QtGui.QColor(Qt.Qt.white))
        else:
            self.ui = Ui_IcePapDriverWidgetSmall()
            self.ui.setupUi(self)
        
        self.ui.ledStatus.changeColor(Led.YELLOW)
        self.ui.ledLimitPos.changeColor(Led.ORANGE)
        self.ui.ledLimitNeg.changeColor(Led.GREEN)
        self._manager = MainManager()
        
        self.setAutoFillBackground(True)
        
        QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL("clicked(bool)"),self.btnEnDis_on_click)

        
    def mouseDoubleClickEvent(self, event):
        self.emit(QtCore.SIGNAL("icepapDoubleClicked(PyQt_PyObject)"), self._driver)
        event.accept()
    
    def mousePressEvent(self, event):
        tooltip = str(self._driver.current_cfg)
        QtGui.QToolTip.showText(event.globalPos(), tooltip)
        event.accept()
    
    def mouseMoveEvent(self, event):
        tooltip = str(self._driver.current_cfg)
        #self.setToolTip(tooltip)        
        event.accept()
    
    def btnEnDis_on_click(self,bool):
        if bool:
            self.ui.pushButton.setText("disable")
            self._manager.enableDriver(self._driver.icepapsystem_name, self._driver.addr)
        else:
            self.ui.pushButton.setText("enable")
            self._manager.disableDriver(self._driver.icepapsystem_name, self._driver.addr)

    def getDriver(self):
        return self._driver
    
    def fillData(self, driver):
        self._driver = driver
        if driver is None:
            self.ui.lblName.setText("")
            self.ui.frame.setEnabled(False)
            return False
        else:
            return self.fillStatus()
    
    def refresh(self):
        if not self._driver is None:
            return self.fillStatus()
        else:
            return True
    
    def fillStatus(self):
        if self._driver.name == None:
            self.ui.lblName.setText("- %d -" % self._driver.addr)
        elif self._driver.name <> "":
            self.ui.lblName.setText("%d- %s" % (self._driver.addr,self._driver.name))
        else:
            self.ui.lblName.setText("- %d -" % self._driver.addr)
        
        if self._driver.conflict == Conflict.DRIVER_NOT_PRESENT:
            self.setPaletteColor(self.ui.frame,self.colorerror ,Qt.Qt.black)
        elif self._driver.conflict == Conflict.DRIVER_CHANGED:
            self.setPaletteColor(self.ui.frame,self.colorwarning,Qt.Qt.black)
        elif self._driver.mode == IcepapMode.CONFIG:
            self.setPaletteColor(self.ui.frame,self.colorconfig,Qt.Qt.black)
        else:
            self.setPaletteColor(self.ui.frame,self.colorok,Qt.Qt.black)
            
        (status, power, current) = self._manager.getDriverStatus(self._driver.icepapsystem_name, self._driver.addr)
        if status == -1:                
            self.ui.pushButton.setEnabled(False)
            self.ui.ledStatus.changeColor(Led.RED)
            self.ui.ledStatus.on()
            return
        
        disabled = IcepapStatus.isDisabled(status)
        ready = IcepapStatus.isReady(status)
        mode = IcepapStatus.getMode(status)
        if self.status <> disabled or self.mode <> mode or self.power <> power or self.ready <> ready:
            if disabled == 0:
                if power:
                    self.ui.ledStatus.changeColor(Led.GREEN)
                    self.ui.ledStatus.on()
                    self.ui.pushButton.setText("disable")
                    self.ui.pushButton.setChecked(True)
                    self.ui.pushButton.setEnabled(True)
                    self.mode = mode                    
                else:
                    self.ui.pushButton.setEnabled(True)
                    self.ui.pushButton.setText("enable")
                    self.ui.pushButton.setChecked(False)
                    self.ui.ledStatus.changeColor(Led.RED)
                    self.ui.ledStatus.on()                    
            elif disabled == 1:
                # driver is not active disable motion and enable
                self.ui.pushButton.setEnabled(False)
                self.ui.ledStatus.changeColor(Led.RED)
                self.ui.ledStatus.on()
            else:
                self.ui.pushButton.setEnabled(True)
                self.ui.pushButton.setText("enable")
                self.ui.pushButton.setChecked(False)
                self.ui.ledStatus.changeColor(Led.RED)
                self.ui.ledStatus.on()
        
        if status == -1:                
            self.ui.pushButton.setEnabled(False)
            self.ui.ledStatus.changeColor(Led.RED)
            self.ui.ledStatus.on()

               
        
        self.status = disabled
        self.ready = ready   
        self.power = power

        lower = IcepapStatus.getLimitNegative(status) 
        upper = IcepapStatus.getLimitPositive(status)
        if lower:
            self.ui.ledLimitNeg.on()
        else:
            self.ui.ledLimitNeg.off()
        
        if upper:
            self.ui.ledLimitPos.on()
        else:
            self.ui.ledLimitPos.off()
            
        
        if self.BigSize:
            self.setCurrent(current)
        return True
    
    def setCurrent(self, current):
        self.ui.lcdCurrent.display(current)
        color = QtGui.QColor()
        if current < 0 or current >7:
            color = self.coloroff
        else:
            percentage = ((self.MaxCurrent)-current) / self.MaxCurrent
            
            S = 255 - abs(int(128*percentage))
            H = abs(int(180*percentage))
            V = 255 - abs(int(60*percentage))
            color.setHsv(H,S,V)
        self.setPaletteColor(self.ui.lcdCurrent, color, QtGui.QColor(Qt.Qt.black))
    
    def setPaletteColor(self, widget, backcolor, forecolor):
        palette = widget.palette()
        widget.setAutoFillBackground(True)
        palette.setColor(QtGui.QPalette.Base ,backcolor)
        palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text ,forecolor)
        widget.setPalette(palette)
        widget.show()
        
        