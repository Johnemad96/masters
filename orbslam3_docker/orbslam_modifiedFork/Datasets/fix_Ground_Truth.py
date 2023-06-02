#!/usr/bin/env python

import os
import shutil
import subprocess

"""
Script to preprocess ground truth data for EuRoC datasets and generate the corresponding TUM file.
The script looks for the "GroundTruth_Transformed_clean.csv" file in each subdirectory of the specified main directory. 
If the file is found, it skips the directory. Otherwise, it looks for the "GroundTruth_Transformed.csv" file, copies it to "GroundTruth_Transformed_clean.csv", 
removes the first row and column from the copied file, and then runs the EuRoC trajectory ground truth command "evo_traj euroc GroundTruth_Transformed_clean.csv --save_as_tum" 
on the modified file to generate the corresponding TUM file. The TUM file is saved in the same directory as the input file.
"""


# Set the terminal command to run
EVO_TRAJ_GND_TRUTH_TERMINAL_COMMAND = "evo_traj euroc GroundTruth_Transformed_clean.csv --save_as_tum"
# TERMINAL_COMMAND = "pwd"

# Get a list of all the directories inside the main directory
main_dir = "/home/john/masters/orbslam3_docker/orbslam_modifiedFork/Datasets/carlaDatasets"
dir_list = [d for d in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, d)) and d[0].isdigit()]

def RunTerminalCommand(directory,command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True,cwd=(directory))
    print(directory,result.stdout)

# Iterate over each directory and copy the csv file
for dir_name in dir_list:
    # if os.listdir(os.path.join(main_dir, dir_name)) :
    directory = (os.path.join(main_dir, dir_name))
    if "GroundTruth_Transformed_clean.tum" in [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]:
        continue
    if "GroundTruth_Transformed_clean.csv" in [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]:
        RunTerminalCommand(directory,EVO_TRAJ_GND_TRUTH_TERMINAL_COMMAND)
        # result = subprocess.run(EVO_TRAJ_GND_TRUTH_TERMINAL_COMMAND, shell=True, capture_output=True, text=True,cwd=(directory))
        # print(directory,result.stdout)
        continue
    src_file = os.path.join(main_dir, dir_name, "GroundTruth_Transformed.csv")
    dest_file = os.path.join(main_dir, dir_name, "GroundTruth_Transformed_clean.csv")
    shutil.copyfile(src_file, dest_file)

    # Open the copied csv file and remove the first row and column
    with open(dest_file, "r") as f:
        lines = f.readlines()[1:]
        stripped_lines = [line.split(",")[1:] for line in lines]

    # Write the modified csv file back to disk
    with open(dest_file, "w") as f:
        for line in stripped_lines:
            f.write(",".join(line))

    # Run the terminal command and print the result
    RunTerminalCommand(directory,EVO_TRAJ_GND_TRUTH_TERMINAL_COMMAND)
    # result = subprocess.run(EVO_TRAJ_GND_TRUTH_TERMINAL_COMMAND, shell=True, capture_output=True, text=True,cwd=(directory))
    # print(directory,result.stdout)
