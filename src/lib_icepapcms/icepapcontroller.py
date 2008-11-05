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
from ui_icepapcms.messagedialogs import MessageDialogs
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt
import re
import socket
from IPy import IP

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
        self.icepap_cfginfos = {}
        self.icepap_cfgorder = {}
        self.programming_ipap = None        
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
        if not self.host_in_same_subnet(icepap_name):
            MessageDialogs.showInformationMessage(None,"Host connection","It is not allowed to connect to %s"%host)
            return False
        else:
            try:
                self.iPaps[icepap_name] = EthIcePAP(host, port, log_path = log_folder)
                self.iPaps[icepap_name].connect(shouldReconnect = False)
                return True
            except:
                return False
        
    def closeConnection(self, icepap_name):
        if self.iPaps.has_key(icepap_name):
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
        self.icepap_cfginfos[icepap_name] = {}
        self.icepap_cfgorder[icepap_name] = {}
        try:
            sys_status = self.iPaps[icepap_name].getSysStatus()
            sys_status = int(sys_status, 16)
            for crate in range(16):
                if (sys_status & (1<<crate)) > 0:
                    crate_status =  self.iPaps[icepap_name].getRackStatus(crate)[1]
                    crate_status = int(crate_status, 16)
                    for driver in range(8):
                        if (crate_status & (1<<driver)) > 0:
                            addr = self._getDriverAddr(crate, driver+1)
                            """ TO-DO STORM review"""
                            driver = icepapdriver.IcepapDriver(driver_name, addr)
                            driver_cfg = self.getDriverConfiguration(icepap_name, addr)
                            driver.addConfiguration(driver_cfg)
                            driver.setName(driver_cfg.getParameter(unicode("IPAPNAME"),True))
                            #print driver_cfg.getParameter(unicode("IPAPNAME"),True)
                            #print driver_cfg.getParameter(unicode("VER"),True)
                            #print driver_cfg.getParameter(unicode("ID"),True)

                            # CFGINFO IS ALSO SPECIFIC FOR EACH DRIVER    
                            cfginfo_dict,order_list = self.getDriverCfgInfoDictAndList(icepap_name,addr)
                            self.icepap_cfginfos[icepap_name][addr] = cfginfo_dict    
                            self.icepap_cfgorder[icepap_name][addr] = order_list

                            driver.setName(self.iPaps[icepap_name].getName(addr))
                            driver.setMode(self.iPaps[icepap_name].getMode(addr))
                            driver_list[addr] = driver
                            
        except:
            print "Unexpected errors:", sys.exc_info()[1]
            self.closeConnection(icepap_name)
            return {}

        return driver_list
    
    def getDriverConfiguration(self, icepap_name, driver_addr):
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
        ipap_name = self.iPaps[icepap_name].getName(driver_addr)
        driver_cfg.setParameter(unicode("VER"), ver)
        driver_cfg.setParameter(unicode("ID"), ipap_id)
        driver_cfg.setParameter(unicode("IPAPNAME"), ipap_name)
        
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
        # INSTEAD OF READING PARAM BY PARAM, WE SHOULD ASK THE ICEPAP FOR ALL THE CONFIGURATION
        # WITH THE #N?:CFG COMMAND, USING SOME .getCfg() METHOD.
        config = self.iPaps[icepap_name].getConfig(driver_addr)
        config = config.replace('$\r\n',"")
        config = config.replace('\r\n$',"")
        params_list = config.split("\r\n")
        for param_value in params_list:
            split = param_value.split(" ")
            driver_cfg.setParameter(split[0],split[1])

        return driver_cfg
    
    def setDriverConfiguration(self, icepap_name, driver_addr, new_values, expertFlag = False):
        try:
            """ TO-DO STORM review"""
            if self.iPaps[icepap_name].getMode(driver_addr) != IcepapMode.CONFIG:
                self.iPaps[icepap_name].startConfig(driver_addr)

            # THE CONFIGURATION VALUES SHOULD BE SENT IN A SPECIFIC ORDER
            order_list = self.icepap_cfgorder[icepap_name][driver_addr]
            params_ordered = {}
            not_found_index = []
            for (name,value) in new_values:
                try:
                    index = order_list.index(name)
                    params_ordered[index] = (name,value)
                except:
                    not_found_index.append((name,value))
            
            keys = params_ordered.keys()
            keys.sort()
            for key in keys:
                (name,value) = params_ordered.get(key)
                if name != "VER":
                    self.iPaps[icepap_name].setCfgParameter(driver_addr, name, str(value))

            # NOW THE NOT_FOUND INDEX ORDER...
            for (name,value) in not_found_index:
                if name == "NAME" or name == "IPAPNAME":
                    name = "NAME"
                    self.iPaps[icepap_name].writeParameter(driver_addr, name, str(value))
                else:
                    self.iPaps[icepap_name].setCfgParameter(driver_addr, name, str(value))
                    

            if expertFlag:
                self.iPaps[icepap_name].setExpertFlag(driver_addr)
            driver_cfg = self.getDriverConfiguration(icepap_name, driver_addr)    
            return driver_cfg
        except:
            return None
        
    def discardDriverCfg(self,icepap_name, driver_addr):
        if self.iPaps.has_key(icepap_name):
            self.iPaps[icepap_name].signConfig(driver_addr, "")
        
    def signDriverConfiguration(self,icepap_name, driver_addr, signature):
        if self.iPaps.has_key(icepap_name):
            if self.iPaps[icepap_name].getMode(driver_addr) != IcepapMode.CONFIG:
                self.iPaps[icepap_name].startConfig(driver_addr)
            self.iPaps[icepap_name].signConfig(driver_addr, signature)
   
    def getDriverStatus(self, icepap_name, driver_addr):
        """
            Returns an array with the Status, Limit Switches and Current of the driver
        """
        if not self.iPaps[icepap_name].connected:
            return (-1,False,-1)

        if self.programming_ipap is not None:
            return (-1,False,-1)
        
        try:
            register = self.iPaps[icepap_name].getStatus(driver_addr)
            if "x" in register:
                register = int(register,16)
            else:
                register = int(register)
            
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
        except Exception,e:
            #print "There was an exception while accessing the driver ("+icepap_name+":"+str(driver_addr)+"):",e
            #raise e
            return (-1, False, -1)
            
        
    def getDriverTestStatus(self, icepap_name, driver_addr, pos_sel, enc_sel):
        """
            Returns an array with the Status, Limit Switches and Position of the driver
        """
        if self.programming_ipap is not None:
            return (-1,-1,[-1,-1])

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
        
    def getDriverActiveStatus(self, icepap_name, driver_addr):
        return self.iPaps[icepap_name].getActive(driver_addr)

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
        # THE CONFIGURATION VALUES SHOULD BE SENT IN A SPECIFIC ORDER
        order_list = self.icepap_cfgorder[icepap_name][driver_addr]
        params_ordered = {}
        not_found_index = []
        for (name,value) in par_var_list:
            try:
                index = order_list.index(name)
                params_ordered[index] = (name,value)
            except:
                not_found_index.append((name,value))

        keys = params_ordered.keys()
        keys.sort()
        for key in keys:
            (name,value) = params_ordered.get(key)
            self.iPaps[icepap_name].writeParameter(driver_addr, name, value)

        # NOW THE NOT FOUND INDEX ORDER...
        for (name,value) in not_found_index:
            self.iPaps[icepap_name].writeParameter(driver_addr,name,value)


    def configDriverToDefaults(self,icepap_name,driver_addr):
        self.iPaps[icepap_name].setDefaultConfig(driver_addr)

    def getDriverCfgInfo(self,icepap_name,driver_addr):
        cfginfo = self.iPaps[icepap_name].getCfgInfo(driver_addr)
        return cfginfo

    def getDriverCfgInfoDictAndList(self, icepap_name, driver_addr):
        """
            Returns a dictionary with all the Driver params cfginfo
        """
        
        """ TO-DO STORM review"""   
        # THE AVAILABLE OPTIONS FOR EACH PARAMETER ARE ALSO GIVEN BY THE DRIVER INSTEAD OF
        # FIXED VALUES FROM THE APPLICATION
        # THE CFGINFO IS NEEDED TO POPULATE THE QComboBoxes with correct available values
        cfginfo_str = self.getDriverCfgInfo(icepap_name,driver_addr)
        cfginfo_str = cfginfo_str.replace('$\r\n',"")
        cfginfo_str = cfginfo_str.replace('\r\n$',"")
        cfginfo_list = cfginfo_str.split("\r\n")
        cfginfo_dict = {}
        order_list = []
        for param_cfg in cfginfo_list:
            split = param_cfg.split(" ",1)
            if len(split) > 1:
                param = split[0]
                values = split[1]
                values = values.replace("{","")
                values = values.replace("}","")
                cfginfo_dict[split[0]] = values.split()
                order_list.append(param)
            else:
                print "THE CONTROLLER DID NOT RECEIVE ALL THE CFGINFO FOR THE DRIVER "+str(driver_addr)
                print "PLEASE, TRY TO RECONNECT TO THE "+str(icepap_name)+" ICEPAP SYSTEM"
                print "AND REPORT THIS OUTPUT TO THE MANTAINER\n\n\n"
                
                MessageDialogs.showWarningMessage(None, "Driver configuration", "Could not retrive all the CFGINFO for the driver "+str(driver_addr)+". Please, try to reconnect to "+str(icepap_name)+".")
                #print "ALL INFO WAS (str): "+str(cfginfo_str)
                #print "ALL INFO WAS (list): "+str(cfginfo_list)
                #print "SOME ERROR GETTING CFGINFO: "+str(param_cfg)
        return (cfginfo_dict,order_list)

    
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
            # CMOVE ONLY ALLOWS ABSOLUTE POSITIONS, IT SHOULD BE CALCULATED
            #self.iPaps[icepap_name].cmove(driver_addr, steps)
            pos = self.iPaps[icepap_name].getPosition(driver_addr)
            new_pos = int(pos) + int(steps)
            self.iPaps[icepap_name].cmove(driver_addr, new_pos)
        else:
            self.iPaps[icepap_name].rmove(driver_addr, steps)
        
    def moveDriverAbsolute(self, icepap_name, driver_addr, pos):
        if self.iPaps[icepap_name].getMode(driver_addr) == IcepapMode.CONFIG:
            self.iPaps[icepap_name].cmove(driver_addr, pos)
        else:
            self.iPaps[icepap_name].move(driver_addr, pos)
        
    def stopDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].stopMotor(driver_addr)
    
    def abortDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].abortMotor(driver_addr)

    def blinkDriver(self, icepap_name, driver_addr,secs):
        self.iPaps[icepap_name].blink(driver_addr,secs)
    
    def jogDriver(self, icepap_name, driver_addr, speed):
        self.iPaps[icepap_name].jog(driver_addr, speed)
    
    def enableDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].enable(driver_addr)
    
    def disableDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].disable(driver_addr)
    
    def checkIcepapStatus(self, icepap_name):
        if self.iPaps.has_key(icepap_name) and not self.iPaps[icepap_name].connected:
            return False
        if not self.iPaps.has_key(icepap_name):
            return False
        return True
        
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

    def upgradeDrivers(self,icepap_name,progress_dialog):
        if self.programming_ipap is not None:
            return False
        self.programming_ipap = self.iPaps[icepap_name]
        self.progress_dialog = progress_dialog
        self.progress_dialog.show()
        self.updateProgressBarTimer = Qt.QTimer()
        QtCore.QObject.connect(self.updateProgressBarTimer,QtCore.SIGNAL("timeout()"),self.updateProgressBar)
        cmd = "#MODE PROG"
        answer = self.programming_ipap.sendWriteReadCommand(cmd)
        if answer != "MODE OK":
            print "icepapcontroller:upgradeDrivers:Some error trying to set mode PROG:",answer
            return False
        cmd = "PROG DRIVERS"
        self.programming_ipap.sendWriteCommand(cmd)
        self.updateProgressBarTimer.start(2000)
        return True

    def updateProgressBar(self):
        cmd = "?PROG"
        answer = self.programming_ipap.sendWriteReadCommand(cmd)
        if answer.count("ACTIVE") > 0:
            p = int(answer.split(" ")[2].split(".")[0])
            self.progress_dialog.setValue(p)
        else:
            self.progress_dialog.setValue(100)
            self.updateProgressBarTimer.stop()
            cmd = "#MODE OPER"
            answer = self.programming_ipap.sendWriteReadCommand(cmd)
            self.programming_ipap = None
        
    def upgradeFirmware(self, serial, dst, filename, addr, options, logger):
        logger.addToLog("Reading file "+ filename)
        f = file(filename,'rb')
        data = f.read()
        data = array.array('H', data)
        f.close()
        nwordata = (len(data)) 
        
        chksum = sum(data) 
        logger.addToLog("File size: "+ str(len(data))+ " bytes, checksum: "+str(chksum)+" ("+str(hex(chksum & 0xffffffff)+")"))
        
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
        # THIS SLEEP IS NECESSARY TO LET THE TRITON COMPUTE THE CHECKSUM AND STORE IF "SAVE"
        time.sleep(7)
        logger.addToLog("Firmware sent.")
        # Notify the user that the data has been sent.
        logger.addToLog("Wait for progammming ends")
        logger.addToLog("At the end, issue a #MODE OPER")            

    
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
            #ver = ipap.getVersionDsp(0)
            ver = ipap.getSystemVersion()
            ipap.disconnect()
            return True
        except:
            return False

    def find_posix_networks(self):
        ifconfigs = ['/sbin/ifconfig','/usr/sbin/ifconfig','/bin/ifconfig','/usr/bin/ifconfig']
        ifconfig = filter(os.path.exists,ifconfigs)[0]
        fp = os.popen(ifconfig+' -a')
        config = fp.read().split('\n\n')
        fp.close()
        digits = r'[0-9]{1,3}'
        addr_pat = r'(addr:) *(%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
        addr_parse = re.compile(addr_pat)
        mask_pat = r'(Mask:) *(%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
        mask_parse = re.compile(mask_pat)
        networks = []
        for c in config:
            addr = addr_parse.search(c)
            mask = mask_parse.search(c)
            if addr and mask:
                net = IP(addr.group(2)+"/"+mask.group(2),make_net=True)
                networks.append(net)
        return networks

    def host_in_same_subnet(self,host):
        if not self._config._options.subnet:
            return True
        networks = []
        if os.name == 'posix':
            networks = self.find_posix_networks()
            host_addr = socket.gethostbyname(host)
            for net in networks:
                if host_addr in net:
                    return True
            return False
        else:
            MessageDialogs.showInformationMessage(None,"Not posix operating system","Sorry system not yet supported.\nWe allow access to the icepap even if it is in another subnet.")
            return True
        
