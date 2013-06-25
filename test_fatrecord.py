#!/usr/bin/env python
# coding: utf-8

import unittest
import marcx
import base64
import pymarc
import unittest
 
# 00909cas a2200265   4500
# 001 000119652
# 003 DE-576
# 005 20120615084520.0
# 007 tu
# 008 850101c19uuuuuuxx    m            0ger c
# 016    $a (OCoLC)309922781
# 035    $a (DE-599)BSZ000119652
# 040    $a DE-576 $b ger $c DE-576 $e rakwb
# 041 0  $a ger
# 041 07 $a dt.
# 084    $a GL 9346 $2 rvk
# 110 2  $a Adalbert-Stifter-Institut des Landes Oberösterreich $9 g:Linz
#        $0 (DE-588)2003604-8 $0 (DE-576)19159427X
# 245 10 $a Schriftenreihe des Adalbert-Stifter-Institutes
#           des Landes Oberösterreich
# 260    $a Linz : $b Oberoesterr. Landesverl.
# 591    $a 5090, 5550: FRUB11/Sred
# 689 00 $D p $0 (DE-588)118618156 $0 (DE-576)163200580 $2 gnd
#        $a Stifter, Adalbert
# 689 0  $5 DE-576
# 785 00 $i Ab Bd. 42 u.d.T. $t Beiträge zur Stifterforschung
#        $w (DE-576)262359677
# 935    $b druck
# 936 rv $a GL 9346 $b Sekundärliteratur. $0 201559404
MARCREC = base64.b64decode("""
MDA5MDljYXMgYTIyMDAyNjUgICA0NTAwMDAxMDAxMDAwMDAwMDAzMDAwNzAwMDEwMDA1MDAxNzAwMDE3
MDA3MDAwMzAwMDM0MDA4MDA0MTAwMDM3MDE2MDAyMTAwMDc4MDM1MDAyNTAwMDk5MDQwMDAzMTAwMTI0
MDQxMDAwODAwMTU1MDQxMDAwODAwMTYzMDg0MDAxNzAwMTcxMTEwMDEwNDAwMTg4MjQ1MDA3OTAwMjky
MjYwMDAzNzAwMzcxNTkxMDAyODAwNDA4Njg5MDA2ODAwNDM2Njg5MDAxMTAwNTA0Nzg1MDA3MzAwNTE1
OTM1MDAxMDAwNTg4OTM2MDA0NTAwNTk4HjAwMDExOTY1Mh5ERS01NzYeMjAxMjA2MTUwODQ1MjAuMB50
dR44NTAxMDFjMTl1dXV1dXV4eCAgICBtICAgICAgICAgICAgMGdlciBjHiAgH2EoT0NvTEMpMzA5OTIy
NzgxHiAgH2EoREUtNTk5KUJTWjAwMDExOTY1Mh4gIB9hREUtNTc2H2JnZXIfY0RFLTU3Nh9lcmFrd2Ie
MCAfYWdlch4wNx9hZHQuHiAgH2FHTCA5MzQ2HzJydmseMiAfYUFkYWxiZXJ0LVN0aWZ0ZXItSW5zdGl0
dXQgZGVzIExhbmRlcyBPYmVyb8yIc3RlcnJlaWNoHzlnOkxpbnofMChERS01ODgpMjAwMzYwNC04HzAo
REUtNTc2KTE5MTU5NDI3WB4xMB9hU2NocmlmdGVucmVpaGUgZGVzIEFkYWxiZXJ0LVN0aWZ0ZXItSW5z
dGl0dXRlcyBkZXMgTGFuZGVzIE9iZXJvzIhzdGVycmVpY2geICAfYUxpbnogOh9iT2Jlcm9lc3RlcnIu
IExhbmRlc3ZlcmwuHiAgH2E1MDkwLCA1NTUwOiBGUlVCMTEvU3JlZB4wMB9EcB8wKERFLTU4OCkxMTg2
MTgxNTYfMChERS01NzYpMTYzMjAwNTgwHzJnbmQfYVN0aWZ0ZXIsIEFkYWxiZXJ0HjAgHzVERS01NzYe
MDAfaUFiIEJkLiA0MiB1LmQuVC4fdEJlaXRyYcyIZ2UgenVyIFN0aWZ0ZXJmb3JzY2h1bmcfdyhERS01
NzYpMjYyMzU5Njc3HiAgH2JkcnVjax5ydh9hR0wgOTM0Nh9iU2VrdW5kYcyIcmxpdGVyYXR1ci4fMDIw
MTU1OTQwNB4d""".replace("\n", ""))


