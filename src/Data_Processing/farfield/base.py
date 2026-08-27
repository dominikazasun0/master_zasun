__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Tuple, Optional
from src.Data_Processing.measurement.config import FFData

class FF(ABC):
    C0 = 299792458.0          # Speed of light (m/s)
    MU0 = 4 * np.pi * 1e-7    # Permeability of free space
    EPS0 = 8.854187e-12       # Permittivity of free space
    ETA0 = 376.73             # Intrinsic impedance of vacuum (~120π)

    def __init__(self, farfield: FFData):
        self.farfield = farfield

    @abstractmethod
    def compute(self):
        pass