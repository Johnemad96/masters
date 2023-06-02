# Use ROS Melodic as the base image
FROM ros:melodic

# Set the environment variable to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Update the system and install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libgtk2.0-dev \
    pkg-config \
    python-dev \
    python-numpy \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libdc1394-22-dev \
    libatlas-base-dev \
    libboost-all-dev \
    libgflags-dev \
    libgoogle-glog-dev \
    libhdf5-serial-dev \
    libleveldb-dev \
    liblmdb-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libsnappy-dev \
    libblas-dev \
    liblapack-dev \
    python3-pip \
    python3-pytest \
    python3-setuptools \
    python3-dev \
    python3-numpy \
    python3-opencv \
    python3-protobuf \
    python3-h5py \
    python3-networkx \
    python3-nose \
    python3-lxml \
    python3-scipy \
    python3-matplotlib \
    python3-coverage \
    python3-sphinx \
    python3-seaborn \
    python3-pandas \
    python3-sphinx-rtd-theme \
    python3-yaml \
    python3-docutils \
    wget \
    unzip \
    vim \
    curl

# Download and install Eigen 3.1.0
# WORKDIR /
# RUN wget http://bitbucket.org/eigen/eigen/get/3.1.0.tar.gz
# RUN tar -xzvf 3.1.0.tar.gz
# WORKDIR /eigen-eigen-b3f3d4950030
# RUN mkdir build
# WORKDIR /eigen-eigen-b3f3d4950030/build
# RUN cmake ..
# RUN make install

# Install Eigen from the package manager
RUN apt-get install -y libeigen3-dev

# # Download and install OpenCV 3.2.0
# WORKDIR /
# RUN wget https://github.com/opencv/opencv/archive/3.2.0.zip
# RUN unzip 3.2.0.zip
# WORKDIR /opencv-3.2.0
# RUN mkdir build
# WORKDIR /opencv-3.2.0/build
# RUN cmake ..
# RUN make install

# Install OpenCV 4.4.0
WORKDIR /
RUN wget https://github.com/opencv/opencv/archive/4.4.0.zip \
    && unzip 4.4.0.zip \
    && mkdir /opencv-4.4.0/cmake_binary \
    && cd /opencv-4.4.0/cmake_binary \
    && cmake .. \
    && make install \
    && rm /4.4.0.zip

# Install OpenGL
RUN apt-get install -y libgl1-mesa-dev

# Install GLEW
RUN apt-get install -y libglew-dev

# Install additional Pangolin dependencies
RUN apt-get install -y libavcodec-dev libavformat-dev libavutil-dev libswscale-dev \
    libjpeg-dev libpng-dev libtiff-dev libopenexr-dev doxygen libuvc-dev

# Install Pangolin
WORKDIR /
RUN git clone https://github.com/stevenlovegrove/Pangolin.git
WORKDIR /Pangolin
RUN mkdir build
WORKDIR /Pangolin/build
RUN cmake ..
RUN make -j$(nproc)
RUN make install


# Initialize rosdep
# RUN rosdep init
RUN rosdep update

# Clone the ORB-SLAM3 repository
WORKDIR /
RUN git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git ORB_SLAM3 

# Check the contents of the ORB_SLAM3 directory
# RUN ls /ORB_SLAM3

# Build the Thirdparty libraries and ORB-SLAM3
WORKDIR /ORB_SLAM3
RUN chmod +x build.sh
RUN ./build.sh

# Build the ROS nodes
RUN chmod +x build_ros.sh
RUN ./build_ros.sh

