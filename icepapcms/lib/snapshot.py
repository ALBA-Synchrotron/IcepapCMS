import yaml
import logging
import time
import click
import os

from icepap import IcePAPController
from icepap.cli.utils import get_axes

from .configmanager import ConfigManager
from .stormmanager import StormManager

ERROR_VALUE = 'ERROR'

REGISTER_MAP = {
    'NONE': ['pos_motor', 'enc_motor'],
    'EncIn': ['pos_encin', 'enc_encin'],
    'AbsEnc': ['pos_absenc', 'enc_absenc'],
    'InPos': ['pos_inpos', 'enc_inpos']
}

REGISTERS = ['pos', 'enc', 'pos_encin', 'enc_encin',
             'pos_inpos', 'enc_inpos', 'pos_absenc', 'enc_absenc',
             'pos_motor', 'enc_motor', 'pos_sync', 'enc_sync']


class IcepapSnapshot:
    """
    Class to create/restore IcePAP backups based on Ethernet communication.
    """

    def __init__(self, icepap: IcePAPController):
        log_name = '{0}.IcepapSnapshot'.format(__name__)
        self.log = logging.getLogger(log_name)
        self.ipap = icepap
        self.snapshot = {}
        self.done = 0
        self.axes_errors = []

    def create_snapshot(self, filename,):
        self.axes_errors = []
        factor = 100 / (len(self.ipap.axes) + 2)
        _done = 0
        self.snapshot['Date'] = time.strftime('%Y/%m/%d %H:%M:%S +%z')
        self.snapshot['System'] = system = {}
        self.snapshot['AxesErrors'] = axes_errors = []
        self.snapshot['Axes'] = axes = {}
        system['HOST'] = self.ipap.host
        system['PORT'] = self.ipap.port
        system['VER'] = self.ipap.ver['SYSTEM']['VER'][0]
        _done += 1
        self.done = _done * factor

        for axis in self.ipap.axes:
            axis_snapshot = AxisSnapshot(self.ipap[axis])
            error = axis_snapshot.create_snapshot()
            if error:
                axes_errors.append(axis)
            axes[axis] = axis_snapshot.snapshot
            _done += 1
            self.done = _done * factor
        self._save(filename)
        self.done = 100
        self.axes_errors = list(axes_errors)
        return axes_errors

    def check(self, snapshot):
        self.axes_errors = []
        axes = self.ipap.find_axes()
        total_diff = {}
        system_ver = snapshot['System']['VER']
        new_system_ver = self.ipap.ver['SYSTEM']['VER'][0]
        if system_ver != new_system_ver:
            total_diff['SystemVer'] = (system_ver, new_system_ver)
        # TODO Check versions
        total_diff['AxesNotFound'] = axes_not_found = []
        for axis_nr, axis_snapshot in snapshot['Axes'].items():
            if axis_nr not in axes:
                self.log.error('Axis {} not found in {}'.format(axis_nr,
                                                                 self.ipap))
                axes_not_found.append(axis_nr)
                continue
            axis_snap = AxisSnapshot(self.ipap[axis_nr])
            diff = axis_snap.check(axis_snapshot)
            if axis_snap.flag_error:
                self.axes_errors.append(axis_nr)

            if diff:
                total_diff[axis_nr] = diff
        return total_diff

    def _save(self, filename):
        with open(filename, 'w') as f:
            yaml.safe_dump(self.snapshot, f)


