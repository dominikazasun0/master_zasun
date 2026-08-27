__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import numpy as np
from dataclasses import asdict
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Tuple, Optional
from src.Data_Processing.measurement.config import FFData

@dataclass
class NF2FFData:
    frequency_hz: float               # In Hz 
    distance_mm: float                # Probe-to-AUT distance
    sampling: Tuple[float, float]     # (dx, dy) in mm or (d_theta, d_phi) in deg
    copolar_data: np.ndarray          # Data of copolar polarization
    coordinates: np.ndarray           # X, Y or Theta, Phi
    copolar_rotation: float           # Copolar axis rotation angle in deg (0-90)
    cross_pol: bool = False           # True if crosspolar is to be included
    crosspolar_data: Optional[np.ndarray] = None
    probe_correction: Optional[np.ndarray] = None
    base_2: bool = False              # zero-pad (if needed) for computation efficiency

class NF2FF(ABC):
    C0 = 299792458.0          # Speed of light (m/s)
    MU0 = 4 * np.pi * 1e-7    # Permeability of free space
    EPS0 = 8.854187e-12       # Permittivity of free space
    ETA0 = 376.73             # Intrinsic impedance of vacuum (~120π)
    ff_result : FFData | None = None

    def __init__(self, nearfield: NF2FFData):
        self.nf = nearfield
        self.lambda_m = self.C0 / self.nf.frequency_hz
        self.k = 2 * np.pi / self.lambda_m

    @property
    def name(self) -> str:
        return "NF2FF"
    
    def serialize(self) -> dict:
        return {
            "measurement_type": self.name,
            "config": {
                "frequency_hz": self.nf.frequency_hz,
                "sampling": self.nf.sampling,
                "copolar_data": self.nf.copolar_data,
                "coordinates": self.nf.coordinates,
                "copolar_rotation": self.nf.copolar_rotation,
                "cross_pol": self.nf.cross_pol,
                "crosspolar_data": self.nf.crosspolar_data,
                "probe_correction": self.nf.probe_correction,
                "base_2": self.nf.base_2,
            },
            "data": {
                "meshgrid": self.ff_result.meshgrid,
                "e_theta": self.ff_result.e_theta,
                "e_phi": self.ff_result.e_phi
            },
        }
    