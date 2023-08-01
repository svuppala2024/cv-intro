import numpy as np
import lane_detection
import cv2

def get_lane_center(lanes, width):
    i = 0
    avgslopes = []
    avgxints = []
    while i < len(lanes):
        print(lanes[i])
        slopes, xInts = lane_detection.get_slopes_intercepts(lanes[i])
        avgslopes.append(1/((1/slopes[0] + 1/slopes[1])/2))
        avgxints.append((xInts[0] + xInts[1])/2)
    index = 0
    i = 1
    print(f'{len(avgxints)} {len(avgslopes)}')
    if len(avgxints) > 1:
        while i < len(avgxints):
            if abs(avgxints[index] - width/2) > abs(avgxints[i] - width/2):
                index = i
            i += 1

    return avgxints[index], avgslopes[index]

def draw_lane_center(img, xInt, slope, height):
    b = -1 * slope * xInt
    x2 = (height - b) / slope
    cv2.line(img, (xInt, 0), (x2, height), (0, 255, 0))
    return img

def recommend_direction(center, slope, width):
    translational = ''
    rotational = ''
    if center > width * 0.53:
        translational = 'stafe right'
        powerTranslational = [100, -100, 100, -100, 0, 0]
    elif center < width * 0.47:
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

