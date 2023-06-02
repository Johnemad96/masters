# import rospy
from sensor_msgs.msg import Imu
import pandas as pd
import os

imuData = pd.read_csv('imu_log.csv')
print(imuData)



