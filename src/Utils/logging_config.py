__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
from PySide6.QtCore import Signal, QObject


class Handler(QObject, logging.Handler):
    new_record = Signal(str, int)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        logging.Handler.__init__(self)
        
        formatter = Formatter(
            fmt="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
            datefmt="%H:%M:%S",
        )
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        self.new_record.emit(msg, record.levelno)

class Formatter(logging.Formatter):
    
    def formatException(self, ei):
        result = super().formatException(ei)
        return result.replace('\n', '')

    def format(self, record):
        s = super().format(record)
        if record.exc_text:
            s = s.replace('\n', '')
        return s
    
def get_logger(name=None) -> logging.Logger:
    return logging.getLogger(name)
