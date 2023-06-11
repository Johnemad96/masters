#!/usr/bin/env python3
import os

def create_incremented_folder(path):
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
        
        # Increment the last directory number by 1
        new_dir_num = int(last_dir) + 1
        
        # Format the new directory number with leading zeros
        new_dir = str(new_dir_num).zfill(2)
    
    # Create the new directory
    new_dir_path = os.path.join(path, new_dir)
    os.makedirs(new_dir_path, exist_ok=True)
    
    return new_dir_path

if __name__ == "__main__":

    # Use the function
    new_dir_path = create_incremented_folder('/path/to/your/folder')
    print('Created new directory:', new_dir_path)
