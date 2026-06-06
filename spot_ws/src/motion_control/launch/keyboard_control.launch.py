from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='joint_ctl',
            executable='servo_ctl',
            name='servo_ctl',
        ),
        Node(
            package='motion_control',
            executable='classic_gait',
            name='gait_control',
        ),
    ])
