__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import os
import logging
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.exporters import ImageExporter
import h5py
import time
from datetime import datetime
from enum import IntEnum
from typing import Dict, Any
from scipy.io import savemat
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot, QThread, Signal, QObject, Qt, QTimer
from pathlib import Path
from .ui_PNF import Ui_PNF
from src.Utils.config_files.measure_config import MEASUREMENT_TYPES, SAVE_PATH, EXPORT_FORMATS, Priority, State
from src.Data_Processing import (
    VNAConfig, AUTConfig, GeneralConfig,
    PNFMeasurement, PNFMeasurementConfig, PNFData,
    MeasurementFile, HDF5Format, MATFormat)

log = logging.getLogger("GUI")

pg.setConfigOption('background', 'w')   # white background
pg.setConfigOption('foreground', 'k')   # black axes, ticks, labels

class PNF(QWidget):

    controlRequest = Signal(str, str, int) # passing dev_label, client_id, priority level
    controlRelease = Signal(str, str, str) # passing dev_label, client_id, token
    command = Signal(str, str, dict)       # passing dev_label, client_id, dict of method + arguments

    def __init__(self, workers:dict, threads:dict, mediator:QObject, parent=None):
        super().__init__(parent)
        self.ui = Ui_PNF()
        self.ui.setupUi(self)
        self.parent = parent
        self.dev_label = None
        self.client_id = "PNF"
        self._threads = threads
        self._workers = workers
        self.worker = self._workers["MEAS"]
        self._tokens = {}
        self.mediator = mediator

        self._devs = {
            "VNA": {"worker": self._workers.get("VNA"), "control": False},
            "RARM" : {"worker": self._workers.get("RARM"), "control": False}
        }
        names = [name for name, obj in self._devs.items() if obj is not None]
        text = (", ".join(names) if names else "— none —")

        self.f_data = []

        self.new_f = None
        self.new_re = None
        self.new_im = None
        self.current_index = None
        self.N_x = None
        self.N_y = None
        self.N_f = None
        self.meas_data = None
        self.mag_db = None
        self.phase = None
        self.phase_plot_data = None
        self.mag_db_plot_data = None
        self.selected_freq = None
        self.progress = 0
        self.start_time = None
        self.accumulated_time = 0
        self.total_step_time = 0
        self.last_step_timestamp = None
        self.cross_pol = True
        self.current_pol = "copolar"
        self.ant_dist = None
        self.calibrated = False
        self.meas_config = PNFMeasurementConfig(type=self.client_id)

        self.PNF_timer = QTimer()
        self.PNF_timer.timeout.connect(self.update_elapsed_time)
        self.ui.meas_progress.setRange(0,100)
        self.ui.meas_progress.setValue(0)
        self.ui.screenshot_btn.setEnabled(False)
        self.ui.export_btn.setEnabled(False)
        self.ui.export_format_combo.setEnabled(False)
        self.ui.export_format_combo.addItems(EXPORT_FORMATS)
        self.ui.spinbox_lvl_mag_max.setValue(0)
        self.ui.spinbox_lvl_mag_min.setValue(-80)
        self.ui.cross_pol_check.toggled.connect(self.on_pol_toggled)
        self.ui.export_btn.clicked.connect(self.export_meas)
        self.ui.screenshot_btn.clicked.connect(self.save_screenshots)
        self.ui.spinbox_lvl_mag_max.valueChanged.connect(self.update_mag_plot_levels)
        self.ui.spinbox_lvl_mag_min.valueChanged.connect(self.update_mag_plot_levels)
        self.plot_setup()
        self.ui.freq_comboBox.currentIndexChanged.connect(self.change_plot_freq)


    @Slot(str, str, str)
    def _on_granted(self, dev_label: str, client_id: str, token: str):
        if self.client_id != client_id: return
        if dev_label not in self._devs: return
        log.debug(f"granted token for {dev_label}")
        self._tokens[dev_label] = token
        self._devs[dev_label]["control"] = True
        if all(dev in self._tokens for dev in self._devs):
            log.debug("All devices locked. Starting measurement…")
    
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
    
    def _on_get_config(self, dev_label:str, dev_config:dict):
        match dev_label:
            case "VNA":
                self._on_freq_N_acquired(dev_config["pwr"],
                                         dev_config["f_start"],
                                         dev_config["f_stop"],
                                         dev_config["N"],
                                         dev_config["s_param"])
            case "RARM":
                self._on_rarm_params_acquired(dev_config["d_x"],
                                              dev_config["d_y"],
                                              dev_config["pos"],
                                              dev_config["pos_matrix"],
                                              dev_config["copolar_rotation"],
                                              dev_config["ant_dist"],
                                              dev_config["calibrated"])
        self.aut_config = AUTConfig()
        self.parent._on_get_devs_config(dev_label)

    @Slot(float, float, int)
    def _on_freq_N_acquired(self, pwr ,f_start, f_stop, N, s_param):
        self.f_data = np.linspace(f_start, f_stop, N)
        self.N_f = N
        self.vna_config = VNAConfig(
            pwr,
            self.f_data,
            f_start,
            f_stop,
            N,
            s_param
        )
        self.ui.freq_comboBox.clear()  # usuń stare elementy
        self.ui.freq_comboBox.addItems([f"{f/1e6:.3f} MHz" for f in self.f_data])
        log.debug(f"new_f acquired {self.f_data.shape} {self.f_data}")
    
    def _on_meas_prepare(self, status:bool):
        log.info(f"Measurement prepare status: {status}")
        if all(param is not None for param in (self.N_x, self.N_y, self.N_f)):
            self.meas_data = np.full((self.N_y, self.N_x, self.N_f), np.nan, dtype=complex)
            self.mag_db = np.full((self.N_y, self.N_x, self.N_f), np.nan, dtype=float)
            self.phase = np.full((self.N_y, self.N_x, self.N_f), np.nan, dtype=float)
            if self.selected_freq is None:
                self.selected_freq = self.ui.freq_comboBox.currentIndex()
            self.mag_db_plot_data = self.mag_db[:, :, self.selected_freq]
            self.phase_plot_data = self.phase[:, :, self.selected_freq]
        self.clean_plots()

    def _on_started(self):
        log.info("started!")
        self.meas_config.crosspolar = self.cross_pol
        self.ui.screenshot_btn.setEnabled(False)
        self.ui.export_btn.setEnabled(False)
        self.ui.export_format_combo.setEnabled(False)
        self.current_pol = "copolar"
        if self.cross_pol:
            self.steps = len(self.pos_matrix) * len(self.pos_matrix[0]) * 2
        else:
            self.steps = len(self.pos_matrix) * len(self.pos_matrix[0])
        self.time_started = datetime.now()
        self.ui.meas_progress.setFormat("%p%")
        self.ui.meas_progress.setValue(0)
        self.accumulated_time = 0
        self.step_count = 0
        self.total_step_time = 0
        self.start_time = time.perf_counter() # start timer
        self.last_step_timestamp = self.start_time
        self.PNF_timer.start(200)
        self.general_config = GeneralConfig(
            t_start=self.time_started,
            devices = list(self._devs.keys())
        )
        self.data = PNFData()
        self.data.copolar = np.full((self.N_y, self.N_x, self.N_f), np.nan, dtype=complex)
        self.data.crosspolar = np.full((self.N_y, self.N_x, self.N_f), np.nan, dtype=complex)

    def _on_scan_finished(self):
        if self.cross_pol:
            if self.current_pol == "copolar":
                self.current_pol = "crosspolar"
                self.data.copolar = self.meas_data
                self.meas_data = np.full((self.N_y, self.N_x, self.N_f), np.nan, dtype=complex)
                self.mag_db = np.full((self.N_y, self.N_x, self.N_f), np.nan, dtype=float)
                self.phase = np.full((self.N_y, self.N_x, self.N_f), np.nan, dtype=float)
                if self.selected_freq is None:
                    self.selected_freq = self.ui.freq_comboBox.currentIndex()
                self.mag_db_plot_data = self.mag_db[:, :, self.selected_freq]
                self.phase_plot_data = self.phase[:, :, self.selected_freq]
                self.clean_plots()
                self.parent.command.emit(self.parent.dev_label, self.parent.client_id, {"method": "next_scan", "kwargs": {}})
            else:
                self.data.crosspolar = self.meas_data
                self.parent.command.emit(self.parent.dev_label, self.parent.client_id, {"method": "no_scan", "kwargs": {}})
        else:
            self.data.copolar = self.meas_data
            self.parent.command.emit(self.parent.dev_label, self.parent.client_id, {"method": "no_scan", "kwargs": {}})

    def _on_finished(self):
        log.debug("Measurement finished.")
        self.time_stop = datetime.now()
        self.PNF_timer.stop()
        self.generate_output()
        self.ui.meas_progress.setFormat("Done!")
        self.ui.screenshot_btn.setEnabled(True)
        self.ui.export_btn.setEnabled(True)
        self.ui.export_format_combo.setEnabled(True)

    def _on_stopped(self):
        log.debug("Measurement was stopped.")
        self.time_stop = datetime.now()
        self.PNF_timer.stop()
        self.generate_output()
        self.ui.meas_progress.setFormat("Stopped")
        self.ui.screenshot_btn.setEnabled(True)
        self.ui.export_btn.setEnabled(True)
        self.ui.export_format_combo.setEnabled(True)

    
    def _on_paused(self):
        self.PNF_timer.stop()
        self.accumulated_time += time.perf_counter() - self.start_time
        self.ui.screenshot_btn.setEnabled(True)
        self.ui.export_btn.setEnabled(True)
        self.ui.export_format_combo.setEnabled(True)
    
    def _on_resumed(self):
        self.start_time = time.perf_counter()  # reset start reference
        self.last_step_timestamp = self.start_time
        self.PNF_timer.start(200)
        self.ui.screenshot_btn.setEnabled(False)
        self.ui.export_btn.setEnabled(False)
        self.ui.export_format_combo.setEnabled(False)

    @Slot(np.ndarray, np.ndarray)
    def _on_data_acquired(self, re_data, im_data):
        self.new_re = re_data
        self.new_im = im_data
        log.debug(f"New re acquired {self.new_re[10]}")
        self.save_sample()

    @Slot(float)
    def _on_position_acquired(self, pos):
        self.current_index = pos
        if pos is None:
            self.ui.current_posLabel.setText(f"Current: None")
        else:
            self.ui.current_posLabel.setText(f"Current: ({pos[0]},{pos[1]})")
        log.debug(f"New index acquired {self.current_index}")
        now = time.perf_counter()
        step_time = now - self.last_step_timestamp
        self.total_step_time += step_time
        self.step_count+=1
        self.last_step_timestamp = now
        self.progress = round((self.step_count/self.steps) * 100)
        self.ui.meas_progress.setValue(self.progress) # Update progress bar

    @Slot(float, float)
    def _on_rarm_params_acquired(self, d_x, d_y, pos, pos_matrix, copolar_rotation, ant_dist, calibrated):
        self.pos_matrix = pos_matrix
        if pos is not None:
            self.ui.current_posLabel.setText(f"({pos[0]},{pos[1]})")
        #self.ui.stop_posEntry.setText(stop)
        self.ui.stepLabel.setText(f"Dims: [{len(pos_matrix)},{len(pos_matrix[0])}]")
        if calibrated:
            self.ui.calibration_lbl.setText('Calibration: <span style="color: green;">Calibrated</span>')
        else:
            self.ui.calibration_lbl.setText('Calibration: <span style="color: red;">Not calibrated</span>')
        self.d_x = d_x
        self.d_y = d_y
        self.N_y = len(pos_matrix)
        self.N_x = len(pos_matrix[0])
        self.ant_dist = ant_dist
        self.copolar_rotation = copolar_rotation
        self.calibrated = calibrated
        log.debug(f"positions acquired: {pos}, [{len(pos_matrix[0])},{len(pos_matrix)}], Copolar rotation: {self.copolar_rotation}, distance: {self.ant_dist}")
        self.steps = len(pos_matrix) * len(pos_matrix[0]) # amount of steps
        #self.current_index = (0,0)
        self.meas_config.distance = ant_dist
        self.meas_config.scan_mat = pos_matrix
        self.meas_config.d_x = d_x
        self.meas_config.d_y = d_y
        self.meas_config.copolar_rotation = copolar_rotation
        self.meas_config.crosspolar = self.cross_pol

    def plot_setup(self):
        # ------------------ Magnitude ImageView ------------------
        self.mag_view = pg.ImageView()
        self.ui.Mag_2D_plot.addWidget(self.mag_view)
        self.mag_view.getView().setBackgroundColor('black')
        cmap = pg.colormap.get("viridis")
        self.mag_view.setColorMap(cmap)
        self.mag_view.setLevels(-70, -10)

        # ------------------ Phase ImageView ------------------
        self.phase_view = pg.ImageView()
        self.ui.Phase_2D_plot.addWidget(self.phase_view)
        self.phase_view.getView().setBackgroundColor('black')
        # Cyclic HSV colormap
        #cmap = pg.colormap.getFromMatplotlib("hsv")
        cmap = pg.colormap.get("viridis")
        self.phase_view.setColorMap(cmap)
        self.phase_view.setLevels(-np.pi, np.pi)

    def save_sample(self):
        if self.current_index is None:
            log.error("Measurement point missing!")
            return
        log.debug(f"Current measurement point: {self.current_index}")
        vec_complex = self.new_re + 1j * self.new_im
        mag = np.abs(vec_complex)
        mag = np.maximum(mag, 1e-15)              # avoid log10(0)
        mag_db_vec = 20 * np.log10(mag)
        phase_vec = np.angle(vec_complex)
        self.meas_data[self.current_index[0], self.current_index[1], :] = vec_complex
        self.mag_db[self.current_index[0], self.current_index[1], :] = mag_db_vec
        self.phase[self.current_index[0], self.current_index[1], :] = phase_vec
        if self.selected_freq is not None:
            self.mag_db_plot_data[self.current_index[0], self.current_index[1]] = mag_db_vec[self.selected_freq]
            self.phase_plot_data[self.current_index[0], self.current_index[1]] = phase_vec[self.selected_freq]
            self.update_plots()
    
    def update_plots(self):
        if self.mag_db_plot_data is None or self.phase_plot_data is None:
            return
        self.mag_view.setImage(self.mag_db_plot_data.T, autoLevels=False)
        self.phase_view.setImage(self.phase_plot_data.T, autoLevels=False)
        #clean plot and put new one
        
    def change_plot_freq(self):
        self.selected_freq = self.ui.freq_comboBox.currentIndex()
        if self.mag_db is None or self.phase is None:
            return
        self.mag_db_plot_data = self.mag_db[:, :, self.selected_freq]
        self.phase_plot_data = self.phase[:, :, self.selected_freq]
        self.update_plots()

    def update_mag_plot_levels(self):
        vmin = self.ui.spinbox_lvl_mag_min.value()
        vmax = self.ui.spinbox_lvl_mag_max.value()
        if vmin >= vmax:
            vmax = vmin + 1
            self.ui.spinbox_lvl_mag_max.setValue(vmax)
        self.mag_view.setLevels(vmin, vmax)
    
    def clean_plots(self):
        self.mag_view.clear()
        self.phase_view.clear()
        #clean plot
        
    def generate_output(self):
        self.general_config.t_stop = self.time_stop
        self.general_config.duration = self.ui.elapsed_time_lbl.text()
        self.measurement = PNFMeasurement(
            general=self.general_config,
            measurement=self.meas_config,
            vna=self.vna_config,
            aut=self.aut_config
        )
        self.measurement.data = self.data
        #print(self.measurement.serialize_config())

    def on_pol_toggled(self, checked: bool):
        self.cross_pol = checked

    def export_meas(self):
        try:
            date_str = self.time_started.strftime("%Y.%m.%d")
            start_time = self.time_started.strftime("%H_%M_%S")
            folder_name = f"PNF_MEAS-{date_str}_{start_time}"

            folder_path = SAVE_PATH / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)

            format_ = EXPORT_FORMATS[self.ui.export_format_combo.currentIndex()]

            match format_:
                case ".h5":
                    file_path = folder_path / "measurement.h5"
                    file = MeasurementFile(
                        path=file_path,
                        file_format=HDF5Format(),
                    )
                    file.save(self.measurement)
                    log.info(f"Exported {file_path}")

                case ".mat":
                    file_path = folder_path / "measurement.mat"
                    file = MeasurementFile(
                        path=file_path,
                        file_format=MATFormat(),
                    )
                    file.save(self.measurement)
                    log.info(f"Exported {file_path}")

        except Exception as e:
            log.exception(e)

        #Save and read test
        #
        # try:
        #     fmt = HDF5Format()
        #     cls_name = fmt.peek_meas_type(file_path)
        #     measurement_cls = MEASUREMENT_TYPES[cls_name]
        #     file = MeasurementFile(path=file_path, file_format=fmt)
        #     measurement_obj = file.load(measurement_cls)
        #     print(measurement_obj.name)
        #     print(measurement_obj.serialize_config())
        #     print(measurement_obj.data)
        # except Exception as e:
        #     log.exception(e)
        
    def save_screenshots(self):
        try:
            date_str = self.time_started.strftime("%Y.%m.%d")
            time_str = self.time_started.strftime("%H_%M_%S")
            folder_name = f"PNF_MEAS-{date_str}_{time_str}"
            save_path = os.path.join(SAVE_PATH, folder_name)
            if not os.path.exists(save_path):
                os.makedirs(save_path, exist_ok=True)
            freq = self.ui.freq_comboBox.currentText()
            freq = freq.replace(" ", "_")
            mag_exporter = ImageExporter(self.mag_view.getImageItem())
            mag_exporter.export(save_path + '\\'+f'MAG_dB_{freq}_PNF_MEAS-{date_str}_{time_str}.png')
            mag_exporter = ImageExporter(self.phase_view.getImageItem())
            mag_exporter.export(save_path + '\\'+f'PHASE_{freq}_PNF_MEAS-{date_str}_{time_str}.png')
        except Exception as e:
            log.error(e)

        
    def update_elapsed_time(self):
        if not self.start_time:
            return
        current_elapsed = (time.perf_counter() - self.start_time)
        total = self.accumulated_time + current_elapsed
        self.ui.elapsed_time_lbl.setText(f"{self.format_time(total)}")
        if self.step_count > 0:
            avg_step = self.total_step_time / self.step_count
            remaining = avg_step * (self.steps - self.step_count)
            self.ui.remaining_time_lbl.setText(f"/{self.format_time(remaining)}")
        else:
            self.ui.remaining_time_lbl.setText("/--:--:--")

    @staticmethod
    def format_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"