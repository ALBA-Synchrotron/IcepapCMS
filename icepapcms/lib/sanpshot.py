import yaml
from icepap import IcePAPController
import logging
import time


class IcepapSnapshot:
    """
    Class to create/restore IcePAP backups based on Ethernet communication.
    """

    def __init__(self, host='', port=5000, timeout=3):
        log_name = '{0}.IcepapSnapshot'.format(__name__)
        self.log = logging.getLogger(log_name)
        self._host = host
        self._port = port
        self._ipap = IcePAPController(host, port, timeout, auto_axes=True)
        self.snapshot = {}
        self.done = 0

    def create_snapshot(self, filename):
        factor = 100 / (len(self._ipap.axes) + 2)
        _done = 0
        self.snapshot['Date'] = time.strftime('%Y/%m/%d %H:%M:%S +%z')
        self.snapshot['System'] = system = {}
        self.snapshot['Axes'] = axes = {}
        system['HOST'] = self._host
        system['PORT'] = self._port
        system['VER'] = self._ipap.ver['SYSTEM']['VER'][0]
        _done += 1
        self.done = _done * factor
        for axis in self._ipap.axes:
            axis_snapshot = AxisSnapshot(self._ipap[axis])
            axis_snapshot.create_snapshot()
            axes[axis] = axis_snapshot.snapshot
            _done += 1
            self.done = _done * factor
        self._save(filename)
        self.done = 100

    def _save(self, filename):
        with open(filename, 'w') as f:
            yaml.safe_dump(self.snapshot, f)


