# Set the root directory
root_dir="/home/john/masters/orbslam3_docker/orbslam_modifiedFork/Datasets/carlaDatasets"
cd ${root_dir}
pwd
# parameterToTest="baseline"
# parameterToTest="ORBextractor_nFeatures"
parameterToTest="baseline_ORBextractor_nFeatures"
subdirectory="testParametersEffect/stereo/${parameterToTest}/01"
test_index=$(basename "$subdirectory")

# target_dir="${root_dir}${subdirectory}"
target_dir=${subdirectory}

# WEATHER_CONDITION="Daytime_Rain&Fog"
WEATHER_CONDITION="Daytime_Normal"

ALIGN_SCALE="Align"
USE_FILENAMES="--use_filenames"
PLOT="-p"
SAVE_PLOT="--save_plot"
PLOT_PATH_PNG_NAME="justForPlotingZIPResults/${WEATHER_CONDITION}/${test_index}/${ALIGN_SCALE}/${parameterToTest}_plot"
PLOT_PNG_EXTENSION=".png"
PLOT_PATH="${root_dir}/$(dirname "$PLOT_PATH_PNG_NAME")"


if [ ! -d ${PLOT_PATH} ]; then
  mkdir -p ${PLOT_PATH}
fi

# Set the target file extension
target_extension=".zip"

# Initialize an empty string to store the paths of the target files
target_files=""

# # Use a for loop to iterate over all the .zip files in the subdirectories of the root directory
# for file in $(find $target_dir -type f -name "*$target_extension" | sort); do
#     # Add the file path to the string
#     target_files+="$file "
# done

# # Now you can use the string of target files in your command
# evo_res $target_files $USE_FILENAMES $PLOT $SAVE_PLOT $PLOT_PATH_PNG_NAME

# Assume that 'files' is an array of file paths
files=($(find $target_dir -type f -name "*$target_extension" | sort))

# Get the total number of files
total_files=${#files[@]}
# echo ${target_dir}
# Set the chunk size
chunk_size=6

loop_counter=1
# Loop over the files array in chunks
for ((i=0; i<$total_files; i+=chunk_size)); do
    # Get the current chunk of files
    chunk_files=("${files[@]:$i:$chunk_size}")
    
    # Convert the chunk of files into a string
    chunk_files_string="${chunk_files[*]}"

    # Execute your command on the current chunk of files

    evo_res $chunk_files_string $USE_FILENAMES $PLOT $SAVE_PLOT $PLOT_PATH_PNG_NAME${loop_counter}
    ((loop_counter++))

done

# if [ ! -d "/path/to/directory" ]; then
#   mkdir -p /path/to/directory
# fi
