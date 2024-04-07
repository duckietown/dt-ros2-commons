#!/bin/bash

source /environment.sh

# initialize launch file
dt-launchfile-init

# launch publisher
ros2 run my_package my_publisher_node &

# launch subscriber
ros2 run my_package my_subscriber_node

# wait for app to end
dt-launchfile-join