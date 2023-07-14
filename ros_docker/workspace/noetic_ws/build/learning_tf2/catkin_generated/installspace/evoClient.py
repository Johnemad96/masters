#!/usr/bin/env python3

import sys
import rospy
from learning_tf2.srv import *
from std_msgs.msg import String, Float32

"""
this file is a middle node that handles data transfer between Genetic Algorithm and Evo tool
Notes:
    GA runs from inside docker container (orbslam_modifiedFork)
    Evo tool runs locally since it needs anaconda env.
How everything works:
    GA Node (Sender, sends evo command)             --> this node (receiver), act as (client) and call evo server               --> evo (Server) locally, called
                                                                                                                                                ||||
    GA Node (Receiver, receives RMSE from this Node)<-- this node (Client), receives RMSE, & sends (Sender) it to GA (Receiver) <-- evo (Server) local, send RMSE value   
"""

received_cmd = ""
last_received_cmd = ""

def requestEvaluation(eval_command):
    rospy.wait_for_service('evaluate_SLAM_Evo')
    try:
        evaluate_SLAM_Evo = rospy.ServiceProxy('evaluate_SLAM_Evo', evaluateSLAMEvo)
        resp1 = evaluate_SLAM_Evo(eval_command)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        resp1 = -999
    return resp1

class Receiver:
    def __init__(self,rospy):
        self.received_expected_data = False
        # rospy.init_node('receiver')
        rospy.Subscriber('cmd_from_GA', String, self.callback)

    def callback(self, msg):
        global received_cmd
        rospy.loginfo('Received: %s', msg.data)
        if msg.data.startswith("evo_ape"):
            self.received_expected_data = True
            received_cmd = msg.data

    def spin(self):
        rate = rospy.Rate(1)  # 1 Hz
        while not rospy.is_shutdown() and not self.received_expected_data:
            rate.sleep()
        self.received_expected_data = False  

class Sender:
    def __init__(self,rospy):
        # rospy.init_node('sender')
        self.publisher = rospy.Publisher('rmse_to_GA', Float32, queue_size=10)
    def send(self, data):
        msg = Float32()
        msg.data = data
        self.publisher.publish(msg)

if __name__ == "__main__":
    # eval_command = "evo_ape tum /Datasets/optimization/GA/Daytime_Normal_GroundTruth_Transformed_clean.tum /Datasets/optimization/GA/GAtests/21_2params_baseline_ORBextractor_nFeatures/01_0095_0600/FrameTrajectory_TUM_Format.txt --align --save_results /Datasets/optimization/GA/GAtests/21_2params_baseline_ORBextractor_nFeatures/01_0095_0600/21_2params_baseline_ORBextractor_nFeatures_01_0095_0600_ALIGN_results.zip"
    
    # rospy.wait_for_service('evaluate_SLAM_Evo')
    # try:
    #     evaluate_SLAM_Evo = rospy.ServiceProxy('evaluate_SLAM_Evo', evaluateSLAMEvo)
    #     resp1 = evaluate_SLAM_Evo(eval_command)
    # except rospy.ServiceException as e:
    #     print("Service call failed: %s"%e)
    rospy.init_node('evoClient_middle_node')
    receiver = Receiver(rospy)
    sender = Sender(rospy)
    receiver.spin()
    if received_cmd != "" and received_cmd != last_received_cmd:
        rmse = requestEvaluation(received_cmd)
        last_received_cmd = received_cmd
    sender.send(rmse)
    
    