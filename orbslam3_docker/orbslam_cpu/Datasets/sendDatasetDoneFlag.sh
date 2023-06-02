#!/bin/bash
# cd ~/masters/orbslam3_docker/orbslam_modifiedFork/Datasets
# cd ~/Datasets
# rosbag play --pause dataset-room2_512_16_small_chunks.bag /cam0/image_raw:=/camera/left/image_raw /cam1/image_raw:=/camera/right/image_raw /imu0:=/imu  
# rostopic pub /flagROSBagDone std_msgs/Int16 "data: 1"

rosbag play --pause $1 /cam0/image_raw:=/camera/left/image_raw /cam1/image_raw:=/camera/right/image_raw /imu0:=/imu  
rostopic pub /flagROSBagDone std_msgs/Int16 "data: 1"
vscode % bash