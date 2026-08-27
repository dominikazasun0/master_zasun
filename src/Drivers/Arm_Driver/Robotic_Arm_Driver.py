__author__ = "Adrianna Konysz"
__copyright__ = ""
__version__ = "1.0"
__email__ = "a.konysz@microamp-solutions.com"
__status__ = "Development"
__year__ = "2025"


import time
import os
import logging
import msvcrt
from threading import Thread, Event
from xarm.wrapper import XArmAPI
from xarm.core.utils import convert
import json
import time
import datetime

log = logging.getLogger("GUI")

class RA(object):


    PATH_CONFIG = os.path.join(os.path.dirname(__file__), "config.json")

    def __init__(self, ip):
        try:   
            
            self._arm = XArmAPI(ip, baud_checkset=False)
            self._callback_target = None
            with open(self.PATH_CONFIG, "r") as f:
                config = json.load(f)
        
            self.on = config["reduced_mode"]
            self.joint_range = config["joint_range"]
            self.max_joint_speed = config["max_joint_speed"]
            self.max_tcp_speed = config["max_tcp_speed"]
            self.safety_boundary = config["safety_boundary"]
            self.safety_boundary_after_calib = config["safety_boundary_after_calib"]
            self.safe_angle = config["safe_home"]
            self.weight_cal = config["weight_cal"]
            

        except Exception as e:
            log.error(f"Could not initialize robot: {e}")
            self.alive = False

    def arise(self):
        try:   
            
            self._arm.connect()

            self._arm.clean_error()
            self._arm.clean_warn()
            self.stop_event = Event()
            self._arm.register_error_warn_changed_callback(self._error_warn_changed_callback)
            self._arm.register_state_changed_callback(self._state_changed_callback)
            self._same_position_callback = None
            self._arm.register_feedback_callback(self._on_feedback)




            self.estop_listener_thread = Thread(target=self._estop_key_listener, daemon=False)
            self.estop_listener_thread.start()
            log.debug(f"E-STOP listener alive: {self.estop_listener_thread.is_alive()}")




            self._arm.motion_enable(True)
            self.safety()

            self._arm.set_mode(0)
            self._arm.set_state(0)

            log.info("[INFO] Robot initialized.")

            self.alive = True
            self.set_base_coordinate_system()
            self.reset_tcp_offset()
            self._arm.set_tcp_load(self.weight_cal[0],[self.weight_cal[1], self.weight_cal[2], self.weight_cal[3]], wait=True)
        except Exception as e:
            log.error(f"[ERROR] Could not initialize robot: {e}")
            self.alive = False

    def register_callback_target(self, target):
        """Optionally register a worker or handler that should be notified of feedback."""
        self._callback_target = target
        log.debug("Robot listening set...")

    def set_mode(self, mode: int=None):

    #       0: position control mode
    #     1: servo motion mode
    #         Note: the use of the set_servo_angle_j interface must first be set to this mode
    #         Note: the use of the set_servo_cartesian interface must first be set to this mode
    #     2: joint teaching mode
    #         Note: use this mode to ensure that the arm has been identified and the control box and arm used for identification are one-to-one.
    #     3: cartesian teaching mode (invalid)
    #     4: joint velocity control mode
    #     5: cartesian velocity control mode
    #     6: joint online trajectory planning mode
    #     7: cartesian online trajectory planning mode

        if mode is None:
            dane = input('Choose mode (0-7): ')
            if not dane.isdigit() or len(dane) != 1:
                print("ERROR: invalid mode.")
                return
            mode = int(dane)

        else:
            if not isinstance(mode, int) or not(0 <= mode <= 7):
                print("ERROR: invalid mode.")
                return
            
        print(f"Robot arm mode set to {mode}")

        print(self._arm.set_mode(mode))

    def set_state(self, state: int = None):
        # Jeśli nie podano stanu, pytamy użytkownika w konsoli
        if state is None:
            dane = input('Choose state (0-4): ')
            if not dane.isdigit() or len(dane) != 1:
                print("ERROR: invalid state.")
                return
            state = int(dane)
        else:
            # Walidacja parametru
            if not isinstance(state, int) or not (0 <= state <= 4):
                print("ERROR: invalid state.")
                return


        # Wywołanie metody robota
        self._arm.set_state(state)


    def get_state(self):
        state =  self._arm.state
        return state

    def go_home(self):
        
        #SPRAWDZANIE CZY NIE JEST W TRYBIE RĘCZNYM
        
        #trzeba będzie jeszcze napisać dodatkową pozycję HOME bezpieczną dla komory!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self._arm.move_gohome(speed=100, mvacc=None, mvtime=None, is_radian=None, wait=True, timeout=None)
    
    def is_connected(self):
        if self.alive:
            return True
        else:
            return False
        
    # def safe_home(self):
    #     self._arm.set_state(0)
    #     self._arm.set_mode(1)
    #     self._arm.set_servo_angle_j(self.safe_angle, speed=50, is_radian=False)



