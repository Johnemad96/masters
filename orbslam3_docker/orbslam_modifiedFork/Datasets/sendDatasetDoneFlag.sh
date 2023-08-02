#!/bin/bash
# cd ~/masters/orbslam3_docker/orbslam_modifiedFork/Datasets
# cd ~/Datasets
# rosbag play --pause dataset-room2_512_16_small_chunks.bag /cam0/image_raw:=/camera/left/image_raw /cam1/image_raw:=/camera/right/image_raw /imu0:=/imu  
# rostopic pub /flagROSBagDone std_msgs/Int16 "data: 1"

#topic mapping for external Dataset
# rosbag play --pause $1 /cam0/image_raw:=/camera/left/image_raw /cam1/image_raw:=/camera/right/image_raw /imu0:=/imu  

# carla-made dataset, no mapping needed

### ORIGINAL SCRIPT

# rosbag play --pause $1
# rostopic pub /flagROSBagDone std_msgs/Int16 "data: 1"


rosbag play $1 & 
rosbag_pid=$!
sleep 90
kill -SIGINT $rosbag_pid
rostopic pub -1 /flagROSBagDone std_msgs/Int16 "data: 1"

