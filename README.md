#  Budget SpotMicro ROS2
### AI-Assisted Search and Rescue Robot Dog — under $500

[![ROS2](https://img.shields.io/badge/ROS2-Jazzy-blue)](https://docs.ros.org/en/jazzy/)
[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205-red)](https://www.raspberrypi.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Cost](https://img.shields.io/badge/Build%20Cost-Under%20%24500-brightgreen)]()
[![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)]()

A low-cost quadruped robot built for Search and Rescue (SAR) operations. Based on the SpotMicro open hardware platform, modified to run on a Raspberry Pi 5 with dual PCA9685 servo controllers and ROS2 Jazzy. Capable of autonomous human detection via YOLOv8, GPS location reporting, and offline operation over 1km range via LoRa radio — all for under $500.

> Built as a student robotics project by [roberenest](https://github.com/roberenest).  
> Based on [mogar/spot_micro](https://github.com/mogar/spot_micro) — modified for Raspberry Pi 5, dual PCA9685 boards, and ROS2 Jazzy.

---

##  Why this robot?

Traditional SAR tools struggle in disaster zones:
- **Drones** can't navigate inside collapsed buildings
- **Tracked robots** get stuck on rubble and stairs
- **Boston Dynamics Spot** costs ~$75,000

This robot walks on four legs, fits through tight spaces, climbs uneven terrain, detects humans with AI vision, and reports GPS coordinates back to an operator — all offline, all for under $500.

---

##  Features

- ✅ 12-servo quadruped walking with inverse kinematics (IK)
- ✅ YOLOv8n real-time human detection via onboard camera
- ✅ Keyboard and gamepad control
- ✅ Live video feed
- 🔧 LoRa radio communication (1km range) — in progress
- 🔧 GPS location reporting — in progress
- 🔧 Autonomous human detection alerts — in progress

---

##  Hardware

| Component | Details |
|---|---|
| Computer | Raspberry Pi 5 (8GB RAM) |
| OS | Debian Trixie (aarch64) |
| Servo Controllers | 2x PCA9685 (front: 0x40, rear: 0x41) |
| Servos | 12x (3 per leg) |
| Camera | Logitech Brio 100 |
| Distance Sensor | HC-SR04 Ultrasonic |
| IMU | MPU6050 Gyroscope |
| Power | XL4016 power modules |
| Comms | LoRa radio (USB dongle) — WIP |
| GPS | USB GPS module — WIP |
| Frame | 3D printed SpotMicro body |

### Servo Channel Mapping

| Leg | Controller | Coxa | Hip | Knee |
|---|---|---|---|---|
| Front Left | PCA 0x40 | CH 8 | CH 7 | CH 15 |
| Front Right | PCA 0x40 | CH 5 | CH 3 | CH 0 |
| Back Left | PCA 0x41 | CH 14 | CH 7 | CH 11 |
| Back Right | PCA 0x41 | CH 15 | CH 0 | CH 9 |

---

##  Software Stack

- **ROS2 Jazzy** (running in Docker)
- **YOLOv8n** — human detection
- **Python** — control nodes
- **Docker** — containerized ROS2 environment

---

##  Getting Started

### Requirements
- Raspberry Pi 5 (8GB recommended)
- Docker installed
- I2C enabled (`raspi-config`)
- I2C speed set to 400kHz for reduced servo jitter — add this to `/boot/firmware/config.txt`:
  ```
  dtparam=i2c_arm_baudrate=400000
  ```

### Running the robot

**Step 1 — Start the Docker container** (in any terminal on the Pi):
```bash
cd ~/spot_micro/docker-full && sudo docker compose up -d
```

**Step 2 — Get a shell inside the container:**
```bash
sudo docker exec -it docker-full-ros2-1 bash
```

**Step 3 — Launch the robot inside that shell:**
```bash
cd /home/ros/spot_ws && \
source /opt/ros/jazzy/setup.bash && \
source install/setup.bash && \
/home/ros/spot_ws/start.sh
```

The robot is now live. Use keyboard or gamepad to control it.

### Servo Calibration

Calibration values are in `spot_ws/src/joint_ctl/joint_ctl/lib/spot_joints.py`.

Current tuned values:
```
flc=302, flh=341, flk=375(inv)
frc=295, frh=245(inv), frk=360
blc=323, blh=430(inv), blk=289(inv)
brc=285, brh=241(inv), brk=309
```

To recalibrate: use the Adafruit PCA9685 library to get raw PWM values, then convert with `raw_pwm / 16` to get the `zero_count` format used by this codebase.

---

##  Repository Structure

```
spot_micro/
├── docker-full/        # Dockerfile and docker-compose for ROS2 Jazzy
├── spot_ws/
│   ├── src/
│   │   ├── commanding/         # Keyboard control node
│   │   ├── joint_ctl/          # Servo control + calibration
│   │   └── motion_control/     # Gait, IK, launch files
│   └── start.sh                # ROS2 launch script (run inside Docker)
└── README.md
```

---

##  Roadmap

- [x] Walking with IK gait
- [x] YOLOv8 human detection
- [x] Keyboard and gamepad control
- [x] Live video feed
- [ ] LoRa offline communication
- [ ] GPS location reporting
- [ ] Human detection → location alert pipeline
- [ ] Microphone for audio survivor detection
- [ ] Autonomous navigation

---

##  Credits

- [mogar/spot_micro](https://github.com/mogar/spot_micro) — original ROS2 SpotMicro codebase this project is built on
- [SpotMicro community](https://github.com/topics/spotmicro) — open hardware platform

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
