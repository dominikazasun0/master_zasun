__author__ = "Kacper Marks"
__copyright__ = ""
__version__ = "1.0"
__email__ = "k.marks@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"

import logging
from src.Drivers.VNA_driver.N5224B import N5224B_driver
from src.Drivers.VNA_driver.N9918A import N9918A_driver
from src.Drivers.TIC_driver.TIC_driver import TIC_driver
from src.Drivers.Arm_Driver.Robotic_Arm_Driver import RA
from src.Drivers.Camera_driver.Camera_Driver import Camera_driver
log = logging.getLogger("GUI")

class Devices:
    def __init__(self):
        self._devices = {}
        self._factories = {
            "AUT": self._create_aut,
            "Robotic Arm": self._create_robotic_arm,
            "VNA": self._create_vna,
            "TIC": self._create_positioner,
            "Camera": self._create_camera,
            "Digimatic Indicator": self._create_dig_ind,
        }

        self._delete_factories = {
            "VNA": self._delete_vna,
            "TIC": self._delete_TIC,
            "Robotic Arm": self._delete_robotic_arm 
        }

        # rejestr dostępnych VNA
        self._vna_drivers = {
            "N9918A": N9918A_driver,
            "N5224B": N5224B_driver,
        }

    def add_device(self, dev_type: str, address: str, instance=None):
        if instance is None:
            factory = self._factories.get(dev_type)
            if not factory:
                raise ValueError(f"Unknown device type: {dev_type}")
            log.debug(f"Devices dev_type {dev_type} address {address}")
            instance = factory(address)
        self._devices.setdefault(dev_type, {})[address] = instance
        return instance

    def get_device(self, dev_type: str, address: str = None):
        devices_of_type = self._devices.get(dev_type, {})
        if address is not None:
            return devices_of_type.get(address)
        # no address → return first available
        return next(iter(devices_of_type.values()), None)



        # print(self._devices.get(dev_type, {}).get(address))
        # return self._devices.get(dev_type, {}).get(address)

    def has_device(self, dev_type: str, address: str) -> bool:
        return address in self._devices.get(dev_type, {})
    
    def list_devices(self):
        """Return a flat list of (dev_type, address, instance)."""
        devices_list = []
        for dev_type, addr_map in self._devices.items():
            for address, instance in addr_map.items():
                devices_list.append((dev_type, address, instance))
        return devices_list
    
    def delete_device(self, dev_type: str):
        dev = self._devices.pop(dev_type, {})
        if not dev:
            log.error(f"Device \"{dev_type}\" doesn't exist.")
            return None
        return dev
            
    
    def _create_aut(self, address):
        log.debug("AUT created!")
        return True
        # return AUT(address)

    def _create_robotic_arm(self, address, label):
        
        log.debug("Robotic arm created")
        arm = RobotArm(address)
        if arm is not None:
            if arm.alive:
                self.add_device("Robotic Arm", address, arm)  
                return arm
            else:
                return None
        else:
            return None
        
    def _delete_robotic_arm(self, address, label):
        dev_dict= self.delete_device("Robotic Arm")
        dev = next(iter(dev_dict.values()))
        if dev is None:
            return False
        dev.shutdown() 
        return True

    def _delete_TIC(self, address, label):
        dev_dict= self.delete_device("TIC")
        dev = next(iter(dev_dict.values()))
        if dev is None:
            return False
        dev.shutdown()
        return True

        
    def _create_vna(self, address, label):

        log.debug(f"create_vna: label = {label}")

        try:
            model = label.split(",")[1].strip()
        except IndexError:
            raise ValueError(f"Unexpected VNA label format: {label}")

        driver_cls = self._vna_drivers.get(model)

        if driver_cls is None:
            raise ValueError(f"Unknown VNA model: {model}")

        vna = driver_cls(address)
        vna.connect()
        status = vna.is_connected()
        if status:
            return vna
        else:
            return None

    def _create_vna_n5224b(self, address):
        vna_n5224b = N5224B_driver(address)
        vna_n5224b.connect()
        status = vna_n5224b.is_connected()
        if status:   
            return vna_n5224b
        else:
            return None
        
    def _delete_vna(self, address, label):
        dev_dict= self.delete_device("VNA")
        dev = next(iter(dev_dict.values()))
        if dev is None:
            return False
        dev.disconnect() 
        return True

    def _create_positioner(self, address, label):
        log.debug(f"_create positioner address {address}")
        motor = TIC_driver(address)
        motor.connect()
        status = motor.is_connected()
        if status:
            return motor
        else:
            return None

    def _create_camera(self, _label, address):
        log.debug(f"_create positioner address {address}")
        camera = Camera_driver(address)
        camera.connect()
        status = camera.is_connected()
        if status:
            return camera
        else:
            return None
        # return Camera(address)

    def _create_dig_ind(self, _label, address):
        log.debug("Digimatic indicator created!")
        return True
        # return Camera(address)
