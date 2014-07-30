""" Geometry Package for Python 2.7
	This file includes:
	Polygon Class
	Triangulation
	Line Intersection
"""
import math




class Node(object):

	def __init__(self, coordinate):

		self.coord = coordinate
		self.next  = None
		self.prev  = None


	def __repr__(self):
		return repr(self.coord)



class GNode(object):

	def __init__(self, value):

		self.value = value
		self.edges = []


	def __repr__(self):
		return repr(self.value)



class Graph(object):

	def __init__(self, nodes, edges, name):

		self.nodes = self.initEdges(nodes, edges)
		self.edges = edges
		self.name = name


	def initEdges(self, nodes, edges):
		
		for edge in edges:
			nodes[edge[0]].edges.append(nodes[edge[1]])
			nodes[edge[1]].edges.append(nodes[edge[0]])
		return nodes


	def __repr__(self):
		return repr(self.name)



class Polygon(object):
	'Polygon Class using doubly linked lists for vertices'

	################
	#Data Properties
	################

	def __init__(self, data, CW_bool):

		self.data    = data
		self.CW 	 = None
		self.vnumber = self.countVertices()
		self.convex  = []
		self.concave = []
		self.lines   = None

		if CW_bool:
			self.head = self.initDataCW(data)
		else:
			self.head = self.initDataCCW(data)


	def clone(self):
		return Polygon(self.data)


	def initDataCW(self, data):

		nodes = [Node(coordinate) for coordinate in data]
		n     = len(nodes)
		for i in xrange(n):
			nodes[i % n].prev = nodes[(i-1) % n]
			nodes[i % n].next = nodes[(i+1) % n]
		self.CW = True
		return nodes[0]


	def initDataCCW(self, data):

		nodes = [Node(coordinate) for coordinate in data]
		n = len(nodes)
		for i in xrange(n):
			nodes[i % n].next = nodes[(i-1) % n]
			nodes[i].prev = nodes[(i+1) % n]
		self.CW = False
		return nodes[0]


	def search(self, coordinate):
		return True if coordinate in self.data else False


	def remove(self, coordinate):

		if not self.search(coordinate):
			raise Exception('Coordinate not in polygon')

		if self.vnumber == 3:
			raise Exception('Simple polygon must have three vertices')

		cursor = self.head
		while cursor.coord != coordinate:
			cursor = cursor.next

		cursor.prev.next = cursor.next
		cursor.next.prev = cursor.prev

		if cursor == self.head:
			self.head = cursor.next

		self.data.remove(coordinate)
		self.vnumber -= 1

	def insertVertex(self, insertpoint, coordinate):

		if not self.search(insertpoint):
			raise Exception('Point not in polygon')

		cursor = self.head
		while cursor.coord != insertpoint:
			cursor = cursor.next

		newpoint 					 = Node(coordinate)
		newpoint.prev, newpoint.next = cursor.prev, cursor
		cursor.prev.next 			 = newpoint
		cursor.prev 	 			 = newpoint
		n = self.data.index(cursor.coord)
		self.data.insert(n, coordinate)
		self.vnumber += 1

		if not self.isSimple():
			self.remove(coordinate)
			raise Exception('Resultant polygon not simple')

		if n == 0:
			self.head = newpoint


	def changeVertex(self, oldcoord, newcoord):

		if not self.search(oldcoord):
			raise Exception('Vertex not in polygon')

		cursor = self.head
		while cursor.coord != oldcoord:
			cursor = cursor.next

		cursor.coord = newcoord
		if not self.isSimple():
			cursor.coord = oldcoord
			raise Exception('Resultant polygon not simple')


	def countVertices(self):
		return len(self.data)

	######################
	#Polygon Line Segments
	######################

	def getEdges(self):
		""" Calculates slopes between each line-segment
			along border in current orientation and
			returns as list of triples.
		"""
		first    	= 	self.head
		second   	= 	first.next
		sentinel 	= 	first
		lines       =	[]
		
		lines.append([first.coord, second.coord])

		first  = second
		second = first.next
		while first != sentinel:
			lines.append([first.coord, second.coord])
			first  = second
			second = first.next
		self.lines = lines
		return lines


	def getLength(self, segment):
		""" Segment taken as [(x1,y1),(x2,y2)]
		"""
		return math.sqrt((segment[1][1]-segment[0][1])**2 + 
						 (segment[1][0]-segment[0][0])**2)


	def getPerimeter(self):

		first = self.head
		second = first.next
		sentinel = first
		lengths = []
		lengths.append(self.getLength([first.coord, second.coord]))

		first = second
		second = first.next
		while first != sentinel:
			lengths.append(self.getLength([first.coord, second.coord]))
			first = second
			second = first.next
		return sum(lengths)


	def isSimple(self):
		""" See Line Intersection Class for details.
		"""
		LI = LineIntersection(self.getEdges())
		return not LI.checkIntersection()

	##############
	#Polygon Areas
	##############

	def getSignedAreaTotal(self):
		""" Calculates total signed area of polygon.
		"""
		first    = self.head
		second   = first.next
		sentinel = first
		area     = self.SAHelper(first, second)

		first  = second
		second = first.next
		while first != sentinel:
			area    += self.SAHelper(first, second)
			first    = second
			second   = first.next
		return 0.5*area


	def getAreaTotal(self):
		return abs(self.getSignedAreaTotal())

	###################
	#Polygon Properties
	###################

	def getCentroid(self):
		""" Calculates centroid of simple polygon.
			CCW or CW orientation doesn't matter.
			Formulae can be found at:
			http://en.wikipedia.org/wiki/Centroid
		"""
		A        = self.getSignedAreaTotal()
		first    = self.head
		second   = first.next
		sentinel = first

		Cx = (1.0*(first.coord[0] + second.coord[0])*
				 self.SAHelper(first, second))
		Cy = (1.0*(first.coord[1] + second.coord[1])*
				 self.SAHelper(first, second))

		first  = second
		second = first.next
		while first != sentinel:
			Cx += (1.0*(first.coord[0] + second.coord[0])*
							  	self.SAHelper(first, second))
			Cy += (1.0*(first.coord[1] + second.coord[1])*
							 	self.SAHelper(first, second))
			first = second
			second = first.next
		return ((1/(6*A))*Cx, (1/(6*A))*Cy)


	def checkConvex(self, vertex):
		""" Checks if angle made by vertex.prev - vertex - vertex.next
			is convex relative to polygon.  Uses sign of triple product
			of vectors which gives orientation.  CCW = +, CW = -.
			If same orientation as cycling then convex, else concave.
			eg. If vertices are cycling clockwise and signed_area is
			negative then returns True.  Signed_area = 0 happens when
			triangle is degenerate.
		"""
		x = vertex.prev.coord
		y = vertex.coord
		z = vertex.next.coord

		signed_area = (x[0]*y[1] + y[0]*z[1] + z[0]*x[1] -
					   y[0]*x[1] - z[0]*y[1] - x[0]*z[1])
		if self.CW:
			return True if signed_area < 0 else False
		else:
			return True if signed_area > 0 else False


	def isConvex(self):

		if not self.convex and not self.concave:
			self.getConvexVertices()
		return True if not self.concave else False


	def rotate(self, degrees):
		""" Creates new Polygon by rotating CCW.
		"""
		centroid = self.getCentroid()
		radians  = math.radians(degrees)
		newpoly  = []
		first    = self.head
		sentinel = first
		
		newpoly.append(self.rotateVertex(first, centroid, radians))
		first = first.next
		while first != sentinel:
			newpoly.append(self.rotateVertex(first, centroid, radians))
			first = first.next
		return Polygon(newpoly, self.CW)


	def translate(self, translation):
		""" Creates new Polygon by translating.
		"""
		newpoly  = []
		first    = self.head
		sentinel = first
		
		newpoly.append(self.translateVertex(first, translation))
		first = first.next
		while first != sentinel:
			newpoly.append(self.translateVertex(first, translation))
			first = first.next
		return Polygon(newpoly, self.CW)


	def scale(self, scale):
		""" Creates new Polygon() by scaling.
		"""
		if scale == 0:
			raise Exception('This would produce a degenerate polygon')

		newpoly  = []
		centroid = self.getCentroid()
		first	 = self.head
		sentinel = first

		newpoly.append(self.scaleVertex(first, centroid, abs(scale)))
		first = first.next
		while first != sentinel:
			newpoly.append(self.scaleVertex(first, centroid, abs(scale)))
			first = first.next
		return Polygon(newpoly, self.CW)

	##############
	#Miscellaneous
	##############

	def scaleVertex(self, vertex, point, scale):
		""" Returns new vertex coordinate by scaling
			from specified point.
		"""
		x = vertex.coord[0] - point[0]
		y = vertex.coord[1] - point[1]
		return (x*scale + point[0], y*scale + point[1])


	def rotateVertex(self, vertex, point, radians):
		""" Returns new vertex coordinate by rotating CCW
			about specified point.
		"""
		x = vertex.coord[0] - point[0]
		y = vertex.coord[1] - point[1]
		rotated_x = math.cos(radians)*x - math.sin(radians)*y
		rotated_y = math.sin(radians)*x + math.cos(radians)*y
		return (rotated_x + point[0], rotated_y + point[1])


	def translateVertex(self, vertex, translation):
		""" Returns new vertex coordinate according to 
			translation vector.
		"""
		moved_x = vertex.coord[0] + translation[0]
		moved_y = vertex.coord[1] + translation[1]
		return (moved_x, moved_y)


	def SAHelper(self, vertexA, vertexB):
		""" Used in centroid/signed area formulae:
			returns + area => CCW cycling
			returns - area => CW cycling
		""" 
		return 1.0*(vertexA.coord[0]*vertexB.coord[1] -
					vertexB.coord[0]*vertexA.coord[1])


	def getCVHelper(self, vertex):
		""" Used in getConvexVertices
		"""
		if self.checkConvex(vertex):
			self.convex.append(vertex.coord)
		else:
			self.concave.append(vertex.coord)


	def getConvexVertices(self):
		""" Used in isConvex
		"""
		self.convex = self.concave = []
		cursor      = self.head
		sentinel    = cursor
		self.getCVHelper(cursor)

		cursor = cursor.next
		while cursor != sentinel:
			self.getCVHelper(cursor)
			cursor = cursor.next


	def __repr__(self):
		return '%s-gon at %s' % (self.vnumber, self.head)




