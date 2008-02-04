#from pyIcePAP import EthIcePAP, IcePAPException, IcePAP, SerialIcePAP
from pyIcePAP import *
from xml.dom import minidom, Node
import os
import sys
from singleton import Singleton
import struct
import time, datetime
import array
from icepapdrivercfg import IcepapDriverCfg, CfgParameter
import icepapdriver
from conflict import Conflict
from configmanager import ConfigManager
 
class IcepapController(Singleton):
    
    def __init__(self):
        pass
    
    def init(self, *args):        
        self.iPaps = {}
        pathname = os.path.dirname(sys.argv[0])
        path = os.path.abspath(pathname)
        self.config_template = path+'/templates/driverparameters.xml'
        self._parseDriverTemplateFile()
        self._config = ConfigManager()
        try:
            self.debug = self._config.config[self._config.icepap]["debug_enabled"] == str(True)
            self.log_folder = self._config.config[self._config.icepap]["log_folder"]
            if not os.path.exists(self.log_folder):
                os.mkdir(self.log_folder)            
        except:
            print "icepapcontroller_init():", sys.exc_info()
            pass
       
    def reset(self):
        self.closeAllConnections()
        self.iPaps = {}
        
    def openConnection(self, icepap_name, host, port):
        log_folder = None
        if self.debug:
            log_folder = self.log_folder
        self.iPaps[icepap_name] = EthIcePAP(host, port, log_path = log_folder)        
        self.iPaps[icepap_name].connect()
        
    def closeConnection(self, icepap_name):
        self.iPaps[icepap_name].disconnect()
        del self.iPaps[icepap_name]
    
    def closeAllConnections(self):
        for iPap in self.iPaps.values():
            try:
                iPap.disconnect()
            except:
                pass
        self.iPaps = {}
        
    def scanIcepapSystem(self, icepap_name, compare = False):
        """ 
            Get the status of the icepap system, the drivers present, and its
            configuration.
        """
        driver_name = icepap_name
        if compare:
            driver_name = "compare"
        
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
                            """ TO-DO STORM review"""
                            driver = icepapdriver.IcepapDriver(driver_name, addr)
                            driver_cfg = self.getDriverConfiguration(icepap_name, addr)
                            driver.addConfiguration(driver_cfg)
                            driver.setName(self.iPaps[icepap_name].getName(addr))
                            mode = self.iPaps[icepap_name].getMode(addr)
                            driver.setMode(mode)
                            driver_list[addr] = driver
                            
        except:
            print "Unexpected errors:", sys.exc_info()[1]
            return {}

        return driver_list
    
    def  getDriverConfiguration(self, icepap_name, driver_addr):
        """
            Returns a IcepaDriverCfg object of the attributes predefined in
            driverparameters.xml
        """
        
        """ TO-DO STORM review"""   
              
        driver_cfg = IcepapDriverCfg(unicode(datetime.datetime.now()))
        driver_cfg.setSignature(self.iPaps[icepap_name].getConfigSignature(driver_addr))
        #ver = self.iPaps[icepap_name].getVersionDsp(driver_addr)
        # THE VERSION NUMBER TO BE SHOWN IS THE DRIVER'S VERSION INSTEAD OF THE DSP'S ONE.
        ver = self.iPaps[icepap_name].getVersion(driver_addr,"DRIVER")
        ipap_id = self.iPaps[icepap_name].getId(driver_addr)
        driver_cfg.setParameter("VER", ver)
        driver_cfg.setParameter("ID", ipap_id)
        # INSTEAD OF READING PARAM BY PARAM, WE SHOULD ASK THE ICEPAP FOR ALL THE CONFIGURATION
        # WITHT THE #N?:CFG COMMAND, USING SOME .getCfg() METHOD.
        ###for name in self.config_parameters:
        ###    #print name
        ###    try:
        ###        value = self.iPaps[icepap_name].getCfgParameter(driver_addr, name)
        ###        #CHECK THAT THE VALUE COULD BE READ (ASCII PROBLEMS)
        ###        #print "I COULD READ THE VALUE "+str(value)
        ###    except:
        ###        value = "ERROR"
        ###    #print value
        ###    #value = value.lstrip()
        ###    #value = value.lstrip(name)
        ###    driver_cfg.setParameter(name, value)
        config = self.iPaps[icepap_name].getConfig(driver_addr)
        config = config.replace('$\r\n',"")
        config = config.replace('\r\n$',"")
        params_list = config.split("\r\n")
        for param_value in params_list:
            split = param_value.split(" ")
            driver_cfg.setParameter(split[0],split[1])

        return driver_cfg
    
    def setDriverConfiguration(self, icepap_name, driver_addr, new_values):
        try:
            """ TO-DO STORM review"""
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
        if self.iPaps.has_key(icepap_name):
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
        disabled = IcepapStatus.isDisabled(register)
        if disabled <> 1:
            # only if driver is active
            power = self.iPaps[icepap_name].getPower(driver_addr)
            power = (power == IcepapAnswers.ON)
        else:
            power = False
        
        current = self.iPaps[icepap_name].getCurrent(driver_addr)
        
        state = (int(register), power, float(current))
        return state
            
        
    def getDriverTestStatus(self, icepap_name, driver_addr, pos_sel, enc_sel):
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
            position = self.iPaps[icepap_name].getPosition(driver_addr, pos_sel)
            encoder = self.iPaps[icepap_name].getEncoder(driver_addr, enc_sel)
            power = self.iPaps[icepap_name].getPower(driver_addr)
            power = (power == IcepapAnswers.ON)
            try:
                encoder = float(encoder)
            except:
                encoder = -1
            try:
                position = float(position)
            except:
                position = -1
            posarray = [position, encoder]
        else:
            posarray = [-1, -1]
            power = False
            
        state = (int(register), power, posarray)
        return state
        
    def readIcepapParameters(self, icepap_name, driver_addr, par_list):
        values = []
        for name in par_list:
            if type(name) == type(values):
                value = self.iPaps[icepap_name].readParameter(driver_addr, name[0], name[1])
            else:
                value = self.iPaps[icepap_name].readParameter(driver_addr, name)
            values.append([name, value])
        return values
    
    def writeIcepapParameters(self, icepap_name, driver_addr, par_var_list):
        values = []
        for name, value in  par_var_list:
            self.iPaps[icepap_name].writeParameter(driver_addr, name, value)
    
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
    def setDriverPosition(self, icepap_name, driver_addr, pos_sel, position):
        try:
            self.iPaps[icepap_name].setPosition(driver_addr, position, pos_sel)
            return 0
        except:
            return -1
    
    def setEncoderPosition(self, icepap_name, driver_addr, enc_sel, position):
        try:
            self.iPaps[icepap_name].setPosition(driver_addr, position, enc_sel)
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
    
    def checkIcepapStatus(self, icepap_name):
        try:
            if self.iPaps.has_key(icepap_name):
                if self.iPaps[icepap_name].Status == CStatus.Connected:
                    self.iPaps[icepap_name].getSysStatus()
                else:
                    self.iPaps[icepap_name].connect()
                return True
            else:
                """ nothing to check, driver it's not monitored """
                return True
        except IcePAPException, e:
            if e.code == IcePAPException.TIMEOUT:
                return False
        
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
            if not inTestSection:
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
            
        #if addr == "NONE":
        #    addr = ""
        #if options == "NONE":
        #    options = ""
        addr = addr.replace("NONE","")
        options = options.replace("NONE","")
        ipap.connect()
        logger.addToLog("Configuring connection: "+addr+","+options)
        cmd = "#MODE PROG"
        logger.addToLog(cmd)
        answer = ipap.sendWriteReadCommand(cmd)
        logger.addToLog("-> "+str(answer))
        if answer != "MODE OK":
            logger.addToLog("Exiting: The IcePAP could not be set to MODE PROG: "+str(answer))
            return

        cmd = "*PROG %s %s" %(addr, options)
        logger.addToLog(cmd)
        ipap.sendWriteCommand(cmd)
        
        logger.addToLog("Transferring firmware")
        ipap.sendData(struct.pack('L',startmark))
        ipap.sendData(struct.pack('L',nwordata))
        maskedchksum = chksum & 0xffffffff
        ipap.sendData(struct.pack('L',maskedchksum))
        
        #ipap.sendData(data.tostring())
        for i in range(len(data)):
            ipap.sendData(struct.pack('H',data[i]))
        logger.addToLog("Wait for progammming ends")

        # Waiting the data to be completely in the Triton
        time.sleep(5)
        if addr != "":
            cmd = "?PROG"
            retry = True
            while retry:
                try:
                    logger.addToLog(cmd)
                    answer = ipap.sendWriteReadCommand(cmd)
                    logger.addToLog("-> "+str(answer))
                    if answer.find("ACTIVE") > 0:
                        time.sleep(1)
                    elif answer.find("ERROR") > 0:
                        logger.addToLog("Exiting: The programming has ended with an error.")
                        return
                    elif answer.find("DONE") > 0:
                        retry = False
                except IcePAPException,iex:
                    if iex.code == IcePAPException.TIMEOUT:
                        logger.addToLog("Lost connection with the COMM module.")
                        logger.addToLog("WAIT UNTIL THE ICEPAP ENDS THE PROGRAMMING AND")
                        logger.addToLog("USE THE CONSOLE TO INPUT: '#MODE OPER' command to the IcePAP.")
                    else:
                        logger.addToLog("The connection has been lost (NOT TIMEOUT!).")
                    return
        cmd = "#MODE OPER"
        retry = True
        while retry:
            try:
                logger.addToLog(cmd)
                answer = ipap.sendWriteReadCommand(cmd)
                logger.addToLog("-> "+str(answer))
                if answer == "MODE OK":
                    retry = False
                else:
                    logger.addToLog("Exiting: The IcePAP could not be set to MODE OPER: "+str(answer))
                    return
            except IcePAPException,iex:
                if iex.code == IcePAPException.TIMEOUT:
                    time.sleep(1)
                    logger.addToLog("Waiting one second more, still programming")
                else:
                    retry = False
            

    
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
        
