__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Research"
__year__ = "2025"

# --------- created using Python 3.12.0 --------------

from PySide6.QtCore import Qt, QSize, QThread, QEventLoop, QTimer, Slot, QObject, Signal
from src.Drivers.VNA_driver.N5224B import N5224B_driver
from src.Drivers.VNA_driver.N9918A import N9918A_driver
from src.Workers.DEV_worker import DEV_Worker, WorkerState

import logging

log = logging.getLogger("GUI")

vna_drivers = {
    "N9918A": N9918A_driver,
    "N5224B": N5224B_driver,
}


class VnaWorker(DEV_Worker):
    ready = Signal(str, bool)  # passing dev_label, response
    shutdown = Signal(str, bool)  # passing dev_label, response
    response = Signal(str, dict)  # passing client_id, dict of method + arguments
    progress = Signal(str)  # passing message
    stateChanged = Signal(int)  # passing new state number
    faultOccurred = Signal(str, str)  # passing dev_label, message
    heartbeat = Signal(str)  # passing dev_label

    def __init__(self, dev_label: str):
        super().__init__(dev_label)

        self.re_data = []
        self.im_data = []

        self.f_start_Hz = 10.0e9
        self.f_stop_Hz = 20.0e9
        self.N = 101

        self.current_trace = "CH1_S11_1"

        self.power_level = -20.0
        self.RF_state = True

    def set_device(self, dev_model: str, dev_address: str):
        self.model = dev_model.split(",")[1].strip()
        self.device = vna_drivers.get(self.model)
        log.debug(f"device: {self.device} model {dev_model}")
        self.device = self.device(dev_address)

    @Slot(str, str, str)
    def connect(self, dev_label: str, dev_model: str, dev_address: str):
        log.debug(f"dev_label {dev_label} model {dev_model} address {dev_address}")
        if self.dev_label != dev_label:
            return
        try:
            self.set_device(dev_model, dev_address)
            #self.model = dev_model.split(",")[1].strip()
            #self.device = vna_drivers.get(self.model)
            #self.device = self.device(dev_address)

            if self.device is None:
                raise Exception("no device")
            self.device.connect()
            status = self.device.is_connected()
            if status:
                log.debug(f"{dev_label} model {self.model} connected.")
                self.ready.emit(self.dev_label, True)
            else:
                log.error(f"Connection to {dev_label} model {self.model} failed.")
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

    """ ---------------- wpisanie konfiguracji ---------------- """
    @Slot(float, float, int, str, float, bool, int)
    def configure(self, f_start_Hz, f_stop_Hz, N, sel_trace_name, power_level, RF_state, delay) -> None:
        log.debug(f"f_start_Hz {f_start_Hz}, f_stop_Hz {f_stop_Hz}, N {N}, sel_trace_name {sel_trace_name}")

        # zapisz częstotliwości w urządzeniu
        self.set_vna_freq_N(f_start_Hz, f_stop_Hz, N)
        # zapisz aktywny trace
        self.set_vna_trace(sel_trace_name)
        # moc
        self.set_vna_power(power_level, RF_state)

        # zapisz opóźnienie
        self.set_delay(delay)

    """ ------------------------------------------------------- """

    @Slot(float, float, int)
    def set_vna_freq_N(self,f_start_Hz: float, f_stop_Hz: float, N: int):
        if (self.device is None) or (not self.device.is_connected()):
            log.error("VNA is not set")
            return
        try:
            log.debug(f"f_start_Hz {f_start_Hz}, f_stop_Hz {f_stop_Hz}, N {N}")
            self.device.set_frequency_range(f_start_Hz, f_stop_Hz)
            self.device.set_num_points(N)

            self.f_start_Hz = f_start_Hz
            self.f_stop_Hz = f_stop_Hz
            self.N = N

        except Exception as e:
            log.error(f"vna_worker can not control VNA: {e}")

    @Slot(str)
    def set_vna_trace(self, current_trace):
        if (self.device is None) or (not self.device.is_connected()):
            log.error("VNA is not set")
            return
        try:
            log.debug(f"current_trace: {current_trace}")
            self.device.set_active_trace(current_trace)

            self.current_trace = current_trace

        except Exception as e:
            log.error(f"vna_worker can not control VNA: {e}")

    @Slot(float, bool)
    def set_vna_power(self, power_level, on: bool):

        if (self.device is None) or (not self.device.is_connected()):
            log.error("VNA is not set")
            return
        try:
            self.device.set_pow_level(power_level, on)

            self.power_level = power_level
            self.RF_state = on

        except Exception as e:
            log.error(f"vna_worker can not control VNA: {e}")

    def set_delay(self, value):
        """Ustawia opóźnienie między ruchami"""
        self.delay_between_use = value

    @Slot(bool)
    def switch_on_off(self, on: bool):
        if (self.device is None) or (not self.device.is_connected()):
            log.error("VNA is not set")
            self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": False}})
            return

        try:
            self._running = on
            if on:
                self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": on}})
                log.info("Device started")
                # --- start ---
                self.state = WorkerState.GET_DATA
            else:
                log.info("Device stopped")
                self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": on}})
                # --- stop ---
                self.state = WorkerState.FINISHED

            self.do_next_event()

        except Exception as e:
            log.error(f"vna_worker can not measure: {e}")

    def meas_prepare(self):
        self.state = WorkerState.GET_DATA

    def next_in_sequ(self):
        if self.owner == "tabs/VNA":    # If it is a full run
            if not self._running:
                self.state = WorkerState.IDLE
                log.debug(f"[VNAworker] NEXT IN SEQU, state -> {self.state}")
                return
            self.state = WorkerState.GET_DATA
            QTimer.singleShot(self.delay_between_use, lambda: self.do_next_event())
        else: # If it is a measurement setup
            self.state = WorkerState.GET_DATA
            self.response.emit(self.owner, {"method": "_on_update", "kwargs": {"dev_label": self.dev_label, "dev_data": {"method": "_on_data_acquired",
                                                                                   "kwargs": {"re_data": self.re_data, "im_data": self.im_data}}}})
            self.response.emit(self.owner, {"method": "_on_event_done", "kwargs": {"dev_label": self.dev_label, "result": True}})


    @Slot(str)
    def do_next_event(self):
        if self.device is None:
            log.error("Vna is not set")
            return
        #log.debug(f"[VNAWorker] DO NEXT EVENT, {self.state}")
        try:
            match self.state:
                case WorkerState.GET_DATA:
                    complex_data = self.device.get_trace_data(channel=1, trace=self.current_trace)
                    self.re_data = complex_data.real
                    self.im_data = complex_data.imag
                    self.finished_step()

                case WorkerState.NEXT:
                    self.next_in_sequ()

                case WorkerState.FINISHED: # Exclusive for tabs/VNA
                    self.state = WorkerState.IDLE
                    self.owner = None

        except Exception as e:
            log.error("VNA read error: %s", e)
            if self.owner == "tabs/VNA":
                self.switch_on_off(False)
            else:
                self.response.emit(self.owner, {"method": "_on_event_done", "kwargs": {"dev_label" : self.dev_label,"result" : False}})

    def finished_step(self):
        # pomiar zakończony
        self.response.emit("tabs/VNA", {"method": "_plot_trace_data", "kwargs": {"re_data": self.re_data, "im_data": self.im_data}})

        self.state = WorkerState.NEXT
        QTimer.singleShot(0, self.do_next_event)

    def get_vna_power(self):
        try:
            self.power_level, self.RF_state = self.device.get_pow_level()
            self.response.emit("tabs/VNA", {"method": "on_power_acquired",
                                            "kwargs": {"power_level": self.power_level, "RF_on": self.RF_state}})
        except Exception as e:
                log.error(str(e))

    def get_vna_traces(self):
        try:
            trace_list = self.device.get_trace_list()
            self.current_trace = self.device.get_trace_sel()

            self.response.emit("tabs/VNA", {"method": "on_trace_list_acquired",
                                        "kwargs": {"trace_list": trace_list, "current_trace": self.current_trace}})
        except Exception as e:
                log.error(str(e))

    def get_vna_freq_N(self):
        try:
            self.f_start_Hz = self.device.get_freq_start()
            self.f_stop_Hz = self.device.get_freq_stop()
            self.N = self.device.get_num_points()
            # wysłanie sygnału do GUI
            #log.debug(f"get_vna_freq_N: dev_label {self.dev_label}, owner {self.owner}")
            self.response.emit("tabs/VNA", {"method": "on_freq_N_acquired",
                                            "kwargs": {"f_start_Hz": self.f_start_Hz, "f_stop_Hz": self.f_stop_Hz,
                                                       "N": self.N}})

        except Exception as e:
            log.error(str(e))

    @Slot()
    def get_config(self):
        try:
            self.device.cls_vna()
            self.f_start_Hz = self.device.get_freq_start()
            self.f_stop_Hz = self.device.get_freq_stop()
            self.N = self.device.get_num_points()
            self.current_trace = self.device.get_trace_sel()
            # wysłanie sygnału do GUI
            #log.debug(f"get_vna_freq_N: dev_label {self.dev_label}, owner {self.owner}")
            self.response.emit("tabs/VNA", {"method": "on_freq_N_acquired",
                                            "kwargs": {"f_start_Hz": self.f_start_Hz, "f_stop_Hz": self.f_stop_Hz,
                                                       "N": self.N}})

            if self.owner != "tabs/VNA":
                # wyślij dane do ownera
                log.debug(f"get_config: dev_label {self.dev_label} -> {self.owner} _on_get_config")
                self.response.emit(self.owner, {"method": "_on_get_config",
                                                "kwargs":{"dev_label": self.dev_label,
                                                          "kwargs": {"method" : "_on_get_config",
                                                                     "kwargs": {
                                                                         "dev_label" : self.dev_label,
                                                                         "dev_config" : {
                                                                             "pwr" : self.power_level,
                                                                             "f_start" : self.f_start_Hz,
                                                                             "f_stop" : self.f_stop_Hz,
                                                                             "N" : self.N,
                                                                             "s_param" : self.current_trace}}}}})
        except Exception as e:
            log.error(str(e))

    # --- slot sprzątający ---
    @Slot()
    def stop(self):
        """Zatrzymaj wszystkie akcje workera"""
        try:
            self.switch_on_off(False)
        except Exception:
            pass
        log.debug("VnaWorker: shutdown done")