#!/usr/bin/env python

import matplotlib
import carla
import math
import time
import random
# import t
import matplotlib.pyplot as plt
import numpy as np
import cv2
from agents.navigation.global_route_planner import GlobalRoutePlanner
from agents.navigation.basic_agent import BasicAgent
import pandas as pd
# from agents.navigation.global_route_planner_dao import GlobalRoutePlannerDAO

showAxis = False

def readPath():
    path = []
    with open('dataset/path.txt', 'r') as f:
        for line in f:
            if line.startswith('Path:') or line.startswith('\\') :
                continue
            path.append(int(line.strip(',\n')))
    return path

def savePath(filenameStr,path): #save path to the output folder
    txtfilename = "dataset/"+filenameStr+"/Path.txt"
    with open("Path.txt", "w") as file:
        for element in path:
            file.write(str(element) + "\n")
    file.close()

def destroy_all_actors(world):
    """
    Destroys all actors in the given Carla world.
    """
    actors = world.get_actors()
    for actor in actors:
        actor.destroy()

def draw_axes(world, transform, scale=1,thickness=0.1):
    """
    Draw three lines that represent the three axes of the given transform.
    """
    if showAxis == True:
        red = carla.Color(255, 0, 0)
        green = carla.Color(0, 255, 0)
        blue = carla.Color(0, 0, 255)
        x_axis = transform.rotation.get_forward_vector()
        y_axis = transform.rotation.get_right_vector()
        z_axis = transform.rotation.get_up_vector()
        world.debug.draw_line(transform.location, transform.location + scale * x_axis,thickness, red, life_time=0.03)
        world.debug.draw_line(transform.location, transform.location + scale * y_axis,thickness, green, life_time=0.03)
        world.debug.draw_line(transform.location, transform.location + scale * z_axis,thickness, blue, life_time=0.03)


def get_quaternion_from_euler(roll, pitch, yaw):
    """
    Convert an Euler angle to a quaternion.

    Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.

    Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
    """
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - \
        np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + \
        np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - \
        np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + \
        np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return qx, qy, qz, qw


def fixOrientationRange(x): return (x+360) if x < 0 else x

def Switch_Traffic_Light_ToGreen():

    # Get all traffic lights in the world and set them to green
    traffic_lights = [actor for actor in world.get_actors().filter('traffic.traffic_light')]

    for traffic_light in traffic_lights:
        traffic_light.set_state(carla.TrafficLightState.Green)


filenameStr = "20220827_2"
designedPath = readPath()
actorsList = [] #append every added actor to this in order to destroy later 
client = carla.Client('127.0.0.1', 2000)
# world = client.reload_world()
# print(client.get_available_maps())
print(client.get_available_maps())

# world = client.load_world('Town04')
world = client.get_world()
town_map = world.get_map()
boundingBoxes = carla.BoundingBox()
settings = world.get_settings()
settings.synchronous_mode = True  # Enables synchronous mode
settings.fixed_delta_seconds = 0.01
world.apply_settings(settings)
bp_lib = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

# world.reset_all_traffic_lights()


waypoints = world.get_map().generate_waypoints(2.0)  # get_waypoint()
# world.get_map().save_to_disk("")
waypoints_tulipe_topology = world.get_map().get_topology()
# world.get_map().
# print((spawn_points))
# print(waypoints.transform.location.x)
# plt.ion()
fig = plt.figure()  # (figsize=(100, 75))
# fig = plt.figure(figsize=(100, 75))


grp = GlobalRoutePlanner(town_map, 0.5)

route_waypoints = grp.trace_route(
    waypoints[1018].transform.location, waypoints[684].transform.location)
# print((route_waypoints[0][1]))
# print(waypoints, sep='\n')
# function to extract transform values from the waypoinrinting road id
# print(w.road_id , w.transform.location.x , w.transform.location.y)
# if previous_road_id != w.road_id:
#     previous_road_id = w.road_id
#     print(w.road_id)
#     plt.scatter(w.transform.location.x, w.transform.location.y)
# x.append(w.transform.location.x)ts
# transform_list = extract_transforms(waypoints)
# function to plot the positions in the transforms.
# plt.plot(transform_list)
# x = []
# y = []

