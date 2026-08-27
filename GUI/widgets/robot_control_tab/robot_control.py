__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"


import logging
import numpy as np
from typing import Dict, Any
from PySide6.QtWidgets import QWidget, QButtonGroup, QToolButton, QFileDialog, QTableWidgetItem,QMessageBox
from PySide6.QtCore import Qt, QObject, Signal, QThread, Slot, QRegularExpression, QSettings
from PySide6.QtGui import QRegularExpressionValidator, QBrush, QColor
from .ui_robot_control import Ui_robot_control
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, Priority, State


log = logging.getLogger("GUI")

state_map = {
    1: "In Motion",
    2: "Sleeping",
    3: "Suspended",
    4: "Stopping"}

class RobotControl(QWidget):

    controlRequest = Signal(str, str, int) # passing dev_label, client_id, priority level
    preemptDone = Signal(str, str, str)    # passing dev_label, client_id, token
    command = Signal(str, str, dict)       # passing dev_label, client_id, dict of method + arguments

    def __init__(self, worker):
        super().__init__()
        self.ui = Ui_robot_control()
        self.ui.setupUi(self)
        self.worker = worker
        self.dev_label = "RARM"
        self.client_id = "tabs/RARM"
        self.token = None
        self._have_control = False
        self.moving = False
        self.preempt = False
        self.default_pos = {"x" : 500,
                            "y" : 0,
                            "z" : 600,
                            "roll" : -90,
                            "pitch" : -90,
                            "yaw" : -90}

        self.restore_rarm_params()
        self.mov_matrix = None
        self.current_index = None
        self.ui.lamda.setReadOnly(True)
        self.ui.show_matrix_btn.setEnabled(False)
        regex = QRegularExpression(r"^\d*\.?\d*([eE]\+?\d*)?$")
        validator = QRegularExpressionValidator(regex, self.ui.lamda)
        self.ui.lamda.setValidator(validator)
        self.ui.freq.editingFinished.connect(self.update_lamda)
        self.ui.calc_x_btn.toggled.connect(self.delta_x_radio)
        self.ui.calc_x_combo.currentIndexChanged.connect(self.delta_x_combo)
        self.ui.calc_y_btn.toggled.connect(self.delta_y_radio)
        self.ui.calc_y_combo.currentIndexChanged.connect(self.delta_y_combo)
        self.ui.dims_calc_btn.clicked.connect(self.calc_dims)
        self.ui.show_matrix_btn.clicked.connect(self.fill_matrix)
        self.ui.reqCtrl.clicked.connect(self.request_control)
        self.ui.load_matrix_btn.clicked.connect(self.set_param)
        self.ui.get_state_btn.clicked.connect(self.get_state)
        self.ui.home_btn.clicked.connect(self.go_home)
        self.ui.copolar_rotation_spin.valueChanged.connect(self.update_pitch)
        self.ui.ant_dist.textChanged.connect(self.update_dist)
        self.ui.move_to_start_btn.clicked.connect(self.move_to_start)
        self.ui.resume_btn.clicked.connect(self.resume)
        self.ui.run_btn.clicked.connect(self.toggle_on_off)
        self.ui.mov_left_btn.clicked.connect(self.move_to)
        self.ui.mov_right_btn.clicked.connect(self.move_to)
        self.ui.mov_up_btn.clicked.connect(self.move_to)
        self.ui.mov_down_btn.clicked.connect(self.move_to)
        self.ui.mov_to_0.clicked.connect(self.move_to)
        self.copolar_rotation = self.ui.copolar_rotation_spin.value()
        self.ant_dist = self.ui.ant_dist.text()
        self.ui.reset_btn.clicked.connect(self.reset_settings)
        self.fill_fields()

    @Slot()
    def request_control(self):
        log.debug(f"request_control: dev_label {self.dev_label}, client_id {self.client_id}")  # dev_label "RARM", client_id="tabs/RARM"
        self.controlRequest.emit(self.dev_label, self.client_id, Priority.Manual)
    
    @Slot(str, str, str)
    def _on_granted(self, dev_label:str, client_id:str, token:str):
        if self.dev_label != dev_label:
            return
        if self.client_id != client_id:
            return
        self._have_control = True
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
        self.token = None
    
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

    def update_lamda(self):
        freq = float(self.ui.freq.text())
        C0 = 299792458.0
        try:
            lamda = 100 * (C0)/freq
            self.ui.lamda.setText(f"{lamda:.4f}")
        except ValueError:
            self.ui.lamda.setText("Invalid")

    def fill_fields(self):
        self.ui.calc_x_combo.addItem("λ/2", 1/2)
        self.ui.calc_x_combo.addItem("λ/4", 1/4)
        self.ui.calc_x_combo.addItem("λ/5", 1/5)
        self.ui.calc_x_combo.addItem("λ/10", 1/10)
        self.ui.calc_y_combo.addItem("λ/2", 1/2)
        self.ui.calc_y_combo.addItem("λ/4", 1/4)
        self.ui.calc_y_combo.addItem("λ/5", 1/5)
        self.ui.calc_y_combo.addItem("λ/10", 1/10)
        self.ui.x_start.setText(f"{self.default_pos["x"]}")
        self.ui.y_start.setText(f"{self.default_pos["y"]}")
        self.ui.z_start.setText(f"{self.default_pos["z"]}")
        self.ui.roll_start.setText(f"{self.default_pos["roll"]}")
        self.ui.pitch_start.setText(f"{self.default_pos["pitch"]}")
        self.ui.yaw_start.setText(f"{self.default_pos["yaw"]}")
    
    def delta_x_radio(self):
        if self.ui.calc_x_btn.isChecked():
            try:
                d_x = float(self.ui.lamda.text()) * self.ui.calc_x_combo.currentData()
                self.ui.delta_x.setReadOnly(True)
                self.ui.delta_x.setText(f"{d_x:.2f}")
            except ValueError:
                self.ui.delta_x.setReadOnly(True)
                self.ui.delta_x.setText("Invalid")
        else:
                self.ui.delta_x.setReadOnly(False)

    def delta_x_combo(self):
        if self.ui.calc_x_btn.isChecked():
            try:
                d_x = float(self.ui.lamda.text()) * self.ui.calc_x_combo.currentData()
                self.ui.delta_x.setText(f"{d_x:.2f}")
            except ValueError:
                self.ui.delta_x.setText("Invalid")

    def delta_y_radio(self):
        if self.ui.calc_y_btn.isChecked():
            try:
                d_y = float(self.ui.lamda.text()) * self.ui.calc_y_combo.currentData()
                self.ui.delta_y.setReadOnly(True)
                self.ui.delta_y.setText(f"{d_y:.2f}")
            except ValueError:
                self.ui.delta_y.setReadOnly(True)
                self.ui.delta_y.setText("Invalid")
        else:
                self.ui.delta_y.setReadOnly(False)

    def delta_y_combo(self):
        if self.ui.calc_y_btn.isChecked():
            try:
                d_y = float(self.ui.lamda.text()) * self.ui.calc_y_combo.currentData()
                self.ui.delta_y.setText(f"{d_y:.2f}")
            except ValueError:
                self.ui.delta_y.setText("Invalid")

    def calc_dims(self):
        try:
            self.d_x = float(self.ui.delta_x.text())
            self.d_y = float(self.ui.delta_y.text())
            self.N_x = self.ui.N_x.value()
            self.N_y = self.ui.N_y.value()
            if (self.d_x and self.d_y is not None) and (self.N_x > 1) and (self.N_y > 1):
                min_x = -1 * self.d_x * (self.N_x - 1) / 2
                max_x = self.d_x * (self.N_x - 1) / 2
                min_y = -1 * self.d_y * (self.N_y - 1) / 2
                max_y = self.d_y * (self.N_y - 1) /2
                self.ui.x_dims.setText(f"[{min_x :.2f} , {max_x :.2f}] cm")
                self.ui.y_dims.setText(f"[{min_y :.2f} , {max_y :.2f}] cm")
            self.ui.show_matrix_btn.setEnabled(True)
        except ValueError:
            self.ui.x_dims.setText("ERROR")
            self.ui.y_dims.setText("ERROR")
    
    def fill_matrix(self):
        try:
            x0 = -self.d_x * (self.N_x - 1) / 2.0
            y0 =  self.d_y * (self.N_y - 1) / 2.0
            self.mov_matrix = [
            [(round((x0 + c * self.d_x) * 10, 2), round((y0 - r * self.d_y) * 10, 2)) for c in range(self.N_x)]
            for r in range(self.N_y)
            ]
            self.ui.coordinates_table.setRowCount(self.N_y)
            self.ui.coordinates_table.setColumnCount(self.N_x)
            self.ui.coordinates_table.setHorizontalHeaderLabels([str(c) for c in range(self.N_x)])
            self.ui.coordinates_table.setVerticalHeaderLabels([str(r) for r in range(self.N_y)])
            for r in range(self.N_y):
                for c in range(self.N_x):
                    x, y = self.mov_matrix[r][c]
                    item = QTableWidgetItem(f"({x/10 :.2f}, {y/10 :.2f})")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # read-only cell
                    self.ui.coordinates_table.setItem(r, c, item)
            self.ui.coordinates_table.resizeColumnsToContents()
            self.ui.coordinates_table.resizeRowsToContents()
        except Exception as e:
            log.error(e)
    @Slot()
    def get_state(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        self.command.emit(self.dev_label, self.client_id,{"method" : "get_state", "kwargs" : {}})
    
    def _on_get_state(self, state):
        if state == 1:
            self.moving = True
        else:
            self.moving = False
        self.ui.robot_state.setText(f"{state} - {state_map.get(state, "Unknown")}")

    @Slot()
    def go_home(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if self.moving:
            log.warning("RARM is moving, unable to execute command...")
            return
        self.command.emit(self.dev_label, self.client_id,{"method" : "move_to_start", "kwargs" : {}})
    
    @Slot()
    def update_pitch(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if self.moving:
            log.warning("RARM is moving, unable to execute command...")
            return
        self.copolar_rotation = self.ui.copolar_rotation_spin.value()
        pitch_value = self.default_pos["pitch"] + self.copolar_rotation
        self.ui.pitch_start.setText(str(pitch_value))
        self.set_param()
    
    @Slot()
    def update_dist(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if self.moving:
            log.warning("RARM is moving, unable to execute command...")
            return
        self.ant_dist = float(self.ui.ant_dist.text())
        self.set_param()
    
    @Slot()
    def move_to_start(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if self.moving:
            log.warning("RARM is moving, unable to execute command...")
            return
        self.command.emit(self.dev_label, self.client_id,{"method" : "move_to_start", 
                                                          "kwargs" : {}})
        if self.current_index is not None:
            self.ui.coordinates_table.item(self.current_index[0], self.current_index[1]).setBackground(QBrush(Qt.NoBrush))
        self.current_index = None

    @Slot()
    def resume(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if self.moving:
            log.warning("RARM is moving, unable to execute command...")
            return
        self.command.emit(self.dev_label, self.client_id,{"method" : "resume", "kwargs" : {}})
    
    @Slot()
    def run_demo(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if self.moving:
            log.warning("RARM is moving, unable to execute command...")
            return
        mov_matrix_corrected =[
            self.mov_matrix[i] if i % 2 == 0 else self.mov_matrix[i][::-1]  # Reverse only rows with odd indices (1, 3,...)
            for i in range(len(self.mov_matrix))
        ]
        self.command.emit(self.dev_label, self.client_id,{"method" : "run_demo", 
                                                          "kwargs" : {"mov_matrix" : mov_matrix_corrected,
                                                                      "x" : float(self.ui.x_start.text()),
                                                                      "roll" : float(self.ui.roll_start.text()),
                                                                      "pitch" : float(self.ui.pitch_start.text()),
                                                                      "yaw" : float(self.ui.yaw_start.text())}})
    def toggle_on_off(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if not self.moving:
            # Start
            self.set_param()
            self.command.emit(self.dev_label, self.client_id, {"method" : "switch_on_off", "kwargs" : {"on": True}})
        else:
            # Stop
            self.command.emit(self.dev_label, self.client_id, {"method" : "switch_on_off", "kwargs" : {"on": False}})

        

    def set_param(self):
        try:
            if self.mov_matrix is None:
                log.error("Please generate coordinate matrix.")
                return
            self.d_x = float(self.ui.delta_x.text())
            self.d_y = float(self.ui.delta_y.text())
            self.N_x = self.ui.N_x.value()
            self.N_y = self.ui.N_y.value()
            self.start_pos = {"x" : float(self.ui.x_start.text()),
                            "y" : float(self.ui.y_start.text()),
                            "z" : float(self.ui.z_start.text()),
                            "roll" : float(self.ui.roll_start.text()),
                            "pitch" : float(self.ui.pitch_start.text()),
                            "yaw" : float(self.ui.yaw_start.text())}
        except ValueError:
            QMessageBox.warning(self, "Input error", "Invalid scan parameters")
            return
        self.command.emit(self.dev_label, self.client_id, {"method" : "configure",
                                                           "kwargs" : {
                                                               "d_x" : self.d_x,
                                                               "d_y" : self.d_y,
                                                               "N_x" : self.N_x,
                                                               "N_y" : self.N_y,
                                                               "start_pos" : self.start_pos,
                                                               "ant_dist" : self.ant_dist,
                                                               "current_index" : self.current_index,
                                                               "mov_matrix" : self.mov_matrix,
                                                               "copolar_rotation" : self.copolar_rotation}})
    @Slot()
    def move_to(self):
        if not self._have_control:
            log.error(f"{self.client_id} doesn't control {self.dev_label}")
            return
        if self.moving:
            log.warning("RARM is moving, unable to execute command...")
            return
        if self.mov_matrix is None:
            log.error("Generate coordinate matrix first.")
            return
        sender = self.sender()
        try:
            self.set_param()
            target = self.get_target_loc(sender)
            if target is None:
                log.error(f"Move is out of bound!")
                return
            self.command.emit(self.dev_label, self.client_id,{"method" : "move_to", "kwargs" : {"target":target}})
            self.widgets_disable()
        except ValueError:
            QMessageBox.warning(self, "Input error", "Invalid position")
    
    def get_target_loc(self, sender):
        if sender is self.ui.mov_to_0:
            return (0,0)
        if self.current_index is None:
            log.error("No starting point set!")
            return
        x, y = self.current_index
        rows, cols = self.N_y, self.N_x
        moves = {
            self.ui.mov_up_btn : (-1, 0),
            self.ui.mov_down_btn : (1, 0),
            self.ui.mov_left_btn : (0, -1),
            self.ui.mov_right_btn : (0, 1)
        }
        dx, dy = moves[sender]
        nx, ny = x + dx, y + dy

        if 0 <= nx < rows and 0 <= ny < cols:
            return (nx, ny)
        else:
            return None

    def widgets_disable(self):
        return
    
    def widgets_enable(self):
        return

    @Slot(bool)
    def _on_toggled(self, running: bool):
        self.moving = running
        if self.moving:
            self.ui.run_btn.setText("STOP")
        else:
            self.ui.run_btn.setText("START")
            if self.preempt:
                self.preempt = False
                self.preemptDone.emit(self.dev_label, self.client_id, self.token)
                self.token = None
                self._have_control = False
        log.info(f"Robot movement: {self.moving}")

    def _out_of_steps(self, dev_label:str):
        log.info(f"{dev_label} finished moving!")
        self.toggle_on_off()
    
    @Slot(int,int)
    def _update_robot_position(self, pos):
        log.debug(f"Move to {pos} succesfull!")
        if self.current_index is not None and self.in_bounds(self.mov_matrix, *self.current_index):
            self.ui.coordinates_table.item(self.current_index[0], self.current_index[1]).setBackground(QBrush(Qt.NoBrush))
        if pos is not None:
            self.ui.coordinates_table.item(pos[0], pos[1]).setBackground(QColor("lightgreen"))
        self.current_index = pos
    
    def _on_rarm_pos_acquired(self, pos):
        if self.current_index is not None and self.in_bounds(self.mov_matrix, *self.current_index):
            self.ui.coordinates_table.item(self.current_index[0], self.current_index[1]).setBackground(QBrush(Qt.NoBrush))
        if pos is not None:
            self.ui.coordinates_table.item(pos[0], pos[1]).setBackground(QColor("lightgreen"))
        self.current_index = pos

    def in_bounds(self, matrix, i, j):
        return 0 <= i < len(matrix) and 0 <= j < len(matrix[0])
            
    def save_rarm_params(self):
        settings = QSettings("Microamp", "GUI")
        settings.beginGroup("RARMparams")
        settings.setValue("freq", self.ui.freq.text())
        settings.setValue("lamda", self.ui.lamda.text())
        settings.setValue("delta_x", self.ui.delta_x.text())
        settings.setValue("delta_y", self.ui.delta_y.text())
        settings.setValue("N_x", self.ui.N_x.value())
        settings.setValue("N_y", self.ui.N_y.value())
        settings.setValue("ant_dist", self.ui.ant_dist.text())
        settings.setValue("copolar_rotation", self.ui.copolar_rotation_spin.value())
        settings.setValue("x_start", self.ui.x_start.text())
        settings.setValue("y_start", self.ui.y_start.text())
        settings.setValue("z_start", self.ui.z_start.text())
        settings.setValue("roll_start", self.ui.roll_start.text())
        settings.setValue("pitch_start", self.ui.pitch_start.text())
        settings.setValue("yaw_start", self.ui.yaw_start.text())
        settings.endGroup()

    def restore_rarm_params(self):
        settings = QSettings("Microamp", "GUI")
        settings.beginGroup("RARMparams")
        self.ui.freq.setText(settings.value("freq", "", type=str))
        self.ui.lamda.setText(settings.value("lamda", "", type=str))
        self.ui.delta_x.setText(settings.value("delta_x", "", type=str))
        self.ui.delta_y.setText(settings.value("delta_y", "", type=str))
        self.ui.N_x.setValue(settings.value("N_x", 0, type=int))
        self.ui.N_y.setValue(settings.value("N_y", 0, type=int))
        self.ui.ant_dist.setText(settings.value("ant_dist", "", type=str))
        self.ui.copolar_rotation_spin.setValue(settings.value("copolar_rotation", 0, type=int))
        self.ui.x_start.setText(settings.value("x_start", "", type=str))
        self.ui.y_start.setText(settings.value("y_start", "", type=str))
        self.ui.z_start.setText(settings.value("z_start", "", type=str))
        self.ui.roll_start.setText(settings.value("roll_start", "", type=str))
        self.ui.pitch_start.setText(settings.value("pitch_start", "", type=str))
        self.ui.yaw_start.setText(settings.value("yaw_start", "", type=str))
        settings.endGroup()

    def reset_settings(self):
        self.command.emit(self.dev_label, self.client_id, {"method" : "_reset_settings", "kwargs" : {}})