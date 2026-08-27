__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Research"
__year__ = "2025"

# --------- created using Python 3.12.0 --------------
import numpy as np
from PySide6.QtCore import Qt, QSize, QThread, QEventLoop, QTimer, Slot, QObject, Signal
from src.Drivers.TIC_driver.TIC_driver import TIC_driver
from src.Workers.DEV_worker import DEV_Worker, WorkerState

import logging
log = logging.getLogger("GUI")

class MotorWorker(DEV_Worker):

    ready = Signal(str, bool)  # passing dev_label, response
    shutdown = Signal(str, bool)  # passing dev_label, response
    response = Signal(str, dict)     # passing client_id, dict of method + arguments
    progress = Signal(str)           # passing message
    stateChanged = Signal(int)       # passing new state number
    faultOccurred = Signal(str, str) # passing dev_label, message
    heartbeat = Signal(str)          # passing dev_label

    def __init__(self, dev_label:str):
        super().__init__(dev_label)

        # pozycje w stopniach
        self.start_pos_deg = 0.0
        self.stop_pos_deg = 90.0
        self.step_deg = 0.9

        self.current_pos_deg = self.start_pos_deg

        # w krokach
        self.start_pos = self.start_pos_deg / self.step_deg
        self.stop_pos = self.stop_pos_deg / self.step_deg
        self.step_pos = 1

        self.current_pos = self.start_pos
        self.target_pos = None

        # prąd limit
        self.current_limit = None

    def set_device(self, dev_model:str, dev_address:str):
        self.model = dev_model.split("→")[1].strip()
        self.device = TIC_driver(dev_address)

    @Slot(str, str, str)
    def connect(self, dev_label:str, dev_model:str, dev_address:str):
        log.debug(f"dev_label {dev_label} model {self.model}")
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
                log.error(f"Connection to {dev_label} {self.model} failed.")
                self.ready.emit(self.dev_label, False)
        except Exception as e:
            log.error(f"Connection failed: {e}")
            self.ready.emit(self.dev_label, False)

    @Slot(str)
    def disconnect(self, dev_label:str):
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

    """ ---------------- wpisanie konfiguracji ---------------- """
    @Slot(float, float, float, int)
    def configure(self, start, stop, step_deg, delay):

        """Ustawia zakres ruchu."""
        self.start_pos = start
        self.stop_pos = stop

        self.step_deg = step_deg
        self.target_pos = start
        # current position
        self.get_motor_position()
        #log.debug(f"configure target_pos = {self.target_pos} stop_pos = {self.stop_pos} current_pos = {self.current_pos}")

        self.start_pos_deg = self.start_pos * self.step_deg
        self.stop_pos_deg = self.stop_pos * self.step_deg

        # zapisz krok w urządzeniu
        idx_step = int(np.log2 (1.8 / step_deg))
        self.set_step_mode(idx_step)

        # kierunek kroków
        if self.start_pos > self.stop_pos:
            self.step_pos = -1
        else:
            self.step_pos = 1

        # zapisz opóźnienie
        self.set_delay(delay)
    """ ------------------------------------------------------- """

    def set_step_mode(self, idx:int):
        # stara pozycja w krokach
        current_pos_old = self.device.get_current_position()
        #print(f"current_pos_old: {current_pos_old}")
        # stary krok w stopniach
        step_deg_old = self.step_deg
        self.device.set_step_mode(idx)
        # nowy krok w stopniach
        self.step_deg = 1.8 / (2 ** idx)
        ratio = step_deg_old / self.step_deg
        #print(f"ratio: {ratio}")
        self.current_pos = int(current_pos_old * ratio)
        #print(f"current_pos: {self.current_pos}")
        self.device.halt_and_set_position(self.current_pos)

        self.get_motor_position()
        #print(self.stop_pos)
        self.start_pos = self.start_pos_deg / self.step_deg
        self.stop_pos = self.stop_pos_deg / self.step_deg


    def set_current_limit(self, mamps: int):
        self.device.set_current_limit(mamps)

    def set_delay(self, value):
        """Ustawia opóźnienie między ruchami"""
        self.delay_between_use = value

    @Slot(bool)
    def energize_motor(self, on: bool):
        try:
            if on:
                self.device.energize()
            else:
                self.device.deenergize()
            self.response.emit(self.owner, {"method": "_on_energized", "kwargs": {"on":on}})

        except Exception as e:
            log.error(f"motor_worker energize error: {e}")

    @Slot(bool)
    def switch_on_off(self, on: bool):
        if (self.device is None) or (not self.device.is_connected()):
            log.error("Positioner is not set")
            self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": False}})
            return
        try:
            self._running = on
            if on:
                self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": on}})
                log.info("MotorWorker started")
                # --- ruch ---
                self.state = WorkerState.SET_POSITION
            else:
                log.info("Positioner stopped")
                self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": on}})
                # --- stop ---
                self.state = WorkerState.FINISHED

            self.do_next_event()

        except Exception as e:
            log.error(f"motor_worker can not move: {e}")

    def meas_prepare(self):
        self.state = WorkerState.SET_POSITION
        self.device.energize()
        if self.current_pos != self.start_pos:
            self.move_to(self.start_pos)
        self.target_pos = self.start_pos + self.step_pos

    def next_in_sequ(self):
        #log.debug(f"step_pos = {self.step_pos} current_pos = {self.current_pos} stop_pos = {self.stop_pos}")
        if ((self.step_pos > 0 and self.current_pos >= self.stop_pos) or
                (self.step_pos < 0 and self.current_pos <= self.stop_pos)):  # end of steps
            self.state = WorkerState.FINISHED
            self.device.deenergize()
            self.response.emit(self.owner, {"method": "_out_of_steps", "kwargs": {"dev_label": self.dev_label}})
        else:
            self.target_pos = int(self.current_pos + self.step_pos)
            self.state = WorkerState.SET_POSITION
            #self.response.emit("tabs/TIC", {"method": "update_motor_position", "kwargs": {"pos": self.current_pos}})

            if self.owner == "tabs/TIC":    # If it is a full run
                if not self._running:
                    self.state = WorkerState.IDLE
                    return
                QTimer.singleShot(self.delay_between_use, lambda: self.do_next_event())
            else: # If it is a measurement setup
                self.response.emit(self.owner, {"method": "_on_update",
                                                "kwargs": {
                                                    "dev_label": self.dev_label,
                                                    "dev_data": {
                                                        "method": "_on_position_acquired",
                                                        "kwargs": {"pos": self.current_pos}}}})
                self.response.emit(self.owner, {"method": "_on_event_done",
                                                "kwargs": {
                                                    "dev_label" : self.dev_label,
                                                    "result" : True}})

    @Slot(str)
    def do_next_event(self):
        if self.device is None:
            log.error("Motor is not set")
            return
        log.debug(f"[MotorWorker] DO NEXT EVENT, {self.state}")
        try:
            match self.state:
                case WorkerState.SET_POSITION:
                    log.debug(f"target pos = {self.target_pos}")

                    self.move_to(int(self.target_pos))
                    self.run_timer.start(100)  # sprawdzamy czy skończył co 100 ms

                case WorkerState.NEXT:
                    self.get_motor_position()
                    self.next_in_sequ()

                case WorkerState.FINISHED:
                    self.state = WorkerState.IDLE
                    self.owner = None

        except Exception as e:
            log.error(str(e))
            if self.owner == "tabs/TIC":
                self.switch_on_off(False)
            else:
                self.device.deenergize()
                self.response.emit(self.owner, {"method": "_on_event_done", "kwargs": {"dev_label" : self.dev_label,"result" : False}})

    def _finished_step(self):
        if self.device.is_motor_moving():
            self.get_motor_position()
            return
        # ruch zakończony
        self.run_timer.stop()
        self.state = WorkerState.NEXT
        QTimer.singleShot(0, self.do_next_event)

    def inc_decrease_pos(self, step):
        try:
            log.info(f"inc_decrease_pos to {self.target_pos}")
            if not self._running:
                self.target_pos = self.current_pos + step
                self.state = WorkerState.SET_POSITION
                self.do_next_event()
            else:
                self.target_pos = self.target_pos + step

            #self._on_move_to(int(self.current_pos))
        except Exception as e:
            log.error(str(e))

    @Slot(int)
    def move_to(self, target):
        try:
            self.device.enter_safe_start()
            log.info(f"move_to {target}")
            self.device.move_motor(int(target))
        except Exception as e:
            log.error(str(e))

    def get_motor_position(self):
        try:
            self.current_pos = self.device.get_current_position()
            log.info(f"get_motor_position {self.current_pos}")
            # wysłanie sygnału do GUI
            self.response.emit("tabs/TIC", {"method": "_on_position_acquired",
                                            "kwargs": {"pos": self.current_pos}})
        except Exception as e:
            log.error(str(e))

    @Slot()
    def get_motor_step(self):
        try:
            self.step_deg = self.device.get_step()
            # wysłanie sygnału do GUI
            self.response.emit("tabs/TIC", {"method": "_handle_step_acquired",
                                            "kwargs": {"step_deg": self.step_deg}})
        except Exception as e:
            log.error(str(e))

    @Slot()
    def get_motor_current_limit(self):
        try:
            self.device.enter_safe_start()
            self.current_limit = self.device.get_current_limit()
            # wysłanie sygnału do GUI
            self.response.emit("tabs/TIC", {"method": "_on_current_limit_acquired",
                                            "kwargs": {"mamps": self.current_limit}})
        except Exception as e:
            log.error(str(e))

    @Slot()
    def get_config(self):
        try:
            self.get_motor_step()
            self.get_motor_position()
            if self.owner != "tabs/TIC":
                # wyślij dane do ownera
                log.debug(f"get_pos_step: dev_label {self.dev_label} start, pos, stop, step -> {self.owner} on_pos_step_acquired")
                self.response.emit(self.owner, {"method" : "_on_get_config",
                                                "kwargs" : {"dev_label": self.dev_label,
                                                           "kwargs" : {"method" : "_on_get_config",
                                                                      "kwargs" : {
                                                                          "dev_label" : self.dev_label,
                                                                          "dev_config" : {
                                                                              "start_pos" : self.current_pos,
                                                                              "stop_pos" : self.stop_pos,
                                                                              "current_pos" : self.current_pos,
                                                                              "step_deg" : self.step_deg}}}}})
        except Exception as e:
            log.error(str(e))

    @Slot(int)
    def set_zero_position(self, value):
        """Ustawia aktualną pozycję jako nową zero-pos"""
        try:
            self.device.halt_and_set_position(0)
            self.get_motor_position()

        except Exception as e:
            log.error(str(e))
    # --- slot sprzątający ---
    @Slot()
    def stop(self):
        """Zatrzymaj wszystkie akcje workera"""
        try:
            self.switch_on_off(False)
            self.energize_motor(False)
        except Exception:
            pass
        log.debug("MotorWorker: shutdown done")