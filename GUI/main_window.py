
import os
import logging
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QTextCharFormat, QColor, QTextCursor, QIcon
from PySide6.QtCore import QThread, QObject
from .ui_main_window import Ui_MainWindow
from .widgets.connections_tab.connections import Connections
from .widgets.measurement_tab.meas_setup import MeasSetup
from .widgets.measurement_tab.setups.FF_az.FF_az import FF_az
from .widgets.measurement_tab.setups.FF_el.FF_el import FF_el
from .widgets.measurement_tab.setups.PNF.PNF import PNF
from .widgets.measurement_tab.setups.Calib.Calib import Calib

from .widgets.vna_tab.vna import Vna
from .widgets.positioners_tab.positioners import Positioner
from .widgets.micrometer_tab.micrometer import Micrometer
from .widgets.camera_tab.camera import Camera # import mojego wigetu do zakładki kamery
from .widgets.data_processing_tab.data_processing import DataProcessing
from .widgets.robot_control_tab.robot_control import RobotControl
from src.Workers.mediator import Mediator
from src.Workers.vna_worker import VnaWorker
from src.Workers.motor_worker import MotorWorker
from src.Workers.camera_worker import CameraWorker # import workera kamery
from src.Workers.rarm_worker import RarmWorker
from src.Workers.micro_worker import MicroWorker
from src.Workers.meas_worker import MeasWorker
from src.Workers.data_processing_worker import DataProcessingWorker
from src.Utils.logging_config import Handler

import threading

LEVEL_BOXES = [
    ("log_debug_box",    logging.DEBUG),
    ("log_info_box",     logging.INFO),
    ("log_warning_box",  logging.WARNING),
    ("log_error_box",    logging.ERROR),
    ("log_critical_box", logging.CRITICAL),
]

