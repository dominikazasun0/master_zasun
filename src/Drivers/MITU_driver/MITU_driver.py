__author__ = "Dominika Zasuń"
__copyright__ = ""
__version__ = "1.0"
__email__ = "d.zasun@microamp-solutions.com"
__status__ = "Research"
__year__ = "2025"

# --------- created using Python 3.12.0 --------------
import serial
import time
import threading  # <<< DODANO MODUŁ THREADING

import logging

log = logging.getLogger("GUI")


class MITU_driver():

    def __init__(self, port, baudrate=115200, timeout=0.2):  # Ustawiono sensowny timeout dla wątku
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        # Flagi kontrolne dla wątku
        self.connected = False
        self._running = False
        self._thread = None

        # Miejsce na przechowywanie ostatnio odczytanych danych
        self.latest_data = None

    def connect(self):
        # Inicjalizacja sterownika MITUTOYO
        try:
            # Używamy zdefiniowanego timeoutu (np. 0.2s)
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.connected = True
            log.info(f"MITUTOYO connected on {self.port}")

            # 1. Sprawdzenie, czy urządzenie jest gotowe
            # Można tu zachować is_connected/is_ready, ale wątek przejmie główną rolę

            # 2. Uruchomienie wątku tła do ciągłego odczytu
            self._running = True
            # daemon=True oznacza, że wątek zostanie automatycznie zakończony, gdy zamknie się program główny
            self._thread = threading.Thread(target=self._reading_loop, daemon=True)
            self._thread.start()

            return True

        except Exception as e:
            self.connected = False
            log.error(f"Connection with MITU error: {e}")
            return False

    def disconnect(self):
        # Najpierw zatrzymujemy pętlę w wątku tła
        self._running = False
        if self._thread and self._thread.is_alive():
            # Czekamy, aż wątek bezpiecznie się zakończy
            self._thread.join()
            log.info("MITUTOYO reading thread stopped.")

        if self.ser and self.ser.is_open:
            self.ser.close()
        self.connected = False
        log.info("MITUTOYO disconnected.")

    def _reading_loop(self):
        """
        Metoda uruchamiana w osobnym wątku.
        Ciągle odczytuje dane z portu, aż do momentu ustawienia self._running na False.
        """
        log.debug("Starting MITUTOYO reading loop.")
        while self._running:
            try:
                # Blokujące wywołanie (do max. 0.2s z timeout=0.2)
                line = self.ser.readline()

                if line:
                    # Dekodowanie i czyszczenie linii
                    decoded_line = line.decode('utf-8', errors='ignore').strip()
                    if decoded_line:
                        # Zapisanie odczytanej wartości w atrybucie
                        self.latest_data = decoded_line
                        #log.debug(f"Received (in thread): {decoded_line}")

                # Jeśli timeout jest > 0, nie musimy dodawać dodatkowego time.sleep()

            except serial.SerialException as e:
                log.error(f"Port error in reading thread: {e}")
                self._running = False  # Przerwanie pętli w przypadku poważnego błędu
            except Exception as e:
                log.error(f"Unexpected error in reading thread: {e}")

    def get_latest_data(self):
        """
        Publiczna metoda dla wątku głównego (GUI) do pobrania ostatniego pomiaru.
        """
        return self.latest_data

    def is_ready(self):
        """
        Sprawdza, czy urządzenie jest gotowe do pracy.
        Oznacza to, że:
        - jest połączone,
        - port jest otwarty,
        - wątek odczytu działa.
        """
        return self.is_connected() and self._thread and self._thread.is_alive()

    def is_connected(self):
        """Sprawdza, czy połączenie jest aktywne"""
        return self.connected and self.ser and self.ser.is_open

# Stara metoda read_serial została usunięta, ponieważ odczyt odbywa się ciągle w tle.
# Zamiast niej używaj MITU_driver.get_latest_data() w wątku GUI.