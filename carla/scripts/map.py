
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
mapName = "Town04"
waypointDistance = 6
client = carla.Client('127.0.0.1', 2000)
world = client.load_world(mapName)
world = client.get_world()
settings = world.get_settings()
town_map = world.get_map()
# waypoints = world.get_map().generate_waypoints(2.0)  # get_waypoint()

## save map in *.xodr extension
# world.get_map().save_to_disk("waypoints_"+mapName)
x = []
y = []
waypoints = world.get_map().generate_waypoints(waypointDistance)  # get_waypoint()

fig = plt.figure(figsize=(100, 75))  # (figsize=(100, 75))
# plt.scatter([w.transform.location.x for w in waypoints] ,[w.transform.location.y for w in waypoints],c = 'c',marker = 's')
waypoints_index = 0
previous_road_id = -1
for w in waypoints:  # spawn_points:
#     # print((w))
#     # printing road id
#     # print(w.road_id , w.transform.location.x , w.transform.location.y)
    # if previous_road_id != w.road_id:
    #     previous_road_id = w.road_id
    #     # print(w.road_id)
    plt.scatter(w.transform.location.x, w.transform.location.y,c = 'c',marker = 'o')

#     # appending waypoints to x and y variables for further plotting, replaced later with one-liner
    x.append(w.transform.location.x)
    y.append(w.transform.location.y)

#     # plot on carla itself
#     # world.debug.draw_string(w.transform.location, '-', draw_shadow=True,color=carla.Color(r=255, g=0, b=0), life_time=120.0,persistent_lines=True)

#     # add points to plot
    # plt.annotate(("(" + str("{:.2f}".format(w.transform.location.x)) + ", " + str("{:.2f}".format(w.transform.location.y)) + ")" ),(w.transform.location.x + 0.5, w.transform.location.y +1))

#     # add waypoint index to plot
    plt.annotate(str(waypoints_index),(w.transform.location.x + 0.5, w.transform.location.y +0.5))
    waypoints_index = waypoints_index + 1
# _ = [plt.scatter(w.transform.location.x, w.transform.location.y, c='c', marker='o') and
#      plt.annotate(str(i), (w.transform.location.x + 0.5, w.transform.location.y + 0.5))
#      for i, w in enumerate(waypoints)]
# plt.annotate(str(waypoints_index),(w.transform.location.x + 0.5, w.transform.location.y +0.5))

plt.savefig("waypoints_"+str(waypointDistance)+"_meters_"+mapName+"_.png")
