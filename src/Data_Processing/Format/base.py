__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
from abc import ABC, abstractmethod

log = logging.getLogger("GUI")

class FileFormat(ABC):
    name: str

    @abstractmethod
    def write(self, path, payload):
        pass

    @abstractmethod
    def read(self, path):
        pass

    @abstractmethod
    def peek_meas_type(self, path) -> str:
        """Read minimal info without loading full data."""
