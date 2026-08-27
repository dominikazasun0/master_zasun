
import threading
import logging
from enum import IntEnum
from typing import Dict, Any
from PySide6.QtCore import Qt, QSize, QThread, QEventLoop, QTimer, Slot, QObject, Signal
#
from src.Drivers.Camera_driver.CameraConfig import CameraConfig
from src.Drivers.Camera_driver.Preprocessor import Preprocessor
from src.Drivers.Camera_driver.SquareDetector import SquareDetector
from src.Drivers.Camera_driver.PoseEstimator import PoseEstimator
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, Priority, State
from src.Workers.DEV_worker import DEV_Worker, WorkerState
import cv2
from src.Drivers.Camera_driver.Camera_Driver import Camera_driver


log = logging.getLogger("GUI")

class CameraWorker(DEV_Worker):

    ready = Signal(str, bool)  # passing dev_label, response
    shutdown = Signal(str, bool)  # passing dev_label, response
    response = Signal(str, dict)  # To jest moja odpowiedź
    progress = Signal(str)  # passing message
    stateChanged = Signal(int)  # passing new state number
    faultOccurred = Signal(str, str)  # passing dev_label, message
    heartbeat = Signal(str)  # passing dev_label


    def __init__(self, dev_label: str):
        super().__init__(dev_label)

        self.target_w = 55.0  # mm (dostosuj do swojego wzorca)
        self.target_h = 55.0  # mm
        self.delay_between_use = 30  # ms (ok. 30 klatek na sekundę)



    def set_device(self, dev_model: str, dev_address: str):
        self.model = "EMEET S600"
        self.device = Camera_driver(dev_address)
        # Tutaj dodatkowo tworzę obiekty które są potrzene do przetważania obrazu
        config = CameraConfig("src/Utils/config_files/config_camera.json")
        self.estimator = PoseEstimator(config)
        self.preprocessor = Preprocessor(config)
        self.detector = SquareDetector()


    @Slot(str, str, str)
    def connect(self, dev_label: str, dev_model: str, dev_address: str):
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
    def disconnect(self, dev_label: str):
        if self.dev_label != dev_label:
            return
        try:
            self.stop()
            self.device.release()
            log.debug(f"{dev_label} model {self.model} disconnected.")
            self.shutdown.emit(self.dev_label, True)
        except Exception as e:
            log.error(f"Disconnect failed: {e}")
            self.shutdown.emit(self.dev_label, False)


    def configure(self, refresh_time):
        """Ustawia odświeżanie odczytu."""
        self.refresh_time = refresh_time
        status = self.device.is_ready()
        log.debug(f"EMEET S600 ready: {status}")


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
            log.debug(f"[CAMworker] NEXT IN SEQU, state -> {self.state}")
            return

        self.state = WorkerState.GET_DATA

        if self.owner == "tabs/CAM":    # If it is a full run
            QTimer.singleShot(self.delay_between_use, lambda: self._do_next_event())
        else: # If it is a measurement setup
            #self.response.emit(self.owner, {"method": "_on_update", "kwargs": {"dev_label": self.dev_label, "dev_data": {"method": "on_data_acquired", "kwargs": {"pos": self.data}}}})
            self.response.emit(self.owner, {"method": "_on_event_done", "kwargs": {"dev_label": self.dev_label, "result": True}})

    @Slot(str)
    def _do_next_event(self):
        if self.device is None:
            log.error("EMEET S600 is not set")
            return
        #log.debug(f"[VNAWorker] DO NEXT EVENT, {self.state}")
        try:
            match self.state:
                case WorkerState.GET_DATA:
                    self.my_frame = self._process_single_frame() # pobranie klatki
                    self

                    self._finished_step() # wysłanie klati do gui

                case WorkerState.NEXT:
                    self._next_in_sequ()

                case WorkerState.FINISHED:
                    self.state = WorkerState.IDLE
                    self.owner = None

        except Exception as e:
            log.error("MICRO read error: %s", e)
            if self.owner == "tabs/CAM":
                self.switch_on_off(False)
            else:
                self.response.emit(self.owner, {"method": "_on_event_done", "kwargs": {"dev_label" : self.dev_label,"result" : False}})

    def _finished_step(self):

        # pomiar zakończony
        self.response.emit("tabs/CAM", {
            "method": "update_video_feed",
            "kwargs": {"frame": self.my_frame}  # Klucz musi być identyczny z nazwą argumentu w GUI!
        })
        #log.debug("wysłałam")
        self.state = WorkerState.NEXT
        QTimer.singleShot(0, self._do_next_event)


    @Slot() # pobranie pojedyńczyej klatki z kamerki
    def _process_single_frame(self):
        frame = self.device.get_frame()

        return frame

    @Slot(int) # zmiana fps -> aktualizacja z gui
    def set_fps(self, fps: int):
        if fps <= 0: fps = 1
        self.delay_between_use = int(1000 / fps)
        log.info(f"[CAM] FPS changed to {fps} (delay: {self.delay_between_use}ms)")

    @Slot(float, float) # zmiana wymiarów -> aktualizacja GUI
    def set_target_dimensions(self, w: float, h: float):
        self.target_w = w
        self.target_h = h
        log.debug(f"[CAM Worker] Nowe wymiary docelowe: {w}x{h}")

    def _send_frame_to_meas(self):
        # 1. Pobranie i przetwarzanie klatki
        current_frame = self._process_single_frame()
        if current_frame is None:
            return

        mask = self.preprocessor.get_mask(current_frame)
        result = self.detector.find_square(mask, self.target_w / self.target_h)
        
        display_frame = current_frame.copy()
        
        # Inicjalizacja danych domyślnych
        rvec, tvec, distance = None, None, 0.0

        if result is not None:
            corners, simplified_cnt = result
            cv2.drawContours(display_frame, [simplified_cnt], -1, (0, 0, 255), 3)

            rvec, tvec = self.estimator.solve(corners, self.target_w, self.target_h)
            distance = self.estimator.get_distance(tvec)
            
            # Opcjonalnie: rysowanie osi na display_frame tutaj
        
        # 2. Wysyłka zbiorcza do MeasWorker (przez self.owner)
        # Pakujemy wszystko w jeden słownik kwargs
        self.response.emit(self.owner, {
            "method": "on_received_camera_data",
            "kwargs": {
                "frame": display_frame, # Wysyłamy klatkę z narysowanym konturem
                "rvec": rvec,
                "tvec": tvec,
                "distance": float(distance)
            }
        })

        # 3. Reset właściciela na podgląd ogólny
        self.owner = "tabs/CAM"
    

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

    # --- slot sprzątający ---
    @Slot()
    def stop(self):
        """Zatrzymaj wszystkie akcje workera"""
        try:
            self.switch_on_off(False)
            if self.device:
                self.device.release()
        except Exception:
            pass
        log.debug("MotorWorker: shutdown done")

