import subprocess
import time
import signal
import os

root_dir = "/Datasets/carlaDatasets"
def Transform_GT(datasetName):
    # note that for this script (tf2_gt_broadcast.py), datasetname and directory is the same
    orbslam_process = subprocess.Popen(["rosrun", "learning_tf2" ,"tf2_gt_broadcast.py", datasetName])

if __name__ == "__main__":
    pathToSaveTestResults = "/Datasets/carlaDatasets/"
