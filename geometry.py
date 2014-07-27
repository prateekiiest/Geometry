""" File for Geometry Classes
	Including:
	Polygon
	Triangulation
"""

class Node(object):
	""" Node Class:
		Used to represent vertices of simple polygon using a
		doubly linked list.  Assumptions are that vertices
		are connected cyclically in clockwise rotation.
	"""
	def __init__(self, coordinate):

		self.coord = coordinate
		self.next  = None
		self.prev  = None

	def __repr__(self):
		return repr(self.coord)



class Polygon(object):
	""" Polygon Class:
		Converts list of coordinates into list of nodes given
		assumptions made in node class regarding coordinates.
		--Need to implement method for verifying simple poly.
	"""
	def __init__(self, data):

		self.data    = data
		self.head    = self.initDataCW(data)
		self.vnumber = self.countVertices()
		self.convex  = []
		self.concave = []
		self.CW 	 = None

	def initDataCW(self, data):
		""" Takes list of cartesian coordinates and returns
			doubly linked list of nodes cycling clockwise.
		"""
		nodes = [Node(coordinate) for coordinate in data]
		nodes[0].prev  = nodes[-1]
		nodes[-1].next = nodes[0]

		n = len(nodes)
		for i in xrange(1, n):
			nodes[i].prev = nodes[i-1]
		for i in xrange(0, n-1):
			nodes[i].next = nodes[i+1]
		self.CW = True
		return nodes[0]

	def initDataCCW(self, data):
		""" Takes list of cartesian coordinates and returns
			doubly linked list of nodes cyclic CCW.
		"""
		nodes = [Node(coordinate) for coordinate in data]
		nodes[-1].prev = nodes[0]
		nodes[0].next  = nodes[-1]
		
		n = len(nodes)
		for i in xrange(1, n):
			nodes[i].next = nodes[i-1]
		for i in xrange(0, n-1):
			nodes[i].prev = nodes[i+1]
		self.CW = False
		return nodes[0]

	def search(self, coordinate):
		""" Searches for vertex at coordinate.
		"""
		return True if coordinate in self.data else False

	def remove(self, coordinate):
		""" Removes if possible vertex at coordinate.
		"""
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
		self.vnumber = self.countVertices()

	def countVertices(self):
		return len(self.data)

	def getSlope(self, vertexA, vertexB):
		""" Slope between line-segment vertexA - vertexB
		"""
		try:
			slope = ((vertexB.coord[1]  - vertexA.coord[1])/
					 (vertexB.coord[0]  - vertexA.coord[0]))
		except Exception as e:
			return 'Infinity'
		return (vertexA.coord, vertexB.coord, slope)

	def getBorder(self):
		""" Calculates slopes between each line-segment
			along border in current orientation and
			returns as list of triples.
		"""
		first    	= 	self.head
		second   	= 	first.next
		sentinel 	= 	first
		border   	= 	[self.getSlope(first, second)]

		first  = second
		second = first.next
		while first != sentinel:
			border.append(self.getSlope(first, second))
			first  = second
			second = first.next
		return border

	def SAHelper(self, vertexA, vertexB):
		""" Used in centroid/signed area formulae:
			returns + area => CCW cycling
			returns - area => CW cycling
		""" 
		return 1.0*(vertexA.coord[0]*vertexB.coord[1] -
					vertexB.coord[0]*vertexA.coord[1])

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

	def getCVHelper(self, vertex):
		""" Helper to getConvexVertices
		"""
		if self.checkConvex(vertex):
			self.convex.append(vertex.coord)
		else:
			self.concave.append(vertex.coord)

	def getConvexVertices(self):

		self.convex = self.concave = []
		cursor      = self.head
		sentinel    = cursor
		self.getCVHelper(cursor)

		cursor = cursor.next
		while cursor != sentinel:
			self.getCVHelper(cursor)
			cursor = cursor.next

	def isConvexPolygon(self):

		if not self.convex and not self.concave:
			self.getConvexVertices()
		return True if not self.concave else False

	def clone(self):
		return Polygon(self.data)

	def __repr__(self):
		return '%s-gon at %s' % (self.vnumber, self.head)



class Triangulate(object):
	""" Triangulate Class for Simple Polygons in
		Polygon Class.
		Note:  Reduces data to triangle so should
			   send self.data, not polygon class.
	"""
	def __init__(self, data):

		self.polygon = Polygon(data)
		self.triangulation = []

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
		""" Using definition of Barycentric Coordinate System:
			if coordinates all in (0,1) then inside, else outside
			or on border.
		"""
		point_bbc = self.getBarycentricCoordinate(triangle, point)
		for i in point_bbc:
			if i <= 0.0 or i >= 1.0:
				return False
		return True

	def checkPointOn(self, triangle, point):
		""" Using definition of Barycentric Coordinate System:
			if at least one coordinate is 0 or 1 and the rest
			in [0,1] then point is on border of triangle.
		"""
		point_bbc = self.getBarycentricCoordinate(triangle, point)
		gate = False
		for i in point_bbc:
			if i < 0.0 or i > 1.0:
				return False
			if i == 0 or i == 1:
				gate = True
		return True if gate else False

	def noConcaveIn(self, triangle):
		""" Checks self.polygon.concave for intersecting points.
		"""
		for vertex_coord in self.polygon.concave:
			if self.checkPointIn(triangle, vertex_coord):
				return False
		return True

	def findEar(self):
		""" Resets and populates self.convex/self.concave,
			checks triangles where the ear-tip is a convex
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

	def triangulate(self):
		""" Finds an ear, documents and removes vertice from polygon,
			repeats until only a triangle is left and adds that to
			triangulation.
		"""
		while self.polygon.vnumber > 3:
			ear = self.findEar()
			self.triangulation.append(ear[0])
			self.polygon.remove(ear[1])

		finalear = self.findEar()
		self.triangulation.append(finalear[0])
		return self.triangulation

	def __repr__(self):
		return 'Triangulation Class for %s' % self.polygon



#####################################
#Testing Parameters for a Unit Square
#####################################

X = [(0,0), (0,1), (1,1), (1,0)]
Square = Polygon(X)
SquareT = Triangulate(X)