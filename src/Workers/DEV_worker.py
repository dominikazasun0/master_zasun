__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Research"
__year__ = "2025"

# --------- created using Python 3.12.5 --------------
from PySide6.QtCore import QObject, Slot, Signal, QTimer
from abc import ABCMeta, abstractmethod
from enum import Enum, auto


import logging
log = logging.getLogger("GUI")

# Metaklasa łącząca metaklasy QObject i ABC
class MetaQObjectABC(type(QObject), ABCMeta):
    pass

class WorkerState(Enum):
    IDLE = auto()
    SET_POSITION = auto()
    GET_DATA = auto()
    PROCESS = auto()
    READY = auto()
    NEXT = auto()
    FINISHED = auto()

# Abstrakcyjna baza dla workerów Qt
class DEV_Worker(QObject, metaclass=MetaQObjectABC):

    def __init__(self, label, /):
        super().__init__()
        self.dev_label = label
        self.model = None
        self.owner = None
        self.device = None
        self._running = False
        self.should_continue = False
        self.delay_between_use = 10

        # maszyna stanów - inicjalizacja
        self.state = WorkerState.IDLE

        self.run_timer = QTimer(self)
        self.run_timer.setInterval(100)  # ms
        self.run_timer.timeout.connect(self._finished_step)

    @Slot(str, str, dict)
    def command_interp(self, dev_label:str, client_id:str, command: dict):
        """
        Interpreter komend sterujących wysyłanych po sygnale Qt.
        """
        # Komenda nie jest do tego urządzenia → ignoruj
        if self.dev_label != dev_label:
            return
        self.owner = client_id

        # Urządzenie niepodłączone
        if self.device is None:
            log.error(f"No {self.dev_label} connected!")
            return

        # Pobierz metodę z payloadu
        method = command.get("method")
        kwargs = command.get("kwargs", {})
        log.debug(f"command_interp self.dev_label: {self.dev_label} dev_label: {dev_label} client_id {client_id} method {method} kwargs {kwargs}")

        if not method:
            log.error("Missing 'method' in command payload")
            return

        # Pobierz referencję do metody
        fn = getattr(self, method, None)
        if not callable(fn):
            log.error(f"{self.dev_label}_worker has no method '{method}'")
            return
        try:
            # Wywołanie metody z parametrami
            fn(**kwargs) # type: ignore[arg-type]
        except TypeError as e:
            log.error(
                f"Argument mismatch when calling {method}: {e}\n"
                f"Provided kwargs: {kwargs}"
            )
        except Exception as e:
            log.exception(f"Error executing command '{method}': {e}")

    @abstractmethod
    def next_in_sequ(self):
        """Metoda abstrakcyjna – do zaimplementowania w klasie dziedziczącej"""
        pass

    @abstractmethod
    def _finished_step(self):
        """Metoda abstrakcyjna – do zaimplementowania w klasie dziedziczącej"""
        pass

    @abstractmethod
    def switch_on_off(self):
        """Metoda abstrakcyjna – do zaimplementowania w klasie dziedziczącej"""
        pass

    @abstractmethod
    def configure(self, *args, **kwargs):
        """Metoda abstrakcyjna – do zaimplementowania w klasie dziedziczącej"""
        pass

    @abstractmethod
    def do_next_event(self, client_id):
        """Metoda abstrakcyjna – do zaimplementowania w klasie dziedziczącej"""
        pass

    @abstractmethod
    def set_device(self, dev_model: str, dev_address: str):
        """Metoda abstrakcyjna – do zaimplementowania w klasie dziedziczącej"""
        pass

    @abstractmethod
    def stop(self):
        """Metoda abstrakcyjna – do zaimplementowania w klasie dziedziczącej"""
        pass