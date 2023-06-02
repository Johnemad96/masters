#!/usr/bin/env python
import rospy

# to get commandline arguments
import sys

import pandas as pd
import math
import numpy as np
import os
import time
# because of transformations
import tf

import tf2_ros
import geometry_msgs.msg


def ImageToDictionary(imageList):
    # image=[]
    image = {'images':[], 'timestamp':[], 'frameID':[]}
    for filename in imageList:
            image['images'].append(filename)
            image['timestamp'].append((int)(filename.split('_')[0]))
            image['frameID'].append((int)(filename.split('_')[1].split('.')[0]))
            # print(image[-1])
    return image

pathForGT = "/home/dataset/carlaDatasets/"

def quat_rotate(rotation, vector):
    """
    Rotate a vector according to a quaternion. Equivalent to the C++ method tf::quatRotate
    :param rotation: the rotation
    :param vector: the vector to rotate
    :return: the rotated vector
    """

    def quat_mult_point(q, w):
        return (q[3] * w[0] + q[1] * w[2] - q[2] * w[1],
                q[3] * w[1] + q[2] * w[0] - q[0] * w[2],
                q[3] * w[2] + q[0] * w[1] - q[1] * w[0],
                -q[0] * w[0] - q[1] * w[1] - q[2] * w[2])

    q = quat_mult_point(rotation, vector)
    q = tf.transformations.quaternion_multiply(
        q, tf.transformations.quaternion_inverse(rotation))
    return [q[0], q[1], q[2]] 

def approx_nanosec_num(num):

        x = (round((num/(10**9)),2))
        return x*(10**9)
#        return ((round((num/(10**9)),2))*(10**9))

