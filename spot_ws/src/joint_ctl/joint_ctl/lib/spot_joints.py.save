

from joint_ctl.lib.servo import Servo, PcaPwm, get_joint_limits


# joint rotation limits for each spot_joint_limits["type of"] joint
spot_joint_limits = {
    "coxa_min": -30.0,
    "coxa_max": 30.0,
    "hip_min": -78.0,
    "hip_max": 78.0,
    "knee_min": -60.0,
    "knee_max": 150.0,
}

# calibrated joint limits for each individual joint
# The integer parameter is the count-value for which the servo is at angle 0
(flc_min, flc_max) = get_joint_limits(400, spot_joint_limits["coxa_min"], spot_joint_limits["coxa_max"])
(flh_min, flh_max) = get_joint_limits(400, spot_joint_limits["hip_min"],  spot_joint_limits["hip_max"], True)
(flk_min, flk_max) = get_joint_limits(360, spot_joint_limits["knee_min"], spot_joint_limits["knee_max"], True)
(frc_min, frc_max) = get_joint_limits(380, spot_joint_limits["coxa_min"], spot_joint_limits["coxa_max"])
(frh_min, frh_max) = get_joint_limits(333, spot_joint_limits["hip_min"],  spot_joint_limits["hip_max"])
(frk_min, frk_max) = get_joint_limits(400, spot_joint_limits["knee_min"], spot_joint_limits["knee_max"])
(blc_min, blc_max) = get_joint_limits(365, spot_joint_limits["coxa_min"], spot_joint_limits["coxa_max"])
(blh_min, blh_max) = get_joint_limits(420, spot_joint_limits["hip_min"],  spot_joint_limits["hip_max"], True)
(blk_min, blk_max) = get_joint_limits(370, spot_joint_limits["knee_min"], spot_joint_limits["knee_max"], True)
(brc_min, brc_max) = get_joint_limits(370, spot_joint_limits["coxa_min"], spot_joint_limits["coxa_max"])
(brh_min, brh_max) = get_joint_limits(340, spot_joint_limits["hip_min"],  spot_joint_limits["hip_max"])
(brk_min, brk_max) = get_joint_limits(390, spot_joint_limits["knee_min"], spot_joint_limits["knee_max"])

# PWM controller object
controller = PcaPwm(channel = 1)

# Spot Joint objects for one Spot Micro
# The integer parameter is the pin ID the servo is connected to
spot_joint_servos = {
        # Front Left Leg
        "flc": Servo(controller, 3, min_out = flc_min, max_out = flc_max),
        "flh": Servo(controller, 4, min_out = flh_min, max_out = flh_max),
        "flk": Servo(controller, 5, min_out = flk_min, max_out = flk_max),
        # Front Right Leg
        "frc": Servo(controller, 0, min_out = frc_min, max_out = frc_max),
        "frh": Servo(controller, 1, min_out = frh_min, max_out = frh_max),
        "frk": Servo(controller, 2, min_out = frk_min, max_out = frk_max),
        # Back Left Leg
        "blc": Servo(controller, 9, min_out = blc_min, max_out = blc_max),
        "blh": Servo(controller, 10, min_out = blh_min, max_out = blh_max),
        "blk": Servo(controller, 11, min_out = blk_min, max_out = blk_max),
        # Back Right Leg
        "brc": Servo(controller, 6, min_out = brc_min, max_out = brc_max),
        "brh": Servo(controller, 7, min_out = brh_min, max_out = brh_max),
        "brk": Servo(controller, 8, min_out = brk_min, max_out = brk_max),
}
