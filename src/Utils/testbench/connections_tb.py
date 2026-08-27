import psutil
import pyvisa
from serial.tools import list_ports

# Example usage
instruments = pyvisa.ResourceManager().list_resources()
for inst in instruments:
    print(inst)

# Example usage
for port in list_ports.comports():
    print(f"{port.device} - {port.description}")
