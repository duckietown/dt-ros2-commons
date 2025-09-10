cmake_minimum_required(VERSION 3.5)
project(duckietown_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)

set(msg_files
  msg/AntiInstagramThresholds.msg
  msg/AprilTagDetection.msg
  msg/AprilTagDetectionArray.msg
  msg/AprilTagsWithInfos.msg
  msg/BoolStamped.msg
  msg/ButtonEvent.msg
  msg/CarControl.msg
  msg/CoordinationClearance.msg
  msg/CoordinationSignal.msg
  msg/DiagnosticsCodeProfiling.msg
  msg/DiagnosticsCodeProfilingArray.msg
  msg/DiagnosticsRosLink.msg
  msg/DiagnosticsRosLinkArray.msg
  msg/DiagnosticsRosNode.msg
  msg/DiagnosticsRosParameterArray.msg
  msg/DiagnosticsRosTopic.msg
  msg/DiagnosticsRosTopicArray.msg
  msg/DisplayFragment.msg
  msg/DroneControl.msg
  msg/DroneMode.msg
  msg/DroneMotorCommand.msg
  msg/NodeParameter.msg
  msg/DuckiebotLED.msg
  msg/DuckiematrixLinkDescription.msg
  msg/EncoderStamped.msg
  msg/EpisodeStart.msg
  msg/FSMState.msg
  msg/H264MotionVectors.msg
  msg/IntersectionPose.msg
  msg/IntersectionPoseImg.msg
  msg/IntersectionPoseImgDebug.msg
  msg/KinematicsParameters.msg
  msg/KinematicsWeights.msg
  msg/LanePose.msg
  msg/LEDDetection.msg
  msg/LEDDetectionArray.msg
  msg/LEDDetectionDebugInfo.msg
  msg/LEDInterpreter.msg
  msg/LEDPattern.msg
  msg/LightSensor.msg
  msg/LineFollowerStamped.msg
  msg/MaintenanceState.msg
  msg/ObstacleImageDetection.msg
  msg/ObstacleImageDetectionList.msg
  msg/ObstacleProjectedDetection.msg
  msg/ObstacleProjectedDetectionList.msg
  msg/ObstacleType.msg
  msg/ParamTuner.msg
  msg/Pixel.msg
  msg/PIDDiagnostics.msg
  msg/PIDState.msg
  msg/Pose2DStamped.msg
  msg/Rect.msg
  msg/Rects.msg
  msg/SceneSegments.msg
  msg/Segment.msg
  msg/SegmentList.msg
  msg/SignalsDetection.msg
  msg/SignalsDetectionETHZ17.msg
  msg/SourceTargetNodes.msg
  msg/StopLineReading.msg
  msg/TagInfo.msg
  msg/ThetaDotSample.msg
  msg/Trajectory.msg
  msg/TurnIDandType.msg
  msg/Twist2DStamped.msg
  msg/Vector2D.msg
  msg/VehicleCorners.msg
  msg/VehiclePose.msg
  msg/Vsample.msg
  msg/WheelEncoderStamped.msg
  msg/WheelsCmd.msg
  msg/WheelsCmdStamped.msg
  msg/WheelsCmdDBV2Stamped.msg
)

set(srv_files
  srv/ChangePattern.srv
  srv/GetVariable.srv
  srv/IMUstatus.srv
  srv/LFstatus.srv
  srv/NodeGetParamsList.srv
  srv/NodeRequestParamsUpdate.srv
  srv/SensorsStatus.srv
  srv/SetCustomLEDPattern.srv
  srv/SetDroneCommandsOverride.srv
  srv/SetDroneMode.srv
  srv/SetFSMState.srv
  srv/SetValue.srv
  srv/SetVariable.srv
  srv/ToFstatus.srv
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  DEPENDENCIES builtin_interfaces std_msgs geometry_msgs sensor_msgs visualization_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
