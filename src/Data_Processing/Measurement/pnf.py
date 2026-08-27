__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
import numpy as np
from dataclasses import asdict
from . import MeasurementType, GeneralConfig, PNFMeasurementConfig, VNAConfig, AUTConfig, PNFData

log = logging.getLogger("GUI")

class PNFMeasurement(MeasurementType):
    def __init__(
        self,
        general: GeneralConfig,
        measurement: PNFMeasurementConfig,
        vna: VNAConfig,
        aut: AUTConfig,
        data: PNFData | None = None
    ):
        super().__init__(general, measurement, vna, aut)
        self.data = data

    @property
    def name(self) -> str:
        return "PNF"

    def serialize(self) -> dict:
        return {
            "measurement_type": self.name,
            "config": {
                "general": asdict(self.general),
                "measurement": asdict(self.measurement),
                "vna": asdict(self.vna),
                "aut": asdict(self.aut),
            },
            "data": {
                "copolar": self.data.copolar,
                "crosspolar": self.data.crosspolar
            },
        }
    
    def serialize_config(self):
        return {
            "general": asdict(self.general),
            "measurement": asdict(self.measurement),
            "vna": asdict(self.vna),
            "aut": asdict(self.aut)
        }
    
    @classmethod
    def from_serialized(cls, payload):
        return cls(
            general=GeneralConfig(**payload["config"]["general"]),
            measurement=PNFMeasurementConfig(**payload["config"]["measurement"]),
            vna=VNAConfig(**payload["config"]["vna"]),
            aut=AUTConfig(**payload["config"]["aut"]),
            data=PNFData(copolar=payload["data"]["copolar"], crosspolar=payload["data"]["crosspolar"]),
        )

    def parse(self, raw_data):
        # parse raw data using self.measurement.scan_point_matrix, etc.
        ...

    def transform(self, data, params):
        ...