class AxisSnapshot:

    def __init__(self, axis):
        self.axis = axis
        self.snapshot = {}
        log_name = '{}.AxisSnapshot_({})'.format(__name__, axis)
        self.flag_error = False
        self.log = logging.getLogger(log_name)

    def create_snapshot(self):
        flag_error = False
        try:
            drv_ver = self.axis.fver
        except Exception as e:
            error = str(e).strip('\r\n')
            self.log.error('Error on reading version:{}'.format(error))
            drv_ver = 0
            flag_error = True

        self.snapshot['VER'] = drv_ver
        for i in range(3):
            try:
                # Get Configuration
                value = dict(self.axis.get_cfg())
                break
            except Exception as e:
                if i == 2:
                    error = str(e).strip('\r\n')
                    self.log.error('Error on reading configuration: {}'
                                   ''.format(error))
                    value = ERROR_VALUE

        self.snapshot['Configuration'] = value
        if value == ERROR_VALUE:
            flag_error = True

        # Get Operation:
        self.snapshot['Operation'] = oper = {}

        # Basic operation attributes
        attrs = ['velocity', 'name', 'acctime', 'pcloop', 'indexer', 'infoa',
                 'infob', 'infoc', 'pos', 'enc', 'pos_encin', 'enc_encin',
                 'pos_inpos', 'enc_inpos', 'pos_absenc', 'enc_absenc',
                 'pos_motor', 'enc_motor', 'id',
                 'power']

        # Attributes can fail on reading because they are on version 3.17
        # This attributes won on the backup file if the version is < 3
        v3_attrs = ['cswitch', 'velocity_min', 'velocity_max', 'ecam',
                    'outpos', 'outpaux', 'syncpos', 'syncaux',
                    'pos_sync', 'enc_sync']

        attrs += v3_attrs
        attrs.sort()

        for attr in attrs:
            if attr in v3_attrs and drv_ver < 3:
                continue
            for i in range(3):
                try:
                    value = self.axis.__getattribute__(attr)
                    break
                except Exception as e:
                    error = str(e).strip('\r\n')

                    self.log.error('Error on reading {}: {}'
                                   ''.format(attr, error))
                    value = ERROR_VALUE
                    if 'allowed in active' in error:
                        break
            oper[attr] = value
            if value == ERROR_VALUE:
                flag_error = True

        # External Disable. Valid for FW < 3
        if drv_ver < 3:
            try:
                value = eval(self.axis.send_cmd('?DISDIS')[0])
            except Exception as e:
                error = str(e).strip('\r\n')
                self.log.error('Error on reading DISDIS: {}'
                               ''.format(error))
                value = ERROR_VALUE
                flag_error = True
            oper['DISDIS'] = value
        self.flag_error = flag_error
        return flag_error

    def check(self, snapshot):
        self.create_snapshot()
        diff = {}
        not_check = ['id']
        ver = snapshot['VER']
        if ver != self.snapshot['VER']:
            diff['Ver'] = (ver, self.snapshot['VER'])

        # Check configuration
        configured_enc = set()
        diff['Encoders'] = configured_enc

        diff['Configuration'] = diff_conf = {}
        if ERROR_VALUE not in [snapshot['Configuration'],
                               self.snapshot['Configuration']]:

            for i in ['CTRLENC', 'SHFTENC', 'TGTENC']:
                try:
                    enc = snapshot['Configuration'][i]
                    configured_enc.update(set(REGISTER_MAP[enc]))
                except KeyError:
                    diff_conf[i] = ('Snapshot corrupted', self.snapshot[
                        'Configuration'][i])

            for k, v in snapshot['Configuration'].items():
                if k not in self.snapshot['Configuration']:
                    diff_conf[k] = (v, 'Missing Parameter')
                elif v != self.snapshot['Configuration'][k]:
                    diff_conf[k] = (v, self.snapshot['Configuration'][k])
        else:
            diff_conf = ERROR_VALUE

        diff['Operation'] = diff_oper = {'Error': {}, 'Change': {},
                                         'ChangeNoise': {} }
        for k, v in snapshot['Operation'].items():
            if k in not_check:
                continue
            if k not in self.snapshot['Operation']:
                diff_oper['Change'][k] = (v, 'Missing Parameter')
                continue
            new_v = self.snapshot['Operation'][k]
            if ERROR_VALUE in [v, new_v]:
                diff_oper['Error'][k] = (v, new_v)
            if v != new_v:
                if k in REGISTERS:
                    try:
                        d = v - new_v
                    except TypeError:
                        d = float('inf')
                    if k in configured_enc:
                        diff_oper['Change'][k] = (d, v, new_v)
                    else:
                        diff_oper['ChangeNoise'][k] = (d, v, new_v)
                    continue
                diff_oper['Change'][k] = (v, new_v)
                
        return diff

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


