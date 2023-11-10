# coding: utf-8

"""
Tests for ES marc.
"""

import unittest

import marcx
import warnings

DOC_03692895X = {u'_id': u'03692895X',
 u'_index': u'bsz',
 u'_score': 1.0,
 u'_source': {u'content': {u'001': u'03692895X',
   u'003': u'DE-576',
   u'005': u'20100313023318.0',
   u'007': u'tu',
   u'008': u'940120s1850    xx       m    000 0 lat c',
   u'016': [{u'a': u'(OCoLC)253442902', u'ind1': u' ', u'ind2': u' '}],
   u'035': [{u'a': u'(DE-599)BSZ03692895X', u'ind1': u' ', u'ind2': u' '}],
   u'040': [{u'a': u'DE-576',
     u'b': u'ger',
     u'c': u'DE-576',
     u'e': u'rakwb',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'041': [{u'a': u'lat', u'ind1': u'0', u'ind2': u' '},
    {u'a': u'lat.', u'ind1': u'0', u'ind2': u'7'}],
   u'046': [{u'2': u'DE-576', u'ind1': u' ', u'ind2': u' ', u'j': u'a19a'}],
   u'100': [{u'0': u'(DE-576)171604253',
     u'a': u'Nahmer, Friedrich Wilhelm V. D.',
     u'ind1': u'1',
     u'ind2': u' '}],
   u'245': [{u'a': u'De hydrophobia nonnulla /',
     u'c': u'Friedrich Wilhelm V. D. Nahmer',
     u'ind1': u'1',
     u'ind2': u'0'}],
   u'260': [{u'a': u'Gryphiae,', u'c': u'1850', u'ind1': u' ', u'ind2': u' '}],
   u'502': [{u'a': u'Greifswald, Univ., Diss., 1850.',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'751': [{u'4': u'uvp', u'a': u'Greifswald', u'ind1': u' ', u'ind2': u' '}],
   u'935': [{u'b': u'druck', u'ind1': u' ', u'ind2': u' '},
    {u'c': u'hs', u'ind1': u' ', u'ind2': u' '}]},
  u'meta': {u'date': u'2014-03-04'}},
 u'_type': u'title'}

DOC_091849799 = {u'_id': u'091849799',
 u'_index': u'bsz',
 u'_score': 1.8562834,
 u'_source': {u'content': {u'001': u'091849799',
   u'003': u'DE-576',
   u'005': u'20101119034051.0',
   u'007': u'tu',
   u'008': u'010619s2001    xx             00 0 eng c',
   u'010': [{u'a': u'   000103127', u'ind1': u' ', u'ind2': u' '}],
   u'016': [{u'a': u'(OCoLC)64655014', u'ind1': u' ', u'ind2': u' '}],
   u'020': [{u'9': u'0-262-03293-7',
     u'a': u'0262032937',
     u'ind1': u' ',
     u'ind2': u' '},
    {u'9': u'0-07-013151-1',
     u'a': u'0070131511',
     u'ind1': u' ',
     u'ind2': u' '},
    {u'9': u'0-262-53196-8',
     u'a': u'0262531968',
     u'ind1': u' ',
     u'ind2': u' '},
    {u'9': u'978-0-262-03293-3',
     u'a': u'9780262032933',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'024': [{u'a': u'9780262032933', u'ind1': u'3', u'ind2': u' '},
    {u'a': u'9780262531962', u'ind1': u'8', u'ind2': u' '}],
   u'035': [{u'a': u'(DE-599)BSZ091849799', u'ind1': u' ', u'ind2': u' '}],
   u'040': [{u'a': u'DE-576',
     u'b': u'ger',
     u'c': u'DE-576',
     u'e': u'rakwb',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'041': [{u'a': u'eng', u'ind1': u'0', u'ind2': u' '}],
   u'082': [{u'a': u'005.1', u'ind1': u'0', u'ind2': u' '}],
   u'084': [{u'2': u'rvk', u'a': u'ST 130', u'ind1': u' ', u'ind2': u' '},
    {u'2': u'rvk', u'a': u'ST 134', u'ind1': u' ', u'ind2': u' '}],
   u'245': [{u'a': u'Introduction to algorithms /',
     u'c': u'Thomas H. Cormen ...',
     u'ind1': u'1',
     u'ind2': u'0'}],
   u'250': [{u'a': u'2. ed.', u'ind1': u' ', u'ind2': u' '}],
   u'260': [{u'a': u'Cambridge, Mass. [u.a.] :',
     u'b': u'MIT Press [u.a.],',
     u'c': u'2001',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'300': [{u'a': u'XXI, 1180 S. :',
     u'b': u'graph. Darst.',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'591': [{u'a': u'720 ddsu/sos; 721 ddsu/sfu\u0308 ; 720 ff. (DDC): GBV/LOC',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'650': [{u'a': u'Computer',
     u'ind1': u' ',
     u'ind2': u'0',
     u'x': u'Programming'},
    {u'a': u'Computer algorithms', u'ind1': u' ', u'ind2': u'0'}],
   u'689': [{u'0': [u'(DE-588c)4200409-3', u'(DE-576)210135271'],
     u'2': u'swd',
     u'A': u's',
     u'a': u'Algorithmentheorie',
     u'ind1': u'0',
     u'ind2': u'0'},
    {u'5': u'DE-576', u'ind1': u'0', u'ind2': u' '}],
   u'700': [{u'0': [u'(DE-588a)12942661X', u'(DE-576)166909602'],
     u'a': u'Cormen, Thomas H.',
     u'd': u'1989-',
     u'ind1': u'1',
     u'ind2': u' '}],
   u'780': [{u'i': u'1. Aufl. u.d.T.',
     u'ind1': u'0',
     u'ind2': u'0',
     u't': u'Cormen, Thomas H.: Introduction to algorithms'}],
   u'935': [{u'b': u'druck', u'ind1': u' ', u'ind2': u' '}],
   u'936': [{u'0': u'200877461',
     u'a': u'ST 130',
     u'b': u'Allgemeines',
     u'ind1': u'r',
     u'ind2': u'v'},
    {u'0': u'202612511',
     u'a': u'ST 134',
     u'b': u'Algorithmen-, Komplexita\u0308tstheorie',
     u'ind1': u'r',
     u'ind2': u'v'}]},
  u'meta': {u'date': u'2014-03-04'}},
 u'_type': u'title'}


DOC_004867815 = {u'_id': u'004867815',
 u'_index': u'bsz',
 u'_score': 1.0,
 u'_source': {u'content': {u'001': u'004867815',
   u'003': u'DE-576',
   u'005': u'20110402021658.0',
   u'007': u'tu',
   u'008': u'850101s1976    xx             00 0 fre c',
   u'016': [{u'a': u'(OCoLC)02377915', u'ind1': u' ', u'ind2': u' '}],
   u'035': [{u'a': u'(DE-599)BSZ004867815', u'ind1': u' ', u'ind2': u' '}],
   u'040': [{u'a': u'DE-576',
     u'b': u'ger',
     u'c': u'DE-576',
     u'e': u'rakwb',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'041': [{u'a': u'fre', u'ind1': u'0', u'ind2': u' '},
    {u'a': u'franz.', u'ind1': u'0', u'ind2': u'7'}],
   u'082': [{u'a': u'938.01', u'ind1': u'0', u'ind2': u' '}],
   u'084': [{u'2': u'rvk', u'a': u'NH 6000', u'ind1': u' ', u'ind2': u' '}],
   u'100': [{u'0': u'(DE-576)162013574',
     u'a': u'Le\u0301vy, Edmond',
     u'ind1': u'1',
     u'ind2': u' '}],
   u'245': [{u'a': u'Athe\u0300nes devant la de\u0301faite de 404 :',
     u'b': u"histoire d'une crise ide\u0301ologique /",
     u'c': u'par Edmond Le\u0301vy',
     u'ind1': u'1',
     u'ind2': u'0'}],
   u'260': [{u'a': u'Athe\u0300nes [u.a.] :',
     u'b': u"E\u0301cole Franc\u0327. d'Athe\u0300nes,",
     u'c': u'1976',
     u'ind1': u' ',
     u'ind2': u' '}],
   u'300': [{u'a': u'IX, 339 S.', u'ind1': u' ', u'ind2': u' '}],
   u'490': [{u'a': u"Bibliothe\u0300que des E\u0301coles Franc\u0327aises d'Athe\u0300nes et de Rome ; ",
     u'ind1': u'1',
     u'ind2': u' ',
     u'v': u'225'}],
   u'591': [{u'a': u'5090: DDSU/sred', u'ind1': u' ', u'ind2': u' '}],
   u'810': [{u'a': u'E\u0301cole Franc\u0327aise',
     u'ind1': u'2',
     u'ind2': u' ',
     u't': u"Bibliothe\u0300que des Ecoles Franc\u0327aises d'Athe\u0300nes et de Rome",
     u'v': u'225',
     u'w': u'(DE-576)000529850'}],
   u'935': [{u'b': u'druck', u'ind1': u' ', u'ind2': u' '}],
   u'936': [{u'a': u'NH 6000',
     u'b': u'Peloponnesischer Krieg und Niedergang der Polis (431 - 360)',
     u'ind1': u'r',
     u'ind2': u'v',
     u'k': [u'Geschichte',
      u'Griechisch-ro\u0308mische Geschichte',
      u'Griechische Geschichte',
      u'Griechische Geschichte (500 - 338)',
      u'Peloponnesischer Krieg und Niedergang der Polis (431 - 360)']}]},
  u'meta': {u'date': u'2014-03-04'}},
 u'_type': u'title'}

class MarcDocTest(unittest.TestCase):

    def test_DOC_03692895X(self):
        with warnings.catch_warnings():
            em = marcx.marcdoc(DOC_03692895X)
        self.assertNotEqual(None, em)
        self.assertEqual(em.x245a, [u'De hydrophobia nonnulla /'])
        self.assertEqual(em.x245b, [])
        self.assertEqual(em.x100a, [u'Nahmer, Friedrich Wilhelm V. D.'])
        self.assertEqual(em.x700a, [])
        self.assertEqual(list(em.isbns()), [])

    def test_DOC_091849799(self):
        with warnings.catch_warnings():
            em = marcx.marcdoc(DOC_091849799)
        self.assertNotEqual(None, em)
        self.assertEqual(list(em.isbns()), [u'0262032937',
                                             u'0070131511',
                                             u'0262531968',
                                             u'9780262032933',
                                             u'0-262-03293-7',
                                             u'0-07-013151-1',
                                             u'0-262-53196-8',
                                             u'978-0-262-03293-3'])

        self.assertEqual(em.x700a, [u'Cormen, Thomas H.'])
        self.assertEqual(em.x935b, [u'druck'])
        self.assertEqual(em.x650x, [u'Programming'])
        self.assertEqual(em.x650x, [u'Programming'])
        self.assertEqual(em.y650x, [u'Programming'])
        self.assertEqual(em._650x, [u'Programming'])
        self.assertEqual(em.x999, [])
        self.assertEqual(em.x999yyyyy, [])

    def test_dict_functionality(self):
        with warnings.catch_warnings():
            em = marcx.marcdoc(DOC_091849799)
        self.assertEqual('bsz', em.get('_index'))
        self.assertEqual('091849799',
                          em.get('_source').get('content').get('001'))

    def test_flattened_689(self):
        with warnings.catch_warnings():
            em = marcx.marcdoc(DOC_004867815)
        self.assertEqual(5, len(em.x936k))
        self.assertEqual(em.x936, [[{u'a': u'NH 6000', u'k': [
            u'Geschichte',
            u'Griechisch-ro\u0308mische Geschichte',
            u'Griechische Geschichte',
            u'Griechische Geschichte (500 - 338)',
            u'Peloponnesischer Krieg und Niedergang der Polis (431 - 360)'],
            u'b': u'Peloponnesischer Krieg und Niedergang der Polis (431 - 360)',
            u'ind1': u'r', u'ind2': u'v'}]])

    def test_values(self):
        with warnings.catch_warnings():
            em = marcx.marcdoc(DOC_004867815)
        self.assertEqual(5, len(em.values('936k')))
        self.assertEqual(5, len(em.values('936.k')))

        self.assertEqual([u'Geschichte',
                           u'Griechisch-ro\u0308mische Geschichte',
                           u'Griechische Geschichte',
                           u'Griechische Geschichte (500 - 338)',
                           u'Peloponnesischer Krieg und Niedergang der Polis (431 - 360)'],
                           em.values('936k'))
        self.assertEqual([u'Geschichte',
                           u'Griechisch-ro\u0308mische Geschichte',
                           u'Griechische Geschichte',
                           u'Griechische Geschichte (500 - 338)',
                           u'Peloponnesischer Krieg und Niedergang der Polis (431 - 360)'],
                           em.values('936.k'))

        self.assertEqual(3, len(em.values('260.a', '260.b', '260.c')))
        self.assertEqual([u'Athe\u0300nes [u.a.] :',
                           u"E\u0301cole Franc\u0327. d'Athe\u0300nes,",
                           u'1976'],
                           em.values('260.a', '260.b', '260.c'))
