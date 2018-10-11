from PyQt4 import QtGui
from ui_dialogstatusinfo import Ui_DialogStatusInfo
from lib_icepapcms import IcepapController
from messagedialogs import MessageDialogs


class DialogStatusInfo(QtGui.QDialog):

    def __init__(self, parent, drv):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogStatusInfo()
        self.drivers = IcepapController().iPaps[drv.icepapsystem_name]
        self.icepap_addr = drv.addr
        self.ui.setupUi(self)
        txt = 'Status Info  |  ' + drv.icepapsystem_name + '  |  ' + str(self.icepap_addr) + ' ' + drv.name
        self.setWindowTitle(txt)
        self._connect_signals()
        self._do_vstatus()
        self.allDriversCommands = ['?cfg extdisable',
                                   '?power',
                                   '?positions',
                                   '?warning',
                                   'c ?warning',
                                   'a ?warning',
                                   '?alarm',
                                   '?isg ?ssierrtoggles',
                                   '?isg ssiwarningrst',
                                   '?ver info',
                                   'c ?ver info',
                                   'a ?ver info',
                                   'c ?rdispol',
                                   '?vstatus DISABLE',
                                   '?vstatus STOPCODE',
                                   'a ?meas T',
                                   'a ?wtemp']
        for cmd in self.allDriversCommands:
            self.ui.cbAllDrivers.addItem(cmd)

    def _connect_signals(self):
        self.ui.btnUpdate.clicked.connect(self._do_vstatus)
        self.ui.btnEsync.clicked.connect(self._do_esync)
        self.ui.btnUpdate.setDefault(False)
        self.ui.btnEsync.setDefault(False)
        self.ui.btnUpdate.setAutoDefault(False)
        self.ui.btnEsync.setAutoDefault(False)
        self.ui.txt1Command.returnPressed.connect(self._get_info)
        self.ui.cbAllDrivers.activated.connect(self._get_info_multi)

    def _do_vstatus(self):
        try:
            val = self.drivers[self.icepap_addr].vstatus
            self.ui.textBrowser.setText(val)
        except RuntimeError as e:
            msg = 'VSTATUS failed:\n{}'.format(e)
            print(msg)

    def _do_esync(self):
        try:
            self.drivers[self.icepap_addr].esync()
        except RuntimeError as e:
            msg = 'ESYNC failed:\n{}'.format(e)
            print(msg)

    def _get_info(self):
        msg = 'Freetext field does not work with pyIcePAP API v2.'
        print(msg)
        MessageDialogs.showErrorMessage(None, 'Freetest Box', msg)

    def _get_info_multi(self):
        sel = self.ui.cbAllDrivers.currentText()
        prefix = sel[:2]
        cmd = sel[2:]
        if prefix == 'a ':
            txt = self._get_info_controllers(cmd, True)
        elif prefix == 'c ':
            txt = self._get_info_controllers(cmd, False)
        else:
            txt = self._get_info_drivers(sel)
        self.ui.textBrowser.setText(txt)

    def _get_info_controllers(self, cmd, include_drivers):
        txt = ''
        for rack_id in self._get_racks_present():
            contr_address = rack_id * 10
            c = ''
            try:
                if cmd == '?ver info':
                    c = '{}:?VER INFO'.format(contr_address)
                    ans = self.drivers.send_cmd(c)
                    val = ''
                    for line in ans:
                        val += line + '\n'
                elif cmd == '?meas T':
                    c = '{}:?MEAS T'.format(contr_address)
                    ans = self.drivers.send_cmd(c)
                    val = ans[0]
                else:
                    c = '{}:{}'.format(contr_address, cmd)
                    ans = self.drivers.send_cmd(c)
                    val = ans[0]
            except RuntimeError as e:
                msg = 'Controller command failed:\n{}:\n{}'.format(c, e)
                print(msg)
                return ''
            txt += '{} {}\n'.format(contr_address, val)
            if include_drivers:
                txt += self._get_info_drivers(cmd, contr_address)
        return txt

    def _get_info_drivers(self, cmd, controller=-1):
        axes = []
        if controller == -1:
            axes.append(self.icepap_addr)
        else:
            for ax in range(controller + 1, controller + 9):
                if ax in self.drivers:
                    axes.append(ax)
        txt = ''
        try:
            if cmd == '?positions':
                txt = 'dr name axis absenc encin inpos tgtenc\n'
                for addr in axes:
                    val0 = self.drivers[addr].name
                    val1 = self.drivers[addr].pos
                    val2 = self.drivers[addr].enc_absenc
                    val3 = self.drivers[addr].enc_encin
                    val4 = self.drivers[addr].enc_inpos
                    cfg = self.drivers[addr].get_cfg('TGTENC')
                    val5 = cfg['TGTENC']
                    if val0 == '':
                        val0 = 'noname'
                    txt += '{} {} {} {} {} {} {}\n'.format(addr, val0, val1, val2, val3, val4, val5)
            elif cmd == '?ver info':
                for addr in axes:
                    c = '{}:?VER INFO'.format(addr)
                    ans = self.drivers.send_cmd(c)
                    val = ''
                    for line in ans:
                        val += line + '\n'
                    txt += '{} {}\n'.format(addr, val)
            elif cmd == '?meas T':
                for addr in axes:
                    val = self.drivers[addr].meas_t
                    txt += '{} {}\n'.format(addr, val)
            elif cmd[:9] == '?vstatus ' and len(cmd.split(' ')) == 2:
                field = cmd[9:]
                for addr in axes:
                    val = self.drivers[addr].vstatus
                    val_lines = val.split('\n')
                    for l in val_lines:
                        if str(field) in l:
                            txt += '{} {}\n'.format(addr, l)
            else:
                for addr in axes:
                    ans = self.drivers[addr].send_cmd(cmd)
                    val = ''
                    for i in ans:
                        val += ' {}'.format(i)
                    txt += '{} {}\n'.format(addr, val)
        except RuntimeError as e:
            msg = 'Controller command failed:\n{}:\n{}'.format(cmd, e)
            print(msg)
            return ''
        return txt

    def _get_racks_present(self):
        try:
            val = self.drivers.send_cmd('?SYSSTAT')
        except RuntimeError as e:
            msg = 'Failed to retrieve list of present racks:\n{}'.format(e)
            print(msg)
            return []
        rack_list = []
        for rack_str in val:
            id = int(rack_str, 16) - 1
            rack_list.append(id)
        return rack_list
