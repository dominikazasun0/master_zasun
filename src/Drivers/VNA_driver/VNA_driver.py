__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Research"
__year__ = "2025"

# --------- created using Python 3.12.5 --------------
from abc import ABC, abstractmethod
import pyvisa
import logging
log = logging.getLogger("GUI")

class VNA_driver(ABC):

    def __init__(self, ip_address: str, timeout_ms: int = 5000):
        self.ip = ip_address
        self.timeout_ms = timeout_ms
        self.resource_string = self.ip
        self.rm = pyvisa.ResourceManager()
        self.connected = False
        self.instr = None

    # Inicjalizacja połączenia z analizatorem (za pomocą VISA)
    def connect(self):
        try:
            self.instr = self.rm.open_resource(self.resource_string)
            self.instr.timeout = self.timeout_ms
            idn = self.instr.query("*IDN?")
            self.connected = True
            opcje_vna = self.instr.query("*OPT?")
            log.debug(f"Connected to: {idn}, {opcje_vna}")
        except Exception as e:
            log.error(f"Connection error: {e}")
            # messagebox.showerror("Błąd", f"Nie można połączyć z analizatorem: {e}")
            self.instr = None
            return None

    def disconnect(self):
        if self.instr:
            self.instr.close()
            log.debug("Disconnected from instrument.")
        self.instr = None
        self.connected = False

    def is_connected(self) -> bool:
        return self.instr is not None

    def query(self, command: str) -> str:
        if not self.instr:
            raise RuntimeError("Instrument not connected.")
        return self.instr.query(command).strip()

    def write(self, command: str):
        if not self.instr:
            raise RuntimeError("Instrument not connected.")
        self.instr.write(command)

    def read(self) -> str:
        if not self.instr:
            raise RuntimeError("Instrument not connected.")
        return self.instr.read().strip()

    def read_L(self, L: int = 1024) -> str:
        data = self.instr.read_bytes(L).decode('ascii')  # zwraca bytes
        # print(f"Data read_L: {data.decode('ascii')}")
        return data

    def read_bytes(self, n: int) -> bytes:
        return self.instr.read_bytes(n)

    def read_raw(self):
        raw = self.read_raw()
        #log.debug(f"raw {raw}")

    def cls_vna(self):
        self.write("*CLS")

        while True:
            err = self.query("SYST:ERR?")
            log.info(f"Clear error VNA: {err}")
            if "No error" in err or "+0" in err:
                break
        self.write("*OPC?")  # single sweep
        opc = self.read()
        log.debug(f"cls_opc: {opc}")

    def reset(self):
        self.write("*RST")

    def hold_sweep(self):
        self.write("INIT:CONT OFF;*OPC?")
        hold_opc = self.instr.read()
        log.debug(f"hold: {hold_opc}")

    def single_sweep(self) -> str:
        # self.write("INIT:CONT OFF;*OPC?")
        self.write("INIT:IMM;*OPC?")  # single sweep
        imm_opc = self.instr.read()
        # print(f"imm_opc: {imm_opc}")
        return imm_opc

    def continuous_sweep(self):
        self.write("INIT:CONT ON;*OPC?")
        cont_opc = self.instr.read()
        #log.debug(f"cont_opc: {cont_opc}")

    def get_num_points(self) -> int:
        if not self.connected:
            raise RuntimeError("VNA not connected")
        self.write("SENS:SWE:POIN?")
        N = int(self.read().strip())
        log.debug(f"N = {N}")
        return N

    def get_freq_start(self) -> float:
        if not self.connected:
            raise RuntimeError("VNA not connected")
        self.write("SENS:FREQ:STAR?")
        start_freq_Hz = float(self.read().strip())
        log.debug(f"f_start = {start_freq_Hz/1e9} [GHz]")
        return start_freq_Hz

    def get_freq_stop(self) -> float:
        if not self.connected:
            raise RuntimeError("VNA not connected")
        self.write("SENS:FREQ:STOP?")
        stop_freq_Hz = float(self.read().strip())
        log.debug(f"f_stop = {stop_freq_Hz/1e9} [GHz]")
        return stop_freq_Hz

    def set_num_points(self, num_points: int, channel: int = 1):
        self.write(f"SENS{channel}:SWE:POIN {num_points}")

    def set_frequency_range(self, start_freq_Hz: float, stop_freq_Hz: float, channel: int = 1):
        self.write(f"SENS{channel}:FREQ:STAR {start_freq_Hz}")
        self.write(f"SENS{channel}:FREQ:STOP {stop_freq_Hz}")

    @abstractmethod
    def set_active_trace(self, trace: str):
        """ustawia aktywny trace"""
        pass

    @abstractmethod
    def read_data(self):
        """Metoda abstrakcyjna – do zaimplementowania w klasie dziedziczącej"""
        pass

    @abstractmethod
    def get_trace_data(self, channel: int = 1, trace: str = "S11") -> list:
        """Pobiera dane z danego kanału i śladu (trace)"""
        pass

    @abstractmethod
    def get_trace_list(self) -> list:
        """Pobiera listę trace-ów"""
        pass

    @abstractmethod
    def get_pow_level(self) -> list:
        """Pobiera poziom mocy"""
        pass

