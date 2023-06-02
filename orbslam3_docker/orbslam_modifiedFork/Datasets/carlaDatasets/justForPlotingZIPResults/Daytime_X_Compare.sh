#!/bin/bash

# Set the directories
# WEATHER_CONDITION="Daytime_Rain&Fog"
WEATHER_CONDITION1="Daytime_Normal"
WEATHER_CONDITION2="Daytime_Rain&Fog"

ALIGN_SCALE="Align"
ALIGN_SCALE_SHORT="" #add _as if needed not just as

# DIR1="Daytime_Normal/AlignScale/25baseline_as_results.zip"
# DIR2="Daytime_Normal/AlignScale/50baseline_as_results.zip"
# DIR3="Daytime_Normal/AlignScale/900ORBFeatures_as_results.zip"
# DIR4="Daytime_Normal/AlignScale/1200ORBFeatures_as_results.zip"
# DIR5="Daytime_Normal/AlignScale/1200ORBFeatures_as_results_2.zip"
# DIR6="Daytime_Normal/AlignScale/1500ORBFeatures_as_results.zip"
DIR1="${WEATHER_CONDITION1}/${ALIGN_SCALE}/1200ORBFeatures${ALIGN_SCALE_SHORT}_results.zip"
DIR1_1="${WEATHER_CONDITION2}/${ALIGN_SCALE}/1200ORBFeatures${ALIGN_SCALE_SHORT}_results.zip"

DIR2="${WEATHER_CONDITION1}/${ALIGN_SCALE}/25baseline${ALIGN_SCALE_SHORT}_results.zip"
DIR2_2="${WEATHER_CONDITION2}/${ALIGN_SCALE}/25baseline${ALIGN_SCALE_SHORT}_results.zip"

DIR3="${WEATHER_CONDITION1}/${ALIGN_SCALE}/50baseline${ALIGN_SCALE_SHORT}_results.zip"
DIR3_3="${WEATHER_CONDITION2}/${ALIGN_SCALE}/50baseline${ALIGN_SCALE_SHORT}_results.zip"

DIR_FOR_COMPARISON="$DIR3 $DIR4 $DIR5 $DIR6"

USE_FILENAMES="--use_filenames"
PLOT="-p"
SAVE_PLOT="--save_plot"
PLOT_PATH="${WEATHER_CONDITION1}/${ALIGN_SCALE}/Compare${WEATHER_CONDITION1}_${WEATHER_CONDITION2}/COMPAREBaseline_plot.png"

# SAVE_TABLE="--save_table"
# TABLE_PATH="${WEATHER_CONDITION}/${ALIGN_SCALE}/Results.csv"

# Run the evo_res command with the directories as parameters
evo_res "$DIR1" "$DIR1_1" "$DIR2" "$DIR2_2" "$DIR3" "$DIR3_3" "$USE_FILENAMES" "$PLOT" "$SAVE_PLOT" "$PLOT_PATH" #"$SAVE_TABLE" "$TABLE_PATH"
# evo_res "${DIR_FOR_COMPARISON}" "$USE_FILENAMES" "$PLOT" "$SAVE_PLOT" "$PLOT_PATH" #"$SAVE_TABLE" "$TABLE_PATH"
