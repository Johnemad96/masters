# Set the root directory
root_dir="/home/john/masters/orbslam3_docker/orbslam_modifiedFork/Datasets/carlaDatasets"
subdirectory="/testParametersEffect/stereo/baseline/01"
test_index=$(basename "$subdirectory")

target_dir="${root_dir}${subdirectory}"

# WEATHER_CONDITION="Daytime_Rain&Fog"
WEATHER_CONDITION="Daytime_Normal"

ALIGN_SCALE="Align"
USE_FILENAMES="--use_filenames"
PLOT="-p"
SAVE_PLOT="--save_plot"
PLOT_PATH_PNG="justForPlotingZIPResults/${WEATHER_CONDITION}/${test_index}/${ALIGN_SCALE}/baseline_plot.png"
PLOT_PATH="${root_dir}/$(dirname "$PLOT_PATH_PNG")"


if [ ! -d ${PLOT_PATH} ]; then
  mkdir -p ${PLOT_PATH}
fi

# Set the target file extension
target_extension=".zip"

# Initialize an empty string to store the paths of the target files
target_files=""

# Use a for loop to iterate over all the .zip files in the subdirectories of the root directory
for file in $(find $target_dir -type f -name "*$target_extension" | sort); do
    # Add the file path to the string
    target_files+="$file "
done

# echo $target_files
# echo $PLOT_PATH

# Now you can use the string of target files in your command
evo_res $target_files $USE_FILENAMES $PLOT $SAVE_PLOT $PLOT_PATH


# if [ ! -d "/path/to/directory" ]; then
#   mkdir -p /path/to/directory
# fi