class FatRecordTests(unittest.TestCase):
    def test_init(self):
        r = marcx.FatRecord()
        self.assertIsNotNone(r)

    def test_sigels_add_remove(self):
        r = marcx.FatRecord()
        self.assertTrue(hasattr(r, 'sigels'), msg='no `sigels` attribute')
        self.assertEqual(0, len(r.sigels), msg='sigel not empty on fresh record')

    def test_can_set_control_number(self):
        r = marcx.FatRecord()
        cno = '124387974'
        r.control_number = cno
        self.assertEqual(r['001'].value(), cno)
        self.assertEqual(r.control_number, cno)

    def test_constructor(self):
        obj = marcx.FatRecord()
        self.assertIsNotNone(obj)
 
    def test_superclass(self):
        obj = marcx.FatRecord()
        self.assertTrue(isinstance(obj, pymarc.Record))
 
    def test_constructor_passes_data(self):
        # data='', to_unicode=False, force_utf8=False,
        # hide_utf8_warnings=False, utf8_handling='strict'
        obj = marcx.FatRecord(data=MARCREC, to_unicode=True, force_utf8=True)
        self.assertEquals(obj.as_marc(), MARCREC)
 
    def test_add_field_fast(self):
        obj = marcx.FatRecord()
        obj.add('980', a='81723')
        self.assertEqual(['81723'], obj['980'].get_subfields('a'))
 
        obj.add('981', a='A', b='B', c='C')
        self.assertEqual(['A'], obj['981'].get_subfields('a'))
        self.assertEqual(['B'], obj['981'].get_subfields('b'))
        self.assertEqual(['C'], obj['981'].get_subfields('c'))
 
    def test_add_indicator(self):
        obj = marcx.FatRecord()
        obj.add('980', a='81723', indicators=['0', ' '])
        self.assertEqual(['0', ' '], obj['980'].indicators)
        self.assertEqual('0', obj['980'].indicator1)
        self.assertEqual(' ', obj['980'].indicator2)
 
    def test_add_two_fields(self):
        obj = marcx.FatRecord()
        obj.add('041', a='ger', indicators=['0', ' '])
        obj.add('041', a='dt.', indicators=['0', '7'])
 
        self.assertEquals(2, len(obj.get_fields('041')))
        self.assertEquals(['ger'], obj['041'].get_subfields('a'))
        self.assertEquals(['ger', 'dt.'],
            [f['a'] for f in obj.get_fields('041')])
 
        self.assertEquals([['0', ' '], ['0', '7']],
            [f.indicators for f in obj.get_fields('041')])
 
    def test_add_control_field(self):
        obj = marcx.FatRecord()
        obj.add('001', data='129')
        self.assertEqual('129', obj['001'].value())
 
        with self.assertRaises(ValueError):
            obj.add('010', data='129')
 
        with self.assertRaises(ValueError):
            obj.add('001', data='helo', c='hello')
 
    def test_accepts_strings_as_indicators(self):
        obj = marcx.FatRecord()
        obj.add('980', a='81723', indicators='0 ')
        self.assertEqual(['0', ' '], obj['980'].indicators)
        self.assertEqual('0', obj['980'].indicator1)
        self.assertEqual(' ', obj['980'].indicator2)
 
        obj.add('981', a='81723', indicators='07')
        self.assertEqual(['0', '7'], obj['981'].indicators)
        self.assertEqual('0', obj['981'].indicator1)
        self.assertEqual('7', obj['981'].indicator2)
 
    def test_does_not_ignore_invalid_indicator_strings(self):
        obj = marcx.FatRecord()
        with self.assertRaises(ValueError):
            obj.add('980', a='81723', indicators='Welcome')
 
    def test_remove_single(self):
        obj = marcx.FatRecord()
        obj.add('001', data='123')
        self.assertEquals(1, len(obj.get_fields('001')))
        obj.remove('001')
        self.assertEquals(0, len(obj.get_fields('001')))
 
    def test_remove_all(self):
        obj = marcx.FatRecord()
        obj.add('001', data='123')
        obj.add('001', data='456')
        self.assertEquals(2, len(obj.get_fields('001')))
        obj.remove('001')
        self.assertEquals(0, len(obj.get_fields('001')))
 
    def test_vs_slim_vs_record(self):        
        # w/ Record
        record = pymarc.Record()
        field = pymarc.Field(
            tag='245', 
            indicators=['0', '1'], 
            subfields=[
                'a', 'The pragmatic programmer : ', 
                'b', 'from journeyman to master /', 
                'c', 'Andrew Hunt, David Thomas.' 
            ])
        record.add_field(field)
 
        # w/ SlimRecord
        obj = marcx.FatRecord()
        obj.add('245', 
            a='The pragmatic programmer : ', 
            b='from journeyman to master /', 
            c='Andrew Hunt, David Thomas.', 
            indicators='01')
 
        self.assertEquals(len(obj.get_fields('245')), 
            len(record.get_fields('245')))
 
        self.assertEquals(
            obj.get_fields('245')[0].get_subfields('a'), 
            record.get_fields('245')[0].get_subfields('a')
        )
 
        self.assertEquals(
            obj.get_fields('245')[0].get_subfields('b'), 
            record.get_fields('245')[0].get_subfields('b')
        )
 
        self.assertEquals(
            obj.get_fields('245')[0].get_subfields('c'), 
            record.get_fields('245')[0].get_subfields('c')
        )
 
        # NOTE: this might fail, although the only difference
        # is in the subfield ordering (hashing effect)
        # self.assertEquals(
        #     obj.get_fields('245')[0].__str__(), 
        #     record.get_fields('245')[0].__str__()
        # )