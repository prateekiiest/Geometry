"""
Geometry Module for Python 2.7

Things to do:

re-write is_simple in SimplePolygon
"""

"""Subclassing Vertice"""
class Vertice(object):

    def __init__(self, coordinate):
        self.coord = coordinate
        self.next  = None
        self.prev  = None

    def __repr__(self):
        return "Vertice at %s." % repr(self.coord)

"""
Polygon class
- using doubly linked lists for vertices
"""
class SimplePolygon(object):

    """Initialization of Polygon instance"""
    def __init__(self, coordinates, orientation_bool):
        """
        orientation_bool is true for clockwise, false for ccw.
        coordinates is a list of tuples denoting coordinates in
        the cartesian plane.
        The coordinates need to be listed in order of connection.
        Also, coordinates[i+1] is clockwise from coordinates[i].

        self.orientation/self.head require methods for init as
        seen below.  Note that self.head will become a vertice
        with data from coordinates[0].

        self.convex/concave_vertices are populated after some
        later methods, as with line_segments.
        """
        self.coordinates      = coordinates
        self.vertex_number    = self.count_vertices()
        self.orientation      = None
        self.head             = None
        self.line_segments    = None
        self.convex_vertices  = []
        self.concave_vertices = []

        """ Orientation initialization """
        if orientation_bool:
            self.head = self.orientate(coordinates)
        else:
            self.head = self.orientate(coordinates, False)


    def orientate(self, coordinates, clockwise = True):
        """
        This method creates a list of vertices with data from
        coordinates.  It then iterates over the list assigning
        pointers to the appropriate vertices (clockwise = next).
        """
        vertices   = [Vertice(coord) for coord in coordinates]
        poly_sides = len(vertices)
        orient_var = 1 if clockwise else -1

        for i in xrange(poly_sides):
            vertices[i % polysides].prev = vertices[(i-orient_var) % polysides]
            vertices[i % polysides].next = vertices[(i+orient_var) % polysides]
        """
        self.orientation is set to clockwise argument and self.head
        becomes the first vertice in the list.
        """
        self.orientation = clockwise
        return vertices[0]


    def count_vertices(self):
        return len(self.coordinates)


    def coordinate_in_polygon(self, coord):
        return True if coord in self.coordinates else False


    def remove_vertice(self, vertice_coord):
        """
        Conditions where removing is impossible:
        - vertice coordinate is not in Polygon
        - polygon has 3 sides (2 sides is not a polygon)
        """
        if not self.coordinate_in_polygon(vertice_coord):
            raise Exception('Vertice not in polygon')

        elif self.vertex_number == 3:
            raise Exception('Simple polygon must have three vertices')

        """
        Removing vertice makes use of a cursor.  Initializing cursor at
        self.head, we traverse the polygon until we reach the vertice
        to be removed.  We change the vertices adjacent to connect with
        eachother, and remove coordinate from self.coordinates, updating
        self.vertex_number as well.
        """
        cursor = self.head
        while cursor.coord != vertice_coord:
            cursor = cursor.next
        """ We have reached the desired vertice"""
        cursor.prev.next = cursor.next
        cursor.next.prev = cursor.prev
        """ Dealing with case where removed vertice was self.head """
        if cursor == self.head:
            self.head = cursor.next
        """ Tidying up and updating polygon attributes"""
        cursor = None
        self.data.remove(vertice_coord)
        self.vertex_number -= 1
        return


    def insert_vertice(self, insertion_point, vertice_coord):
        """
        Similar method to remove_vertice.  Locates insertion_point and
        initializes a new vertice with vertice_coord data.  We change
        the appropriate vertice connections so that the new vertice
        comes before the insertion_point in the polygon.  Updates
        polygon, and then checks if it remains simple.  If not, applies
        self.remove_vertice immediately.
        """
        if not self.coordinate_in_polygon(insertion_point):
            raise Exception('Insertion point not in polygon')
        """
        Should refactor this into another function, it is repeatedly
        occuring.
        """
        cursor = self.head
        while cursor.coord != insertion_point:
            cursor = cursor.next
        """ Updating vertice connections """
        new_vertice                        = Vertice(vertice_coord)
        new_vertice.prev, new_vertice.next = cursor.prev, cursor
        cursor.prev.next                   = new_vertice
        cursor.prev                        = new_vertice
        """ Updating polygon data"""
        cursor_index = self.coordinates.index(cursor.coord)
        self.coordinates.insert(cursor_index, vertice_coord)
        self.vertex_number += 1
        """ Checking if polygon remains simple """
        if not self.is_simple():
            self.remove(vertice_coord)
            raise Exception('Resultant polygon is not simple')
        """ Addressing case where cursor was self.head """
        if not cursor_index:
            self.head = new_vertice
        return


    def move_vertex(self, old_coord, new_coord):
        """
        Identical traversal as insert/remove_vertice.  Locates vertex,
        and updates its coordinate and self.coordinates.  It then checks
        if new polygon is simple, and will revert if not and raise an
        exception.
        """
        if not self.coordinate_in_polygon(old_coord):
            raise Exception('Vertice not in polygon')
        """ Traversal"""
        cursor = self.head
        while cursor.coord != old_coord:
            cursor = cursor.next
        """ Updating coordinates"""
        cursor.coord    = new_coord
        old_coord_index = self.coordinates.index(old_coord)
        self.coordinates[old_coord_index] = new_coord
        """ Checking if polygon remains simple """
        if not self.is_simple():
            cursor.coord = old_coord
            self.coordinates[old_coord_index] = old_coord
            raise Exception('Resultant polygon is not simple')
        return
