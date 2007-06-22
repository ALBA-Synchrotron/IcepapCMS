from PyQt4 import QtCore, QtGui, Qt
from ui_icepapdriverwidget import Ui_IcePapDriverWidget
from ui_icepapdriverwidgetsmall import Ui_IcePapDriverWidgetSmall
from ui_icepapcms.qrc_icepapcms import *
from ui_icepapcms.Led import Led
from  lib_icepapcms import MainManager, IcepapDriver, Conflict

class IcePapDriverWidget(QtGui.QWidget):
    def __init__(self, parent=None, BigSize = True):
        QtGui.QWidget.__init__(self, parent)
        self.initView(BigSize)
        self.MaxCurrent = 7
        self._driver = None
        
    def initView(self, Big):
        self.BigSize = Big
        self.coloroff = QtGui.QColor(225,255,200)
        self.colorerror = QtGui.QColor(255,179,179)
        self.colorok = QtGui.QColor(223,223,237)
        self.colorwarning = QtGui.QColor(255,226,179)
        self.colorconfig = QtGui.QColor(255,206,162)
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
        self.emit(QtCore.SIGNAL("icepapDoubleClicked(PyObject *)"), self._driver)
        event.accept()
    
    def mousePressEvent(self, event):
        tooltip = str(self._driver.currentCfg)
        QtGui.QToolTip.showText(event.globalPos(), tooltip)
        event.accept()
        
    
    def btnEnDis_on_click(self,bool):
        if bool:
            self.ui.pushButton.setText("disable")
            self._manager.enableDriver(self._driver.icepap_name, self._driver.addr)
        else:
            self.ui.pushButton.setText("enable")
            self._manager.disableDriver(self._driver.icepap_name, self._driver.addr)

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
        if self._driver.nemonic == None:
            self.ui.lblName.setText("- %d -" % self._driver.addr)
        elif self._driver.nemonic <> "":
            self.ui.lblName.setText(self._driver.nemonic)
        else:
            self.ui.lblName.setText("- %d -" % self._driver.addr)
        
        if self._driver.conflict == Conflict.DRIVER_NOT_PRESENT:
            self.setPaletteColor(self.ui.frame,self.colorerror ,Qt.Qt.black)
        elif self._driver.conflict == Conflict.DRIVER_CHANGED:
            self.setPaletteColor(self.ui.frame,self.colorwarning,Qt.Qt.black)
        else:
            self.setPaletteColor(self.ui.frame,self.colorok,Qt.Qt.black)
            
        (status, switches, current) = self._manager.getDriverStatus(self._driver.icepap_name, self._driver.addr)
        
        if status == 0:
            self.ui.ledStatus.changeColor(Led.GREEN)
            self.ui.ledStatus.on()
            self.ui.pushButton.setText("disable")
            self.ui.pushButton.setChecked(True)
        elif status == 1:
            self.ui.ledStatus.changeColor(Led.RED)
            self.ui.ledStatus.on()
            self.ui.pushButton.setText("enable")
            self.ui.pushButton.setChecked(False)
        elif status == -1:
            return True
        
        if switches == 2:
            self.ui.ledLimitNeg.on()
            self.ui.ledLimitPos.off()
        elif switches == 4:
            self.ui.ledLimitPos.on()
            self.ui.ledLimitNeg.off()
        elif switches == 6:
            self.ui.ledLimitPos.on()
            self.ui.ledLimitNeg.on()
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
        
        