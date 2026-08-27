__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import numpy as np
import pyqtgraph as pg
import logging
from typing import Dict, Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QButtonGroup
from PySide6.QtCore import Qt, QMetaObject, Slot, Signal
from .ui_vna import Ui_vna
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, FORMAT_MAP, POWER_VNA_MAP, DELAY_MAP, Priority, State

log = logging.getLogger("GUI")


class Vna(QWidget):
    controlRequest = Signal(str, str, int)  # passing dev_label, client_id, priority level
    preemptDone = Signal(str, str, str)  # passing dev_label, client_id, token
    command = Signal(str, str, dict)  # passing dev_label, client_id, dict of method + arguments

    def __init__(self, worker):
        super().__init__()
        self.worker = worker
        self.ui = Ui_vna()
        self.ui.setupUi(self)
        self.dev_label = "VNA"
        self.client_id = "tabs/VNA"
        self.token = None
        self._have_control = False  # flaga kontroli nad urządzeniem
        self.measuring = False

        # maszyna stanów
        self.param_pending = {
            "power": False,
            "freq": False,
            "trace": False
        }
        self.preempt = False  # flaga wywłaszczania

        self.power_level = float(POWER_VNA_MAP[2])    #-20 dBm
        self.RF_state = False

        self.f_start_Hz = 10000000.0
        self.f_stop_Hz = 1000000000.0
        self.N = int(201)
        self.f_data_Hz = []

        self.trace_list_name = []
        self.sel_trace_name = ""
        self.format_selected = FORMAT_MAP["A_name"][0]  # amp [dB]

        # skale wykresu
        self.y_min_dB = -30.0
        self.y_max_dB = 0.0
        self.y_min_deg = -180.0
        self.y_max_deg = 180.0

        layout = QVBoxLayout(self.ui.plotWidgetPlaceholder)

        # Widget wykresu
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', FORMAT_MAP["A_name"][0])
        self.plot_widget.setLabel('bottom', f'Frequency [{UNITS_MAP[3]}]')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.curve = self.plot_widget.plot(pen='b', symbol='o')
        layout.addWidget(self.plot_widget)
        # sygnał 'sigRangeChanged' ViewBoxa
        self.plot_widget.getViewBox().sigRangeChanged.connect(self.on_chart_range_changed)

        # przyciski
        self.ui.getTrace.setText("Read VNA")
        self.ui.getTrace.setEnabled(False)
        self.ui.getTrace.clicked.connect(self.toggle_on_off)

        self.ui.reqCtrl.clicked.connect(self.request_control)

        # pola edycji
        self.ui.fstartEntry.editingFinished.connect(self.on_freq_N_changed)
        self.ui.fstopEntry.editingFinished.connect(self.on_freq_N_changed)
        self.ui.NEntry.editingFinished.connect(self.on_freq_N_changed)

        self.ui.ymaxEntry.setText(f"{self.y_max_dB:.1f}")
        self.ui.yminEntry.setText(f"{self.y_min_dB:.1f}")
        self.ui.ymaxEntry.editingFinished.connect(self.on_y_range_changed)
        self.ui.yminEntry.editingFinished.connect(self.on_y_range_changed)

        # pola wyboru
        # mapa wyborów opóźnień
        self.delay = 500
        self.ui.delay_comboBox.addItems(DELAY_MAP)
        self.ui.delay_comboBox.setCurrentText(DELAY_MAP[5])  # domyślne 500 ms
        self.ui.delay_comboBox.currentIndexChanged.connect(self.on_delay_changed)

        self.current_unit = 1000 ** 3  # domyślnie GHz
        self.ui.f_units_comboBox.addItems(UNITS_MAP)
        self.ui.f_units_comboBox.setCurrentText(UNITS_MAP[3])  # domyślne GHz [3]
        self.ui.f_units_comboBox.currentIndexChanged.connect(self.handle_units_changed)
        self.ui.tracelistWidget.setSelectionMode(QListWidget.SingleSelection)
        self.ui.tracelistWidget.setCurrentRow(0)
        #self.ui.tracelistWidget.setSelectionMode(QListWidget.MultiSelection)
        #item = self.ui.tracelistWidget.item(0)
        #item.setSelected(True)

        self.ui.tracelistWidget.itemSelectionChanged.connect(self.on_trace_change)

        # format radiobuttons
        self.format_group = QButtonGroup(self)
        self.format_group.addButton(self.ui.radioA)
        self.format_group.addButton(self.ui.radioB)
        self.format_group.setExclusive(True)
        # ustaw domyślne zaznaczenie po zmianie
        self.ui.radioA.setChecked(True)
        self.format_group.buttonClicked.connect(self.update_format_changed)


        self.ui.format_comboBox.addItems(FORMAT_MAP["format_name"])
        self.ui.format_comboBox.setCurrentText(FORMAT_MAP["format_name"][0])  # domyślne dB/deg [0]
        self.ui.format_comboBox.currentIndexChanged.connect(self.update_format_changed)

        self.ui.power_comboBox.addItems(POWER_VNA_MAP)
        self.ui.power_comboBox.setCurrentText(POWER_VNA_MAP[2])  # domyślne -20 dBm
        self.ui.power_comboBox.currentIndexChanged.connect(self.on_power_changed)

        self.ui.RF_checkBox.setEnabled(False)
        self.ui.RF_checkBox.setChecked(True)
        self.ui.RF_checkBox.stateChanged.connect(self.on_power_changed)

        self.ui.label_name.setText(f"VNA: {self.dev_label}")

        self.on_y_range_changed()
        self._set_btns_enable(False)

    def request_control(self):
        log.debug(f"request_control: dev_label {self.dev_label}, client_id {self.client_id}")  #dev_label "VNA", client_id="tabs/VNA"
        self.controlRequest.emit(self.dev_label, self.client_id, Priority.Manual)

    @Slot(str, str, str)
    def _on_granted(self, dev_label: str, client_id: str, token: str):
        if self.dev_label != dev_label:
            return
        if self.client_id != client_id:
            return
        log.debug(f"_on_granted: dev_label {self.dev_label}, client_id {self.client_id}")
        self._have_control = True
        self._set_btns_enable(True)
        self.get_param()
        self.token = token

    @Slot(str, str)
    def _on_preempt(self, dev_label: str, client_id: str):
        """
        Obsługuje żądanie odebrania kontroli (preempt) temu klientowi.
        Jeśli pomiar trwa, najpierw go zatrzymuje, a dopiero później oddaje token.
        Jeśli nie trwa – token oddawany jest natychmiast.
        """
        if self.client_id != client_id:  # żądanie nie do nas
            return

        self.preempt = True
        if self.measuring:
            self.command.emit(self.dev_label, self.client_id, {"method": "switch_on_off", "kwargs": {"on": False}})
        else:
            self.preempt = False
            self.preemptDone.emit(self.dev_label, self.client_id, self.token)
            self.token = None
        self._have_control = False

    @Slot(str, str)
    def _on_denied(self, dev_label: str, client_id: str):
        if self.dev_label != dev_label:
            return
        if self.client_id != client_id:
            return
        self._have_control = False
        self.ui.reqCtrl.setEnabled(True)
        self._set_btns_enable(False)
        self.token = None

    # @Slot(str, str)
    # def _on_revoked(self, dev_label:str, client_id:str):

    def _set_btns_enable(self, en: bool = False):
        self.ui.getTrace.setEnabled(en)
        self.ui.RF_checkBox.setEnabled(en)
        self.ui.radioA.setEnabled(en)
        self.ui.radioB.setEnabled(en)

    """ ----- interpreter ----- """
    @Slot(str, dict)
    def response_interp(self, client_id: str, response: Dict):
        if self.client_id != client_id:
            return
        method = response.get("method")
        kwargs = response.get("kwargs", {})
        fn = getattr(self, method, None)
        if callable(fn):
            fn(**kwargs)
        else:
            log.error(f"{client_id} has no method {method}.")
    """ ------------------------------------------------------- """

    """ ----- pobieranie workerem parametrów z urządzenia ----- """
    def get_param(self):
        for k in self.param_pending:
            self.param_pending[k] = False

        log.debug(f"vna get_param: dev_label {self.dev_label}, client_id {self.client_id}")
        self.command.emit(self.dev_label, self.client_id, {"method": "get_vna_power", "kwargs": {}})
        self.command.emit(self.dev_label, self.client_id, {"method": "get_vna_freq_N", "kwargs": {}})
        self.command.emit(self.dev_label, self.client_id, {"method": "get_vna_traces", "kwargs": {}})

    def on_power_acquired(self, power_level: float, RF_on: bool):
        power_closest = min(POWER_VNA_MAP, key=lambda x: abs(float(x) - float(power_level)))
        # zapisanie zmiennych w klasie
        self.power_level = float(power_closest)
        self.RF_state = RF_on

        self.param_pending["power"] = True
        self.try_finish_param_load()

    def on_freq_N_acquired(self, f_start_Hz, f_stop_Hz, N):
        # zapisanie zmiennych w klasie
        self.f_start_Hz = f_start_Hz
        self.f_stop_Hz = f_stop_Hz
        self.N = N
        # wpisanie wektora częstotliwości
        self.f_data_Hz = np.linspace(self.f_start_Hz, self.f_stop_Hz, self.N)

        self.param_pending["freq"] = True
        self.try_finish_param_load()

    def on_trace_list_acquired(self, trace_list, current_trace):
        # zapisanie zmiennych w klasie
        self.trace_list_name = [entry.get("name", "").strip('"') for entry in trace_list ]
        self.sel_trace_name = current_trace

        self.param_pending["trace"] = True
        self.try_finish_param_load()

    def try_finish_param_load(self):
        log.debug(f"try {self.param_pending}")
        if all(self.param_pending.values()):
            self.update_gui_from_params()

    def update_gui_from_params(self):

        # moc
        self.ui.power_comboBox.setCurrentText(str(self.power_level))
        self.ui.RF_checkBox.setChecked(self.RF_state)

        # częstotliwości
        self.ui.fstartEntry.setText(str(self.f_start_Hz / self.current_unit))
        self.ui.fstopEntry.setText(str(self.f_stop_Hz / self.current_unit))
        self.ui.NEntry.setText(str(self.N))

        # oś x wykresu
        x_min = float(self.ui.fstartEntry.text())
        x_max = float(self.ui.fstopEntry.text())
        self.plot_widget.getViewBox().enableAutoRange(axis=pg.ViewBox.XAxis, enable=False)
        self.plot_widget.setXRange(x_min, x_max, padding=0)

        # trace - y
        self.ui.tracelistWidget.blockSignals(True)

        self.ui.tracelistWidget.clear()
        log.debug(f"trace list {self.trace_list_name}")
        log.debug(f"trace item {self.ui.tracelistWidget.currentIndex()}")

        for name in self.trace_list_name:
            item = QListWidgetItem(name)
            self.ui.tracelistWidget.addItem(item)

        # zaznaczenie poprzednio wybranego trace, jeśli istnieje
        found = False
        log.debug(f"Selected trace: {self.sel_trace_name}")
        if self.sel_trace_name:
            for i in range(self.ui.tracelistWidget.count()):
                item = self.ui.tracelistWidget.item(i)
                if item.text() == self.sel_trace_name:
                    item.setSelected(True)
                    found = True
                    break

        # jeśli poprzednia wartość nie istnieje w nowej liście, zaznacz pierwszy element
        if not found and self.ui.tracelistWidget.count() > 0:
            log.debug("Not found, selecting first trace.")
            self.ui.tracelistWidget.item(0).setSelected(True)

        self.ui.tracelistWidget.blockSignals(False)

    """ ------------------------------------------------------- """

    """ ---------- ustawienie workera i urządzenia ------------ """
    def set_param(self):
        # odczytaj i ustaw wartości
        try:
            x_min = float(self.ui.fstartEntry.text())
            x_max = float(self.ui.fstopEntry.text())
            self.N = int(self.ui.NEntry.text())
            self.f_start_Hz = x_min * self.current_unit
            self.f_stop_Hz = x_max * self.current_unit
            self.power_level = float(self.ui.power_comboBox.currentText())
            self.RF_state = self.ui.RF_checkBox.isChecked()
            self.delay = int(self.ui.delay_comboBox.currentText())
        except ValueError:
            # nieprawidłowy wpis — zignoruj
            log.debug(f"invalid entry")
            return
        # do workera aby zapisał w urządzeniu
        log.debug(f"Selected name: {self.sel_trace_name}")
        self.command.emit(self.dev_label, self.client_id, {"method": "configure",
                                                           "kwargs": {"f_start_Hz": self.f_start_Hz,
                                                                      "f_stop_Hz": self.f_stop_Hz,
                                                                      "N": self.N,
                                                                      "sel_trace_name": self.sel_trace_name,
                                                                      "power_level": self.power_level,
                                                                      "RF_state": self.RF_state,
                                                                      "delay": self.delay}})

    @Slot(bool)
    def _on_toggled(self, running: bool):
        self.measuring = running
        if self.measuring:
            self.ui.getTrace.setText("Stop VNA")
        else:
            self.ui.getTrace.setText("Read VNA")
            if self.preempt:
                self.preempt = False
                self.preemptDone.emit(self.dev_label, self.client_id, self.token)
                self.token = None


    """-----callbacki------"""
    @Slot()
    def toggle_on_off(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if not self.measuring:
            log.debug(f"{self.client_id} control {self.dev_label}")
            self.set_param()
            # Start
            self.command.emit(self.dev_label, self.client_id, {"method": "switch_on_off", "kwargs": {"on": True}})
        else:
            # Stop
            self.command.emit(self.dev_label, self.client_id, {"method": "switch_on_off", "kwargs": {"on": False}})

    # ustaw zadane parametry w workerze i urządzeniu

    def on_power_changed(self, idx: int):
        """Obsługa wyboru z QComboBox"""
        if 0 <= idx < len(POWER_VNA_MAP):
            power_level = float(self.ui.power_comboBox.currentText())
            RF_state = self.ui.RF_checkBox.isChecked()

            self.param_pending["power"] = False
            self.command.emit(self.dev_label, self.client_id, {"method": "set_vna_power",
                                                               "kwargs": {"power_level": power_level, "on": RF_state}})
        else:
            log.debug(f"[Vna] ")

    def on_trace_change(self):
        """obsłuba wyboru trace-ów"""
        current_item  = self.ui.tracelistWidget.currentItem()
        #selected_items  = self.ui.tracelistWidget.selectedItems()
        #current_item = [item.text() for item in selected_items]

        log.debug(f"Current item {current_item} sel_trace_name: {self.sel_trace_name}")
        if current_item is None:
            # brak zaznaczenia
            self.sel_trace_name = None
            sel_idx_trace = None
            log.debug("Brak zaznaczenia")
            return

        # Zapisz tekst (np. "S11") i indeks w liście
        self.sel_trace_name = current_item.text()
        sel_trace_idx = self.ui.tracelistWidget.currentRow()
        log.debug(f"Selected name: {self.sel_trace_name}, Selected idx: {sel_trace_idx}")

        self.param_pending["trace"] = False
        self.command.emit(self.dev_label, self.client_id, {"method": "set_vna_trace",
                                                           "kwargs": {"current_trace": self.sel_trace_name}})

    def on_freq_N_changed(self):
        try:
            x_min = float(self.ui.fstartEntry.text())
            x_max = float(self.ui.fstopEntry.text())
            self.plot_widget.getViewBox().enableAutoRange(axis=pg.ViewBox.XAxis, enable=False)
            self.plot_widget.setXRange(x_min, x_max, padding=0)

            self.f_start_Hz = x_min * self.current_unit
            self.f_stop_Hz = x_max * self.current_unit
            self.N = int(self.ui.NEntry.text())
            self.f_data_Hz = np.linspace(self.f_start_Hz, self.f_stop_Hz, self.N)

            self.param_pending["freq"] = False
            self.command.emit(self.dev_label, self.client_id, {"method": "set_vna_freq_N",
                                                               "kwargs": {"f_start_Hz": self.f_start_Hz,
                                                                          "f_stop_Hz": self.f_stop_Hz,
                                                                          "N": self.N}})

        except ValueError:
            # nieprawidłowy wpis — zignoruj
            log.debug(f"invalid entry")
            return

    def on_chart_range_changed(self):
        y_min, y_max = self.plot_widget.getViewBox().viewRange()[1]
        y_min = np.floor(y_min * 100) / 100  # zaokrąglenie w dół do 0.01
        y_max = np.ceil(y_max * 10) / 10  # zaokrąglenie w górę do 0.1        self.ui.ymaxEntry.setText(str(y_max))

        # blokuj sygnały, aby nie uruchomić ponownie on_y_range_changed()
        self.ui.yminEntry.blockSignals(True)
        self.ui.ymaxEntry.blockSignals(True)

        self.ui.yminEntry.setText(f"{y_min:.1f}")
        self.ui.ymaxEntry.setText(f"{y_max:.1f}")
        # odblokuj sygnały
        self.ui.yminEntry.blockSignals(False)
        self.ui.ymaxEntry.blockSignals(False)
        #print(f"Nowy zakres Y: {y_min:.2f}  →  {y_max:.2f}")

        self.calc_format_scale()

    def on_y_range_changed(self):
        try:
            y_min = float(self.ui.yminEntry.text())
            y_max = float(self.ui.ymaxEntry.text())
            self.calc_format_scale()

            self.plot_widget.getViewBox().enableAutoRange(axis=pg.ViewBox.YAxis, enable=False)
            self.plot_widget.setYRange(y_min, y_max, padding=0)
        except ValueError:
            # nieprawidłowy wpis
            log.error(f"wrong entry")
            pass

    @Slot(int)
    def handle_units_changed(self, idx: int):
        """Obsługa wyboru z QComboBox"""
        if 0 <= idx < len(UNITS_MAP):
            self.current_unit = 1000 ** idx
            self.on_freq_N_acquired(self.f_start_Hz, self.f_stop_Hz, self.N)
            log.info(f"[Vna] f_unit changed to {UNITS_MAP[idx]}")
            self.plot_widget.setLabel('bottom', f'Frequency [{UNITS_MAP[idx]}]')
        else:
            log.debug(f"[Vna] wrong unit")

    @Slot()
    def update_format_changed(self):
        idx = self.ui.format_comboBox.currentIndex()
        checked_button = self.format_group.checkedButton()
        log.debug(f"format_changed {FORMAT_MAP["format_name"][idx]} : {checked_button.text()}")

        if 0 <= idx < len(FORMAT_MAP["A_name"]):
            self.ui.radioA.setText(FORMAT_MAP["A_name"][idx])
            self.ui.radioB.setText(FORMAT_MAP["B_name"][idx])

            self.format_selected = self.format_group.checkedButton().text()
            self.plot_widget.setLabel('left', f'{self.format_selected}')

            if idx == 0:  # dB/deg
                if self.ui.radioA.isChecked():
                    y_min = self.y_min_dB
                    y_max = self.y_max_dB
                else:
                    y_min = self.y_min_deg
                    y_max = self.y_max_deg
            elif idx == 1:  # lin/rad
                if self.ui.radioA.isChecked():
                    y_min = np.pow(10, (self.y_min_dB / 20))
                    y_max = np.pow(10, (self.y_max_dB / 20))
                else:
                    y_min = self.y_min_deg * np.pi / 180
                    y_max = self.y_max_deg * np.pi / 180
            elif idx == 2:  # re/im
                y_min = -1.0
                y_max = 1.0

            self.ui.yminEntry.setText(f"{y_min:.1f}")
            self.ui.ymaxEntry.setText(f"{y_max:.1f}")
            self.on_y_range_changed()

        else:
            log.debug(f"[Vna] wrong format")
            return

    def on_delay_changed(self, idx: int):
        """Obsługa wyboru z QComboBox"""
        if 0 <= idx < len(DELAY_MAP):
            delay = int(DELAY_MAP[idx])
            self.command.emit(self.dev_label, self.client_id,{"method" : "set_delay", "kwargs" : {"value" : delay}})
            log.info(f"[Positioner] Delay changed to {delay} [ms]")



    """-----metody-----"""

    def calc_format_scale(self):
        y_min = float(self.ui.yminEntry.text())
        y_max = float(self.ui.ymaxEntry.text())
        idx = self.ui.format_comboBox.currentIndex()
        #checked_button = self.format_group.checkedButton()
        #log.debug(f"calc_scale {FORMAT_MAP["format_name"][idx]} : {checked_button.text()}")
        if idx == 0:  # dB/deg
            if self.ui.radioA.isChecked():
                self.y_min_dB = y_min
                self.y_max_dB = y_max
            else:
                self.y_min_deg = y_min
                self.y_max_deg = y_max
        elif idx == 1:  # lin/rad
            if self.ui.radioA.isChecked():
                if y_min < 1e-10:
                    self.y_min_dB = -200
                else:
                    self.y_min_dB = 20 * np.log10(y_min)
                if y_max < 1e-9:
                    self.y_min_dB = -180
                else:
                    self.y_max_dB = 20 * np.log10(y_max)
            else:
                self.y_min_deg = y_min * 180 / np.pi
                self.y_max_deg = y_max *180 / np.pi
        elif idx == 2:  # re/im
            y_min = -1.0
            y_max = 1.0

    @Slot(np.ndarray, np.ndarray)
    def _plot_trace_data(self, re_data, im_data):
        if len(self.f_data_Hz) != len(re_data):
            return
        idx = self.ui.format_comboBox.currentIndex()
        if idx == 0:  # dB/deg
            if self.ui.radioA.isChecked():
                values = 20 * np.log10(np.sqrt(pow(re_data, 2) + pow(im_data, 2)))
            else:
                values = np.degrees(np.arctan2(im_data, re_data))
        elif idx == 1:  # lin/rad
            if self.ui.radioA.isChecked():
                values = (np.sqrt(pow(re_data, 2) + pow(im_data, 2)))
            else:
                values = np.arctan2(im_data, re_data)
        elif idx == 2:  # re/im
            if self.ui.radioA.isChecked():
                values = re_data
            else:
                values = im_data
        # wyświetl
        self.curve.setData(self.f_data_Hz / self.current_unit, values, symbol=None)
