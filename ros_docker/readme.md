# ROS-Melodic Docker Container
- this is t a readme for the steps, every thing is open source and ther isn't any container I build from scratch.
- the container is made by OSRF (Open Source Robotics Foundation - the guys behind ros) 
- Also note that this contains rviz, it just needs access for the display

# Command used to run
- start with 
```sh
    xhost + 
```
- followed by
```sh
    docker run -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $HOME/.Xauthority:/root/.Xauthority  \
    -v /home/john/masters/orbslam3_docker/orbslam_modifiedFork/Datasets:/home/dataset  \
    -v /home/john/masters/ros_docker/workspace:/home/workspace \
    --privileged \
    --net=host  \
    --name ros_melodic \
    osrf/ros:melodic-desktop-full
```
# Notes
## Sourcing
- 2 "setup.bash" files should be sourced:
    - source /opt/ros/melodic/setup.bash
    - source the workspace "inside catkin_ws", ``` . devel/setup.bash ``` 

## For the previos Commmand
- The previous command also mounted folders for:
(1) the dataset inside the docker container (in /home/datasets), (2) folder for ros workspaces.
Also note that the local folder was mounted inside the container without previously knowing that the folder existed 

## Errors
- to solve the catkin_make error (cmake failed), I followed this [link](https://answers.ros.org/question/244007/invoking-cmake-failed/?answer=258920#post-id-258920). 
- note that this required a ``` apt-get update``` followed by ``` apt-get install python3-pip```