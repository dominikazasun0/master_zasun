
import logging
import threading
import copy
from enum import IntEnum
from PySide6.QtCore import Qt, QSize, QThread, QEventLoop, QTimer, Slot, QObject, Signal
from fontTools.misc.cython import returns
from src.Drivers.Arm_Driver.Robotic_Arm_Driver import RA
from src.Workers.DEV_worker import DEV_Worker, WorkerState
import time
log = logging.getLogger("GUI")

class RarmWorker(DEV_Worker):

    ready = Signal(str, bool)        # passing dev_label, response
    shutdown = Signal(str, bool)     # passing dev_label, response
    response = Signal(str, dict)     # passing client_id, dict of method + arguments
    progress = Signal(str)           # passing message
    stateChanged = Signal(int)       # passing new state number
    faultOccurred = Signal(str, str) # passing dev_label, message
    heartbeat = Signal(str)          # passing dev_label
    RARM_state_changed = Signal(int)

    def __init__(self, dev_label:str):
        super().__init__(dev_label)
        self.d_x = 1
        self.d_y = 1
        self.N_x = 1
        self.N_y = 1
        self.non_cal_start_pos = {
            "x" : 500,
            "y" : 0,
            "z" : 600,
            "roll" : -90,
            "pitch" : -90,
            "yaw" : -90
        }
        self.cal_start_pos = {
            "x" : 0,
            "y" : 0,
            "z" : 0,
            "roll" : 0,
            "pitch" : 0,
            "yaw" : 0
        }
        
        self.start_pos_calib = {
            "x" : 649.5,
            "y" : -3.2,
            "z" : 625.6,
            "roll" : -90,
            "pitch" : -90,
            "yaw" : 0
        }
        '''
        self.start_pos_calib = {
            "x" : -495,
            "y" : -22,
            "z" : 645,
            "roll" : -50,
            "pitch" : -88,
            "yaw" : 142
        }
        '''
        self.cal_pos_matrix = [[(-1,1),(0,1),(1,1)],
                           [(-1,0),(0,0),(1,0)],
                           [(-1,-1),(0,-1),(1,-1)]]
        self.non_cal_pos_matrix = None
        self.copolar_rotation = 0
        self.ant_dist = 5 #cm
        self.current_pol = "copolar"
        self.current_index = None
        self.target_index = None
        self.RARM_state_changed.connect(self.state_changed)
        self.moving = False
        self.calibrated = False


    def set_device(self, dev_model:str, dev_address:str):
        self.model = dev_model
        self.device = RA(dev_address)
        self.device.register_callback_target(self)
        self.device.arise()
        self.device.set_same_position_callback(self._finished_step)
        self.calibrated = False

    @Slot(str, str, str)
    def connect(self, dev_label:str, dev_model:str, dev_address:str):
        log.debug(f"dev_label {dev_label} model {dev_model}")
        if self.dev_label != dev_label:
            return
        try:
            self.set_device(dev_model, dev_address)
            if not self.device:
                raise Exception("no device")
            status = self.device.is_connected()
            if status:
                log.debug(f"{dev_label} model {self.model} connected.")
                self.calibrated = False
                self.ready.emit(self.dev_label, True)
            else:
                log.error(f"Connection to Robotic Arm {self.model} failed.")
                self.ready.emit(self.dev_label, False)
        except Exception as e:
            log.error(f"Connection failed: {e}")
            self.ready.emit(self.dev_label, False)
    
    @Slot(str)
    def disconnect(self, dev_label:str):
        if self.dev_label != dev_label:
            return
        try:
            #self.stop()
            self.device.shutdown()
            log.debug(f"{dev_label} model {self.model} disconnected.")
            self.shutdown.emit(self.dev_label, True)
        except Exception as e:
            log.error(f"Disconnect failed: {e}")
            self.shutdown.emit(self.dev_label, False)
    
    def get_state(self):
        if self.owner != "tabs/RARM":
            return
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        state = self.device.get_state()
        self.response.emit(self.owner, {"method" : "_on_get_state", "kwargs": {"state" : state}})
    
    def state_changed(self, state:int): # THIS IS A POTENTIAL PROBLEM
        if (self.moving is True) and (state == 2):
            self.moving = False
            self._finished_step()
        elif (self.moving is True) and (state == 4):
            self.moving = False
            self._step_failed()
        if self.owner == "tabs/RARM":
            self.response.emit(self.owner, {"method" : "_on_get_state", "kwargs": {"state" : state}})
    
    def go_home(self):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        self.device.safe_home()
    
    def move_to_start(self):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        if any(v is None for v in self.non_cal_start_pos.values()):
            log.error("Not all values given.")
            return
        if any(v is None for v in self.cal_start_pos.values()):
            log.error("Not all values given.")
            return
        order = ("x", "y", "z", "roll", "pitch", "yaw")
        if self.calibrated:
            self.device.move_to(*(self.cal_start_pos[k] for k in order))
        else:
            self.device.move_to(*(self.non_cal_start_pos[k] for k in order))
        self.moving = True
        self.target_index = None
        self.current_index = None

    def move_to_calib_start(self):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        if any(v is None for v in self.start_pos_calib.values()):
            log.error("Not all values given.")
            return
        order = ("x", "y", "z", "roll", "pitch", "yaw")
        self.device.move_to(*(self.start_pos_calib[k] for k in order))
        self.moving = True
        self.target_index = None
        self.current_index = None
    
    def _change_tcp_probe(self):
        try:
            self.ant_dist = float(self.ant_dist)
            x, y, z, roll, pitch, yaw = self.device.get_actual_pose() 
            self.device.move_to_wait(x, y, z-180-(self.ant_dist*10), roll, pitch, yaw)
            print(self.ant_dist*10, float(self.copolar_rotation))
            self.device.set_probe_offset(0, 0, self.ant_dist*10, float(self.copolar_rotation))
            
            self.device.set_state(0)
            self.device.move_to_wait(0, 0, 0, 0, 0, 0)

            self.response.emit(self.owner, {
            "method": "on_calibration_finished", 
            "kwargs": {"status": "success"}
            })
        except Exception as e:
            log.error(str(e))
        
    
    @Slot(int,int)
    def move_to(self, target):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        try:
            log.info(f"Moving to: {target}")
            self.target_index = target
            self.moving = True
            log.info(f"Calibration:{self.calibrated}")
            if self.calibrated:
                self.device.move_to(*self.cal_pos_matrix[target[0]][target[1]])
            else:
                self.device.move_to(*self.non_cal_pos_matrix[target[0]][target[1]])
        except Exception as e:
            log.error(str(e))
            self.calibrated = False
            self._set_base_system()
    
    
    def _move_to_calib(self, is_verification, x, y, z, roll, pitch, yaw):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return # Pamiętaj o return, żeby nie kontynuować przy błędzie
        if is_verification:
            self.device.move_to_wait(x, y, z-10, roll, pitch, yaw)
            self.device.move_to_wait(x, y, z, roll, pitch, yaw)
        else:
            self.device.move_to_wait(x-10, y, z, roll, pitch, yaw)
            self.device.move_to_wait(x, y, z, roll, pitch, yaw)
        time.sleep(1)
        self.response.emit(self.owner, {
        "method": "on_move_finished", 
        "kwargs": {"status": "success"}
        })
    
    def _move_to_retract(self, is_verification,x, y, z, roll, pitch, yaw):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        if is_verification:
            self.device.move_to_wait(x, y, z-10, roll, pitch, yaw)
        else:
            self.device.move_to_wait(x-10, y, z, roll, pitch, yaw)
        self.response.emit(self.owner, {
        "method": "on_move_retract_finished", 
        "kwargs": {"status": "success"}
        })
        
        

    def _finished_step(self):
        self.current_index = self.target_index
        self.response.emit("tabs/RARM", {"method" : "_update_robot_position",
                                        "kwargs" : {"pos" : self.current_index}})
        if self.owner == "tabs/RARM" and not self._running: # If it is a single move
            return
        self.state = WorkerState.NEXT
        QTimer.singleShot(0, self.do_next_event)

    def _step_failed(self):
        log.error(f"Move to {self.target_index} failed!")
        if self.owner == "tabs/RARM":
            self.switch_on_off(False)
        else:
            self.response.emit(self.owner, {"method": "_on_event_done", "kwargs": {"dev_label" : self.dev_label,"result" : False}})

    def resume(self):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        self.device.resume()
    
    def run_demo(self, mov_matrix, x, roll, pitch, yaw):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        paths = [[x, y, z, roll, pitch, yaw]
                        for row in mov_matrix
                        for (y, z) in row]
        print(paths)
        self.device.offline_move(paths)
    
    def get_config(self):
        try:
            log.debug(f"get_rarm_params: dev_label {self.dev_label}, owner {self.owner}")
            self.response.emit("tabs/RARM", {"method": "_on_rarm_pos_acquired",
                                            "kwargs": {"pos": self.current_index}})
            if self.owner != "tabs/RARM" and self.owner != "tabs/MEAS/Calib":
                self.state = WorkerState.SET_POSITION
                log.debug(f"get_config: dev_label {self.dev_label} d_x={self.d_x}, d_y={self.d_y}, (i,j)={self.current_index}")
                
                self.response.emit(self.owner, {"method": "_on_get_config",
                                                "kwargs": {"dev_label": self.dev_label, 
                                                           "kwargs": {"method" : "_on_get_config",
                                                                      "kwargs" : {
                                                                          "dev_label": self.dev_label,
                                                                          "dev_config":{
                                                                              "d_x" : self.d_x,
                                                                              "d_y" : self.d_y,
                                                                              "pos" : self.current_index,
                                                                              "pos_matrix" : self.cal_pos_matrix,
                                                                              "copolar_rotation" : self.copolar_rotation,
                                                                              "ant_dist" : self.ant_dist,
                                                                              "calibrated" : self.calibrated}}}}})
        except Exception as e:
            log.error(f"Error in get_config: {e}")

    def switch_on_off(self, on: bool):
        if (self.device is None) or (not self.device.is_connected()):
            log.error("Robot is not set")
            self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": False}})
            return
        try:
            self._running = on
            if on:
                self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": on}})
                log.info("Robot started")
                # --- start ---
                self.state = WorkerState.SET_POSITION
            else:
                log.info("Robot stopped")
                self.response.emit(self.owner, {"method": "_on_toggled", "kwargs": {"running": on}})
                # --- stop ---
                self.state = WorkerState.FINISHED
                # self.owner = None
                # self.client_id = None

            self.do_next_event()

        except Exception as e:
            log.error(f"rarm_worker can not move: {e}")

    def configure(self, d_x, d_y, N_x, N_y, start_pos, ant_dist, current_index, mov_matrix, copolar_rotation):
        self.d_x = d_x
        self.d_y = d_y
        self.N_x = N_x
        self.N_y = N_y
        self.current_index = current_index
        self.non_cal_start_pos = start_pos
        self.ant_dist = ant_dist
        self.cal_pos_matrix = [
            [
                [y, -z, 0, 0, 0, copolar_rotation]
                for (y, z) in row
            ]
            for row in mov_matrix
        ]
        self.non_cal_pos_matrix = [
            [
                [start_pos["x"], -y + start_pos["y"], z + start_pos["z"], start_pos["roll"], start_pos["pitch"], start_pos["yaw"]]
                for (y, z) in row
            ]
            for row in mov_matrix
        ]
        self.copolar_rotation = copolar_rotation
        self.cal_start_pos["yaw"] = copolar_rotation
        # self.move_to(start_pos["x"], start_pos["y"], start_pos["z"],
        #              start_pos["roll"], start_pos["pitch"], start_pos["yaw"])
    def switch_crosspolar(self):
        if self.calibrated:
            cross_pitch = self.cal_start_pos["yaw"] + 90 #Its yaw becuase of coordinate system transfer
            for row in self.cal_pos_matrix:
                for point in row:
                    point[5] = cross_pitch
        else:
            cross_pitch = self.non_cal_start_pos["pitch"] + 90
            for row in self.non_cal_pos_matrix:
                for point in row:
                    point[4] = cross_pitch
        self.move_to_start()
        self.state = WorkerState.SET_POSITION

    def switch_copolar(self):
        if self.calibrated:
            for row in self.cal_pos_matrix:
                for point in row:
                    point[5] = self.cal_start_pos["yaw"]
        else:
            for row in self.non_cal_pos_matrix:
                for point in row:
                    point[4] = self.cal_start_pos["pitch"]
        self.move_to_start()
            
    def meas_prepare(self):
        self.current_pol = "copolar"
        self.move_to_start()
        self.state = WorkerState.SET_POSITION
    
    def _meas_prepare_calib(self):
        code = self._set_base_system()
        if code == 0:
            self.device.set_state(0)
            code1 = self.reset_tcp_offset()
            self.device.set_state(0)
            if code1 == 0:
                self.move_to_calib_start()
                self.state = WorkerState.SET_POSITION
    
    def _reset_state(self):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        code = self.device.set_state(0)
        return code
    
    def reset_tcp_offset(self):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        code = self.device.reset_tcp_offset()
        return code
    
    def _reset_settings(self):
        self.calibrated = False
        code = self._set_base_system()
        if code == 0:
            self.device.set_state(0)
            code1 = self.reset_tcp_offset()
            self.device.set_state(0)
    
    def _set_base_system(self):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        code = self.device.set_base_coordinate_system()
        return code

    def _set_new_coordinate_system(self, list):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        code = self.device.set_calibrated_coordinate_system(list)
        return code
    
    def _set_calibrated_boundry(self):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        code = self.device.set_boundry_after_calib()
        self.device.set_state(0)
        return code
    
    def set_calibrated(self, calibrated:bool):
        if not self.device.is_connected():
            log.error(f"{self.dev_label} is not set.")
            return
        self._set_calibrated_boundry()
        self.calibrated = calibrated

    def next_in_sequ(self):
        self.state = WorkerState.SET_POSITION
        if self._running: # If it is a full run
            self.do_next_event()
        elif self.owner == "tabs/RARM": # If it is a single move
            return
        else: # If it is a measurement
            self.response.emit(self.owner, {"method": "_on_update",
                                            "kwargs": {
                                                "dev_label": self.dev_label,
                                                "dev_data": {
                                                    "method": "_on_position_acquired",
                                                    "kwargs": {"pos": self.current_index}}}})
            self.response.emit(self.owner, {"method": "_on_event_done",
                                            "kwargs": {
                                                "dev_label" : self.dev_label,
                                                "result" : True}})

    def do_next_event(self):
        log.debug(f"Current pos: {self.current_index}")
        #log.debug(f"{self.dev_label} _do_next_event for {self.owner} _running {self._running}")
        if self.device is None:
            log.error("Robot is not set")
            return
        log.debug(f"current pos: {self.current_index}")
        if self.calibrated and self.cal_pos_matrix is None:
            log.error("NO MEASUREMENT POINTS LOADED")
            return
        if not self.calibrated and self.non_cal_pos_matrix is None:
            log.error("NO MEASUREMENT POINTS LOADED")
            return
        log.debug(f"[RARMWorker] DO NEXT EVENT, {self.state}")
        try:
            match self.state:
                case WorkerState.SET_POSITION:
                    if self.current_index is not None:
                        i, j = self.current_index
                    if self.current_index is None:
                        self.move_to((0,0)) # move from start point (calibration) to first meas point
                    # Moving left-to-right on even rows
                    elif i % 2 == 0:
                        if((i == self.N_y - 1) and (j == self.N_x - 1)):
                            self.state = WorkerState.FINISHED
                            self.response.emit(self.owner, {"method" : "_out_of_steps", "kwargs" : {"dev_label" : self.dev_label}}) # end of matrix
                        elif j < self.N_x - 1:
                            self.move_to((i, j+1)) # move right
                        else:
                            if i < self.N_y - 1:
                                self.move_to((i+1, j)) # move down

                    # Moving right-to-left on odd rows
                    else:
                        if((i == self.N_y - 1) and (j == 0)):
                            self.state = WorkerState.FINISHED
                            self.response.emit(self.owner, {"method" : "_out_of_steps", "kwargs" : {"dev_label" : self.dev_label}}) # end of matrix
                        elif j > 0:
                            self.move_to((i, j-1)) # move left
                        else:
                            if i < self.N_y - 1:
                                self.move_to((i+1, j)) # move down

                case WorkerState.NEXT:
                    self.next_in_sequ()

                case WorkerState.FINISHED:
                    self.state = WorkerState.IDLE
                    self.owner = None

        except Exception as e:
            log.error(str(e))
            self.calibrated = False
            self._set_base_system()
            if self.owner == "tabs/RARM":
                self.switch_on_off(False)
            else:
                self.response.emit(self.owner, {"method": "_on_event_done", "kwargs": {"dev_label" : self.dev_label,"result" : False}})


    def _get_position(self):
        current_pose = self.device.get_actual_pose()
        self.response.emit(self.owner, {"method": "on_received_robot_pose", "kwargs": {"pose": current_pose}})
            
    def _setup_environment(self, three_points, center_pose):
        
        if not three_points or not isinstance(three_points, list):
            return
        code, result = self.device.calculate_udc(three_points, center_pose)
        if code == 0 :
            self.response.emit(self.owner,{"method": "on_recived_new_coordinate_system", "kwargs": {"new_coordinate": result}})
        else:
            return


    def _setup_micrometer_reference(self):
        if self.device is None:
            log.error("Robot is not set")
            return
        result = self.device.set_micrometer_offset()
        return result

    def stop(self):
        """Zatrzymaj wszystkie akcje workera"""
        try:
            self.switch_on_off(False)
        except Exception:
            pass
        log.debug("RarmWorker: shutdown done")
