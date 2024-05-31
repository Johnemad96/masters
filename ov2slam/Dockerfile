# Use Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Set working directory
WORKDIR /root

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    cmake \
    build-essential \
    libeigen3-dev \
    libopencv-dev \
    ros-melodic-desktop-full \
    && rm -rf /var/lib/apt/lists/*

# Setup ROS environment
RUN rosdep init \
    && rosdep update \
    && echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc

# Clone OV2SLAM repository
RUN cd ~/catkin_ws/src/ \
    && git clone https://github.com/ov2slam/ov2slam.git \
    && cd ov2slam \
    && chmod +x build_thirdparty.sh \
    && ./build_thirdparty.sh

# Build OV2SLAM
RUN /bin/bash -c '. /opt/ros/melodic/setup.bash; cd ~/catkin_ws; catkin_make --pkg ov2slam'

# Set the default command for the container
CMD ["bash"]

