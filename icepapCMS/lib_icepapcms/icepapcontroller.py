#!/usr/bin/env python

# ------------------------------------------------------------------------------
# This file is part of icepapCMS (https://github.com/ALBA-Synchrotron/icepapcms)
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# ------------------------------------------------------------------------------


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
from ..ui_icepapcms.messagedialogs import MessageDialogs
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
        self.config_template = os.path.join(path,
                                            'templates',
                                            'driverparameters.xml')
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
            MessageDialogs.showInformationMessage(None,"Host connection","It is not allowed to connect to %s. (Check subnet)"%host)
            return False
        else:
            try:
                self.iPaps[icepap_name] = EthIcePAP(host, port, log_path = log_folder)
                self.iPaps[icepap_name].connect()
                return True
            except Exception,e:
                #print "icepapcontroller: Some exception opening connection.",e
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
            # IMPROVE OF SPEED BY SAVING CFGINFOS BY VERSION
            cfginfos_version_dict = {}
            for addr in self.iPaps[icepap_name].getDriversAlive():
                """ TO-DO STORM review"""
                driver = icepapdriver.IcepapDriver(driver_name, addr)
                driver_cfg = self.getDriverConfiguration(icepap_name, addr)
                driver.addConfiguration(driver_cfg)

                # CFGINFO IS ALSO SPECIFIC FOR EACH DRIVER
                # To improve speed, this is true but instead of 'each driver', better each version
                driver_version = driver_cfg.getParameter(unicode('VER'),True)
                if not cfginfos_version_dict.has_key(driver_version):
                    cfginfo_dict,order_list = self.getDriverCfgInfoDictAndList(icepap_name,addr)
                    cfginfos_version_dict[driver_version] = (cfginfo_dict, order_list)

                # GET CFGINFO FROM CACHED DICT INSTEAD OF QUERYING EACH TIME
                #cfginfo_dict,order_list = self.getDriverCfgInfoDictAndList(icepap_name,addr)
                cfginfo_dict,order_list = cfginfos_version_dict[driver_version]
                
                self.icepap_cfginfos[icepap_name][addr] = cfginfo_dict    
                self.icepap_cfgorder[icepap_name][addr] = order_list

                driver.setName(driver_cfg.getParameter(unicode("IPAPNAME"),True))
                driver.setMode(self.iPaps[icepap_name].getMode(addr))
                driver_list[addr] = driver
                            
        except Exception,e:
            self.closeConnection(icepap_name)
            print 'exception:',e
            raise
        return driver_list
    
    def getDriverConfiguration(self, icepap_name, driver_addr):
        """
            Returns a IcepaDriverCfg object of the attributes predefined in
            driverparameters.xml
        """
        
        """ TO-DO STORM review"""   
        driver_cfg = IcepapDriverCfg(unicode(datetime.datetime.now()))
        driver_cfg.setSignature(self.iPaps[icepap_name].getConfig(driver_addr))
        #ver = self.iPaps[icepap_name].getVersionDsp(driver_addr)
        # THE VERSION NUMBER TO BE SHOWN IS THE DRIVER'S VERSION INSTEAD OF THE DSP'S ONE.
        ver = self.iPaps[icepap_name].getVersion(driver_addr,"DRIVER")
        ipap_id = self.iPaps[icepap_name].getId(driver_addr)
        ipap_name = self.iPaps[icepap_name].getName(driver_addr)
        # FIX NON-ASCII CHARS ISSUE IN NAME:
        if not all(ord(c) < 128 for c in ipap_name):
            ipap_name = repr(ipap_name)
        driver_cfg.setParameter(unicode("VER"), ver)
        driver_cfg.setParameter(unicode("ID"), ipap_id)
        try:
            driver_cfg.setParameter(unicode("IPAPNAME"), ipap_name)
        except Exception,e:
            print 'Exception when trying to write the driver name (%s):' % ipap_name
            print e
            ipap_name = 'NON-ASCII_NAME'
            driver_cfg.setParameter(unicode("IPAPNAME"), ipap_name)
        
        # INSTEAD OF READING PARAM BY PARAM, WE SHOULD ASK THE ICEPAP FOR ALL THE CONFIGURATION
        # WITH THE #N?:CFG COMMAND, USING SOME .getCfg() METHOD.
        config = self.iPaps[icepap_name].getCfg(driver_addr)
        config = config.replace('$\r\n',"")
        config = config.replace('\r\n$',"")
        params_list = config.split("\r\n")
        for param_value in params_list:
            splitted = param_value.split(" ")
            # TRAC #38 TASK
            param_name = splitted[0]
            param_value = splitted[1:]
            param_value = ' '.join(param_value)
            driver_cfg.setParameter(param_name, param_value)

        return driver_cfg
    
    def setDriverConfiguration(self, icepap_name, driver_addr, new_values, expertFlag = False):
        """ TO-DO STORM review"""
        if self.iPaps[icepap_name].getMode(driver_addr) != IcepapMode.CONFIG:
            self.iPaps[icepap_name].setConfig(driver_addr)

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
                try:
                    self.iPaps[icepap_name].setCfgParameter(driver_addr, name, str(value))
                except IcePAPException,iex:
                    msg = 'Error configuring parameter %s = %s' % (name,str(value))
                    msg += '\n'+iex.msg
                    MessageDialogs.showErrorMessage(None,'Driver conf',msg)
                    print iex.msg
                    raise iex

        # NOW THE NOT_FOUND INDEX ORDER...
        for (name,value) in not_found_index:
            try:
                if name == "NAME" or name == "IPAPNAME":
                    name = "NAME"
                    # IN CASE OF NAMELOCK SET TO YES, UNLOCK FIRST
                    namelock = self.iPaps[icepap_name].getCfgParameter(driver_addr,'NAMELOCK')
                    if namelock == 'YES':
                        self.iPaps[icepap_name].setCfgParameter(driver_addr,'NAMELOCK','NO')
                    self.iPaps[icepap_name].writeParameter(driver_addr, name, str(value))
                    self.iPaps[icepap_name].setCfgParameter(driver_addr,'NAMELOCK',namelock)
                elif name in ["VER","ID"]:
                    pass
                else:
                    self.iPaps[icepap_name].setCfgParameter(driver_addr, name, str(value))
            except IcePAPException,iex:
                msg = 'Error configuring parameter %s = %s' % (name,str(value))
                msg += '\n'+iex.msg
                MessageDialogs.showErrorMessage(None,'Driver conf',msg)
                print iex.msg
                raise iex
            except Exception,e:
                print "something happened when configuring the driver",e
                    

        try:
            if expertFlag:
                self.iPaps[icepap_name].setExpertFlag(driver_addr)
        except IcePAPException,iex:
            msg = 'Error setting expert flag.'
            msg += '\n'+iex.msg
            MessageDialogs.showErrorMessage(None,'Expert flag',msg)
            print iex.msg
            raise iex


        driver_cfg = self.getDriverConfiguration(icepap_name, driver_addr)    
        return driver_cfg
        
    def discardDriverCfg(self,icepap_name, driver_addr):
        try:
            if self.iPaps.has_key(icepap_name):
                self.iPaps[icepap_name].signConfig(driver_addr, "")
        except IcePAPException,iex:
            msg = 'Error signing config.'
            msg += '\n'+iex.msg
            MessageDialogs.showErrorMessage(None,'config',msg)
            print iex.msg
            raise iex
        
    def signDriverConfiguration(self,icepap_name, driver_addr, signature):
        try:
            if self.iPaps.has_key(icepap_name):
                if self.iPaps[icepap_name].getMode(driver_addr) != IcepapMode.CONFIG:
                    self.iPaps[icepap_name].setConfig(driver_addr)
                self.iPaps[icepap_name].signConfig(driver_addr, signature)
        except IcePAPException,iex:
            msg = 'Error signing config.'
            msg += '\n'+iex.msg
            MessageDialogs.showErrorMessage(None,'sign driver',msg)
            print iex.msg
            raise iex
   
    def startConfiguringDriver(self, icepap_name, driver):
        try:
            mode = self.iPaps[icepap_name].getMode(driver.addr)
            if mode == IcepapMode.PROG:
                return mode
            if mode != IcepapMode.CONFIG:
                self.iPaps[icepap_name].setConfig(driver.addr)
            driver.setMode(IcepapMode.CONFIG)
        except IcePAPException,iex:
            msg = 'Error starting config.'
            msg += '\n'+iex.msg
            MessageDialogs.showErrorMessage(None,'config',msg)
            print iex.msg
            raise iex
        return mode


    def endConfiguringDriver( self, icepap_name, driver):
        try:    
            if not self.iPaps.has_key(icepap_name):
                return
            mode = self.iPaps[icepap_name].getMode(driver.addr)
            if mode == IcepapMode.PROG:
                return
            if mode != IcepapMode.OPER:
                last_signature = self.iPaps[icepap_name].getConfig(driver.addr)
                self.iPaps[icepap_name].signConfig(driver.addr, last_signature)
            driver.setMode(IcepapMode.OPER)
        except IcePAPException,iex:
            msg = 'Error ending config.'
            msg += '\n'+iex.msg
            MessageDialogs.showErrorMessage(None,'end config',msg)
            print iex.msg
            raise iex

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
            
            power = IcepapStatus.isPowerOn(register)

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

        power = False
        position = -1
        encoder = -1

        power = IcepapStatus.isPowerOn(register)

        position = self.iPaps[icepap_name].getPositionFromBoard(driver_addr, pos_sel)
        encoder = self.iPaps[icepap_name].getEncoder(driver_addr, enc_sel)

        try:
            encoder = float(encoder)
        except:
            encoder = -1
        try:
            position = float(position)
        except:
            position = -1
        posarray = [position, encoder]
            
        state = (int(register), power, posarray)
        return state
        
    def getDriverActiveStatus(self, icepap_name, driver_addr):
        try:
            return self.iPaps[icepap_name].getActive(driver_addr)
        except IcePAPException,iex:
            msg = 'Error reading active status.'
            msg += '\n'+iex.msg
            MessageDialogs.showErrorMessage(None,'get active',msg)
            print iex.msg
            raise iex

    def readIcepapParameters(self, icepap_name, driver_addr, par_list):
        try:
           values = []
           for name in par_list:
               if type(name) == type(values):
                   value = self.iPaps[icepap_name].readParameter(driver_addr, name[0], name[1])
               else:
                   value = self.iPaps[icepap_name].readParameter(driver_addr, name)
               values.append([name, value])
           
           return values
        except IcePAPException,iex:
            msg = 'Error reading parameters for driver %s.'%(str(driver_addr))
            msg += '\n'+iex.msg
            MessageDialogs.showErrorMessage(None,'read param',msg)
            print iex.msg
            raise iex

    
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
            try:
                self.iPaps[icepap_name].writeParameter(driver_addr, name, value)
            except IcePAPException,iex:
                msg = 'Error writing icepap parameter %s = %s.' % (name,str(value))
                msg += '\n'+iex.msg
                MessageDialogs.showErrorMessage(None,'write param',msg)
                print iex.msg
                raise iex
        
        # NOW THE NOT FOUND INDEX ORDER...
        for (name,value) in not_found_index:
            try:
                self.iPaps[icepap_name].writeParameter(driver_addr,name,value)
            except IcePAPException,iex:
                msg = 'Error writing icepap parameter %s = %s.' % (name,str(value))
                msg += '\n'+iex.msg
                MessageDialogs.showErrorMessage(None,'write param',msg)
                print iex.msg
                raise iex


    def configDriverToDefaults(self,icepap_name,driver_addr):
        try:
            self.iPaps[icepap_name].setDefaultConfig(driver_addr)
        except IcePAPException,iex:
            msg = 'Error configuring to defaults.'
            msg += '\n'+iex.msg
            MessageDialogs.showErrorMessage(None,'default config',msg)
            print iex.msg
            raise iex

    def getDriverCfgInfo(self,icepap_name,driver_addr):
        try:
            cfginfo = self.iPaps[icepap_name].getCfgInfo(driver_addr)
            return cfginfo
        except IcePAPException,iex:
            msg = 'Error getting cfginfo (%s).' % (str(driver_addr))
            msg += '\n'+iex.msg
            MessageDialogs.showErrorMessage(None,'cfg info',msg)
            print iex.msg
            raise iex


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
    
    def setDriverEncoder(self, icepap_name, driver_addr, enc_sel, position):
        try:
            self.iPaps[icepap_name].setEncoder(driver_addr, position, enc_sel)
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
        self.iPaps[icepap_name].stop(driver_addr)
    
    def abortDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name].abort(driver_addr)

    def blinkDriver(self, icepap_name, driver_addr,secs):
        self.iPaps[icepap_name].blink(driver_addr,secs)
    
    def jogDriver(self, icepap_name, driver_addr, speed):
        if self.iPaps[icepap_name].getMode(driver_addr) != IcepapMode.CONFIG:
            self.iPaps[icepap_name].jog(driver_addr, speed)
        else:
            self.iPaps[icepap_name].cjog(driver_addr, speed)
    
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
            return []

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
        self.programming_ipap.sendWriteCommand(cmd, prepend_ack=False)
        self.updateProgressBarTimer.start(2000)
        return True

    def updateProgressBar(self):
        progress = self.programming_ipap.getProgressStatus()
        if progress is not None:
            self.progress_dialog.setValue(progress)
        else:
            self.progress_dialog.setValue(100)
            self.updateProgressBarTimer.stop()
            cmd = "#MODE OPER"
            answer = self.programming_ipap.sendWriteReadCommand(cmd)
            self.programming_ipap = None    
         
        ##cmd = "?PROG"
        ##answer = self.programming_ipap.sendWriteReadCommand(cmd)
        ##if answer.count("ACTIVE") > 0:
        ##    p = int(answer.split(" ")[2].split(".")[0])
        ##    self.progress_dialog.setValue(p)
        ##else:
        ##    self.progress_dialog.setValue(100)
        ##    self.updateProgressBarTimer.stop()
        ##    cmd = "#MODE OPER"
        ##    answer = self.programming_ipap.sendWriteReadCommand(cmd)
        ##    self.programming_ipap = None
        
    def sendFirmware(self, ipap, filename, logger, save=True):
        logger.addToLog("Setting MODE PROG")
        cmd = "#MODE PROG"
        logger.addToLog(cmd)
        ans = ipap.sendWriteReadCommand(cmd)
        logger.addToLog(ans)
        
        logger.addToLog("Transferring firmware")
        ipap.sendFirmware(filename, save=save)

        time.sleep(5)
        ipap.sendWriteCommand("MODE OPER")
        cmd = "#MODE OPER"
        logger.addToLog(cmd)
        ans = ipap.sendWriteReadCommand(cmd)
        logger.addToLog(ans)

    def upgradeFirmware(self, serial, dst, filename, addr, options, logger):
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
            
        addr = addr.replace("NONE", "")
        options = options.replace("NONE", "")
        ipap.connect()

        if filename != '':
            save = options == 'SAVE'
            self.sendFirmware(ipap, filename, logger, save=save)
        else:
            # NO POSSIBILITY TO 'SAVE OR SL' if no filename
            options = ''

        logger.addToLog("Setting MODE PROG")
        cmd = "#MODE PROG"
        logger.addToLog(cmd)
        ans = ipap.sendWriteReadCommand(cmd)
        logger.addToLog(ans)
        
        
        logger.addToLog("Configuring connection: "+addr+","+options)
        
        cmd = "PROG %s %s" % (addr, options)
        logger.addToLog(cmd)
        ipap.sendWriteCommand(cmd, prepend_ack=False)
        
        shouldwait = True
        while shouldwait:
            p = ipap.getProgressStatus()
            if p == 'DONE':
                shouldwait = False
            elif isinstance(p, int):
                logger.addToLog('Programming %d %%' % p)
                time.sleep(5)
        
        logger.addToLog("Setting MODE OPER")
        cmd = "#MODE OPER"
        logger.addToLog(cmd)
        ans = ipap.sendWriteReadCommand(cmd)
        logger.addToLog(ans)

        #if addr == 'ALL':
        if True:
            logger.addToLog('SHOULD BE ONLY IF %s IS ALL' % addr)
            logger.addToLog('Wait while rebooting... (25-30) secs')
            cmd = '#REBOOT'
            logger.addToLog(cmd)
            ans = ipap.sendWriteReadCommand(cmd)
            logger.addToLog(ans)

            # WE SHOULD WAIT UNTIL CONNECTION IS LOST
            secs = 0
            for i in range(10):
                time.sleep(1)
                secs += 1
                if (secs % 5) == 0:
                    logger.addToLog('Waiting... (%2d secs).' % secs)
            ipap.disconnect()

            # WE SHOULD WAIT UNTIL ICEPAP IS RECONNECTED
            while not ipap.connected:
                time.sleep(1)
                secs += 1
                if (secs % 5) == 0:
                    logger.addToLog('Waiting... (%2d secs).' % secs)

        cmd = '0:?VER INFO'
        logger.addToLog(cmd)
        ans = ipap.sendWriteReadCommand(cmd)
        logger.addToLog(ans)
        logger.addToLog('\n\nProgramming sequence done!')

    
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
            print "testing connection"
            ipap.disconnect()
            return True
        except:
            return False


    def find_networks(self,configs,addr_pattern,mask_pattern):
      addr_parse = re.compile(addr_pattern)
      mask_parse = re.compile(mask_pattern)
      networks = []
      for config in configs:
          addr = addr_parse.search(config)
          mask = mask_parse.search(config)
          if addr and mask:
              net = IP(addr.group(2)+"/"+mask.group(2),make_net=True)
              networks.append(net)
      return networks
  
    def host_in_same_subnet(self,host):
          if self._config._options.allnets:
              return True
  
          networks = []
          configs = None
          addr_pattern = None
          mask_pattern = None
          digits = r'[0-9]{1,3}'
          
          if os.name == 'posix':
              ifconfigs = ['/sbin/ifconfig','/usr/sbin/ifconfig','/bin/ifconfig','/usr/bin/ifconfig']
              ifconfig = filter(os.path.exists,ifconfigs)[0]
              fp = os.popen(ifconfig+' -a')
              configs = fp.read().split('\n\n')
              fp.close()
              # 180214 - Adapted to Debian9 "/sbin/ifconfig -a" output
              #addr_pattern = r'(inet addr:) *(%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
              #mask_pattern = r'(Mask:) *(%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
              addr_pattern = r'(inet ) *(%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
              mask_pattern = r'(netmask ) *(%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
          elif os.name == 'nt':
              fp = os.popen('ipconfig /all')
              configs = fp.read().split(':\r\n\r\n')
              fp.close()
              # 180214 - Adapted to Windows7 "ipconfig /all" output
              #addr_pattern = r'(IP Address).*: (%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
              addr_pattern = r'(IPv4 Address).*: (%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
              mask_pattern = r'(Subnet Mask).*: (%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
  
          if configs and addr_pattern and mask_pattern:
              networks = self.find_networks(configs,addr_pattern,mask_pattern)
  
          if len(networks)>0:
              host_addr = socket.gethostbyname(host)
              for net in networks:
                  if host_addr in net:
                      return True
              return False            
          else:
              MessageDialogs.showInformationMessage(None,"Not posix operating system","Sorry system not yet supported.\nWe allow you access to the icepap even if it is in another subnet.")
              return True
        
