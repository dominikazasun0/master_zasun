__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
import numpy as np
from dataclasses import dataclass, asdict
from . import MeasurementType, GeneralConfig, FFMeasurementConfig, VNAConfig, AUTConfig, FFData

log = logging.getLogger("GUI")

class FFMeasurement(MeasurementType):
    def __init__(
        self,
        general: GeneralConfig,
        measurement: FFMeasurementConfig,
        vna: VNAConfig,
        aut: AUTConfig,
        data: FFData | None = None
    ):
        super().__init__(general, measurement, vna, aut)
        self.data = data

    @property
    def name(self) -> str:
        return "FF"

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
                "values": self.data.values,
            },
        }

    @classmethod
    def from_serialized(cls, payload):
        return cls(
            general=GeneralConfig(**payload["config"]["general"]),
            measurement=FFMeasurementConfig(**payload["config"]["measurement"]),
            vna=VNAConfig(**payload["config"]["vna"]),
            aut=AUTConfig(**payload["config"]["aut"]),
            data=FFData(values=payload["data"]["values"]),
        )

    def parse(self, raw_data):
        ...

    def transform(self, data, params):
        ...
