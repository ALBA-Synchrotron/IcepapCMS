# !/usr/bin/env python
# ------------------------------------------------------------------------------
# This file is part of IcepapCMS
#      https://github.com/ALBA-Synchrotron/icepapcms
#
# Copyright 2008-2018 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Distributed under the terms of the GNU General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# ------------------------------------------------------------------------------


from pyIcePAP import EthIcePAPController, Mode
from xml.dom import minidom, Node
import os
import sys
from singleton import Singleton
import datetime
from icepapdrivercfg import IcepapDriverCfg
import icepapdriver
from configmanager import ConfigManager
from ..ui_icepapcms.messagedialogs import MessageDialogs
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
            ipap = self._config.icepap
            debug_set = self._config.config[ipap]["debug_enabled"]
            self.debug = debug_set == str(True)
            self.log_folder = self._config.config[ipap]["log_folder"]
            if not os.path.exists(self.log_folder):
                os.mkdir(self.log_folder)
        except Exception:
            print "icepapcontroller_init():", sys.exc_info()
            pass

    def reset(self):
        self.closeAllConnections()
        self.iPaps = {}

    def openConnection(self, icepap_name, host, port):
        # TODO: Configure logging
        # log_folder = None
        # if self.debug:
        #     log_folder = self.log_folder
        if not self.host_in_same_subnet(icepap_name):
            MessageDialogs.showInformationMessage(None, "Host connection",
                                                  "It is not allowed to "
                                                  "connect to %s. (Check "
                                                  "subnet)" % host)
            return False
        else:
            try:
                # TODO: Configure logging log_path=log_folder
                self.iPaps[icepap_name] = EthIcePAPController(host, port)
                return True
            except Exception:
                return False

    def closeConnection(self, icepap_name):
        if icepap_name in self.iPaps:
            self.iPaps[icepap_name].disconnect()
            del self.iPaps[icepap_name]

    def closeAllConnections(self):
        for iPap in self.iPaps.values():
            try:
                iPap.disconnect()
            except Exception:
                pass
        self.iPaps = {}

    def _get_driver_cfg_info(self, icepap_name, driver_addr):
        try:
            cfg_info = self.iPaps[icepap_name][driver_addr].get_cfginfo()
        except RuntimeError as e:
            msg = 'Failed to retrieve cfginfo ' \
                  '({0}).\n{1}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Driver Config Info', msg)
            raise e
        for key, val in cfg_info.items():
            if val.startswith('{'):
                val = val.replace("{", "")
                val = val.replace("}", "")
            val = val.split()
            cfg_info[key] = val
        return cfg_info

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
            # IMPROVE OF SPEED BY SAVING CFGINFOS BY VERSION
            cfginfos_version_dict = {}
            for addr in self.iPaps[icepap_name]:
                """ TO-DO STORM review"""
                driver = icepapdriver.IcepapDriver(driver_name, addr)
                driver_cfg = self.getDriverConfiguration(icepap_name, addr)
                driver.addConfiguration(driver_cfg)

                # CFGINFO IS ALSO SPECIFIC FOR EACH DRIVER
                # To improve speed, this is true but instead of 'each driver',
                # better each version
                driver_version = driver_cfg.getParameter(unicode('VER'), True)
                if driver_version not in cfginfos_version_dict:
                    cfginfos_version_dict[driver_version] = \
                        self._get_driver_cfg_info(icepap_name, addr)

                # GET CFGINFO FROM CACHED DICT INSTEAD OF QUERYING EACH TIME
                cfginfo_dict = cfginfos_version_dict[driver_version]
                self.icepap_cfginfos[icepap_name][addr] = cfginfo_dict

                driver.setName(driver_cfg.getParameter(
                    unicode("IPAPNAME"), True))
                driver.setMode(self.iPaps[icepap_name][addr].mode)
                driver_list[addr] = driver

        except Exception as e:
            self.closeConnection(icepap_name)
            print 'exception:', e
            raise
        return driver_list

    def getDriverConfiguration(self, icepap_name, driver_addr):
        """
            Returns a IcepaDriverCfg object of the attributes predefined in
            driverparameters.xml
        """

        """ TO-DO STORM review"""
        driver_cfg = IcepapDriverCfg(unicode(datetime.datetime.now()))
        axis = self.iPaps[icepap_name][driver_addr]
        try:
            driver_cfg.setSignature(axis.config)
        except Exception as e:
            msg = 'Failed to retrieve configuration for ' \
                  'driver {0}.\n{1}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Get Driver Config', msg)
            raise e

        # THE VERSION NUMBER TO BE SHOWN IS THE DRIVER'S VERSION INSTEAD OF
        # THE DSP'S ONE.
        axis_name = axis.name
        # FIX NON-ASCII CHARS ISSUE IN NAME:
        if not all(ord(c) < 128 for c in axis_name):
            axis_name = repr(axis.name)
        driver_cfg.setParameter(unicode("VER"), axis.ver.driver[0])
        driver_cfg.setParameter(unicode("ID"), axis.id)
        try:
            driver_cfg.setParameter(unicode("IPAPNAME"), axis_name)
        except Exception as e:
            msg = 'Exception when trying to write the driver name ' \
                  '(%s):' % axis_name
            print msg
            print e
            axis_name = 'NON-ASCII_NAME'
            driver_cfg.setParameter(unicode("IPAPNAME"), axis_name)

        # INSTEAD OF READING PARAM BY PARAM, WE SHOULD ASK THE ICEPAP FOR
        # ALL THE CONFIGURATION
        # WITH THE #N?:CFG COMMAND, USING SOME .getCfg() METHOD.
        axis = self.iPaps[icepap_name][driver_addr]
        cfg = axis.get_cfg()
        for param_name, param_value in cfg.items():
            driver_cfg.setParameter(unicode(param_name), param_value)

        return driver_cfg

    def setDriverConfiguration(self, icepap_name, driver_addr, new_values,
                               expertFlag=False):
        """ TO-DO STORM review"""
        axis = self.iPaps[icepap_name][driver_addr]
        try:
            if Mode.CONFIG not in axis.mode:
                axis.set_config()
        except RuntimeError as e:
            msg = 'Failed to set driver {0} in CONFIG mode.\n{1}'.format(
                driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Set Driver Mode', msg)
            raise e

        # Convert the new_values list in a dictionary
        new_values_dict = {}
        for name, value in new_values:
            new_values_dict[name] = value

        # THE CONFIGURATION VALUES SHOULD BE SENT IN A SPECIFIC ORDER
        cfg_info = self.icepap_cfginfos[icepap_name][driver_addr]
        for cfg_name in cfg_info:
            if cfg_name in new_values_dict:
                try:
                    value = str(new_values_dict.pop(cfg_name))
                    axis.set_cfg(cfg_name, value)
                except Exception as e:
                    msg = 'Error configuring parameter {0} = {1} for driver ' \
                          '{2}\n{3}'.format(cfg_name, value, driver_addr, e)
                    print(msg)
                    MessageDialogs.showErrorMessage(None, 'Set Driver Config',
                                                    msg)
                    raise e

        # The new_values will have the the not found parameter on the
        # configuration dictionary
        for cfg_name, value in new_values_dict.items():
            if cfg_name.upper() in ['VER', 'ID']:
                # Ignore the change
                pass
            elif cfg_name.upper() in ['NAME', 'IPAPNAME']:
                try:
                    have_namelock = False
                    cfg = axis.get_cfg()
                    # IN CASE OF NAMELOCK SET TO YES, UNLOCK FIRST
                    have_namelock = cfg['NAMELOCK'].upper() == 'YES'
                    if have_namelock:
                        axis.set_cfg('NAMELOCK', 'NO')
                    axis.name = value
                except Exception as e:
                    msg = 'Error configuring parameter ' \
                          '{0} = {1}\n{2}'.format(cfg_name, value, e)
                    print(msg)
                    MessageDialogs.showErrorMessage(None, 'Set Driver Config',
                                                    msg)
                finally:
                    if have_namelock:
                        axis.set_cfg('NAMELOCK', 'YES')
            else:
                msg = 'Parameter {0}({1}) is not exist for the current ' \
                      'version. Check the configuration ' \
                      'parameter list ({2}).'.format(cfg_name, value,
                                                    cfg_info.keys())
                print(msg)
                MessageDialogs.showErrorMessage(None, 'Set Driver Config', msg)
                raise ValueError(msg)
        try:
            if expertFlag:
                axis.set_cfg('EXPERT')
        except Exception as e:
            msg = 'Error setting expert flag.{0}\n'.format(e)
            MessageDialogs.showErrorMessage(None, 'Expert flag', msg)
            print(msg)
            raise e

        driver_cfg = self.getDriverConfiguration(icepap_name, driver_addr)
        return driver_cfg

    def discardDriverCfg(self, icepap_name, driver_addr):
        try:
            if icepap_name in self.iPaps:
                self.iPaps[icepap_name][driver_addr].set_config()
        except RuntimeError as e:
            msg = 'Error discarding driver config.\n{0}'.format(e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Discard Driver Config', msg)
            raise e

    def signDriverConfiguration(self, icepap_name, driver_addr, signature):
        try:
            if icepap_name in self.iPaps:
                axis = self.iPaps[icepap_name][driver_addr]
                if Mode.CONFIG not in axis.mode:
                    axis.set_config()
                axis.set_config(signature)
        except RuntimeError as e:
            msg = 'Error signing config.\n{0}'.format(e)
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
            msg = 'Error starting config.\n{0}'.format(e)
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
            msg = 'Error ending config for driver ' \
                  '{0}.\n{1}'.format(driver.addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'End Config', msg)
            raise e

    def getDriverStatus(self, icepap_name, driver_addr):
        """
        Returns an array with the Status, Limit Switches and Current of the
        driver
        """
        if not self.iPaps[icepap_name].connected:
            state = (-1, False, -1)
            return state
        if self.programming_ipap is not None:
            state = (-1, False, -1)
            return state
        try:
            axis_state = self.iPaps[icepap_name].get_states(driver_addr)[0]
            power = axis_state.is_poweron()
            cfg_current = self.iPaps[icepap_name][driver_addr].get_cfg('NCURR')
            current = cfg_current['NCURR']
            status_register = axis_state.status_register
            return status_register, power, current
        except Exception:
            msg = 'Failed to retrieve status for ' \
                  'driver {0}.\n{1}'.format(driver_addr, e)
            print(msg)
            return -1, False, -1

    def getDriverTestStatus(self, icepap_name, driver_addr, pos_sel, enc_sel):
        """
        Returns an array with the Status, Limit Switches and Position of
        the driver
        """
        if self.programming_ipap is not None:
            return -1, -1, [-1, -1]

        axis_state = self.iPaps[icepap_name].get_states(driver_addr)[0]
        register = axis_state.status_register
        power = axis_state.is_poweron()

        axis = self.iPaps[icepap_name][driver_addr]
        try:
            position = axis.get_pos(pos_sel)
        except Exception as e:
            msg = 'Failed to retrieve position for driver ' \
                  '{0}.\n{1}'. format(driver_addr, e)
            print(msg)
            position = -1

        try:
            encoder = axis.get_enc(enc_sel)
        except Exception as e:
            msg = 'Failed to retrieve encoder for driver ' \
                  '{0}.\n{1}'.format(driver_addr, e)
            print(msg)
            encoder = -1

        return register, power, [position, encoder]

    def getDriverActiveStatus(self, icepap_name, driver_addr):
        try:
            active = self.iPaps[icepap_name][driver_addr]
            if active:
                return 'YES'
            else:
                return 'NO'
        except Exception as e:
            msg = 'Failed to read activation status for ' \
                  'driver {0}.\n{1}'.format(driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Get Active', msg)
            raise e

    def readIcepapParameters(self, icepap_name, driver_addr, par_list):
        axis = self.iPaps[icepap_name][driver_addr]
        try:
            values = []
            for name in par_list:
                if type(name) == type(values):
                    cmd = '?{0} {1}'.format(name[0], name[1])
                else:
                    cmd = '?{0}'.format(name)

                value = ' '.join(axis.send_cmd(cmd))
                values.append([name, value])

            return values
        except Exception as e:
            msg = 'Failed to read parameter {0} ' \
                  'for driver {1}.\n{2}'.format(name, driver_addr, e)
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Read Param', msg)
            raise e

    def writeIcepapParameters(self, icepap_name, driver_addr, par_var_list):
        # This method is only called with the command widgets changes, not with
        # the configuration widgets changes. For that reason it is not
        # needed to send the parameter in any specific order.
        axis = self.iPaps[icepap_name][driver_addr]
        for param, value in par_var_list:
            cmd = '{0} {1}'.format(param, value)
            try:
                axis.send_cmd(cmd)
            except Exception as e:
                msg = 'Failed to write icepap ' \
                      'parameter {0} = {1}\n{2}'.format(param, value, e)
                print(msg)
                MessageDialogs.showErrorMessage(None, 'Write Param', msg)
                raise e

    def configDriverToDefaults(self, icepap_name, driver_addr):
        try:
            self.iPaps[icepap_name].setDefaultConfig(driver_addr)
        except IcePAPException as iex:
            msg = 'Error configuring to defaults.'
            msg += '\n' + iex.msg
            MessageDialogs.showErrorMessage(None, 'default config', msg)
            print iex.msg
            raise iex

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
        except Exception:
            return -1

    def setDriverPosition(self, icepap_name, driver_addr, pos_sel, position):
        try:
            self.iPaps[icepap_name].setPosition(driver_addr, position, pos_sel)
            return 0
        except Exception:
            return -1

    def setDriverEncoder(self, icepap_name, driver_addr, enc_sel, position):
        try:
            self.iPaps[icepap_name].setEncoder(driver_addr, position, enc_sel)
            return 0
        except Exception:
            return -1

    def moveDriver(self, icepap_name, driver_addr, steps):
        axis = self.iPaps[icepap_name][driver_addr]
        if Mode.CONFIG in axis.mode:
            # CMOVE ONLY ALLOWS ABSOLUTE POSITIONS, IT SHOULD BE CALCULATED
            # self.iPaps[icepap_name].cmove(driver_addr, steps)
            new_pos = axis.pos + int(steps)
            axis.cmove(new_pos)
        else:
            axis.rmove(steps)

    def moveDriverAbsolute(self, icepap_name, driver_addr, pos):
        axis = self.iPaps[icepap_name][driver_addr]
        if Mode.CONFIG in axis.mode:
            axis.cmove(pos)
        else:
            axis.move(pos)

    def stopDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name][driver_addr].stop()

    def abortDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name][driver_addr].abort()

    def blinkDriver(self, icepap_name, driver_addr, secs):
        self.iPaps[icepap_name][driver_addr].blink(secs)

    def jogDriver(self, icepap_name, driver_addr, speed):
        axis =self.iPaps[icepap_name][driver_addr]
        if Mode.CONFIG not in axis.mode:
            self.iPaps[icepap_name][driver_addr].jog(speed)
        else:
            self.iPaps[icepap_name][driver_addr].cjog(speed)

    def enableDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name][driver_addr].power = True

    def disableDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name][driver_addr].power = False

    def checkIcepapStatus(self, icepap_name):
        if icepap_name not in self.iPaps \
                or not self.iPaps[icepap_name].connected:
            return False
        return True

    def isExpertFlagSet(self, icepap_name, driver_addr):
        axis = self.iPaps[icepap_name][driver_addr]
        try:
            return axis.get_cfg('EXPERT')['EXPERT']
        except Exception:
            return 'NO'

    def _parseDriverTemplateFile(self):
        self.config_parameters = []
        doc = minidom.parse(self.config_template)
        root = doc.documentElement
        for section in root.getElementsByTagName("section"):
            if section.nodeType == Node.ELEMENT_NODE:
                    section_name = section.attributes.get('name').value
            inTestSection = (section_name == "test")
            if not inTestSection:
                for pars in section.getElementsByTagName("par"):
                    if pars.nodeType == Node.ELEMENT_NODE:
                        parname = pars.attributes.get('name').value
                        self.config_parameters.append(str(parname))

    def getSerialPorts(self):
        try:
            return IcePAP.serialScan()
        except Exception:
            return []

    def upgradeDrivers(self, icepap_name, progress_dialog):
        if self.programming_ipap is not None:
            return False
        self.programming_ipap = self.iPaps[icepap_name]
        self.progress_dialog = progress_dialog
        self.progress_dialog.show()
        self.updateProgressBarTimer = Qt.QTimer()
        QtCore.QObject.connect(self.updateProgressBarTimer,
                               QtCore.SIGNAL("timeout()"),
                               self.updateProgressBar)
        cmd = "#MODE PROG"
        answer = self.programming_ipap.sendWriteReadCommand(cmd)
        if answer != "MODE OK":
            print("icepapcontroller:upgradeDrivers:Some error trying to set "
                  "mode PROG:", answer)
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
            self.programming_ipap.sendWriteReadCommand(cmd)
            self.programming_ipap = None

        # cmd = "?PROG"
        # answer = self.programming_ipap.sendWriteReadCommand(cmd)
        # if answer.count("ACTIVE") > 0:
        #     p = int(answer.split(" ")[2].split(".")[0])
        #     self.progress_dialog.setValue(p)
        # else:
        #     self.progress_dialog.setValue(100)
        #     self.updateProgressBarTimer.stop()
        #     cmd = "#MODE OPER"
        #     answer = self.programming_ipap.sendWriteReadCommand(cmd)
        #     self.programming_ipap = None

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

            ipap = EthIcePAP(host, port)

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
                ipap = EthIcePAP(host, port)
            ipap.connect()
            ipap.getSystemVersion()
            print "testing connection"
            ipap.disconnect()
            return True
        except Exception:
            return False

    def find_networks(self, configs, addr_pattern, mask_pattern):
        addr_parse = re.compile(addr_pattern)
        mask_parse = re.compile(mask_pattern)
        networks = []
        for config in configs:
            addr = addr_parse.search(config)
            mask = mask_parse.search(config)
            if addr and mask:
                net = IP(addr.group(2)+"/"+mask.group(2), make_net=True)
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
            ifconfigs = ['/sbin/ifconfig', '/usr/sbin/ifconfig',
                         '/bin/ifconfig', '/usr/bin/ifconfig']
            ifconfig = filter(os.path.exists, ifconfigs)[0]
            fp = os.popen(ifconfig+' -a')
            configs = fp.read().split('\n\n')
            fp.close()
            # 180214 - Adapted to Debian9 "/sbin/ifconfig -a" output
            # addr_pattern = r'(inet addr:) *(%s\.%s\.%s\.%s)[^0-9]' \
            #   % ((digits,)*4)
            # mask_pattern = r'(Mask:) *(%s\.%s\.%s\.%s)[^0-9]' \
            #   % ((digits,)*4)
            addr_pattern = r'(inet ) *(%s\.%s\.%s\.%s)' \
                           r'[^0-9]' % ((digits,)*4)
            mask_pattern = r'(netmask ) *(%s\.%s\.%s\.%s)' \
                           r'[^0-9]' % ((digits,)*4)
        elif os.name == 'nt':
            fp = os.popen('ipconfig /all')
            configs = fp.read().split(':\r\n\r\n')
            fp.close()
            # 180214 - Adapted to Windows7 "ipconfig /all" output
            # addr_pattern = r'(IP Address).*: (%s\.%s\.%s\.%s)[^0-9]' % ((
            # digits,)*4)
            addr_pattern = r'(IPv4 Address).*: (%s\.%s\.%s\.%s)' \
                           r'[^0-9]' % ((digits,)*4)
            mask_pattern = r'(Subnet Mask).*: (%s\.%s\.%s\.%s)' \
                           r'[^0-9]' % ((digits,)*4)

        if configs and addr_pattern and mask_pattern:
            networks = self.find_networks(configs, addr_pattern, mask_pattern)

        if len(networks) > 0:
            host_addr = socket.gethostbyname(host)
            for net in networks:
                if host_addr in net:
                    return True
            return False
        else:
            msg = "Sorry system not yet supported.\nWe allow you access to " \
                  "the icepap even if it is in another subnet."
            MessageDialogs.showInformationMessage(None,
                                                  "Not posix operating system",
                                                  msg)
            return True
