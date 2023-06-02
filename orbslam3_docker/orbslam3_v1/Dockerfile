# make my own orbslam3 docker file by combining the following
#   steps of installing orbslam3 v1 from LMWafer
#   steps prior to those from other file by the same developper
#   ros steps from jahaniam/orbslam3_docker or appliedAI-Initiative/orb_slam_2_ros
#       the latter one I already have locally



# from lmwafer/orb-slam-3-ready:1.1-ubuntu18.04
FROM ros:melodic-robot
USER root

# WORKDIR /dpds
# RUN mkdir Datasets

# CMD /bin/bash

RUN apt-get update

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y gnupg2 curl lsb-core vim wget python-pip libpng16-16 libjpeg-turbo8 libtiff5

# # Installing ROS-melodic
# RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
# RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
# RUN curl -sSL 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xC1CF6E31E6BADE8868B172B4F42ED6FBAB17C654' | apt-key add -
# RUN apt update
# RUN apt install -y ros-melodic-desktop
# RUN apt-get install -y python-rosdep
# RUN rosdep init
# RUN rosdep update
RUN echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
RUN apt install -y python-rosinstall python-rosinstall-generator python-wstool build-essential ros-melodic-tf2-geometry-msgs python-catkin-tools -y

# Intalling python-catkin
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list'
RUN wget http://packages.ros.org/ros.key -O - | sudo apt-key add -
RUN apt-get update
RUN apt-get install -y python-catkin-tools
RUN apt-get install -y software-properties-common

# RUN echo "source /opt/ros/melodic/setup.bash" >> ~/.bash_profile
# RUN apt-get install -y \
#         # Base tools
#         cmake \
#         build-essential \
#         git \
#         unzip \
#         pkg-config \
#         python-dev \
#         # OpenCV dependencies
#         python-numpy \
#         # Pangolin dependencies
#         libgl1-mesa-dev \
#         libglew-dev \
#         libpython2.7-dev \
#         libeigen3-dev \
#         apt-transport-https \
#         ca-certificates\
#         software-properties-common

