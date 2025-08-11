from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'test_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mack',
    maintainer_email='mack@duckietown.org',
    description='Test package for ROS2',
    license='GPLv3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker.py = test_ros.talker:main',
            'listener.py = test_ros.listener:main',
        ],
    },
)