matplotlib.use('tkagg')
plt.scatter([w.transform.location.x for w in waypoints], [
            w.transform.location.y for w in waypoints], c='c', marker='o')
plt.show(block=False)
# previous_road_id = -1
waypoints_index = 0
for w in waypoints:  # spawn_points:
    # print((w))
    # printing road id
    # print(w.road_id , w.transform.location.x , w.transform.location.y)
    # if previous_road_id != w.road_id:
    #     previous_road_id = w.road_id
    #     print(w.road_id)
    #     plt.scatter(w.transform.location.x, w.transform.location.y)

    # appending waypoints to x and y variables for further plotting, replaced later with one-liner
    # x.append(w.transform.location.x)
    # y.append(w.transform.location.y)

    # plot on carla itself
    # world.debug.draw_string(w.transform.location, '-', draw_shadow=True,color=carla.Color(r=255, g=0, b=0), life_time=120.0,persistent_lines=True)

    # add points to plot
    # plt.annotate(("(" + str("{:.2f}".format(w.transform.location.x)) + ", " + str("{:.2f}".format(w.transform.location.y)) + ")" ),(w.transform.location.x + 0.5, w.transform.location.y +1))

    # add waypoint index to plot
    # plt.annotate(str(waypoints_index),(w.transform.location.x + 0.5, w.transform.location.y +0.5))
    waypoints_index = waypoints_index + 1

#Plot Map Itself
# plt.scatter([w.transform.location.x for w in waypoints] ,[w.transform.location.y for w in waypoints],c = 'c',marker = 's')
# mapName = INSERT_TOWNNAME_AND_MOVE_IT_TO_THE_TOP
# plt.savefig("waypoints_"+mapName+".png")

# plot spawn points
# plt.scatter([w.location.x for w in spawn_points] ,[w.location.y for w in spawn_points],c = 'r',marker = 'x')
# waypoints_index = 0
# for w in spawn_points:
#     plt.annotate(str(waypoints_index),(w.location.x , w.location.y +0.1))
#     waypoints_index = waypoints_index +1
# plt.legend(["waypoint", "spawn points"],loc ="lower right")
# plt.savefig("map01_with_spawn_points.png")
# print([rw.location.x for rw in spawn_points] ,[rw.location.y for rw in spawn_points],[rw.location.z for rw in spawn_points])

# for w in waypoints_tulipe_topology:
#     print(w[0].transform.location.x , w[0].transform.location.y," -> " ,w[1].transform.location.x ,w[1].transform.location.y)
# plt.scatter([w[0].transform.location.x for w in waypoints_tulipe_topology[:2]] ,[w[0].transform.location.y for w in waypoints_tulipe_topology[:2]],c = 'r',marker = '+')
# plt.scatter([w[1].transform.location.x for w in waypoints_tulipe_topology[:2]] ,[w[1].transform.location.y for w in waypoints_tulipe_topology[:2]],c = 'b',marker = 'x')


# plot generated route waypoints
# for w in route_waypoints:
#     world.debug.draw_string(w[0].transform.location, '-', draw_shadow=True,color=carla.Color(r=255, g=0, b=0), life_time=120.0,persistent_lines=True)

# plt.scatter([rw[0].transform.location.x for rw in route_waypoints] ,[rw[0].transform.location.y for rw in route_waypoints],c = 'r',marker = 'p')

# route_waypoints = grp.trace_route(waypoints[684].transform.location, waypoints[2270].transform.location)
# plt.scatter([rw[0].transform.location.x for rw in route_waypoints] ,[rw[0].transform.location.y for rw in route_waypoints],c = 'b',marker = 'p')

# route_waypoints = grp.trace_route(waypoints[2270].transform.location, waypoints[2671].transform.location)
# plt.scatter([rw[0].transform.location.x for rw in route_waypoints] ,[rw[0].transform.location.y for rw in route_waypoints],c = 'g',marker = 'p')

# route_waypoints = grp.trace_route(waypoints[369].transform.location, waypoints[2671].transform.location)
# plt.scatter([rw[0].transform.location.x for rw in route_waypoints] ,[rw[0].transform.location.y for rw in route_waypoints],c = 'm',marker = 'p')

