from geometry_msgs.msg import Twist
from spot_interfaces.msg import JointAngles

import motion_control.lib.motion_utils as mu
from motion_control.lib.spot_kinematics import SpotKinematics

import numpy as np

class TrotManager():
    def __init__(self) -> None:
        self._phase = 0
        self._walking_state = 0
        self._num_legs = 4

        self._kinematics = SpotKinematics()
        self._stand_foot_pos = self._kinematics.get_foot_coords()
        self._target_foot_pos = self._kinematics.get_foot_coords().copy()

        # Slow trot parameters
        self._leg_up_height = 0.04
        self._leg_stride = 0.08
        self._balance_roll = 0.1
        self._balance_pitch = 0.08

        # FL=0, FR=1, BL=2, BR=3
        self._pair_a = [0, 3]  # FL + BR
        self._pair_b = [1, 2]  # FR + BL

        self._kinematics.set_body_angles(body_pitch_rad=self._balance_pitch, body_roll_rad=self._balance_roll)

    def is_standing(self, cmd: Twist) -> bool:
        if abs(cmd.linear.x) < 0.5:
            if self._walking_state == 3:
                return True
            self._walking_state = 2
        return False

    def new_joint_angles(self, current_angles: JointAngles, cmd: Twist, max_angle_delta: float) -> JointAngles:
        if self._walking_state == 2 or self._walking_state == 3:
            return self.to_stand_angles(current_angles, max_angle_delta)
        else:
            return self.trot_angles(current_angles, cmd, max_angle_delta)

    def to_stand_angles(self, current_angles: JointAngles, max_angle_delta: float) -> JointAngles:
        self._kinematics.set_body_angles(body_pitch_rad=0.0, body_roll_rad=0.0)
        target_angles = self._kinematics.get_joint_angles()
        target_joints = mu.np_array_to_joint_angles(target_angles)
        if mu.joint_angles_match(current_angles, target_joints):
            self._walking_state = 3
            self._target_foot_pos = self._stand_foot_pos.copy()
        self._kinematics.set_foot_coords(self._target_foot_pos)
        return self.get_next_joint_angles(current_angles, max_angle_delta)

    def trot_angles(self, current_angles: JointAngles, cmd: Twist, max_angle_delta: float) -> JointAngles:
        self.update_trot_phase(current_angles)
        return self.get_next_joint_angles(current_angles, max_angle_delta)

    def update_trot_phase(self, current_angles: JointAngles) -> None:
        target_angles = self._kinematics.get_joint_angles()
        target_joints = mu.np_array_to_joint_angles(target_angles)

        if not mu.joint_angles_match(current_angles, target_joints):
            return

        if self._phase == 0:
            self._phase = 1
            for leg in self._pair_a:
                self._target_foot_pos[leg, 1] += self._leg_up_height
                self._target_foot_pos[leg, 0] += self._leg_stride / 2
            self._kinematics.set_body_angles(body_roll_rad=self._balance_roll, body_pitch_rad=self._balance_pitch)

        elif self._phase == 1:
            self._phase = 2
            for leg in self._pair_a:
                self._target_foot_pos[leg, 1] = self._stand_foot_pos[leg, 1]
                self._target_foot_pos[leg, 0] += self._leg_stride / 2

        elif self._phase == 2:
            self._phase = 3
            for leg in range(self._num_legs):
                self._target_foot_pos[leg, 0] -= self._leg_stride / 2

        elif self._phase == 3:
            self._phase = 4
            for leg in self._pair_b:
                self._target_foot_pos[leg, 1] += self._leg_up_height
                self._target_foot_pos[leg, 0] += self._leg_stride / 2
            self._kinematics.set_body_angles(body_roll_rad=-self._balance_roll, body_pitch_rad=self._balance_pitch)

        elif self._phase == 4:
            self._phase = 5
            for leg in self._pair_b:
                self._target_foot_pos[leg, 1] = self._stand_foot_pos[leg, 1]
                self._target_foot_pos[leg, 0] += self._leg_stride / 2

        elif self._phase == 5:
            self._phase = 0
            for leg in range(self._num_legs):
                self._target_foot_pos[leg, 0] -= self._leg_stride / 2
            self._kinematics.set_body_angles(body_roll_rad=self._balance_roll, body_pitch_rad=self._balance_pitch)

        self._kinematics.set_foot_coords(self._target_foot_pos)

    def get_next_joint_angles(self, current_angles: JointAngles, max_angle_delta: float) -> JointAngles:
        target_angles = self._kinematics.get_joint_angles()
        target_joints = mu.np_array_to_joint_angles(target_angles)
        return mu.multi_joint_one_step_interp(current_angles, target_joints, max_angle_delta)
