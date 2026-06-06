from setuptools import find_packages, setup
package_name = 'commanding'
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Morgan',
    maintainer_email='redfieldm@gmail.com',
    description='User inputs for commanding spot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joy2joints = commanding.joy2joints:main',
            'joy2cmd = commanding.joy2cmd:main',
            'keyboard_cmd = commanding.keyboard_cmd:main',
        ],
    },
)
