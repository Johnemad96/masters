# ORBSLAM3 Docker

This dockerfile creates an image of orbslam3 (v1) with all its dependencies. The full credit for this image goes to (https://github.com/LMWafer/orb-slam-3-ready). I just added a folder to mount Datasets folder (locally).

## command 
sudo xhost +local:root && docker run --privileged --name orb-3-v1 -it --net=host -e DISPLAY=$DISPLAY -e QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev:/dev:ro -v /home/john/masters/orbslam3_docker/orbslam_modifiedFork/Datasets:/dpds/Datasets --gpus all -it orbslam3v1docker:latest