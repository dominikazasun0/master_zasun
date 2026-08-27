
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QMetaObject, Slot, QTimer, Signal, QThread, QObject
from PySide6.QtGui import QStandardItemModel, QStandardItem, QVector3D, QLinearGradient, QColor
from PySide6.QtDataVisualization import (
    Q3DSurface,
    QSurfaceDataProxy,
    QSurface3DSeries,
    QSurfaceDataItem, Q3DCamera, Q3DTheme,
)
import pyqtgraph as pg
from .ui_FF_az import Ui_FF_az
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, Priority, State
from typing import Dict, Any

import logging

log = logging.getLogger("GUI")

class FF_az(QWidget):
    controlRequest = Signal(str, str, int)  # passing dev_label, client_id, priority level
    controlRelease = Signal(str, str, str)  # passing dev_label, client_id, token
    command = Signal(str, str, dict)       # passing dev_label, client_id, dict of method + arguments

    def __init__(self, workers: dict, threads: dict, mediator: QObject, parent=None):
        super().__init__(parent)
        self.ui = Ui_FF_az()
        self.ui.setupUi(self)
        self.parent = parent
        self.dev_label = None
        self.client_id = "FF_az"
        self._threads = threads
        self._workers = workers
        self.worker = self._workers["MEAS"]
        self._tokens = {}
        self.mediator = mediator

        self._devs = {
            "TIC_AZ": {"worker": self._workers.get("TIC_AZ"), "control": False},
            "VNA": {"worker": self._workers.get("VNA"), "control": False}
        }
        #print(f"workers{workers}")
        #print(f"_devs{self._devs}")
        names = [name for name, dev in self._devs.items() if dev.get("worker") is not None]
        text = (", ".join(names) if names else "— none —")

        # maszyna stanów
        self.param_pending = {
            "freq": False,
            "step": False,
            "position": False,
            "data": False
        }

        # Dane wykresu
        # vna f, v
        self.f_data = []
        self.re_data = []
        self.im_data = []
        self.A_data_formatted = []
        self.B_data_formatted = []
        # positioner a
        self.a_data = []

        # dane bieżące tymczasowe
        # vna
        self.new_f = None
        self.new_re = None
        self.new_im = None
        # pozycjoner
        self.step_deg = 0.9
        self.new_a = None

        # Bufor danych
        self.view_a_data = []
        self.view_v_data = []
        self.max_measurements = 6

        self.target_z_min = 0
        self.target_z_max = 0
        self.current_z_min = 0
        self.current_z_max = 0

        self.z_animation_timer = QTimer()
        self.z_animation_timer.timeout.connect(self._animate_z_axis)


        # === Wykres 2D ===
        # layout in placeholder
        layout2d = QHBoxLayout(self.ui.plot2DWidgetPlaceholder)
        layout2d.setContentsMargins(0, 0, 0, 0)
        layout2d.setSpacing(0)
        # Widget wykresu
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', '[dB]')
        self.plot_widget.setLabel('bottom', f'Frequency []')
        #self.plot_widget.setLabel('bottom', f'Frequency [{units_map[3]}]')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setYRange(-100, -10)
        self.curve = self.plot_widget.plot(pen='b', symbol='o')
        layout2d.addWidget(self.plot_widget)

        # === Wykres 3D ===
        layout3d = QHBoxLayout(self.ui.plot3DWidgetPlaceholder)
        self.surface = Q3DSurface()
        self.surface_container = QWidget.createWindowContainer(self.surface, self.ui.plot3DWidgetPlaceholder)
        self.surface_container.setMinimumSize(550, 320)
        camera = self.surface.scene().activeCamera()
        # ustaw kąt (pitch, yaw, roll)
        camera.setCameraPosition(30.0, 10.0)
        # camera.setProjectionType(Q3DCamera.CameraProjection.Orthographic)
        layout3d.addWidget(self.surface_container)

        # Proxy danych
        self.data_proxy = QSurfaceDataProxy()
        self.series = QSurface3DSeries(self.data_proxy)
        self.series.setDrawMode(QSurface3DSeries.DrawSurface)
        # self.series.setDrawMode(QSurface3DSeries.DrawWireframe)
        self.series.setFlatShadingEnabled(False)
        # self.series.setFlatShadingEnabled(True)
        self.series.setMeshSmooth(False)
        self.surface.addSeries(self.series)
        gr = QLinearGradient()
        gr.setColorAt(0.0, Qt.black)
        gr.setColorAt(0.33, Qt.blue)
        gr.setColorAt(0.67, Qt.green)
        gr.setColorAt(0.84, Qt.yellow)
        gr.setColorAt(1.0, Qt.red)
        self.series.setBaseGradient(gr)
        self.series.setColorStyle(Q3DTheme.ColorStyleUniform)
        self.series.setBaseColor(Qt.white)
        self.series.setColorStyle(Q3DTheme.ColorStyleRangeGradient)
        # Ustawienia osi
        self.surface.axisX().setTitle("Measurement")
        self.surface.axisY().setTitle("[dB]")
        self.surface.axisZ().setTitle("position")
        self.surface.axisX().setLabelAutoRotation(45)
        self.surface.axisZ().setLabelAutoRotation(45)

    @Slot(str, str, str)
    def _on_granted(self, dev_label: str, client_id: str, token: str):
        if self.client_id != client_id:
            return
        if dev_label not in self._devs:
            return
        log.debug(f"granted token for {dev_label}")
        self._tokens[dev_label] = token
        self._devs[dev_label]["control"] = True
        if all(dev in self._tokens for dev in self._devs):
            log.debug("All devices locked. Starting measurement…")

    
    def _on_started(self):
        log.info("started!")
    
    def _on_finished(self):
        log.debug("Measurement can be saved.")

    def _on_paused(self):
        log.debug("Measurement paused.")
    
    def _on_resumed(self):
        log.debug("Measurement resumed.")

    @Slot(str)
    def release_all(self, client_id: str):
        if self.client_id != client_id:
            return

        log.debug(f"releaseALL from owner {client_id}")
        self.controlRelease.emit("TIC_AZ", self.client_id, self._tokens["TIC_AZ"])
        self.controlRelease.emit("VNA", self.client_id, self._tokens["VNA"])

    # Mediator.release -> controlRevoked
    @Slot(str, str)
    def done(self, dev_label: str, client_id: str):
        # jeśli nie "FF_az"
        if self.client_id != client_id:
            return
        # jeśli nie "TIC_AZ" lub "VNA"
        if dev_label not in self._devs:
            return

        log.debug(f"done {dev_label} client_id {client_id}")

        self._devs[dev_label]["control"] = False
        self._tokens.pop(dev_label, None)
        # jeśli oba False
        if not (self._devs["TIC_AZ"]["control"] or self._devs["VNA"]["control"]):
            self.command.emit("MEAS", "tabs/MEAS", {"method": "switch_on_off", "kwargs": {"on": False}})

    """ ----- interpreter ----- """
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
    """ ------------------------------------------------------- """

    @Slot(str)
    def _do_next_event(self, client_id):
        log.debug(f"{self.dev_label} _do_next_event for {client_id} ")


    @Slot(float, float)
    def _on_pos_step_acquired(self, start_pos, stop_pos, current_pos, step_deg):
        self.start_pos = start_pos
        self.stop_pos = stop_pos
        self.current_pos = current_pos
        self.step_deg = step_deg
        self.ui.start_posEntry.setText(str(start_pos * step_deg))
        #self.ui.stop_posEntry.setText(stop)
        self.ui.stepLabel.setText(f"step: {step_deg:.3f} [deg]")

        #log.debug(f"positions acquired: from {pos} to {stop} every {step_deg} deg")

    def _on_get_config(self, dev_label:str, dev_config:dict):
        match dev_label:
            case "VNA":
                self._on_freq_N_acquired(dev_config["f_start"],
                                         dev_config["f_stop"],
                                         dev_config["N"])
            case "TIC_AZ":
                self._on_pos_step_acquired(dev_config["start_pos"],
                                           dev_config["stop_pos"],
                                           dev_config["current_pos"],
                                           dev_config["step_deg"])
        self.parent._on_get_devs_config(dev_label)
    
    @Slot(float, float, int)
    def _on_freq_N_acquired(self, f_start, f_stop, N):
        self.f_data = np.linspace(f_start, f_stop, N)
        self.ui.freq_comboBox.clear()  # usuń stare elementy
        for f in self.f_data:
            label = f"{f/1e6:.3f} MHz"
            self.ui.freq_comboBox.addItem(label, userData=f)  # <-- attach real freq here
        log.debug(f"new_f acquired {self.f_data.shape} {self.f_data}")

        self.param_pending["freq"] = True
        self.try_update_plot()

    @Slot(np.ndarray, np.ndarray)
    def _on_data_acquired(self, re_data, im_data):
        self.new_re = re_data
        self.new_im = im_data
        log.debug(f"new_re acquired {self.new_re[10]}")

        self.param_pending["data"] = True
        self.try_update_plot()

    @Slot(float)
    def _on_position_acquired(self, pos):
        self.new_a = pos * self.step_deg
        self.ui.current_posLabel.setText(f"current: {self.new_a :.2f}")
        log.debug(f"new_a acquired {self.new_a}")

        self.param_pending["position"] = True
        self.try_update_plot()

    @Slot(bool)
    def _on_meas_prepare(self, status:bool):
        log.info(f"Measurement prepare status: {status}")

    @Slot(float, float)
    def handle_step_acquired(self, step_deg):
        self.step_deg = step_deg
        #self.ui.stop_posEntry.setText(stop)
        self.ui.stepLabel.setText(f"step: {step_deg:.3f} [deg]")

        self.param_pending["step"] = True
        self.try_update_plot()

    def try_update_plot(self):
        #if all(self.param_pending.values()):
        if self.new_a is not None and self.new_re is not None and self.new_im is not None:
            self.a_data.append(self.new_a)
            self.re_data.append(self.new_re)
            self.im_data.append(self.new_im)

            # amplituda i faza
            amp_db = 20 * np.log10(np.sqrt(np.pow(self.new_re, 2) + np.pow(self.new_im, 2)))
            phase = np.degrees(np.arctan2(self.new_im, self.new_re))

            self.A_data_formatted.append(amp_db)
            self.B_data_formatted.append(phase)

            self.view_a_data.append( self.new_a )
            self.view_v_data.append(list(map(float, amp_db)))

            if len(self.view_v_data) > self.max_measurements:
                self.view_a_data.pop(0)
                self.view_v_data.pop(0)

            log.debug(f"view_a_data {len(self.view_a_data)}")
            #log.debug(f"re_data {len(self.re_data)} {self.re_data[0].shape}")
            #log.debug(f"im_data {len(self.im_data)} {self.im_data[0].shape}")
            log.debug(f"A_data_formatted {len(self.A_data_formatted)} {self.A_data_formatted[0].shape}")
            #log.debug(f"Added measurement #{len(self.measurements)}")

            # jedna częstotliwość
            # amplituda
            real = [re[20] for re in self.re_data]
            imag = [im[20] for im in self.im_data]
            values = 20 * np.log10( np.sqrt(np.pow(real,2) + np.pow(imag,2)) )

            #values = [v[20] for v in self.A_data_formatted]
            self.curve.setData(self.a_data, values, symbol='o')
            self._update_3d_plot()

            self.param_pending["position"] = False
            self.param_pending["data"] = False
            self.new_a = None
            self.new_re = None
            self.new_im = None

    def _update_3d_plot(self):
        """Aktualizuje 3D wykres na podstawie nowych danych pomiarowych."""

        num_rows = len(self.view_a_data)  # liczba pomiarów
        if num_rows == 0:
            return
        num_cols = len(self.f_data)  # liczba punktów w jednym pomiarze
        log.debug(f"Added measurement num_rows ={num_rows} num_cols ={num_cols}")

        # lista list QSurfaceDataItem
        data_array = []

        for i in range(num_rows):
            row = []
            log.debug(f"i = {i} view_a_data[{i}] = {(self.view_a_data[i])}")
            a_val = float(self.view_a_data[i])  # np. pozycja anteny albo numer pomiaru
            #log.debug(f"Z row {i} -> a_val={self.view_a_data[i]}")
            for j in range(num_cols):
                f_val = float((self.f_data[j])/1e9)
                v_val = float(self.view_v_data[i][j])
                row.append(QSurfaceDataItem(QVector3D(f_val, v_val, a_val)))

            data_array.append(row)

        log.debug(f"row_count {self.data_proxy.rowCount()}")
        # aktualizacja wykresu
        log.debug(f"axisZ range before reset: {self.surface.axisZ().min()} - {self.surface.axisZ().max()}")
        self.data_proxy.resetArray(data_array)
        log.debug(f"row_count {self.data_proxy.rowCount()}")

        self.surface.axisX().setRange(self.f_data[0]/1e9, self.f_data[-1]/1e9)
        self.surface.axisX().setAutoAdjustRange(True)
        self.surface.axisX().setSegmentCount(10)

        self.surface.axisY().setRange(-100, -10)
        self.surface.axisY().setAutoAdjustRange(True)
        self.surface.axisY().setSegmentCount(10)

        self.surface.axisZ().setLabelAutoRotation(90)
        self.surface.axisZ().setLabelFormat("%.1f")
        self.surface.axisZ().setSegmentCount(self.max_measurements)

        z_window = self.max_measurements-1
        if num_rows > z_window:
            self.target_z_min = self.view_a_data[-z_window]
            self.target_z_max = self.view_a_data[-1]
        else:
            self.target_z_min = self.view_a_data[0]
            self.target_z_max = self.view_a_data[-1]



    def _animate_z_axis(self):
        """Płynne przesuwanie osi Z w stronę target range."""
        # Odczytaj bieżący zakres
        current_min = self.surface.axisZ().min()
        current_max = self.surface.axisZ().max()

        # Oblicz krok przesunięcia
        alpha = 0.2  # im mniejszy, tym wolniejsze przesuwanie
        new_min = current_min + alpha * (self.target_z_min - current_min)
        new_max = current_max + alpha * (self.target_z_max - current_max)

        # Zaktualizuj wykres
        self.surface.axisZ().setRange(new_min, new_max)

