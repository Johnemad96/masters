# ORB-SLAM2 docker container (standalone, without ROS)
# Sources
    forked from repo        :   https://github.com/open-shade/orbslam2/blob/main/docker/standalone/Dockerfile
    instruction & info via  :   https://morioh.com/p/05c0b1ec326b
    docker via              :   docker pull shaderobotics/orbslam2-standalone:latest
    pangolin error solution :   https://github.com/stevenlovegrove/Pangolin/issues/194#issuecomment-1061480961

# Command used to run
- start with 
```sh
    xhost + 
```
- followed by
```sh
    docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $HOME/.Xauthority:/root/.Xauthority  \
    -v /home/john/masters/orbslam3_docker/orbslam_modifiedFork/Datasets:/home/dataset  \
    --privileged  \
    --gpus all  \
    -e NVIDIA_DRIVER_CAPABILITIES=all  \
    --net=host  \
    --name orbslam2_standalone \
    shaderobotics/orbslam2-standalone
```
# Notes
## For the previos Commmand
- The previous command also mounted a folder for the dataset inside the docker container (in /home/datasets). Also note that the local folder was mounted inside the container without previously knowing that the folder existed 

- the flag "--rm" deletes the container on exit, remove this to keep it and access later using
```sh
$ docker exec -it <container_name> bash
```

## Personal Note on running kitti 04 using this container
- Inside the containter, at ($pwd /home/datasets/results/kitti_orbslam2) run the following to execute visual slam with result saved in the previous directory
```sh
./../../../../root/ORB_SLAM2/Examples/Stereo/stereo_kitti ../../../../root/ORB_SLAM2/Vocabulary/ORBvoc.txt ../../../../root/ORB_SLAM2/Examples/Stereo/KITTI04-12.yaml ../../kitti/04
```

