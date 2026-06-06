#!/bin/bash
source /opt/ros/jazzy/setup.bash
source /home/ros/spot_ws/install/setup.bash
ros2 launch motion_control keyboard_control.launch.py &
sleep 4
ros2 run commanding keyboard_cmd
