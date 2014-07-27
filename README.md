Geometry
========

(Simple) Polygon/Triangulation Classes for Python 2.7

Package includes Polygon Class and Triangulation Class.
Both take lists of tuples as arguments.

Polygon Class:

Able to initiate simple polygon in either CW or CCW orientation.
Retains copy of list for search/remove functions.
There is a need to implement a test for simplicity using line intersections.

Currently available functions in Polygon:

initDataCW / initDataCCW
clone
search (vertex)
remove (vertex)
countVertices
getSlope (vertexA, vertexB)
getBorder - returns list of triples (vertexA, vertexB, slope) for each edge of polygon.
getSignedAreaTotal
getAreaTotal
getCentroid
checkConvex (vertex)
getConvexVertices
isConvexPolygon


Triangulation Class:

Initiates a polygon using a list of tuples.

Currently available functions in Triangulate:

getTriangle - returns triplet of coordinates with the argument vertex as the 'ear-tip'.
getTriangleNormals
getBarycentricCoordinate
checkPointIn (triangle)
checkPointOn (triangle)
findEar
triangulate - returns list of triangle triplets and reduces initiated polygon to a single triangle
