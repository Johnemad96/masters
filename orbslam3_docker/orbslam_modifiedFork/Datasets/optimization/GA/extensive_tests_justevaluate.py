# Python 2 code to process the CSV file as per the requirements

import csv
import re
# Read the CSV file

#!/usr/bin/env python
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
parent_dir = os.sep.join(current_dir.split(os.sep)[:-2])
print(parent_dir)
sys.path.insert(1, parent_dir)

import rospy
from decimal import Decimal
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


def parse_tuple(cell):
    # Remove the parentheses and split the string by comma
    items = cell.strip('()').split(',')
    # Convert each item to a float and return as tuple
    return tuple(map(float, items))
    
# def search_dataset(time_of_day, weather_condition):
#     with open('dataset_groundtruth.csv', 'rb') as csvfile:
#         lookUpGroundTruth = csv.reader(csvfile)
#         next(lookUpGroundTruth, None)  # skip the headers
#         for row in lookUpGroundTruth:
#             if row[0] == time_of_day and row[1] == weather_condition:
#                 return row[2], row[3]
#     return None, None
def search_dataset(time_of_day, weather_condition, dataset_index):
    with open('dataset_groundtruth.csv', 'rb') as csvfile:
        lookUpGroundTruth = csv.reader(csvfile)
        next(lookUpGroundTruth, None)  # skip the headers
        for row in lookUpGroundTruth:
            # print(row[0], time_of_day)
            # print(row[1], weather_condition)
            # print(row[2], dataset_index)
            if row[0] == time_of_day and row[1] == weather_condition and row[2] == dataset_index:
                return row[3], (row[4]+" ")
    return None, None
