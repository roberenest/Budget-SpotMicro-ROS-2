from rclpy import logging

from spot_interfaces.msg import JointAngles
from geometry_msgs.msg import Twist
from spot_interfaces.msg import StateCmd

from motion_control.lib.spot_kinematics import SpotKinematics
from motion_control.lib.walking import WalkManager
import motion_control.lib.motion_utils as mu
import motion_control.lib.poses as poses


class BaseState():
    def __init__(self):
        pass

    def next_state_from_cmd(self, cmd, state_cmd):
        return self

    def joint_angles_from_cmd(self, current_angles, cmd, state_cmd):
        return current_angles

class SitState(BaseState):
    def __init__(self):
        self._sit_angles = poses.get_sitting_pose()

    def next_state_from_cmd(self, cmd, state_cmd):
        if state_cmd.sit == 0:
            logging.get_logger("SitState").info("transition to stand")
            return StandState()
        return self

    def joint_angles_from_cmd(self, current_angles, cmd, state_cmd, max_angle_delta):
        target_angles = JointAngles()
        target_angles.flc = mu.one_step_interp(current_angles.flc, self._sit_angles.flc, max_angle_delta)
        target_angles.flh = mu.one_step_interp(current_angles.flh, self._sit_angles.flh, max_angle_delta)
        target_angles.flk = mu.one_step_interp(current_angles.flk, self._sit_angles.flk, max_angle_delta)
        target_angles.frc = mu.one_step_interp(current_angles.frc, self._sit_angles.frc, max_angle_delta)
        target_angles.frh = mu.one_step_interp(current_angles.frh, self._sit_angles.frh, max_angle_delta)
        target_angles.frk = mu.one_step_interp(current_angles.frk, self._sit_angles.frk, max_angle_delta)
        target_angles.blc = mu.one_step_interp(current_angles.blc, self._sit_angles.blc, max_angle_delta)
        target_angles.blh = mu.one_step_interp(current_angles.blh, self._sit_angles.blh, max_angle_delta)
        target_angles.blk = mu.one_step_interp(current_angles.blk, self._sit_angles.blk, max_angle_delta)
        target_angles.brc = mu.one_step_interp(current_angles.brc, self._sit_angles.brc, max_angle_delta)
        target_angles.brh = mu.one_step_interp(current_angles.brh, self._sit_angles.brh, max_angle_delta)
        target_angles.brk = mu.one_step_interp(current_angles.brk, self._sit_angles.brk, max_angle_delta)
        return target_angles

class StandState(BaseState):
    def __init__(self):
        self._kinematics = SpotKinematics()

    def next_state_from_cmd(self, cmd, state_cmd):
        if state_cmd.sit != 0:
            logging.get_logger("StandState").info("transition to sit")
            return SitState()
        elif cmd.linear.x > 0:
            logging.get_logger("StandState").info("transition to walk")
            return WalkState()
        return self

    def joint_angles_from_cmd(self, current_angles, cmd, state_cmd, max_angle_delta):
        self._kinematics.set_body_angles(body_pitch_rad=cmd.angular.z, body_roll_rad=cmd.angular.x, body_yaw_rad=cmd.angular.y)
        target_angles = self._kinematics.get_joint_angles()
        target_joints = mu.multi_joint_one_step_interp(current_angles, mu.np_array_to_joint_angles(target_angles), max_angle_delta)
        return target_joints

class WalkState(BaseState):
    def __init__(self):
        self._walk_mgr = WalkManager()

    def next_state_from_cmd(self, cmd, state_cmd):
        if self._walk_mgr.is_standing(cmd):
            logging.get_logger("WalkState").info("transition to stand")
            return StandState()
        return self

    def joint_angles_from_cmd(self, current_angles, cmd, state_cmd, max_angle_delta):
        return self._walk_mgr.new_joint_angles(current_angles, cmd, max_angle_delta)
