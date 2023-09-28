#!/usr/bin/env python
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
parent_dir = os.sep.join(current_dir.split(os.sep)[:-2])
print(parent_dir)
sys.path.insert(1, parent_dir)

import rospy

from changeYamlFileValues import Change_Yaml_Parameters
from readParams import Read_Required_Params
from createIcrementedDatasetTestFolder import create_incremented_folder
from parseResults import ParseResults_SubSubfolder, Update_Global_Variables
from automateORBSLAM import list_bag_files, Run_ORBSlam_and_Dataset
from parseResults_Generic import find_files
from std_msgs.msg import String, Float32
import time
# quick test
# import sys
# # import rospy
# from learning_tf2.srv import *

received_rmse = 0
last_received_rmse = 0

def is_float_num(n):
    return isinstance(n, (int, float)), isinstance(n, float)

class Receiver:
    def __init__(self,rospy):
        self.received_expected_data = False
        # rospy.init_node('receiver')
        rospy.Subscriber('rmse_to_GA', Float32, self.callback)

    def callback(self, msg):
        global received_rmse
        rospy.loginfo('Received: %s', msg.data)
        is_digit, is_float = is_float_num(msg.data)
        if is_digit == True:
            self.received_expected_data = True
            received_rmse = msg.data

    def spin(self):
        rate = rospy.Rate(1)  # 1 Hz
        while not rospy.is_shutdown() and not self.received_expected_data:
            rate.sleep()
        self.received_expected_data = False  

class Sender:
    def __init__(self,rospy):
        # rospy.init_node('sender')
        self.publisher = rospy.Publisher('cmd_from_GA', String, queue_size=10)
    def send(self, data):
        msg = String()
        msg.data = data
        # print(msg.data)
        self.publisher.publish(msg)


if __name__ == "__main__":

    parameters = Read_Required_Params('optimizationParameters.txt')
    dataset_dir = parameters['dataset_dir']
    root_dir = parameters['root_dir']
    test_results_path = '/Datasets/carlaDatasets/_paperResults/' #parameters['test_results_path']
    test_parameter = 'RainFogNighttime_defaultparameter' #parameters['test_parameter']

    bag_files, filtered_files = list_bag_files(dataset_dir, ["20230401_7", "rain&fog_night"])
    pathToSaveTestResults_testParameter = create_incremented_folder(test_results_path, folder_name_suffix=test_parameter)
    rospy.init_node('GA_Node')
    sender = Sender(rospy)
    time.sleep(1)
    receiver = Receiver(rospy)
    time.sleep(1)
    for i in range(3):
        new_ThDepth = 35.0
        new_ORBextractor_nFeatures = 1200

        new_ThDepth = new_ThDepth*1.0
        # Change_Yaml_Parameters(new_ThDepth=new_ThDepth, new_ORBextractor_nFeatures = new_ORBextractor_nFeatures)
        pathToSaveTestResults = os.path.join(pathToSaveTestResults_testParameter,((str(int(new_ThDepth)).zfill(4)) +"_"+ (str(new_ORBextractor_nFeatures).zfill(4))).replace('.', '_'))

        pathToSaveTestResults = create_incremented_folder(pathToSaveTestResults_testParameter, folder_name_suffix=((str(int(new_ThDepth)).zfill(4)) +"_"+ (str(new_ORBextractor_nFeatures).zfill(4))).replace('.', '_'))

        # os.makedirs(pathToSaveTestResults, exist_ok=True)
        print("running orb slam")
        Run_ORBSlam_and_Dataset(filtered_files[0], pathToSaveTestResults)
        # time.sleep(3)

        # full_path, relative_path = find_files(parameters['ROOT_DIR'], "FrameTrajectory_TUM_Format.txt", parameters['STEREO_FOLDER_NAME'],parameters['test_parameter'])
        evaluationParameters =Update_Global_Variables("parseResultsParameters.txt")
        _ , resultInstance_Index = os.path.split(pathToSaveTestResults_testParameter)
        subfolder_path, subfolder = os.path.split(pathToSaveTestResults)
        subfolder_path = (os.path.join(subfolder_path, subfolder))
        print(resultInstance_Index,"\n", subfolder,"\n" ,subfolder_path,"\n", os.getcwd())
        if "FrameTrajectory_TUM_Format.txt" in sorted(os.listdir(pathToSaveTestResults)):
            eval_command = ParseResults_SubSubfolder(subfolder, sorted(os.listdir(subfolder_path)),
                                    subfolder_path, 
                                    dataset_ground_truth_folder=evaluationParameters['dataset_ground_truth_folder'], 
                                    Stereo_Folder_Name=resultInstance_Index, 
                                    external_server_evaluation=True)
            print(eval_command)
        # eval_command = "evo_ape tum /Datasets/optimization/GA/Daytime_Normal_GroundTruth_Transformed_clean.tum /Datasets/optimization/GA/GAtests/22_2params_baseline_ORBextractor_nFeatures/01_0095_0600/FrameTrajectory_TUM_Format.txt --align --save_results /Datasets/optimization/GA/GAtests/22_2params_baseline_ORBextractor_nFeatures/01_0095_0600/22_2params_baseline_ORBextractor_nFeatures_01_0095_0600_ALIGN_results.zip"
        # rospy.wait_for_service('evaluate_SLAM_Evo')
        # try:
        #     evaluate_SLAM_Evo = rospy.ServiceProxy('evaluate_SLAM_Evo', evaluateSLAMEvo)
        #     resp1 = evaluate_SLAM_Evo(eval_command)
        # except rospy.ServiceException as e:
        #     print("Service call failed: %s"%e)    
        sender.send(eval_command)
        receiver.spin()
        print(received_rmse)
