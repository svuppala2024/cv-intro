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
        powerTranslational = [100, -100, 100, -100, 0, 0]
    elif center > 1940:
        translational = 'strafe left'
        powerTranslational = [-100, 100, -100, 100, 0, 0]
    else:
        translational = 'forward'
        powerTranslational = [100, 100, -100, -100, 0, 0]
    if abs(slope) > 10:
        rotational = 'don\'t turn'
        powerRotational = [0, 0, 0, 0, 0, 0]
    elif slope >= 0:
        rotational = 'turn right'
        powerRotational = [100, -100, -100, 100, 0, 0]
    else:
        rotational = 'turn left'
        powerRotational = [-100, 100, 100, -100, 0, 0]
    thrusterPower = np.divide(np.add(np.array(powerTranslational), np.array(powerRotational)), 2)
    return translational + ' and ' + rotational, thrusterPower 