def echo(msg, level=0, color='green'):
    space = ' ' * 4 * (level)
    msg = click.style(f'{space}{msg}', fg=color)
    click.echo(msg)


@click.group()
@click.pass_context
def icepapsnapshot(ctx):
    """
    Command line interface for create, compare and load snapshots
    """
    pass


@icepapsnapshot.command()
@click.pass_context
@click.argument("icepap", type=IcePAPController.from_url)
@click.option('-o', '--output',
              type=click.Path(exists=False, dir_okay=True, resolve_path=True),
              default=None, help='By default generates the same filename '
                                 'than the GUI')
@click.option("--axes", "axes_str", type=str, default="alive",
              help="comma separated list of axes. Also supports 'all' and "
                   "'alive'")
def create(ctx, icepap, output, axes_str):
    """
    Create a snapshot and save to file

    Connects to the given ICEPAP (a url in format [tcp://]<host/ip>[:<port=5000])
    (ex: 'ice1', 'tcp://ice1' and 'tcp://ice1:5000' all mean the same)
    Create a snapshot of the given axes, by default all alive, and save to file

    """
    get_axes(icepap, axes_str)
    snapshot = IcepapSnapshot(icepap)
    if output is None:
        config_manager = ConfigManager()
        str_time = time.strftime('%Y%m%d_%H%M%S')
        name = '{}_snapshot_{}.yaml'.format(icepap.host, str_time)
        snapshots_folder = config_manager.config['icepap']['snapshots_folder']
        output = os.path.join(snapshots_folder, name)
    axes_error = snapshot.create_snapshot(output)
    echo('*' * 79)
    echo(f'System: {icepap.host}; axes: {axes_str}')
    echo('Results:')
    echo(f'Output: {output}', level=1)
    if axes_error:
        echo(f'Axes with error: {axes_error}', level=1, color='red')
    echo('*' * 79)
    click.echo()


@icepapsnapshot.command
@click.pass_context
def create_from_db(ctx):
    """
    Create snapshot for all icepap defined on the database configured
    :return:
    """
    db = StormManager()
    for location in db.getAllLocations().keys():
        echo('*'*79)
        echo(f'Create snapshot for all icepaps in location: {location}')
        icepap_systems = db.getLocationIcepapSystem(location).values()
        if not icepap_systems:
            echo(f'No icepaps for this location')
            continue

        for ipap_system in icepap_systems:
            host = ipap_system.host
            try:
                echo('*' * 79)
                echo(f'Creating snapshot for host: {host}')
                ctx.invoke(create, icepap=IcePAPController.from_url(host))
            except:
                echo(f'Error creating snapshot for {host}', color='red' )
                echo('*' * 79)


@icepapsnapshot.command()
@click.argument('filename',
                type=click.Path(exists=True))
@click.option('-a', '--all', is_flag=True, 
              help='Show all position register difference. By defualt it '
                   'shows only the register used on Shaft, Target and '
                   'Control encoder ')
