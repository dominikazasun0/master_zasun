from src.devices.devices import Devices

devices = Devices()

devices.add_device("AUT", "192.168.1.10")
devices.add_device("VNA", "GPIB::10")
devices.add_device("Camera", "/dev/video0")