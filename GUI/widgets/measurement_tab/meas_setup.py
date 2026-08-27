

import copy
from typing import Dict, Any
from OpenGL.converters import ReturnValues
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QMetaObject, QMutex, QWaitCondition, Slot, QTimer, Signal, QThread, QObject
from PySide6.QtGui import QStandardItemModel, QStandardItem
from .ui_meas_setup import Ui_measurement
from src.Utils.config_files.measure_config import DEV_ROW, MEASURE_MODE_MAP, UNITS_MAP, Priority, State

import logging

log = logging.getLogger("GUI")

class MeasSetup(QWidget):

    controlRequest = Signal(str, str, int) # passing dev_label, client_id, priority level
    controlRelease = Signal(str, str, str) # passing dev_label, client_id, token
    command = Signal(str, str, dict)       # passing dev_label, client_id, dict of method + arguments

    def __init__(self, workers: dict, threads:dict, mediator:QObject, parent=None):
        super().__init__(parent)
        self.ui = Ui_measurement()
        self.ui.setupUi(self)
        self.parent = parent
        self.dev_label = "MEAS"
        self.client_id = "tabs/MEAS"
        self.sub_client_id = None
        self._workers = workers
        #print(f"Meas_worker {self._workers["MEAS"]}; workers {workers}")
        self._threads = threads
        self.mediator = mediator

        self._devs = {
            name: {"worker": self._workers.get(name), "control": False} for name in DEV_ROW.keys()
        }

        self._tokens = {}
        self.have_control = False
        self.selected_mode = ""
        self.selected_devs = []

        # devices connected
        self.received = {}

        # usuwa wszystkie domyślne strony oprócz jednej pustej z QStackedWidget (setup_widget)
        while self.ui.setup_widget.count() > 1:
            widget = self.ui.setup_widget.widget(1)
            self.ui.setup_widget.removeWidget(widget)
            widget.deleteLater()

        self.pages = {"": self.ui.page_empty}
        for name in MEASURE_MODE_MAP.keys():
            if name:  # pomijamy pusty - juz jest
                self.pages[name] = getattr(self.parent, name)

        # tryby pomiarów aktywne - na razie żadne
        self.enabled_modes = []

        # tworzymy model dla comboBox
        self.model = QStandardItemModel(self.ui.setup_comboBox)
        self.populate_combo()
        self.ui.setup_comboBox.setModel(self.model)

        # measure mode
        labels = list(MEASURE_MODE_MAP.keys())
        self.setup_id = {}
        for name in labels:
            idx = self.ui.setup_widget.addWidget(self.pages[name])
            self.setup_id[name] = idx
            #print(f"meas_setup init idx {idx} {self.pages[name]}")

        self.ui.setup_comboBox.currentIndexChanged.connect(self.ui.setup_widget.setCurrentIndex)
        self.ui.setup_comboBox.currentTextChanged.connect(self.on_measurement_mode_changed)

        self.ui.setup_comboBox.setCurrentIndex(0)
        self.ui.setup_widget.setCurrentIndex(self.setup_id[labels[0]])

        self.ui.startButton.setEnabled(False)
        self.ui.startButton.clicked.connect(self.toggle_on_off)

        self.ui.pauseButton.setEnabled(False)
        self.ui.pauseButton.clicked.connect(self.toggle_pause)

        self.ui.reqCtrl_btn.setEnabled(False)
        self.ui.reqCtrl_btn.clicked.connect(self.toggle_ctrl)

        # stan ruchu
        self.master_measuring = False
        self._paused_GUI = False

    def request_control(self):
        for dev_label in self.selected_devs:
            log.debug(f"request_control: dev_label {dev_label}, client_id {self.client_id}")
            self.controlRequest.emit(dev_label, self.client_id, Priority.Measurement)

    @Slot(str, str, str)
    def _on_granted(self, dev_label:str, client_id:str, token:str):
        if self.client_id != client_id:
            return
        self._tokens[dev_label] = token
        self.selected_devs[dev_label]["control"] = True
        if all(state["control"] for state in self.selected_devs.values()):
            # All devices are connected!
            self.have_control = True
            self.ui.reqCtrl_btn.setText("Release All")
            self.ui.setup_comboBox.setEnabled(False)
            self.get_dev_config()


    """ ----- interpreter ----- """
    @Slot(str, dict)
    def response_interp(self, client_id:str, response: Dict):
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
    def get_dev_config(self):
        for dev in MEASURE_MODE_MAP[self.selected_mode]:
            log.info(f"get config of {dev} for mode: {self.selected_mode}")
            self.command.emit(self.dev_label, self.client_id, {"method": "get_dev_config",
                                                               "kwargs" : {
                                                                   "dev_label" : dev}})
    def _on_get_devs_config(self, dev_label:str):
        self.selected_devs[dev_label]["configured"] = True
        if all(state["configured"] for state in self.selected_devs.values()):
            # All devices are configured, ready to start meas
            log.info("Ready to start measuring.")
            self.ui.startButton.setEnabled(True)

    def toggle_ctrl(self):
        if self.have_control:
            self.release_all()
        else:
            self.request_control()

    @Slot(str,bool)
    def check_mode_ready(self, name: str, connected: bool):

        self._devs[name]["control"] = connected
        if connected:
            self.received[name] = True
        elif name in self.received:
            del self.received[name]

        received_set = set(self.received.keys())

        for mode, devices in MEASURE_MODE_MAP.items():
            # pomijamy pusty tryb
            if not mode:
                continue
            device_set = set(devices)

            if device_set.issubset(received_set):
                self.enabled_modes.append(mode)

        log.info(f"Measurements modes enabled: {self.enabled_modes}")
        self.populate_combo()


    def populate_combo(self):
        """Odświeża listę trybów w comboboxie"""
        self.model.clear()
        # odłączamy na chwilę
        #self.ui.setup_comboBox.currentTextChanged.disconnect(self.on_measurement_mode_changed)
        self.ui.setup_comboBox.blockSignals(True)
        for mode in MEASURE_MODE_MAP.keys():
            item = QStandardItem(mode)
            if mode not in self.enabled_modes:
                item.setFlags(Qt.NoItemFlags)  # wyszarzone, nieaktywne
                item.setForeground(Qt.gray)  # opcjonalnie – kolor szary

            self.model.appendRow(item)
        # podłączam z powrotem
        self.ui.setup_comboBox.blockSignals(False)
        #self.ui.setup_comboBox.currentTextChanged.connect(self.on_measurement_mode_changed)

    # przy wyborze w comboBox
    def on_measurement_mode_changed(self, mode: str):
        log.debug(f"Measurement mode chosen 1 {mode}")
        idx = self.ui.setup_comboBox.currentIndex()
        self.selected_devs = None

        if mode and mode in MEASURE_MODE_MAP:
            self.command.emit(self.dev_label, self.client_id, {"method" : "mode_update", "kwargs" : {"mode" : mode}})
            self.selected_devs = {dev: {"control": False, "configured": False} for dev in MEASURE_MODE_MAP[mode]}

            log.debug(f"Measurement mode chosen 2 {mode} devices {self.selected_devs}")
            # etykiety (label) tylko dla dostępnych urządzeń
            selected_labels = []
            for dev_name in self.selected_devs:
                label_attr = f"{dev_name}_label"
                if hasattr(self._workers[dev_name], "model"):
                    label_value = getattr(self._workers[dev_name], "model")

                    selected_labels.append(label_value)
                else:
                    selected_labels.append(" ")
            

            # Wyświetl etykiety w GUI
            selected_labels = [label for label in selected_labels if label is not None]
            devices_str = "  +  ".join(selected_labels)
            log.debug(f"Mode {mode}: selected_keys = {self.selected_devs}, labels = {selected_labels}")

            # sub widget
            self.sub_client_id = getattr(self.ui.setup_widget.currentWidget(), "client_id", None)
            self.selected_mode = mode
            log.debug(f"on_measurement_mode_changed: dev_label {self.client_id}, sub_client_id {self.sub_client_id}")

            names = [name for name, dev in self._devs.items() if dev.get("control") is True]
            text = (", ".join(names) if names else "— none —")

            self.ui.dev_name.setText(f"Devices: {devices_str}")
            self.ui.reqCtrl_btn.setEnabled(True)
        else:
            self.sub_client_id = None
            self.ui.dev_name.setText("Devices: ")
            self.ui.startButton.setEnabled(False)
            self.ui.pauseButton.setEnabled(False)
            self.ui.reqCtrl_btn.setEnabled(False)

    def _on_toggled(self, running:bool):
        self.master_measuring = running
        if self.master_measuring:
            log.debug(f"start toggle from client_id {self.client_id} for mode: {self.sub_client_id} run: {str(self.master_measuring)}")
            self.ui.setup_comboBox.setEnabled(False)
            self.ui.reqCtrl_btn.setEnabled(False)
            self.ui.startButton.setText("Stop")
            self.ui.pauseButton.setEnabled(True)
            self.ui.setup_comboBox.setEnabled(False)
        else:
            self.ui.reqCtrl_btn.setEnabled(True)
            self.ui.startButton.setText("Start")
            self.ui.pauseButton.setEnabled(False)

    def toggle_on_off(self):
        if not self.master_measuring:
            self.command.emit(self.dev_label, self.client_id, {"method": "meas_prepare", "kwargs": {}})
        else:
            # Stop
            self.command.emit(self.dev_label, self.client_id, {"method": "switch_on_off", "kwargs": {"on":False}})

    @Slot(bool)
    def _on_pause_toggled(self, pausing:bool):
        self._paused_GUI = pausing
        if self._paused_GUI:
            self.ui.pauseButton.setText("Resume")
        else:
            self.ui.pauseButton.setText("Pause")

        log.info(f"Measurement run: {str(self.master_measuring)} pause: {self._paused_GUI}")

    def toggle_pause(self):
        if self._paused_GUI:
            # Resume
            self.command.emit(self.dev_label, self.client_id, {"method": "pause_on_off", "kwargs": {"on": False}})
            self.ui.pauseButton.setText("Pause")
        else:
            # Pause
            self.command.emit(self.dev_label, self.client_id, {"method": "pause_on_off", "kwargs": {"on": True}})
            self.ui.pauseButton.setText("Resume")
    
    def _on_stopped(self):
        """
        Somthing to do.
        """
        pass

    def _on_finished(self):
        """
        Somthing to do.
        """
        pass

    @Slot(str)
    def release_all(self):
        log.debug(f"Release devices from owner {self.client_id}")
        self.ui.startButton.setEnabled(False)
        for dev in MEASURE_MODE_MAP[self.selected_mode]:
            self.controlRelease.emit(dev, self.client_id, self._tokens[dev])
    
    @Slot(str,str)
    def _on_revoked(self, dev_label:str, client_id:str):
        if self.client_id != client_id:
            return
        log.debug(f"Control on {dev_label} revoked.")
        self.selected_devs[dev_label]["control"] = False
        self.selected_devs[dev_label]["configured"] = False
        if all(not state["control"] for state in self.selected_devs.values()):
            self.have_control = False
            self.ui.reqCtrl_btn.setText("Get Control")
            self.ui.setup_comboBox.setEnabled(True)