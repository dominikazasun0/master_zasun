"""This class is responsible for setting up the connection with the camera, it contains methods for disconnecting and downloading a frame."""

__author__ = "Dominika Zasuń"
__copyright__ = ""
__version__ = "1.0"
__email__ = "d.zasun@microamp-solutions.com"
__status__ = "Development"
__year__ = "2026"

import cv2

class Camera_driver:
    def __init__(self, device_id=0, width=3840, height=2160):
        self.device_id = device_id
        self.width = width
        self.height = height
        self.cap = None

        # Konwersja na int, na wypadek gdyby z GUI przyszedł string "0"
    def connect(self):
        """Otwiera kamerę dopiero po wywołaniu tej metody."""
        try:
            # Konwersja na int dla kamer USB
            dev_index = int(self.device_id)
        except ValueError:
            dev_index = self.device_id

        # Używamy CAP_DSHOW lub CAP_MSMF dla stabilności na Windows
        self.cap = cv2.VideoCapture(dev_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if not self.is_connected():
            raise RuntimeError(f"Błąd: Nie można otworzyć kamery o ID {dev_index}")

    def get_frame(self):
        """
        Fetches a single frame.
        """
        ret, frame = self.cap.read()
        if not ret:
            print("Warning: Failed to retrieve frame.")
            return None
        return frame

    def release(self):
        """Frees up camera resources and closes windows."""
        self.cap.release()
        #cv2.destroyAllWindows()
        print("The camera was released correctly.")

    def is_connected(self):
        """Sprawdza czy kamera jest zainicjalizowana."""
        return self.cap is not None and self.cap.isOpened()
