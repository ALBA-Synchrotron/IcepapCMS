from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
from ui_dialogcurves import Ui_DialogCurves
import pyqtgraph as pg
from collections import namedtuple
from functools import partial
from lib_icepapcms import IcepapController
import time
from messagedialogs import MessageDialogs


class CurveItem:
    """Represents a curve to be plotted in a diagram."""

    SignalAppearance = namedtuple('SignalAppearance', ['pen_color', 'pen_width', 'pen_style', 'drop_down_list_pos'])

    signals = {'PosAxis': SignalAppearance(QtGui.QColor(255, 255, 0), 1, QtCore.Qt.SolidLine, 0),
               'PosTgtenc': SignalAppearance(QtGui.QColor(255, 0, 0), 1, QtCore.Qt.SolidLine, 1),
               'PosShftenc': SignalAppearance(QtGui.QColor(0, 255, 0), 1, QtCore.Qt.SolidLine, 2),
               'PosEncin': SignalAppearance(QtGui.QColor(255, 255, 255), 1, QtCore.Qt.SolidLine, 3),
               'PosAbsenc': SignalAppearance(QtGui.QColor(51, 153, 255), 1, QtCore.Qt.SolidLine, 4),
               'PosInpos': SignalAppearance(QtGui.QColor(0, 255, 255), 1, QtCore.Qt.SolidLine, 5),
               'PosMotor': SignalAppearance(QtGui.QColor(255, 0, 255), 1, QtCore.Qt.SolidLine, 6),
               'PosCtrlenc': SignalAppearance(QtGui.QColor(204, 153, 102), 1, QtCore.Qt.SolidLine, 7),
               'PosMeasure': SignalAppearance(QtGui.QColor(0, 0, 255), 1, QtCore.Qt.SolidLine, 8),
               'DifAxMeasure': SignalAppearance(QtGui.QColor(0, 255, 0), 1, QtCore.Qt.SolidLine, 9),
               'DifAxMotor': SignalAppearance(QtGui.QColor(255, 204, 0), 1, QtCore.Qt.SolidLine, 10),
               'DifAxTgtenc': SignalAppearance(QtGui.QColor(153, 255, 153), 3, QtCore.Qt.DotLine, 11),
               'DifAxShftenc': SignalAppearance(QtGui.QColor(255, 170, 0), 2, QtCore.Qt.DashLine, 12),
               'DifAxCtrlenc': SignalAppearance(QtGui.QColor(255, 0, 0), 3, QtCore.Qt.DashLine, 13),
               'EncEncin': SignalAppearance(QtGui.QColor(0, 255, 255), 1, QtCore.Qt.DotLine, 14),
               'EncAbsenc': SignalAppearance(QtGui.QColor(255, 170, 255), 1, QtCore.Qt.DashLine, 15),
               'EncTgtenc': SignalAppearance(QtGui.QColor(127, 255, 127), 1, QtCore.Qt.DashLine, 16),
               'EncInpos': SignalAppearance(QtGui.QColor(255, 255, 127), 1, QtCore.Qt.DashLine, 17),
               'StatReady': SignalAppearance(QtGui.QColor(255, 0, 0), 5, QtCore.Qt.DotLine, 18),
               'StatMoving': SignalAppearance(QtGui.QColor(255, 0, 0), 1, QtCore.Qt.DashLine, 19),
               'StatSettling': SignalAppearance(QtGui.QColor(0, 255, 0), 3, QtCore.Qt.DotLine, 20),
               'StatOutofwin': SignalAppearance(QtGui.QColor(255, 255, 255), 2, QtCore.Qt.SolidLine, 21),
               'StatStopcode': SignalAppearance(QtGui.QColor(51, 153, 255), 1, QtCore.Qt.DashLine, 22),
               'StatWarning': SignalAppearance(QtGui.QColor(255, 0, 255), 1, QtCore.Qt.DashLine, 23),
               'StatLim+': SignalAppearance(QtGui.QColor(255, 153, 204), 1, QtCore.Qt.DashLine, 24),
               'StatLim-': SignalAppearance(QtGui.QColor(204, 153, 102), 1, QtCore.Qt.DashLine, 25),
               'StatHome': SignalAppearance(QtGui.QColor(255, 204, 0), 1, QtCore.Qt.DashLine, 26),
               'MeasI': SignalAppearance(QtGui.QColor(255, 0, 255), 1, QtCore.Qt.DashLine, 27),
               'MeasIa': SignalAppearance(QtGui.QColor(255, 153, 204), 1, QtCore.Qt.DashLine, 28),
               'MeasIb': SignalAppearance(QtGui.QColor(204, 153, 102), 1, QtCore.Qt.DashLine, 29),
               'MeasVm': SignalAppearance(QtGui.QColor(255, 204, 0), 1, QtCore.Qt.DashLine, 30)}

    def __init__(self, driver_idx, sig_name, y_axis_idx):
        """
        Initializes an instance of class CurveItem.

        driver_idx - IcePAP driver index.
        sig_name   - Signal name.
        y_axis_idx - Index of Y axis to plot against.
        """
        self.start_over = True
        self.array_time = []
        self.array_val = []
        self.val_min = 0
        self.val_max = 0
        self.signal_name = sig_name
        sig_vals = self.signals[str(sig_name)]
        self.color = sig_vals.pen_color
        self.pen = {'color': sig_vals.pen_color, 'width': sig_vals.pen_width, 'style': sig_vals.pen_style}
        self.driver_idx = driver_idx
        self.y_axis_idx = y_axis_idx
        self.measure_resolution = 1.
        self.curve_plot = None
        self.signature = ''
        self.update_signature()

    def update_signature(self):
        """Sets the new value of the signature string."""
        self.signature = '%s:%s:%s' % (self.driver_idx + 1, self.signal_name, self.y_axis_idx + 1)

    def get_y(self, t):
        """
        Retrieve the signal value corresponding to the provided time value.

        t - Time value.
        Return: Signal value corresponding to an adjacent sample in time.
        """
        for x, v in zip(self.array_time, self.array_val):
            if x > t:
                return v


