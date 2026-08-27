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
from PySide6.QtGui import QImage, QPixmap, Qt # Dodaj te importy!
from PySide6.QtWidgets import QWidget, QMessageBox, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtCore import Slot, Signal, QObject
from .ui_camera import Ui_camera
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, DELAY_MAP, DELAY_MAP, Priority, State
import cv2

import logging
log = logging.getLogger("GUI")

class Camera(QWidget):
    controlRequest = Signal(str, str, int)  # passing dev_label, client_id, priority level
    preemptDone = Signal(str, str, str)  # passing dev_label, client_id, token
    command = Signal(str, str, dict)  # passing dev_label, client_id, dict of method + arguments

    def __init__(self):
        super().__init__()
        self.ui = Ui_camera()
        self.ui.setupUi(self)
        self.dev_label = "CAM"
        self.client_id = "tabs/CAM"
        self.token = None
        self._have_control = False  # flaga kontroli nad urządzeniem
        self.measuring = False

        self.preempt = False  # flaga wywłaszczania
        self.ui.send_dim_btn.setEnabled(False)
        # maszyna stanów
        self.param_pending = {
            "position": False
        }

        self.ui.get_control_btn.clicked.connect(self.request_control) # przycisk do przejęcia kontroli nad kamerą zakładki z kamerą

        # przyciski
        #self.ui.startButton.setText("Start")
        self.ui.start_btn.setEnabled(False)
        self.ui.start_btn.clicked.connect(self.toggle_on_off)

        self.ui.fps_comboBox.currentTextChanged.connect(self.on_fps_changed)

        self.ui.lineEdit_w.textChanged.connect(self.validate_dimensions)
        self.ui.lineEdit_h.textChanged.connect(self.validate_dimensions)

        self.ui.send_dim_btn.clicked.connect(self.send_dimensions_to_worker)

    @Slot()
    def request_control(self): # funkcja przejmująca kontrolę
        log.debug(f"request_control: dev_label {self.dev_label}, client_id {self.client_id}")
        self.controlRequest.emit(self.dev_label, self.client_id, Priority.Manual)

    @Slot(str, str, str)
    def _on_granted(self, dev_label:str, client_id:str, token:str):
        if self.dev_label != dev_label:
            return
        if self.client_id != client_id:
            return
        self._have_control = True
        self.ui.start_btn.setEnabled(True)
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
            self.ui.start_btn.setText("Stop")
        else:
            self.ui.start_btn.setText("Start")
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
            #self.set_param()
            #log.debug(f"dev_label: {self.dev_label} client_id {self.client_id}")
            self.command.emit(self.dev_label, self.client_id,{"method" : "switch_on_off", "kwargs" : {"on": True}})
        else:
            # Stop
            self.command.emit(self.dev_label, self.client_id,{"method" : "switch_on_off", "kwargs" : {"on": False}})

    def on_fps_changed(self, text):
        try:
            fps_val = int(text)
            self.command.emit(self.dev_label, self.client_id, {
                "method": "set_fps",
                "kwargs": {"fps": fps_val}
            })
        except ValueError:
            pass

    @Slot(object)  # Dodaj dekorator Slot
    def update_video_feed(self, frame):
        if frame is None: return

        try:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            qt_image = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(qt_image)

            # Pobieramy aktualny rozmiar labela (który teraz jest duży dzięki layoutom)
            label_size = self.ui.label.size()

            # Skalujemy do rozmiaru labela zachowując proporcje
            scaled_pixmap = pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.FastTransformation  # Przy 1080p FastTransformation jest kluczowe dla płynności
            )

            self.ui.label.setPixmap(scaled_pixmap)
            # Wyśrodkowanie obrazu w labelu
            self.ui.label.setAlignment(Qt.AlignCenter)

        except Exception as e:
            log.error(f"Error: {e}")

    def validate_dimensions(self):
        """Sprawdza stan obu pól i aktywuje przycisk tylko gdy oba są poprawne."""
        w_text = self.ui.lineEdit_w.text().strip()
        h_text = self.ui.lineEdit_h.text().strip()

        # 1. Jeśli którekolwiek pole jest puste, wyłącz przycisk i wyjdź
        if not w_text or not h_text:
            self.ui.send_dim_btn.setEnabled(False)
            return

        try:
            # 2. Próba konwersji (zamieniamy przecinki na kropki dla bezpieczeństwa)
            w = float(w_text.replace(',', '.'))
            h = float(h_text.replace(',', '.'))

            # 3. Sprawdzenie czy wymiary są sensowne (większe od 0)
            is_valid = (w > 0 and h > 0)
        except ValueError:
            # Jeśli tekst nie jest liczbą (np. ktoś wpisał "abc")
            is_valid = False

        self.ui.send_dim_btn.setEnabled(is_valid)

    def send_dimensions_to_worker(self):
        """Wywoływane tylko po kliknięciu aktywnego przycisku."""
        w = float(self.ui.lineEdit_w.text().replace(',', '.'))
        h = float(self.ui.lineEdit_h.text().replace(',', '.'))

        self.command.emit(self.dev_label, self.client_id, {
            "method": "set_target_dimensions",
            "kwargs": {"w": w, "h": h}
        })
        log.info(f"Wysłano nowe wymiary wzorca: {w} x {h} mm")