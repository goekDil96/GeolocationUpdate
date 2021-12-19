# -*- coding: utf-8 -*-

# auxilium
# --------
# A Python project for an automated test and deploy toolkit - 100%
# reusable.
#
# Author:   sonntagsgesicht
# Version:  0.1.4, copyright Sunday, 11 October 2020
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from os import getcwd
from os.path import basename
from unittest import TestCase
from GeolocationUpdate.getlimit import angle_north
from GeolocationUpdate.getlimit import find_distance
from GeolocationUpdate.getlimit import cross
from GeolocationUpdate.getlimit import norm
from GeolocationUpdate.getlimit import diff
from GeolocationUpdate.getlimit import s_mul
from GeolocationUpdate.getlimit import sortIndexList

class getLimitTests(TestCase):
    def setUp(self):
        pass

    def test_sortIndexList(self):
        v1_error = "hello"
        i1_error = 2.3
        reverse_error = 3

        v1 = [(1, 7, 3), (3, 2, 8), (2, 5, 6)]
        i1 = 1
        reverse = True
    
        self.assertRaises(TypeError, sortIndexList, v1_error, i1)
        self.assertRaises(TypeError, sortIndexList, v1, i1_error)
        self.assertRaises(TypeError, sortIndexList, v1, i1, reverse_error)

        self.assertEqual(sortIndexList(v1, i1), [(3, 2, 8), (2, 5, 6), (1, 7, 3)])
        self.assertEqual(sortIndexList(v1), [(1, 7, 3), (2, 5, 6), (3, 2, 8)])
        self.assertEqual(sortIndexList(v1, i1, reverse), [(1, 7, 3), (2, 5, 6), (3, 2, 8)])
    
    def test_angle_north(self):
        v1_error = "hallo"
        v2_error = [1, 2, 3]
        v1 = [0, 0]

        self.assertRaises(TypeError, angle_north, v1_error, v1)
        self.assertRaises(ValueError, angle_north, v2_error, v1)
        # Rechter Winkel
        v2 = [1, 0]
        self.assertEqual(angle_north(v1, v2), 90.)

        # Parallel
        v2 = [0, 2]
        self.assertEqual(angle_north(v1, v2), 0.)

        # Spitzer Winkel
        v2 = [1, 1]
        self.assertEqual(angle_north(v1, v2), 45.)

        # Stumpfer Winkel (Gibt auch spitzen Winkel aus)
        v2 = [1, -1]
        self.assertEqual(angle_north(v1, v2), 135.)

        # Winkel über 180 Grad
        v3 = [-1, 0]
        self.assertEqual(angle_north(v1, v3), 270.)

    def test_find_distance(self):
        v1 = [1, 1]
        v2 = [0, 0]
        v3 = [0, 1]
        self.assertEqual(find_distance(v1, v2, v3), 1)

        v4 = [1, -1]
        self.assertEqual(find_distance(v1, v2, v4), 2 ** (1 / 2))

        v5 = [0, 0]
        self.assertEqual(find_distance(v5, v2, v3), 0)

    def test_cross(self):
        v1_error = "hallo"
        v2_error = [1]
        v1 = [1, 1, 1]
        v2 = [1, 2, 3]

        self.assertRaises(TypeError, cross, v1_error, v1)
        self.assertRaises(ValueError, cross, v2_error, v1)

        self.assertEqual(cross(v1, v2), [1, -2, 1])

    def test_norm(self):
        v1_error = "hallo"
        v2_error = [1]
        v1 = [1, 1]
        v2 = [1, 1, 1]

        self.assertRaises(TypeError, norm, v1_error)
        self.assertRaises(ValueError, norm, v2_error)

        self.assertEqual(norm(v1), 2 ** (1 / 2))
        self.assertEqual(norm(v2), 3 ** (1 / 2))

    def test_diff(self):
        v1_error = "hallo"
        v2_error = [1]
        v1 = [1, 1]
        v2 = [1, 1, 1]

        self.assertRaises(TypeError, diff, v1_error, v1)
        self.assertRaises(ValueError, diff, v2_error, v1)
        self.assertRaises(ValueError, diff, v1, v2)

        self.assertEqual(diff(v1, v1), [0, 0])
        self.assertEqual(diff(v2, v2), [0, 0, 0])

    def test_s_mul(self):
        s1_error = "hallo"
        v1_error = "hallo"
        v2_error = [1]
        s1 = 3
        v1 = [1, 1]
        v2 = [1, 1, 2]

        self.assertRaises(TypeError, s_mul, s1_error, v1)
        self.assertRaises(TypeError, s_mul, s1, v1_error)
        self.assertRaises(ValueError, s_mul, s1, v2_error)

        self.assertEqual(s_mul(s1, v1), [3, 3])
        self.assertEqual(s_mul(s1, v2), [3, 3, 6])