#__________________CALLBACKS________________________

    def _state_changed_callback(self, data):
        state = data.get('state', None)

        state_map = {
            1: "In Motion",
            2: "Sleeping",
            3: "Suspended",
            4: "Stopping"}
        
        state_str = state_map.get(state, "Unknown")

        
        log.debug(f"[CALLBACK] Robot state changed: {state} - {state_str}")
        self._callback_target.RARM_state_changed.emit(state)

    def set_same_position_callback(self, callback):
        """
        Register a function to call when the robot is already in the same position.
        The callback will receive the position list as an argument.
        """
        self._same_position_callback = callback

    def _error_warn_changed_callback(self, data):
        error_code = data.get('error_code', 0)
        warn_code = data.get('warn_code', 0)
        log.debug(f"[CALLBACK]  Warning code: {warn_code} Error code: {error_code}")

    def _on_feedback(data):
        cmd_id = convert.bytes_to_u16(data[0:2])
        feedback_type = data[8]
        feedback_funcode = data[9]
        feedback_taskid = convert.bytes_to_u16(data[10:12])
        feedback_code = data[12]
        feedback_us = convert.bytes_to_u64(data[13:21])
        if feedback_type == 1:
            # motion start
            print('[FB] motion task {} starts executing, funcode={}, cmd_id={}, us={}, {}'.format(feedback_taskid, feedback_funcode, cmd_id, feedback_us, datetime.datetime.now()))
        elif feedback_type == 2:
            if feedback_code == 0:
                # motion finish
                print('[FB] motion task {} execution completed, funcode={}, cmd_id={}, us={}, {}'.format(feedback_taskid, feedback_funcode, cmd_id, feedback_us, datetime.datetime.now()))
            elif feedback_code == 2:
                # motion discard
                print('[FB] motion task {} is discarded, funcode={}, cmd_id={}, us={}, {}'.format(feedback_taskid, feedback_funcode, cmd_id, feedback_us, datetime.datetime.now()))        
        elif feedback_type == 4:
            # trigger
            print('[FB] task {} is triggered, funcode={}, cmd_id={}, us={}, {}'.format(feedback_taskid, feedback_funcode, cmd_id, feedback_us, datetime.datetime.now()))
        elif feedback_type == 32:
            # other cmd start
            print('[FB] other cmd {} starts executing, funcode={}, us={}, {}'.format(cmd_id, feedback_funcode, feedback_us, datetime.datetime.now()))
        elif feedback_type == 64:
            if feedback_code == 0:
                # other cmd success
                print('[FB] other cmd {} execution success, funcode={}, us={}, {}'.format(cmd_id, feedback_funcode, feedback_us, datetime.datetime.now()))
            elif feedback_code == 1:
                # other cmd failure
                print('[FB] other cmd {} execution failure, funcode={}, us={}, {}'.format(cmd_id, feedback_funcode, feedback_us, datetime.datetime.now())) 

    

    def _estop_key_listener(self):
        log.debug("[INFO] Emergency stop listener thread started.")
        while not self.stop_event.is_set():
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'e':
                    log.critical("[E-STOP] Emergency stop triggered by SPACE key (listener thread)!")
                    self._arm.set_state(4)
                    self.stop_event.set() 

            self.stop_event.wait(0.1)



    def shutdown(self):
        log.info("[INFO] Shutting down robot...")

        if hasattr(self, 'stop_event'):
            self.stop_event.set()  # sygnalizujemy zakończenie pętli wątku
        if hasattr(self, 'estop_listener_thread') and self.estop_listener_thread.is_alive():
            self.estop_listener_thread.join()  # czekamy aż wątek zakończy działanie
            log.debug("[INFO] E-STOP listener thread stopped.")

        try:
            self._arm.set_state(4)  # state 4 = zatrzymanie robota
            self._arm.motion_enable(False)  # wyłączamy silniki
            log.info("[INFO] Robot motion disabled.")
        except Exception as e:
            log.error(f"[ERROR] Could not disable robot motion: {e}")

        try:
        
            self._arm.disconnect()
            log.info("[INFO] Robot disconnected.")
        except Exception as e:
            log.error(f"[ERROR] Could not disconnect robot: {e}")

        self.alive = False
        log.info("[INFO] Shutdown complete.")

    def offline_move(self, paths):
        # paths = [
        #     [300, 0, 150, -180, 0, 0],
        #     [300, 200, 250, -180, 0, 0],
        #     [500, 200, 150, -180, 0, 0],
        #     [500, -200, 250, -180, 0, 0],
        #     [300, -200, 150, -180, 0, 0],
        #     [300, 0, 250, -180, 0, 0],
        #     [300, 200, 350, -180, 0, 0],
        #     [500, 200, 250, -180, 0, 0],
        #     [500, -200, 350, -180, 0, 0],
        #     [300, -200, 250, -180, 0, 0],
        #     [300, 0, 350, -180, 0, 0],
        # ]
        if self.stop_event.is_set():
            log.error("Move blocked: Emergency stop is active")
            return
        
        self._arm.set_position(*paths[0], wait=False)
        _, angles = self._arm.get_servo_angle()
        self._arm.set_pause_time(0.2)

        ret = self._arm.set_servo_angle(angle=angles, is_radian=False, speed=self.max_joint_speed, wait=False)
        if ret < 0:
            log.debug(f"set_servo_angle, ret={ret}")
            return -1
        for path in paths:
            ret = self._arm.set_position(*path[:6], radius=0, is_radian=False, wait=False, speed=self.max_tcp_speed)
            if ret < 0:
                log.debug(f"set_position, ret={ret}")
                return -1
        return 0
    

    def resume(self):
        try:
            log.debug("[E-STOP] Resume.")

            self.stop_event.clear()
            self._arm.set_state(0)
            self._arm.motion_enable(enable=True)
            self._arm.set_state(0)

        except Exception as e:
            print(f"[E-STOP] Could not resume robot: {e}")

    def move_to(self, x=None, y=None, z=None, roll=None, pitch=None, yaw=None):
        pos = self._arm.position.copy()
        if x is not None:
            pos[0] = x
        if y is not None:
            pos[1] = y
        if z is not None:
            pos[2] = z
        if roll is not None:
            pos[3] = roll
        if pitch is not None:
            pos[4] = pitch
        if yaw is not None:
            pos[5] = yaw

        if self.stop_event.is_set():
            log.warning("Move blocked: Waiting for operator resume")
            return

        current_pos = self._arm.get_position()[1]
        log.debug(f"Current position: {current_pos}")
        log.debug(f"Next position: {pos}")
        if self.is_same_pos(current_pos, pos):
            log.info("SAME POSITION")
            if self._same_position_callback:      # check if callback exists
                self._same_position_callback()    # call it
            return                                # optionally skip sending a move
        else:
            log.info("DIFFERENT POSITION")

        self._arm.set_position(
            *pos,
            speed=self.max_tcp_speed,
            is_radian=False,
            wait=False
        )

    def is_same_pos(self, current_pos, next_pos, tolerance=0.001):
        # First 3: X, Y, Z — normal comparison
        for x, y in zip(current_pos[:3], next_pos[:3]):
            if abs(x - y) > tolerance:
                return False

        # Last 3: roll, pitch, yaw — angle-wrapped comparison
        for x, y in zip(current_pos[3:], next_pos[3:]):
            if self.angle_diff(x, y) > tolerance:
                return False
        return True

    def angle_diff(self, a, b):
        d = abs(a - b) % 360
        return min(d, 360 - d)


    def online_move(self, step = 0.5, rot_step= 0.5, speed=200):
        fixed_roll = 180.0
        fixed_pitch = 0.0
        fixed_yaw = 90.0
        
        self._arm.set_mode(1)  # tryb dynamiczny
        self._arm.set_state(0)
        position = self._arm.position.copy() 


        def get_key():
            key = msvcrt.getch()
            if key in (b'\x00', b'\xe0'):
                key = key + msvcrt.getch()
            return key

        try:
            while True:

          
                # Sprawdzenie resume_event
                if self.stop_event.is_set():
                    print("Move blocked: Waiting for operator resume")
                    while self.stop_event.is_set():
                        if msvcrt.kbhit():
                            key = get_key()
                            if key == b't':
                                print("[E-STOP] Resume")
                                self.resume()
                        time.sleep(0.05)
                    continue
                if msvcrt.kbhit():
                    key = get_key()
                    print(f"Pressed: {key}")

                    # Sterowanie pozycją
                    if key == b'\xe0H':  # Strzałka w górę
                        position[1] += step
                    elif key == b'\xe0P':  # Strzałka w dół
                        position[1] -= step
                    elif key == b'\xe0M':  # Strzałka w prawo
                        position[0] += step
                    elif key == b'\xe0K':  # Strzałka w lewo
                        position[0] -= step
                    elif key == b'n':   #+Z
                        position[2] += step
                    elif key == b'm':   #-Z
                        position[2] -= step
                    elif key == b'e':
                        print("[E-STOP] Emergency stop triggered")
                        self.stop_event.set()
             
                    elif key == b'q':
                        print("Exit")
                        break
                    else:
                        print("Unknow key")
                        continue



                    print(f"Position: {position[:3]} mm | Rotation: {[fixed_roll, fixed_pitch, fixed_yaw]} deg")
                    time.sleep(0.05)

                    self._arm.set_servo_cartesian(
                    [position[0], position[1], position[2], fixed_roll, fixed_pitch, fixed_yaw]
                    )

                    print(f"Position: {position[:3]} mm | RPY: {[fixed_roll, fixed_pitch, fixed_yaw]}°")
                    time.sleep(0.05)

        except KeyboardInterrupt:
            print("Keyboard inerrupt.")

        self._arm.set_mode(0)
        self._arm.set_state(0)



