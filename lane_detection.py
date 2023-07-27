import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

def detect_lines(img, threshold1 = 50, threshold2 = 150, apertureSize = 3, minLineLength = 100, maxLineGap = 10):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize=apertureSize) # detect edges
    lines = cv2.HoughLinesP(
                    edges,
                    1,
                    np.pi/360,
                    120,
                    minLineLength=minLineLength,
                    maxLineGap=maxLineGap,
            ) # detect lines

    return lines

def draw_lines(img, lines, color):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 10)

    return img

def get_slopes_intercepts(lines):
    yInts = []
    slopes = []
    xInts = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1)/(x2 - x1)
        slopes.append(slope)
        yInt = y1 - slope * x1
        yInts.append(yInt)
        xInts.append(-1 * yInt / slope)
    return slopes, xInts

def detect_lanes(lines):
    slopes, xInts = get_slopes_intercepts(lines)
    i = 0
    lanes = []
    while i < len(lines) - 1:
        dists = {}
        for j in range(1, len(lines) - i):
            dists[j + i] = abs(xInts[i] - xInts[j])
        temp = min(dists.values())
        res = [key for key in dists if dists[key] == temp][0]
        lanes.append([lines[i], lines[res]])
        np.delete(lines, res)
        np.delete(lines, i)
        slopes.pop(res)
        slopes.pop(i)
        xInts.pop(res)
        xInts.pop(i)
        print('pass')
        i += 1
    return lanes

def rmvExcessLines(lines):
    slopes = []
    Y_intercepts = []
    newLines = []

    for i in range(len(lines)):
        x1, y1, x2, y2 = lines[i][0]

        slope = (y2-y1)/(x2-x1)
        slopes.append(slope)

        y_intercept = y1 - (x1*slope)
        Y_intercepts.append(y_intercept)


        y_intercepts = [y for _,y in sorted(zip(slopes,Y_intercepts))]
        slopes.sort()
        closeto = False
        
        for j in range(1, len(slopes)):
            ratio = (slopes[j-1]/slope, (y_intercepts[j-1]/y_intercept))
            if ratio[0] > 0.95 and ratio[1] > 0.95:
                slopes.remove(slope)
                closeto = True
                break
        if not closeto:
            newLines.append(lines[i])
            #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv2.putText(img, str(slope), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), cv2.LINE_4)
            closeto = False
    return  newLines

def draw_lanes(img, lanes):
    for lane in lanes:
        print(lane)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        for line in lane:
            x1, y1, x2, y2 = line[0]
            print((r, g, b))
            cv2.line(img, (x1, y1), (x2, y2), (r, g, b), 15)
    return img
        
        

