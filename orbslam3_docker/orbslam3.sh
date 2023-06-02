#   this needs to be run before ORB-Slam docker container
#   gives priviliges to docker to open GUI
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
xhost +local:docker

# docker start orbslam3_modifiedFork
# docker start ros_melodic_host

# gnome-terminal -x docker exec -it ros_melodic_host bash -i -c "source /opt/ros/melodic/setup.bash && /bin/bash"
# gnome-terminal -x docker exec -it orbslam3_modifiedFork bash -i -c "export ROS_PACKAGE_PATH=/opt/ros/melodic/share:/ORB_SLAM3/Examples/ROS && /bin/bash"
# gnome-terminal -x docker exec -it orbslam3_modifiedFork bash -i -c "export ROS_PACKAGE_PATH=/opt/ros/melodic/share:/ORB_SLAM3/Examples/ROS && /bin/bash"

# gnome-terminal -x docker exec -it ros_melodic_host bash -i -c "source /opt/ros/melodic/setup.bash && /bin/bash"
# gnome-terminal --tab -e 'docker exec -it orbslam3 bash -i -c "export ROS_PACKAGE_PATH=/opt/ros/melodic/share:/ORB_SLAM3/Examples/ROS && /bin/bash"'\
# --tab -e 'docker exec -it orbslam3 bash -i -c "export ROS_PACKAGE_PATH=/opt/ros/melodic/share:/ORB_SLAM3/Examples/ROS && /bin/bash"'