# route_waypoints = grp.trace_route(waypoints[2043].transform.location, waypoints[1018].transform.location)
# plt.scatter([rw[0].transform.location.x for rw in route_waypoints] ,[rw[0].transform.location.y for rw in route_waypoints],c = 'y',marker = 'p')
# plt.savefig("map01_route_generated_waypoints_008.png")

# cv2.imread("map01_2.png")
# cv2.imshow("map01_2.png")
# if cv2.waitKey(0) & 0xFF == ord('q'):
#     cv2.destroyAllWindows()
# plt.plot(1)
# plt.show(block=False)

# spawn at 1018 then autopilot from 1018 to 1492
# spawn_point = waypoints[1018].transform
# loop
# spawn_point = waypoints[2795].transform
# spawn_point = waypoints[1621].transform
savePath(filenameStr,designedPath)
spawn_point = waypoints[designedPath.pop(0)].transform
# spawn_point = waypoints[1179].transform
# spawn_point = waypoints[1383].transform
# spawn_point = waypoints[1609].transform # testing acceleration in x axis
spawn_point.location.z += 0.1
vehicle_bp = bp_lib.find('vehicle.tesla.model3')
print(vehicle_bp)
# waypoints[1018].transform)
vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)

actorsList.append(vehicle)
vehicle.set_light_state(carla.VehicleLightState.HighBeam)

spectator = world.get_spectator()
transform = carla.Transform(vehicle.get_transform().transform(
    carla.Location(x=-6, z=1.5)), vehicle.get_transform().rotation)
spectator.set_transform(transform)

# adding traffic manager to ignore traffic lights

# Spawn Sensors
# Camera
camera_bp = bp_lib.find('sensor.camera.rgb')
camera_bp.set_attribute('sensor_tick', '0.05')
camera_bp.set_attribute('image_size_x', '752')
camera_bp.set_attribute('image_size_y', '480')
camera_bp.set_attribute('fov', '82')
camera_init_trans_left = carla.Transform(carla.Location(z=1.7, y=-0.27, x=0.5))
camera_init_trans_right = carla.Transform(carla.Location(z=1.7, y=0.27, x=0.5))
camera_left = world.spawn_actor(
    camera_bp, camera_init_trans_left, attach_to=vehicle)
camera_right = world.spawn_actor(
    camera_bp, camera_init_trans_right, attach_to=vehicle)
actorsList.append([camera_left, camera_right])

def camera_callback(image, data_dic, left=True):
    # if left == true, hence left camera, else right
    if left == True:
        data_dic['image_left'] = np.reshape(
            np.copy(image.raw_data), (image.height, image.width, 4))
        # image.save_to_disk('/dataset/left/%09d.png' % (int)(image.timestamp*100))
    else:
        data_dic['image_right'] = np.reshape(
            np.copy(image.raw_data), (image.height, image.width, 4))
        # image.save_to_disk('/dataset/right/%09d.png' % (int)(image.timestamp*100))


image_w = camera_bp.get_attribute("image_size_x").as_int()
image_h = camera_bp.get_attribute("image_size_y").as_int()
camera_data = {'image_left': np.zeros(
    (image_h, image_w, 4)), 'image_right': np.zeros((image_h, image_w, 4))}
# camera_left.listen(lambda image: camera_callback(image, camera_data,True))
# camera_right.listen(lambda image: camera_callback(image, camera_data,False))

# cv2.namedWindow('Stereo Camera', cv2.WINDOW_AUTOSIZE)
# stereo_camera_show = np.concatenate((camera_data['image_left'],camera_data['image_right']),axis=1)

# camera_left.listen(lambda image: camera_callback(image, camera_data,left = True))
# camera_right.listen(lambda image: camera_callback(image, camera_data,left = False))

# cv2.imshow('Stereo Camera',stereo_camera_show)
# cv2.waitKey(1)

# camera_left.listen(lambda image: image.save_to_disk('dataset/'+filenameStr+'/left/%09d_%09d.png' % ((int)(image.timestamp*100), image.frame) ))
# camera_right.listen(lambda image: image.save_to_disk('dataset/'+filenameStr+'/right/%09d_%09d.png' % ((int)(image.timestamp*100), image.frame) ))

