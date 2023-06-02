import numpy as np
import pandas as pd
def get_quaternion_from_euler(roll, pitch, yaw):
    """
    Convert an Euler angle to a quaternion.

    Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.

    Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
    """
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return qx, qy, qz, qw

import os
import sys
directory = sys.argv[1]
# read excel (csv) file for to import data to convert
fileToConvert = pd.read_csv(directory + 'GroundTruth.csv')
og_x = 0
og_y = 0
og_z = 0

# create a csv file to save the quaternion angles after conversion
csvfilename = directory + "GroundTruth_EulerToQuaternion.csv" #filename.insert(len(filename)-4,"_pynmea2Converted")
data = pd.DataFrame( columns=['qw','qx','qy','qz'])
data.to_csv(csvfilename, index=False,header="auto",mode='a')
csvfile = open(csvfilename, "a")

for i in range(len(fileToConvert)):
    og_x = fileToConvert['roll'][i]
    og_y = fileToConvert['pitch'][i] * -1
    og_z = fileToConvert['yaw'][i] * -1
    temp_qx, temp_qy, temp_qz, temp_qw = get_quaternion_from_euler(np.radians(og_x) ,np.radians(og_y),np.radians(og_z))
    data = pd.DataFrame([[ temp_qw,temp_qx, temp_qy, temp_qz]], columns=['qw','qx','qy','qz'])
    data.to_csv(csvfilename, index=False,header=False,mode='a')
csvfile.close()