#_________________HANDGUIDE____________________
    def start_handguide(self):
        self.set_state(0)
        #sprawdzanie czy napewno stan się zmienił
        self.set_mode(2)

    def start_recording(self):
        self._arm.start_record_trajectory()

    def end_recording(self):
        while True:
            name = input('Please enter file name.').strip()
            if not name:
                print("File name cannot be empty!")
                continue
            break

        self._arm.stop_record_trajectory(name)

        print(f"Recording saved as '{name}'")
        
    def save_recording(self, name):
        self._arm.save_record_trajectory(name)
        #sprawdzanie czy się zapisało
        while True:
            code, status = self._arm.get_trajectory_rw_status()

            
            if status == 5:
                print(f"Recording saved successfully as '{name}'")
                break
            elif status == 6:
                print(f"Failed to save recording '{name}'")
                break
            elif status == 4:
                # zapis w toku
                print("Saving recording...", end="\r")
            else:
                print("Sth's wrong.")
                break
            
            time.sleep(0.2)



    def play_recording(self, name):
        self._arm.load_trajectory(name)
        pass
        
    #pause, resume
    def delete_recording(self, name):
        self._arm.delete_trajectory(name)

    def end_handguide(self):
        self.set_mode(0)
        time.sleep(0.1)


#________________________________UDC_________________________________

    def calculate_udc(self, three_points, center_pose):

        code, rpy_offset = self._arm.calibrate_user_orientation_offset(three_points = three_points, input_is_radian = False, return_is_radian = False)
        print(rpy_offset)
        if code != 0: 
            print("Calib error:", code)
            return

        tcp_pos = self._arm.position.copy()
        print(tcp_pos)
        code, xyz_offset = self._arm.calibrate_user_coordinate_offset(rpy_ub=rpy_offset, pos_b_uorg=tcp_pos[:3], is_radian=False)

        if code == 0:
            xyz_offset.append(rpy_offset[0])
            xyz_offset.append(rpy_offset[1])
            xyz_offset.append(rpy_offset[2])

            return code, xyz_offset
        else:
            return code

    def set_base_coordinate_system(self):
        code = self._arm.set_world_offset([0,0,0,0,0,0])
        return code

    def set_calibrated_coordinate_system(self, list):
        code = self._arm.set_world_offset(list)
        return code

    def set_micrometer_offset(self):
        code = self._arm.set_tcp_offset([0,0,0,0,90,90])
        return code
    
    def reset_tcp_offset(self):
        code = self._arm.set_tcp_offset([0,0,0,0,0,0])
        return code
    
    def set_probe_offset(self, x, y, distance, rotation):
        code = self._arm.set_tcp_offset([x-6,y+5.2,127+distance,1,0, 90])
        return code
