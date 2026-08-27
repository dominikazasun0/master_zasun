__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Research"
__year__ = "2025"

# --------- created using Python 3.12.5 --------------

from src.Drivers.VNA_driver.VNA_driver import VNA_driver
import random
import numpy as np
import struct
import logging
log = logging.getLogger("GUI")

class N5224B_driver(VNA_driver):

    def read_data(self) -> float:
        if not self.connected:
            raise RuntimeError("VNA not connected")
        try:
            # self.write("CALC:MARK1 ON")
            # self.write("CALC:MARK:MAX")
            response = self.query("CALC:MEAS:MARK:Y?")
            parts = response.strip().split(",")
            p1 = float(parts[0])
            p2 = float(parts[1])
            # z = complex(real, imag)
            peak_value = p1  # random.uniform(-60, 0)#p1#20 * np.log10(np.abs(z))
            return peak_value
        except Exception as e:
            # messagebox.showerror("Błąd", f"Nie udało się odczytać wartości Peak: {e}")
            log.error("Error", f"Can not read trace: {e}")
            return random.uniform(-60, 0)
        # symulowany odczyt z VNA — losowy poziom sygnału
        # return random.uniform(-60, 0)

    def get_pow_level(self) -> tuple[str, bool]:
        self.write("SOUR:POW:LEV?")
        power_level = self.read()
        self.write(f"OUTP:STAT?")
        RF_state = bool(self.read())
        return power_level, RF_state

    def get_trace_list(self, field: str | None = None) -> list:
        self.write("CALC:PAR:CAT:EXT?")
        _przebiegi = self.read()
        vs = _przebiegi.split(",")
        # lista słowników
        traceVNA = [{"name": vs[i].strip('"') , "trace": vs[i+1].strip('"') } for i in range(0, len(vs), 2)]
        if field in ("name", "trace"):
            return [t[field] for t in traceVNA]

        log.debug(f"przebiegi {traceVNA}")
        return traceVNA

    def get_trace_sel(self) -> str:
        self.write("CALC:PAR:SEL?")
        current_trace = self.read().strip().strip('"')
        return current_trace

    def get_trace_data(self, channel: int = 1, trace: str = "CH1_S11_1") -> np.ndarray:
        self.write(f"CALC:PAR1:SEL '{trace}'")
        self.write("INIT:CONT OFF;*OPC?")
        stop_opc = self.read()
        #log.debug(f"CONT OFF: {stop_opc}")
        self.write("INIT:IMM;*wai")  # single sweep
        # imm_opc = self.read()
        # print(f"Hold: {imm_opc}")
        # self.write(f"CALC{channel}:DATA? SDATA")
        self.write("FORM:DATA REAL,64")
        # Wyłączenie znaku końca transmisji
        self.term_chars = ''  # np. dla pyvisa, lub instr.read_termination = ''
        self.write("CALC:DATA? SDATA")
        # hash = self.read_bytes(1)
        hash = self.read_L(1)  # znak 0x23 czyli string # lub bajt b'#'
        #log.debug(f"hash: {hash}")
        h = int(self.read_L(1))
        #log.debug(f"h: {h}")
        data_len = int(self.read_L(h))
        #log.debug(f"data_len: {data_len}")

        # dane
        raw_bytes = self.read_bytes(data_len)

        # Przywrócenie znaku końca transmisji
        self.term_chars = '\n'

        x = self.read()
        #log.debug(f"koniec: {x}")

        # Parsowanie danych binarnych do floatów (8 bajtów float64 (double), 16 bajtów na liczbę zespoloną)
        num_points = data_len // 16
        data_re = np.zeros(num_points)
        data_im = np.zeros(num_points)
        for i in range(num_points):
            re_part = struct.unpack('>d', raw_bytes[i * 16 + 0: i * 16 + 8])[0]  # > = big-endian
            im_part = struct.unpack('>d', raw_bytes[i * 16 + 8: i * 16 + 16])[0]
            data_re[i] = re_part
            data_im[i] = im_part

        complex_data = data_re + 1j * data_im
        self.write("INIT:CONT ON;*OPC?")
        x = self.read()
        #log.debug(f"CONT ON: {x}")
        return complex_data

    def set_active_trace(self, trace: str = "CH1_S11_1"):
        self.write(f"CALC:PAR1:SEL '{trace}'")

    def set_pow_level(self, pow_dBm: float, rf_on: bool, channel: int = 1):
        power = str (pow_dBm)
        self.write(f"SOUR{channel}:POW {power}")
        rf_state = "OFF"
        if rf_on: rf_state = "ON"

        self.write(f"OUTP:STAT {rf_state}")
