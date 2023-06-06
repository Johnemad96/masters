#!/usr/bin/env python3
import subprocess
import time
import signal
import os

from changeYamlFileValues import Change_Yaml_Parameters

root_dir = '/Datasets'

def list_bag_files(directory , filter_bag_files_strings = None):
    # Initialize an empty list to store the file names
    bag_files = []

    # Use os.listdir to get the list of all files and directories in the directory
    for filename in os.listdir(directory):
        # Check if the file has a .bag extension
        if filename.endswith('.bag'):
            # Add the file to the list
            bag_files.append(os.path.join(directory, filename))

    # Sort the list of files
    bag_files.sort()

    # Initialize an empty list to store the filtered files
    filtered_files = []

    if filter_bag_files_strings!= None:
        # Search for the strings in the list of files
        for file in bag_files:
            if any(s in file for s in filter_bag_files_strings):
                filtered_files.append(file)
    return bag_files, filtered_files

## MISSING:
#  how to save the output of this in a specific output directory
def Run_ORBSlam_and_Dataset(rosbagName, testResultDirectory=None):
    # Start a command
    # this needs to be run from inside the docker container that has orbslam

    orbslam_process = subprocess.Popen(["rosrun", "ORB_SLAM3" ,"Stereo", "../../ORB_SLAM3/Vocabulary/ORBvoc.txt" ,"../../ORB_SLAM3/Examples/Stereo/EuRoC.yaml", "false"], cwd= )

    time.sleep(15)
    rosbagName = "carlaDatasets/" + rosbagName
    startDataset_process = subprocess.Popen(["/Datasets/sendDatasetDoneFlag.sh", rosbagName])

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

if __name__ == "__main__":
    # assuming a case where I need to make multiple tests by variyng parameters 

    # list bag files in Datasets/carlaDatasets
    bag_files, filtered_files = list_bag_files((root_dir +"carlaDatasets/"), ["20230331_2", "normal_night"])
    
    # change EuRoC.yaml Parameters, and later this will be a loop to change try multiple parameters and then run the required dataset 
    Change_Yaml_Parameters(new_ThDepth = 35, new_ORBextractor_nFeatures = 1200)
    pathToSaveTestResults = "/Datasets/carlaDatasets/"
    Run_ORBSlam_and_Dataset("38_PaperDataset_Town10_20230331_2_normal_night_euroc.bag", pathToSaveTestResults)