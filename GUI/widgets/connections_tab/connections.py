__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import os
import logging
import pyvisa
import re
import subprocess
import yaml

from serial.tools import list_ports
from PySide6.QtWidgets import QWidget, QHeaderView, QPushButton, QLabel, QAbstractItemView, QTableWidgetItem, QLineEdit
from PySide6.QtGui import  QIcon, QMovie
from PySide6.QtCore import Qt, QSize, QThread, QObject, Signal, QSettings, Slot
from .ui_connections import Ui_connections
from src.Devices.Devices import Devices
from .Device_selector.Device_selector import DeviceSelector
from src.Utils.config_files.measure_config import DEV_ROW, MEASURE_MODE_MAP, UNITS_MAP, RARM_DATA, Priority, State

image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../images"))
log = logging.getLogger(__name__)

class Connections(QWidget):

    connectRequested = Signal(str, str, str) # passing dev_label, dev_model, dev_address
    disconnectRequested = Signal(str)        # passing dev_label

    def __init__(self):
        self.devices = Devices()
        super().__init__()
        self.ui = Ui_connections()
        self.ui.setupUi(self)
        self.populate_table()
        self.restore_table_state()
        self.ui.connect_all_btn.clicked.connect(self.connect_all_devices)
        self.ui.tableWidget.setColumnWidth(0, 300)
        self.ui.tableWidget.setColumnWidth(1, 300)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)             
        self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self._active_jobs = 0 
        self._threads = []
        self.device_sel = None
        self.label = None

        log.debug("Loaded Connections tab.")


    def populate_table(self):
        devices = self.available_devices()
        for row in range(self.ui.tableWidget.rowCount()):
            self.device_sel = DeviceSelector(devices, self.ui.tableWidget, row)
            self.ui.tableWidget.setCellWidget(row, 0, self.device_sel)

            dev_label = QLineEdit("")
            self.ui.tableWidget.setCellWidget(row, 1, dev_label)

            icon_label = QLabel()
            icon_path = os.path.join(image_dir, "question-sign.png")
            icon = QIcon(icon_path)
            pixmap = icon.pixmap(QSize(20, 20))
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignCenter)
            self.ui.tableWidget.setCellWidget(row, 2, icon_label)

            button = QPushButton()
            icon_path = os.path.join(image_dir, "link.png")
            button.setIcon(QIcon(icon_path))
            button.clicked.connect(lambda _, r=row: self.connect_device(r))
            self.ui.tableWidget.setCellWidget(row, 3, button)

            button = QPushButton()
            icon_path = os.path.join(image_dir, "disconnect.png")
            button.setIcon(QIcon(icon_path))
            button.clicked.connect(lambda _, r=row: self.disconnect_device(r))
            self.ui.tableWidget.setCellWidget(row, 4, button)
            button.setEnabled(False)

    def connect_all_devices(self):
        # avoid launching empty rows
        launched = 0
        for row in range(self.ui.tableWidget.rowCount()):
            selector = self.ui.tableWidget.cellWidget(row, 0)
            address = selector.get_value() 
            if address:  # only launch if we have an address
                self.connect_device(row)
                launched += 1
        if launched:
            self.ui.connect_all_btn.setEnabled(False) 

    def get_tic_devices(self):
        output = subprocess.check_output(["ticcmd", "--list"], text=True)
        data = yaml.safe_load(output)

        if isinstance(data, str):
            # Dopasuj: 8 cyfr + przecinek + dowolna liczba znaków (do kolejnych 8 cyfr lub końca)
            matches = re.findall(r"(\d{8}),\s+(.*?)(?=\d{8},|$)", data)
            devices = [{"serial": serial.strip(), "name": name.strip()} for serial, name in matches]
            return devices

        elif isinstance(data, list):
            devices = []
            for line in data:
                parts = line.split(",", 1)
                if len(parts) == 2:
                    devices.append({"serial": parts[0].strip(), "name": parts[1].strip()})
            return devices
        return []

    def available_devices(self):
        devices = []
        # --- VNA ---
        try:
            rm = pyvisa.ResourceManager()
            for resource in rm.list_resources():
                try:
                    idn = rm.open_resource(resource).query("*IDN?").strip()
                    label = f"{resource} → {idn}"
                except Exception:
                    label = f"{resource} → [Unknown]"
                devices.append((resource, idn))
        except Exception as e:
            log.error(("[VISA error]", str(e)))

        # --- serial ---
        try:
            for port in list_ports.comports():
                devices.append((port.device, port.description))
        except Exception as e:
            log.error(("[Serial error]", str(e)))

        # --- TIC ---
        try:
            devs = self.get_tic_devices()
            serial_nums = [d['serial'] for d in devs]
            names = [d['name'] for d in devs]
            for sn, label in zip(serial_nums, names):
                devices.append((sn, f"#{sn} → {label}"))
                log.debug(f"_available devices sn {sn}")
        except Exception as e:
            log.error(("[Serial error]", str(e)))
        
        # --- Robotic Arm ---
        devices.append((RARM_DATA["IP"], RARM_DATA["LBL"]))
        return devices
    
    @Slot(int)
    def connect_device(self, row: int):
        btn = self.ui.tableWidget.cellWidget(row, 3)
        if isinstance(btn, QPushButton):
            btn.setEnabled(False)
        self.start_loading(row)
        dev_name = self.ui.tableWidget.verticalHeaderItem(row).text()
        dev_model = self.ui.tableWidget.cellWidget(row, 1).text()
        dev_address = self.ui.tableWidget.cellWidget(row, 0).get_value()
        self.connectRequested.emit(dev_name, dev_model, dev_address)

    @Slot(str, bool)
    def handle_connect_resp(self, dev_label:str, resp:bool):
        row = DEV_ROW[dev_label]
        label = self.ui.tableWidget.cellWidget(row, 2)
        if isinstance(label, QLabel) and hasattr(label, "_movie"):
            label._movie.stop()
            del label._movie
        if resp:
            icon_path = os.path.join(image_dir, "green_mark.png")
            self.ui.tableWidget.cellWidget(row, 4).setEnabled(True)
        else:
            icon_path = os.path.join(image_dir, "red_cross.png")
            self.ui.tableWidget.cellWidget(row, 3).setEnabled(True)
        icon = QIcon(icon_path)
        label.setPixmap(icon.pixmap(QSize(20, 20)))
        label.setAlignment(Qt.AlignCenter)

    @Slot(int)
    def disconnect_device(self, row: int):
        btn = self.ui.tableWidget.cellWidget(row, 4)
        if isinstance(btn, QPushButton):
            btn.setEnabled(False)
        self.start_loading(row)
        dev_name = self.ui.tableWidget.verticalHeaderItem(row).text()
        address = self.ui.tableWidget.cellWidget(row, 0).get_value()
        label = self.ui.tableWidget.cellWidget(row, 1).text()
        self.disconnectRequested.emit(dev_name)

    @Slot(str, bool)
    def handle_disconnect_resp(self, dev_label:str, resp:bool):
        row = DEV_ROW[dev_label]
        label = self.ui.tableWidget.cellWidget(row, 2)
        if isinstance(label, QLabel) and hasattr(label, "_movie"):
            label._movie.stop()
            del label._movie
        icon_path = os.path.join(image_dir, "question-sign.png")        
        icon = QIcon(icon_path)
        label.setPixmap(icon.pixmap(QSize(20, 20)))
        label.setAlignment(Qt.AlignCenter)
        self.ui.tableWidget.cellWidget(row, 3).setEnabled(True)

    def start_loading(self, row: int):
        label = self.ui.tableWidget.cellWidget(row, 2)
        if not isinstance(label, QLabel):
            label = QLabel()
            label.setAlignment(Qt.AlignCenter)
            self.ui.tableWidget.setCellWidget(row, 2, label)

        movie = QMovie(os.path.join(image_dir, "loading_spin.gif"))
        movie.setScaledSize(QSize(20, 20))
        label.setMovie(movie)
        movie.start()
        label._movie = movie

    def print_devices(self):
        log.debug("=== Devices ===")
        for dev_type, by_addr in getattr(self.devices, "_devices", {}).items():
            for addr, dev in by_addr.items():
                log.debug(f"- {dev_type} @ {addr}: {dev!r}")

    def save_table_state(self):
        settings = QSettings("Microamp", "GUI")
        settings.beginGroup("ConnectionsTable")
            # save addresses per row (keyed by row header text; fallback to row index)
        for row in range(self.ui.tableWidget.rowCount()):
            header_item = self.ui.tableWidget.verticalHeaderItem(row)
            key = header_item.text() if header_item else f"row_{row}"

            selector = self.ui.tableWidget.cellWidget(row, 0)
            sel_value = selector.get_value() if hasattr(selector, "get_value") else ""

            label_widget = self.ui.tableWidget.cellWidget(row, 1)
            label_value = label_widget.text() if label_widget else ""

            settings.setValue(f"rows/{key}/col0", sel_value)
            settings.setValue(f"rows/{key}/col1", label_value)
        
        settings.endGroup()

    def restore_table_state(self):
        settings = QSettings("Microamp", "GUI")
        settings.beginGroup("ConnectionsTable")

        for row in range(self.ui.tableWidget.rowCount()):
            header_item = self.ui.tableWidget.verticalHeaderItem(row)
            key = header_item.text() if header_item else f"row_{row}"

            sel_value = settings.value(f"rows/{key}/col0", "", type=str)
            selector = self.ui.tableWidget.cellWidget(row, 0)
            if hasattr(selector, "set_value"):
                selector.set_value(sel_value)
            elif hasattr(selector, "setText"):
                selector.setText(sel_value)

            label_value = settings.value(f"rows/{key}/col1", "", type=str)
            label_widget = self.ui.tableWidget.cellWidget(row, 1)
            label_widget.setText(label_value)
        
        settings.endGroup()

