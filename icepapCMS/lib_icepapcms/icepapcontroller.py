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


from pyIcePAP import EthIcePAPController
from pyIcePAP import Mode
from xml.dom import minidom, Node
import os
import sys
from singleton import Singleton
import time
import datetime
from icepapdrivercfg import IcepapDriverCfg
import icepapdriver
from configmanager import ConfigManager
from ui_icepapcms.messagedialogs import MessageDialogs
from PyQt4 import QtCore
from PyQt4 import Qt
import re
import socket
import collections
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
        self.programming_ipap = None
        try:
            self.debug = self._config.config[self._config.icepap]["debug_enabled"] == str(True)
            self.log_folder = self._config.config[self._config.icepap]["log_folder"]
            if not os.path.exists(self.log_folder):
                os.mkdir(self.log_folder)            
        except Exception as e:
            msg = 'IcepapController init failed:\n{}\n{}'.format(sys.exc_info(), e)
            print(msg)

    def reset(self):
        self.iPaps = {}

    def openConnection(self, icepap_name, host, port):
        if not self.host_in_same_subnet(icepap_name):
            msg = 'It is not allowed to connect to {}'.format(host)
            MessageDialogs.showInformationMessage(None, 'Host Connection', msg)
            return False
        try:
            self.iPaps[icepap_name] = EthIcePAPController(host, port)
        except Exception as e:
            msg = 'IcepapController: Exception opening connection.\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Host Connection', msg)
            return False
        return True

    def closeConnection(self, icepap_name):
        if icepap_name in self.iPaps:
            del self.iPaps[icepap_name]
    
    def closeAllConnections(self):
        self.iPaps = {}

    def scanIcepapSystem(self, icepap_name, compare=False):
        """
            Get the status of the icepap system, the drivers present, and its
            configuration.
        """
        driver_name = icepap_name
        if compare:
            driver_name = "compare"
        driver_list = {}
        self.icepap_cfginfos[icepap_name] = collections.OrderedDict()
        try:
            cfginfos_version_dict = {}
            for addr in self.iPaps[icepap_name].keys():
                driver = icepapdriver.IcepapDriver(driver_name, addr)
                driver_cfg = self.getDriverConfiguration(icepap_name, addr)
                driver.addConfiguration(driver_cfg)
                driver_version = driver_cfg.getParameter(unicode('VER'), True)
                if driver_version not in cfginfos_version_dict:
                    cfginfos_version_dict[driver_version] = self._get_driver_cfg_info(icepap_name, addr)
                self.icepap_cfginfos[icepap_name][addr] = cfginfos_version_dict[driver_version]
                driver.setName(driver_cfg.getParameter(unicode("IPAPNAME"), True))
                driver.setMode(self.iPaps[icepap_name][addr].mode)
                driver_list[addr] = driver
        except Exception as e:
            self.closeConnection(icepap_name)
            msg = 'Exception scanning the system.\n{}'.format(e)
            print(msg)
            raise
        return driver_list

    def getDriverConfiguration(self, icepap_name, driver_addr):
        """
            Returns a IcepaDriverCfg object of the attributes predefined in
            driverparameters.xml
        """
        driver_cfg = IcepapDriverCfg(unicode(datetime.datetime.now()))
        axis = self.iPaps[icepap_name][driver_addr]
        try:
            axis_config = axis.config
        except Exception as e:
            msg = 'Failed to retrieve configuration for driver {}.\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Get Driver Config', msg)
            raise e
        driver_cfg.setSignature(axis_config)
        ver = self.iPaps[icepap_name].ver.driver[0]
        driver_cfg.setParameter("VER", ver)
        driver_cfg.setParameter("ID", axis.id)
        try:
            driver_cfg.setParameter("IPAPNAME", axis.name)
        except Exception, e:
            msg = 'Exception when reading the driver name ({})\n{}'.format(axis.name, e)
            print(msg)
            axis.name = 'NON-ASCII_NAME'
            driver_cfg.setParameter("IPAPNAME", axis.name)
        param_dict = axis.get_cfg()
        for param_name in param_dict:
            driver_cfg.setParameter(param_name, param_dict[param_name])
        return driver_cfg

    def setDriverConfiguration(self, icepap_name, driver_addr, new_values, expertFlag = False):
        try:
            if Mode.CONFIG not in self.iPaps[icepap_name][driver_addr].mode:
                self.iPaps[icepap_name][driver_addr].set_config()
        except RuntimeError as e:
            msg = 'Failed to set driver {} in CONFIG mode.\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Set Driver Mode', msg)
            raise e
        cfg_info = self.icepap_cfginfos[icepap_name][driver_addr]
        not_found = []
        for (name, value) in new_values:
            if name in cfg_info:
                if name != "VER":
                    try:
                        self.iPaps[icepap_name][driver_addr].set_cfg(name, str(value))
                    except RuntimeError as e:
                        msg = 'Error configuring parameter {} = {} for driver {}\n{}'
                        msg = msg.format(name, value, driver_addr, e)
                        print(msg)
                        MessageDialogs.showErrorMessage(None, 'Set Driver Config', msg)
                        raise e
            else:
                not_found.append((name, value))
        for (name, value) in not_found:
            try:
                if name in ["NAME", "IPAPNAME"]:
                    cfg = self.iPaps[icepap_name][driver_addr].get_cfg()
                    have_namelock = cfg['NAMELOCK'].upper() == 'YES'
                    if have_namelock:
                        self.iPaps[icepap_name][driver_addr].set_cfg('NAMELOCK', 'NO')
                    cmd = 'NAME {}'.format(value)
                    self.iPaps[icepap_name][driver_addr].send_cmd(cmd)
                    if have_namelock:
                        self.iPaps[icepap_name][driver_addr].set_cfg('NAMELOCK', 'YES')
                elif name in ["VER", "ID"]:
                    pass
                else:
                    self.iPaps[icepap_name][driver_addr].set_cfg(name, str(value))
            except RuntimeError as e:
                msg = 'Error configuring parameter {} = {}\n{}'.format(name, value, e)
                print(msg)
                MessageDialogs.showErrorMessage(None, 'Set Driver Config', msg)
                raise e
        try:
            if expertFlag:
                self.iPaps[icepap_name][driver_addr].set_cfg('EXPERT')
        except RuntimeError as e:
            msg = 'Error setting expert flag.\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Expert Flag', msg)
            raise e
        driver_cfg = self.getDriverConfiguration(icepap_name, driver_addr)
        return driver_cfg

    def discardDriverCfg(self, icepap_name, driver_addr):
        try:
            if icepap_name in self.iPaps:
                self.iPaps[icepap_name][driver_addr].set_config()
        except RuntimeError as e:
            msg = 'Error discarding driver config.\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Discard Driver Config', msg)
            raise e

    def signDriverConfiguration(self, icepap_name, driver_addr, signature):
        try:
            if icepap_name in self.iPaps:
                if Mode.CONFIG not in self.iPaps[icepap_name][driver_addr].mode:
                    self.iPaps[icepap_name][driver_addr].set_config()
                self.iPaps[icepap_name][driver_addr].set_config(signature)
        except RuntimeError as e:
            msg = 'Error signing config.\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Sign Driver', msg)
            raise e
   
    def startConfiguringDriver(self, icepap_name, driver):
        try:
            mode = self.iPaps[icepap_name][driver.addr].mode
            if Mode.PROG in mode:
                return mode[0]
            if Mode.CONFIG not in mode:
                self.iPaps[icepap_name][driver.addr].set_config()
            driver.setMode(Mode.CONFIG)
        except RuntimeError as e:
            msg = 'Error starting config.\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'config', msg)
            raise e
        return mode[0]

    def endConfiguringDriver(self, icepap_name, driver):
        axis = self.iPaps[icepap_name][driver.addr]
        try:
            if icepap_name not in self.iPaps:
                return
            if Mode.PROG in axis.mode:
                return
            if Mode.OPER not in axis.mode:
                last_signature = axis.config
                axis.set_config(last_signature)
            driver.setMode(Mode.OPER)
        except RuntimeError as e:
            msg = 'Error ending config for driver {}.\n{}'.format(driver.addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'End Config', msg)
            raise e

    def getDriverStatus(self, icepap_name, driver_addr):
        """
            Returns the Status, Limit Switches and Current of the driver.
        """
        if not self.iPaps[icepap_name].connected:
            state = (-1, False, -1)
            return state
        if self.programming_ipap is not None:
            state = (-1, False, -1)
            return state
        try:
            register = self.iPaps[icepap_name].get_fstatus(driver_addr)[0]
            power = self.iPaps[icepap_name][driver_addr].state_poweron
            cfg = self.iPaps[icepap_name][driver_addr].get_cfg('NCURR')
            current = float(cfg['NCURR'])
            state = (register, power, current)
            return state
        except Exception as e:
            msg = 'Failed to retrieve status for driver {}.\n{}'.format(driver_addr, e)
            print(msg)
            state = (-1, False, -1)
            return state

    def getDriverTestStatus(self, icepap_name, driver_addr, pos_sel, enc_sel):
        """
            Returns an array with the Status, Limit Switches and Position of the driver.
        """
        if self.programming_ipap is not None:
            status = (-1, -1, [-1, -1])
            return status
        register = self.iPaps[icepap_name].get_fstatus(driver_addr)[0]
        power = self.iPaps[icepap_name][driver_addr].state_poweron
        try:
            position = self.iPaps[icepap_name][driver_addr].get_pos(pos_sel)
            encoder = self.iPaps[icepap_name][driver_addr].get_enc(enc_sel)
        except Exception as e:
            msg = 'Failed to retrieve position/encoder for driver {}.\n{}'.format(driver_addr, e)
            print(msg)
            status = (-1, -1, [-1, -1])
            return status
        status = (register, power, [position, encoder])
        return status

    def is_driver_active(self, icepap_name, driver_addr):
        try:
            return self.iPaps[icepap_name][driver_addr].active == 'YES'
        except RuntimeError as e:
            msg = 'Failed to read activation status for driver {}.\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Get Status Active', msg)
            raise e

    def getDriverActiveStatus(self, icepap_name, driver_addr):
        try:
            return self.iPaps[icepap_name][driver_addr].active
        except RuntimeError as e:
            msg = 'Failed to read activation status for driver {}.\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Get Active', msg)
            raise e

    def read_icepap_indexer(self, icepap_name, driver_addr):
        try:
            return self.iPaps[icepap_name][driver_addr].indexer
        except RuntimeError as e:
            msg = 'Failed to read indexer for driver {}.\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Read Indexer', msg)
            raise e

    def read_icepap_infox(self, icepap_name, driver_addr, parameter):
        axis = self.iPaps[icepap_name][driver_addr]
        ch = parameter[4]
        try:
            if ch == 'A':
                return axis.infoa
            elif ch == 'B':
                return axis.infob
            return axis.infoc
        except RuntimeError as e:
            msg = 'Failed to read parameter {} for driver {}.\n{}'.format(parameter, driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Read INFOx', msg)
            raise e

    def read_icepap_pcb_version(self, icepap_name, driver_addr):
        try:
            return self.iPaps[icepap_name][driver_addr].ver.driver_pcb[0]
        except RuntimeError as e:
            msg = 'Failed to read PCB version for driver {}.\n{}'.format(driver_addr, e)
            print(msg)

    def writeIcepapParameters(self, icepap_name, driver_addr, par_var_list):
        cfg_info = self.icepap_cfginfos[icepap_name][driver_addr]
        not_found = []
        for (name, value) in par_var_list:
            if name in cfg_info:
                try:
                    cmd = '{} {}'.format(name, value)
                    self.iPaps[icepap_name][driver_addr].send_cmd(cmd)
                except RuntimeError as e:
                    msg = 'Failed to write icepap parameter {} = {}\n{}'.format(name, value, e)
                    print(msg)
                    MessageDialogs.showErrorMessage(None, 'Write Param', msg)
                    raise e
            else:
                not_found.append((name, value))
        for (name, value) in not_found:
            try:
                cmd = '{} {}'.format(name, value)
                self.iPaps[icepap_name][driver_addr].send_cmd(cmd)
            except RuntimeError as e:
                    msg = 'Failed to write non-found icepap parameter {} = {}\n{}'.format(name, value, e)
                    print(msg)
                    MessageDialogs.showErrorMessage(None, 'Write Param', msg)
                    raise e

    def configDriverToDefaults(self, icepap_name, driver_addr):
        try:
            self.iPaps[icepap_name][driver_addr].set_cfg('DEFAULT')
        except RuntimeError as e:
            msg = 'Error configuring driver {} to defaults.\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Default Config', msg)
            raise e

    def _get_driver_cfg_info(self, icepap_name, driver_addr):
        try:
            cfg_info = self.iPaps[icepap_name][driver_addr].get_cfginfo()
        except RuntimeError as e:
            msg = 'Failed to retrieve cfginfo ({}).\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Driver Config Info', msg)
            raise e
        for key, val in cfg_info.items():
            if val.startswith('{'):
                cfg_info[key] = val[1:-1]
        return cfg_info

    def getDriverMotionValues(self, icepap_name, driver_addr):
        try:
            speed = self.iPaps[icepap_name][driver_addr].velocity
            acc = self.iPaps[icepap_name][driver_addr].acctime
        except RuntimeError as e:
            msg = 'Failed to retrieve motion values from driver {}.\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Driver Motion Values', msg)
            raise e
        state = (speed, acc)
        return state

    def setDriverMotionValues(self, icepap_name, driver_addr, values):
        try:
            self.iPaps[icepap_name][driver_addr].velocity = values[0]
            self.iPaps[icepap_name][driver_addr].acctime = values[1]
            return 0
        except RuntimeError as e:
            msg = 'Failed to set motion values for driver {}.\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Driver Motion Values', msg)
            return -1

    def setDriverPosition(self, icepap_name, driver_addr, pos_sel, position):
        try:
            self.iPaps[icepap_name][driver_addr].set_pos(pos_sel, position)
            return 0
        except Exception as e:
            msg = 'Failed to set driver position for selector {}\n{}'.format(pos_sel, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Set Driver Position', msg)
            return -1
    
    def setDriverEncoder(self, icepap_name, driver_addr, enc_sel, position):
        try:
            self.iPaps[icepap_name][driver_addr].set_enc(enc_sel, position)
            return 0
        except Exception as e:
            msg = 'Failed to set encoder position for selector {}\n{}'.format(enc_sel, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Set Encoder Position', msg)
            return -1
        
    def moveDriver(self, icepap_name, driver_addr, steps):
        try:
            if Mode.CONFIG in self.iPaps[icepap_name][driver_addr].mode:
                pos = int(self.iPaps[icepap_name].get_fpos(driver_addr)[0])
                self.iPaps[icepap_name][driver_addr].cmove(pos + steps)
            else:
                self.iPaps[icepap_name][driver_addr].rmove(steps)
        except RuntimeError as e:
            msg = 'Failed to move driver {}\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Move Driver', msg)

    def moveDriverAbsolute(self, icepap_name, driver_addr, pos):
        try:
            if Mode.CONFIG in self.iPaps[icepap_name][driver_addr].mode:
                self.iPaps[icepap_name][driver_addr].cmove(pos)
            else:
                self.iPaps[icepap_name][driver_addr].move(pos)
        except RuntimeError as e:
            msg = 'Failed to move driver {} to absolute position\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Move Driver Absolute', msg)

    def stopDriver(self, icepap_name, driver_addr):
        try:
            self.iPaps[icepap_name][driver_addr].stop()
        except RuntimeError as e:
            msg = 'Failed to stop driver {}\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Stop Driver', msg)

    def abortDriver(self, icepap_name, driver_addr):
        try:
            self.iPaps[icepap_name][driver_addr].abort()
        except RuntimeError as e:
            msg = 'Failed to abort driver {}\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Abort Driver', msg)

    def blinkDriver(self, icepap_name, driver_addr, secs):
        try:
            self.iPaps[icepap_name][driver_addr].blink(secs)
        except RuntimeError as e:
            msg = 'Failed to blink driver {}\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Blink Driver', msg)

    def jogDriver(self, icepap_name, driver_addr, speed):
        try:
            if Mode.CONFIG in self.iPaps[icepap_name][driver_addr].mode:
                self.iPaps[icepap_name][driver_addr].jog(speed)
            else:
                self.iPaps[icepap_name][driver_addr].cjog(speed)
        except RuntimeError as e:
            msg = 'Failed to jog driver {}\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Jog Driver', msg)

    def enableDriver(self, icepap_name, driver_addr):
        try:
            self.iPaps[icepap_name][driver_addr].power = True
        except RuntimeError as e:
            msg = 'Failed to enable driver {}\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Enable Driver', msg)

    def disableDriver(self, icepap_name, driver_addr):
        try:
            self.iPaps[icepap_name][driver_addr].power = False
        except RuntimeError as e:
            msg = 'Failed to disable driver {}\n{}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Disable Driver', msg)

    def checkIcepapStatus(self, icepap_name):
        if icepap_name not in self.iPaps:
            return False
        if not self.iPaps[icepap_name].connected:
            return False
        return True
        
    def _parseDriverTemplateFile(self):
        self.config_parameters = []
        doc = minidom.parse(self.config_template)
        root = doc.documentElement
        for section in root.getElementsByTagName("section"):
            section_name = ''
            if section.nodeType == Node.ELEMENT_NODE:
                section_name = section.attributes.get('name').value
            in_test_section = (section_name == "test")
            if not in_test_section:
                for pars in section.getElementsByTagName("par"):
                    if pars.nodeType == Node.ELEMENT_NODE:
                        parname = pars.attributes.get('name').value
                        self.config_parameters.append(str(parname))

    @staticmethod
    def getSerialPorts():
        return []

    def upgradeDrivers(self, icepap_name, progress_dialog):
        if self.programming_ipap is not None:
            return False
        self.programming_ipap = self.iPaps[icepap_name]
        self.progress_dialog = progress_dialog
        self.progress_dialog.show()
        self.updateProgressBarTimer = Qt.QTimer()
        QtCore.QObject.connect(self.updateProgressBarTimer, QtCore.SIGNAL("timeout()"), self.updateProgressBar)
        try:
            self.programming_ipap.mode = 'PROG'
        except RuntimeError as e:
            msg = 'Failed to set programming mode for firmware upgrade!\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Firmware Upgrade', msg)
            self.programming_ipap = None
            return False
        try:
            self.programming_ipap.prog('DRIVERS')
        except RuntimeError as e:
            msg = 'Failed to upgrade driver firmware!\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Firmware Upgrade', msg)
            self.programming_ipap = None
            return False
        self.updateProgressBarTimer.start(2000)
        return True

    def updateProgressBar(self):
        try:
            status = self.programming_ipap.get_prog_status()
        except RuntimeError as e:
            msg = 'Failed to request programming status!\n{}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Firmware Upgrade', msg)
            self.programming_ipap = None
            self.updateProgressBarTimer.stop()
            self.progress_dialog.cancel()
            return
        if status[0] in ['OFF', 'ERROR']:
            msg = 'Programming finished with error. Status is {}.'.format(status[0])
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Firmware Upgrade', msg)
            self.programming_ipap = None
            self.updateProgressBarTimer.stop()
            self.progress_dialog.cancel()
            return
        elif status[0] == 'ACTIVE':
            val = int(float(status[1]))
            self.progress_dialog.setValue(val)
            return
        elif status[0] == 'DONE':
            pass
        else:
            msg = 'Internal error! Bad status returned.'
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Firmware Upgrade', msg)
            self.programming_ipap = None
            self.updateProgressBarTimer.stop()
            self.progress_dialog.cancel()
            return
        self.updateProgressBarTimer.stop()
        self.progress_dialog.cancel()
        try:
            self.programming_ipap.mode = 'OPER'
        except RuntimeError as e:
            msg = 'Failed to set operating mode!\n'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Firmware Upgrade', msg)
        self.programming_ipap = None

    @staticmethod
    def error_msg(msg, logger):
        msg += '\nAborting!'
        logger.addToLog(msg)
        print(msg)
        MessageDialogs.showErrorMessage(None, 'Firmware Update', msg)

    def set_mode_oper(self, ipap, logger):
        logger.addToLog('Setting operating mode.')
        try:
            ipap.mode = 'OPER'
        except RuntimeError as e:
            self.error_msg('Failed to set operating mode!\n' + str(e), logger)

    def upgrade_firmware(self, use_serial, dst, filename, component, force, save, logger):
        # Retrieve a controller.
        if use_serial:
            # 2018-09-12
            msg = 'Serial connection is currently not supported by pyIcePAP library.'
            self.error_msg(msg, logger)
            return
        str_list = dst.split(':')
        host = str_list[0]
        port = 5000
        if len(str_list) > 1:
            port = int(str_list[1])
        try:
            ipap = EthIcePAPController(host, port)
        except RuntimeError as e:
            self.error_msg('Failed to create new ethernet controller for firmware upgrade.\n' + str(e), logger)
            return

        # Display the stored version number.
        ver = ipap.ver.system[0]
        logger.addToLog('Version before update: {}'.format(ver))

        # Set programming mode.
        logger.addToLog('Setting programming mode.')
        try:
            ipap.mode = 'PROG'
        except RuntimeError as e:
            self.error_msg('Failed to set programming mode!\n' + str(e), logger)
            return

        # Initiate programming.
        try:
            if filename.isEmpty():
                logger.addToLog('No filename provided. Using code stored in system master flash. See manual (PROG).')
                logger.addToLog('Programming. Wait...')
                ipap.prog(component, force)
            else:
                logger.addToLog('Programming. Wait...')
                ipap.sprog(component, force, save)
        except RuntimeError as e:
            self.error_msg('Programming failed.\n' + str(e), logger)
            return

        # Keep track of progress.
        wait_more = True
        while wait_more:
            time.sleep(2)
            try:
                status = ipap.get_prog_status()
            except RuntimeError as e:
                self.error_msg('Failed to request programming status!\n' + str(e), logger)
                self.set_mode_oper(ipap, logger)
                return
            if status[0] in ['OFF', 'ERROR']:
                msg = 'Programming finished with error. Status is {}.'.format(status[0])
                self.error_msg(msg, logger)
                self.set_mode_oper(ipap, logger)
                return
            elif status[0] == 'ACTIVE':
                logger.addToLog('Progress: {}%'.format(status[1]))
            elif status[0] == 'DONE':
                logger.addToLog('Programming finished ok.')
                wait_more = False
            else:
                msg = 'Internal error! Bad status returned.'
                self.error_msg(msg, logger)
                self.set_mode_oper(ipap, logger)
                return

        # Set back to operating mode.
        self.set_mode_oper(ipap, logger)

        # Reboot.
        logger.addToLog('Rebooting! Wait 60 seconds.')
        try:
            ipap.reboot()
        except RuntimeError as e:
            self.error_msg('Failed to initiate reboot!\n' + str(e), logger)
            return
        time.sleep(60)

        # Retrieve a controller.
        try:
            ipap = EthIcePAPController(host, port)
        except RuntimeError as e:
            msg = 'Failed to create ethernet controller after reboot.\n{}'.format(e)
            self.error_msg(msg, logger)
            return
        logger.addToLog('Now we are connected again.')

        # Display the stored version number.
        ver = ipap.ver.system[0]
        logger.addToLog('Version after update: {}'.format(ver))
        logger.addToLog('DONE!')

    @staticmethod
    def testConnection(serial, dst):
        if serial:
            # 2018-09-12
            msg = 'Serial connection is currently not supported by pyIcePAP library.'
            print(msg)
            return False

        # Connected via Ethernet.
        if dst.find(':') >= 0:
            str_list = dst.split(':')
            host = str_list[0]
            port = int(str_list[1])
        else:
            host = dst
            port = 5000
        try:
            ipap = EthIcePAPController(host, port)
            sys_ver = ipap.ver.system[0]
            msg = 'Testing Ethernet connection: System version is {}'.format(sys_ver)
            print(msg)
        except RuntimeError as e:
            msg = 'Failed to create new Ethernet connected controller for connection test.\n{}'.format(e)
            print(msg)
            return False
        return True

    @staticmethod
    def _find_networks(configs, addr_pattern, mask_pattern):
        addr_parse = re.compile(addr_pattern)
        mask_parse = re.compile(mask_pattern)
        networks = []
        for config in configs:
            addr = addr_parse.search(config)
            mask = mask_parse.search(config)
            if addr and mask:
                net = IP(addr.group(2) + "/" + mask.group(2), make_net=True)
                networks.append(net)
        return networks
  
    def host_in_same_subnet(self, host):
        if self._config._options.allnets:
            return True

        networks = []
        configs = None
        addr_pattern = None
        mask_pattern = None
        digits = r'[0-9]{1,3}'

        if os.name == 'posix':
            ifconfigs = ['/sbin/ifconfig', '/usr/sbin/ifconfig', '/bin/ifconfig', '/usr/bin/ifconfig']
            ifconfig = filter(os.path.exists, ifconfigs)[0]
            fp = os.popen(ifconfig + ' -a')
            configs = fp.read().split('\n\n')
            fp.close()
            addr_pattern = r'(inet ) *(%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
            mask_pattern = r'(netmask ) *(%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
        elif os.name == 'nt':
            fp = os.popen('ipconfig /all')
            configs = fp.read().split(':\r\n\r\n')
            fp.close()
            addr_pattern = r'(IPv4 Address).*: (%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
            mask_pattern = r'(Subnet Mask).*: (%s\.%s\.%s\.%s)[^0-9]' % ((digits,)*4)
  
        if configs and addr_pattern and mask_pattern:
            networks = self._find_networks(configs, addr_pattern, mask_pattern)
  
        if len(networks) > 0:
            host_addr = socket.gethostbyname(host)
            for net in networks:
                if host_addr in net:
                    return True
            return False
        else:
            msg = "Sorry system not yet supported.\nWe allow you access to the icepap even if it is in another subnet."
            MessageDialogs.showInformationMessage(None, "Not Posix Operating System", msg)
            return True

    def is_expert_flag_set(self, system, addr):
        try:
            cfg = self.iPaps[system][addr].get_cfg('EXPERT')
        except RuntimeError as e:
            msg = 'Failed to retrieve EXPERT flag from driver {}.\n{}'.format(addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Expert Flag', msg)
            return False
        return cfg['EXPERT'] == 'YES'
