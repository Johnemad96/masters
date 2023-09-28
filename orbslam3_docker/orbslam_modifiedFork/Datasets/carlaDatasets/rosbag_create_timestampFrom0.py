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

# datasetBaseDirectory = '/home/john/masters/carla/scripts/dataset/'
def createARosBag(filenameToSave):
    # datasetDirectory = datasetBaseDirectory
    datasetDirectory = filenameToSave + '/'
    rosbagName = '43_PaperDataset_Town10_'+ filenameToSave +'_rain&fog_50'+'_euroc'
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
    leftImages_refTimestamp = (leftImages['timestamp'][15])
    print("*******")
    right_imagesFolder = sorted(os.listdir(datasetDirectory + 'right/'))
    rightImages = ImageToDictionary(right_imagesFolder)
    rightImages_refTimestamp = (rightImages['timestamp'][15])
    # print(rightImages['images'][4])

    # print((rightImages[1]['timestamp']/100.0))
    # print(rightImages[2]['images'])
    # # img = cv2.imread('left/'+ (leftImages[1]['images']),cv2.IMREAD_GRAYSCALE)
    # # print(img)
    # # print(len(rightImages))
    # # print(bridge.cv2_to_imgmsg(img,encoding="passthrough").header)

    imuExcel = pd.read_csv(datasetDirectory + 'imu_log.csv')
    # imu_refTimestamp = imuExcel['timestamp'][0]

    # print(imuExcel['timestamp'])
    # print(imuExcel['timestamp'][0])
    bag = rosbag.Bag(rosbagName + '.bag','w')
    bridge = CvBridge()
    imu_temp = Imu()
    # print(len(imuExcel['frame']))
    firstImuFrameIndex = -1
    newCameraData=0
    for i in range(len(imuExcel['frame'])):
        # skipping the first 15 images and guarranting that the 1st imu frame id to be considered is matching
        # to the frame id of the left images (and consecquently the right images as well)
        if (imuExcel['frame'][i] < leftImages['frameID'][15]) and (firstImuFrameIndex == -1):
             continue
        else:
            # firstImuFrameIndex = firstImuFrameIndex + 1
            if (firstImuFrameIndex == -1):
                firstImuFrameIndex = i
                imu_refTimestamp = round(imuExcel['timestamp'][i],2)
                print("First IMU Frame ID: ", imuExcel['frame'][i])
        imu_temp.header.seq = (i - firstImuFrameIndex)
        imu_temp.header.stamp.secs = (int)(round(imuExcel['timestamp'][i],2) - imu_refTimestamp)
        imu_temp.header.stamp.nsecs = (int)(((round(imuExcel['timestamp'][i],2) - imu_refTimestamp) - imu_temp.header.stamp.secs) * (10**9)) 
        # if imu_temp.header.stamp.secs <0 or imu_temp.header.stamp.nsecs <0:
            #  print("**ERROR**", " Frame ID " ,imuExcel['frame'][i])
        imu_temp.header.frame_id = str(imuExcel['frame'][i])
        imu_temp.angular_velocity.x = imuExcel['gyro x (rad/s)'][i]
        imu_temp.angular_velocity.y = imuExcel['gyro y (rad/s)'][i]
        imu_temp.angular_velocity.z = imuExcel['gyro z (rad/s)'][i]
        imu_temp.linear_acceleration.x = imuExcel['acc x (m/s^2)'][i]
        imu_temp.linear_acceleration.y = imuExcel['acc y (m/s^2)'][i]
        imu_temp.linear_acceleration.z = imuExcel['acc z (m/s^2)'][i]
        bag.write('/imu',imu_temp,imu_temp.header.stamp)
        if ((i - firstImuFrameIndex)%5) == 0 :
            cameraFrameIndex = ((i - firstImuFrameIndex) + 5*15)
            if (imuExcel['frame'][i] == leftImages['frameID'][(int)(cameraFrameIndex/5)]):
                newCameraData=1
                # print(imuExcel['frame'][i])
                img_temp = cv2.imread(datasetDirectory + 'left/'+ (leftImages['images'][(int)(cameraFrameIndex/5)]))
                leftImage_temp = bridge.cv2_to_imgmsg(img_temp,"bgr8")
                leftImage_temp.header.seq = i
                leftImage_temp.header.stamp.secs = (leftImages['timestamp'][(int)(cameraFrameIndex/5)] - leftImages_refTimestamp)/100
                leftImage_temp.header.stamp.nsecs = (int)((((leftImages['timestamp'][(int)(cameraFrameIndex/5)] - leftImages_refTimestamp)/100.0)- leftImage_temp.header.stamp.secs)*(10**9))
                leftImage_temp.header.frame_id = str(leftImages['frameID'][(int)(cameraFrameIndex/5)])
                bag.write('/camera/left/image_raw',leftImage_temp,leftImage_temp.header.stamp)

                img_temp = cv2.imread(datasetDirectory + 'right/'+ (rightImages['images'][(int)(cameraFrameIndex/5)]))
                rightImage_temp = bridge.cv2_to_imgmsg(img_temp,"bgr8")
                rightImage_temp.header.seq = i
                rightImage_temp.header.stamp.secs = ((rightImages['timestamp'][(int)(cameraFrameIndex/5)] - rightImages_refTimestamp)/100)
                rightImage_temp.header.stamp.nsecs = (int)((((rightImages['timestamp'][(int)(cameraFrameIndex/5)] - rightImages_refTimestamp)/100.0)- rightImage_temp.header.stamp.secs)*(10**9))
                rightImage_temp.header.frame_id = str(rightImages['frameID'][(int)(cameraFrameIndex/5)])
                bag.write('/camera/right/image_raw',rightImage_temp,rightImage_temp.header.stamp)
            else:
                newCameraData=0
                print("FrameID Imu - Camera L/R",imuExcel['frame'][i], " - ",  (leftImages['frameID'][(int)(cameraFrameIndex/5)]) , " / " , (rightImages['frameID'][(int)(cameraFrameIndex/5)]))
        else:
            newCameraData=0
        if newCameraData ==1:
            data = pd.DataFrame([[imuExcel['frame'][i],(round(imuExcel['timestamp'][i],2) - imu_refTimestamp), (leftImages['timestamp'][(int)(cameraFrameIndex/5)] - leftImages_refTimestamp),
                        ]],
                        columns=['FrameID','ImuTimeStamp', 'CameraTimestamp'])
        else:
            data = pd.DataFrame([[imuExcel['frame'][i],(round(imuExcel['timestamp'][i],2) - imu_refTimestamp), 0,
                        ]],
                        columns=['FrameID','ImuTimeStamp', 'CameraTimestamp'])
        data.to_csv(rosbagName + ".csv", index=False,header=False,mode='a')

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