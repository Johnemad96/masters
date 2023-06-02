#!/usr/bin/env python3
import subprocess
import time
import signal

# Start a command
orbslam_process = subprocess.Popen(["rosrun", "ORB_SLAM3" ,"Stereo", "../../ORB_SLAM3/Vocabulary/ORBvoc.txt" ,"../../ORB_SLAM3/Examples/Stereo/EuRoC.yaml", "false"])

time.sleep(15)

startDataset_process = subprocess.Popen(["/Datasets/sendDatasetDoneFlag.sh", "carlaDatasets/38_PaperDataset_Town10_20230331_2_normal_night_euroc.bag"])

# Wait for a certain amount of time
time.sleep(90)

# # If the process is still running after this time, terminate it
# if process.poll() is None:
#     process.terminate()

# If the process is still running after this time, send a SIGINT signal
if orbslam_process.poll() is None:
    startDataset_process.send_signal(signal.SIGINT)
    orbslam_process.send_signal(signal.SIGINT)
    time.sleep(5)
    orbslam_process.send_signal(signal.SIGINT)