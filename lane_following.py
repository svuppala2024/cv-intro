import numpy as np
import lane_detection

def get_lane_center(lanes):
    i = 0
    avgslopes = []
    avgxints = []
    while i < len(lanes):
        slopes, xInts = lane_detection.get_slopes_intercepts(lanes[i])
        avgslopes.append(1/((1/slopes[0] + 1/slopes[1])/2))
        avgxints.append((xInts[0] + xInts[1])/2)
    index = 0
    for i in range(len(avgxints) - 1):
        if abs(avgxints[i] - 1920) <= abs(avgxints[i + 1] - 1920):
            index = i
        else:
            index = i + 1
    return avgxints[index], avgslopes[index]

def recommend_direction(center, slope):
    translational = ''
    rotational = ''
    if center < 1900:
        translational = 'stafe right'
    elif center > 1940:
        translational = 'strafe left'
    else:
        translational = 'forward'
    if abs(slope) > 30:
        rotational = 'don\'t turn'
    elif slope >= 0:
        rotational = 'turn right'
    else:
        rotational = 'turn left'

    return translational + ' and ' + rotational

