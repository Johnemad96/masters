#!/usr/bin/env python3
import os
from parseResults import ParseResults_SubSubfolder, Update_Global_Variables
from readParams import Read_Required_Params

def find_files(root_dir, target_file, target_folder, only_digit_folders=False):
    print(root_dir)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(dirpath, dirnames, filenames)
        if target_file in filenames and target_folder in dirpath:
            # if only_digit_folders is True, check if the directory name starts with a digit
            if only_digit_folders and not os.path.basename(dirpath)[0].isdigit():
                continue
            # remove the target_file from the path
            target_dir = dirpath
            # process the files in target_dir
            process_files(target_dir)
            # remove the first two parts of the path
            parts = target_dir.split(os.sep)[9:-1]
            relative_dir = os.sep.join(parts)
            # since you mentioned that once you find a target_file, 
            # you can assume that all other subfolders will have the same structure,
            # we can break the loop here to avoid unnecessary searching
            break
    return target_dir, relative_dir

def process_files(target_dir):
    # here goes the logic of your script
    # you can iterate over the subfolders in target_dir and do whatever processing you need
    pass

if __name__ == "__main__":
    parameters = Update_Global_Variables('parseResults_Generic_EVO_Parameters.txt')
    # print(parameters)
    # usage:
    # full_path, relative_path = find_files("carlaDatasets/testParametersEffect", "FrameTrajectory_TUM_Format.txt", "stereo")
    full_path, relative_path = find_files(parameters['ROOT_DIR'], "FrameTrajectory_TUM_Format.txt", parameters['STEREO_FOLDER_NAME'])
    print("Full path:", full_path)
    print("Relative path:", relative_path)
    # print(os.listdir(os.path.join(parameters['ROOT_DIR'],relative_path)))
    subfolder = '30_0'
    subfolder_path = os.path.join(parameters['ROOT_DIR'],relative_path,subfolder)
    subfolder_list = os.listdir(subfolder_path)
    dataset_ground_truth_folder = parameters['ROOT_DIR'].split(os.sep)[1]
    print(subfolder,subfolder_list, subfolder_path,dataset_ground_truth_folder)
    print("***** SUBFOLDER PATH", subfolder_path)
    ParseResults_SubSubfolder(subfolder,subfolder_list, subfolder_path)
    # subfolder:                    subfolder name under stereo(/1/, /2/, /3/)
    # subfolder_path:               path from ROOT till the subfolder (under stereo: /1/, /2/, /3/)
    # subfolder_list:               list of files (and possibly folders) under the subfolder path which is the trajectory txt files
    # dataset_ground_truth_folder:  renamed from timestamped_folder, the folder inside "carlaDatasets/" which contains the groundtruth file,
    #                               stereo/stereo_inertial folder

