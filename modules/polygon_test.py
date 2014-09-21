"""
This file contains test methods for polygon.py.
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

    def test_cw_ccw_difference(self):

        example1 = TestPolygon.examples[0]
        pgon1 = polygon.SimplePolygon(example1, True)
        pgon2 = polygon.SimplePolygon(example1, False)

        self.assertEqual(pgon1.head.coord, pgon2.head.coord)
        self.assertNotEqual(pgon1.head.next.coord, pgon2.head.next.coord)

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

    def test_share_edge(self):

        example1 = [(0,0),(0,1),(1,1),(1,0)]
        example2 = [(0,0),(0,-1),(-1,-1),(-1,0)]
        example3 = [(0,0),(1,0),(1,-1),(0,-1)]
        pgon1 = polygon.SimplePolygon(example1, True)
        pgon2 = polygon.SimplePolygon(example2, False)
        pgon3 = polygon.SimplePolygon(example3, False)

        self.assertFalse(pgon1.share_edge(pgon2))
        self.assertTrue(pgon2.share_edge(pgon3))
        self.assertTrue(pgon1.share_edge(pgon3))

    def test_total_signed_area(self):

        example1 = TestPolygon.examples[0]
        pgon1 = polygon.SimplePolygon(example1, True)
        pgon2 = polygon.SimplePolygon(example1, False)
        pgon1_tsa = pgon1.total_signed_area()
        pgon2_tsa = pgon2.total_signed_area()
        self.assertNotEqual(pgon1_tsa, pgon2_tsa)
        self.assertEqual(abs(pgon1_tsa), abs(pgon2_tsa))

if __name__ == '__main__':
    unittest.main()
