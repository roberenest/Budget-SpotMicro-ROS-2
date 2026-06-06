"""
Lightweight servo control library for use with the PCA9685.
"""

import time
from smbus2 import SMBus
from rclpy import logging
from math import pi
from math import radians as rad

degrees_per_count = 0.6

def get_joint_limits(zero_count: int, neg_limit_deg: float, pos_limit_deg: float, invert: bool = False):
    if not invert:
        return ([rad(neg_limit_deg), int(zero_count + neg_limit_deg/degrees_per_count)],
                [rad(pos_limit_deg), int(zero_count + pos_limit_deg/degrees_per_count)])
    else:
        return ([rad(neg_limit_deg), int(zero_count - neg_limit_deg/degrees_per_count)],
                [rad(pos_limit_deg), int(zero_count - pos_limit_deg/degrees_per_count)])

class PcaPwm():
    def __init__(self, channel: int, address: int = 0x40, reuse_gpio=None) -> None:
        self._osc = 25E6
        self._mode_addx = 0x00
        self._mode_restart = 0x80
        self._mode_sleep = 0x10
        self._prescale_addx = 0xFE
        self._address = address
        self._bus = SMBus(channel)
        self.set_frequency(60)

    def get_frequency(self):
        return self._osc/(4095*(self._clamped_prescale + 1))

    def set_frequency(self, freq: int) -> None:
        prescale = self._osc/(4096*freq) - 1
        self._clamped_prescale = int(max(3, min(prescale, 255)))
        try:
            mode1 = self._bus.read_byte_data(self._address, self._mode_addx)
            temp_mode = (mode1 & ~self._mode_restart) | self._mode_sleep
            self._bus.write_byte_data(self._address, self._mode_addx, temp_mode)
            self._bus.write_byte_data(self._address, self._prescale_addx, self._clamped_prescale)
            new_mode = mode1 & ~self._mode_sleep
            self._bus.write_byte_data(self._address, self._mode_addx, new_mode)
            time.sleep(0.005)
            new_mode = new_mode | self._mode_restart
            self._bus.write_byte_data(self._address, self._mode_addx, new_mode)
        except:
            logging.get_logger("PcaPwm").info("ERROR: couldn't write frequency to PWM controller")

    def enable(self) -> None:
        pass

    def disable(self) -> None:
        pass

    def write_pwm(self, pin: int, pwm: int) -> None:
        pwm = int(max(0, min(pwm, 4095)))
        pwm_lo = pwm & 0xFF
        pwm_hi = (pwm >> 8) & 0xFF
        try:
            self._bus.write_byte_data(self._address, (6+4*pin), 0)
            self._bus.write_byte_data(self._address, (6+4*pin + 1), 0)
            self._bus.write_byte_data(self._address, (6+4*pin + 2), pwm_lo)
            self._bus.write_byte_data(self._address, (6+4*pin + 3), pwm_hi)
        except:
            pass

class Servo():
    def __init__(self, comms: PcaPwm, servo_id: int, min_out: list = [-pi/2, 750], max_out: list = [pi, 1500], home: float = 0.0) -> None:
        self._comms = comms
        self._servo_id = servo_id
        self._min_out = min_out
        self._max_out = max_out
        self._home = home
        self.set_angle_rad(self._home)

    def set_target(self, target: int) -> int:
        self._target = max(0, min(target, 1500))
        self._comms.write_pwm(self._servo_id, self._target)
        return self._target

    def get_target(self) -> int:
        return self._target

    def angle_rad_to_target(self, angle: float) -> int:
        target = (self._min_out[1] - self._max_out[1])/(self._min_out[0] - self._max_out[0]) * \
                (angle - self._max_out[0]) + self._max_out[1]
        return int(target)

    def target_to_angle_rad(self, target: int) -> float:
        angle = (self._min_out[0] - self._max_out[0])/(self._min_out[1] - self._max_out[1]) * \
                (target - self._max_out[1]) + self._max_out[0]
        return angle

    def set_angle_rad(self, angle: float) -> float:
        angle = max(self._min_out[0], min(angle, self._max_out[0]))
        self.set_target(self.angle_rad_to_target(angle))
        return angle

    def get_angle_rad(self) -> float:
        return self.target_to_angle_rad(self._target)
