__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

from enum import IntEnum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot, Signal, QThread, QObject

from .ui_FF_el import Ui_FF_el
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, Priority, State

import logging
log = logging.getLogger("GUI")

class FF_el(QWidget):

    controlRequest = Signal(str, str, int) # passing dev_label, client_id, priority level
    controlRelease = Signal(str, str, str) # passing dev_label, client_id, token
    command = Signal(str, str, dict)       # passing dev_label, client_id, dict of method + arguments

    def __init__(self, workers:dict, threads:dict, mediator:QObject, parent=None):
        super().__init__(parent)
        self.ui = Ui_FF_el()
        self.ui.setupUi(self)
        self.client_id = "FF_el"
        self._threads = threads
        self._workers = workers
        self._tokens = {}
        self.mediator = mediator
        self._devs = {
            "TIC_EL" : {"worker": self._workers.get("TIC_EL"), "control": False},
            "VNA" : {"worker": self._workers.get("VNA"), "control": False}
        }
        names = [name for name, obj in self._devs.items() if obj is not None]
        text = (", ".join(names) if names else "— none —")
        self.ui.label_dev_name.setText(text)
        self.ui.pause_btn.setEnabled(False)
        self.ui.start_btn.pressed.connect(self.Start)

    @Slot()
    def Start(self):
        self.controlRequest.emit("TIC_EL", self.client_id, Priority.Measurement)
        self.controlRequest.emit("VNA", self.client_id, Priority.Measurement)

    @Slot(str, str, str)
    def _on_granted(self, dev_label:str, client_id:str, token:str):
        if self.client_id != client_id: return
        if dev_label not in self._devs: return
        self._tokens[dev_label] = token
        self._devs[dev_label]["control"] = True
        if all(dev in self._tokens for dev in self._devs):
            log.debug("All devices locked. Starting measurement…")
            #self.parent.runSequence.emit()
            self.mediator.runSequence.emit("FF_el")

    @Slot(str)
    def release_all(self, client_id: str):
        if self.client_id != client_id: return
        self.controlRelease.emit("TIC_EL", self.client_id, self._tokens["TIC_EL"])
        self.controlRelease.emit("VNA", self.client_id, self._tokens["VNA"])

    def make_thread(self):
        log.debug(f"Creating thread for {self.client_id}...")
        #self.controller = FF_el_Controller()
        #thread = QThread()
        #thread.setObjectName("MEAS")
        #self.controller.moveToThread(thread)
        #thread.start()
        #self._threads["MEAS"] = thread
        #self._workers["MEAS"] = self.controller