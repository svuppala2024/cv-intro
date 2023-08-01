import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

def detect_lines(img, threshold1 = 50, threshold2 = 150, apertureSize = 3, minLineLength = 100, maxLineGap = 10):
    # blur = cv2.GaussianBlur(img,(5,5),0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    # thresh, bw = cv2.threshold(gray, 145, 160, cv2.THRESH_BINARY)
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize=apertureSize) # detect edges
    lines = cv2.HoughLinesP(
                    edges,
                    1,
                    np.pi/180,
                    100,
                    minLineLength=minLineLength,
                    maxLineGap=maxLineGap,
            ) # detect lines
    return lines

def draw_lines(img, lines, color):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), color, 10)

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
    res = 2160
    slopes, intercepts = get_slopes_intercepts(lines)

    lanes = []
    for i in range(len(slopes)):
        for j in range(i + 1, len(slopes)):
            min_intercept = min(intercepts[i], intercepts[j])
            max_intercept = max(intercepts[i], intercepts[j])
            min_slope = min(slopes[i], slopes[j])
            max_slope = max(slopes[i], slopes[j])
            intercept_ratio = abs(min_intercept / max_intercept)
            slope_ratio = abs(min_slope / max_slope)
            slope_difference = abs(1 / slopes[i] - 1 / slopes[j])

            # print(f"dist1:{abs(intercepts[i]-intercepts[j])}")
            # print(f"slope1:{abs(1/ slopes[i]-1 /slopes[j])}")
            # print(f"dist2:{max_intercept - min_intercept }")
            # print(f"slope2:{slope_difference}")

            if (
                max_intercept - min_intercept > 100
                and max_intercept - min_intercept < 10000
                and slope_difference < 1
            ):
                # m1(x-x1) = m2(x - x2)
                # m1x - m1x1 = m2x - m2x2
                # m1x - m2x = m1x1 - m2x2
                # x = (m1x1 - m2x2) / (m1-m2)
                x = (slopes[i] * intercepts[i] - slopes[j] * intercepts[j]) / (
                    slopes[i] - slopes[j]
                )
                # plug in x into any equation, add resolution to account for cam
                y = slopes[i] * (x - intercepts[i]) + res

                line1 = [intercepts[i], res, x, y]
                line2 = [intercepts[j], res, x, y]
                lanes.append([line1, line2])
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
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        for line in lane:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (r, g, b), 15)
    return img
        
        

