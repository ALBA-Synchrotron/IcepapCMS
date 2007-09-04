from pyIcePAP import EthIcePAP, IcePAPException, IcePAPStatus, IcePAP, SerialIcePAP
from icepapdriver import IcepapDriver
from icepapdrivercfg import IcepapDriverCfg
from xml.dom import minidom, Node
import os
import sys
from singleton import Singleton
import struct
import time
import array
 
class IcepapController(Singleton):

    def __init__(self):
        pass

    def init(self, *args):
        
        self.iPaps = {}
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        self.config_template = path+'/templates/driverparameters.xml'
        self._parseDriverTemplateFile()
       
    def reset(self):
        self.closeAllConnections()
        self.iPaps = {}
        
    def openConnection(self, icepap_name, host, port):
        self.iPaps[icepap_name] = EthIcePAP(host, port)
        self.iPaps[icepap_name].connect()
        
    def closeConnection(self, icepap_name):
        self.iPaps[icepap_name].disconnect()
        del self.iPaps[icepap_name]
    
    def closeAllConnections(self):
        for iPap in self.iPaps.values():
            iPap.disconnect()
        self.iPaps = {}
        
    def scanIcepapSystem(self, icepap_name):
        """ 
            Get the status of the icepap system, the drivers present, and its
            configuration.
        """
        driver_list = {}
        try:
            for cratenr in range(16):
                cratepresent = False
                for drivernr in range(1,9):
                    addr = self._getDriverAddr(cratenr, drivernr)
                    status = self._checkDriverStatus(icepap_name, addr)
                    
                    if status >= 0:
                        # Driver Present
                        driver = IcepapDriver(icepap_name, addr, cratenr, drivernr)
                        driver_cfg = self.getDriverConfiguration(icepap_name, addr)
                        driver.setConfiguration(driver_cfg)
                        driver.signDriver()
                        driver_list[addr] = driver
                        cratepresent = True
                if not cratepresent:
                    break
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return {}

        return driver_list
    
    def  getDriverConfiguration(self, icepap_name, driver_addr):
        """
            Returns a IcepaDriverCfg object of the attributes predefined in
            driverparameters.xml
        """
        driver_cfg = IcepapDriverCfg()           
        for name in self.config_parameters:
            value = self.iPaps[icepap_name].readPar(driver_addr, name)
            value = value.lstrip()
            value = value.lstrip(name)
            driver_cfg.setAttribute(name, value)
        ver = self.iPaps[icepap_name].getVersionDsp(driver_addr)
        driver_cfg.setAttribute("VER", ver)
        return driver_cfg
    
    def setDriverConfiguration(self, icepap_name, driver_addr, new_values):
        try:
            for (name, value) in new_values:
                self.iPaps[icepap_name].writePar(driver_addr, name, str(value))
            driver_cfg = self.getDriverConfiguration(icepap_name, driver_addr)    
            return driver_cfg
        except:
            return None
   
    def getDriverStatus(self, icepap_name, driver_addr):
        """
            Returns an array with the Status, Limit Switches and Current of the driver
        """
        
        register = self.iPaps[icepap_name].getStatus(driver_addr)
        
        if "X" in register:
            register = int(register,16)
        else:
            register = int(register)
        
        status = IcePAPStatus.isDisabled(register + 0) 
        
        status = (status > 0)
        lower = IcePAPStatus.getLimitNegative(register) 
        upper = IcePAPStatus.getLimitPositive(register) 
        #(lower, upper) = self.iPaps[icepap_name].getLimitSwitches(driver_addr)
        switchstate = 0
        if int(lower) == 1 and int(upper) == 1:
            switchstate = 6
        elif int(lower) == 1:
            switchstate = 2
        elif int(upper) == 1:
            switchstate = 4
        current = self.iPaps[icepap_name].getCurrent(driver_addr)
        state = (int(status), switchstate, float(current))
        return state
            
        
    def getDriverTestStatus(self, icepap_name, driver_addr):
        """
            Returns an array with the Status, Limit Switches and Position of the driver
        """
        
        register = self.iPaps[icepap_name].getStatus(driver_addr)
        if "X" in register:
            register = int(register,16)
        else:
            register = int(register)
        disabled = IcePAPStatus.isDisabled(register) 
        disabled = (disabled > 0)
        moving = IcePAPStatus.isMoving(register)
        #(lower, upper) = self.iPaps[icepap_name].getLimitSwitches(driver_addr)
        lower = IcePAPStatus.getLimitNegative(register) 
        upper = IcePAPStatus.getLimitPositive(register) 
        switchstate = 0
        if int(lower) == 1 and int(upper) == 1:
            switchstate = 6
        elif int(lower) == 1:
            switchstate = 2
        elif int(upper) == 1:
            switchstate = 4
        position = self.iPaps[icepap_name].getPosition(driver_addr)
        state = (int(disabled), moving, switchstate, float(position))
        return state
        
            
    def getDriverMotionValues(self, icepap_name, driver_addr):
    
        speed = self.iPaps[icepap_name].getSpeed(driver_addr)
        acc = self.iPaps[icepap_name].getAcceleration(driver_addr)
        state = (speed, acc)
        return state
     
            
    
    def setDriverMotionValues(self, icepap_name, driver_addr, values):
        try:
            self.iPaps[icepap_name].setSpeed(driver_addr, values[0])
            self.iPaps[icepap_name].setAcceleration(driver_addr, values[1])
            return 0
        except:
            return -1
    def setDriverPosition(self, icepap_name, driver_addr, position):
        try:
            self.iPaps[icepap_name].setPosition(driver_addr, position)
            return 0
        except:
            return -1
    
    def configureInputSignal(self, icepap_name, driver_addr, signal, mode, edge, dir):
        try:
            cfg = mode | (edge << 1) | (dir << 2)
            self.iPaps[icepap_name].configureInputSignal(driver_addr, signal, cfg)
            if (signal == IcepapSignal.SyncIn):
                self.iPaps[icepap_name].setSignalDirection(driver_addr, IcepapSignal.SyncIn, IcepapSignalCfg.INPUT)
            return 0
        except:
            return -1
    
    def configureOutputSignal(self, icepap_name, driver_addr, signal, source, mode, edge, dir, pulse):
        try:
            cfg = mode | (edge << 1) | (dir << 2) | (pulse << 3)
            self.iPaps[icepap_name].configureOutputSignal(driver_addr, signal, source, cfg)

            if signal == IcepapSignal.SyncOut:
                
                self.iPaps[icepap_name].setSignalDirection(driver_addr, IcepapSignal.SyncIn, IcepapSignalCfg.OUTPUT)
                
            return 0
        except:
            
            return -1
    
    def setCounterSource(self, icepap_name, driver_addr, counter, src):
        try:
            if counter == IcepapSignalSrc.Target: 
                if src <> IcepapSignalSrc.DSPin:
                    self.iPaps[icepap_name].setSilent(driver_addr, 0)
                    self.iPas[icepap_name].sendWriteCommand(addr, "IDX_EXT 1")
                else:
                    self.iPas[icepap_name].sendWriteCommand(addr, "IDX_EXT 0")
            self.iPaps[icepap_name].setCounterSource(driver_addr, counter, src)
            return 0
        except:
            return -1
    
    def configureAuxInputSignal(self, icepap_name, driver_addr, signal, polarity):
        try:
            self.iPaps[icepap_name].configureAuxInputSignal(driver_addr, signal, polarity)
            if (signal == IcepapSignal.SyncAuxIn):
                self.iPaps[icepap_name].setSignalDirection(driver_addr, IcepapSignal.SyncAuxIn, IcepapSignalCfg.INPUT)
            return 0
        except:
            return -1
    
    def configureAuxOutputSignal(self, icepap_name, driver_addr, signal, src, polarity):
        try:
            self.iPaps[icepap_name].configureAuxOutputSignal(driver_addr, signal, src, polarity)
            if (signal == IcepapSignal.SyncAuxOut):
                self.iPaps[icepap_name].setSignalDirection(driver_addr, IcepapSignal.SyncAuxIn, IcepapSignalCfg.OUTPUT)
            return 0
        except:
            return -1
        
    def moveDriver(self, icepap_name, driver_addr, steps, direction):
        self.iPaps[icepap_name].setDirection(driver_addr, direction)
        self.iPaps[icepap_name].go(driver_addr, steps)
        
    def stopDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].stopMotor(driver_addr)
    
    def jogDriver(self, icepap_name, driver_addr, speed, direction):
        self.iPaps[icepap_name].setDirection(driver_addr, direction)
        self.iPaps[icepap_name].jog(driver_addr, speed)
    
    def enableDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].enable(driver_addr)
    
    def disableDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].disable(driver_addr)
        
    def _checkDriverStatus(self, icepap_name, driver_addr):
        """
            Check the status of a Icepap Driver
             0 - Disabled
             1 - Enabled
            -1 - Not Present
        """
        try:
            return self.iPaps[icepap_name].checkDriver(driver_addr)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return -1
        
    def _getDriverAddr(self, cratenr, drivernr):
        """
            returns (cratenr * 10) + drivernr
        """
        return (cratenr * 10) + drivernr
    
    def _parseDriverTemplateFile(self):
        self.config_parameters = []
        doc = minidom.parse(self.config_template)
        root  = doc.documentElement
        for section in root.getElementsByTagName("section"):
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    parname =  pars.attributes.get('name').value
                    self.config_parameters.append(parname)
    
    def getSerialPorts(self):
        try:
            return IcePAP.serialScan()
        except:
            return None
    
    def upgradeFirmware(self, serial, dst, filename, addr, options, logger):
        logger.addToLog("Reading file "+ filename)
        f = file(filename,'rb')
        data = f.read()
        data = array.array('H', data)
        f.close()
        nwordata = (len(data)) 
        
        chksum = sum(data) 
        logger.addToLog("File size: "+ str(len(data))+ " bytes, checksum: "+str(chksum))
        
        startmark = 0xa5aa555a
        if serial:
            ipap = SerialIcePAP(dst, 0)
        else:
            
            if dst.find(":") >= 0:
                aux = dst.split(':')
                host = aux[0]
                port = aux[1]
            else:
                host = dst
                port = "5000"
            
            ipap = EthIcePAP(host , port)
            
        if addr == "NONE":
            addr = ""
        if options == "NONE":
            options = ""
        ipap.connect()
        logger.addToLog("Configuring connection")
        ipap.sendWriteCommand(None, "*PROG %s %s" %(addr, options))
        logger.addToLog("Transferring firmware")        
        ipap.sendData(struct.pack('L',startmark))
        ipap.sendData(struct.pack('L',nwords))
        ipap.sendData(struct.pack('L',chksum))
        ipap.sendData(data.tostring())
        logger.addToLog("Wait for progammming ends")
    
    def testConnection(self, serial, dst):
        try:
            if serial:
                ipap = SerialIcePAP(dst, 0)
            else:
                if dst.find(":") >= 0:
                    aux = dst.split(':')
                    host = aux[0]
                    port = aux[1]
                else:
                    host = dst
                    port = "5000"
                ipap = EthIcePAP(host , port)
            ipap.connect()
            ver = ipap.getVersionDsp(0)
            ipap.disconnect()
            return True
        except:
            return False
        
        
                          


class IcepapSignal:
    InPos = 9
    OutPos = 19
    SyncIn = 10
    SyncOut = 18
    EncIn = 8
    InPosAux=6
    OutPosAux=17
    SyncAuxIn=7
    SyncAuxOut=13
    EncAux=5
    LimitPos=3
    LimitNeg=2
    Home=4
    InfoA=14
    InfoB=15
    InfoC=16
    
class IcepapSignalCfg:
    QUADRATURE, STEPDIR = range(2)
    RISING, FALLING = range(2)
    NORMAL, INVERTED = range(2)
    W50NS, W200NS, W2US, W20US = range(4)
    INPUT, OUTPUT = range(2)
class IcepapSignalSrc:
    EncIn, InPos, SyncIn, DSPin = range(4)
    Target, AuxPos1, AuxPos2 = range(3)

    
                    
                    
                    
        


