import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R
import json


class NewPosition:
    def __init__(self, config_path = 'src/Utils/config_files/config_hand_eye.json'):

        with open(config_path, 'r') as file:
                data = json.load(file)
            

        self.R_handeye = data['R_handeye']
        self.t_handeye = data['t_handeye']
        self.R_micrometer = data['R_micrometer']
        self.t_micrometer = data['t_micrometer']


    def pose_to_matrix(self, x, y, z, roll, pitch, yaw, seq='xyz'):
        rot = R.from_euler(seq, [roll, pitch, yaw], degrees=True).as_matrix()
        T = np.eye(4)
        T[:3, :3] = rot
        T[:3, 3] = [x, y, z]
        return T

    def matrix_to_pose(self, T, seq='xyz'):
        x, y, z = T[:3, 3]

        angles = R.from_matrix(T[:3, :3]).as_euler(seq, degrees=True)
        
        # Zwracamy czyste floaty Pythonaclesr
        return [float(x), float(y), float(z), float(angles[0]), float(angles[1]), float(angles[2])]

    def new_robot_coordinates(self, rvec, tvec, robot_pos, goal, aim):


        R_obj, _ = cv2.Rodrigues(rvec)

        T_cam_obj = np.eye(4)
        T_cam_obj[:3, :3] = R_obj
        T_cam_obj[:3, 3] = tvec.flatten()

        rx, ry, rz, rr, rp, ryaw = robot_pos
        T_base_gripper = self.pose_to_matrix(rx, ry, rz, rr, rp, ryaw)

        T_gripper_cam = np.eye(4)
        T_gripper_cam[:3, :3] = self.R_handeye
        T_gripper_cam[:3, 3] = self.t_handeye

        # Macierz Baza -> Obiekt
        T_base_obj = T_base_gripper @ T_gripper_cam @ T_cam_obj

        # 4. Obliczenie celu z offsetem
        target_x, target_y, target_z_offset = goal

        T_obj_target = np.eye(4)
        T_obj_target[:3, 3] = [target_x, target_y, target_z_offset]

        # Pozycja celu w układzie bazy
        T_base_target_pos = T_base_obj @ T_obj_target

        if aim == "camera":
            T_base_final_gripper = T_base_target_pos @ np.linalg.inv(T_gripper_cam)
        else:
            T_gripper_micro = np.eye(4)
            T_gripper_micro[:3, :3] = self.R_micrometer
            T_gripper_micro[:3, 3] = self.t_micrometer
            T_base_final_gripper = T_base_target_pos @ np.linalg.inv(T_gripper_micro) 

        pose = self.matrix_to_pose(T_base_final_gripper)

        
        return pose
    

    def new_pose_0(self, pose):
        new_pose = pose[:]
        new_pose[1] = pose[1]+5
        new_pose[2] = pose[2]-5
        return new_pose
    
    def new_pose_p(self, pose):
        new_pose = pose[:]
        # for AB outside chamber
        #new_pose[1] += 71
        # for AB inside chamber
        new_pose[1] = pose[1]-60
        new_pose[2] = pose[2] -60
        return new_pose
    def new_pose_centre(self, pose):
        new_pose = pose[:] 
        # for AB outside chamber
        # new_pose[1] += 35.5
        # for AB inside chamber
        new_pose[1] = pose[1]-27.5
        new_pose[2] = pose[2] -27.5
        return new_pose
    
    def new_pose_px(self, pose):
        new_pose = pose[:] 
        
        new_pose[1] = pose[1]-60
        new_pose[2] = pose[2]-5
        return new_pose
