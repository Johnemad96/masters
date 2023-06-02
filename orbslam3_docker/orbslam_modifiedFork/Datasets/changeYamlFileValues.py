#!/usr/bin/env python3
# Open the YAML file and read its lines into a list

# update Baseline
new_ThDepth = 35

# update number of orb features extracted per frame
new_ORBextractor_nFeatures = 1200


with open('file.yaml', 'r') as file:
    lines = file.readlines()

# Loop over the lines in the file
for i, line in enumerate(lines):
    # If this line contains the key you want to change, replace it
    if ('ThDepth:' in line) and ('new_ThDepth' in globals()):
        # Split the line into a list of words
        words = line.split()
        # Change the value of the key
        words[1] = str(new_ThDepth) #'new_value_for_ThDepth'
        # Join the words back into a line and add it back to the list of lines
        lines[i] = ' '.join(words) + '\n'
        continue
    if ('ORBextractor.nFeatures:' in line) and ('new_ORBextractor_nFeatures' in globals()):
        words = line.split()
        words[1] = str(new_ORBextractor_nFeatures) #'new_value_for_ORBextractor.nFeatures'
        lines[i] = ' '.join(words) + '\n'
        continue

# Write the lines back to the YAML file
with open('file.yaml', 'w') as file:
    file.writelines(lines)