# imu
imu_bp = bp_lib.find('sensor.other.imu')
imu = world.spawn_actor(imu_bp, carla.Transform(carla.Location(x=0, y=0, z=3.5),carla.Rotation(roll=90, pitch=90, yaw=-90)
), attach_to=vehicle, attachment_type=carla.AttachmentType.Rigid)
imu_gt = world.spawn_actor(imu_bp, carla.Transform(
), attach_to=vehicle, attachment_type=carla.AttachmentType.Rigid)

actorsList.append([imu,imu_gt])

# vehicle.set_simulate_physics(enabled=True)
# imu.set_simulate_physics(enabled= True)


def imu_callback(imu, data_dic):
    data_dic['frame'] = imu.frame
    data_dic['timestamp'] = imu.timestamp
    data_dic['accel'] = imu.accelerometer
    data_dic['gyro'] = imu.gyroscope
    data_dic['compass'] = imu.compass
    data_dic['transform'] = imu.transform


imu_data = {'frame': 0, 'timestamp': 0, 'accel': carla.Vector3D(
), 'gyro': carla.Vector3D(), 'compass': 0, 'transform': carla.Transform()}
imu.listen(lambda imu: imu_callback(imu, imu_data))

imu_gt_data = {'frame': 0, 'timestamp': 0, 'accel': carla.Vector3D(
), 'gyro': carla.Vector3D(), 'compass': 0, 'transform': carla.Transform()}
imu_gt.listen(lambda imu_gt: imu_callback(imu_gt, imu_gt_data))

# traffic_lights = world.get_actors().filter('traffic.traffic_light')

# trafficManager = client.get_trafficmanager(8000) #8000 is the default port
# trafficManager.set_synchronous_mode(True)
# trafficManager.ignore_lights_percentage(vehicle,100)

# trafficManager.ignore_signs_percentage(vehicle,100)
# trafficManager.ignore_lights_percentage(camera_right,100)
# trafficManager.ignore_lights_percentage(camera_left,100)
# trafficManager.ignore_lights_percentage(imu,100)


# trafficManager.ignore_signs_percentage(camera_left,100)
# world.freeze_all_traffic_lights(True)
# display IMU vars on cv2
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontColor = (255, 125, 125)
thickness = 1
lineType = int(2)
world.tick()
ba = BasicAgent(vehicle, target_speed=40)
# ba.set_destination(waypoints[1496].transform.location)
temp_location = vehicle.get_transform().location
prev_location = vehicle.get_transform().location
plt.pause(0.00000000000000001)
time.sleep((3))
# path = [waypoints[684],waypoints[2394],waypoints[2671]]
# loop
#   path = [waypoints[684],waypoints[1412],waypoints[2394],waypoints[2671],waypoints[2815]]
# L-Shape
# path = [waypoints[791],waypoints[1726],waypoints[466]]# path = [waypoints[2418],waypoints[2671]]
# path = [waypoints[1560],waypoints[2410], waypoints[1179], waypoints[2671]]
# path = [waypoints[1982],waypoints[1196],waypoints[2203],waypoints[2425],waypoints[1403],waypoints[2805],waypoints[1621]]
path = []
[path.append(waypoints[designedPath.pop(0)]) for i in range(len(designedPath))]
print(path)
# path = [waypoints[2783]]
# path = [waypoints[684],waypoints[2418],waypoints[2671]]
# path = [waypoints[1653]]

imu_data_list = {'frame': [], 'timestamp': [], 'accel': [],
                 'gyro': [], 'compass': [], 'transform': []}
imu_data_list['frame'] = []
imu_data_list['timestamp'] = []
imu_data_list['accel'] = []
imu_data_list['gyro'] = []
imu_data_list['compass'] = []
imu_data_list['transform'] = []

# ground truth is obtained from the imu actor itself, not the imu Data.
# imu actor is attached to the vehicle actor, without any transformation.
# hence it has the same location
# Timestamp is from IMU data, other data obtained from the actor
groundTruth = {'frame': [], 'timestamp': [], 'transform': [],
               'linear_velocity': [], 'angular_velocity': [], 'acceleration': []}
