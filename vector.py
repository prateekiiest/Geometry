""" File for Vector Class
	Need to work on accuracy issues with some functions.
"""

class Vector(object):

	def __init__(self, coordinate):
		self.vector = coordinate
		self.label = None

	def dimension(self):
		return len(self.vector)

	def dotProduct(self, other):
		if self.dimension() != other.dimension():
			raise Exception('Invalid operation')
		return sum([x[0]*x[1] for x in zip(self.vector, other.vector)])

	def crossProduct(self, other):
		if self.dimension() != 3 or self.dimension() != other.dimension():
			raise Exception('Invalid operation')
		u1, u2, u3 = self.vector[0], self.vector[1], self.vector[2]
		v1, v2, v3 = other.vector[0], other.vector[1], other.vector[2]
		i = u2*v3 - v2*u3
		j = -1*(u1*v3 - v1*u3)
		k = u1*v2 - v1*u2
		return Vector((i, j, k))

	def tripleProduct(self, other):
		return (self.crossProduct(other)).magnitude()

	def project(self, dimension):
		if self.dimension() <= dimension:
			return Vector(tuple([0 for i in xrange(dimension)]))
		projection = [0 for i in xrange(self.dimension())]
		projection[dimension] = self.vector[dimension]
		return Vector(tuple(projection))

	def normalize(self):
		mag = self.magnitude()
		normalized = [(1.0*x)/mag for x in self.vector]
		return Vector(tuple(normalized))

	def getAngle(self, other):
		mags = self.magnitude()
		mago = other.magnitude()
		dot  = self.dotProduct(other)
		return math.degrees(math.acos((1.0*dot)/(mags*mago)))

	def orthogonal(self, other):
		return True if self.dotProduct(other) == 0 else False

	def collinear(self, other):
		if self.dotProduct(other) == self.magnitude()*other.magnitude():
			return True
		return False

	def sum(self, other):
		if self.dimension() != other.dimension():
			raise Exception('Invalid operation')
		summand = [sum(x) for x in zip(self.vector, other.vector)]
		return Vector(tuple(summand))

	def scale(self, k):
		scaled = [k*x for x in self.vector]
		return Vector(tuple(scaled))

	def difference(self, other):
		if self.dimension() != other.dimension():
			raise Exception('Invalid operation')
		difference = [x[0]-x[1] for x in zip(self.vector, other.vector)]
		return Vector(tuple(difference))

	def negate(self):
		return Vector(tuple([-x for x in self.vector]))

	def magnitude(self):
		return math.sqrt(sum([x**2 for x in self.vector]))

	def __repr__(self):
		return '%s %s' % (self.vector, self.label)