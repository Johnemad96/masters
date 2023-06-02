#!/usr/bin/env python
import os
import subprocess
import pandas as pd

# to filter output with regex, 
import re



ROOT_DIR = "/home/john/masters/orbslam3_docker/orbslam_modifiedFork/Datasets/carlaDatasets"
STEREO_FOLDER_NAME = "stereo"
OUTPUT_FILENAME = "output.csv"
BASE_TERMINAL_COMMAND = "evo_ape tum " #GroundTruth_Transformed_clean.tum stereo/1/FrameTrajectory_TUM_Format.txt -as --save_plot plot.pgf --save_results stereo/stereo_1_results.zip"
TERMINAL_COMMAND = ""
GROUND_TRUTH_FILE_NAME = "GroundTruth_Transformed_clean.tum "
TRAJECTORY_FILE_NAME = "FrameTrajectory_TUM_Format.txt "
ALIGN = "--align " #--align --correct_scale
# SCALE = "--correct_scale "
SAVE_PLOT_CMD = "--save_plot "
SAVE_RESULTS_CMD = "--save_results "
SAVE_PLOT_FILE = "plot.png "
PLOT_FOLDER_NAME = "Plots"
PLOT_FILE_NAME = ""
RESULTS_FILE_NAME = ""
SAVE_RESULTS_FILE = "results.zip "

if 'ALIGN' in globals():
    RESULT_CSV = "RMSE_ALIGN.csv"
if 'SCALE' in globals():
    RESULT_CSV = "RMSE_ALIGN_SCALE.csv"

New_Added_Zip_Files = []

# global variables for the table size
num_rows = 8 # Assuming each "stereo" folder has 7 subfolders
num_cols = 0

# global variable for the data
data = {}
df = pd.DataFrame(data)

def write_to_csv(col_name, row_idx, value):
    global num_cols, data

    # check if column name exists
    if col_name in data:
        col_data = data[col_name]
    else:
        # create new column
        col_data = [None] * num_rows
        data[col_name] = col_data
        num_cols += 1

    # update value at the specified row index
    col_data[row_idx] = value

    # write to CSV file
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(ROOT_DIR,RESULT_CSV), index=False)

def FilterOutputToExtractRMSEData(output,path):
    # function to extract RMSE data from the command output
    match = re.search(r'rmse\s+(\d+\.\d+)\D', output, re.IGNORECASE)
    if match:
        rmse = float(match.group(1))
    else:
        rmse = -1
        print(output, "\n")
        print("[**ERROR**] : in path", path)
    return rmse
    # pass

def RunTerminalCommand(DIR,CMD):
    result = subprocess.run(CMD, shell=True, capture_output=True, text=True,cwd=(DIR))
    # print(DIR,result.stdout)
    return result

# get a list of all the timestamped folders in the root directory
# timestamped_folders = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]
# timestamped_folders = [f.pop() for f in timestamped_folders if f[0].isdigit() == False]
timestamped_folders = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f)) and f[0].isdigit()]

print(timestamped_folders)
# create an empty dataframe to store the results
# df = pd.DataFrame(columns=['Timestamped Folder Name', '1', '2', '3'])

