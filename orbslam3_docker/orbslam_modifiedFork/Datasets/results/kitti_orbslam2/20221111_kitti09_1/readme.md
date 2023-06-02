# ORBSLAM2 with Stereo Image Using Kitti-09 dataset
  - using ORB-SLAM2 docker image available as a [Dockerfile on github](https://github.com/open-shade/orbslam2/blob/main) and as a ready docker container {``` $ docker pull shaderobotics/orbslam2-standalone:latest ``` }. Also available with ROS2 intergration {```$ docker pull shaderobotics/orbslam2-ros2:latest ```}.
- Here I used the standalone one. Steps are explained better in the other readme.md {locally -> [here](//home//john//masters//orbslam2_docker//open-shade_orbslam2//readme.md)}

# Evaluation
- for evaluation, EVO tool was used (as described in my [onenote](https://onedrive.live.com/redir?resid=B2D5D77D18775A1C%212596&page=Edit&wd=target%28Masters%2FImplementation.one%7C660241d9-5356-4226-91c2-826e4186f024%2FEVO%20tool%7C85333b87-604a-41d2-880b-16dd6e3df887%2F%29&wdorigin=703))

## Command used
- Evo tool was activated inside its container via 
```sh 
$ conda activate refactoredOrbSlam2 
```
- then inside the results directory (for me it's [here](//home//john//masters//orbslam3_docker//orbslam_modifiedFork//Datasets//results//kitti_orbslam2)), run evo tool using the following command
```sh
$ evo_ape kitti ../../kitti/09/groundtruth/09.txt 20221111_kitti09_1/CameraTrajectory.txt -as --plot
```
- which gave the following result 
```
APE w.r.t. translation part (m)
(with Sim(3) Umeyama alignment)

       max      3.053030
      mean      1.441994
    median      1.363450
       min      0.470290
      rmse      1.537482
       sse      3760.887417
       std      0.533389
```
![alt text](evo_rpe_map.png)
 
![alt text](evo_rpe_raw.png)