image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../GUI/images"))

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        app_icon = os.path.join(image_dir, "app_icon.png").replace("\\", "/")
        self.setWindowIcon(QIcon(app_icon))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._log_records = []
        self._log_updating_checks = False
        logger = self.setup_logger()
        self._threads: dict[str, QThread] = {}
        self._workers: dict[str, QObject] = {}

        #self.load_widgets()

    #def load_widgets(self):
        # --- MEDIATOR ---
        self.mediator_thread = QThread()
        self.mediator_thread.setObjectName("mediator")
        self.mediator = Mediator(self._threads, self._workers)
        self.mediator.moveToThread(self.mediator_thread)
        self.mediator_thread.start()
        self._threads["mediator"] = self.mediator_thread
        self._workers["mediator"] = self.mediator
        
        # --- MEASURE ---
        self.meas_thread = QThread()
        self.meas_thread.setObjectName("MEAS")
        self.meas_worker = MeasWorker("MEAS", self._workers)
        self.meas_worker.moveToThread(self.meas_thread)
        self.meas_thread.start()
        self._threads["MEAS"] = self.meas_thread
        self._workers["MEAS"] = self.meas_worker

        # --- VNA thread & worker---
        self.vna_thread = QThread()
        self.vna_thread.setObjectName("VNA")
        self.vna_worker = VnaWorker("VNA")
        self.vna_worker.moveToThread(self.vna_thread)
        self.vna_thread.start()
        self._threads["VNA"] = self.vna_thread
        self._workers["VNA"] = self.vna_worker

        # --- Motor Azimuth thread & worker---
        self.motor_thread = QThread()
        self.motor_thread.setObjectName("TIC_AZ")
        self.motor_worker = MotorWorker("TIC_AZ")
        self.motor_worker.moveToThread(self.motor_thread)
        self.motor_thread.start()
        self._threads["TIC_AZ"] = self.motor_thread
        self._workers["TIC_AZ"] = self.motor_worker

        # --- Motor Elevation thread & worker---
        self.m_elev_thread = QThread()
        self.m_elev_thread.setObjectName("TIC_EL")
        self.m_elev_worker = MotorWorker("TIC_EL")
        self.m_elev_worker.moveToThread(self.motor_thread)
        self.m_elev_thread.start()
        self._threads["TIC_EL"] = self.m_elev_thread
        self._workers["TIC_EL"] = self.m_elev_worker

        # --- ROBOT ARM thread & worker---
        self.rarm_thread = QThread()
        self.rarm_thread.setObjectName("RARM")
        self.rarm_worker = RarmWorker("RARM")
        self.rarm_worker.moveToThread(self.rarm_thread)
        self.rarm_thread.start()
        self._threads["RARM"] = self.rarm_thread
        self._workers["RARM"] = self.rarm_worker

        # --- Micrometer thread & worker---
        self.micro_thread = QThread()
        self.micro_thread.setObjectName("MICRO")
        self.micro_worker = MicroWorker("MICRO")
        self.micro_worker.moveToThread(self.micro_thread)
        self.micro_thread.start()
        self._threads["MICRO"] = self.micro_thread
        self._workers["MICRO"] = self.micro_worker

        self.camera_thread = QThread()
        self.camera_thread.setObjectName("CAM")
        self.camera_worker = CameraWorker("CAM")
        self.camera_worker.moveToThread(self.camera_thread)
        self.camera_thread.start()
        self._threads["CAM"] = self.camera_thread
        self._workers["CAM"] = self.camera_worker
        # --- Data Processing thread & worker---
        self.data_proc_thread = QThread()
        self.data_proc_thread.setObjectName("DATA_PROC")
        self.data_proc_worker = DataProcessingWorker("DATA_PROC")
        self.data_proc_worker.moveToThread(self.data_proc_thread)
        self.data_proc_thread.start()
        self._threads["DATA_PROC"] = self.data_proc_thread
        self._workers["DATA_PROC"] = self.data_proc_worker

        # --- Camera thread & worker---


        # widgety - obiekty
        self.connections = Connections()
        self.meas_setup = None
        self.FF_az = FF_az(self._workers, self._threads, self.mediator, self.meas_setup)
        self.FF_el = FF_el(self._workers, self._threads, self.mediator, self.meas_setup)
        self.PNF = PNF(self._workers, self._threads, self.mediator, self.meas_setup)
        self.Calib = Calib(self._workers, self._threads, self.mediator, self.meas_setup)
        self.meas_setup = MeasSetup(self._workers, self._threads, self.mediator, self)
        self.FF_az.parent = self.meas_setup
        self.FF_az.parent = self.meas_setup
        self.PNF.parent = self.meas_setup
        self.Calib.parent = self.meas_setup
        self.vna = Vna(self.vna_worker)
        self.motor = Positioner(self.motor_worker)
        self.rarm = RobotControl(self.rarm_worker)
        self.micro = Micrometer()
        self.camera = Camera() # tworze instancje wigetu
        self.data_processing = DataProcessing(self.data_proc_worker)

        # widgety - zakładki
        self.ui.main_tabs.clear()
        self.ui.main_tabs.addTab(self.connections, "Connections")
        self.ui.main_tabs.addTab(self.meas_setup, "Measurement")
        self.ui.main_tabs.addTab(self.vna, "VNA")
        self.ui.main_tabs.addTab(self.motor, "Positioners")
        self.ui.main_tabs.addTab(self.rarm, "Robot")
        self.ui.main_tabs.addTab(self.micro, "Micrometer")
        self.ui.main_tabs.addTab(self.data_processing, "Data Processing")
        self.ui.main_tabs.addTab(self.camera, "Camera") #dodaje zakładkę

        # --- Connections signal listeners ---
        self.connections.connectRequested.connect(self.mediator.connect)
        self.connections.disconnectRequested.connect(self.mediator.disconnect)

        # --- MeasSetup tab signal listeners ---
        self.meas_setup.controlRequest.connect(self.mediator.request)
        self.meas_setup.controlRelease.connect(self.mediator.release)
        self.meas_setup.command.connect(self.meas_worker.command_interp)

        # --- MeasSetup subtab signal listeners ---
        self.FF_az.controlRelease.connect(self.mediator.release)
        self.FF_az.command.connect(self.mediator.command_interp)
        self.FF_az.command.connect(self.meas_worker.command_interp)

        self.PNF.command.connect(self.meas_worker.command_interp)
        
        self.Calib.controlRelease.connect(self.mediator.release)
        self.Calib.command.connect(self.mediator.command_interp)
        self.Calib.command.connect(self.meas_worker.command_interp)

        # --- Robotic Arm tab signal listeners ---
        self.rarm.controlRequest.connect(self.mediator.request)
        self.rarm.preemptDone.connect(self.mediator._on_preempt)
        self.rarm.command.connect(self.rarm_worker.command_interp)

        # --- VNA tab signal listeners ---
        self.vna.controlRequest.connect(self.mediator.request)
        self.vna.preemptDone.connect(self.mediator._on_preempt)
        self.vna.command.connect(self.vna_worker.command_interp)

        # --- Motor tab signal listeners ---
        self.motor.controlRequest.connect(self.mediator.request)
        self.motor.preemptDone.connect(self.mediator._on_preempt)
        self.motor.command.connect(self.motor_worker.command_interp)

        # --- Micro tab signal listeners ---
        self.micro.controlRequest.connect(self.mediator.request)
        self.micro.preemptDone.connect(self.mediator._on_preempt)
        self.micro.command.connect(self.micro_worker.command_interp)

        # --- Camera tab signal listeners ---
        self.camera.controlRequest.connect(self.mediator.request)
        self.camera.preemptDone.connect(self.mediator._on_preempt)
        self.camera.command.connect(self.camera_worker.command_interp)
        # --- Data Processing tab signal listeners ---
        self.data_processing.command.connect(self.data_proc_worker.command_interp)

        # --- meas_worker signal listeners ---
        self.meas_worker.response.connect(self.meas_setup.response_interp)
        self.meas_worker.response.connect(self.PNF.response_interp)
        self.meas_worker.response.connect(self.FF_az.response_interp)
        self.meas_worker.response.connect(self.Calib.response_interp)

        self.meas_worker.command.connect(self.vna_worker.command_interp)
        self.meas_worker.command.connect(self.rarm_worker.command_interp)
        self.meas_worker.command.connect(self.motor_worker.command_interp)
        self.meas_worker.command.connect(self.camera_worker.command_interp)
        self.meas_worker.command.connect(self.micro_worker.command_interp)

        # --- vna_worker signal listeners ---
        self.vna_worker.ready.connect(self.mediator._handle_connect_resp)
        self.vna_worker.shutdown.connect(self.mediator._handle_disconnect_resp)
        self.vna_worker.response.connect(self.vna.response_interp)
        self.vna_worker.response.connect(self.meas_worker.response_interp)

        # --- motor_worker signal listeners ---
        self.motor_worker.ready.connect(self.mediator._handle_connect_resp)
        self.motor_worker.shutdown.connect(self.mediator._handle_disconnect_resp)
        self.motor_worker.response.connect(self.motor.response_interp)
        self.motor_worker.response.connect(self.meas_worker.response_interp)

        # --- m_elev_worker signal listeners ---
        self.m_elev_worker.ready.connect(self.mediator._handle_connect_resp)
        self.m_elev_worker.shutdown.connect(self.mediator._handle_disconnect_resp)
        self.m_elev_worker.response.connect(self.motor.response_interp)

        # --- ROBOT ARM worker signal listeners ---
        self.rarm_worker.ready.connect(self.mediator._handle_connect_resp)
        self.rarm_worker.shutdown.connect(self.mediator._handle_disconnect_resp)
        self.rarm_worker.response.connect(self.rarm.response_interp)
        self.rarm_worker.response.connect(self.meas_worker.response_interp)

        # --- micro_worker signal listeners ---
        self.micro_worker.ready.connect(self.mediator._handle_connect_resp)
        self.micro_worker.shutdown.connect(self.mediator._handle_disconnect_resp)
        self.micro_worker.response.connect(self.micro.response_interp)
        self.micro_worker.response.connect(self.meas_worker.response_interp)

        # --- camera_worker signal listeners ---
        self.camera_worker.ready.connect(self.mediator._handle_connect_resp)
        self.camera_worker.shutdown.connect(self.mediator._handle_disconnect_resp)
        self.camera_worker.response.connect(self.camera.response_interp)
        self.camera_worker.response.connect(self.meas_worker.response_interp)

        # --- data_processing_worker signal listeners ---
        self.data_proc_worker.response.connect(self.data_processing.response_interp)

        # --- Mediator signal listeners ---
        self.mediator.deviceConnect.connect(self.vna_worker.connect)
        self.mediator.deviceConnect.connect(self.motor_worker.connect)
        self.mediator.deviceConnect.connect(self.m_elev_worker.connect)
        self.mediator.deviceConnect.connect(self.rarm_worker.connect)
        self.mediator.deviceConnect.connect(self.micro_worker.connect)
        self.mediator.deviceConnect.connect(self.camera_worker.connect) # połączenie workera z mediatorem do połączenia

        self.mediator.deviceDisconnect.connect(self.vna_worker.disconnect)
        self.mediator.deviceDisconnect.connect(self.motor_worker.disconnect)
        self.mediator.deviceDisconnect.connect(self.m_elev_worker.disconnect)
        self.mediator.deviceDisconnect.connect(self.rarm_worker.disconnect)
        self.mediator.deviceDisconnect.connect(self.micro_worker.disconnect)
        self.mediator.deviceDisconnect.connect(self.camera_worker.disconnect) # połączenie workera z mediatorem do odłączenia

        self.mediator.preempt.connect(self.vna._on_preempt)
        self.mediator.preempt.connect(self.motor._on_preempt)
        self.mediator.preempt.connect(self.micro._on_preempt)
        self.mediator.preempt.connect(self.rarm._on_preempt)
        self.mediator.preempt.connect(self.camera._on_preempt)

        self.mediator.controlGranted.connect(self.vna._on_granted)
        self.mediator.controlGranted.connect(self.motor._on_granted)
        self.mediator.controlGranted.connect(self.rarm._on_granted)
        self.mediator.controlGranted.connect(self.micro._on_granted)
        self.mediator.controlGranted.connect(self.meas_setup._on_granted)
        self.mediator.controlGranted.connect(self.camera._on_granted)

        self.mediator.controlDenied.connect(self.vna._on_denied)
        self.mediator.controlDenied.connect(self.motor._on_denied)
        self.mediator.controlDenied.connect(self.rarm._on_denied)
        self.mediator.controlDenied.connect(self.micro._on_denied)
        self.mediator.controlDenied.connect(self.camera._on_denied)
        self.mediator.controlRevoked.connect(self.meas_setup._on_revoked)

        self.mediator.deviceConnectResp.connect(self.meas_setup.check_mode_ready)
        self.mediator.deviceConnectResp.connect(self.connections.handle_connect_resp)
        self.mediator.deviceDisconnectResp.connect(self.connections.handle_disconnect_resp)

        # urządzenia
        self.devices = self.connections.devices

        background_img = os.path.join(image_dir, "microamp_white.png").replace("\\", "/")
        self.ui.main_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: #DCDCDC;
                background-image: url({background_img});
                background-repeat: no-repeat;
                background-position: center;
            }}
        """)
        self.showMaximized()

    def setup_logger(self):
        handler = Handler(self)
        handler.new_record.connect(self.handle_log_record)
        palette = self.ui.log_text_box.palette()
        self.ui.log_text_box.setPalette(palette)

        self.ui.log_all_box.toggled.connect(self.on_all_toggled)
        for obj_name, _ in LEVEL_BOXES:
            getattr(self.ui, obj_name).toggled.connect(self.on_level_toggled)
        self.ui.log_clear_btn.clicked.connect(self.clear_logs)

        logger = logging.getLogger("GUI")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return logger

    def handle_log_record(self, message: str, level: int):
        self._log_records.append((message, level))
        if self._is_level_enabled(level):
            self._append_line(message, level)



    def _append_line(self, message: str, level: int):
        color = {
            logging.DEBUG: QColor("black"),
            logging.INFO: QColor("blue"),
            logging.WARNING: QColor("#CC6600"),
            logging.ERROR: QColor("red"),
            logging.CRITICAL: QColor("darkred"),
        }.get(level, QColor("black"))

        cursor = self.ui.log_text_box.textCursor()
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(message + '\n', fmt)
        self.ui.log_text_box.setTextCursor(cursor)


    def _enabled_levels(self) -> set[int]:
        levels = set()
        for obj_name, lvl in LEVEL_BOXES:
            if getattr(self.ui, obj_name).isChecked():
                levels.add(lvl)
        return levels
    
    def _is_level_enabled(self, levelno: int) -> bool:
        return levelno in self._enabled_levels()
    
    def on_all_toggled(self, checked: bool):
        if self._log_updating_checks:
            return
        self._log_updating_checks = True
        try:
            for obj_name, _ in LEVEL_BOXES:
                getattr(self.ui, obj_name).setChecked(checked)
        finally:
            self._log_updating_checks = False
        self._refresh_view()
    
    def clear_logs(self):
        self.ui.log_text_box.clear()
        self._log_records.clear()
    
    def on_level_toggled(self, _checked: bool):
        if self._log_updating_checks:
            return
        all_on = all(getattr(self.ui, obj_name).isChecked() for obj_name, _ in LEVEL_BOXES)
        self._log_updating_checks = True
        try:
            self.ui.log_all_box.setChecked(all_on)
        finally:
            self._log_updating_checks = False
        self._refresh_view()

    def _refresh_view(self):
        self.ui.log_text_box.clear()
        enabled = self._enabled_levels()
        for msg, lvl in self._log_records:
            if lvl in enabled:
                self._append_line(msg, lvl)

    def apply_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(__file__), "styles", "Combinear.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"[Style] style.qss not found at: {qss_path}")
            
    def closeEvent(self, event):
        self.connections.save_table_state()
        self.rarm.save_rarm_params()
        """Sprzątanie przy zamykaniu aplikacji"""
        if self._workers["RARM"].device is not None:
            self._workers["RARM"].device.shutdown()
        for thread in self._threads.values():
            thread.quit()
            thread.wait()
        super().closeEvent(event)
