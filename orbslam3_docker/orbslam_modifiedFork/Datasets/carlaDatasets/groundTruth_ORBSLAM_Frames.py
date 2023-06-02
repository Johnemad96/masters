import pandas as pd
import math
import numpy as np
import os

import math
 
def euler_from_quaternion(x, y, z, w):
    
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians
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
gt = pd.read_csv( 'GroundTruth.csv') # from rosbag_create.py

modified_gt = {'frame':[],'timestamp':[],'transform':[], 'linear_velocity':[],'angular_velocity':[],'acceleration':[],'roll':[],'pitch':[],'yaw':[]}
modified_gt['roll'] = []
modified_gt['pitch'] = []
modified_gt['yaw'] = []
# modified_gt['transform'].orientation.z = []

i=0
while i < len(gt['timestamp']):
    # modified_gt['frame'].append(gt['frame'][i])
    # modified_gt['timestamp'].append(gt['frame'][i])
    # modified_gt['transform'].append(gt['frame'][i])
    # modified_gt['linear_velocity'].append(gt['frame'][i])
    # modified_gt['angular_velocity'].append(gt['frame'][i])
    # modified_gt['frame'].append(gt['frame'][i])
    # modified_gt['frame'].append(gt['frame'][i])
    temp_roll, temp_pitch, temp_yaw = euler_from_quaternion(gt['qx'][i],gt['qy'][i],gt['qz'][i],gt['qw'][i])
    modified_gt['roll'].append(temp_roll)
    modified_gt['pitch'].append(temp_pitch)
    modified_gt['yaw'].append(temp_yaw)
    i+=1
# print (modified_gt['frame'])

##***** new modified ground truth
## CARLA Frames mapped into ORB-SLAM frames:
## New Frames -> [-y -z x]


csvfilename = "GroundTruth_Modified.csv"
data = pd.DataFrame( columns=['frame', 'timestamp','x','y','z','qw','qx','qy','qz','v_x (m/s)','v_y (m/s)','v_z (m/s)','w_x (rad/s)','w_y (rad/s)','w_z (rad/s)','acc x (m/s^2)','acc y (m/s^2)','acc z (m/s^2)'])
data.to_csv(csvfilename, index=False,header="auto",mode='a')
csvfile = open(csvfilename, "a")
i=0
while i < len(gt['timestamp']):
    # print(i)
    # temp_qx, temp_qy, temp_qz, temp_qw = get_quaternion_from_euler(np.radians(fixOrientationRange(np.round(groundTruth['transform'][i].rotation.roll,decimals=0))),np.radians(fixOrientationRange(np.round(groundTruth['transform'][i].rotation.pitch,decimals=0))),np.radians(fixOrientationRange(groundTruth['transform'][i].rotation.yaw)))
    temp_qx, temp_qy, temp_qz, temp_qw = get_quaternion_from_euler(
        (modified_gt['pitch'][i] - modified_gt['pitch'][0] )* -1 , 
        (modified_gt['yaw'][i] - modified_gt['yaw'][0])* -1,
        (modified_gt['roll'][i] - modified_gt['roll'][0]))
    data = pd.DataFrame([[gt['frame'][i], gt['timestamp'][i],
                        (gt['y'][i] - gt['y'][0])* -1 , (gt['z'][i] - gt['z'][0])* -1 , (gt['x'][i]- gt['x'][0] ) ,
                        temp_qw, temp_qx, temp_qy, temp_qz,
                        gt['v_y (m/s)'][i]-1, gt['v_z (m/s)'][i]* -1, gt['v_x (m/s)'][i],
                        # groundTruth['w_y (rad/s)'][i]*-1, groundTruth['w_z (rad/s)'][i]*-1, groundTruth['w_x (rad/s)'][i],
                        # groundTruth['acc y (m/s^2)'][i]*-1, groundTruth['acc z (m/s^2)'][i]*-1, groundTruth['acc x (m/s^2)'][i],
                        0.0001,0.0001,0.0001,
                        0.0001,0.0001,0.0001
                        ]],
                        columns=['frame', 'timestamp', 'x', 'y', 'z', 'qw', 'qx', 'qy', 'qz', 'v_x (m/s)', 'v_y (m/s)', 'v_z (m/s)', 'w_x (rad/s)', 'w_y (rad/s)', 'w_z (rad/s)', 'acc x (m/s^2)', 'acc y (m/s^2)', 'acc z (m/s^2)'])
    data.to_csv(csvfilename, index=False,header=False,mode='a')
    i+=1
csvfile.close()
