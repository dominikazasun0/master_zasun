__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

# --------- created using Python 3.12.0 --------------
from typing import Dict, Any

import numpy as np
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Qt, QMetaObject, Slot, Signal
from .ui_positioners import Ui_positioners
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, TIC_STEP_MAP, DELAY_MAP, Priority, State

import logging

log = logging.getLogger("GUI")

class Positioner(QWidget):

    controlRequest = Signal(str, str, int) # passing dev_label, client_id, priority level
    preemptDone = Signal(str, str, str)    # passing dev_label, client_id, token
    command = Signal(str, str, dict)       # passing dev_label, client_id, dict of method + arguments

    def __init__(self, worker):
        super().__init__()
        self.worker = worker
        self.ui = Ui_positioners()
        self.ui.setupUi(self)
        self.dev_label = "TIC_AZ"
        self.client_id = "tabs/TIC"
        self.token = None
        self._have_control = False
        self.preempt = False

        # maszyna stanów
        self.param_pending = {
            "step": False,
            "position": False,
            "current": False
        }

        # w krokach
        self.current_pos = 0
        # w stopniach
        self.start_pos_deg = 0
        self.stop_pos_deg = 90
        self.current_pos_deg = 0

        self.ui.reqCtrl.clicked.connect(self.request_control)
        self.current_limit = 576 # domyślnie [mA]
        self.ui.current_limitEntry.editingFinished.connect(self.on_current_limit_changed)

        # mapa wyborów kroku (case)
        self.step_deg = 1.8 / (2 ** 1)  # domyślnie
        self.ui.step_comboBox.addItems(TIC_STEP_MAP)
        self.ui.step_comboBox.setCurrentText(TIC_STEP_MAP[1])  # domyślne 0.9 deg
        self.ui.step_comboBox.currentIndexChanged.connect(self.on_step_changed)

        # mapa wyborów opóźnień
        self.delay = 500
        self.ui.delay_comboBox.addItems(DELAY_MAP)
        self.ui.delay_comboBox.setCurrentText(DELAY_MAP[5])  # domyślne 500 ms
        self.ui.delay_comboBox.currentIndexChanged.connect(self.on_delay_changed)

        # przyciski
        self.ui.energizeButton.setText("Energize")
        self.ui.energizeButton.clicked.connect(self.toggle_energize)
        self.ui.leftButton.clicked.connect(self.on_left_right_move)
        self.ui.rightButton.clicked.connect(self.on_left_right_move)
        self.ui.setButton.clicked.connect(self.set_zero_position)

        self.ui.startButton.setText("Start")
        self.ui.startButton.clicked.connect(self.toggle_on_off)

        # stan energize
        self.energize = False

        # stan ruchu
        self.moving = False
        self.ui.label_name.setText(f"Positioner {self.dev_label}")  # GUI widzi nazwę
        self.ui.energizeButton.setEnabled(False)

        # cały widget wyłączony
        #self.setEnabled(False)
        # przyciski wyłączone
        self._set_btns_enable(False)


    @Slot()
    def request_control(self):
        log.debug(f"request_control: dev_label {self.dev_label}, client_id {self.client_id}")  # dev_label "TIC_AZ", client_id="tabs/TIC"
        self.controlRequest.emit(self.dev_label, self.client_id, Priority.Manual)
    
    @Slot(str, str, str)
    def _on_granted(self, dev_label:str, client_id:str, token:str):
        if self.dev_label != dev_label:
            return
        if self.client_id != client_id:
            return
        self._have_control = True
        self.get_param()
        self.setEnabled(True)
        self.ui.energizeButton.setEnabled(True)
        #self._set_btns_enable(True)
        self.token = token

    @Slot(str, str)
    def _on_preempt(self, dev_label:str, client_id:str):
        """
        Obsługuje żądanie odebrania kontroli (preempt) temu klientowi.
        Jeśli pomiar trwa, najpierw go zatrzymuje, a dopiero później oddaje token.
        Jeśli nie trwa – token oddawany jest natychmiast.
        """
        if self.client_id != client_id: return # żądanie nie do nas

        self.preempt = True
        if self.moving:
            self.command.emit(self.dev_label, self.client_id,{"method" : "switch_on_off", "kwargs" : {"on": False}})
        else:
            self.preempt = False
            self.preemptDone.emit(self.dev_label, self.client_id, self.token)
            self.token = None
        self._have_control = False

    @Slot(str, str)
    def _on_denied(self, dev_label:str, client_id:str):
        if self.dev_label != dev_label:
            return
        if self.client_id != client_id:
            return
        self._have_control = False
        self.ui.reqCtrl.setEnabled(True)
        self.setEnabled(False)
        self.token = None

    """ ----- interpreter ----- """
    @Slot(str, dict)
    def response_interp(self, client_id:str, response:Dict):
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

        log.debug(f"get_param: dev_label {self.dev_label}, client_id {self.client_id}")
        self.command.emit(self.dev_label, self.client_id,{"method" : "get_motor_step", "kwargs" : {}})
        self.command.emit(self.dev_label, self.client_id,{"method" : "get_motor_position", "kwargs" : {}})
        self.command.emit(self.dev_label, self.client_id,{"method" : "get_motor_current_limit", "kwargs" : {}})

    def _handle_step_acquired(self, step_deg):
        # zapisanie zmiennych w klasie
        self.step_deg = step_deg

        self.param_pending["step"] = True
        self.try_finish_param_load()

    def _on_position_acquired(self, pos):
        # zapisanie zmiennych w klasie
        self.current_pos = pos

        self.param_pending["position"] = True
        self.try_finish_param_load()

    def _on_pos_step_acquired(self, pos, step_deg):
        # zapisanie zmiennych w klasie
        self.current_pos = pos
        self.step_deg = step_deg

        self.param_pending["position"] = True
        self.param_pending["step"] = True
        self.try_finish_param_load()

    def _on_current_limit_acquired(self, mamps):
        # zapisanie zmiennych w klasie:
        self.current_limit = mamps

        self.param_pending["current"] = True
        self.try_finish_param_load()

    def try_finish_param_load(self):
        log.debug(f"try {self.param_pending}")
        if all(self.param_pending.values()):
            self.update_gui_from_params()

    def update_gui_from_params(self):
        # krok
        self.ui.step_entry.setText(str(self.step_deg))

        # pozycja aktualna
        self.current_pos_deg = self.current_pos * self.step_deg
        self.ui.actual_posLabel.setText(str(f"{self.current_pos_deg:.2f}"))

        # limit prądu
        self.ui.current_limitEntry.setText(str(self.current_limit))
    """ ------------------------------------------------------- """

    """ ---------- ustawienie workera i urządzenia ------------ """
    def set_param(self):
        # odczytaj i ustaw wartości scanu
        try:
            # w stopniach
            self.start_pos_deg = float(self.ui.start_posEntry.text())
            self.stop_pos_deg = float(self.ui.target_posEntry.text())
            self.step_deg = float(self.ui.step_entry.text())
            #log.debug(f"Start pos: {self.start_pos_deg}°, Stop pos: {self.stop_pos_deg}°, Step: {self.step_deg}°")
            # w krokach
            start_pos = int(self.start_pos_deg / abs(self.step_deg))
            stop_pos = int(self.stop_pos_deg / abs(self.step_deg))
            #log.debug(f"Start pos: {start_pos}, Stop pos: {stop_pos}")
            self.delay = int(self.ui.delay_comboBox.currentText())
        except ValueError:
            QMessageBox.warning(self, "Input error", "Invalid scan parameters")
            return
        # do workera aby zapisał w urządzeniu
        self.command.emit(self.dev_label, self.client_id,{"method" : "configure",
                                                          "kwargs" : {
                                                              "start" : start_pos,
                                                              "stop" : stop_pos,
                                                              "step_deg" : self.step_deg,
                                                              "delay" : self.delay}})

    """ ------------------------------------------------------- """

    @Slot(bool)
    def _on_toggled(self, running:bool):
        self.moving = running
        if self.moving:
            self.ui.startButton.setText("Stop")
        else:
            self.ui.startButton.setText("Start")
            if self.preempt:
                self.preempt = False
                self.preemptDone.emit(self.dev_label, self.client_id, self.token)
                self.token = None
                self._have_control = False
        log.info(f"TIC movement: {str(self.moving)}")

    def toggle_on_off(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if not self.moving:
            # Start
            self.set_param()
            self.command.emit(self.dev_label, self.client_id,{"method" : "switch_on_off", "kwargs" : {"on": True}})
        else:
            # Stop
            self.command.emit(self.dev_label, self.client_id,{"method" : "switch_on_off", "kwargs" : {"on": False}})

    @Slot(bool)
    def _on_energized(self, on: bool):
        if on:
            log.debug("Motor energized.")
            self.ui.energizeButton.setText("Deenergize")
        else:
            log.debug("Motor de-energized.")
            self.ui.energizeButton.setText("Energize")
        self._set_btns_enable(on)
        self.energize = on

    def toggle_energize(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if not self.energize:
            # Start
            self.set_param()
            self.command.emit(self.dev_label, self.client_id,{"method" : "energize_motor", "kwargs" : {"on": True}})
        else:
            # Stop
            self.command.emit(self.dev_label, self.client_id,{"method" : "energize_motor", "kwargs" : {"on": False}})

    def move_to(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        sender = self.sender()
        try:
            #self.set_param()
            # w krokach
            current_pos = int(self.current_pos_deg / abs(self.step_deg))
            if sender == self.ui.leftButton:
                target = current_pos - 1
            elif sender == self.ui.rightButton:
                target = current_pos + 1
            else:
                return
            self.command.emit(self.dev_label, self.client_id,{"method" : "move_to", "kwargs" : {"target":target}})
        except ValueError:
            QMessageBox.warning(self, "Input error", "Invalid position")

    def on_left_right_move(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        sender = self.sender()
        try:
            # w krokach
            if sender == self.ui.leftButton:
                step = -1
            elif sender == self.ui.rightButton:
                step = 1
            else:
                return
            self.command.emit(self.dev_label, self.client_id,{"method" : "inc_decrease_pos", "kwargs" : {"step":step}})
        except ValueError:
            QMessageBox.warning(self, "Input error", "Invalid position")

    def _out_of_steps(self, dev_label:str):
        log.info(f"{dev_label} finished moving!")
        self.toggle_on_off()

    def _set_btns_enable(self, en: bool = False):
        self.ui.startButton.setEnabled(en)
        self.ui.leftButton.setEnabled(en)
        self.ui.rightButton.setEnabled(en)
        self.ui.setButton.setEnabled(en)

    def on_step_changed(self, idx: int):
        """Obsługa wyboru z QComboBox"""
        #print(f"idx: {idx}")
        if 0 <= idx < len(TIC_STEP_MAP):
            self.step_deg = 1.8 / (2 ** idx)
            self.ui.step_entry.setText(str(self.step_deg))
            self.command.emit(self.dev_label, self.client_id,{"method" : "set_step_mode", "kwargs" : {"idx" : idx}})
            log.info(f"[Positioner] Step changed to {self.step_deg}")

    def on_current_limit_changed(self):
        if not self._have_control:
            log.error(f"{self.client_id} is not the owner of {self.dev_label}")
            return
        try:
            value = int(self.ui.current_limitEntry.text())
            mamps = (value // 32) * 32  # zaokrąglenie w dół do 32 mA

            self.param_pending["current"] = False
            self.command.emit(self.dev_label, self.client_id,{"method" : "set_current_limit", "kwargs" : {"mamps" : mamps}})
        except ValueError:
            QMessageBox.warning(self, "Input error", "Invalid current value")

    def on_delay_changed(self, idx: int):
        """Obsługa wyboru z QComboBox"""
        if 0 <= idx < len(DELAY_MAP):
            delay = int(DELAY_MAP[idx])
            self.command.emit(self.dev_label, self.client_id,{"method" : "set_delay", "kwargs" : {"value" : delay}})
            log.info(f"[Positioner] Delay changed to {delay} [ms]")

    def set_zero_position(self):
        try:
            current_pos_deg = float(self.ui.actual_posLabel.text())
            step_deg = float(self.ui.step_entry.text())
            val = int(current_pos_deg / abs(step_deg))
            self.command.emit(self.dev_label, self.client_id,{"method" : "set_zero_position", "kwargs" : {"value" : val}})
        except ValueError:
            QMessageBox.warning(self, "Input error", "Invalid position")
    
    @Slot(float)
    def update_motor_position(self, pos):
        #self.step_deg = float(self.ui.step_entry.text())
        # wypisanie akualnej pozycji
        self.current_pos_deg = pos * self.step_deg
        self.ui.actual_posLabel.setText(str(f"{self.current_pos_deg:.2f}"))




