import pygame
import time
import os

def get_distance(point1, point2, positive_only=False):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]
    if positive_only:
        return (abs(x), abs(y))
    return (x, y)

def get_delta_time(last_time):
    #possible_delta_time = (time.time() - last_time) * 60
    #if old_delta_time + 0.5 >= possible_delta_time >= old_delta_time - 0.5:
    #    delta_time = old_delta_time
    #else:
    delta_time = (time.time() - last_time) * 60
    new_last_time = time.time()
    return delta_time, new_last_time
