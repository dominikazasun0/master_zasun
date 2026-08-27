__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

from .base import FileFormat
from .hdf5 import HDF5Format
from .mat import MATFormat

__all__ = ["FileFormat", "HDF5Format", "MATFormat"]