if __name__ == '__main__':

        fileName = (sys.argv[1])
        pathForGT = pathForGT + fileName + "/"
        '''
        steps:
                - create a node (to be able to interface with tf using ros)
                - read groundTruth CSV file
                - take the data of the first frame (of the trajectory) and publish it as
                        Static transormation
                - loop:
                        = take the following frame, broadcast w.r.t WORLD
                        = look-up that frame w.r.t the first frame 
                        = check that this was the last sent frame from the frame ID
                        = save the new transformed data to a new DataFrame to save in 
                                a new excel sheet (and add rough gyro and accel bias)
                *** note that the previous steps doesn't mention the linear velocity, 
                    this is still to be descussed. 
        '''
        gt = pd.read_csv( pathForGT+'GroundTruth.csv') # from rosbag_create.py

        '''
        csv frame structure
                ['frame', 
                'timestamp',
                'x','y','z',
                'qw','qx','qy','qz',
                'v_x (m/s)','v_y (m/s)','v_z (m/s)',
                'w_x (rad/s)','w_y (rad/s)','w_z (rad/s)',
                'acc x (m/s^2)','acc y (m/s^2)','acc z (m/s^2)']
        '''

        '''
                the following will do getting the list of images to match its frame ID of the 16th picture
                to match with the frame ID of the ground truth to consider this GroundTruth frame
                as the first one and the 0 /ref of the timestamp
        '''

        left_imagesFolder = sorted(os.listdir(pathForGT + 'left/'))
        leftImages = ImageToDictionary(left_imagesFolder)
        leftImages_refTimestamp = leftImages['timestamp'][15]
        print("*******")
        right_imagesFolder = sorted(os.listdir(pathForGT + 'right/'))
        rightImages = ImageToDictionary(right_imagesFolder)
        rightImages_refTimestamp = rightImages['timestamp'][15]

        first_ground_truth_frame_index = 0
        frame_id_index = 0
        for frame_id_index in range(len(gt['frame'])):
                if gt['frame'][frame_id_index] == leftImages['frameID'][15]:
                        first_ground_truth_frame_index = frame_id_index#gt['frame'][frame_id_index]
                        print("matched frame index: ", first_ground_truth_frame_index)
                        print("-->frameID_Pic: ", leftImages['frameID'][15])
                        print("-->frameID_GT: ", gt['frame'][frame_id_index])
                        break

        rospy.init_node('my_static_tf2_broadcaster')
        broadcaster = tf2_ros.StaticTransformBroadcaster()
        static_transformStamped = geometry_msgs.msg.TransformStamped()

        static_transformStamped.header.seq = gt['frame'][first_ground_truth_frame_index] 
        static_transformStamped.header.stamp.secs = 0 #gt['timestamp'][first_ground_truth_frame_index]/100 
        static_transformStamped.header.stamp.nsecs = 0 #(int)(((gt['timestamp'][first_ground_truth_frame_index]/100.0)- static_transformStamped.header.stamp.secs)*(10**9))
        static_transformStamped.header.frame_id = "world"
        static_transformStamped.child_frame_id = "firstFrame"

        static_transformStamped.transform.translation.x = gt['x'][first_ground_truth_frame_index]
        static_transformStamped.transform.translation.y = gt['y'][first_ground_truth_frame_index]
        static_transformStamped.transform.translation.z = gt['z'][first_ground_truth_frame_index]

        eulerFromQuat = tf.transformations.euler_from_quaternion([gt['qx'][first_ground_truth_frame_index],gt['qy'][first_ground_truth_frame_index],gt['qz'][first_ground_truth_frame_index],gt['qw'][first_ground_truth_frame_index]])
        roll  =   eulerFromQuat[0] - math.pi/2
        pitch =   eulerFromQuat[1]
        yaw   =   eulerFromQuat[2] - math.pi/2
        quat = tf.transformations.quaternion_from_euler(
                   roll,pitch,yaw)

        static_transformStamped.transform.rotation.x = quat[0]
        static_transformStamped.transform.rotation.y = quat[1]
        static_transformStamped.transform.rotation.z = quat[2]
        static_transformStamped.transform.rotation.w = quat[3]
        broadcaster.sendTransform(static_transformStamped)
        # # rospy.spin()
        time.sleep(2)
        # for i in range():
        # rospy.init_node('my_tf2_broadcaster')
        tfBuffer = tf2_ros.Buffer()
        listener = tf2_ros.TransformListener(tfBuffer)
        broadcaster = tf2_ros.TransformBroadcaster()
        transformStamped = geometry_msgs.msg.TransformStamped()
        # i = 200
        # i = 5
        # rate = rospy.Rate(10.0)
        transformedGT =  {'frame':[],'timestamp':[],
                'x':[], 'y':[], 'z':[],
                'qw':[],'qx':[],'qy':[],'qz':[], 
                'v_x (m/s)':[],'v_y (m/s)':[],'v_z (m/s)':[],
                'w_x (rad/s)':[],'w_y (rad/s)':[],'w_z (rad/s)':[],
                'acc x (m/s^2)':[],'acc y (m/s^2)':[],'acc z (m/s^2)':[]}
        previous_sequence = 0
        sequence_counter = 0
        # transofrmation of linear velocity is only rotation
        linearVelocity_x =0
        linearVelocity_y =0
        linearVelocity_z =0
        q_around_z= tf.transformations.quaternion_from_euler(0,0,-math.pi/2) #roll,pitch,yaw
        q_around_x= tf.transformations.quaternion_from_euler(-math.pi/2,0,0) #roll,pitch,yaw

        #create a file to append CSV

        csvfilename = pathForGT + "GroundTruth_Transformed.csv"
        data = pd.DataFrame( columns=['frame', 'timestamp','x','y','z','qw','qx','qy','qz','v_x (m/s)','v_y (m/s)','v_z (m/s)','w_x (rad/s)','w_y (rad/s)','w_z (rad/s)','acc x (m/s^2)','acc y (m/s^2)','acc z (m/s^2)'])
        data.to_csv(csvfilename, index=False,header="auto",mode='a')
        csvfile = open(csvfilename, "a")
        i=first_ground_truth_frame_index

        while not rospy.is_shutdown():
                transformStamped.header.seq = int(gt['frame'][i]) 
                transformStamped.header.stamp.secs = (gt['timestamp'][i] - gt['timestamp'][first_ground_truth_frame_index])/100 
                transformStamped.header.stamp.nsecs = (int)((((gt['timestamp'][i] -  gt['timestamp'][first_ground_truth_frame_index])/100.0)- transformStamped.header.stamp.secs)*(10**9))
                transformStamped.header.frame_id = "world"
                transformStamped.child_frame_id = "secondFrame"
                # if (i==first_ground_truth_frame_index):
                #         print(gt['timestamp'][i] - gt['timestamp'][first_ground_truth_frame_index])
                transformStamped.transform.translation.x = gt['x'][i]
                transformStamped.transform.translation.y = gt['y'][i]
                transformStamped.transform.translation.z = gt['z'][i]

                eulerFromQuat = tf.transformations.euler_from_quaternion([gt['qx'][i],gt['qy'][i],gt['qz'][i],gt['qw'][i]])
                roll  =   eulerFromQuat[0] - math.pi/2
                pitch =   eulerFromQuat[1]
                yaw   =   eulerFromQuat[2] - math.pi/2
                quat = tf.transformations.quaternion_from_euler(
                        roll,pitch,yaw)

                transformStamped.transform.rotation.x = quat[0]
                transformStamped.transform.rotation.y = quat[1]
                transformStamped.transform.rotation.z = quat[2]
                transformStamped.transform.rotation.w = quat[3]

                # tf_ob = FixedTFBroadcaster(transformStamped)
                broadcaster.sendTransform(transformStamped)  

                previous_sequence = transformStamped.header.stamp.secs   
                rospy.sleep(0.1)
                # q= tf.transformations.quaternion_from_euler(0,0,-math.pi/2) #roll,pitch,yaw

                # print(tf2_.transformations.quatRotate(q,linearVel))
                temp_velocity_vector = quat_rotate(q_around_z,[gt['v_x (m/s)'][i],gt['v_y (m/s)'][i],gt['v_z (m/s)'][i]])
                # q= tf.transformations.quaternion_from_euler(-math.pi/2,0,0) #roll,pitch,yaw

                transformed_Velocity = quat_rotate(q_around_x,temp_velocity_vector)
                try:
                        trans = tfBuffer.lookup_transform("firstFrame","secondFrame", rospy.Time(),)
                except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                        # rate.sleep()
                        continue

                # print( gt['frame'][i] ,trans.header.seq, trans.transform.translation.z)
                # # rospy.spin()

                data = pd.DataFrame([[gt['frame'][i], (round(gt['timestamp'][i] - gt['timestamp'][first_ground_truth_frame_index],-7)),
                # data = pd.DataFrame([[gt['frame'][i], (round(((approx_nanosec_num(gt['timestamp'][i] - gt['timestamp'][first_ground_truth_frame_index]))),-7)),
                        trans.transform.translation.x,trans.transform.translation.y,trans.transform.translation.z,
                        trans.transform.rotation.w, trans.transform.rotation.x, trans.transform.rotation.y, trans.transform.rotation.z,
                        transformed_Velocity[0], transformed_Velocity[1],transformed_Velocity[2],
                        # groundTruth['w_y (rad/s)'][i]*-1, groundTruth['w_z (rad/s)'][i]*-1, groundTruth['w_x (rad/s)'][i],
                        # groundTruth['acc y (m/s^2)'][i]*-1, groundTruth['acc z (m/s^2)'][i]*-1, groundTruth['acc x (m/s^2)'][i],
                        -0.002153,0.020744,0.075806,
                        -0.013337,0.103464,0.093086
                        ]],
                        columns=['frame', 'timestamp', 'x', 'y', 'z', 'qw', 'qx', 'qy', 'qz', 'v_x (m/s)', 'v_y (m/s)', 'v_z (m/s)', 'w_x (rad/s)', 'w_y (rad/s)', 'w_z (rad/s)', 'acc x (m/s^2)', 'acc y (m/s^2)', 'acc z (m/s^2)'])
                data.to_csv(csvfilename, index=False,header=False,mode='a')

                if (previous_sequence == trans.header.stamp.secs ) :
                        print (i)
                        i = i + 1
                        if (i >= (len(gt['timestamp']))):
                                print( " lenght =  " + str(i))
                                break
                # i = i + 1
                #  listener
                # time.sleep(2)
                # tfBuffer = tf2_ros.Buffer()
                # listener = tf2_ros.TransformListener(tfBuffer)
                # if i >=1000:
                #         break
                # rate.sleep()


                #         try:
                #                 trans = tfBuffer.lookup_transform("secondFrame", "firstFrame", rospy.Time())
                #                 time.sleep(1)
                #                 print("trans: " + trans.transform.translation.x)
                #                 rate.sleep*()
                #                 break
                #         except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                #                 print("  exception !!")
                #                 rate.sleep()
                #         #     continue
                        # rate.sleep()
                # # while(1):
                # #         continue