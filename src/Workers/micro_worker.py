__author__ = "Dominika Zasuń"
__copyright__ = ""
__version__ = "1.0"
__email__ = "d.zasun@microamp-solutions.com"
__status__ = "Research"
__year__ = "2025"

import threading
import logging
from enum import IntEnum
from typing import Dict, Any
from PySide6.QtCore import Qt, QSize, QThread, QEventLoop, QTimer, Slot, QObject, Signal
from src.Drivers.MITU_driver.MITU_driver import MITU_driver
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, Priority, State
from src.Workers.DEV_worker import DEV_Worker, WorkerState

log = logging.getLogger("GUI")

class MicroWorker(DEV_Worker):

    ready = Signal(str, bool)  # passing dev_label, response
    shutdown = Signal(str, bool)  # passing dev_label, response
    response = Signal(str, dict)  # passing client_id, dict of method + arguments
    progress = Signal(str)  # passing message
    stateChanged = Signal(int)  # passing new state number
    faultOccurred = Signal(str, str)  # passing dev_label, message
    heartbeat = Signal(str)  # passing dev_label

    def __init__(self, dev_label: str):
        super().__init__(dev_label)

        self.data = 0.0

    def set_device(self, dev_model: str, dev_address: str):
        self.model = "MITUTOYO"
        self.device = MITU_driver(dev_address)

    @Slot(str, dict)
    def response_interp(self, client_id:str, response: Dict):
        if self.dev_label != client_id:
            return
        method = response.get("method")
        kwargs = response.get("kwargs", {})
        fn = getattr(self, method, None)
        if callable(fn):
            fn(**kwargs)
        else:
            log.error(f"{client_id} has no method {method}.")

    @Slot(str, str, str)
    def connect(self, dev_label: str, dev_model: str, dev_address: str):
        log.debug(f"dev_label {dev_label} model {self.model} address {dev_address}")
        if self.dev_label != dev_label:
            return
        try:
            self.set_device(dev_model, dev_address)
            if not self.device:
                raise Exception("no device")
            self.device.connect()
            status = self.device.is_connected()
            if status:
                log.debug(f"{dev_label} model {self.model} connected.")
                self.ready.emit(self.dev_label, True)
            else:
                log.error(f"Connection to MICRO {self.model} failed.")
                self.ready.emit(self.dev_label, False)
        except Exception as e:
            log.error(f"Connection failed: {e}")
            self.ready.emit(self.dev_label, False)

    @Slot(str)
    def disconnect(self, dev_label: str):
        if self.dev_label != dev_label:
            return
        try:
            self.stop()
            self.device.disconnect()
            log.debug(f"{dev_label} model {self.model} disconnected.")
            self.shutdown.emit(self.dev_label, True)
        except Exception as e:
            log.error(f"Disconnect failed: {e}")
            self.shutdown.emit(self.dev_label, False)

    def configure(self, refresh_time):
        """Ustawia odświeżanie odczytu."""
        self.refresh_time = refresh_time
        status = self.device.is_ready()
        log.debug(f"MICRO ready: {status}")

    @Slot(bool)
    def switch_on_off(self, on: bool):

        if (self.device is None) or (not self.device.is_connected()):
            log.error("Device is not set")
            self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": False}})
            return
        try:
            self._running = on
            if on:
                self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": on}})
                log.info("Device started")
                # --- start ---
                self.state = WorkerState.GET_DATA
                #self.should_continue = True
                #self._do_next_event(self.owner)
            else:
                self.should_continue = False
                log.info("Device stopped")
                self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": on}})
                self.state = WorkerState.FINISHED
                #self.owner = None

            self._do_next_event()

        except Exception as e:
            log.error(f"device error: {e}")

    def _next_in_sequ(self):

        if not self._running:
            self.state = WorkerState.IDLE
            log.debug(f"[MICROworker] NEXT IN SEQU, state -> {self.state}")
            return

        self.state = WorkerState.GET_DATA

        if self.owner == "tabs/MICRO":    # If it is a full run
            QTimer.singleShot(self.delay_between_use, lambda: self._do_next_event())
        else: # If it is a measurement setup
            #self.response.emit(self.owner, {"method": "_on_update", "kwargs": {"dev_label": self.dev_label, "dev_data": {"method": "on_data_acquired", "kwargs": {"pos": self.data}}}})
            self.response.emit(self.owner, {"method": "_on_event_done", "kwargs": {"dev_label": self.dev_label, "result": True}})

    @Slot(str)
    def _do_next_event(self):
        if self.device is None:
            log.error("Micrometer is not set")
            return
        #log.debug(f"[VNAWorker] DO NEXT EVENT, {self.state}")
        try:
            match self.state:
                case WorkerState.GET_DATA:
                    self.data = self.device.get_latest_data()

                    self._finished_step()

                case WorkerState.NEXT:
                    self._next_in_sequ()

                case WorkerState.FINISHED:
                    self.state = WorkerState.IDLE
                    self.owner = None

        except Exception as e:
            log.error("MICRO read error: %s", e)
            if self.owner == "tabs/MICRO":
                self.switch_on_off(False)
            else:
                self.response.emit(self.owner, {"method": "_on_event_done", "kwargs": {"dev_label" : self.dev_label,"result" : False}})

    def _finished_step(self):

        # pomiar zakończony
        self.response.emit("tabs/MICRO", {"method": "update_data", "kwargs": {"pos": self.data}})

        self.state = WorkerState.NEXT
        QTimer.singleShot(0, self._do_next_event)

    def get_data(self):
        try:
            self.data = self.device.get_latest_data()
            log.info(f"get_data {self.data}")
            # wysłanie sygnału do GUI
            self.response.emit("tabs/MICRO", {"method": "on_position_acquired",
                                            "kwargs": {"pos": self.data}})
        except Exception as e:
            log.error(str(e))

    def set_delay(self, value):
        """Ustawia opóźnienie między ruchami"""
        self.delay_between_use = value

    # Metoda dodana żeby pogodzić ze sobą calib i pnf w meas_setup
    def get_config(self):
        try:
            if self.owner != "tabs/MICRO":
                self.response.emit(self.owner, {"method": "_on_get_config",
                                                "kwargs": {"dev_label": self.dev_label,
                                                           "kwargs": {"method": "_on_get_config",
                                                                      "kwargs": {
                                                                          "data": self.data }}}})
        except Exception as e:
            log.error(f"Error in get_config: {e}")

    def _send_data_to_meas(self):
        log.info(f"CameraWorker: Przetwarzam klatkę dla {self.owner}")
        current_data =  0.0

        # 1. Pobranie i przetwarzanie klatki
        current_data = self.device.get_latest_data()
        if current_data is None:
            return
        
        # Inicjalizacja danych domyślnych
        
        
        self.response.emit(self.owner, {
            "method": "on_measurement_received",
            "kwargs": {
                "value": current_data, # Wysyłamy klatkę z narysowanym konturem
            }
        })

        # 3. Reset właściciela na podgląd ogólny
        self.owner = "tabs/MICRO"  

    # Metoda dodana żeby pogodzić ze sobą calib i pnf w meas_setup
    def meas_prepare_calib(self):
        pass

    @Slot()
    def stop(self):
        """Zatrzymaj wszystkie akcje workera"""
        try:
            self.switch_on_off(False)

        except Exception:
            pass
        log.debug("MotorWorker: shutdown done")