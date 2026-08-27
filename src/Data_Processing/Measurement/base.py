__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
from abc import ABC, abstractmethod
from .config import GeneralConfig, MeasurementConfig, VNAConfig, AUTConfig

log = logging.getLogger("GUI")

class MeasurementType(ABC):
    def __init__(
        self,
        general: GeneralConfig,
        measurement: MeasurementConfig,
        vna: VNAConfig,
        aut: AUTConfig
    ):
        self.general = general
        self.measurement = measurement
        self.vna = vna
        self.aut = aut
        self.data = None

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def parse(self, raw_data):
        pass
    @abstractmethod
    def serialize_config(self) -> dict:
        """Return all configs as a nested dict"""
    
    @abstractmethod
    def serialize(self) -> dict:
        """domain → serializable dict"""

    @classmethod
    @abstractmethod
    def from_serialized(cls, payload: dict):
        """rebuild object from serialized data"""