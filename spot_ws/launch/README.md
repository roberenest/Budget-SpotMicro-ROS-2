# Launch Files

These files launch a set of ROS nodes together to accomplish various tasks.

To use any of these, make sure you've sourced the workspace setup file and then run something like this:

```
spot_ws$ ros2 launch launch/<launch_file_name>.py
```

## Simple Walking

### simple_walker_launch.py

Basic remote control via gamepad of a walking spot. No sensors or autonomy, just direct remote control.
