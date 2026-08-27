"""The class determines where the detected square is located relative to the camera"""

__author__ = "Dominika Zasuń"
__copyright__ = ""
__version__ = "1.0"
__email__ = "d.zasun@microamp-solutions.com"
__status__ = "Development"
__year__ = "2026"

import cv2
import numpy as np

class PoseEstimator:
    def __init__(self, config):
        """
        Initialization of fixed camera parameters.
        """
        self.camera_matrix = config.camera_matrix
        self.dist_coeffs = config.dist_coeffs

    def solve(self, image_points, width, height):
        """
        Calculates the position (tvec) and rotation (rvec) of a shape.
        """
        if image_points is None:
            return None, None

        self.object_points = np.array([
            [0, 0, 0],  # Lewy górny
            [width, 0, 0],  # Prawy górny
            [width, height, 0],  # Prawy dolny
            [0, height, 0]  # Lewy dolny
        ], dtype=np.float32)


        success, rvec, tvec = cv2.solvePnP(
            self.object_points,
            image_points,
            self.camera_matrix,
            self.dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if success:
            return rvec, tvec
        return None, None

    def get_distance(self, tvec):
        if tvec is None:
            return None
        distance = np.linalg.norm(tvec)
        return distance
