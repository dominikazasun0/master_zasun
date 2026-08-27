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
import matplotlib.pyplot as plt
import copy
from pathlib import Path
from typing import Callable, Dict
from OpenGL import GL as gl_lib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.interpolate import RegularGridInterpolator
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QDir, QModelIndex, Signal, Slot
from PySide6.QtGui import QColor, QVector3D, QLinearGradient
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileSystemModel,QSizePolicy, QButtonGroup
from PySide6.QtGraphsWidgets import Q3DSurfaceWidgetItem
from PySide6.QtDataVisualization import (
    Q3DSurface, QSurface3DSeries, QSurfaceDataProxy, QValue3DAxis, Q3DTheme)
from .ui_data_processing import Ui_data_processing
from src.Utils.config_files.measure_config import SAVE_PATH, EXPORT_FORMATS, MEASUREMENT_TYPES
from src.Data_Processing import (
    MeasurementFile, HDF5Format, NF2FF, NF2FFData, FFData)

image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../images"))
log = logging.getLogger(__name__)

pg.setConfigOption('background', 'w')   # white background
pg.setConfigOption('foreground', 'k')   # black axes, ticks, labels

class DataProcessing(QWidget):

    command = Signal(str, str, dict)       # passing dev_label, client_id, dict of method + arguments

    def __init__(self, worker):
        super().__init__()
        self.ui = Ui_data_processing()
        self.ui.setupUi(self)
        self.dev_label = "DATA_PROC"
        self.client_id = "tabs/DATA_PROC"
        self.detail_map = {
            "PNF" : self.fill_PNF_details,
            "FF_AZ" : self.fill_FF_details
        }
        self.result_map = {
            "PNF" : self.fill_PNF_results,
            "FF_AZ" : self.fill_FF_results
        }
        self.transform_map = {
            "PWS" : self.try_nf2ff_transform,
            "MoM" : self.try_nf2ff_transform,
        }
        self.worker = worker
        self.meas_mag_db = None
        self.meas_phase = None
        self.copolar_data_mag_db = None
        self.crosspolar_data_mag_db = None
        self.copolar_phase = None
        self.crosspolar_phase = None
        self.file_tree = self.ui.dir_tree_view
        self.dir = SAVE_PATH
        self.ff_3d_plot_mesh = None
        self.ff_uv_mesh = None
        self.pattern_color_dynamic = 50
        self.setup_file_view(self.dir)
        self.file_tree.doubleClicked.connect(self.try_load_meas)
        self.ui.tree_view_refresh_btn.clicked.connect(self.refresh_file_view)
        self.ui.transform_combo.addItem("Plane Wave Spectrum (PWS)", "PWS")
        self.ui.transform_combo.addItem("Method of Moments (MoM)", "MoM")
        self.ui.transform_combo.addItem("Far-Field Prepare", "FF")
        self.ui.trans_start_btn.clicked.connect(self.try_transform)
        self.ui.sel_freq_combo.currentTextChanged.connect(self.update_PNF_meas_res_plots)
        self.ui.crosspolar_radio_btn.toggled.connect(self.update_PNF_meas_res_plots)
        self.ui.copolar_radio_btn.toggled.connect(self.update_PNF_meas_res_plots)
        self.ui.post_proc_grp.setEnabled(False)
        self.ui.result_grp.setEnabled(False)
        self.transforming = False

        # self.TH, self.PH, self.AF = array_factor_rect(
        #     Nx=16, Ny=16, dx=0.5, dy=0.5,
        #     theta0_deg=20, phi0_deg=20,
        #     window=None, n_theta=91, n_phi=361,
        #     upper_hemisphere_only=True
        # )
        # self.current_dataset_uv = self.Convert_to_UV(self.TH, self.PH, self.AF)
        # self.TH_2, self.PH_2, self.AF_2 = self.el_over_az_to_spherical(self.TH, self.PH, self.AF)
        # np.savetxt("TH_Converted.csv", np.rad2deg(self.TH_B), delimiter=",")
        # np.savetxt("PH_Converted.csv", np.rad2deg(self.PH_B), delimiter=",")
        # np.savetxt("AF_Converted.csv", self.AF_B, delimiter=",")

        self.setup_plots()

        log.debug("Loaded Data Processing tab.")

    """ ----- interpreter ----- """
    @Slot(str, dict)
    def response_interp(self, client_id: str, response: Dict):
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

    def setup_file_view(self, directory):
            self.model = QFileSystemModel(self)
            self.model.setRootPath(str(directory))
            self.file_tree.setModel(self.model)
            self.file_tree.setRootIndex(self.model.index(str(directory)))
    
    def refresh_file_view(self):
        root_path = self.model.rootPath()
        # Re-setting the root path forces the QFileSystemWatcher to update
        self.model.setRootPath("") # Clear it briefly
        self.model.setRootPath(root_path) 
        log.debug("File tree refreshed!")
    
    def try_load_meas(self, index:QModelIndex):
        model = self.file_tree.model()
        self.sel_file_path = model.filePath(index)
        if os.path.isfile(self.sel_file_path):
            _, extension = os.path.splitext(self.sel_file_path)
            if extension.lower() in EXPORT_FORMATS:
                log.debug(f"Valid file detected: {self.sel_file_path}")
                self.load_meas(self.sel_file_path, extension)
            else:
                log.error(f"Unsupported format: {extension}")
        else:
            # User clicked a folder, ignore or handle expansion
            pass
    
    def load_meas(self, file_path:str, extension:str):
        try:
            match extension:
                case ".h5":
                    fmt = HDF5Format()
                    cls_name = fmt.peek_meas_type(file_path)
                    measurement_cls = MEASUREMENT_TYPES[cls_name]
                    file = MeasurementFile(path=file_path, file_format=fmt)
                    self.sel_measurement = file.load(measurement_cls)
                    self.fill_details()
                    self.fill_post_proc()
                    self.result_map.get(self.sel_measurement.name)()
                    self.ui.post_proc_grp.setEnabled(True)
                    self.ui.result_grp.setEnabled(True)
        except Exception as e:
            log.exception(e)
            self.ui.post_proc_grp.setEnabled(False)
            self.ui.result_grp.setEnabled(False)
    
    def fill_details(self):
        meas = self.sel_measurement
        mapping = [
            (meas.general.t_start, self.ui.t_start_lbl, lambda v: str(v).split('.')[0]),
            (meas.general.t_stop, self.ui.t_stop_lbl, lambda v: str(v).split('.')[0]),
            (meas.general.duration, self.ui.duration_lbl, lambda v: str(v)),
            (meas.general.operator, self.ui.operator_lbl, lambda v: str(v)),
            (meas.general.devices, self.ui.devices_lbl, lambda v: str(v)),
            (meas.general.probe_ant, self.ui.probe_lbl, lambda v: str(v)),
            (meas.aut.aut_type, self.ui.aut_type_lbl, lambda v: str(v)),
            (meas.aut.ser_num, self.ui.aut_sn_lbl, lambda v: str(v)),
            (meas.aut.comment, self.ui.aut_com_lbl, lambda v: str(v)),
            (meas.vna.pwr_lvl, self.ui.rf_pwr_lbl, lambda v: f"{float(v)} dBm"),
            (meas.vna.f_start, self.ui.f_start_lbl, lambda v: f"{float(v) / 1e6:.3f} MHz"),
            (meas.vna.f_stop, self.ui.f_stop_lbl, lambda v: f"{float(v) / 1e6:.3f} MHz"),
            (meas.vna.n_freq, self.ui.n_f_lbl, lambda v: str(v)),
            (meas.vna.s_param, self.ui.param_lbl, lambda v: str(v)),
            (meas.measurement.type, self.ui.meas_type_lbl, lambda v: str(v)),
            (meas.measurement.distance, self.ui.meas_dist_lbl, lambda v:  f"{float(v) * 10} mm")
        ]
        for value, label, transform in mapping:
            if value is None or str(value).strip() == "":
                label.setText('<span style="color: red;">Unknown</span>')
            else:
                try:
                    label.setText(transform(value))
                except:
                    label.setText(str(value))
        self.detail_map.get(self.sel_measurement.name)()

    def fill_PNF_details(self):
        self.ui.custom_det_0_lbl.setText("Scan [Ny,Nx]:")
        self.ui.custom_det_1_lbl.setText("x-step:")
        self.ui.custom_det_2_lbl.setText("y-step:")
        self.ui.custom_det_3_lbl.setText("Antenna rotation:")
        self.ui.custom_det_4_lbl.setText("Cal:")
        self.ui.custom_det_5_lbl.setText("Cross-polarization:")
        meas = self.sel_measurement
        mapping = [
            (meas.measurement.scan_mat, self.ui.custom_val_0_lbl, lambda v: str(np.array(v).shape[:2])),
            (meas.measurement.d_x, self.ui.custom_val_1_lbl, lambda v: f"{float(v)} mm"),
            (meas.measurement.d_y, self.ui.custom_val_2_lbl, lambda v: f"{float(v)} mm"),
            (meas.measurement.copolar_rotation, self.ui.custom_val_3_lbl, lambda v: f"{str(v)}°"),
            (meas.measurement.cal_val, self.ui.custom_val_4_lbl, lambda v: str(v)),
            (meas.measurement.crosspolar, self.ui.custom_val_5_lbl, lambda v: "Yes" if v else "No"),
        ]
        for value, label, transform in mapping:
            if value is None or str(value).strip() == "":
                label.setText('<span style="color: red;">Unknown</span>')
            else:
                try:
                    label.setText(transform(value))
                except:
                    label.setText(str(value))
        if meas.measurement.crosspolar:
            self.ui.copolar_radio_btn.setEnabled(True)
            self.ui.crosspolar_radio_btn.setEnabled(True)
        else:
            self.ui.crosspolar_radio_btn.setEnabled(False)
            self.ui.copolar_radio_btn.setEnabled(True)
            self.ui.copolar_radio_btn.setChecked(True)

    def fill_FF_details(self):
        pass

    def fill_FF_results(self):
        pass

    def fill_post_proc(self):
        freq_list = self.sel_measurement.vna.freq_lst
        self.ui.sel_freq_combo.clear()
        self.ui.sel_freq_combo.addItems(f"{float(f) / 1e6:.3f} MHz" for f in freq_list)

    def fill_PNF_results(self):
        copolar_data = self.sel_measurement.data.copolar
        self.copolar_data_mag_db = 20 * np.log10(np.abs(copolar_data))
        self.copolar_phase = np.angle(copolar_data)
        if self.sel_measurement.measurement.crosspolar:
            crosspolar_data = self.sel_measurement.data.crosspolar
            self.crosspolar_data_mag_db = 20 * np.log10(np.abs(crosspolar_data))
            self.crosspolar_phase = np.angle(crosspolar_data)
        self.clear_res_plots()
        self.meas_PNF_plots_setup()
        self.update_PNF_meas_res_plots()

    def clear_res_plots(self):
        layout = self.ui.det_res_plt_1
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())
        layout = self.ui.det_res_plt_2
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

    def meas_PNF_plots_setup(self):
        # ------------------ Magnitude ImageView ------------------
        self.meas_mag_view = pg.ImageView()
        self.ui.det_res_plt_1_title.setText("Magnitude [dB]")
        self.ui.det_res_plt_1.addWidget(self.meas_mag_view)
        self.meas_mag_view.getView().setBackgroundColor('black')
        cmap = pg.colormap.get("viridis")
        self.meas_mag_view.setColorMap(cmap)
        self.meas_mag_view.setLevels(-70, -10)
        # ------------------ Phase ImageView ------------------
        self.meas_phase_view = pg.ImageView()
        self.ui.det_res_plt_2_title.setText("Phase [rad]")
        self.ui.det_res_plt_2.addWidget(self.meas_phase_view)
        self.meas_phase_view.getView().setBackgroundColor('black')
        # Cyclic HSV colormap
        #cmap = pg.colormap.getFromMatplotlib("hsv")
        cmap = pg.colormap.getFromMatplotlib("twilight_shifted")
        #cmap = pg.colormap.get("viridis")
        self.meas_phase_view.setColorMap(cmap)
        self.meas_phase_view.setLevels(-np.pi, np.pi)
    
    def update_PNF_meas_res_plots(self):
        self.selected_freq = self.ui.sel_freq_combo.currentIndex()
        if self.ui.copolar_radio_btn.isChecked() and self.copolar_data_mag_db is not None:
            self.meas_mag_db = self.copolar_data_mag_db
            self.meas_phase = self.copolar_phase
        if self.ui.crosspolar_radio_btn.isChecked() and self.crosspolar_data_mag_db is not None:
            self.meas_mag_db = self.crosspolar_data_mag_db
            self.meas_phase = self.crosspolar_phase
        if self.meas_mag_db is not None or self.meas_phase is not None:
            self.meas_mag_db_plot_data = self.meas_mag_db[:, :, self.selected_freq]
            self.meas_phase_plot_data = self.meas_phase[:, :, self.selected_freq]
            self.meas_mag_view.setImage(self.meas_mag_db_plot_data.T, autoLevels=False)
            self.meas_phase_view.setImage(self.meas_phase_plot_data.T, autoLevels=False)
    
    def try_transform(self):
        try:
            if not self.transforming:
                self.sel_transform = self.ui.transform_combo.currentData()
                transform = self.transform_map.get(self.sel_transform)
                transform()
        except Exception as e:
            log.error(e)

    def try_nf2ff_transform(self):
        log.info("NF2FF transform!")
        try:
            self.sel_nf2ff_data = NF2FFData(
                frequency_hz=self.sel_measurement.vna.freq_lst[self.selected_freq],
                distance_mm=self.sel_measurement.measurement.distance,
                sampling=[self.sel_measurement.measurement.d_y,
                          self.sel_measurement.measurement.d_x],
                copolar_data=self.sel_measurement.data.copolar[:,:,self.selected_freq],
                coordinates=self.sel_measurement.measurement.scan_mat,
                copolar_rotation=self.sel_measurement.measurement.copolar_rotation,
                cross_pol=self.sel_measurement.measurement.crosspolar)
            if self.sel_measurement.measurement.crosspolar:
                self.sel_nf2ff_data.crosspolar_data = self.sel_measurement.data.crosspolar[:,:, self.selected_freq]
            self.command.emit(self.dev_label, self.client_id, {"method": "nf2ff_transform",
                                                               "kwargs": {
                                                                   "type": self.sel_transform,
                                                                   "data": self.sel_nf2ff_data}})

        except Exception as e:
            log.error(e)
    
    def _on_nf2ff_trans_start(self):
        log.debug("NF2FF transformation started!")

    def _on_nf2ff_trans_stop(self):
        log.critical("NF2FF transformation stopped!")

    def _on_nf2ff_trans_finish(self, result):
        log.info("NF2FF transformation finished!")
        #self.try_save_ff(result)
        self.ff_plot_data = result
        self.clear_ff_plots()
        self.update_ff_3d_plot(result)
        self.update_ff_uv_plot(result)
        self.update_cut_1_plot(result)
        self.update_cut_2_plot(result)

    def try_save_ff(self, result):
        try:
            format_ = ".h5"
            match format_:
                case ".h5":
                    file_path = "C:\\Users\\kmark\\Desktop\\test" + f"nf2ff_result_{self.sel_measurement.vna.freq_lst[self.selected_freq]// 1000000}_MHz.h5"
                    file = MeasurementFile(
                        path=file_path,
                        file_format=HDF5Format(),
                    )
                    self.nf2ff = NF2FF(self.sel_nf2ff_data)
                    self.nf2ff.ff_result = result
                    file.save(self.nf2ff)
                    log.info(f"Created {file_path}")
        except Exception as e:
            log.exception(e)

    def clear_ff_plots(self):
        if self.ff_3d_plot_mesh is not None:
            self.pattern_plot.removeItem(self.ff_3d_plot_mesh)
        if self.ff_uv_mesh is not None:
            self.uv_plot.removeItem(self.ff_uv_mesh)

    def setup_plots(self):
        self.setup_ff_3d_plot()
        self.setup_ff_uv_plot()
        self.setup_ff_cut_1_plot()
        self.setup_ff_cut_2_plot()

    def setup_ff_3d_plot(self):
        self.pattern_cmap = pg.ColorMap(
            pos=np.array([0.0, 0.25, 0.5, 0.75, 1.0]),
            color=np.array([
                [148, 0, 211, 255], # Violet (Min)
                [0, 0, 255, 255],   # Blue
                [0, 255, 0, 255],   # Green
                [255, 255, 0, 255], # Yellow
                [255, 0, 0, 255]    # Red (Max)
            ], dtype=np.ubyte)
        )
        self.clear_layout(self.ui.ff_3d_plot)
        self.pattern_plot = gl.GLViewWidget()
        self.pattern_colorbar = pg.GraphicsLayoutWidget()
        self.pattern_plot.setBackgroundColor(QColor('black'))
        self.pattern_plot.opts['distance'] = 100
        self.pattern_plot.opts['elevation'] = 90
        self.pattern_plot.opts['azimuth'] = -90
        self.ui.ff_3d_plot.addWidget(self.pattern_plot)
        self.ui.ff_3d_plot_color_bar.addWidget(self.pattern_colorbar)
        self.add_polar_grid(radius=50, radial_steps=5, angular_steps=24)
        axes = Axes3D(size=1)
        axes.scale(50, 50, 50)
        self.pattern_plot.addItem(axes)
    
    def setup_ff_uv_plot(self):
        self.uv_widget = pg.GraphicsLayoutWidget()
        self.uv_widget.setBackground('k')
        self.ui.ff_uv_plot.addWidget(self.uv_widget)
        self.uv_plot = self.uv_widget.addPlot(title="Total E-Field (UV Projection)", color='w')
        # Set the title with color and size
        self.uv_plot.setTitle("Total E-Field (UV Projection)", color='w', size='14pt')  
        self.uv_plot.getAxis('bottom').setPen('w')
        self.uv_plot.getAxis('left').setPen('w')
        self.uv_plot.getAxis('bottom').setTextPen('w')
        self.uv_plot.getAxis('left').setTextPen('w')
        self.uv_plot.setLabel('bottom', 'U')
        self.uv_plot.setLabel('left', 'V')
        self.uv_plot.setAspectLocked(True)
        self.uv_plot.showGrid(x=True, y=True, alpha=0.5)

    def setup_ff_cut_1_plot(self):
        self.cut1_plot_widget = pg.PlotWidget(title="Phi = 0° Cut")
        self.cut1_plot_widget.setBackground('w')
        self.cut1_plot_widget.setLabel('bottom', 'Theta', units='degrees')
        self.cut1_plot_widget.setLabel('left', 'Gain', units='dB')
        self.cut1_plot_widget.setYRange(-40, 0)
        self.cut1_plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.ui.ff_cut1_plot.addWidget(self.cut1_plot_widget)

    def setup_ff_cut_2_plot(self):
        self.cut2_plot_widget = pg.PlotWidget(title="Phi = 90° Cut")
        self.cut2_plot_widget.setBackground('w')
        self.cut2_plot_widget.setLabel('bottom', 'Theta', units='degrees')
        self.cut2_plot_widget.setLabel('left', 'Gain', units='dB')
        self.cut2_plot_widget.setYRange(-40, 0)
        self.cut2_plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.ui.ff_cut2_plot.addWidget(self.cut2_plot_widget)

    def update_ff_3d_plot(self, data: FFData):
        try:
            e_total = np.sqrt(np.abs(data.e_theta)**2 + np.abs(data.e_phi)**2)
            e_total = np.nan_to_num(e_total, nan=1e-15)
            e_db = 20 * np.log10(e_total + 1e-15)
            self.db_max = np.max(e_db)
            self.db_min = self.db_max - self.pattern_color_dynamic
            r_plot = np.clip(e_db, self.db_min, self.db_max)
            r_plot = r_plot - self.db_min 
            theta = data.meshgrid[0]
            phi = data.meshgrid[1]
            z = r_plot * np.cos(theta)
            x = r_plot * np.sin(theta) * np.cos(phi)
            y = r_plot * np.sin(theta) * np.sin(phi)
            rows, cols = x.shape
            verts = np.stack([x.flatten(), y.flatten(), z.flatten()], axis=-1).astype(np.float32)
            faces = []
            for r in range(rows - 1):
                for c in range(cols - 1):
                    i = r * cols + c
                    faces.append([i, i + 1, i + cols])
                    faces.append([i + 1, i + cols + 1, i + cols])
            faces = np.array(faces)
            norm_values = (r_plot.flatten() - 0) / (self.db_max - self.db_min)
            colors = self.pattern_cmap.map(norm_values, mode='float') # Returns (N, 4) in 0.0-1.0 range
            md = gl.MeshData(vertexes=verts, faces=faces, vertexColors=colors)
            pattern_mesh = gl.GLMeshItem(
                meshdata=md, 
                smooth=True, 
                glOptions='opaque'
            )
            self.ff_3d_plot_mesh = pattern_mesh
            self.pattern_plot.addItem(self.ff_3d_plot_mesh)
            self.setup_colorbar()
        except Exception as e:
            log.error(e)
        
    def update_ff_uv_plot(self, data: FFData):
        e_total = np.sqrt(np.abs(data.e_theta)**2 + np.abs(data.e_phi)**2)
        e_total = np.nan_to_num(e_total, nan=1e-15)
        e_db = 20 * np.log10(e_total + 1e-15)
        db_max = np.max(e_db)
        e_plot = np.clip(e_db - db_max, -self.pattern_color_dynamic, 0)
        z_data = e_plot[:-1, :-1]
        theta = data.meshgrid[0]
        phi = data.meshgrid[1]
        u = np.sin(theta) * np.cos(phi)
        v = np.sin(theta) * np.sin(phi)
        u = np.nan_to_num(u, nan=0.0)
        v = np.nan_to_num(v, nan=0.0)
        self.ff_uv_mesh = pg.PColorMeshItem(u, v, z_data, shading='flat', antialias=True)
        self.ff_uv_mesh.setColorMap(self.pattern_cmap)
        self.ff_uv_mesh.setLevels([-self.pattern_color_dynamic, 0])
        self.uv_plot.addItem(self.ff_uv_mesh)

    def update_cut_1_plot(self, data: FFData):
        e_total = np.sqrt(np.abs(data.e_theta)**2 + np.abs(data.e_phi)**2)
        e_db = 20 * np.log10(e_total + 1e-15)
        e_db -= np.nanmax(e_db)
        u_grid = np.sin(data.meshgrid[0]) * np.cos(data.meshgrid[1])
        v_grid = np.sin(data.meshgrid[0]) * np.sin(data.meshgrid[1])
        mid_col = v_grid.shape[1] // 2
        v_slice = v_grid[:, mid_col]
        row_idx = np.nanargmin(np.abs(v_slice - 0.0))
        u_row = u_grid[row_idx, :]
        gain_row = e_db[row_idx, :]
        theta_signed = np.degrees(np.arcsin(np.clip(u_row, -1, 1)))
        mask = ~np.isnan(theta_signed) & ~np.isnan(gain_row)
        plot_x = theta_signed[mask]
        plot_y = gain_row[mask]
        sort_idx = np.argsort(plot_x)
        self.cut1_plot_widget.clear()
        self.cut1_plot_widget.plot(
            plot_x[sort_idx], 
            plot_y[sort_idx], 
            pen=pg.mkPen('b', width=2), 
            antialias=True
        )
        self.cut1_plot_widget.setXRange(-90, 90)
        self.cut1_plot_widget.setYRange(-40, 0)

    def update_cut_2_plot(self, data: FFData):
    # 1. Calculate Magnitude and dB
        e_total = np.sqrt(np.abs(data.e_theta)**2 + np.abs(data.e_phi)**2)
        e_db = 20 * np.log10(e_total + 1e-15)
        e_db -= np.nanmax(e_db) # Normalize to 0 dB peak
        
        # 2. Extract Coordinate Grids
        # u typically varies with columns (horizontal), v with rows (vertical)
        u_grid = np.sin(data.meshgrid[0]) * np.cos(data.meshgrid[1])
        v_grid = np.sin(data.meshgrid[0]) * np.sin(data.meshgrid[1])

        # 3. Find the Column where u = 0 (The Vertical Cut)
        # We look at the middle row to find which column has u closest to 0
        mid_row_idx = u_grid.shape[0] // 2
        u_horizontal_slice = u_grid[mid_row_idx, :]
        col_idx = np.nanargmin(np.abs(u_horizontal_slice - 0.0))
        
        # 4. Extract the COLUMN Slices
        # We take the data across all rows for that specific column
        v_col = v_grid[:, col_idx]
        gain_col = e_db[:, col_idx]
        
        # 5. Calculate Signed Theta (-90 to +90)
        # In the phi=90 plane, v = sin(theta), so theta = arcsin(v)
        theta_signed = np.degrees(np.arcsin(np.clip(v_col, -1, 1)))
        
        # 6. Clean and Sort
        # Remove NaNs (corners of the UV square)
        mask = ~np.isnan(theta_signed) & ~np.isnan(gain_col)
        plot_x = theta_signed[mask]
        plot_y = gain_col[mask]
        
        # Sort indices so the line draws correctly from left (-90) to right (+90)
        sort_idx = np.argsort(plot_x)
        
        # 7. Update Plot Widget
        self.cut2_plot_widget.clear()
        self.cut2_plot_widget.plot(
            plot_x[sort_idx], 
            plot_y[sort_idx], 
            pen=pg.mkPen('r', width=2), # Red pen for Phi=90
            antialias=True
        )
        
        # Set standard axis ranges
        self.cut2_plot_widget.setLabel('bottom', 'Theta (Phi=90°)', units='deg')
        self.cut2_plot_widget.setXRange(-90, 90)
        self.cut2_plot_widget.setYRange(-40, 0)
    
    def load_plots_config(self, text: str):
        style = self.ff_plot_styles.get(text)
        style()
    
    def clear_layout(self, layout: QVBoxLayout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
            else:
                sub = item.layout()
                if sub is not None:
                    self.clear_layout(sub)
    

    def add_polar_grid(self, radius=40, radial_steps=4, angular_steps=12):
        """
        Creates a circular polar grid on the XY plane.
        radius: Max radius of the grid
        radial_steps: Number of concentric circles
        angular_steps: Number of radial spokes (12 = every 30 degrees)
        """
        grid_color = (255, 255, 255, 50) # Faint white (RGBA)

        # 1. Create Concentric Circles
        for i in range(1, radial_steps + 1):
            r = (radius / radial_steps) * i
            # Generate points for a circle
            theta = np.linspace(0, 2 * np.pi, 100)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = np.zeros_like(x)
            
            pts = np.stack([x, y, z], axis=-1)
            circle = gl.GLLinePlotItem(pos=pts, color=grid_color, antialias=True)
            self.pattern_plot.addItem(circle)

        # 2. Create Radial "Spoke" Lines
        for i in range(angular_steps):
            angle = (2 * np.pi / angular_steps) * i
            x = np.array([0, radius * np.cos(angle)])
            y = np.array([0, radius * np.sin(angle)])
            z = np.array([0, 0])
            
            pts = np.stack([x, y, z], axis=-1)
            spoke = gl.GLLinePlotItem(pos=pts, color=grid_color, antialias=True)
            self.pattern_plot.addItem(spoke)
        
    def setup_colorbar(self):
        self.pattern_colorbar.clear()
        lut = self.pattern_cmap.getLookupTable(0.0, 1.0, 256)
        self.bar_axis = pg.AxisItem(orientation='right')
        label_style = {
            'color': '#FFFFFF', 
            'font-size': '16pt', # Set your title size here
        }
        self.bar_axis.setLabel("Relative Gain (dB)",**label_style)
        self.bar_axis.setPen('w')
        self.bar_axis.setTextPen('w')
        self.bar_img = pg.ImageItem()
        bar_data = np.linspace(0, 1, 256).reshape(1, 256)
        self.bar_img.setImage(bar_data)
        self.bar_img.setLookupTable(lut)
        self.bar_img.setRect(QtCore.QRectF(0, -self.pattern_color_dynamic, 1, self.pattern_color_dynamic))
        self.bar_vb = self.pattern_colorbar.addViewBox(row=0, col=0)
        self.bar_vb.setFixedWidth(40)
        self.bar_vb.addItem(self.bar_img)
        self.bar_vb.setYRange(-self.pattern_color_dynamic, 0, padding=0)
        self.pattern_colorbar.addItem(self.bar_axis, row=0, col=1)
        self.bar_axis.linkToView(self.bar_vb)
        self.pattern_colorbar.setBackground('k')

    def update_colorbar_limits(self, db_min, db_max):
        """Update the axis numbers when the data changes"""
        # This maps the 0-256 image pixels to your actual dB range
        self.bar_axis.setScale((db_max - db_min) / 256)
        self.bar_axis.setOffset(db_min)

class Axes3D(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, size=1.2):
        super().__init__()
        self.size = size
        self.color_x = (0.85, 0.1, 0.1, 1.0)
        self.color_y = (0.1, 0.6, 0.1, 1.0)
        self.color_z = (0.1, 0.1, 0.9, 1.0)
    def paint(self):
        gl_lib.glLineWidth(3.0)
        gl_lib.glBegin(gl_lib.GL_LINES)
        gl_lib.glColor4f(*self.color_x); gl_lib.glVertex3f(0,0,0); gl_lib.glVertex3f(self.size,0,0)
        gl_lib.glColor4f(*self.color_y); gl_lib.glVertex3f(0,0,0); gl_lib.glVertex3f(0,self.size,0)
        gl_lib.glColor4f(*self.color_z); gl_lib.glVertex3f(0,0,0); gl_lib.glVertex3f(0,0,self.size)
        gl_lib.glEnd()

def array_factor_rect(Nx=16, Ny=16, dx=0.5, dy=0.5,
                      theta0_deg=20.0, phi0_deg=30.0,
                      window="hann",
                      n_theta=120, n_phi=240,
                      upper_hemisphere_only=True):
    """
    AF for Nx x Ny array; spacings dx,dy in wavelengths. Returns TH, PH, AF_mag (linear, max=1).
    If upper_hemisphere_only=True, theta spans [0, pi/2] (z>0).
    """
    k0 = 2.0 * np.pi  # spacings in wavelengths => k0=2π

    th0 = np.deg2rad(theta0_deg)
    ph0 = np.deg2rad(phi0_deg)
    sx0 = np.sin(th0) * np.cos(ph0)
    sy0 = np.sin(th0) * np.sin(ph0)

    mx = np.arange(Nx) - (Nx - 1) / 2.0
    my = np.arange(Ny) - (Ny - 1) / 2.0
    x = mx * dx
    y = my * dy

    if not window:
        wx = np.ones(Nx); wy = np.ones(Ny)
    else:
        w = window.lower()
        wx = np.hanning(Nx) if w == "hann" else (np.hamming(Nx) if w == "hamming" else np.ones(Nx))
        wy = np.hanning(Ny) if w == "hann" else (np.hamming(Ny) if w == "hamming" else np.ones(Ny))
    w2d = np.outer(wx, wy)

    th_max = np.pi/2 if upper_hemisphere_only else np.pi
    theta = np.linspace(0.0, th_max, n_theta, endpoint=True)
    phi   = np.linspace(0.0, 2*np.pi, n_phi, endpoint=True)
    TH, PH = np.meshgrid(theta, phi, indexing="ij")

    sx = np.sin(TH) * np.cos(PH)
    sy = np.sin(TH) * np.sin(PH)

    # phase factors (vectorized)
    P = sx.size
    phase_x = np.exp(1j * k0 * np.outer(x, (sx - sx0).ravel()))  # (Nx, P)
    phase_y = np.exp(1j * k0 * np.outer(y, (sy - sy0).ravel()))  # (Ny, P)
    AF = (phase_x[:, None, :] * phase_y[None, :, :]) * w2d[:, :, None]
    AF = AF.sum(axis=(0,1)).reshape(TH.shape)

    AF_mag = np.abs(AF).astype(np.float64)   # use double precision
    AF_mag /= AF_mag.max() + 1e-15
    AF_dB = 20.0 * np.log10(AF_mag)

    # Set a floor (avoid crazy -240 dB artifacts)
    AF_dB = np.maximum(AF_dB, -120.0)


    return TH, PH, AF_dB