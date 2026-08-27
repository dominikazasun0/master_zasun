__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
import numpy as np
from pathlib import Path
from typing import Callable, Dict, Optional, Union
from PySide6.QtCore import QObject, Signal, Slot, QTimer, QThread
from ..Utils.config_files.measure_config import SAVE_PATH
from ..Data_Processing import PWS, MoM, NF2FFData, FFData

log = logging.getLogger("GUI")

class DataProcessingWorker(QObject):

    response = Signal(str, dict)     # passing client_id, dict of method + arguments

    def __init__(self, dev_label:str):
        super().__init__()
        self.dev_label = dev_label
        self.transform_map = {
            "PWS" : PWS,
            "MoM" : MoM,
        }

    @Slot(str, str, dict)
    def command_interp(self, dev_label:str, client_id:str, command: dict):
        """
        Interpreter komend sterujących wysyłanych po sygnale Qt.
        """
        if self.dev_label != dev_label:
            return
        self.owner = client_id
        method = command.get("method")
        kwargs = command.get("kwargs", {})
        log.debug(f"command_interp self.dev_label: {self.dev_label} dev_label: {dev_label} client_id {client_id} method {method}")
        if not method:
            log.error("Missing 'method' in command payload")
            return
        fn = getattr(self, method, None)
        if not callable(fn):
            log.error(f"{self.dev_label}_worker has no method '{method}'")
            return
        try:
            fn(**kwargs)
        except TypeError as e:
            log.error(
                f"Argument mismatch when calling {method}: {e}\n"
                f"Provided kwargs: {kwargs}"
            )
        except Exception as e:
            log.exception(f"Error executing command '{method}': {e}")
    
    def nf2ff_transform(self, type:str, data: NF2FFData):
        transform_cls = self.transform_map.get(type)
        if transform_cls is None:
            print(f"Transform type '{type}' is not supported or not implemented.")
            return
        try:
            cls = transform_cls(data)
            self.response.emit(self.owner, {"method": "_on_nf2ff_trans_start",
                                            "kwargs": {}})
            result = cls.compute()
            if result is not None:
                self.response.emit(self.owner, {"method": "_on_nf2ff_trans_finish",
                                                "kwargs": {"result" : result}})
            else:
                self.response.emit(self.owner, {"method": "_on_nf2ff_trans_stop",
                                                "kwargs": {}})
        except Exception as e:
            log.error(e)
            self.response.emit(self.owner, {"method": "_on_nf2ff_trans_stop",
                                            "kwargs": {}})