#!/bin/bash

source /environment.sh

# initialize launch file
dt-launchfile-init

# YOUR CODE BELOW THIS LINE
# ----------------------------------------------------------------------------

# NOTE: Use the variable DT_PROJECT_PATH to know the absolute path to your code
# NOTE: Use `dt-exec COMMAND` to run the main process (blocking process)

# set module's health
dt-set-module-healthy

# get vehicle name from environment or use default
VEH_NAME=${VEHICLE_NAME:-testbot}

# launching test ROS2 communication with vehicle namespace
echo "Launching test_ros communication test with vehicle namespace: ${VEH_NAME}"
dt-exec ros2 launch test_ros all_ros2.launch.py veh:=${VEH_NAME}

# ----------------------------------------------------------------------------
# YOUR CODE ABOVE THIS LINE

# wait for app to end
dt-launchfile-join
