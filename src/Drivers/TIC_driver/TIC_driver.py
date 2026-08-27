__author__ = "Jakub Strycharz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "j.strycharz@microamp-solutions.com"
__status__ = "Research"
__year__ = "2025"

# --------- created using Python 3.12.0 --------------
import subprocess
import yaml
import os
from time import sleep

import logging

log = logging.getLogger("GUI")

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Utils/config_files/TIC_config.yml"))

class TIC_driver():

    def __init__(self, serial_number: str):
        self.sn = serial_number
        self.connected = False

    def connect(self):
        # Inicjalizacja sterownika Tic
        try:
            self.set_step_mode(1)
            with open(config_path, "r") as file:
                config = yaml.load(file, Loader=yaml.SafeLoader)  # Wczytanie konfiguracji
            if "max_speed:" in config:
                self.set_max_speed(config["max_speed:"])
            if "starting_speed" in config:
                self.set_starting_speed(config["starting_speed"])
            if "step_mode" in config:
                self.set_step_mode(config["step_mode"])
            if "current_limit" in config:
                self.set_current_limit(config["current_limit"])

            self.halt_and_set_position(0)
            self.connected = self.is_connected()

        except Exception as e:
            self.connected = False
            log.error(f"Connection with TIC error: {e}")
            return None

    def disconnect(self):
        self.deenergize()
        self.connected = False

    def run(self, *args):
        return subprocess.check_output(["ticcmd", "-d", self.sn, *args], text=True)

    def get_status(self):
        try:
            output = self.run("--status", "--full")
            self.connected = True
            return yaml.safe_load(output)
        except Exception as e:
            self.connected = False
            log.error(f"Connection with TIC error: {e}")
            return False

    def get_step_mode(self):
        status = self.get_status()
        return status.get("Step mode", None)

    def get_step(self):
        status = self.get_status()
        step_mode = status.get("Step mode", None)
        step_deg = 1.8
        match step_mode:
            case "Full":
                step_deg = 1.8
            case "1/2 step":
                step_deg = 1.8 / 2
            case "1/4 step":
                step_deg = 1.8 / 4
            case "1/8 step":
                step_deg = 1.8 / 8
            case "1/16 step":
                step_deg = 1.8 / 16
            case "1/32":
                step_deg = 1.8 / 32
            case _:
                step_deg = 1.8
        return step_deg

    def get_current_position(self) -> float:
        status = self.get_status()
        #print(f"status:  {status}")
        return status.get("Current position", None)

    def get_current_limit(self) -> float:
        status = self.get_status()
        return status.get("Current limit", None)

    def get_errors(self):
        status = self.get_status()
        return status.get("error_status", None)

    def exit_safe_start(self):
        subprocess.run(["ticcmd", "-d", self.sn, "--exit-safe-start"], check=True)

    def enter_safe_start(self):
        subprocess.run(["ticcmd", "-d", self.sn, "--enter-safe-start"], check=True)

    def move_motor(self, position):
        try:
            self.exit_safe_start()
            subprocess.run(["ticcmd", "-d", self.sn, "--position", str(position)], check=True)
        except Exception as e:
            log.error("Błąd", f"Can't move motor: {e}")

    def is_motor_moving(self, tolerance: int = 1) -> bool:
        status = self.get_status()
        #result = subprocess.run(["ticcmd", "-d", self.sn, "--status"], capture_output=True, text=True)
        if not status:
            return False

        current = status.get("Current position")
        target = status.get("Target position")

        if current is None or target is None:
            return False

        return abs(current - target) > tolerance

    def set_step_mode(self, idx: int):
        try:
            #log.debug(f"TIC_driver set_step: 1/(2^{idx})")
            if idx == 0:
                mode = "full"
            else:
                mode = str(2**idx)
            subprocess.run(["ticcmd", "-d", self.sn, "--step-mode", mode], check=True)
        except Exception as e:
            log.debug(f"set_step error: {e}")

    def set_starting_speed(self, value: int):
        try:
            subprocess.run(["ticcmd", "-d", self.sn, "--starting-speed", str(value)], check=True)
        except Exception as e:
            log.error(f"set_starting_speed error: {e}")

    def set_max_speed(self, value: int):
        try:
            subprocess.run(["ticcmd", "-d", self.sn, "--max-speed", str(value)], check=True)
        except Exception as e:
            log.error(f"set_max_speed error: {e}")

    def set_current_limit(self, mamps: int):
        try:
            value = (mamps // 32) * 32  # zaokrąglenie w dół do 32 mA
            subprocess.run(["ticcmd", "-d", self.sn, "--current", str(value)], check=True)
        except Exception as e:
            log.error(f"set_current_limit error: {e}")


    def halt_and_set_position(self, position):
        try:
            subprocess.run(["ticcmd", "-d", self.sn, "--halt-and-set-position", str(position)], check=True)
        except Exception as e:
            log.error(f"set_position error: {e}")

    def energize(self):
        try:
            subprocess.run(["ticcmd", "-d", self.sn, "--energize"], check=True)
            self.clear_driver_error()
            self.exit_safe_start()
        except Exception as e:
            log.debug(f"energize: {e}")

    def deenergize(self):
        try:
            subprocess.run(["ticcmd", "-d", self.sn, "--deenergize"], check=True)
        except Exception as e:
            log.error(f"deenergize error: {e}")

    def clear_driver_error(self):
        try:
            subprocess.run(["ticcmd", "-d", self.sn, "--clear-driver-error"], check=True)
        except Exception as e:
            log.error(f"clear error: {e}")

    def is_connected(self):
        try:
            self.run("--status")
            return True
        except subprocess.CalledProcessError as e:
            log.error(f"clear error: {e}")
            return False