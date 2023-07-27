import math
 
# Define a class to represent a point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
# Function to calculate the
# squared Euclidean distance between two points
def dist(p, q):
    return (p.x - q.x) ** 2 + (p.y - q.y) ** 2
 
# Function to calculate the
# absolute area of a triangle formed by three points
def absArea(p, q, r):
    return abs((p.x * q.y + q.x * r.y + r.x * p.y) -
               (p.y * q.x + q.y * r.x + r.y * p.x))
 
# Function to calculate the
# cross product of two vectors formed by three points
def crossProduct(p, q, r):
    return ((q.x - p.x) * (r.y - p.y)) - ((q.y - p.y) * (r.x - p.x))
 
# Function to calculate the convex hull
# of a list of points using the Graham scan algorithm
def convexHull(points):
   
    # Sort the points lexicographically by their x-coordinates,
    # breaking ties by their y-coordinates
    points.sort(key=lambda p: (p.x, p.y))
 
    hull = []
    n = len(points)
     
    # Traverse the sorted points from left to right
    for i in range(n):
       
        # Remove any point from the hull that makes a
        # clockwise turn with the previous two points on the hull
        while len(hull) >= 2 and crossProduct(hull[-2], hull[-1], points[i]) <= 0:
            hull.pop()
             
        hull.append(points[i])
 
    # Traverse the sorted points from right to left
    for i in range(n - 2, -1, -1):
       
        # Remove any point from the hull that makes a
        # clockwise turn with the previous two points on the hull
        while len(hull) >= 2 and crossProduct(hull[-2], hull[-1], points[i]) <= 0:
            hull.pop()
             
        hull.append(points[i])
 
    # Return the hull, omitting the last point, which is the same as the first point
    return hull[:-1]
 
def rotatingCaliper(points):
   
    # Takes O(n)
    convex_hull_points = convexHull(points)
    n = len(convex_hull_points)
 
    # Convex hull point in counter-clockwise order
    hull = []
    for i in range(n):
        hull.append(convex_hull_points[i])
 
    # Base Cases
    if n == 1:
        return 0
    if n == 2:
        return math.sqrt(dist(hull[0], hull[1]))
    k = 1
 
    # Find the farthest vertex
    # from hull[0] and hull[n-1]
    while crossProduct(hull[n - 1], hull[0], hull[(k + 1) % n]) > crossProduct(hull[n - 1], hull[0], hull[k]):
        k += 1
 
    res = 0
 
    # Check points from 0 to k
    for i in range(k + 1):
        j = (i + 1) % n
        while crossProduct(hull[i], hull[(i + 1) % n], hull[(j + 1) % n]) > crossProduct(hull[i], hull[(i + 1) % n], hull[j]):
            # Update res
            res = max(res, math.sqrt(dist(hull[i], hull[(j + 1) % n])))
            j = (j + 1) % n
 
    # Return the result distance
    return res
 