def check(filename, all):
    """
    Check current configuration with a snapshot

    \b
    The script will check the axes on the snapshot with the current
    configuration. It will show:
    * The RAW difference between the snapshot and the current state (blue)
    * Per Axis: State of the Configuration and Operation values:
       -  Green: all OK
       - Yellow: Problem on the reading
       - Red: Changes on values
       - Blue: Changes on position/encoder registers which are not used as
               Target, Shaft or Control Encoders.
    * Final results
    """
    with open(filename, 'r') as f:
        snap = yaml.load(f, Loader=yaml.FullLoader)
    host = snap['System']['HOST']
    port = snap['System']['PORT']
    icepap = IcePAPController(host, port)
    ipap_snap = IcepapSnapshot(icepap)
    try:
        diff = ipap_snap.check(snap)
    except Exception as e:
        echo(f'Error: {e}', color='red')
        return

    echo('*' * 79)
    echo('RAW difference:', color='blue')
    echo(diff, color='blue')
    echo('*'*79)
    axes_changed = []
    axes_change_noise = []
    for axis, change in diff.items():
        if axis in ['SystemVer', 'AxesNotFound']:
            continue
        # Configuration Change
        if 'Ver' in change:
            color = 'red'
        elif axis not in ipap_snap.axes_errors:
            color = 'green'
        else:
            color = 'yellow'
        echo(f'Axis: {axis}', color=color)
        if 'Ver' in change:
            ver = change['Ver'][0]
            new_ver = change['Ver'][1]
            echo(f'Version Changed: ver -> new_ver', level=1, color='red')
        if not change['Configuration']:
            echo(f'Configuration OK', level=1, color='green')
            
        elif change['Configuration'] == ERROR_VALUE:
            echo(f'Configuration ERROR: the snapshot or the current '
                 f'configuration is invalid', level=1, color='red')
            if axis not in axes_changed:
                axes_changed.append(axis)
        else:
            echo(f'Configuration Change:', level=1, color='red')
            for key, value in change['Configuration'].items():
                echo(f'{key}: {value[0]} -> {value[1]}', 
                     level=2, color='red')
                if axis not in axes_changed:
                    axes_changed.append(axis)

        # Operation Change
        if not change['Operation']['Error'] and not change['Operation'][
            'Change'] and not change['Operation']['ChangeNoise']:
            echo(f'Operation OK', level=1, color='green')
            continue

        elif change['Operation']['Error'] and not change['Operation'][
            'Change'] and not change['Operation']['ChangeNoise']:
            echo('Operation Warning: Can not read values', level=1,
                 color='yellow')
            if all:
                for key, value in change['Operation']['Error'].items():
                    echo(f'{key}: {value[0]} -> {value[1]}', level=2,
                         color='yellow')

            continue
        elif change['Operation']['ChangeNoise'] and not change['Operation'][
            'Change']:
            echo('Operation Change: some position register not '
                 'used changed', level=1, color='blue')
            axes_change_noise.append(axis)
            if all:
                for key, value in change['Operation']['ChangeNoise'].items():
                    echo(f'{key}: Difference {value[0]} = {value[1]} -'
                         f' {value[2]}', level=2, color='blue')

        elif change['Operation']['Change']:
            if axis not in axes_changed:
                axes_changed.append(axis)
            echo('Operation Change: ', level=1, color='red')
            for key, value in change['Operation']['Change'].items():
                if len(value) == 2:
                    echo(f'{key}: {value[0]} -> {value[1]}', level=2,
                         color='red')
                else:
                    echo(f'{key}: Difference {value[0]} = {value[1]} -'
                             f' {value[2]}', level=2, color='red')
            if all:
                for key, value in change['Operation']['ChangeNoise'].items():
                    echo(f'{key}: Difference {value[0]} = {value[1]} -'
                         f' {value[2]}', level=2, color='blue')

                for key, value in change['Operation']['Error'].items():
                    echo(f'{key}: {value[0]} -> {value[1]}', level=2,
                         color='yellow')

    echo('*' * 79)
    echo(f'System: {host}')
    if (not axes_changed and not ipap_snap.axes_errors and not
    axes_change_noise and not diff['AxesNotFound']):
        echo(f'Results:\nSystem OK')
        echo('*' * 79)
        return
    echo('Results: TO SEE ALL CHANGES USE FLAG "-a" ')
    if 'SystemVer' in diff:
        echo(f'System version changed: {diff["SystemVer"][0]} -> '
             f'{diff["SystemVer"][1]}', color='red')
    if axes_changed:
        echo(f'Axes with changes: {axes_changed}', color='red')
    if axes_change_noise:
        echo(f'Axes with change on position register not used:'
             f' {axes_change_noise}',
             color='blue')
    if ipap_snap.axes_errors:
        echo(f'Axes with error on reading: {ipap_snap.axes_errors}',
             color='yellow')
    if diff['AxesNotFound']:
        echo(f'Axes not alive on the system: {diff["AxesNotFound"]}',
             color='red')
    echo('*' * 79)


def main():
    icepapsnapshot()