__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Research"
__year__ = "2025"

# --------- created using Python 3.12.5 --------------

from src.Drivers.VNA_driver.VNA_driver import VNA_driver
import numpy as np
import struct


class N9918A_driver(VNA_driver):

    def read_data(self) -> float:
        if not self.connected:
            raise RuntimeError("VNA not connected")
        try:
            # self.write("CALC:MARK1 ON")
            # self.write("CALC:MARK:MAX")
            response = self.query("CALC:MARK:Y?")
            parts = response.strip().split(",")
            p1 = float(parts[0])
            p2 = float(parts[1])
            # z = complex(real, imag)
            peak_value = p1  # random.uniform(-60, 0)#p1#20 * np.log10(np.abs(z))
            return peak_value
        except Exception as e:
            # messagebox.showerror("Błąd", f"Nie udało się odczytać wartości Peak: {e}")
            print("Błąd", f"Nie udało się odczytać wartości Peak: {e}")
            return None

    def get_trace_list(self, field: str | None = None) -> list:
        self.write("CALC:PAR:CAT:EXT?")
        _przebiegi = self.read()
        vs = _przebiegi.split(",")
        # lista słowników
        traceVNA = [{"name": vs[i], "trace": vs[i+1]} for i in range(0, len(vs), 2)]
        if field in ("name", "trace"):
            return [t[field] for t in traceVNA]
        return traceVNA

    def get_trace_data(self, channel: int = 1, trace: str = "S11") -> np.ndarray:
        traceVNA = self.get_trace_list("trace")

        self.write(f"CALC:PAR1:DEF {trace}")
        self.write("INIT:CONT OFF;*OPC?")
        stop_opc = self.read()
        print(f"stop_opc: {stop_opc}")
        self.write("INIT:IMM;*OPC?")  # single sweep
        imm_opc = self.read()
        print(f"imm_opc: {imm_opc}")
        self.write("FORM:DATA REAL,32")
        self.write("CALC:DATA:SDATA?")
        hash = self.read_L(1)  # znak 0x23 czyli string # lub bajt b'#'
        print(f"hash: {hash}")
        h = int(self.read_L(1))
        print(f"h: {h}")
        data_len = int(self.read_L(h))
        print(f"data_len: {data_len}")

        # Wyłączenie znaku końca transmisji
        self.term_chars = ''  # np. dla pyvisa, lub instr.read_termination = ''

        raw_bytes = self.read_bytes(data_len)

        # Przywrócenie znaku końca transmisji
        self.term_chars = '\n'
        x = self.read()
        print(f"koniec: {x}")

        # Parsowanie danych binarnych do floatów (4 bajty float, 8 bajtów na liczbę zespoloną)
        num_points = data_len // 8
        data_re = np.zeros(num_points)
        data_im = np.zeros(num_points)
        for i in range(num_points):
            re_part = struct.unpack('<f', raw_bytes[i * 8 + 0: i * 8 + 4])[0]  # > = big-endian
            im_part = struct.unpack('<f', raw_bytes[i * 8 + 4: i * 8 + 8])[0]
            data_re[i] = re_part
            data_im[i] = im_part

        complex_data = data_re + 1j * data_im
        self.write("INIT:CONT ON;*OPC?")
        x = self.read()
        print(f"CONT OPC: {x}")
        return complex_data


