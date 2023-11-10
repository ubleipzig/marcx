# coding: utf-8

"""
Tests for DotDict with ES marc.
"""

import unittest

import marcx


class DotDictTest(unittest.TestCase):

    def test_basics(self):
        d = marcx.DotDict()
        self.assertTrue(isinstance(d, dict))

    def test_basics(self):
        doc = {'a': 'A', 'b': 'B'}
        d = marcx.DotDict(doc)
        self.assertTrue('a' in d)
        self.assertEqual(d.a, 'A')

    def test_basics(self):
        doc = {'a': 'A', 'b': {'c': {'d': ['e', 'f']}}}
        d = marcx.DotDict(doc)
        self.assertEqual(d.b.c.d[1], 'f')
