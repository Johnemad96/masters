#!/usr/bin/env python2

import sys
import rospy
from learning_tf2.srv import *

if __name__ == "__main__":
    eval_command = "evo_ape tum /Datasets/optimization/GA/Daytime_Normal_GroundTruth_Transformed_clean.tum /Datasets/optimization/GA/GAtests/21_2params_baseline_ORBextractor_nFeatures/01_0095_0600/FrameTrajectory_TUM_Format.txt --align --save_results /Datasets/optimization/GA/GAtests/21_2params_baseline_ORBextractor_nFeatures/01_0095_0600/21_2params_baseline_ORBextractor_nFeatures_01_0095_0600_ALIGN_results.zip"
    rospy.wait_for_service('evaluate_SLAM_Evo')
    try:
        evaluate_SLAM_Evo = rospy.ServiceProxy('evaluate_SLAM_Evo', evaluateSLAMEvo)
        resp1 = evaluate_SLAM_Evo(eval_command)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)