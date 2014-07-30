Plane Geometry
========

Basic Geometric Classes for Python 2.7

Package includes:
Simple Polygon Class
Triangulation Class
General Line Intersection Class
Vector Class


Simple Polygon Class:

Initiate a simple polygon represented by a doubly linked list by a list of tuples.
Polygon can be initiatated in either clockwise or counterclockwise orientation.
Retains copy of original list of tuples for search/add/remove functions.

Currently available functions for Polygon:

initDataCW / initDataCCW
clone
search (vertex)
remove (vertex)
countVertices
getBorder - returns list of line segments [[(x1,y1),(x2,y2)]] representing polygon border.
getSignedAreaTotal
getAreaTotal
getCentroid
scale - returns new polygon
rotate - returns new polygon
translate - returns new polygon
checkConvex (vertex)
isConvex
isSimple (uses General Line Intersection Class)

There is still a need to implement add vertex/move vertex.  These will require isSimple to work.


Triangulation Class:

Acts as a subclass of Polygon (Need to implement it like this, but I am still learning!)
Initiated by a list of tuples, creates a Polygon using this list.
After triangulation, polygon has been reduced to a triangle and is unable to be used as it was.

There is a need to avoid reducing the polygon, and a method for building the original polygon
using triangles.

Currently available functions for Triangulate:

getTriangle - returns triplet of coordinates with the argument vertex as the 'ear-tip'.
getTriangleNormals
getBarycentricCoordinate
checkPointIn (triangle)
checkPointOn (triangle)
findEar
triangulate - returns list of triangle triplets while reducing initial polygon to a single triangle.


General Line Intersection Class:

Initiates with a list of line segments [[(x1,y1),(x2,y2)]], breaking them down into lists of
endpoint and label [(x1,y1), 'n'] using a dictionary to keep track of them.
This class uses a sweep-line method to determine whether any of the line segments intersect
with eachother.  In the future finding specific intersections may be desired, but for now it is
boolean.

Currently available functions for LineIntersection:

addLine
addLines
sortSweeps
intersectTwo (lines)
checkIntersection (all lines in class)


Vector Class:

Initiates with a n-tuple, Vector provides some basic tools for working with Euclidean vectors.
There is a need to specify to what accuracy some of these calculations make, so that false
positives do not occur.

Currently available functions for Vector:

dimension
dotProduct
crossProduct (3-dimensional)
tripleProduct (3-dimensional)
project
normalize
getAngle
orthogonal
collinear
sum
scale
difference
negate
magnitude


Any questions or comments do not hesitate to e-mail me at jonathan.melcher@gmail.com.
I am a novice programmer learning the trade and would appreciate any advice or criticism.