import cv2
import numpy as np
from typing import Dict, Any
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, Slot, Signal, QObject
import logging
from .ui_calib import Ui_Calib

log = logging.getLogger("GUI")

class Calib(QWidget):
    # Sygnały wymagane przez architekturę
    controlRequest = Signal(str, str, int)
    controlRelease = Signal(str, str, str)
    command = Signal(str, str, dict)

    def __init__(self, workers: dict, threads: dict, mediator: QObject, parent=None):
        super().__init__(parent)
        self.ui = Ui_Calib()
        self.ui.setupUi(self)

        self.parent = parent
        self.client_id = "tabs/Calib"  
        self.dev_label = "Calib"    

        self.ui.pose_est_btn.clicked.connect(self._on_pose_est_btn_pressed)
        self.ui.move_btn.clicked.connect(self._on_move_btn_pressed)
        self.ui.new_coordinate_btn.clicked.connect(self._on_new_coordinate_btn_pressed)
        self.ui.start_verify_btn.clicked.connect(self._on_start_verify_btn_pressed)
        self.ui.antenna_btn.clicked.connect(self._on_antenna_btn_pressed)


    @Slot(str, dict)
    def response_interp(self, client_id: str, response: dict):
        if client_id != self.client_id:
            return

        method = response.get("method")
        kwargs = response.get("kwargs", {})

        fn = getattr(self, method, None)

        if callable(fn):
            fn(**kwargs)
        else:
            log.error(f"Widget has no handler: {method}")

    def _update_video_feed(self, frame=None, distance=None, **kwargs):
        if frame is not None:
            self.update_video_feed(frame)
        if distance is not None:
            self.ui.distance_label.setText(f"{distance:.2f} mm")

    def update_current_pose(self, pose=None, **kwargs):
        if pose is not None:
            self.ui.old_x.setText(str(pose[0]))
            self.ui.old_y.setText(str(pose[1]))
            self.ui.old_z.setText(str(pose[2]))
            self.ui.old_roll.setText(str(pose[3]))
            self.ui.old_pitch.setText(str(pose[4]))
            self.ui.old_yaw.setText(str(pose[5]))

    def update_new_pose(self, all_poses=None, **kwargs):

        if not isinstance(all_poses, list) or len(all_poses) < 4:
            return
        ui_groups = [
            [self.ui.p0_x, self.ui.p0_y, self.ui.p0_z, self.ui.p0_roll, self.ui.p0_pitch, self.ui.p0_yaw],      # index 0
            [self.ui.px_x, self.ui.px_y, self.ui.px_z, self.ui.px_roll, self.ui.px_pitch, self.ui.px_yaw],      # index 1
            [self.ui.pxy_x, self.ui.pxy_y, self.ui.pxy_z, self.ui.pxy_roll, self.ui.pxy_pitch, self.ui.pxy_yaw], # index 2
            [self.ui.center_x, self.ui.center_y, self.ui.center_z, self.ui.center_roll, self.ui.center_pitch, self.ui.center_yaw] # index 3
        ]
        for i, labels in enumerate(ui_groups):
            coords = all_poses[i]
            if coords and len(coords) == 6:
                for value, label in zip(coords, labels):
                    label.setText(f"{value:.2f}")

    def on_update_current_coordinate(self, new_coordinate):
        if new_coordinate is not None:
            self.ui.new_cs_x.setText(str(new_coordinate[0]))
            self.ui.new_cs_y.setText(str(new_coordinate[1]))
            self.ui.new_cs_z.setText(str(new_coordinate[2]))
            self.ui.new_cs_roll.setText(str(new_coordinate[3]))
            self.ui.new_cs_pitch.setText(str(new_coordinate[4]))
            self.ui.new_cs_yaw.setText(str(new_coordinate[5]))

    def update_video_feed(self, frame):
       
        if frame is None:
            return
        try:
            # Standardowa konwersja OpenCV (BGR) -> Qt (RGB)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            
            # Skalowanie do rozmiaru labela w GUI
            self.ui.video_label.setPixmap(pixmap.scaled(
                self.ui.video_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
        except Exception as e:
            log.error(f"Błąd wyświetlania klatki w Calib: {e}")    

    #git
    def _on_pose_est_btn_pressed(self):
        
        self.command.emit("MEAS", self.dev_label, {
            "method": "on_start_measure",
            "kwargs": {}
            })
    
    def _on_move_btn_pressed(self):
        self.command.emit("MEAS", self.dev_label, {
            "method": "on_change_status_move",
            "kwargs": {}
            })

    def _on_new_coordinate_btn_pressed(self):
        self.command.emit("MEAS", self.dev_label, {
            "method": "on_accept_new_cs",
            "kwargs": {}
        })

    def _on_start_verify_btn_pressed(self):
        self.command.emit("MEAS", self.dev_label, {
            "method": "on_change_status_veryfication",
            "kwargs": {}
        })
    def _on_antenna_btn_pressed(self):
        self.command.emit("MEAS", self.dev_label, {
            "method": "on_change_tcp_probe",
            "kwargs": {}
        })