if __name__ == "__main__":

    with open('extensive_test.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)  # skip the header row
        
        # print(time_of_day, weather_condition)
        # print(search_dataset("daytime", "Normal", "Dataset "+str(1)))
        # next(csvreader, None)  # skip the headers
        # next(csvreader, None)  # skip the headers
        # next(csvreader, None)  # skip the headers
        # next(csvreader, None)  # skip the headers
        test_results_path = '/Datasets/optimization/GA/longPathTraj/' #parameters['test_results_path']
        test_parameter = 'GA_ParamTest' #parameters['test_parameter']
        test_results_path_list = sorted(os.listdir(test_results_path))

        testCaseIndex =0
        for row in csvreader:
            testCaseIndex +=1
            # Extract time of day and weather condition from the index
            # time_of_day, weather_condition = row[0].split()[0], row[0].split()[1]
            # Extract time of day from the first level of the index
            time_of_day = row[0]

            # Extract weather condition from the second level of the index
            weather_condition = row[1]
            # Extract parameters from the "Parameter" column
            # parameters = row[2][1:-1].split(",")  # remove parentheses and split by comma
            # parameters = re.findall(r"[-+]?\d*\.\d+|\d+", row[2])
            parsed_tuple = parse_tuple(row[2])
            # print(parse_tuple)
            parameters = parsed_tuple
            # print(parameters)
            parameter1, parameter2, parameter3, parameter4 = parsed_tuple
            # print(parameter1, parameter2, parameter3, parameter4 )
            # Loop over the 3 datasets and 3 tests
            parameters = Read_Required_Params('optimizationParameters.txt')
            dataset_dir = parameters['dataset_dir']
            root_dir = parameters['root_dir']

            pathToSaveTestResults = os.path.join(test_results_path, test_results_path_list[testCaseIndex-1] )
            TestResultslist = sorted(os.listdir(pathToSaveTestResults))
            # pathToSaveTestResults_testParameter = create_incremented_folder(test_results_path, folder_name_suffix=test_parameter)
            rospy.init_node('GA_Node')
            sender = Sender(rospy)
            time.sleep(1)
            receiver = Receiver(rospy)
            time.sleep(1)
            rowDatasetResults = []
            dataset_index=0
            for dataset in range(1, 4):
                for test in range(1, 4):
                    
                    # print(dataset," ", test)
                    dataset_date, groundTruthFileName = search_dataset(time_of_day, weather_condition, "Dataset "+str(dataset))
                    # print(time_of_day, weather_condition, dataset_date, groundTruthFileName, dataset)
                    # bag_files, filtered_files = list_bag_files(dataset_dir, [dataset_date])
                    
                    # new_ThDepth = parameter1
                    # new_ORBextractor_nFeatures = Decimal(parameter2)

                    # new_ThDepth = new_ThDepth*1.0
                    # Change_Yaml_Parameters(new_ThDepth=new_ThDepth, new_ORBextractor_nFeatures = new_ORBextractor_nFeatures, ORBextractor_iniThFAST = Decimal(parameter3), ORBextractor_minThFAST = Decimal(parameter4))
                    # pathToSaveTestResults = os.path.join(pathToSaveTestResults_testParameter,((str(int(new_ThDepth)).zfill(4)) +"_"+ (str(new_ORBextractor_nFeatures).zfill(4))).replace('.', '_'))

                    # pathToSaveTestResults = create_incremented_folder(pathToSaveTestResults_testParameter, folder_name_suffix=((str(int(new_ThDepth)).zfill(4)) +"_"+ (str(new_ORBextractor_nFeatures).zfill(4))).replace('.', '_'))

                    # # os.makedirs(pathToSaveTestResults, exist_ok=True)
                    # print("running orb slam")
                    # customTime = 200 if dataset == 1 else 110 if dataset == 2 else 30 if dataset == 3 else 90
                    # print("$$#$ TIME TO WAIT IS ",customTime, )
                    # Run_ORBSlam_and_Dataset(filtered_files[0], pathToSaveTestResults,customTime=customTime)
                    # # time.sleep(3)
                    pathToSaveTestResults_testParameter = os.path.join(pathToSaveTestResults, TestResultslist[dataset_index])
                    # full_path, relative_path = find_files(parameters['ROOT_DIR'], "FrameTrajectory_TUM_Format.txt", parameters['STEREO_FOLDER_NAME'],parameters['test_parameter'])
                    evaluationParameters =Update_Global_Variables("parseResultsParameters.txt")
                    _ , resultInstance_Index = os.path.split(pathToSaveTestResults)
                    subfolder_path, subfolder = os.path.split(pathToSaveTestResults_testParameter)
                    subfolder_path = (os.path.join(subfolder_path, subfolder))
                    # print(subfolder)
                    # print(subfolder_path)
                    # print(pathToSaveTestResults)
                    # print(pathToSaveTestResults_testParameter)
                    # print(resultInstance_Index,"\n", subfolder,"\n" ,subfolder_path,"\n", os.getcwd())
                    if "FrameTrajectory_TUM_Format.txt" in sorted(os.listdir(pathToSaveTestResults_testParameter)):
                        eval_command = ParseResults_SubSubfolder(subfolder, sorted(os.listdir(subfolder_path)),
                                                subfolder_path, 
                                                dataset_ground_truth_folder=evaluationParameters['dataset_ground_truth_folder'], 
                                                Stereo_Folder_Name=resultInstance_Index, 
                                                # Stereo_Folder_Name=None, 
                                                external_server_evaluation=True,
                                                Ground_Truth_File_Name=groundTruthFileName,
                                                RPE_not_APE=True)
                        # print(eval_command)
                    # break
                    # eval_command = "evo_ape tum /Datasets/optimization/GA/Daytime_Normal_GroundTruth_Transformed_clean.tum /Datasets/optimization/GA/GAtests/22_2params_baseline_ORBextractor_nFeatures/01_0095_0600/FrameTrajectory_TUM_Format.txt --align --save_results /Datasets/optimization/GA/GAtests/22_2params_baseline_ORBextractor_nFeatures/01_0095_0600/22_2params_baseline_ORBextractor_nFeatures_01_0095_0600_ALIGN_results.zip"
                    # rospy.wait_for_service('evaluate_SLAM_Evo')
                    # try:
                    #     evaluate_SLAM_Evo = rospy.ServiceProxy('evaluate_SLAM_Evo', evaluateSLAMEvo)
                    #     resp1 = evaluate_SLAM_Evo(eval_command)
                    # except rospy.ServiceException as e:
                    #     print("Service call failed: %s"%e)    
                    sender.send(eval_command)
                    receiver.spin()
                    print("#####", " Time of Day: ",time_of_day," Weather Condition: ",weather_condition," Dataset: ", dataset, " Test: " ,test, " RMSE:",received_rmse)
                    rowDatasetResults.append(received_rmse) 
                    dataset_index+=1  
                # break
            print("=== Summary: ", "TestCase ", testCaseIndex ," :" ,rowDatasetResults)
            rowDatasetResults = []

    # NOTE: When you run this code in a Python 2 environment, you might need to adjust the CSV file path.


    # print(python2_code)
