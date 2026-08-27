
import copy
from PySide6.QtCore import Qt, QSize, QThread, QEventLoop, QMutex, QWaitCondition, QTimer, Slot, QObject, Signal
from typing import Dict, Any
from src.Utils.config_files.measure_config import MEASURE_MODE_MAP, UNITS_MAP, Priority, State
import time
import logging
from src.Utils.calib_calculator.New_pose import NewPosition

log = logging.getLogger("GUI")


# ======== Wątek do pomiarów ========
class MeasWorker(QObject):
    command = Signal(str, str, dict) # passing dev_label, client_id, dict of method + arguments
    response = Signal(str, dict)  # passing client_id, dict of method + arguments
    releaseAll = Signal(str)  # passing client_id

    def __init__(self, dev_label:str, workers: dict):
        super().__init__()
        self.dev_label = dev_label  # MEAS
        self.mode = None
        self.owner = None
        self.device = None
        self._running = False
        self.should_continue = False
        self._workers = workers

        self.pause_delay = 1000
        self.seq = []
        self.flag = 0
        self.waiting = True
        self._paused = False

        self.current_rvec = None
        self.current_tvec = None
        self.current_robot_pose = None
        self.all_poses = None
        self.calculator = NewPosition()  # Inicjalizacja tutaj

    """ ----- interpreter ----- """
    @Slot(str, str, dict)
    def command_interp(self, dev_label:str, client_id:str, command:Dict):

        if self.dev_label != dev_label:
            return
        self.owner = client_id
        method = command.get("method")
        kwargs = command.get("kwargs", {})
        log.debug(f"command_interp dev_label: {dev_label} client_id: {client_id} method: {method} kwargs: {kwargs}")
        fn = getattr(self, method, None)
        if callable(fn):
            fn(**kwargs)
        else:
            log.error(f"Meas Worker has no method {method}.")
    """ ------------------------------------------------------- """

    """ ----- interpreter niewłasciwy ----- """
    @Slot(str, dict)
    def response_interp(self, client_id:str, response: Dict):
        if self.dev_label != client_id:
            return
        method = response.get("method")
        kwargs = response.get("kwargs", {})
        fn = getattr(self, method, None)
        if callable(fn):
            fn(**kwargs)
        else:
            log.error(f"{client_id} has no method {method}.")

    def mode_update(self, mode: str):
        self.mode = mode
        self.state = "Start Calib"  
        self._running = True 
       
    @Slot(str)
    def get_dev_config(self, dev_label:str):
        self.command.emit(dev_label, self.dev_label, {"method" : "get_config",
                                                      "kwargs" : {}})
        
    def _on_get_config(self, dev_label:str, kwargs:dict):
        log.debug(f"mode: {self.mode} dev:{dev_label} -> {kwargs}")
        
   
        self.response.emit(self.mode, {"method" : kwargs["method"], "kwargs" : kwargs["kwargs"]})
        
       
        self.response.emit("tabs/MEAS", {
            "method": "_on_get_devs_config", 
            "kwargs": {"dev_label": dev_label}
        })
        
    
    def meas_prepare(self):

        if self.mode != "Calib":
            for dev_label in MEASURE_MODE_MAP[self.mode]:
                self.command.emit(dev_label, self.dev_label, {"method" : "meas_prepare", "kwargs" : {}})
            # Everything is good.
            self.response.emit(self.mode, {"method" : "_on_meas_prepare",
                                        "kwargs" : {
                                            "status" : True}})
            self.state = "MEASURING"
            self.steps = {dev: False for dev in MEASURE_MODE_MAP[self.mode]}
            # START
            self.switch_on_off(True)
        else:
            for dev_label in MEASURE_MODE_MAP[self.mode]:
                #self.command.emit(dev_label, self.dev_label, {"method" : "set_base_system", "kwargs" : {}})
                self.command.emit(dev_label, self.dev_label, {"method" : "_meas_prepare_calib", "kwargs" : {}})
            # Everything is good.
            self.response.emit(self.mode, {"method" : "_on_meas_prepare",
                                        "kwargs" : {
                                            "status" : True}})
            self.state = "IDLE"
            self.steps = {dev: False for dev in MEASURE_MODE_MAP[self.mode]}
            # START
            self.switch_on_off(True)

    @Slot(bool)
    def switch_on_off(self, on: bool):
        try:
            self._running = on
            if on:
                self.response.emit("tabs/MEAS", {"method": "_on_toggled", "kwargs": {"running": on}}) # tabs/MEAS
                self.response.emit(self.mode, {"method": "_on_started", "kwargs": {}})
                log.info(f"MeasWorker sequence {self.mode} starting ...")
                # --- sekwencja pomiarowa ---
                self.do_next_event() # FF_az
            else:
                log.info("MeasWorker stopped")
                self.response.emit("tabs/MEAS", {"method": "_on_toggled", "kwargs": {"running": on}}) # tabs/MEAS
                if self.state != "FINISHED": # It means something failed
                    self.state = "STOPPED"
                    if self._paused:
                        self.pause_on_off(False)
                    self.do_next_event()
                    self.response.emit(self.mode, {"method" : "_on_stopped", "kwargs" : {}})
                    self.response.emit("tabs/MEAS", {"method" : "_on_stopped", "kwargs" : {}})
                else:
                    # zwolnij urządzenia
                    self.response.emit(self.mode, {"method" : "_on_finished", "kwargs" : {}})
                    self.response.emit("tabs/MEAS", {"method" : "_on_finished", "kwargs" : {}})

        except Exception as e:
            log.error(f"can not measure: {e}")

    @Slot(bool)
    def pause_on_off(self, on: bool):
        self._paused = on
        if on:
            log.info("Pause requested")
            self.response.emit(self.owner, {"method": "_on_pause_toggled", "kwargs": {"pausing": on}})
            self.response.emit(self.mode, {"method": "_on_paused", "kwargs": {}})
        else:
            log.info("Resume requested")
            self.response.emit(self.owner, {"method": "_on_pause_toggled", "kwargs": {"pausing": on}})
            self.response.emit(self.mode, {"method": "_on_resumed", "kwargs": {}})
    
    def _on_update(self, dev_label:str, dev_data:dict):
        self.response.emit(self.mode, {"method" : dev_data["method"], "kwargs" : dev_data["kwargs"]})

    def _on_event_done(self, dev_label:str, result:bool):
        if result:
            self.steps[dev_label] = True # Register the device has finished its step
            self.do_next_event()
        else:
            self.switch_on_off(False)
    
    def _out_of_steps(self, dev_label:str):
        self.state = "FINISHED_SCAN"
        self.do_next_event()
    
    def next_scan(self):
        self.state = "NEXT_SCAN"
        self.do_next_event()
    
    def no_scan(self):
        self.state = "FINISHED"
        self.command.emit("RARM", self.dev_label, {"method" : "switch_copolar", "kwargs" : {}})
        self.do_next_event()
    
   
    @Slot(str)
    def do_next_event(self):
        if self._paused:
            #log.info("Worker paused, re-emit do_next_event after delay")
            QTimer.singleShot(self.pause_delay, lambda: self.do_next_event())
            return
        match self.mode:
            case "PNF":
                match self.state:
                    case "MEASURING":
                        if not self.steps["RARM"]:
                            self.command.emit("RARM", self.dev_label, {"method" : "do_next_event", "kwargs" : {}})
                            return
                        elif not self.steps["VNA"]:
                            self.command.emit("VNA", self.dev_label, {"method" : "do_next_event", "kwargs" : {}})
                            return
                        else:
                            self.state = "NEXT"
                            self.do_next_event()
                            return
                    case "NEXT":
                        self.steps = {dev: False for dev in MEASURE_MODE_MAP[self.mode]}
                        self.state = "MEASURING"
                        self.do_next_event()
                        return
                    case "FINISHED_SCAN":
                        log.info("Finished scanning!")
                        self.response.emit(self.mode, {"method": "_on_scan_finished", "kwargs": {}})
                        return
                    case "NEXT_SCAN":
                        log.info("Started next scan!")
                        self.state = "MEASURING"
                        self.steps = {dev: False for dev in MEASURE_MODE_MAP[self.mode]}
                        self.command.emit("RARM", self.dev_label, {"method" : "switch_crosspolar", "kwargs" : {}})
                        self.command.emit("RARM", self.dev_label, {"method" : "do_next_event", "kwargs" : {}})
                        return
                    case "FINISHED":
                        log.info("Finished Measuring!")
                        self.switch_on_off(False)
                        # finish measurement
                        return
                    case "STOPPED":
                        log.critical("Measurement stopped!")
                        # measurement failed somewhere
                        return
            case "FF_az":
                match self.state:
                    case "MEASURING":
                        if not self.steps["TIC_AZ"]:
                            self.command.emit("TIC_AZ", self.dev_label, {"method" : "do_next_event", "kwargs" : {}})
                            return
                        elif not self.steps["VNA"]:
                            self.command.emit("VNA", self.dev_label, {"method" : "do_next_event", "kwargs" : {}})
                            return
                        else:
                            self.state = "NEXT"
                            self.do_next_event()
                            return
                    case "NEXT":
                        self.steps = {dev: False for dev in MEASURE_MODE_MAP[self.mode]}
                        self.state = "MEASURING"
                        self.do_next_event()
                        return
                    case "FINISHED":
                        log.info("Finished Measuring!")
                        #self.command.emit("RARM", self.dev_label, {"method":"move_to_start", "kwargs":{}})
                        self.switch_on_off(False)
                        # finish measurement
                        return
                    case "STOPPED":
                        log.critical("Measurement stopped!")
                        # measurement failed somewhere
                        return
            case "Calib":
                match self.state:
                    case "ASK_FOR_DATA_TO_START":
                        self.current_rvec = None
                        self.current_robot_pose = None
                    
                        self.command.emit("CAM", self.dev_label, {"method": "_send_frame_to_meas", "kwargs": {}})
                        self.command.emit("RARM", self.dev_label, {"method": "_get_position", "kwargs": {}})
                        self.state = "WAITING_FOR_DATA"
                        self.is_verification = False

                    case "CALCULATE_POSES_FOR_CALIBTATION":
                        # pierwsza wspr=lrzedna to x 
                        pose_start = self.calculator.new_robot_coordinates(self.current_rvec, self.current_tvec, self.current_robot_pose, [0,0,0], "micro") #punkt
                        
                        self.all_poses = [
                            self.calculator.new_pose_0(pose_start),
                            self.calculator.new_pose_px(pose_start),
                            self.calculator.new_pose_p(pose_start),
                            self.calculator.new_pose_centre(pose_start)
                        ]
                        self.response.emit("tabs/Calib", {"method": "update_new_pose", "kwargs": {"all_poses": self.all_poses}})
                        log.info("New poses calculated")
                        self.pose_counter = 0
                        self.measurements = []
                        #self.do_next_event()

                    case "MOVE":
                        if self.pose_counter < len(self.all_poses):
                            target = self.all_poses[self.pose_counter]
                            log.info(f"STEP {self.pose_counter + 1}/{len(self.all_poses)}: Move to {target}")
                            
                            self.command.emit("RARM", self.dev_label, {
                                "method": "_move_to_calib",
                                "kwargs": {"is_verification":self.is_verification,"x": target[0], "y": target[1], "z": target[2], 
                                        "roll": target[3], "pitch": target[4], "yaw": target[5]}
                            })

                            self.state = "WAIT_FOR_ROBOT"
                        else:
                            if self.is_verification:
                                num_new_points = len(self.all_poses)
                                new_measurements = [float(m) for m in self.measurements[-num_new_points:]]
                                max_error = 0
                                for i in range(len(new_measurements) - 2):
                                    diff = abs(new_measurements[i+1] - new_measurements[i])
                                    max_error = max(max_error, diff)
            
                                log.info(f"Veryfication max error: {max_error:.4f}")

                                TOLERANCE = 0.05 

                                if max_error <= TOLERANCE:
                                    log.info("Calibration completed successfully!")
                                    self.state = "FINISH_CALIB"
                                else:
                                    log.warning(f"Too big error, repeat calibration")
                                    self.measurements = new_measurements 
                                    self.state = "FINISH_CALIB"
                                    
                            else:
                                self.state = "CALCULATE_NEW_COORDINATE_SYSTEM"
                                self.do_next_event()

                    case "MEASURE":

                        self.command.emit("MICRO", self.dev_label, {
                            "method": "_send_data_to_meas", # Nazwa metody u Twojego workera
                            "kwargs": {}
                        })
                        self.state = "WAITING_FOR_MICROMETER"
                    
                    case "RETRACT":
                        if self.pose_counter <= 2:
                            target = self.all_poses[self.pose_counter]
                            
                            self.command.emit("RARM", self.dev_label, {
                                "method": "_move_to_retract", 
                                "kwargs": {"is_verification":self.is_verification, "x": target[0], "y": target[1], "z": target[2] ,"roll": target[3], "pitch": target[4], "yaw": target[5]}
                                })
                            self.pose_counter += 1
                        else:
                            self.pose_counter += 1
                            self.state = "MOVE"
                            self.do_next_event()
                        
                    case "CALCULATE_NEW_COORDINATE_SYSTEM":
                        
                        if len(self.measurements) < 3:
                            return

                        m1 = self.measurements[0]
                        m2 = self.measurements[1]
                        m3 = self.measurements[2]
                        m4 = self.measurements[3]
                        self.all_poses[3][3] = float(m4)
                        if not self.is_verification:
                            corrected_points = [
                                self.apply_micrometer_correction(self.all_poses[0], m1, m1),
                                self.apply_micrometer_correction(self.all_poses[1], m2, m1),
                                self.apply_micrometer_correction(self.all_poses[2], m3, m1)
                            ]
                        print(corrected_points)
                        self.is_verification = True
                        self.measurements = [] 
                        
                        self.command.emit("RARM", self.dev_label, {
                            "method": "_setup_micrometer_reference",
                            "kwargs": {}
                        })
                        
                        self.command.emit("RARM", self.dev_label, {
                            "method": "_setup_environment",
                            "kwargs": {"three_points": corrected_points, "center_pose": self.all_poses[3]}
                        })
                        self.state = "ACCEPT_NEW_COORDINATE"

                    case "SET_NEW_COORDINATE_SYSTEM":
                        self.command.emit("RARM", self.dev_label, {
                            "method": "_set_new_coordinate_system",
                            "kwargs": {"list": self.new_coordinate}
                        })
                        
                        self.command.emit("RARM", self.dev_label, {
                            "method": "set_calibrated",
                            "kwargs": {"calibrated": True}
                        })
                        log.info("New coordinate system accepted")
                        
                        

                    case "VERIFY_CALIBRATION":

                        self.command.emit("RARM", self.dev_label, {
                        "method": "_reset_state",
                        "kwargs": {}
                        })

                        self.all_poses = [
                            [-27.5-5, -27.5+5, 0, 0, 0 ,0],
                            [27.5+5, -27.5+5, 0, 0, 0 ,0],
                            [27.5+5, 27.5+5, 0, 0, 0 ,0],
                            [0,0,0,0,0,0]
                        ]
                        self.pose_counter = 0
                        self.state = "MOVE"
                        self.do_next_event()

                    case "ANTENNA_TCP":
                        self.command.emit("RARM", self.dev_label, {
                            "method": "_change_tcp_probe",
                            "kwargs": {}
                        })
                    case "FINISHED":
                        self.switch_on_off(False)


                        

    ''' Calibration methods '''

    def on_start_measure(self):
        # Change state after pose_est_btn pressed
        self.state = "ASK_FOR_DATA_TO_START"
        self.do_next_event()

    def on_received_camera_data(self, frame, rvec=None, tvec=None, distance=0.0):
        # Change current rvec, tvce, update labels in GUI
        self.current_rvec = rvec
        self.current_tvec = tvec

        self.response.emit("tabs/Calib", {
            "method": "_update_video_feed",
            "kwargs": {"frame": frame, "distance": distance}
        })
        # We are checking if we can go further
        self.check_calibration_sync()

    def on_received_robot_pose(self, pose):
        # Change current robot pose update labels in GUI
        self.current_robot_pose = pose
        self.response.emit("tabs/Calib", {"method": "update_current_pose","kwargs": {"pose": self.current_robot_pose}})
        # We are checking if we can go further
        self.check_calibration_sync()

    def check_calibration_sync(self):
        # We check if we have complete data for the current step
        if self.current_rvec is not None and self.current_robot_pose is not None and self.current_tvec is not None:
            self.state = "CALCULATE_POSES_FOR_CALIBTATION"
            self.do_next_event()
    
    def on_change_status_move(self):
        if self.all_poses is not None:
            self.state = "MOVE"
            self.do_next_event()


    def on_recived_new_coordinate_system(self, new_coordinate):
        self.new_coordinate = new_coordinate
        self.response.emit("tabs/Calib", {
            "method": "on_update_current_coordinate", 
            "kwargs": {"new_coordinate": self.new_coordinate}
        })


    def on_move_finished(self, status):
        if status == "success":
            if self.state == "WAIT_FOR_ROBOT":
                self.state = "MEASURE"
                self.do_next_event()
        else:
            log.error("Robot reported a motion error! Aborting calibration")
            self.state = "IDLE"

    def on_calibration_finished(self, status):
        if status == "success":
            if self.state == "ANTENNA_TCP":
                self.state = "FINISHED"
                self.do_next_event()
        else:
            log.error("Robot reported a motion error! Aborting calibration")
            self.state = "IDLE"

    def on_move_retract_finished(self, status):
        if status == "success":
            if self.state == "RETRACT":
                self.state = "MOVE"
                self.do_next_event()
        else:
            log.error("Robot reported a motion error! Aborting calibration")
            self.state = "IDLE"

    def on_measurement_received(self, value):
        log.info(f"Recived data from micrometer: {value}")

        self.measurements.append(value)
        self.state = "RETRACT"
        self.do_next_event()

    def apply_micrometer_correction(self,point, m_val, m_ref):
        new_point = point.copy()
        val = abs(float(m_val))
        ref = abs(float(m_ref))
        correction = val - ref
        new_point[0] -= correction
        return new_point


    def on_accept_new_cs(self):
        self.state = "SET_NEW_COORDINATE_SYSTEM"
        self.do_next_event()

    def on_change_status_veryfication(self):
        self.state = "VERIFY_CALIBRATION"
        self.do_next_event()

    def on_change_tcp_probe(self):
        if self.state == "FINISH_CALIB":
            self.state = "ANTENNA_TCP"
            self.do_next_event()