class AxisSnapshot:

    def __init__(self, axis):
        self.axis = axis
        self.snapshot = {}

    def create_snapshot(self):
        drv_ver = self.axis.ver['SYSTEM']['DRIVER']['VER'][0]
        self.snapshot['VER'] = drv_ver


        # Get Configuration
        self.snapshot['Configuration'] = dict(self.axis.get_cfg())

        # Get Operation:
        self.snapshot['Operation'] = oper = {}

        # Attributes can fail on reading, but we save it anyway with None
        # value
        attrs = ['velocity', 'name', 'acctime', 'pcloop', 'indexer', 'infoa',
                 'infob', 'infoc', 'pos', 'pos_measure', 'pos_shftenc',
                 'pos_tgtenc', 'pos_ctrlenc', 'pos_encin', 'pos_inpos',
                 'pos_absenc', 'pos_motor', 'pos_sync', 'enc', 'enc_measure',
                 'enc_shftenc', 'enc_tgtenc', 'enc_ctrlenc', 'enc_encin',
                 'enc_inpos', 'enc_absenc', 'enc_motor', 'enc_sync', 'id']

        # Attributes can fail on reading because they are on version 3.17
        # This attributes won on the backup file if the version is < 3
        v3_attrs = ['cswitch', 'velocity_min', 'velocity_max', 'ecam',
                    'outpos', 'outpaux', 'syncpos', 'syncaux']

        attrs += v3_attrs
        attrs.sort()

        for attr in attrs:
            if attr in v3_attrs and drv_ver < 3:
                continue
            for i in range(3):
                try:
                    value = self.axis.__getattribute__(attr)
                    break
                except Exception:
                    value = None
            oper[attr] = value

        # External Disable. Valid for FW < 3
        if drv_ver < 3:
            try:
                value = eval(self.axis.send_cmd('?DISDIS')[0])
            except Exception:
                value = None
            oper['DISDIS'] = value


    # def do_check(self, axes=[]):
    #     self._cfg_bkp.pop('GENERAL')
    #     sections = self._cfg_bkp.sections()
    #     sections.pop(sections.index('SYSTEM'))
    #     sections.pop(sections.index('CONTROLLER'))
    #     for axis in axes:
    #         section = 'AXIS_{0}'.format(axis)
    #         try:
    #             sections.pop(sections.index(section))
    #         except Exception:
    #             raise ValueError('There is not backup for the axis '
    #                              '{0}'.format(axis))
    #     if len(axes) > 0:
    #         for section in sections:
    #             self._cfg_bkp.pop(section)
    #     else:
    #         for section in sections:
    #             axis = int(section.split('_')[1])
    #             axes.append(axis)
    #     self.log.info('Checking IcePAP {0} axes: {1}'.format(self._host,
    #                                                          repr(axes)))
    #     self.do_backup(axes=axes, save=False, general=False)
    #     total_diff = {}
    #     if self._cfg_bkp == self._cfg_ipap:
    #         self.log.info('No differences found')
    #     else:
    #         sections = self._cfg_bkp.sections()
    #         for section in sections:
    #             diff = dict_cfg(self._cfg_bkp[section], self._cfg_ipap[
    #                 section])
    #             if len(diff) > 0:
    #                 total_diff[section] = diff
    #         self.log.info('Differences found: {0}'.format(repr(total_diff)))
    #     return total_diff
    #
    # def do_autofix(self, diff, force=False, skip_registers=[]):
    #     """
    #     Solve inconsistencies in IcePAP configuration registers.
    #
    #     :param diff: Differences dictionary.
    #     :param force: Force overwrite of `enc` and `pos` register values.
    #     :param skip_registers: List of registers to do not overwrite
    #         when loading a saved configuration.
    #     :return:
    #     """
    #     self.active_axes(force=True)
    #     time.sleep(2)
    #     sections = list(diff.keys())
    #     axes = []
    #     for section in sections:
    #         if 'AXIS_' in section:
    #             axis = int(section.split('_')[1])
    #             axes.append(axis)
    #     axes.sort()
    #     for axis in axes:
    #         section = 'AXIS_{0}'.format(axis)
    #         registers = diff[section]
    #         for register in registers:
    #             if 'ver' in register:
    #                 continue
    #             if 'cfg' in register:
    #                 continue
    #
    #             value_bkp, value_ipap = diff[section][register]
    #
    #             if UNKNOWN in value_bkp:
    #                 continue
    #
    #             # Check DISDIS configuration
    #             if register.lower() == 'disdis':
    #                 try:
    #                     if 'KeyNot' in value_bkp:
    #                         # Version backup > 3
    #                         value = diff[section]['cfg_extdisable'][0]
    #                         if value.lower() == 'none':
    #                             cmd = 'DISDIS 1'
    #                         else:
    #                             cmd = 'DISDIS 0'
    #                         self._ipap[axis].send_cmd(cmd)
    #                         self.log.info('Fixed axis {0} disdis '
    #                                       'configuration: cfg_extdisable({1})'
    #                                       ' -> {2}'.format(axis, value, cmd))
    #                     else:
    #                         # Version backup < 3:
    #                         value_bkp = eval(value_bkp)
    #                         self._ipap[axis].send_cmd('config')
    #                         value = ['Disable', 'NONE'][value_bkp]
    #                         cfg = 'EXTDISABLE {0}'.format(value)
    #                         self._ipap[axis].set_cfg(cfg)
    #                         cmd_str = 'config conf{0:03d}'.format(axis)
    #                         self._ipap[axis].send_cmd(cmd_str)
    #
    #                         self.log.info('Fixed axis {0} disdis '
    #                                       'configuration: DISDIS {1} -> '
    #                                       'cfg_extdisable {2}'
    #                                       .format(axis, value_bkp, value))
    #                 except Exception as e:
    #                     if self._ipap[axis].mode != 'oper':
    #                         self._ipap[axis].send_cmd('config')
    #                     self.log.error('Cannot fix axis {0} disdis '
    #                                    'configuration: bkp({1}) icepap({2}).'
    #                                    ' Error {3}'.format(axis, value_bkp,
    #                                                        value_ipap, e))
    #
    #             if 'KeyNot' in value_ipap or 'KeyNot' in value_bkp:
    #                 continue
    #
    #             if register in skip_registers:
    #                 self.log.warning('Skip register by user '
    #                                  '{0}'.format(register))
    #                 continue
    #
    #             if register.startswith('enc') and not force:
    #
    #                 self.log.warning('Skip axis {0} {1}: bkp({2}) '
    #                                  'icepap({3})'.format(axis, register,
    #                                                       value_bkp,
    #                                                       value_ipap))
    #                 continue
    #             if register.startswith('pos'):
    #                 self.log.warning('Skip axis {0} {1}: bkp({2}) '
    #                                  'icepap({3})'.format(axis, register,
    #                                                       value_bkp,
    #                                                       value_ipap))
    #                 continue
    #
    #             try:
    #                 value = eval(value_bkp)
    #                 if register == 'velocity':
    #                     acctime = self._ipap[axis].acctime
    #                     self._ipap[axis].velocity = value
    #                     self._ipap[axis].acctime = acctime
    #                 else:
    #                     self._ipap[axis].__setattr__(register, value)
    #
    #                 self.log.info('Fixed axis {0} {1}: bkp({2}) '
    #                               'icepap({3})'.format(axis, register,
    #                                                    value_bkp, value_ipap))
    #             except Exception as e:
    #                 self.log.error('Cannot fix axis {0} {1}: bkp({2}) '
    #                                'icepap({3}). '
    #                                'Error {4})'.format(axis, register,
    #                                                    value_bkp, value_ipap,
    #                                                    e))
    #     self.active_axes()
    #
    # def active_axes(self, axes=[], force=False):
    #     sections = self._cfg_bkp.sections()
    #     for section in sections:
    #         if section in ['GENERAL', 'SYSTEM', 'CONTROLLER']:
    #             continue
    #         axis = int(section.split('_')[1])
    #         if axes == [] or axis in axes:
    #             active = self._cfg_bkp.getboolean(section, 'ACTIVE')
    #             self._ipap[axis].send_cmd('config')
    #             if force:
    #                 cfg = 'ACTIVE YES'
    #             else:
    #                 cfg = 'ACTIVE {0}'.format(['NO', 'YES'][active])
    #             self.log.info('Axis {0}: {1}'.format(axis, cfg))
    #             self._ipap[axis].set_cfg(cfg)
    #             cmd = 'config conf{0:03d}'.format(axis)
    #             self._ipap[axis].send_cmd(cmd)
