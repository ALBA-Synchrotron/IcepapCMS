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

#Remove the QT depency on the update driver
from PyQt5 import Qt
from icepap import IcePAPController, Mode
from pkg_resources import resource_filename
from xml.dom import minidom, Node
import os
import re
import socket
import collections
from IPy import IP
import datetime
import logging
import time
from .singleton import Singleton
from .icepapdrivercfg import IcepapDriverCfg
from . import icepapdriver
from .configmanager import ConfigManager
from ..gui.messagedialogs import MessageDialogs
from ..helpers import loggingInfo, catchError

__all__ = ['IcepapsManager']


class IcepapsManager(Singleton):
    log = logging.getLogger('{}.IcepapController'.format(__name__))

    def __init__(self):
        pass

    @loggingInfo
    def init(self, *args):
        self.iPaps = {}
        self.config_template = resource_filename('icepapcms.templates',
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
        except Exception as e:
            self.log.error("Init error %s", e)
            pass

    @loggingInfo
    def reset(self):
        self.closeAllConnections()
        self.iPaps = {}

    @loggingInfo
    def openConnection(self, icepap_name, host, port):
        if not self.host_in_same_subnet(icepap_name):
            MessageDialogs.showInformationMessage(None, "Host connection",
                                                  "It is not allowed to "
                                                  "connect to %s. (Check "
                                                  "subnet)" % host)
            return False
        else:
            try:
                # TODO Optimize GUI to avoid auto_axes=True
                self.iPaps[icepap_name] = IcePAPController(host, int(port),
                                                           auto_axes=True)
                return True
            except Exception as e:
                self.log.error('Open Connection error %s', e)
                return False

    @loggingInfo
    def closeConnection(self, icepap_name):
        if icepap_name in self.iPaps:
            self.iPaps[icepap_name].disconnect()
            del self.iPaps[icepap_name]

    @loggingInfo
    def closeAllConnections(self):
        for iPap in list(self.iPaps.values()):
            try:
                iPap.disconnect()
            except Exception:
                pass
        self.iPaps = {}

    @loggingInfo
    def _get_driver_cfg_info(self, icepap_name, driver_addr):
        try:
            cfg_info = self.iPaps[icepap_name][driver_addr].get_cfginfo()
        except RuntimeError as e:
            msg = 'Failed to retrieve cfginfo ' \
                  '({0}).\n{1}'.format(driver_addr, e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'Driver Config Info', msg)
            raise e
        for key, val in list(cfg_info.items()):
            if val.startswith('{'):
                val = val.replace("{", "")
                val = val.replace("}", "")
            val = val.split()
            cfg_info[key] = val
        return cfg_info

    @loggingInfo
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
                driver_version = driver_cfg.getParameter('VER', True)
                if driver_version not in cfginfos_version_dict:
                    cfginfos_version_dict[driver_version] = \
                        self._get_driver_cfg_info(icepap_name, addr)

                # GET CFGINFO FROM CACHED DICT INSTEAD OF QUERYING EACH TIME
                cfginfo_dict = cfginfos_version_dict[driver_version]
                self.icepap_cfginfos[icepap_name][addr] = cfginfo_dict

                driver.setName(driver_cfg.getParameter("IPAPNAME", True))
                driver.setMode(self.iPaps[icepap_name][addr].mode)
                driver_list[addr] = driver

        except Exception as e:
            self.closeConnection(icepap_name)
            self.log.error('Scan Icepap System error: %s', e)
            raise
        return driver_list

    @loggingInfo
    def getDriverConfiguration(self, icepap_name, driver_addr):
        """
            Returns a IcepaDriverCfg object of the attributes predefined in
            driverparameters.xml
        """

        """ TO-DO STORM review"""
        driver_cfg = IcepapDriverCfg(str(datetime.datetime.now()))
        axis = self.iPaps[icepap_name][driver_addr]
        try:
            driver_cfg.setSignature(axis.config)
        except Exception as e:
            msg = 'Failed to retrieve configuration for ' \
                  'driver {0}.\n{1}'.format(driver_addr, e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'Get Driver Config', msg)
            raise e

        # THE VERSION NUMBER TO BE SHOWN IS THE DRIVER'S VERSION INSTEAD OF
        # THE DSP'S ONE.
        axis_name = axis.name
        # FIX NON-ASCII CHARS ISSUE IN NAME:
        if axis_name is not None and not all(ord(c) < 128 for c in axis_name):
            axis_name = repr(axis.name)
        driver_cfg.setParameter("VER", axis.ver.driver[0])
        driver_cfg.setParameter("ID", axis.id)
        try:
            driver_cfg.setParameter("IPAPNAME", axis_name)
        except Exception as e:
            self.log.error('Exception when trying to write the driver name ' \
                           '(%s): %s', axis, e)

            axis_name = 'NON-ASCII_NAME'
            driver_cfg.setParameter("IPAPNAME", axis_name)

        # INSTEAD OF READING PARAM BY PARAM, WE SHOULD ASK THE ICEPAP FOR
        # ALL THE CONFIGURATION
        # WITH THE #N?:CFG COMMAND, USING SOME .getCfg() METHOD.
        axis = self.iPaps[icepap_name][driver_addr]
        cfg = axis.get_cfg()
        for param_name, param_value in list(cfg.items()):
            driver_cfg.setParameter(str(param_name), param_value)

        return driver_cfg

    @loggingInfo
    def setDriverConfiguration(self, icepap_name, driver_addr, new_values,
                               expertFlag=False):
        """ TO-DO STORM review"""
        axis = self.iPaps[icepap_name][driver_addr]
        try:
            if Mode.CONFIG != axis.mode:
                axis.set_config()
        except RuntimeError as e:
            msg = 'Failed to set driver {0} in CONFIG mode.\n{1}'.format(
                driver_addr, e)
            self.log.error(msg)
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
                    self.log.error(msg)
                    MessageDialogs.showErrorMessage(None, 'Set Driver Config',
                                                    msg)
                    raise e

        # The new_values will have the the not found parameter on the
        # configuration dictionary
        for cfg_name, value in list(new_values_dict.items()):
            if cfg_name.upper() in ['VER', 'ID']:
                # Ignore the change
                pass
            elif cfg_name.upper() in ['NAME', 'IPAPNAME']:
                have_namelock = False
                try:
                    cfg = axis.get_cfg()
                    # IN CASE OF NAMELOCK SET TO YES, UNLOCK FIRST
                    have_namelock = cfg['NAMELOCK'].upper() == 'YES'
                    if have_namelock:
                        axis.set_cfg('NAMELOCK', 'NO')
                    axis.name = value
                except Exception as e:
                    msg = 'Error configuring parameter ' \
                          '{0} = {1}\n{2}'.format(cfg_name, value, e)
                    self.log.error(msg)
                    MessageDialogs.showErrorMessage(None, 'Set Driver Config',
                                                    msg)
                finally:
                    if have_namelock:
                        axis.set_cfg('NAMELOCK', 'YES')
            else:
                msg = 'Parameter {0}({1}) is not exist for the current ' \
                      'version. Check the configuration ' \
                      'parameter list ({2}).'.format(cfg_name, value,
                                                     list(cfg_info.keys()))
                self.log.error(msg)
                MessageDialogs.showErrorMessage(None, 'Set Driver Config', msg)
                raise ValueError(msg)
        try:
            if expertFlag:
                axis.set_cfg('EXPERT')
        except Exception as e:
            msg = 'Error setting expert flag.{0}\n'.format(e)
            MessageDialogs.showErrorMessage(None, 'Expert flag', msg)
            self.log.error(msg)
            raise e

        driver_cfg = self.getDriverConfiguration(icepap_name, driver_addr)
        return driver_cfg

    @loggingInfo
    def discardDriverCfg(self, icepap_name, driver_addr):
        try:
            if icepap_name in self.iPaps:
                self.iPaps[icepap_name][driver_addr].set_config()
        except RuntimeError as e:
            msg = 'Error discarding driver config.\n{0}'.format(e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'Discard Driver Config', msg)
            raise e

    @loggingInfo
    def signDriverConfiguration(self, icepap_name, driver_addr, signature):
        try:
            if icepap_name in self.iPaps:
                axis = self.iPaps[icepap_name][driver_addr]
                if Mode.CONFIG != axis.mode:
                    axis.set_config()
                axis.set_config(signature)
        except RuntimeError as e:
            msg = 'Error signing config.\n{0}'.format(e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'Sign Driver', msg)
            raise e

    @loggingInfo
    def startConfiguringDriver(self, icepap_name, driver):
        try:
            mode = self.iPaps[icepap_name][driver.addr].mode
            if Mode.PROG == mode:
                return mode[0]
            if Mode.CONFIG != mode:
                self.iPaps[icepap_name][driver.addr].set_config()
            driver.setMode(Mode.CONFIG)
        except RuntimeError as e:
            msg = 'Error starting config.\n{0}'.format(e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'config', msg)
            raise e
        return mode[0]

    @loggingInfo
    def endConfiguringDriver(self, icepap_name, driver):
        try:
            if icepap_name not in self.iPaps:
                return
            axis = self.iPaps[icepap_name][driver.addr]
            if Mode.PROG == axis.mode:
                return
            if Mode.OPER != axis.mode:
                last_signature = axis.config
                axis.set_config(last_signature)
            driver.setMode(Mode.OPER)
        except RuntimeError as e:
            msg = 'Error ending config for driver ' \
                  '{0}.\n{1}'.format(driver.addr, e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'End Config', msg)
            raise e

    @loggingInfo
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
            # TODO: Change the ui to use boolean instead of integers
            power = int(axis_state.is_poweron())
            cfg_current = self.iPaps[icepap_name][driver_addr].get_cfg('NCURR')
            current = cfg_current['NCURR']
            status_register = axis_state.status_register
            return status_register, power, current
        except Exception as e:
            self.log.error('Failed to retrieve status for driver %d: %s',
                           driver_addr, e)
            return -1, False, -1

    @loggingInfo
    def getDriverTestStatus(self, icepap_name, driver_addr, pos_sel, enc_sel):
        """
        Returns an array with the Status, Limit Switches and Position of
        the driver
        """
        if self.programming_ipap is not None:
            return -1, -1, [-1, -1]

        axis_state = self.iPaps[icepap_name].get_states(driver_addr)[0]
        register = axis_state.status_register
        power = int(axis_state.is_poweron())

        axis = self.iPaps[icepap_name][driver_addr]
        try:
            position = axis.get_pos(pos_sel)
        except Exception as e:
            self.log.error('Failed to retrieve position for driver %d: %s',
                           driver_addr, e)

            position = -1

        try:
            encoder = axis.get_enc(enc_sel)
        except Exception as e:
            self.log.error('Failed to retrieve encoder for driver %d: %s',
                           driver_addr, e)
            encoder = -1

        return register, power, [position, encoder]

    @loggingInfo
    def getDriverActiveStatus(self, icepap_name, driver_addr):
        try:
            active = self.iPaps[icepap_name][driver_addr].active
            if active:
                return 'YES'
            else:
                return 'NO'
        except Exception as e:
            msg = 'Failed to read activation status for ' \
                  'driver {0}.\n{1}'.format(driver_addr, e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'Get Active', msg)
            raise e

    @loggingInfo
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
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'Read Param', msg)
            raise e

    @loggingInfo
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
                self.log.error(msg)
                MessageDialogs.showErrorMessage(None, 'Write Param', msg)
                raise e

    @loggingInfo
    def configDriverToDefaults(self, icepap_name, driver_addr):
        try:
            self.iPaps[icepap_name][driver_addr].set_cfg('DEFAULT')
        except RuntimeError as e:
            msg = 'Error configuring driver {0} to ' \
                  'defaults.\n{1}'.format(driver_addr, e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'Default Config', msg)
            raise e

    @loggingInfo
    def getDriverMotionValues(self, icepap_name, driver_addr):
        try:
            speed = self.iPaps[icepap_name][driver_addr].velocity
            acc = self.iPaps[icepap_name][driver_addr].acctime
        except RuntimeError as e:
            msg = 'Failed to retrieve motion values(velocity, acctime) ' \
                  'from driver {0}.\n{1}'.format(driver_addr, e)
            self.log.error(msg)
            MessageDialogs.showErrorMessage(None, 'Driver Motion Values', msg)
            raise e
        return speed, acc

    @loggingInfo
    def setDriverMotionValues(self, icepap_name, driver_addr, values):
        try:
            self.iPaps[icepap_name][driver_addr].velocity = values[0]
            self.iPaps[icepap_name][driver_addr].acctime = values[1]
            return 0
        except Exception as e:
            msg = 'Failed to set motion values for ' \
                  'driver {0}.\n{1}'.format(driver_addr, e)
            self.log.error(msg)
            return -1

    @loggingInfo
    def setDriverPosition(self, icepap_name, driver_addr, pos_sel, position):
        try:
            self.iPaps[icepap_name][driver_addr].set_pos(pos_sel, position)
            return 0
        except Exception as e:
            msg = 'Failed to set driver position for ' \
                  'selector {0}\n{1}'.format(pos_sel, e)
            self.log.error(msg)
            return -1

    @loggingInfo
    def setDriverEncoder(self, icepap_name, driver_addr, enc_sel, position):
        try:
            self.iPaps[icepap_name][driver_addr].set_enc(enc_sel, position)
            return 0
        except Exception as e:

            self.log.error('Failed to set encoder position for selector %d: '
                           '%s', enc_sel, e)
            return -1

    @catchError()
    def moveDriver(self, icepap_name, driver_addr, steps):
        axis = self.iPaps[icepap_name][driver_addr]
        if Mode.CONFIG == axis.mode:
            # CMOVE ONLY ALLOWS ABSOLUTE POSITIONS, IT SHOULD BE CALCULATED
            # self.iPaps[icepap_name].cmove(driver_addr, steps)
            new_pos = axis.pos + int(steps)
            axis.cmove(new_pos)
        else:
            axis.rmove(steps)

    @catchError()
    def moveDriverAbsolute(self, icepap_name, driver_addr, pos):
        axis = self.iPaps[icepap_name][driver_addr]
        if Mode.CONFIG == axis.mode:
            axis.cmove(pos)
        else:
            axis.move(pos)

    @catchError()
    def stopDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name][driver_addr].stop()

    @catchError()
    def abortDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name][driver_addr].abort()

    @catchError()
    def blinkDriver(self, icepap_name, driver_addr, secs):
        self.iPaps[icepap_name][driver_addr].blink(secs)

    @catchError()
    def jogDriver(self, icepap_name, driver_addr, speed):
        axis = self.iPaps[icepap_name][driver_addr]
        if Mode.CONFIG != axis.mode:
            self.iPaps[icepap_name][driver_addr].jog(speed)
        else:
            self.iPaps[icepap_name][driver_addr].cjog(speed)

    @catchError('Check driver status')
    def enableDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name][driver_addr].power = True

    @catchError('Check driver status')
    def disableDriver(self, icepap_name, driver_addr):
        self.iPaps[icepap_name][driver_addr].power = False

    @catchError()
    def checkIcepapStatus(self, icepap_name):
        if icepap_name not in self.iPaps \
                or not self.iPaps[icepap_name].connected:
            return False
        return True

    @loggingInfo
    def isExpertFlagSet(self, icepap_name, driver_addr):
        axis = self.iPaps[icepap_name][driver_addr]
        try:
            return axis.get_cfg('EXPERT')['EXPERT']
        except Exception:
            return 'NO'

    @loggingInfo
    def _parseDriverTemplateFile(self):
        self.config_parameters = []
        doc = minidom.parse(self.config_template)
        root = doc.documentElement
        for section in root.getElementsByTagName("section"):
            section_name = ''
            if section.nodeType == Node.ELEMENT_NODE:
                section_name = section.attributes.get('name').value
            inTestSection = (section_name == "test")
            if not inTestSection:
                for pars in section.getElementsByTagName("par"):
                    if pars.nodeType == Node.ELEMENT_NODE:
                        parname = pars.attributes.get('name').value
                        self.config_parameters.append(str(parname))

    @loggingInfo
    def upgradeDrivers(self, icepap_name, progress_dialog):
        if self.programming_ipap is not None:
            return False
        self.programming_ipap = self.iPaps[icepap_name]
        self.progress_dialog = progress_dialog
        self.progress_dialog.show()
        # TODO: Remove on the future QT depency
        self.updateProgressBarTimer = Qt.QTimer()
        self.updateProgressBarTimer.timeout.connect(self.updateProgressBar)
        try:
            self.programming_ipap.mode = 'PROG'
        except Exception as e:
            print("icepapcontroller:upgradeDrivers:Some error trying to set "
                  "mode PROG:", str(e))
            return False
        self.programming_ipap.prog('DRIVERS')
        self.updateProgressBarTimer.start(2000)
        return True

    def updateProgressBar(self):
        try:
            status = self.programming_ipap.get_prog_status()
        except Exception:
            return

        value = status[0].upper()
        if value == 'DONE':
            self.progress_dialog.setValue(100)
            self.updateProgressBarTimer.stop()
            self.programming_ipap.mode = 'OPER'
            self.programming_ipap = None
        else:
            value = float(value)
            self.progress_dialog.setValue(value)

    def _wait_programming(self, ipap, logger):
        # wait process to finish
        wait = True
        while wait:
            try:
                if not ipap.connected:
                    raise RuntimeError('No connection available')
                status = ipap.get_prog_status()
                if status[0].upper() != 'DONE':
                    logger.put('Programming {}%'.format(status))
                    time.sleep(5)
                else:
                    wait = False
            except RuntimeError:
                logger.put('Connection lost, waiting for reconnection...')
                while not ipap.connected:
                    time.sleep(0.5)
                logger.put('Reconnected!')

    def _get_ipap_and_ver(self, host, port, logger):

        logger.put("Connecting to: {} {}".format(host, port))

        ipap = IcePAPController(host, port)

        try:
            curr_ver = ipap.ver.system[0]
        except Exception as e:
            logger.put('Can not read the current version. {}'.format(e))
            curr_ver = -1
        logger.put('Current firmware version is {}'.format(curr_ver))

        logger.put("Setting MODE PROG")
        ipap.mode = 'PROG'
        logger.put('Mode {}'.format(ipap.mode))
        logger.put('Programing...')

        return ipap, curr_ver

    def _end_programming(self, ipap, logger):
        host = ipap._comm.host
        port = ipap._comm.port

        logger.put('Waiting 5 sec to change Mode to OPER')
        time.sleep(5)
        logger.put("Setting MODE OPER")
        ipap.mode = 'oper'
        if ipap.mode.lower() != 'oper':
            logger.put('It was not possible to change mode to OPER')
        logger.put('Mode {}'.format(ipap.mode))
        logger.put('Reboot system')
        ipap.reboot()
        logger.put('Wait while rebooting... 1 minute')
        for i in range(4):
            time.sleep(15)
            logger.put('Passed {} seconds'.format(15*(i+1)))

        try:
            ipap = IcePAPController(host, port)
        except Exception:
           logger.put('ERROR: Can not connect to the icepap after to restart')
           return

        logger.put('Connected after to restart')
        try:
            curr_ver = ipap.ver.system[0]
        except Exception as e:
            logger.put('Can not read the current version. {}'.format(e))
            logger.put('CHECK Icepap!!!')
            return
        logger.put('Current version: {}'.format(curr_ver))
        logger.put('\n\nProgramming sequence done!')

    def upgradeAutomaticFirmware(self, host, port, filename, log_queue):
        log_queue.put('Upgrade Automatic Firmware')

        ipap, curr_ver = self._get_ipap_and_ver(host, port, log_queue)
        if filename != '':
            log_queue.put('Saving new firmware on the icepap')
            ipap.sprog(filename, saving=True)
        else:
            log_queue.put('Using saved firmware on the icepap')
            try:
                ver_saved = ipap.ver_saved.system[0]
                log_queue.put('Version saved: {}'.format(ver_saved))
            except Exception:
                log_queue.put('Can not read version saved')


        log_queue.put('Send PROG ALL')
        ipap.prog('ALL', force=True)
        self._wait_programming(ipap, log_queue)

        if curr_ver < 2:
            ipap.prog('MCPU0')
            ipap.prog('MCPU1')
            ipap.prog('MCPU2')

        time.sleep(5)
        self._end_programming(ipap, log_queue)
        if curr_ver < 3.21:
            try:
                ipap = IcePAPController(host, port)
                new_ver = ipap.ver.system[0]
                if new_ver >= 3.21:
                    log_queue.put('Restarting first time absolut encoder '
                                    'registers')
                    ipap.send_cmd(':ISG ABSRST')
            except Exception:
                log_queue.put('ERROR!!!!\nCan not restart absolut enconder '
                                'registers')

    @loggingInfo
    def upgradeFirmware(self, host, port, filename, component, options, force,
                        log_queue):

        ipap, _ = self._get_ipap_and_ver(host, port, log_queue)

        if filename != '':
            save = False
            if options == 'SAVE':
                save = True
                options = ''
            ipap.sprog(filename, component, force, save, options)
        else:
            ipap.prog(component, force)

        self._wait_programming(ipap, log_queue)
        self._end_programming(ipap, log_queue)

    @loggingInfo
    def testConnection(self, host, port):
        try:
            ipap = IcePAPController(host, port)
            if self.log.isEnabledFor(logging.INFO):
                self.log.info('Testing connection to: %s:%s version: %s',
                              host, port, ipap.ver.system[0])
            ipap.disconnect()
            return True
        except Exception:
            return False

    @loggingInfo
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

    @loggingInfo
    def host_in_same_subnet(self, host):
        if self._config._options.allnets or \
                self._config.config['all_networks']['use']:
            return True

        networks = []
        configs = None
        addr_pattern = None
        mask_pattern = None
        digits = r'[0-9]{1,3}'

        if os.name == 'posix':
            ifconfigs = ['/sbin/ifconfig', '/usr/sbin/ifconfig',
                         '/bin/ifconfig', '/usr/bin/ifconfig']
            ifconfig = list(filter(os.path.exists, ifconfigs))[0]
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
