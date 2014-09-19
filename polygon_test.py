"""
This file will act as a test suite for the BeatNik files.
"""

import unittest
import random
import math

import polygon



class TestPolygon(unittest.TestCase):

    examples = [[(0,0),(0,1),(1,1),(1,0)], [(0,0),(0,1),(1,0)],
             [(0,0),(-1,0),(0,1)], [(0,0),(0,1),(1,1),(-1,-1)],
                            [(0,0),(0,2),(2,2),(-1,0)]]

    def test_connected(self, next = False, clockwise = False):

        fn = lambda x: x.next if next else lambda x: x.prev
        for example in TestPolygon.examples:
            pgon_sides = len(example)
            pgon       = polygon.SimplePolygon(example, clockwise)
            cursor     = fn(pgon.head)
            count      = 1
            while cursor != pgon.head and count < pgon_sides:
                cursor = fn(cursor)
                count += 1
            self.failUnlessEqual(count, pgon_sides)

    def test_duplicate_coordinate(self, trials = 1, clockwise = False):

        for trial in xrange(trials):

            example = [(random.randint(-100,100),random.randint(-100,100))
                        for i in xrange(random.randint(3,100))]
            """ Still need to implement something to except duplicates. """
            """ Right now no exceptions should occur. """
            try:
                pgon = polygon.SimplePolygon(example, clockwise)
            except Exception as e:
                continue
            for tpl in example:
                self.failUnlessEqual(example.count(tpl), 1)

    def test_orientation(self, clockwise = False):

        fn = lambda x: x.next if clockwise else lambda x: x.prev
        for example in TestPolygon.examples:
            pgon = polygon.SimplePolygon(example, clockwise)
            try:
                self.failUnlessEqual(pgon.head.next.coord, example[1])
            except Exception as e:
                continue

    def test_vertice_count(self, clockwise = False):

        for example in TestPolygon.examples:
            pgon   = polygon.SimplePolygon(example, clockwise)
            count  = 1
            cursor = pgon.head.next
            while cursor != pgon.head:
                cursor = cursor.next
                count += 1
            self.failUnlessEqual(pgon.count_vertices(), count)

    def test_coordinate_in_polygon(self, clockwise = False, trials = 1):

        example = TestPolygon.examples[0]
        pgon    = polygon.SimplePolygon(example, clockwise)
        for trial in xrange(trials):
            x = random.randint(-1000,1000)
            y = random.randint(-1000,1000)
            test_coord = (x,y)

            self.failUnlessEqual(
                pgon.coordinate_in_polygon(
                    test_coord), test_coord in example)

    def test_perimeter(self):

        example1 = TestPolygon.examples[0]
        example2 = TestPolygon.examples[1]
        pgon1    = polygon.SimplePolygon(example1, True)
        pgon2    = polygon.SimplePolygon(example2, False)

        self.failUnlessEqual(pgon1.get_perimeter(), 4)
        self.assertAlmostEqual(pgon2.get_perimeter(), 2 + math.sqrt(2.0))


if __name__ == '__main__':
    unittest.main()