class Triangulate(object):
	""" Triangulate Class for Simple Polygons in
		Polygon Class.
		Note:  Reduces data to triangle so cannot
			   use initial polygon after triangulation.
	"""
	def __init__(self, data):

		self.polygon = Polygon(data, True)
		self.triangulation = []

	#########################
	#Triangulation Properties
	#########################

	def getTriangle(self, vertex):
		""" Returns triangle as triplet of coordinates,
			with vertex as the 'ear-tip'.
		"""
		return [vertex.prev.coord, vertex.coord, vertex.next.coord]


	def getTriangleNormals(self, triangle):
		""" Returns normals of triangle edges. norm([x,y]) = (-y,x)
			Note that these normals are not of length 1.
		"""
		return [(-coord[1], coord[0]) for coord in triangle]


	def getBarycentricCoordinate(self, triangle, point):
		""" http://en.wikipedia.org/wiki/Barycentric_coordinate_system
			if coordinates z_1, z_2, z_3 between 0 and 1 then they are
			inside triangle.  Equal to 1 or 0 and rest in [0,1] means
			on border of triangle.
		"""
		x_1, y_1 = triangle[0][0], triangle[0][1]
		x_2, y_2 = triangle[1][0], triangle[1][1]
		x_3, y_3 = triangle[2][0], triangle[2][1]
		x  , y   = point[0]	     , point[1]

		detT	 = (x_1 - x_3)*(y_2 - y_3) + (x_3 - x_2)*(y_1 - y_3)

		z_1  	 = ((y_2 - y_3)*(x - x_3) + (x_3 - x_2)*(y - y_3)) / detT
		z_2 	 = ((y_3 - y_1)*(x - x_3) + (x_1 - x_3)*(y - y_3)) / detT
		z_3  	 = 1.0 - z_1 - z_2
		return  (z_1, z_2, z_3)


	def checkPointIn(self, triangle, point):
		""" See getBarycentricCoordinate.
		"""
		point_bbc = self.getBarycentricCoordinate(triangle, point)
		for i in point_bbc:
			if i <= 0.0 or i >= 1.0:
				return False
		return True


	def checkPointOn(self, triangle, point):
		""" See getBarycentricCoordinate.
		"""
		point_bbc = self.getBarycentricCoordinate(triangle, point)
		gate = False
		for i in point_bbc:
			if i < 0.0 or i > 1.0:
				return False
			if i == 0 or i == 1:
				gate = True
		return True if gate else False


	def triangulate(self):

		while self.polygon.vnumber > 3:
			ear = self.findEar()
			self.triangulation.append(ear[0])
			self.polygon.remove(ear[1])

		finalear = self.findEar()
		self.triangulation.append(finalear[0])
		return self.triangulation

	##############
	#Miscellaneous
	##############

	def noConcaveIn(self, triangle):
		for vertex_coord in self.polygon.concave:
			if self.checkPointIn(triangle, vertex_coord):
				return False
		return True


	def findEar(self):
		""" Checks triangles where the ear-tip is a convex
			vertex for intersection with any concave vert-
			ices.  If no intersection returns that ear.
		"""
		n = self.polygon.vnumber
		cursor = self.polygon.head

		if n == 3:
			triangle = self.getTriangle(cursor)
			return [triangle, cursor.coord]

		self.polygon.getConvexVertices()

		i = 0
		while i <= n + 2:
			if cursor.coord in self.polygon.convex:
				triangle = self.getTriangle(cursor)
				if self.noConcaveIn(triangle):
					return [triangle, cursor.coord]
			cursor = cursor.next
			i += 1
		raise Exception('Algorithm is bugged, this should not happen.')


	def __repr__(self):
		return 'Triangulation Class for %s' % self.polygon