#___________________________REDUCED_MODE____________________________
    def safety(self):
        self._arm.set_reduced_joint_range(self.joint_range, is_radian=False)
        self._arm.set_reduced_max_joint_speed(self.max_joint_speed, is_radian=False)
        self._arm.set_reduced_max_tcp_speed(self.max_tcp_speed)
        self._arm.set_reduced_tcp_boundary(self.safety_boundary)    #BOUNDARY = [x_max, x_min, y_max, y_min, z_max, z_min]
        code = self._arm.set_reduced_mode(self.on)
        if code != 0:
            log.debug(f"[SAFE MODE] Failed to {'enable' if self.on else 'disable'} reduced mode (code={code})")
            return code

        if not self.on:
            log.debug("[SAFE MODE] Reduced mode disabled")
            return 0
        else:
            log.debug("[SAFE MODE] Reduced mode enabled with given parameters")
        
        
        #self.weight = self._arm.iden_tcp_load()
        #self._arm.set_tcp_load(self.weight_cal[0],[self.weight_cal[1], self.weight_cal[2], self.weight_cal[3]], wait=True)

    def get_safety(self):
        self._arm.get_reduced_mode()
        self._arm.get_reduced_states()
    
    def get_actual_pose(self):
        position = self._arm.get_position()[1]
        return position

    def move_to_wait(self, x=None, y=None, z=None, roll=None, pitch=None, yaw=None):
        pos = self._arm.position.copy()
        if x is not None:
            pos[0] = x
        if y is not None:
            pos[1] = y
        if z is not None:
            pos[2] = z
        if roll is not None:
            pos[3] = roll
        if pitch is not None:
            pos[4] = pitch
        if yaw is not None:
            pos[5] = yaw

        if self.stop_event.is_set():
            log.warning("Move blocked: Waiting for operator resume")
            return

        current_pos = self._arm.get_position()[1]
        log.debug(f"Current position: {current_pos}")
        log.debug(f"Next position: {pos}")
        if self.is_same_pos(current_pos, pos):
            log.info("SAME POSITION")
            if self._same_position_callback:      # check if callback exists
                self._same_position_callback()    # call it
            return                                # optionally skip sending a move
        else:
            log.info("DIFFERENT POSITION")

        self._arm.set_position(
            *pos,
            speed=self.max_tcp_speed,
            is_radian=False,
            wait=True
        )

    def set_boundry_after_calib(self):
        
        self._arm.set_reduced_tcp_boundary(self.safety_boundary_after_calib)
        return 0
    






#____________________PATH_CHECKING_ALGORITHM___________

    def check_path(self, path=None):
        path = self.PATH_CONFIG

        with open(path, "r") as f:
            config = json.load(f)

        tcp_boundary = config["tcp_boundary"]
