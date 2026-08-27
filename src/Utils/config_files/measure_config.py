__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

from enum import IntEnum
from pathlib import Path
from src.Data_Processing import PNFMeasurement, FFMeasurement


SAVE_PATH = Path(r"\\10.1.1.10\nas\_SHARE_\ANTENNA_MEASUREMENT_RANGE\Captures\Saves")

EXPORT_FORMATS = [".h5", ".mat"]

MEASUREMENT_TYPES = {
    "PNF": PNFMeasurement,
    "FF": FFMeasurement,
}

#
DEV_ROW= {
    "AUT" : 0,
    "VNA" : 1,
    "TIC_AZ" : 2,
    "TIC_EL" : 3,
    "RARM" : 4,
    "MICRO" : 5,
    "CAM" : 6
}
# mapa trybów pomiarowych
MEASURE_MODE_MAP = {
    "": ["",""],     # puste
    "FF_az": ["TIC_AZ", "VNA"],
    "FF_el": ["TIC_EL", "VNA"],
    "PNF": ["RARM", "VNA"],
    "Calib": ["RARM"]

}
# mapa wyborów jednostek
UNITS_MAP = ["Hz", "kHz", "MHz", "GHz"]

# mapa formatów danych VNA
FORMAT_MAP = {
    "format_name": ["dB/deg", "lin/rad", "re/im"],
    "A_name": ["amp [dB]", "amp lin", "re"],
    "B_name": ["phase [deg]", "phase [rad]", "im"]
}

# mapa poziomów mocy VNA
POWER_VNA_MAP = ["-30", "-25", "-20", "-15", "-10", "-5", "0", "5", "10", "15"]

# mapa wyborów kroków silnika
TIC_STEP_MAP = ["full", "1/2", "1/4", "1/8", "1/16", "1/32"]

# mapa wyborów opóźnień
DELAY_MAP = ["0", "10", "100", "200", "300", "500", "1000", "2000"]

# dane robota
# 192.168.1.203:18333
RARM_DATA = {
    "IP" : '192.168.1.203',
    "LBL" : "UFACTORY XArm 850"
}

class State(IntEnum):
    Idle=0
    Manual=1
    Measuring=2
    Paused=3
    Error=4

class Priority(IntEnum):
    Manual=0
    Measurement=10