# client.TrafficLight().freeze(True)
# time.sleep(5)
# worldSnapshot = world.get_snapshot()
# # for actor_snapshot in worldSnapshot: # Get the actor and the snapshot information
# #     actual_actor = world.get_actor(actor_snapshot.id)
# #     print(actor_snapshot)
# # worldSnapshot.find(imu.id)
debug = world.debug
# world_snapshot = world.get_snapshot()
# print(worldSnapshot.timestamp,worldSnapshot.find(imu.id).get_velocity())
print("vehicle: ", vehicle, "imu: ", imu)
# print(type(vehicle))
# imu.parent(world.get_snapshot().find(vehicle.id))
# print(vehicle.parent(world.get_actor(vehicle.id)))
arrow_size = 1.0
arrow_duration = 0.1
# debug = world.debug
Switch_Traffic_Light_ToGreen()
for p in path:
    ba.set_destination(p.transform.location,)
    # world.tick()        debug.draw_box(carla.BoundingBox(temp_vehicleActor.get_transform().location,carla.Vector3D(4,1,2)),temp_vehicleActor.get_transform().rotation, 0.05 ,carla.Color(255,0,0,1),0.1)

    while True:
        if round(math.sqrt(vehicle.get_velocity().x**2 + vehicle.get_velocity().y**2)) *3.6 < 20 : # resultant speed vector in xy plane in km/h
            Switch_Traffic_Light_ToGreen()
            print("GREEN LIGHT")
        # debug.draw_arrow(imu.get_transform().location, imu.get_transform().location + arrow_size * imu.get_transform().rotation.get_forward_vector(), arrow_size, (0, 0, 255), arrow_duration)
        # debug.draw_arrow(imu.get_transform().location, imu.get_transform().location + arrow_size * imu.get_transform().rotation.get_right_vector(), arrow_size, (0, 255, 0), arrow_duration)
        # debug.draw_arrow(imu.get_transform().location, imu.get_transform().location + arrow_size * imu.get_transform().rotation.get_up_vector(), arrow_size, (255, 0, 0), arrow_duration)
        worldSnapshot = world.get_snapshot()
        temp_vehicleActor = worldSnapshot.find(vehicle.id)
        # debug.draw_box(carla.BoundingBox(temp_vehicleActor.get_transform().location,carla.Vector3D(4,1,2)),temp_vehicleActor.get_transform().rotation, 0.05 ,carla.Color(255,0,0,1),0.05)
        temp_imuActor = worldSnapshot.find(imu.id)
        temp_imu_gtActor = worldSnapshot.find(imu_gt.id)
        # debug.draw_box(carla.BoundingBox(temp_imuActor.get_transform().transform(carla.Location(z=2)),carla.Vector3D(1,2,3)),temp_imuActor.get_transform().rotation, 0.05 ,carla.Color(0,0,255,1),0.05)
        # vehicle.get_transform().transform(carla.Location(x=-5, z=2.5))
        # if world.get_actor(vehicle.id).is_at_traffic_light():
        #     traffic_light = world.get_actor(vehicle.id).get_traffic_light()

        #     print(traffic_light)
        #     if traffic_light.get_state() == carla.TrafficLightState.Red:
        #         # world.hud.notification("Traffic light changed! Good to go!")
        #         traffic_light.set_state(carla.TrafficLightState.Green)
        # world.tick()
        # stereo_camera_show = np.concatenate((camera_data['image_left'],camera_data['image_right']),axis=1)
        # cv2.imshow('Stereo Camera',stereo_camera_show)
        if cv2.waitKey(1) == ord('q'):
            break
        if ba.done():
            # ba.set_destination(waypoints[1496].transform.location)
            # print("The target has been reached, searching for another target")
            print("arrived at " + str(p.transform.location))
            break
        # trafficManager.ignore_lights_percentage(vehicle,100)
        vehicle.apply_control(ba.run_step())
        world.tick()
        transform = carla.Transform(vehicle.get_transform().transform(
            carla.Location(x=-5, z=2.5)), vehicle.get_transform().rotation)
        spectator.set_transform(transform)
        # time.sleep(0.1)
        temp_location = vehicle.get_transform().location
        # # plt.plot(vehicle.get_transform().location.x,vehicle.get_transform().location.y,c = 'r',marker = 'p')
        # if np.abs(np.sqrt(temp_location.x**2 + temp_location.y**2) - np.sqrt(prev_location.x**2 + prev_location.y**2)) > 2:
        #     plt.plot(vehicle.get_transform().location.x,vehicle.get_transform().location.y,c = 'r',marker = 'p')
        #     plt.pause(0.00000000000000001)
        #     prev_location = temp_location
        imu_data_list['frame'].append(imu_data['frame'])
        imu_data_list['timestamp'].append(imu_data['timestamp'])
        imu_data_list['accel'].append(imu_data['accel'])
        imu_data_list['gyro'].append(imu_data['gyro'])
        imu_data_list['compass'].append(imu_data['compass'])
        imu_data_list['transform'].append(imu_data['transform'])

        # # ground truth
        # worldSnapshot = world.get_snapshot()
        # temp_vehicleActor = worldSnapshot.find(vehicle.id)
        # temp_imuActor = worldSnapshot.find(imu.id)
        groundTruth['frame'].append(worldSnapshot.frame)
        groundTruth['timestamp'].append(worldSnapshot.timestamp.elapsed_seconds)
        groundTruth['transform'].append(vehicle.get_transform())
        groundTruth['linear_velocity'].append(vehicle.get_velocity())
        groundTruth['angular_velocity'].append(vehicle.get_angular_velocity())
        groundTruth['acceleration'].append(vehicle.get_acceleration())
        # # print(fixOrientationRange(np.round(temp_vehicleActor.get_transform().rotation.roll,decimals =0)),fixOrientationRange(np.round(temp_vehicleActor.get_transform().rotation.pitch,decimals = 0)),fixOrientationRange(temp_vehicleActor.get_transform().rotation.yaw))
        # ground truth
        # groundTruth['frame'].append(imu_gt_data['frame'])
        # groundTruth['timestamp'].append(imu_gt_data['timestamp'])
        # groundTruth['transform'].append(imu_gt_data['transform'])
        # groundTruth['linear_velocity'].append(temp_vehicleActor.get_velocity())
        # groundTruth['angular_velocity'].append(imu_gt_data['gyro'])
        # groundTruth['acceleration'].append(imu_gt_data['accel'])

        # print(vehicle.get_transform().location, imu.get_transform().location,imu_data['transform'].location)

        # LAST USED PRINT ****** # print(vehicle.get_acceleration(),imu_data_list['accel'][-1],imu_gt_data['accel'])
        
        # print(vehicle.get_angular_velocity(),imu_data_list['gyro'][-1]*180/math.pi)
        # print(imu.get_transform().rotation.get_right_vector(),vehicle.get_transform().rotation.get_right_vector())
        # print(vehicle.get_acceleration(),imu.get_acceleration())
        # print(math.sqrt(temp_vehicleActor.get_acceleration().x**2 +temp_vehicleActor.get_acceleration().y**2 + temp_vehicleActor.get_acceleration().z ** 2),
        #       math.sqrt(imu_data_list['accel'][-1].x**2 +imu_data_list['accel'][-1].y**2 + imu_data_list['accel'][-1].z ** 2),
        #       math.sqrt(groundTruth['acceleration'][-1].x**2 +groundTruth['acceleration'][-1].y**2 + groundTruth['acceleration'][-1].z ** 2))
        # print(temp_vehicleActor.get_velocity(),vehicle.get_velocity(),temp_imuActor.get_velocity(),imu.get_velocity())
        # groundTruth['frame'].append(imu.get)
        # time.sleep(0.2)
        # accel = imu_data['accel'] #- carla.Vector3D(x=0,y=0,z=9.81)
        # accel.z -=9.81
        # print(len(imu_data_list['timestamp']))
        # cv2.putText(camera_data['image_left'],"Accelerometer: " + str(np.sqrt(accel.x**2 + accel.y**2 + (accel.z)**2)), (10,70), font, fontScale, fontColor, thickness, lineType)
        # print(imu_data_list['timestamp'][-1])
        draw_axes(world, temp_imuActor.get_transform(), scale=2)
        draw_axes(world, temp_imu_gtActor.get_transform(), scale=2)