class LineIntersection(object):
	""" Line Intersection Class. initiates with lines
		[(x1,y1), (x2, y2)] to be converted to labeled
		endpoints [(x,y), label].  Main test for gen.
		line intersection uses sweep-line algorithm.
	"""
	################
	#Data Properties
	################

	def __init__(self, data):

		self.count    = 0
		self.lines    = {}
		self.sweeps   = []
		self.tested   = []
		self.addLines(data)


	def addLine(self, line):
		self.sweeps.append([line[0], str(self.count)])
		self.sweeps.append([line[1], str(self.count)])
		self.lines[str(self.count)] = line
		self.count += 1


	def addLines(self, array):
		for line in array:
			self.addLine(line)


	def sortSweeps(self):
		self.sweeps.sort(key = lambda x: (x[0][0], not x[1]))

	###################
	#Line Intersections
	###################

	def intersectTwo(self, lineA, lineB):
		""" It suffices to check if two points are on
			opposite sides of a line segment.  To do
			this we compute the cross products of
			lineA and the endpoints of lineB and take
			their product.  The product will be negative
			if and only if they intersect.
		"""
		P, Q 	  = lineB[0], lineB[1]
		xproductP = (1.0*(lineA[1][0] - lineA[0][0])*(P[1] - lineA[1][1]) -
					 1.0*(lineA[1][1] - lineA[0][1])*(P[0] - lineA[1][0]))
		xproductQ = (1.0*(lineA[1][0] - lineA[0][0])*(Q[1] - lineA[1][1]) -
					 1.0*(lineA[1][1] - lineA[0][1])*(Q[0] - lineA[1][0]))
		return True if xproductP * xproductQ < 0 else False


	def checkIntersection(self):

		if not self.sweeps:
			return False

		self.sortSweeps()
		self.tested = []
		events 	    = []
		i 			= 0
		while i < len(self.sweeps):
			newvalue = self.sweeps[i][1]

			if not events:
				events.append(newvalue)
			elif newvalue in events:
				events.remove(newvalue)
			else:
				for event in events:
					if (event, newvalue) in self.tested:
						continue
					test = self.intersectTwo(self.lines[event],
										  self.lines[newvalue])
					if test:
						return True
					else:
						self.tested.append((event, newvalue))
			i += 1
		return False

	##############
	#Miscellaneous
	##############

	def __repr__(self):
		return 'Line Intersection Class for lines %s' % self.lines




###########
#Test Cases
###########

X = [(0,0),(0,1),(1,1),(1,0)]
PX = Polygon(X, True)
TX = Triangulate(X)

A = [(0,0),(0,1)]
B = [(0,1),(1,1)]
C = [(1,1),(1,0)]
D = [(1,0),(0,0)]

LI = LineIntersection([A,B,C,D])