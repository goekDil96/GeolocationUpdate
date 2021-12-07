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
import numpy as np
from GeolocationUpdate.getlimit import angle_north, find_distance


class FirstUnitTests(TestCase):
    def setUp(self):
        pass

    def test_serverside(self):
        self.assertEqual(1, 1)

    def test_angle_north(self):
        # Rechter Winkel
        v1 = [0, 0]
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
