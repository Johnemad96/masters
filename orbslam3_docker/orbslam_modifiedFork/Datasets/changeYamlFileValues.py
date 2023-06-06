#!/usr/bin/env python3
import os
# Open the YAML file and read its lines into a list

# update Baseline
# new_ThDepth = 35

# update number of orb features extracted per frame
# new_ORBextractor_nFeatures = 1200

# directory for yaml file
root_dir_yaml = "/ORB_SLAM3/Examples"

def Change_Yaml_Parameters(new_ThDepth = -1,new_ORBextractor_nFeatures = -1,Sensor_Setup = "Stereo" ):
    path_to_yaml = os.path.join(root_dir_yaml, "Stereo" if Sensor_Setup == "Stereo" else "Stereo-Interial")
    with open(os.path.join(path_to_yaml,'EuRoC.yaml'), 'r') as file:
        lines = file.readlines()

    # Loop over the lines in the file
    for i, line in enumerate(lines):
        # If this line contains the key you want to change, replace it
        if ('ThDepth:' in line) and (new_ThDepth != -1):
            # Split the line into a list of words
            words = line.split()
            # Change the value of the key
            words[1] = str(new_ThDepth) #'new_value_for_ThDepth'
            # Join the words back into a line and add it back to the list of lines
            lines[i] = ' '.join(words) + '\n'
            continue
        if ('ORBextractor.nFeatures:' in line) and (new_ORBextractor_nFeatures != -1):
            words = line.split()
            words[1] = str(new_ORBextractor_nFeatures) #'new_value_for_ORBextractor.nFeatures'
            lines[i] = ' '.join(words) + '\n'
            continue

    # Write the lines back to the YAML file
    with open(os.path.join(path_to_yaml,'EuRoC.yaml'), 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    Change_Yaml_Parameters(new_ThDepth = 35, new_ORBextractor_nFeatures = 1200)