RUN apt-get update && \
    # Utilitaires
    apt-get install -y \
    git \
    cmake \
    wget \
    tar \
    libx11-dev \
    xorg-dev \
    libssl-dev \
    build-essential \
    libusb-1.0-0-dev \
    libglu1-mesa-dev && \    
    # OpenGL
    apt-get install -qq --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 && \
    rm -rf /var/lib/apt/lists/* 
    # && \
    # # Get folder ready
    # mkdir /app /dpds && \
    # cd dpds && \
    # # Realsense SDK
    # wget --no-check-certificate https://github.com/IntelRealSense/librealsense/archive/refs/tags/v2.50.0.tar.gz && \
    # tar -xzf v2.50.0.tar.gz && \
    # rm v2.50.0.tar.gz && \
    # cd librealsense-2.50.0/ && \
    # mkdir build && cd build && \
    # cmake .. && \
    # make && \
    # make install

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

RUN apt-get update && \
    apt-get -y upgrade && \
    #-> Install general usage dependencies
    echo "Installing general usage dependencies ..." && \
    apt-get install -y apt-file && \
    apt-file update && \
    apt-get install -y nano \
    pkg-config && \
    #-> Install OpenCV dependencies
    #-? From : http://techawarey.com/programming/install-opencv-c-c-in-ubuntu-18-04-lts-step-by-step-guide/
    echo "Installing OpenCV dependencies ..." && \
    apt-get install -y\
    libgtk2.0-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    software-properties-common && \
    #-> Install Pangolin dependencies
    #-? From : https://cdmana.com/2021/02/20210204202321078t.html
    echo "Installing Pangolin dependencies ..." && \
    apt-get install -y \
    libglew-dev \
    libboost-dev \
    libboost-thread-dev \
    libboost-filesystem-dev \
    ffmpeg \
    libavutil-dev \
    libpng-dev && \
    #-> Install Eigen 3 last version
    #-? Needs to be installed BEFORE Pangolin as it also needs Eigen
    #-> Linear algebra library
    echo "Installing Eigen 3 last version ..." && \
    apt-get install -y libeigen3-dev && \
    #-> Install Pangolin last version
    #-? 3D Vizualisation tool
    #-? From : https://cdmana.com/2021/02/20210204202321078t.html
    echo "Installing Pangolin last version ..." && \
    cd /dpds/ && \
    git clone https://github.com/stevenlovegrove/Pangolin.git Pangolin && \
    cd /dpds/Pangolin/ && \
    mkdir build && \
    cd build/ && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -DCPP11_NO_BOOST=1 \
    /dpds/Pangolin/ && \
    make -j4 && \
    make install

    #-[] Install OpenCV last version
    #-? From : http://techawarey.com/programming/install-opencv-c-c-in-ubuntu-18-04-lts-step-by-step-guide/
    #-? Another RUN command in order to free memory
    #-? Usual computer vision library
RUN echo "Installing OpenCV last version ..." && \
    cd /dpds/ && \
    git clone https://github.com/Itseez/opencv.git opencv && \
    git clone https://github.com/Itseez/opencv_contrib.git opencv_contrib && \
    cd opencv/ && \
    mkdir build && \
    cd build/ && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D BUILD_TIFF=ON \
    -D WITH_CUDA=OFF \
    -D ENABLE_AVX=OFF \
    -D WITH_OPENGL=OFF \
    -D WITH_OPENCL=OFF \
    -D WITH_IPP=OFF \
    -D WITH_TBB=ON \
    -D BUILD_TBB=ON \
    -D WITH_EIGEN=ON \
    -D WITH_V4L=OFF \
    -D WITH_VTK=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/dpds/opencv_contrib/modules \
    /dpds/opencv/ && \
    make -j4 && \
    make install && \
    ldconfig
    
    #-[] Get ORB-SLAM 3 installation ready
    #-? From : https://github.com/UZ-SLAMLab/ORB_SLAM3
    #-? Another RUN command in order to free memory
RUN echo "Getting ORB-SLAM 3 installation ready ..." && \
    cd /dpds/ && \
    git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git ORB_SLAM3 && \
    #-! From here, a compilation method is proposed by the repo: "chmod +x build.sh && ./build.sh"
    #-! Such method remove some control over the image build (simultaneous jobs number, directories, OpenCV version etc.) 
    #-! Thus evey step in build.sh has been added here
    #-> Install DBoW2
    #-? Images to bag-of-word library
    echo "Installing 'built-in' DBoW2 ..." && \
    cd /dpds/ORB_SLAM3/ && \
    cd /dpds/ORB_SLAM3/Thirdparty/DBoW2/ && \
    mkdir build && \
    cd build/ && \
    cmake -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_PREFIX_PATH=/usr/lib/x86_64-linux-gnu/ \
    /dpds/ORB_SLAM3/Thirdparty/DBoW2/ && \
    make -j4 && \
    #-> Install g2o
    #-? Graph optimization
    echo "Installing 'built-in' g2o ..." && \
    cd /dpds/ORB_SLAM3/Thirdparty/g2o/ && \
    mkdir build && \
    cd build/ && \
    cmake -D CMAKE_BUILD_TYPE=Release \
    /dpds/ORB_SLAM3/Thirdparty/g2o/ && \
    make -j4 && \
    #-> Install Sophus
    #-? Lie groups library
    echo "Configuring and building Thirdparty/Sophus ..." && \
    cd /dpds/ORB_SLAM3/Thirdparty/Sophus/ && \
    mkdir build && \
    cd build/ && \
    cmake -D CMAKE_BUILD_TYPE=Release \
    /dpds/ORB_SLAM3/Thirdparty/Sophus/ && \
    make -j4 && \
    #-> Uncompress vocabulary
    #-? ORB-SLAM 3 useful data
    echo "Uncompressing vocabulary ..." && \
    cd /dpds/ORB_SLAM3/ && \
    cd Vocabulary && \
    tar -xf ORBvoc.txt.tar.gz
    
    #-> Install ORB-SLAM 3
    #-? Another RUN command in order to free memory
RUN echo "Configuring and building ORB_SLAM3 ..." && \
    cd /dpds/ORB_SLAM3 && \
    mkdir build && \
    cd build/ && \
    cmake -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_PREFIX_PATH=/usr/lib/x86_64-linux-gnu/ \
    /dpds/ORB_SLAM3 && \
    make -j4