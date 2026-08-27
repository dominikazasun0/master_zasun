"""The class is responsible for applying a mask to the camera image to increase contrast."""

__author__ = "Dominika Zasuń"
__copyright__ = ""
__version__ = "1.0"
__email__ = "d.zasun@microamp-solutions.com"
__status__ = "Development"
__year__ = "2026"

import cv2
import numpy as np

class Preprocessor:
    def __init__(self, config):
        # We get the color ranges from the config (item 1 of your list)
        self.lower = np.array(config.lower_gold)
        self.upper = np.array(config.upper_gold)

    def get_mask(self, frame):
        # Returns only a black and white color mask
        blurred = cv2.GaussianBlur(frame, (9, 9), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)
        return mask
