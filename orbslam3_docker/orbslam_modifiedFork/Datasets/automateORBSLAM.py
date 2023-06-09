#!/usr/bin/env python3
import subprocess
import time
import signal
import os

from changeYamlFileValues import Change_Yaml_Parameters
from readParams import Read_Required_Params
from createIcrementedDatasetTestFolder import create_incremented_folder
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
            if all(s in file for s in filter_bag_files_strings):
                filtered_files.append(file)
    return bag_files, filtered_files

## MISSING:
## SOLVED!!!
#  how to save the output of this in a specific output directory
def Run_ORBSlam_and_Dataset(rosbagName, testResultDirectory=None):
    # Start a command
    # this needs to be run from inside the docker container that has orbslam

    orbslam_process = subprocess.Popen(["rosrun", "ORB_SLAM3" ,"Stereo", "/ORB_SLAM3/Vocabulary/ORBvoc.txt" ,"/ORB_SLAM3/Examples/Stereo/EuRoC.yaml", "false"], cwd= testResultDirectory)

    time.sleep(15)
    # rosbagName = "carlaDatasets/" + rosbagName
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
    parameters = Read_Required_Params('parameters.txt')
    root_dir = parameters['root_dir']
    test_results_path = parameters['test_results_path']
    test_parameter = parameters['test_parameter']
    results_evaluation_path = parameters['results_evaluation_path']
    # assuming a case where I need to make multiple tests by variyng parameters 

    # list bag files in Datasets/carlaDatasets
    bag_files, filtered_files = list_bag_files((root_dir), ["20230331_1", "normal"])

    # change EuRoC.yaml Parameters, and later this will be a loop to change try multiple parameters and then run the required dataset 
    # Change_Yaml_Parameters(new_ThDepth = 35, new_ORBextractor_nFeatures = 1200)
    # Init Value for OrbSlam Parameters, and the incrementation value
    # baseline
    # default_ThDepth = 35.0
    new_ThDepth = 95.0
    # increment_new_ThDepth = 5
    # MAX_new_ThDepth = 130.0

    # orb features
    new_ORBextractor_nFeatures = 600
    increment_new_ORBextractor_nFeatures = 100
    MAX_new_ORBextractor_nFeatures = 2000

    #create test parameter sub directory 
    os.makedirs(os.path.join(test_results_path, test_parameter), exist_ok=True)
    pathToSaveTestResults_testParameter = create_incremented_folder(os.path.join(test_results_path, test_parameter))
    print(pathToSaveTestResults_testParameter)
    # while int(new_ThDepth) <= int(MAX_new_ThDepth):
    # while int(new_ORBextractor_nFeatures) <= int(MAX_new_ORBextractor_nFeatures):
        
    #     # pathToSaveTestResults = "/Datasets/carlaDatasets/"

    #     # Change_Yaml_Parameters(new_ThDepth)
    #     # pathToSaveTestResults = os.path.join(pathToSaveTestResults_testParameter,(str(new_ThDepth).zfill(4)).replace('.', '_'))
    #     # os.makedirs(pathToSaveTestResults, exist_ok=True)
    #     # Run_ORBSlam_and_Dataset(filtered_files[0], pathToSaveTestResults)
    #     # new_ThDepth += increment_new_ThDepth

    #     Change_Yaml_Parameters(new_ThDepth=default_ThDepth, new_ORBextractor_nFeatures = new_ORBextractor_nFeatures)
    #     pathToSaveTestResults = os.path.join(pathToSaveTestResults_testParameter,(str(new_ORBextractor_nFeatures).zfill(4)).replace('.', '_'))
    #     os.makedirs(pathToSaveTestResults, exist_ok=True)
    #     Run_ORBSlam_and_Dataset(filtered_files[0], pathToSaveTestResults)
    #     new_ORBextractor_nFeatures += increment_new_ORBextractor_nFeatures
    
    # Custome test 
    # nORBFeatures_test = [600, 800, 1000, 2000]
    # baseline_test = [70,80,90,100]
    
    for nORBFeatures_test in [600,800,1000,2000]:
        new_ORBextractor_nFeatures = nORBFeatures_test
        for baseline_test in [70,80,90,100]:
            new_ThDepth = baseline_test*1.0
            Change_Yaml_Parameters(new_ThDepth=new_ThDepth, new_ORBextractor_nFeatures = new_ORBextractor_nFeatures)
            pathToSaveTestResults = os.path.join(pathToSaveTestResults_testParameter,((str(new_ThDepth).zfill(4)) + (str(new_ORBextractor_nFeatures).zfill(4))).replace('.', '_'))
            os.makedirs(pathToSaveTestResults, exist_ok=True)
            Run_ORBSlam_and_Dataset(filtered_files[0], pathToSaveTestResults)
            time.sleep(3)
