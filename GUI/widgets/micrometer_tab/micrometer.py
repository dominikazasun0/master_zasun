__author__ = "Dominika Zasuń"
__copyright__ = ""
__version__ = "1.0"
__email__ = "d.zasun@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

# --------- created using Python 3.12.0 --------------
import sys
import serial
import threading
from PySide6.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtCore import Slot, Signal, QObject
from .ui_micrometer import Ui_micrometer
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, DELAY_MAP, DELAY_MAP, Priority, State

import logging
log = logging.getLogger("GUI")

class Micrometer(QWidget):
    controlRequest = Signal(str, str, int)  # passing dev_label, client_id, priority level
    preemptDone = Signal(str, str, str)  # passing dev_label, client_id, token
    command = Signal(str, str, dict)  # passing dev_label, client_id, dict of method + arguments

    def __init__(self):
        super().__init__()
        self.ui = Ui_micrometer()
        self.ui.setupUi(self)
        self.dev_label = "MICRO"
        self.client_id = "tabs/MICRO"
        self.token = None
        self._have_control = False  # flaga kontroli nad urządzeniem
        self.measuring = False

        self.preempt = False  # flaga wywłaszczania

        # maszyna stanów
        self.param_pending = {
            "position": False
        }

        self.current_pos = 0.0

        # Etykieta wyświetlająca ostatnie dane
        self.label = QLabel("Waiting for data ...")

        # Układ czasu odświeżania
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()

        # Główny układ
        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addLayout(refresh_layout)

        self.ui.reqCtrl.clicked.connect(self.request_control)

        # mapa wyborów opóźnień
        self.delay = int(DELAY_MAP[1])
        self.ui.delay_comboBox.addItems(DELAY_MAP)
        self.ui.delay_comboBox.setCurrentText(DELAY_MAP[1])  # domyślne 10 ms
        self.ui.delay_comboBox.currentIndexChanged.connect(self.on_delay_changed)

        # przyciski
        self.ui.startButton.setText("Start")
        self.ui.startButton.setEnabled(False)
        self.ui.startButton.clicked.connect(self.toggle_on_off)

    @Slot()
    def request_control(self):
        log.debug(f"request_control: dev_label {self.dev_label}, client_id {self.client_id}")   #dev_label "MICRO", client_id="tabs/MICRO"
        self.controlRequest.emit(self.dev_label, self.client_id, Priority.Manual)

    @Slot(str, str, str)
    def _on_granted(self, dev_label:str, client_id:str, token:str):
        if self.dev_label != dev_label:
            return
        if self.client_id != client_id:
            return
        self._have_control = True
        self.ui.startButton.setEnabled(True)
        self.setEnabled(True)
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
        if self.measuring:
            self.command.emit(self.dev_label, self.client_id,{"method" : "switch_on_off", "kwargs" : {"on": False}})
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
        self.token = None

    """ ----- interpreter ----- """
    @Slot(str, dict)
    def response_interp(self, client_id: str, response: dict):
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

    def on_position_acquired(self, pos):
        # zapisanie zmiennych w klasie
        self.current_pos = pos

        self.param_pending["position"] = True
        self.try_finish_param_load()

    def try_finish_param_load(self):
        log.debug(f"try {self.param_pending}")
        if all(self.param_pending.values()):
            self.update_gui_from_params()

    def update_gui_from_params(self):
        # pozycja aktualna
        self.ui.label.setText(str(f"{self.current_pos:.2f}"))
    """ ------------------------------------------------------- """

    """ ---------- ustawienie workera i urządzenia ------------ """
    def set_param(self):
        # odczytaj i ustaw wartości
        try:
            self.delay = int(self.ui.delay_comboBox.currentText())
        except ValueError:
            QMessageBox.warning(self, "Input error", "Invalid refresh parameters")
            return
        #log.debug(f"dev_label: {self.dev_label} client_id {self.client_id}")
        self.command.emit(self.dev_label, self.client_id,{"method" : "configure",
                                    "kwargs" : {"refresh_time" : self.delay}})

    @Slot(bool)
    def _on_toggled(self, running:bool):
        self.measuring = running
        if self.measuring:
            self.ui.startButton.setText("Stop")
        else:
            self.ui.startButton.setText("Start")
            if self.preempt:
                self.preempt = False
                self.preemptDone.emit(self.dev_label, self.client_id, self.token)
                self.token = None
                self._have_control = False

        log.info(f"MITUTOYO measure: {str(self.measuring)}")

    def toggle_on_off(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if not self.measuring:
            # Start
            self.set_param()
            #log.debug(f"dev_label: {self.dev_label} client_id {self.client_id}")
            self.command.emit(self.dev_label, self.client_id,{"method" : "switch_on_off", "kwargs" : {"on": True}})
        else:
            # Stop
            self.command.emit(self.dev_label, self.client_id,{"method" : "switch_on_off", "kwargs" : {"on": False}})

    def on_delay_changed(self, idx: int):
        """Obsługa wyboru z QComboBox"""
        if 0 <= idx < len(DELAY_MAP):
            delay = int(DELAY_MAP[idx])
            self.command.emit(self.dev_label, self.client_id,{"method" : "set_delay", "kwargs" : {"value" : delay}})
            log.info(f"[Positioner] Delay changed to {delay} [ms]")

    @Slot(float)
    def update_data(self, pos):
        """Aktualizuje etykietę z nowymi danymi"""
        self.ui.label.setText(str(pos))



