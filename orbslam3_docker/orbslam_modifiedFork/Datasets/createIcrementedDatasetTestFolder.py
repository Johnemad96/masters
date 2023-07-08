#!/usr/bin/env python3
import os

def get_starting_number(s):
    first_part = s.split('_')[0]
    return (first_part) if first_part.isdigit() else None

def create_incremented_folder(path,folder_name_suffix=None):
    # Get a list of all directories in the path
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    
    # Sort the directories
    dirs.sort()
    
    # If there are no directories yet, start with '01'
    if not dirs:
        new_dir = '01'
    else:
        # Get the last directory in the list
        last_dir = dirs[-1]
        last_dir = get_starting_number(last_dir)
        # Increment the last directory number by 1
        new_dir_num = int(last_dir) + 1
        
        # Format the new directory number with leading zeros
        new_dir = str(new_dir_num).zfill(2)
    if folder_name_suffix != None:
        new_dir = new_dir + "_" + folder_name_suffix

    # Create the new directory
    new_dir_path = os.path.join(path, new_dir)
    os.makedirs(new_dir_path, exist_ok=True)
    
    return new_dir_path

if __name__ == "__main__":

    # Use the function
    new_dir_path = create_incremented_folder('/path/to/your/folder')
    print('Created new directory:', new_dir_path)