# timestamped_folders = sorted(os.listdir(timestamped_folders))
# iterate over each timestamped folder
for timestamped_folder in timestamped_folders:
    # find the stereo folder in the timestamped folder
    stereo_folder = os.path.join(ROOT_DIR, timestamped_folder, STEREO_FOLDER_NAME)
    # list the name of the subfolders inside every stereo folder
    stereo_subfolders = [f for f in os.listdir(stereo_folder) if os.path.isdir(os.path.join(stereo_folder, f))]

    # #
    # if (len(stereo_subfolders)+1)>num_rows:
    #     num_rows = num_rows + 1
    # iterate over the subfolders 1, 2, and 3 in the stereo folder
    # for subfolder in ["1", "2", "3"]:
    for subfolder in stereo_subfolders:
        subfolder_path = os.path.join(stereo_folder, subfolder)
        print(timestamped_folder,"\n\t", subfolder)
        subfolder_list = os.listdir(subfolder_path)
        # print(subfolder_list)
        # run the terminal command in the subfolder and filter the output to extract the RMSE data
        # result = subprocess.run(TERMINAL_COMMAND, shell=True, cwd=subfolder_path, capture_output=True, text=True)
        TERMINAL_COMMAND = BASE_TERMINAL_COMMAND + os.path.join(ROOT_DIR, timestamped_folder, GROUND_TRUTH_FILE_NAME)
        TERMINAL_COMMAND = TERMINAL_COMMAND + os.path.join(subfolder_path, TRAJECTORY_FILE_NAME)
        if 'SCALE' in globals():
            TERMINAL_COMMAND = TERMINAL_COMMAND + SCALE    
            PLOT_FOLDER_NAME = PLOT_FOLDER_NAME + "_" + 'ALIGN_SCALE_'  
            print("\t\t", "-ALIGN -SCALE") 
            RESULTS_FILE_NAME = (STEREO_FOLDER_NAME+'_' +subfolder + '_'+'ALIGN_SCALE_'+  SAVE_RESULTS_FILE)
            # if any(s.find(RESULTS_FILE_NAME) != -1 for s in subfolder_list):

            if RESULTS_FILE_NAME.strip() not in subfolder_list:
                New_Added_Zip_Files.append(RESULTS_FILE_NAME.strip())
                print("\t\t-Result file will be created.")
                TERMINAL_COMMAND = TERMINAL_COMMAND + SAVE_RESULTS_CMD + os.path.join(subfolder_path,RESULTS_FILE_NAME)
            else:
                print("\t\t","**-Result file ALREADY EXISTS!.")
        elif 'ALIGN' in globals():
            TERMINAL_COMMAND = TERMINAL_COMMAND + ALIGN 
            PLOT_FOLDER_NAME = PLOT_FOLDER_NAME + "_" + 'ALIGN_'
            print("\t\t", "-ALIGN") 
            RESULTS_FILE_NAME = (STEREO_FOLDER_NAME+'_' +subfolder + '_'+'ALIGN_'+  SAVE_RESULTS_FILE)
            # print((RESULTS_FILE_NAME), subfolder_list[0])
            # if any(s.find(RESULTS_FILE_NAME) != -1 for s in subfolder_list):
            if RESULTS_FILE_NAME.strip() not in subfolder_list:
                New_Added_Zip_Files.append(RESULTS_FILE_NAME.strip())
                print("\t\t", "-Result file will be created.")
                TERMINAL_COMMAND = TERMINAL_COMMAND + SAVE_RESULTS_CMD + os.path.join(subfolder_path,RESULTS_FILE_NAME)
            else:
                print("\t\t","**-Result file ALREADY EXISTS!.")

        # # adding plots
        # PLOT_FILE_NAME = STEREO_FOLDER_NAME + subfolder + SAVE_PLOT_FILE
        # TERMINAL_COMMAND = TERMINAL_COMMAND + SAVE_PLOT_CMD + os.path.join(subfolder_path,PLOT_FOLDER_NAME,PLOT_FILE_NAME)

        # print(TERMINAL_COMMAND)
        # print(RESULTS_FILE_NAME)
        # print("\t\t", TERMINAL_COMMAND)
        result = RunTerminalCommand(subfolder_path, TERMINAL_COMMAND)
        rmse_data = FilterOutputToExtractRMSEData(result.stdout,subfolder_path)
        if rmse_data != -1:
            write_to_csv(timestamped_folder, int(subfolder.split("_")[0]), rmse_data)
        # # if the timestamped folder name is already in the dataframe, update the corresponding row
        # if timestamped_folder in df['Timestamped Folder Name'].values:
        #     df.loc[df['Timestamped Folder Name'] == timestamped_folder, subfolder] = rmse_data
        # # otherwise, create a new row with the timestamped folder name and the RMSE data
        # else:
        #     new_row = {'Timestamped Folder Name': timestamped_folder, subfolder: rmse_data}
        #     df = df.append(new_row, ignore_index=True)
print("Added *.zip Results files are: ", New_Added_Zip_Files)

# save the results to a CSV file
df.to_csv(OUTPUT_FILENAME, index=False)
