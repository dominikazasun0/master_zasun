"""The class detects shapes and evaluates them and returns the shape with the best evaluation"""

__author__ = "Dominika Zasuń"
__copyright__ = ""
__version__ = "1.0"
__email__ = "d.zasun@microamp-solutions.com"
__status__ = "Development"
__year__ = "2026"

import cv2
import numpy as np


class SquareDetector:
    def __init__(self):
        pass

    def _order_points(self, pts):
        """Arranges points in the following order: Top-Left, Top-Right, Bottom-Right, Bottom-Left"""
        pts = pts.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    def points_to_contour(self, points):
        contour = points.astype("int32")
        contour = contour.reshape((-1, 1, 2))
        return contour

    def find_square(self, mask, shape_size):

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        candidates = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 10000:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    aspect_ratio = float(w) / h

                    if (shape_size-0.1) <= aspect_ratio <= (shape_size+0.1):
                        score_diff = abs(1.0 - aspect_ratio)
                        candidates.append({
                            'points': approx,
                            'contour': cnt,
                            'score': score_diff
                        })

        if not candidates:
            return None

        best_candidate = sorted(candidates, key=lambda x: x['score'])[0]
        best_points = best_candidate['points']

        ordered_points = self._order_points(best_points)

        simplified_contour = self.points_to_contour(ordered_points)

        return ordered_points, simplified_contour
