__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
from pathlib import Path
from .abstract import AbstractFile
from ..format import FileFormat

log = logging.getLogger("GUI")

class MeasurementFile(AbstractFile):
    def __init__(self,
                 path: str | Path,
                 file_format: "FileFormat",
                 measurement_type: str | None  =None):
        super().__init__(path)
        self._format = file_format
        self._measurement_type = measurement_type

    @property
    def format(self) -> str:
        return self._format.name

    @property
    def file_type(self) -> str:
        if self._measurement_type is None:
            self._measurement_type = self._format.peek_meas_type(self.path)
        return self._measurement_type

    def load(self, measurement_cls):
        payload = self._format.read(self.path)
        return measurement_cls.from_serialized(payload)

    def save(self, measurement):
        payload = measurement.serialize()
        self._format.write(self.path, payload)