class DialogCurves(QtGui.QDialog):
    """A dialog for plotting signals."""

    def __init__(self, parent, drv):
        """
        Initializes an instance of class DialogCurves.

        parent - Parent of the dialog.
        drv    - IcePAP driver index.
        """
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DialogCurves()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.icepap_system = IcepapController().iPaps[drv.icepapsystem_name]
        self.ui.setupUi(self)
        self.setWindowTitle('Curves  |  ' + drv.icepapsystem_name + '  |  ' + str(drv.addr) + ' ' + drv.name)
        self.curve_items = []
        self._signal_val_getter = {}

        self.plot_widget = pg.PlotWidget()
        self.view_boxes = [self.plot_widget.getViewBox(), pg.ViewBox(), pg.ViewBox()]
        self._plot_item = self.plot_widget.getPlotItem()
        self.ui.gridLayout.addWidget(self.plot_widget)
        self._plot_item.showAxis('right')
        self._plot_item.scene().addItem(self.view_boxes[1])
        self._plot_item.scene().addItem(self.view_boxes[2])
        ax3 = pg.AxisItem(orientation='right', linkView=self.view_boxes[2])
        self.axes = [self._plot_item.getAxis('left'), self._plot_item.getAxis('right'), ax3]
        self.axes[1].linkToView(self.view_boxes[1])
        self.view_boxes[1].setXLink(self.view_boxes[0])
        self.view_boxes[2].setXLink(self.view_boxes[0])
        self._plot_item.layout.addItem(self.axes[2], 2, 3)
        self.view_boxes[0].disableAutoRange(axis=self.view_boxes[0].XAxis)
        self.view_boxes[0].enableAutoRange(axis=self.view_boxes[0].YAxis)
        self.view_boxes[1].disableAutoRange(axis=self.view_boxes[1].XAxis)
        self.view_boxes[1].enableAutoRange(axis=self.view_boxes[1].YAxis)
        self.view_boxes[2].disableAutoRange(axis=self.view_boxes[2].XAxis)
        self.view_boxes[2].enableAutoRange(axis=self.view_boxes[2].YAxis)
        self.label = pg.LabelItem(justify='right')
        self.vertical_line = pg.InfiniteLine(angle=90, movable=False)
        self.view_boxes[0].addItem(self.vertical_line, ignoreBounds=True)
        self.view_boxes[0].addItem(self.label)

        self._fill_combo_box_driver_ids()
        self.ui.cbDriver.setCurrentIndex(drv.addr - 1)
        self._fill_combo_box_signals()
        self._fill_combo_box_axes()
        self._update_button_status()

        self.ref_time = time.time()
        self.last_now = None
        self.ticker = Qt.QTimer(self)
        self.tick_interval = 100  # [milliseconds]

        self._connect_signals()
        self.proxy = pg.SignalProxy(self.plot_widget.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved)

        self.ticker.start(self.tick_interval)

    def _fill_combo_box_driver_ids(self):
        max_drivers = 128
        for i in range(1, max_drivers + 1):
            self.ui.cbDriver.addItem(str(i))

    def _fill_combo_box_signals(self):
        sig_items = []
        for sig_name, sig_vals in CurveItem.signals.items():
            sig_items.append((sig_vals.drop_down_list_pos, sig_name))
        sig_items.sort()
        for i in sig_items:
            self.ui.cbSignals.addItem(i[1])

    def _fill_combo_box_axes(self):
        self.ui.cbPlotAxis.addItem('1')
        self.ui.cbPlotAxis.addItem('2')
        self.ui.cbPlotAxis.addItem('3')

    def _connect_signals(self):
        QtCore.QObject.connect(self.ticker, QtCore.SIGNAL("timeout()"), self._tick)
        self.ui.btnAdd.clicked.connect(self._add_button_clicked)
        self.ui.btnShift.clicked.connect(self.shift_button_clicked)
        self.ui.btnRemove.clicked.connect(self._remove_button_clicked)
        self.ui.btnClearSignal.clicked.connect(self.clear_signal)
        self.ui.btnClear.clicked.connect(self.clear_all_signals)
        self.ui.btnCLoop.clicked.connect(self.prepare_closed_loop)
        self.ui.btnCurrents.clicked.connect(self.prepare_currents)
        self.ui.btnTarget.clicked.connect(self.prepare_target)
        self.ui.btnPause.clicked.connect(self.pause_button_clicked)
        self.ui.btnNow.clicked.connect(self.now_button_clicked)
        self.view_boxes[0].sigResized.connect(self.update_views)

    def update_views(self):
        """Updates the geometry for the view boxes."""
        self.view_boxes[1].setGeometry(self.view_boxes[0].sceneBoundingRect())
        self.view_boxes[2].setGeometry(self.view_boxes[0].sceneBoundingRect())
        self.view_boxes[1].linkedViewChanged(self.view_boxes[0], self.view_boxes[1].XAxis)
        self.view_boxes[2].linkedViewChanged(self.view_boxes[0], self.view_boxes[2].XAxis)

    def _update_button_status(self):
        val = self.ui.listCurves.count() == 0
        self.ui.btnShift.setDisabled(val)
        self.ui.btnRemove.setDisabled(val)
        self.ui.btnClearSignal.setDisabled(val)
        self.ui.btnClear.setDisabled(val)

    def _update_plot_axes_labels(self):
        txt = ['', '', '']
        for ci in self.curve_items:
            t = "<span style='font-size: 8pt; color: %s;'>%s</span>" % (ci.color.name(), ci.signature)
            txt[ci.y_axis_idx] += t
        for i in range(0, len(self.axes)):
            self.axes[i].setLabel(txt[i])

    def _add_button_clicked(self):
        my_driver_idx = self.ui.cbDriver.currentIndex()
        my_signal_name = self.ui.cbSignals.currentText()
        my_axis_idx = self.ui.cbPlotAxis.currentIndex()
        self.add_curve(my_driver_idx, my_signal_name, my_axis_idx)

    def add_curve(self, driver_idx, signal_name, axis_idx):
        """
        Adds a new curve to the plot area.

        driver_idx  - IcePAP driver index.
        signal_name - Signal name.
        y_axis_idx  - Index of Y axis to plot against.
        """
        drv_id = driver_idx + 1
        cfg = None
        msg = None
        try:
            cfg = self.icepap_system[drv_id].get_cfg()
        except RuntimeError as e:
            msg = 'Failed to retrieve configuration parameters for driver {}\n{}.'.format(drv_id, e)
        sn = QtCore.QString(signal_name)
        if self._is_signal_displayed(sn):
            msg = 'Signal {} is already displayed.'.format(sn)
        if msg is None and sn.endsWith('Tgtenc') and cfg['TGTENC'].upper() == 'NONE':
            msg = 'Signal {} is not mapped/valid.'.format(sn)
        if msg is None and sn.endsWith('Shftenc') and cfg['SHFTENC'].upper() == 'NONE':
            msg = 'Signal {} is not mapped/valid.'.format(sn)
        if msg is not None:
            print(msg)
            MessageDialogs.showErrorMessage(None, 'Add Curve', msg)
            return
        ci = CurveItem(driver_idx, sn, axis_idx)
        self._signal_val_getter[ci] = self._set_signal_val_getter(ci)
        if ci.signal_name.endsWith('Measure'):
            ci.measure_resolution = self._calc_measure_resolution(cfg)
        self.plot_curve(ci)
        self.curve_items.append(ci)
        self.ui.listCurves.addItem(ci.signature)
        index = len(self.curve_items) - 1
        self.ui.listCurves.setCurrentRow(index)
        self.ui.listCurves.item(index).setForeground(ci.color)
        self.ui.listCurves.item(index).setBackground(QtGui.QColor(0, 0, 0))
        self._update_plot_axes_labels()
        self._update_button_status()

    def _is_signal_displayed(self, signal_name):
        return signal_name in [ci.signal_name for ci in self.curve_items]

    @staticmethod
    def _calc_measure_resolution(cfg):
        tgtenc = cfg['TGTENC'].upper()
        shftenc = cfg['SHFTENC'].upper()
        axisnstep = cfg['ANSTEP']
        axisnturn = cfg['ANTURN']
        nstep = axisnstep
        nturn = axisnturn
        if tgtenc == 'ABSENC' or (tgtenc == 'NONE' and shftenc == 'ABSENC'):
            nstep = cfg['ABSNSTEP']
            nturn = cfg['ABSNTURN']
        elif tgtenc == 'ENCIN' or (tgtenc == 'NONE' and shftenc == 'ENCIN'):
            nstep = cfg['EINNSTEP']
            nturn = cfg['EINNTURN']
        elif tgtenc == 'INPOS' or (tgtenc == 'NONE' and shftenc == 'INPOS'):
            nstep = cfg['INPNSTEP']
            nturn = cfg['INPNTURN']
        return (float(nstep) / float(nturn)) / (float(axisnstep) / float(axisnturn))

    def clear_all_signals(self):
        """Remove the visible data for all signals."""
        self.ref_time = time.time()
        for ci in self.curve_items:
            ci.start_over = True

    def shift_button_clicked(self):
        """Assign a curve to a different y axis."""
        index = self.ui.listCurves.currentRow()
        ci = self.curve_items[index]
        self.remove_curve_plot(ci)
        ci.y_axis_idx = ci.y_axis_idx % 3
        ci.update_signature()
        self.plot_curve(ci)
        self.ui.listCurves.takeItem(index)
        self.ui.listCurves.insertItem(index, ci.signature)
        self.ui.listCurves.item(index).setForeground(ci.color)
        self.ui.listCurves.item(index).setBackground(QtGui.QColor(0, 0, 0))
        self.ui.listCurves.setCurrentRow(index)
        self._update_plot_axes_labels()

    def plot_curve(self, ci):
        """
        Plot a curve.

        ci - Curve item to plot.
        """
        ci.curve_plot = pg.PlotCurveItem(x=ci.array_time, y=ci.array_val, pen=ci.pen)
        self.view_boxes[ci.y_axis_idx].addItem(ci.curve_plot)

    def clear_signal(self):
        """Remove the visible data for a signal."""
        index = self.ui.listCurves.currentRow()
        self.curve_items[index].start_over = True

    def _remove_button_clicked(self):
        index = self.ui.listCurves.currentRow()
        ci = self.curve_items[index]
        self.remove_curve_plot(ci)
        self.ui.listCurves.takeItem(index)
        self.curve_items.remove(ci)
        self._signal_val_getter.pop(ci)
        self._update_plot_axes_labels()
        self._update_button_status()

    def remove_all_signals(self):
        """Removes all signals."""
        for ci in self.curve_items:
            self.remove_curve_plot(ci)
        self.ui.listCurves.clear()
        self.curve_items = []
        self._signal_val_getter = {}
        self._update_plot_axes_labels()
        self._update_button_status()

    def mouse_moved(self, evt):
        """
        Acts om mouse move.

        evt - Event containing the position of the mouse pointer.
        """
        pos = evt[0]  # The signal proxy turns original arguments into a tuple.
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = self.view_boxes[0].mapSceneToView(pos)
            time_value = mouse_point.x()
            txt = "<span style='font-size: 8pt; color: white;'>" + "%0.2f" % time_value + "</span>"
            txtmax = ''
            txtmin = ''
            for ci in self.curve_items:
                if ci.array_time and ci.array_time[0] < time_value < ci.array_time[-1]:
                    txt1 = "<span style='font-size: 8pt; color: %s;'>" % ci.color.name() + '|'
                    txt += txt1 + str(ci.get_y(time_value)) + "</span>"
                    txtmin += txt1 + str(ci.val_min) + "</span>"
                    txtmax += txt1 + str(ci.val_max) + "</span>"
            self.plot_widget.setTitle("<br>%s<br>%s<br>%s" % (txtmax, txt, txtmin))
            self.vertical_line.setPos(mouse_point.x())

    def _getter_pos_axis(self, ci):
        return self.icepap_system[ci.driver_idx + 1].pos

    def _getter_pos_tgtenc(self, ci):
        return self.icepap_system[ci.driver_idx + 1].pos_tgtenc

    def _getter_pos_shftenc(self, ci):
        return self.icepap_system[ci.driver_idx + 1].pos_shftenc

    def _getter_pos_encin(self, ci):
        return self.icepap_system[ci.driver_idx + 1].pos_encin

    def _getter_pos_absenc(self, ci):
        return self.icepap_system[ci.driver_idx + 1].pos_absenc

    def _getter_pos_inpos(self, ci):
        return self.icepap_system[ci.driver_idx + 1].pos_inpos

    def _getter_pos_motor(self, ci):
        return self.icepap_system[ci.driver_idx + 1].pos_motor

    def _getter_pos_ctrlenc(self, ci):
        return self.icepap_system[ci.driver_idx + 1].pos_ctrlenc

    def _getter_pos_measure(self, ci):
        return self.icepap_system.get_fpos(ci.driver_idx + 1, 'MEASURE')[0]

    def _getter_enc_encin(self, ci):
        return self.icepap_system[ci.driver_idx + 1].enc_encin

    def _getter_enc_absenc(self, ci):
        return self.icepap_system[ci.driver_idx + 1].enc_absenc

    def _getter_enc_tgtenc(self, ci):
        return self.icepap_system[ci.driver_idx + 1].enc_tgtenc

    def _getter_enc_inpos(self, ci):
        return self.icepap_system[ci.driver_idx + 1].enc_inpos

    def _getter_stat_moving(self, ci):
        return 1 if self.icepap_system[ci.driver_idx + 1].state_moving else 0

    def _getter_stat_settling(self, ci):
        return 1 if self.icepap_system[ci.driver_idx + 1].state_settling else 0

    def _getter_stat_outofwin(self, ci):
        return 1 if self.icepap_system[ci.driver_idx + 1].state_outofwin else 0

    def _getter_stat_ready(self, ci):
        return 1 if self.icepap_system[ci.driver_idx + 1].state_ready else 0

    def _getter_stat_stopcode(self, ci):
        return self.icepap_system[ci.driver_idx + 1].state_stop_code

    def _getter_stat_warning(self, ci):
        return 1 if self.icepap_system[ci.driver_idx + 1].state_warning else 0

    def _getter_stat_limit_positive(self, ci):
        return 1 if self.icepap_system[ci.driver_idx + 1].state_limit_positive else 0

    def _getter_stat_limit_negative(self, ci):
        return 1 if self.icepap_system[ci.driver_idx + 1].state_limit_negative else 0

    def _getter_stat_home(self, ci):
        return 1 if self.icepap_system[ci.driver_idx + 1].state_inhome else 0

    def _getter_meas_i(self, ci):
        return self.icepap_system[ci.driver_idx + 1].meas_i

    def _getter_meas_ia(self, ci):
        return self.icepap_system[ci.driver_idx + 1].meas_ia

    def _getter_meas_ib(self, ci):
        return self.icepap_system[ci.driver_idx + 1].meas_ib

    def _getter_meas_vm(self, ci):
        return self.icepap_system[ci.driver_idx + 1].meas_vm

    def _getter_dif_ax_measure(self, ci):
        return self._getter_pos_axis(ci) - self._getter_pos_measure(ci) / ci.measure_resolution

    def _getter_dif_ax_motor(self, ci):
        return self._getter_pos_axis(ci) - self._getter_pos_motor(ci)

    def _getter_dif_ax_tgtenc(self, ci):
        return self._getter_pos_axis(ci) - self._getter_pos_tgtenc(ci)

    def _getter_dif_ax_shftenc(self, ci):
        return self._getter_pos_axis(ci) - self._getter_pos_shftenc(ci)

    def _getter_dif_ax_ctrlenc(self, ci):
        return self._getter_pos_axis(ci) - self._getter_pos_ctrlenc(ci)

    def _set_signal_val_getter(self, ci):
        if ci.signal_name == 'PosAxis':
            return partial(self._getter_pos_axis, ci)
        elif ci.signal_name == 'PosTgtenc':
            return partial(self._getter_pos_tgtenc, ci)
        elif ci.signal_name == 'PosShftenc':
            return partial(self._getter_pos_shftenc, ci)
        elif ci.signal_name == 'PosEncin':
            return partial(self._getter_pos_encin, ci)
        elif ci.signal_name == 'PosAbsenc':
            return partial(self._getter_pos_absenc, ci)
        elif ci.signal_name == 'PosInpos':
            return partial(self._getter_pos_inpos, ci)
        elif ci.signal_name == 'PosMotor':
            return partial(self._getter_pos_motor, ci)
        elif ci.signal_name == 'PosCtrlenc':
            return partial(self._getter_pos_ctrlenc, ci)
        elif ci.signal_name == 'PosMeasure':
            return partial(self._getter_pos_measure, ci)
        elif ci.signal_name == 'DifAxMeasure':
            return partial(self._getter_dif_ax_measure, ci)
        elif ci.signal_name == 'DifAxMotor':
            return partial(self._getter_dif_ax_motor, ci)
        elif ci.signal_name == 'DifAxTgtenc':
            return partial(self._getter_dif_ax_tgtenc, ci)
        elif ci.signal_name == 'DifAxShftenc':
            return partial(self._getter_dif_ax_shftenc, ci)
        elif ci.signal_name == 'DifAxCtrlenc':
            return partial(self._getter_dif_ax_ctrlenc, ci)
        elif ci.signal_name == 'EncEncin':
            return partial(self._getter_enc_encin, ci)
        elif ci.signal_name == 'EncAbsenc':
            return partial(self._getter_enc_absenc, ci)
        elif ci.signal_name == 'EncTgtenc':
            return partial(self._getter_enc_tgtenc, ci)
        elif ci.signal_name == 'EncInpos':
            return partial(self._getter_enc_inpos, ci)
        elif ci.signal_name == 'StatMoving':
            return partial(self._getter_stat_moving, ci)
        elif ci.signal_name == 'StatSettling':
            return partial(self._getter_stat_settling, ci)
        elif ci.signal_name == 'StatOutofwin':
            return partial(self._getter_stat_outofwin, ci)
        elif ci.signal_name == 'StatReady':
            return partial(self._getter_stat_ready, ci)
        elif ci.signal_name == 'StatStopcode':
            return partial(self._getter_stat_stopcode, ci)
        elif ci.signal_name == 'StatWarning':
            return partial(self._getter_stat_warning, ci)
        elif ci.signal_name == 'StatLim+':
            return partial(self._getter_stat_limit_positive, ci)
        elif ci.signal_name == 'StatLim-':
            return partial(self._getter_stat_limit_negative, ci)
        elif ci.signal_name == 'StatHome':
            return partial(self._getter_stat_home, ci)
        elif ci.signal_name == 'MeasI':
            return partial(self._getter_meas_i, ci)
        elif ci.signal_name == 'MeasIa':
            return partial(self._getter_meas_ia, ci)
        elif ci.signal_name == 'MeasIb':
            return partial(self._getter_meas_ib, ci)
        elif ci.signal_name == 'MeasVm':
            return partial(self._getter_meas_vm, ci)
        else:
            print('Internal error! No function would map to signal ' + ci.signal_name)
            return None

    def remove_curve_plot(self, ci):
        """
        Remove a curve from the plot area.

        ci - Curve item to remove.
        """
        self.view_boxes[ci.y_axis_idx].removeItem(ci.curve_plot)

    def prepare_closed_loop(self):
        """Display a specific set of curves."""
        self.remove_all_signals()
        drv_idx = self.ui.cbDriver.currentIndex()
        self.add_curve(drv_idx, 'PosAxis', 0)
        self.add_curve(drv_idx, 'DifAxTgtenc', 1)
        self.add_curve(drv_idx, 'DifAxMotor', 1)
        self.add_curve(drv_idx, 'StatReady', 2)
        self.add_curve(drv_idx, 'StatMoving', 2)
        self.add_curve(drv_idx, 'StatSettling', 2)
        self.add_curve(drv_idx, 'StatOutofwin', 2)

    def prepare_currents(self):
        """Display a specific set of curves."""
        self.remove_all_signals()
        drv_idx = self.ui.cbDriver.currentIndex()
        self.add_curve(drv_idx, 'PosAxis', 0)
        self.add_curve(drv_idx, 'MeasI', 1)
        self.add_curve(drv_idx, 'MeasVm', 2)

    def prepare_target(self):
        """Display a specific set of curves."""
        self.remove_all_signals()
        drv_idx = self.ui.cbDriver.currentIndex()
        self.add_curve(drv_idx, 'PosAxis', 0)
        self.add_curve(drv_idx, 'EncTgtenc', 1)

    def now_button_clicked(self):
        """Pan X axis to display current values."""
        now = time.time() - self.ref_time
        x_small = self.view_boxes[0].viewRange()[0][0]
        x_big = self.view_boxes[0].viewRange()[0][1]
        self.view_boxes[0].setXRange(now - (x_big - x_small), now, padding=0)

    def pause_button_clicked(self):
        """Freeze the X axis."""
        if self.ticker.isActive():
            self.ticker.stop()
            self.ui.btnPause.setText('Run')
        else:
            self.ticker.start(self.tick_interval)
            self.ui.btnPause.setText('Pause')

    def _tick(self):
        now = time.time() - self.ref_time
        x_small = self.view_boxes[0].viewRange()[0][0]
        x_big = self.view_boxes[0].viewRange()[0][1]
        now_in_range = self.last_now <= x_big
        if now_in_range:
            self.view_boxes[0].setXRange(now - (x_big - x_small), now, padding=0)
        self.ui.btnNow.setDisabled(now_in_range)
        for ci in self.curve_items:
            try:
                val = self._signal_val_getter[ci]()
                if ci.start_over:
                    ci.array_time = [now]
                    ci.array_val = [val]
                    ci.val_max = val
                    ci.val_min = val
                    ci.start_over = False
                else:
                    ci.array_time.append(now)
                    ci.array_val.append(val)
                    if val > ci.val_max:
                        ci.val_max = val
                    elif val < ci.val_min:
                        ci.val_min = val
                ci.curve_plot.setData(x=ci.array_time, y=ci.array_val)
            except RuntimeError as e:
                err = 'Failed to update curve plot for signal {}\n{}'.format(ci.signal_name, e)
                print(err)
        self.last_now = now
        self.ticker.start(self.tick_interval)
