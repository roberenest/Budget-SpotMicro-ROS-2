#!/bin/bash
set -e

echo "Starting Docker..."
cd ~/spot_micro/docker-full
sudo docker compose up -d

echo "Waiting for container to be ready..."
sleep 3

echo "Entering container and launching ROS2..."
sudo docker exec -it docker-full-ros2-1 bash -c "cd /home/ros/spot_ws && ./start.sh"
