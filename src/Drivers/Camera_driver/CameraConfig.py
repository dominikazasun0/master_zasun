"""The class is responsible for loading camera parameters and detection conditions."""

__author__ = "Dominika Zasuń"
__copyright__ = ""
__version__ = "1.0"
__email__ = "d.zasun@microamp-solutions.com"
__status__ = "Development"
__year__ = "2026"


import json
import numpy as np

class CameraConfig:
    def __init__(self, config_path):

        self.config_path = config_path
        self.camera_matrix = None
        self.R_handeye = None
        self.t_handeye = None
        self.dist_coeffs = None
        self.lower_gold = None
        self.upper_gold = None
        self.square_size_mm = 0

        # Automatic loading when creating an object
        self._load_config()

    def _load_config(self):

        with open(self.config_path, 'r') as f:
            data = json.load(f)

        # OpenCV wymaga, aby macierze były typu float32 lub float64 w numpy
        self.camera_matrix = np.array(data['camera_matrix'], dtype=np.float32)
        #self.R_handeye = np.array(data['R_handeye'], dtype=np.float32)
        #self.t_handeye = np.array(data['t_handeye'], dtype=np.float32)
        self.dist_coeffs = np.array(data['dist_coeffs'], dtype=np.float32)
        self.lower_gold = np.array(data['lower_gold'], dtype=np.float32)
        self.upper_gold = np.array(data['upper_gold'], dtype=np.float32)
        #self.goal = np.array(data['goal'], dtype=np.float32)
        #self.square_size_mm = data.get('square_size_mm', 55)

    def __repr__(self):
        return f"CameraConfig(Matrix Loaded: {self.camera_matrix is not None})"
