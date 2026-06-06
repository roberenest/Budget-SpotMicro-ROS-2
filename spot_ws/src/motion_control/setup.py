from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'motion_control'
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Morgan',
    maintainer_email='redfieldm@gmail.com',
    description='Motion control for spot micro',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'classic_gait = motion_control.classic_gait:main',
            'pose_cycle = motion_control.pose_cycle:main',
            'trot_gait = motion_control.trot_gait:main',
        ],
    },
)
