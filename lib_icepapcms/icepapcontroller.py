from pyIcePAP import EthIcePAP, IcePAPException, IcePAPStatus, IcePAP, SerialIcePAP
from icepapdriver import IcepapDriver
from icepapdrivercfg import IcepapDriverCfg
from icepapdef import *
from conflict import Conflict
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
            cratespresent = self.iPaps[icepap_name].getSysStatus()
            cratespresent = int(cratespresent, 16)
            for cratenr in range(16):
                if ((cratespresent >> cratenr) & 1) == 1:
                    driversalive =  self.iPaps[icepap_name].getRackStatus(cratenr)[1]
                    driversalive = int(driversalive, 16)
                    for drivernr in range(0,8):
                        if ((driversalive >> drivernr) & 1) == 1:
                            addr = self._getDriverAddr(cratenr, drivernr+1)
                            driver = IcepapDriver(icepap_name, addr, cratenr, drivernr)
                            driver_cfg = self.getDriverConfiguration(icepap_name, addr)
                            driver.setConfiguration(driver_cfg)
                            mode = self.iPaps[icepap_name].getMode(addr)
                            driver.mode = mode                            
                            driver_list[addr] = driver
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
        driver_cfg.signature = self.iPaps[icepap_name].getConfigSignature(driver_addr)
        ver = self.iPaps[icepap_name].getVersionDsp(driver_addr)
        driver_cfg.setAttribute("VER", ver)         
        for name in self.config_parameters:
            #print name
            try:
                value = self.iPaps[icepap_name].getCfgParamenter(driver_addr, name)
            except:
                value = "ERROR"
            #print value
            #value = value.lstrip()
            #value = value.lstrip(name)
            driver_cfg.setAttribute(name, value)
        
        return driver_cfg
    
    def setDriverConfiguration(self, icepap_name, driver_addr, new_values):
        try:
            if self.iPaps[icepap_name].getMode(driver_addr) != IcepapMode.CONFIG:
                self.iPaps[icepap_name].startConfig(driver_addr)
            for (name, value) in new_values:
                if name != "VER":
                    self.iPaps[icepap_name].setCfgParameter(driver_addr, name, str(value))
            driver_cfg = self.getDriverConfiguration(icepap_name, driver_addr)    
            return driver_cfg
        except:
            return None
        
    def discardDriverCfg(self,icepap_name, driver_addr):
        self.iPaps[icepap_name].signConfig(driver_addr, "")
        
    def signDriverConfiguration(self,icepap_name, driver_addr, signature):
        self.iPaps[icepap_name].signConfig(driver_addr, signature)
   
    def getDriverStatus(self, icepap_name, driver_addr):
        """
            Returns an array with the Status, Limit Switches and Current of the driver
        """
        
        register = self.iPaps[icepap_name].getStatus(driver_addr)
        
        if "x" in register:
            register = int(register,16)
        else:
            register = int(register)
        
        #status = IcePAPStatus.isDisabled(register) 
        
        #status = (status > 0)
        
        current = self.iPaps[icepap_name].getCurrent(driver_addr)
        
        state = (int(register), float(current))
        return state
            
        
    def getDriverTestStatus(self, icepap_name, driver_addr):
        """
            Returns an array with the Status, Limit Switches and Position of the driver
        """
        
        register = self.iPaps[icepap_name].getStatus(driver_addr)
        if "x" in register:
            register = int(register,16)
        else:
            register = int(register)
        disabled = IcepapStatus.isDisabled(register)
        if disabled <> 1:
            # only if driver is active
            position = self.iPaps[icepap_name].getPosition(driver_addr)
            power = self.iPaps[icepap_name].getPower(driver_addr)
            power = (power == IcepapAnswers.ON)
        else:
            position = -1
            power = -1
            
        state = (int(register), power, float(position))
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
        
    def moveDriver(self, icepap_name, driver_addr, steps):
        
        if self.iPaps[icepap_name].getMode(driver_addr) == IcepapMode.CONFIG:
            self.iPaps[icepap_name].cmove(driver_addr, steps)
        else:
            self.iPaps[icepap_name].rmove(driver_addr, steps)
        
    def moveDriverAbsolute(self, icepap_name, driver_addr, pos):
        self.iPaps[icepap_name].move(driver_addr, pos)
        
    def stopDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].stopMotor(driver_addr)
    
    def abortDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].abortMotor(driver_addr)
    
    def jogDriver(self, icepap_name, driver_addr, speed):
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
            if section.nodeType == Node.ELEMENT_NODE:
                    section_name =  section.attributes.get('name').value
            inTestSection = (section_name == "test")
            if inTestSection:
                return                
            for pars in section.getElementsByTagName("par"):
                if pars.nodeType == Node.ELEMENT_NODE:
                    parname =  pars.attributes.get('name').value
                    self.config_parameters.append(str(parname))
    
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
        
