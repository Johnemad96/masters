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
import tf2_msgs
import geometry_msgs.msg

pathForGT = "/home/dataset/carlaDatasets/20221112_1/"

class FixedTFBroadcaster:

    def __init__(self,tfMessage):
        self.pub_tf = rospy.Publisher("/tf", tf2_msgs.msg.TFMessage, queue_size=1)

        while not rospy.is_shutdown():
            # Run this loop at about 10Hz
            rospy.sleep(0.1)

        #     t = geometry_msgs.msg.TransformStamped()
        #     t.header.frame_id = "world"
        #     t.header.stamp = rospy.Time.now()
        #     t.child_frame_id = "secondFrame"
        #     t.transform.translation.x = 0.0
        #     t.transform.translation.y = 2.0
        #     t.transform.translation.z = 0.0

        #     t.transform.rotation.x = 0.0
        #     t.transform.rotation.y = 0.0
        #     t.transform.rotation.z = 0.0
        #     t.transform.rotation.w = 1.0
            
            # tfm = tf2_msgs.msg.TFMessage([t])
            tfm = tf2_msgs.msg.TFMessage([tfMessage])
            self.pub_tf.publish(tfm)


if __name__ == '__main__':

        
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
        
        rospy.init_node('my_static_tf2_broadcaster')
        broadcaster = tf2_ros.StaticTransformBroadcaster()
        static_transformStamped = geometry_msgs.msg.TransformStamped()

        static_transformStamped.header.seq = gt['frame'][116] 
        static_transformStamped.header.stamp.secs = gt['timestamp'][116]/100 
        static_transformStamped.header.stamp.nsecs = (int)(((gt['timestamp'][116]/100.0)- static_transformStamped.header.stamp.secs)*(10**9))
        static_transformStamped.header.frame_id = "world"
        static_transformStamped.child_frame_id = "firstFrame"

        static_transformStamped.transform.translation.x = gt['x'][116]
        static_transformStamped.transform.translation.y = gt['y'][116]
        static_transformStamped.transform.translation.z = gt['z'][116]

        eulerFromQuat = tf.transformations.euler_from_quaternion([gt['qx'][116],gt['qy'][116],gt['qz'][116],gt['qw'][116]])
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
        # rospy.spin()
        time.sleep(2)
        # # for i in range():
        
        broadcaster = tf2_ros.TransformBroadcaster()
        transformStamped = geometry_msgs.msg.TransformStamped()

        transformStamped.header.seq = gt['frame'][150] 
        transformStamped.header.stamp.secs = gt['timestamp'][150]/100 
        transformStamped.header.stamp.nsecs = (int)(((gt['timestamp'][150]/100.0)- transformStamped.header.stamp.secs)*(10**9))
        transformStamped.header.frame_id = "world"
        transformStamped.child_frame_id = "secondFrame"

        transformStamped.transform.translation.x = gt['x'][150]
        transformStamped.transform.translation.y = gt['y'][150]
        transformStamped.transform.translation.z = gt['z'][150]

        eulerFromQuat = tf.transformations.euler_from_quaternion([gt['qx'][150],gt['qy'][150],gt['qz'][150],gt['qw'][150]])
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

        # #  listener
        # time.sleep(2)
        # # tfBuffer = tf2_ros.Buffer()
        # # listener = tf2_ros.TransformListener(tfBuffer)
        rate = rospy.Rate(10.0)
        # rate.sleep()

        while not rospy.is_shutdown():

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
            rospy.spin()
            rate.sleep()
        # # while(1):
        # #         continue