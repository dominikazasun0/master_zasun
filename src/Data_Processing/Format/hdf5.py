__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
import h5py
import json
import numpy as np
from .base import FileFormat

log = logging.getLogger("GUI")

class HDF5Format(FileFormat):
    name = "hdf5"

    def write(self, path, payload: dict):
        with h5py.File(path, "w") as f:
            f.attrs["measurement_type"] = payload["measurement_type"]
            config_grp = f.create_group("config")
            for section, values in payload["config"].items():
                grp = config_grp.create_group(section)
                for k, v in values.items():
                    grp.attrs[k] = self.hdf5_safe(v)
            data_grp = f.create_group("data")
            for name, array in payload["data"].items():
                data_grp.create_dataset(name, data=array)

    def read(self, path) -> dict:
        payload = {"config": {}, "data": {}}
        with h5py.File(path, "r") as f:
            payload["measurement_type"] = f.attrs["measurement_type"]

            # Load config group
            for section, grp in f["config"].items():
                section_dict = {}
                for k, v in grp.attrs.items():
                    # Try to parse JSON strings back to original objects
                    try:
                        section_dict[k] = json.loads(v) if isinstance(v, str) else v
                    except json.JSONDecodeError:
                        section_dict[k] = v
                payload["config"][section] = section_dict

            # Load data group
            for name, ds in f["data"].items():
                payload["data"][name] = ds[()]

        return payload
    
    def peek_meas_type(self, path) -> str:
        with h5py.File(path, "r") as f:
            return f.attrs["measurement_type"]
    
    def hdf5_safe(self, v):
        if isinstance(v, (dict, list)):
            return json.dumps(v)
        elif isinstance(v, (int, float, str, bool)):
            return v
        elif isinstance(v, np.ndarray):
            return v
        elif v is None:
            return ""  # or np.nan for numbers
        else:
            return json.dumps(v.__dict__) if hasattr(v, "__dict__") else str(v)