__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime

log = logging.getLogger("GUI")

class AbstractFile(ABC):
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.name: str = self.path.name
        if self.path.exists():
            stat = self.path.stat()
            self.size = stat.st_size
            self.modified = datetime.fromtimestamp(stat.st_mtime)
        else:
            self.size = 0
            self.modified = None  # or datetime.now()


    @property
    @abstractmethod
    def file_type(self) -> str:
        """Logical file type shown in GUI (PNF, FF, etc.)."""

    @property
    @abstractmethod
    def format(self) -> str:
        """Physical file format (hdf5, mat, csv, etc.)."""

    def metadata(self) -> dict:
        """Lightweight info safe for GUI consumption."""
        return {
            "name": self.name,
            "type": self.file_type,
            "format": self.format,
            "size": self.size,
            "modified": self.modified,
            "path": str(self.path),
        }