#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='test_ros',
            executable='talker.py',
            name='talker',
            output='screen'
        ),
        Node(
            package='test_ros',
            executable='listener.py',
            name='listener',
            output='screen'
        ),
    ])