plt.savefig('path.png')
print('path saved')
cv2.destroyAllWindows()
# print(imu_data_list['timestamp'][5])

# # # create csv file and log IMU data
# csvfilename = "dataset/"+filenameStr+"/imu_log.csv" #filename.insert(len(filename)-4,"_pynmea2Converted")
# data = pd.DataFrame( columns=['frame', 'timestamp','acc x (m/s^2)','acc y (m/s^2)','acc z (m/s^2)','gyro x (rad/s)','gyro y (rad/s)','gyro z (rad/s)','x (Ground truth)','y (Ground truth)','z (Ground truth)','yaw (Ground Truth)','pitch (Ground Truth)','roll (Ground Truth)'])
# data.to_csv(csvfilename, index=False,header="auto",mode='a')
# csvfile = open(csvfilename, "a")
# # print(imu_data_list['timestamp'])
# # for i in range(imu_data_list['timestamp']):
# i=0
# while i < len(imu_data_list['timestamp']):
#     # print(i)
#     data = pd.DataFrame([[imu_data_list['frame'][i],imu_data_list['timestamp'][i],imu_data_list['accel'][i].x,imu_data_list['accel'][i].y,imu_data_list['accel'][i].z,imu_data_list['gyro'][i].x,imu_data_list['gyro'][i].y,imu_data_list['gyro'][i].z,imu_data_list['transform'][i].location.x,imu_data_list['transform'][i].location.y,imu_data_list['transform'][i].location.z,imu_data_list['transform'][i].rotation.yaw,imu_data_list['transform'][i].rotation.pitch,imu_data_list['transform'][i].rotation.roll ]], columns=['frame', 'timestamp','acc x (m/s^2)','acc y (m/s^2)','acc z (m/s^2)','gyro x (rad/s)','gyro y (rad/s)','gyro z (rad/s)','x (Ground truth)','y (Ground truth)','z (Ground truth)','yaw (Ground Truth)','pitch (Ground Truth)','roll (Ground Truth)'])
#     data.to_csv(csvfilename, index=False,header=False,mode='a')
#     i+=1
# csvfile.close()
# print("IMU data is saved in " + str(csvfilename) + " file with " + str(i) + " samples")

