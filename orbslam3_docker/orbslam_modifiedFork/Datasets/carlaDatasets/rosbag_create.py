# important note: for ros melodic and older, run with python 2
import sys
import rospy
from sensor_msgs.msg import Imu, Image
import pandas as pd
import os
from cv_bridge import CvBridge
import cv2
import rosbag
import time
# def ImageToDictionary(imageList):
#     image=[]
#     temp = {'images':"", 'timestamp':0, 'frameID':0}
#     for filename in imageList:
#         temp['images'] = filename
#         temp['timestamp'] = (int)(filename.split('_')[0])
#         temp['frameID'] = (filename.split('_')[1].split('.')[0])
#         image.append(temp) 
#         print(image[-1])
#     print(image[2]['images'])
#     return image
# filenameToSave = '20221210_1'
def createARosBag(filenameToSave):
    datasetDirectory = filenameToSave + '/'
    rosbagName = '41_PaperDataset_Town10_'+ filenameToSave +'_rainfog30'+'_euroc'
    def ImageToDictionary(imageList):
        # image=[]
        image = {'images':[], 'timestamp':[], 'frameID':[]}
        for filename in imageList:
            image['images'].append(filename)
            image['timestamp'].append((int)(filename.split('_')[0]))
            image['frameID'].append((int)(filename.split('_')[1].split('.')[0]))
            # print(image[-1])
        return image


    left_imagesFolder = sorted(os.listdir(datasetDirectory + 'left/'))  
    leftImages = ImageToDictionary(left_imagesFolder)
    print("*******")
    right_imagesFolder = sorted(os.listdir(datasetDirectory + 'right/'))
    rightImages = ImageToDictionary(right_imagesFolder)

    # print(rightImages['images'][4])

    # print((rightImages[1]['timestamp']/100.0))
    # print(rightImages[2]['images'])
    # # img = cv2.imread('left/'+ (leftImages[1]['images']),cv2.IMREAD_GRAYSCALE)
    # # print(img)
    # # print(len(rightImages))
    # # print(bridge.cv2_to_imgmsg(img,encoding="passthrough").header)

    imuExcel = pd.read_csv(datasetDirectory + 'imu_log.csv')
    # print(imuExcel['timestamp'])
    # print(imuExcel['timestamp'][0])
    bag = rosbag.Bag(rosbagName + '.bag','w')
    bridge = CvBridge()
    imu_temp = Imu()
    print(len(imuExcel['frame']))
    for i in range(len(imuExcel['frame'])):
        imu_temp.header.seq = i
        imu_temp.header.stamp.secs = (int)(imuExcel['timestamp'][i])
        imu_temp.header.stamp.nsecs = (int)(((imuExcel['timestamp'][i]) - imu_temp.header.stamp.secs) * (10**9)) 
        imu_temp.header.frame_id = str(imuExcel['frame'][i])
        imu_temp.angular_velocity.x = imuExcel['gyro x (rad/s)'][i]
        imu_temp.angular_velocity.y = imuExcel['gyro y (rad/s)'][i]
        imu_temp.angular_velocity.z = imuExcel['gyro z (rad/s)'][i]
        imu_temp.linear_acceleration.x = imuExcel['acc x (m/s^2)'][i]
        imu_temp.linear_acceleration.y = imuExcel['acc y (m/s^2)'][i]
        imu_temp.linear_acceleration.z = imuExcel['acc z (m/s^2)'][i]
        bag.write('/imu',imu_temp,imu_temp.header.stamp)
        if i%5 == 0 :
            img_temp = cv2.imread(datasetDirectory + 'left/'+ (leftImages['images'][(int)(i/5)]))
            leftImage_temp = bridge.cv2_to_imgmsg(img_temp,"bgr8")
            leftImage_temp.header.seq = i
            leftImage_temp.header.stamp.secs = leftImages['timestamp'][(int)(i/5)]/100
            leftImage_temp.header.stamp.nsecs = (int)(((leftImages['timestamp'][(int)(i/5)]/100.0)- leftImage_temp.header.stamp.secs)*(10**9))
            leftImage_temp.header.frame_id = str(leftImages['frameID'][(int)(i/5)])
            bag.write('/camera/left/image_raw',leftImage_temp,leftImage_temp.header.stamp)

            img_temp = cv2.imread(datasetDirectory + 'right/'+ (rightImages['images'][(int)(i/5)]))
            rightImage_temp = bridge.cv2_to_imgmsg(img_temp,"bgr8")
            rightImage_temp.header.seq = i
            rightImage_temp.header.stamp.secs = rightImages['timestamp'][(int)(i/5)]/100
            rightImage_temp.header.stamp.nsecs = (int)(((rightImages['timestamp'][(int)(i/5)]/100.0)- rightImage_temp.header.stamp.secs)*(10**9))
            rightImage_temp.header.frame_id = str(rightImages['frameID'][(int)(i/5)])
            bag.write('/camera/right/image_raw',rightImage_temp,rightImage_temp.header.stamp)

    bag.close()
    print("Bag file created with the name ",rosbagName)
    # for i in range(len(leftImages['images'])):
    #     img_temp = cv2.imread('left/'+ (leftImages['images'][i]))
    #     leftImage_temp = bridge.cv2_to_imgmsg(img_temp,"bgr8")
    #     leftImage_temp.header.seq = i
    #     leftImage_temp.header.stamp.secs = leftImages['timestamp'][i]/100
    #     leftImage_temp.header.stamp.nsecs = (int)(((leftImages['timestamp'][i]/100.0)- leftImage_temp.header.stamp.secs)*(10**9))
    #     leftImage_temp.header.frame_id = str(leftImages['frameID'][i])
    #     bag.write('/camera/left/image_raw',leftImage_temp,leftImage_temp.header.stamp)

    #     img_temp = cv2.imread('right/'+ (rightImages['images'][i]))
    #     rightImage_temp = bridge.cv2_to_imgmsg(img_temp,"bgr8")
    #     rightImage_temp.header.seq = i
    #     rightImage_temp.header.stamp.secs = rightImages['timestamp'][i]/100
    #     rightImage_temp.header.stamp.nsecs = (int)(((rightImages['timestamp'][i]/100.0)- rightImage_temp.header.stamp.secs)*(10**9))
    #     rightImage_temp.header.frame_id = str(rightImages['frameID'][i])
    #     bag.write('/camera/right/image_raw',rightImage_temp,rightImage_temp.header.stamp)

    # bag.close()
if __name__ == '__main__':

        fileName = (sys.argv[1])
        createARosBag(fileName)