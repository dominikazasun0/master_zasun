__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

from dataclasses import dataclass
from datetime import datetime
from typing import List
import numpy as np

@dataclass
class GeneralConfig:
    t_start: datetime
    devices: List[str]
    t_stop: datetime | None = None
    operator: str | None = None
    duration: float | None = None
    probe_ant: str | None = None

@dataclass
class MeasurementConfig:
    type: str
    distance: float | None = None

@dataclass
class VNAConfig:
    pwr_lvl: float
    freq_lst: list
    f_start: float
    f_stop: float
    n_freq: int
    s_param: str

@dataclass
class AUTConfig:
    aut_type: str | None = None
    ser_num: str | None = None
    comment: str | None = None

@dataclass
class PNFMeasurementConfig(MeasurementConfig):
    crosspolar: bool | None = None
    scan_mat: list | None = None
    d_x: float | None = None
    d_y: float | None = None
    cal_val: dict | None = None
    copolar_rotation: float | None = None

@dataclass
class PNFData:
    copolar: np.ndarray | None = None
    crosspolar: np.ndarray | None = None

@dataclass
class FFMeasurementConfig(MeasurementConfig):
    scan_lst: list | None = None
    step_deg: float | None = None

@dataclass
class FFData:
    frequency_hz: float               # In Hz
    meshgrid: np.ndarray = None       # Theta, Phi meshgrid
    e_theta: np.ndarray = None        # Values of E field in theta direction
    e_phi: np.ndarray = None          # Values of E field in phi direction

