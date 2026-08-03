from rclpy import logging
from geometry_msgs.msg import Twist

from spot_interfaces.msg import JointAngles

import motion_control.lib.motion_utils as mu
import motion_control.lib.poses as poses
from motion_control.lib.spot_kinematics import SpotKinematics

import copy
import numpy as np

class WalkManager():
    def __init__(self) -> None:
        self._walking_state = 0
        self._swing_phase = 0
        self._moving_leg = 0
        self._num_legs = 4

        self._kinematics = SpotKinematics()
        self._stand_foot_pos = self._kinematics.get_foot_coords()
        self._target_foot_pos = self._kinematics.get_foot_coords()

        self._leg_up_height = 0.06
        self._leg_stride = 0.125

        self._balance_roll = 0.3
        self._balance_pitch_fwd = -0.2
        self._balance_pitch_back = 0.1

        self._kinematics.set_body_angles(body_pitch_rad = self._balance_pitch_back, body_roll_rad = self._balance_roll)

    def is_standing(self, cmd: Twist) -> bool:
        if (abs(cmd.linear.x) < 0.5):
            if (self._walking_state == 3):
                return True
            self._walking_state = 2
        return False

    def new_joint_angles(self, current_angles: JointAngles, cmd: Twist, max_angle_delta: int) -> JointAngles:
        if self._walking_state == 2 or self._walking_state == 3:
            return self.to_stand_angles(current_angles, max_angle_delta)
        else:
            return self.walking_angles(current_angles, cmd, max_angle_delta)

    def to_stand_angles(self, current_angles: JointAngles, max_angle_delta: int) -> JointAngles:
        target_angles = self._kinematics.get_joint_angles()
        target_joints = mu.np_array_to_joint_angles(target_angles)

        if mu.joint_angles_match(current_angles, target_joints):
            if self._walking_state != 3:
                self._walking_state = 3
                legs_checked = 0
                while legs_checked <= self._num_legs:
                    if np.all(self._target_foot_pos[self._moving_leg,:] != self._stand_foot_pos[self._moving_leg,:]):
                        if self._target_foot_pos[self._moving_leg,1] > self._stand_foot_pos[self._moving_leg,1]:
                            self._target_foot_pos[self._moving_leg,:] = self._stand_foot_pos[self._moving_leg,:]
                        else:
                            self._target_foot_pos[self._moving_leg,1] = self._stand_foot_pos[self._moving_leg,1] + self._leg_up_height
                        self._walking_state = 2
                        break
                    else:
                        self._moving_leg += 1
                        if self._moving_leg >= self._num_legs:
                            self._moving_leg = 0
                        legs_checked += 1
            else:
                self._target_foot_pos = self._stand_foot_pos

        self._kinematics.set_foot_coords(self._target_foot_pos)
        return self.get_next_joint_angles(current_angles, max_angle_delta)

    def walking_angles(self, current_angles: JointAngles, cmd: Twist, max_angle_delta: int) -> JointAngles:
        self.update_phase(current_angles)
        speed = max_angle_delta
        return self.get_next_joint_angles(current_angles, speed)

    def update_phase(self, current_angles: JointAngles) -> None:
        target_angles = self._kinematics.get_joint_angles()
        target_joints = mu.np_array_to_joint_angles(target_angles)

        if mu.joint_angles_match(current_angles, target_joints):
            if self._swing_phase == 0:
                self._swing_phase = 1
                self._target_foot_pos[self._moving_leg, 1] += self._leg_up_height
                self._target_foot_pos[self._moving_leg, 0] += self._leg_stride/2
            elif self._swing_phase == 1:
                self._swing_phase = 2
                self._target_foot_pos[self._moving_leg, 1] = self._stand_foot_pos[self._moving_leg, 1]
                self._target_foot_pos[self._moving_leg, 0] += self._leg_stride/2
            elif self._swing_phase == 2:
                self._swing_phase = 3
                self._target_foot_pos[0, 0] -= self._leg_stride/4
                self._target_foot_pos[1, 0] -= self._leg_stride/4
                self._target_foot_pos[2, 0] -= self._leg_stride/4
                self._target_foot_pos[3, 0] -= self._leg_stride/4
            else:
                self._moving_leg += 1
                if self._moving_leg >= self._num_legs:
                    self._moving_leg = 0
                self._swing_phase = 0

                roll = self._balance_roll
                pitch = self._balance_pitch_fwd
                if self._moving_leg == 1 or self._moving_leg == 3:
                    roll = -self._balance_roll
                if self._moving_leg == 0 or self._moving_leg == 1:
                    pitch = self._balance_pitch_back
                self._kinematics.set_body_angles(body_pitch_rad = pitch, body_roll_rad = roll)

            self._kinematics.set_foot_coords(self._target_foot_pos)

    def get_next_joint_angles(self, current_angles: JointAngles, max_angle_delta: int) -> JointAngles:
        target_angles = self._kinematics.get_joint_angles()
        target_joints = mu.np_array_to_joint_angles(target_angles)
        target_joints = mu.multi_joint_one_step_interp(current_angles, target_joints, max_angle_delta)
        return target_joints
