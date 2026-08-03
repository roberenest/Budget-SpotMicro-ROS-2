from joint_ctl.lib.servo import Servo, PcaPwm, get_joint_limits

spot_joint_limits = {
    "coxa_min": -30.0,
    "coxa_max": 30.0,
    "hip_min": -78.0,
    "hip_max": 78.0,
    "knee_min": -60.0,
    "knee_max": 150.0,
}

(flc_min, flc_max) = get_joint_limits(302, spot_joint_limits["coxa_min"], spot_joint_limits["coxa_max"])
(flh_min, flh_max) = get_joint_limits(341, spot_joint_limits["hip_min"],  spot_joint_limits["hip_max"])
(flk_min, flk_max) = get_joint_limits(375, spot_joint_limits["knee_min"], spot_joint_limits["knee_max"], True)
(frc_min, frc_max) = get_joint_limits(312, spot_joint_limits["coxa_min"], spot_joint_limits["coxa_max"])
(frh_min, frh_max) = get_joint_limits(245, spot_joint_limits["hip_min"],  spot_joint_limits["hip_max"], True)
(frk_min, frk_max) = get_joint_limits(343, spot_joint_limits["knee_min"], spot_joint_limits["knee_max"])
(blc_min, blc_max) = get_joint_limits(340, spot_joint_limits["coxa_min"], spot_joint_limits["coxa_max"])
(blh_min, blh_max) = get_joint_limits(463, spot_joint_limits["hip_min"],  spot_joint_limits["hip_max"], True)
(blk_min, blk_max) = get_joint_limits(289, spot_joint_limits["knee_min"], spot_joint_limits["knee_max"], True)
(brc_min, brc_max) = get_joint_limits(285, spot_joint_limits["coxa_min"], spot_joint_limits["coxa_max"])
(brh_min, brh_max) = get_joint_limits(280, spot_joint_limits["hip_min"],  spot_joint_limits["hip_max"], False)
(brk_min, brk_max) = get_joint_limits(392, spot_joint_limits["knee_min"], spot_joint_limits["knee_max"])

front_controller = PcaPwm(channel=1, address=0x40)
back_controller  = PcaPwm(channel=1, address=0x41, reuse_gpio=front_controller)

spot_joint_servos = {
        "flc": Servo(front_controller, 8,  min_out=flc_min, max_out=flc_max),
        "flh": Servo(front_controller, 7,  min_out=flh_min, max_out=flh_max),
        "flk": Servo(front_controller, 15, min_out=flk_min, max_out=flk_max),
        "frc": Servo(front_controller, 5,  min_out=frc_min, max_out=frc_max),
        "frh": Servo(front_controller, 3,  min_out=frh_min, max_out=frh_max),
        "frk": Servo(front_controller, 0,  min_out=frk_min, max_out=frk_max),
        "blc": Servo(back_controller,  14, min_out=blc_min, max_out=blc_max),
        "blh": Servo(back_controller,  7,  min_out=blh_min, max_out=blh_max),
        "blk": Servo(back_controller,  11, min_out=blk_min, max_out=blk_max),
        "brc": Servo(back_controller,  15, min_out=brc_min, max_out=brc_max),
        "brh": Servo(back_controller,  0,  min_out=brh_min, max_out=brh_max),
        "brk": Servo(back_controller,  9,  min_out=brk_min, max_out=brk_max),
}
