#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace


def generate_launch_description():
    # Declare launch arguments
    veh_arg = DeclareLaunchArgument(
        'veh',
        default_value='',
        description='Name of vehicle. ex: megaman'
    )

    # Get launch configurations
    veh = LaunchConfiguration('veh')

    # Create nodes
    talker_node = Node(
        package='test_ros',
        executable='talker.py',
        name='talker',
        output='screen'
    )

    listener_node = Node(
        package='test_ros',
        executable='listener.py',
        name='listener',
        output='screen'
    )

    # Group nodes under vehicle namespace
    group = GroupAction([
        PushRosNamespace(veh),
        talker_node,
        listener_node,
    ])

    return LaunchDescription([
        veh_arg,
        group,
    ])
