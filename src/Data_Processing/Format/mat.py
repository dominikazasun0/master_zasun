__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
import numpy as np
from datetime import datetime
from scipy.io import loadmat, savemat
from .base import FileFormat

log = logging.getLogger("GUI")

class MATFormat(FileFormat):
    name = "mat"

    def write(self, path, payload: dict):
        mat_dict = self.mat_safe(payload)
        savemat(path, mat_dict, do_compression=True)

    def read(self, path) -> dict:
        mat = loadmat(path, squeeze_me=True, struct_as_record=False)

        payload = {
            "measurement_type": self._decode_scalar(mat["measurement_type"]),
            "config": self._decode_struct(mat["config"]),
            "data": self._decode_struct(mat["data"]),
        }
        return payload

    def peek_meas_type(self, path) -> str:
        mat = loadmat(path, variable_names=["measurement_type"], squeeze_me=True)
        return self._decode_scalar(mat["measurement_type"])
    
    def _encode_struct(self, d: dict) -> dict:
        """
        Convert nested dicts into something savemat understands.
        """
        encoded = {}
        for k, v in d.items():
            if isinstance(v, dict):
                encoded[k] = self._encode_struct(v)
            elif isinstance(v, (list, tuple)):
                encoded[k] = np.array(v)
            else:
                encoded[k] = v
        return encoded

    def _decode_struct(self, obj) -> dict:
        """
        Convert MATLAB struct back into a Python dict.
        """
        if hasattr(obj, "__dict__"):
            return {
                k: self._decode_struct(v)
                for k, v in obj.__dict__.items()
                if not k.startswith("_")
            }
        elif isinstance(obj, np.ndarray) and obj.dtype == object:
            return [self._decode_struct(x) for x in obj]
        else:
            return obj

    def _decode_scalar(self, value):
        if isinstance(value, np.ndarray):
            return value.item()
        return value
    
    def mat_safe(self,v):
        import numpy as np
        if isinstance(v, (dict, list)):
            # recursively convert
            if isinstance(v, dict):
                return {k: self.mat_safe(val) for k, val in v.items()}
            else:
                return [self.mat_safe(x) for x in v]
        elif isinstance(v, datetime):
            return v.isoformat()  # "2026-01-23T16:10:15.460735"
        elif isinstance(v, (int, float, str, bool)):
            return v
        elif isinstance(v, np.ndarray):
            if v.dtype == object:
                # convert each element
                return np.array([self.mat_safe(x) for x in v])
            return v
        elif v is None:
            return ""
        else:
            # fallback
            return str(v)