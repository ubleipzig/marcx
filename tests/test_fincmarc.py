#!/usr/bin/env python
# coding: utf-8

import marcx
import pymarc
import unittest

class FincMarcTests(unittest.TestCase):

    def test_init(self):
        r = marcx.FincMarc()
        self.assertIsNotNone(r)

    def test_sigels_add_remove(self):
        r = marcx.FincMarc()
        self.assertTrue(hasattr(r, 'sigels'), msg='no `sigels` attribute')
        self.assertEqual(0, len(r.sigels),
                         msg='sigel not empty on fresh record')

    def test_can_set_control_number(self):
        r = marcx.FincMarc()
        cno = '124387974'
        r.control_number = cno
        self.assertEqual(r['001'].value(), cno)
        self.assertEqual(r.control_number, cno)

    def test_constructor(self):
        obj = marcx.FincMarc()
        self.assertIsNotNone(obj)

    def test_superclass(self):
        obj = marcx.FincMarc()
        self.assertTrue(isinstance(obj, marcx.FatRecord))
