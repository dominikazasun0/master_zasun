__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import sys
import ctypes
from PySide6.QtWidgets import QApplication
from GUI.main_window import MainWindow

if __name__ == "__main__":
    print("Python executable:", sys.executable) #Ensure Virtual Environment
    app_id = 'ms.ant_meas_gui' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())