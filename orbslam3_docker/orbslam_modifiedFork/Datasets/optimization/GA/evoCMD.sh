#!/bin/bash

# __conda_setup="$('/home/john/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
# if [ $? -eq 0 ]; then
#     eval "$__conda_setup"
# else
#     if [ -f "/home/john/anaconda3/etc/profile.d/conda.sh" ]; then
#         . "/home/john/anaconda3/etc/profile.d/conda.sh"
#     else
#         export PATH="/home/john/anaconda3/bin:$PATH"
#     fi
# fi
# unset __conda_setup

source ~/anaconda3/bin/activate refactoredOrbSlam2

# conda activate refactoredOrbSlam2

$1