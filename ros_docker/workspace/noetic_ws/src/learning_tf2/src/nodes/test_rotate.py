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

# linearVel = geometry_msgs.msg.Vector3Stamped()
# linearVel.vector.x = 3
# linearVel.vector.y = 1
# linearVel.vector.z = 0.5
vec = [3,1,0.5]
q= tf.transformations.quaternion_from_euler(0,0,-math.pi/2) #roll,pitch,yaw

# print(tf2_.transformations.quatRotate(q,linearVel))
temp = (quat_rotate(q,vec))
q= tf.transformations.quaternion_from_euler(-math.pi/2,0,0) #roll,pitch,yaw

# print(tf2_.transformations.quatRotate(q,linearVel))
print (quat_rotate(q,temp))