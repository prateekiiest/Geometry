"""
This file will act as a test suite for the BeatNik files.
"""

import unittest
import random

import polygon



class TestPolygon(unittest.TestCase):

    examples = [[(0,0),(0,1),(1,1),(1,0)], [(0,0),(0,1),(1,0)],
             [(0,0),(-1,0),(0,1)], [(0,0),(0,1),(1,1),(-1,-1)],
                            [(0,0),(0,2),(2,2),(-1,0)],[(0,0)]]

    def test_connected(self, next = True, clockwise = True):

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




"""
class TestSong(unittest.TestCase):

    def setUp(self):
        self.examples = [
            ['3OH!3', "Don't Trust Me", 'Clean Edit', '130 BPM', 'Dance', '', '', ''],
                ["Guns N' Roses", "It's So Easy", '', '75.29', '', '', '', '6B / Bb'],
                    ['Cake', "It's Coming Down", '', '120.00', '', '', '', '9A / Em'],
                      ['Goo Goo Dolls', 'Iris', '', '154.63', '', '', '', '10A / Bm'],
                     ['Tom Petty', "Free Fallin'", '', '84.38', '', '', '', '7B / F'],
                          ['Atreyu', 'Doomsday', '', '163.00', '', '', '', '5A / Cm'],
                               ['3 Days Grace', 'Home', '', '84 BPM', '', '', '', ''],
                         ['3 Doors Down', 'Kryptonite', '', '99 BPM', '', '', '', '']
                        ]


    def testSameSongSameData(self, trials = 1):
        'Tests initialization of Song class.'
        for i in xrange(trials):
            song_data = random.choice(self.examples)
            p = music.Song(song_data)
            q = music.Song(song_data)
            self.failUnlessEqual(p, q)

    def testSameSongDifferentData(self, insertion = '', trials = 1):
        'Tests __eq__ method of Song class.'
        'Use insertion = \'\' to test compatible data and another'
        'character (eg. \'z\') for testing incompatible data.'
        for i in xrange(trials):
            song_data = random.choice(self.examples)
            p = music.Song(song_data)
            song_data[random.randint(2,7)] = insertion
            q = music.Song(song_data)
            self.failUnlessEqual(p, q)

    def testDifferentSongs(self, trials = 1):
        'Tests __eq__ method of Song class.'
        for i in xrange(trials):
            song_data = random.choice(self.examples)
            p = music.Song(song_data)
            altered_data = [x for x in song_data]
            altered_data[0], altered_data[1] = altered_data[1], altered_data[0]
            q = music.Song(altered_data)
            self.failIfEqual(p, q)

    def testEmptySong(self, trials = 1):
        'Tests __nonzero__ method of Song class.'
        for i in xrange(trials):
            p = music.Song(['', ''] + random.choice(self.examples)[2:])
            q = music.Song(['' for i in range(8)])
            self.failIf(not p and not q)

    def testBadInitArgument(self, args = [[],
                          ['' for i in range( 4) ],
                          ['' for i in range(10)]]):
        'Tests __init__ method of Song class.'
        for arg in args:
            try:
                p = Song(arg)
            except Exception as e:
                continue
            self.failIf(True)
        return

    def testBadChangeToArgument(self, args = [-1, 9]):
        'Tests change_to method of Song class.'

        p = music.Song(self.examples[0])
        for arg in args:
            try:
                p.change_to(arg, 'No way Jose!')
            except Exception as e:
                continue
            self.failIf(True)
        return

    def testValidMerge(self, trials = 1):
        'Tests __add__ method of Song class.'
        for i in xrange(trials):
            data = random.choice(self.examples)
            p = music.Song(data)
            q = music.Song(data)
            for j in xrange(3):
               p.data[random.randint(2,7)] = ''
               p.refresh(p.data)
            try:
                r = p + q
                s = q + p
            except Exception as e:
                self.failIf(True)
        return

    # Append test to front to run if main.  Generalizes other tests.
    def GeneralArgumentError(self, args, function, instance = None):
        'Tests functions of Song class for an ArgumentError. args are inputs'
        'for function and instance is an instantiation of the parent class'
        'args should be in form [[arg]] to avoid conditions in code.'
        for arg in args:
            if not instance:
                try:
                    y = function(*arg)
                except Exception as e:
                    continue
            else:
                try:
                    instance.function(*arg)
                except Exception as e:
                    continue
            self.failIf(True)
        return

"""
if __name__ == '__main__':
    unittest.main()
