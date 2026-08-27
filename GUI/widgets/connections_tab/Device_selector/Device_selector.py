__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QMenu, QLabel
from PySide6.QtCore import Qt
import logging
log = logging.getLogger(__name__)

class DeviceSelector(QWidget):
    def __init__(self, devices_list, table, row,  parent=None):
        super().__init__(parent)

        self.table = table
        self.row = row
        self.addr = QLineEdit()
        self.label = None
        self.button = QPushButton("▼")
        self.button.setFixedWidth(30)

        # Create a horizontal layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.addr)
        layout.addWidget(self.button)
        self.setLayout(layout)

        # Create the dropdown menu
        self.menu = QMenu()
        for address, label in devices_list:
            action = self.menu.addAction(f"{address} → {label}")
            action.setData((address, label))  # Store raw address
            action.triggered.connect(lambda checked=False, a=action: self._handle_action(a))

        self.button.setMenu(self.menu)

    def _handle_action(self, action, checked=False):
        addr, lbl = action.data()
        self.addr.setText(addr)
        self.label = lbl
        item = self.table.cellWidget(self.row, 1)
        if isinstance(item, QLineEdit):
            item.setText(lbl)

    def get_value(self):
        return self.addr.text()

    def get_label(self):
        return self.label

    def set_value(self, text):
        self.addr.setText(text)