# csvfilename = "dataset/"+filenameStr+"/GroundTruth.csv" #filename.insert(len(filename)-4,"_pynmea2Converted")
# data = pd.DataFrame( columns=['frame', 'timestamp','x','y','z','qw','qx','qy','qz','v_x (m/s)','v_y (m/s)','v_z (m/s)','w_x (rad/s)','w_y (rad/s)','w_z (rad/s)','acc x (m/s^2)','acc y (m/s^2)','acc z (m/s^2)'])
# data.to_csv(csvfilename, index=False,header="auto",mode='a')
# csvfile = open(csvfilename, "a")
# i=0
# while i < len(groundTruth['timestamp']):
#     # print(i)
#     temp_qx, temp_qy, temp_qz, temp_qw = get_quaternion_from_euler(np.radians(groundTruth['transform'][i].rotation.roll),np.radians(groundTruth['transform'][i].rotation.pitch),np.radians(groundTruth['transform'][i].rotation.yaw))
#     data = pd.DataFrame([[groundTruth['frame'][i],(int)((groundTruth['timestamp'][i])*(10**9)),groundTruth['transform'][i].location.x,groundTruth['transform'][i].location.y,groundTruth['transform'][i].location.z, temp_qw,temp_qx, temp_qy, temp_qz,groundTruth['linear_velocity'][i].x,groundTruth['linear_velocity'][i].y,groundTruth['linear_velocity'][i].z,groundTruth['angular_velocity'][i].x ,groundTruth['angular_velocity'][i].y ,groundTruth['angular_velocity'][i].z ,groundTruth['acceleration'][i].x,groundTruth['acceleration'][i].y,groundTruth['acceleration'][i].z ]], columns=['frame', 'timestamp','x','y','z','qw','qx','qy','qz','v_x (m/s)','v_y (m/s)','v_z (m/s)','w_x (rad/s)','w_y (rad/s)','w_z (rad/s)','acc x (m/s^2)','acc y (m/s^2)','acc z (m/s^2)'])
#     data.to_csv(csvfilename, index=False,header=False,mode='a')
#     i+=1
# csvfile.close()
# print("IMU data is saved in " + str(csvfilename) + " file with " + str(i) + " samples")

time.sleep(1)
# destroy_all_actors(world)
[actor.destroy for actor in actorsList]
# actor_list = world.get_actors()
# actor_ids = [actor.id for actor in actor_list]
# destroy_batch = [carla.command.DestroyActor(actor_id) for actor_id in actor_ids]
# world.apply_batch(destroy_batch)