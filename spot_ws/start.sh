#!/bin/bash
source /opt/ros/jazzy/setup.bash
source /home/ros/spot_ws/install/setup.bash

echo "Launching servo + gait nodes..."
ros2 launch motion_control keyboard_control.launch.py &

echo "Waiting for nodes to come up..."
until ros2 node list 2>/dev/null | grep -q "/gait_control"; do
    sleep 0.5
done
until ros2 node list 2>/dev/null | grep -q "/servo_ctl"; do
    sleep 0.5
done

echo "Nodes ready. Starting keyboard control."
ros2 run commanding keyboard_cmd
